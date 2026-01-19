import re
import shutil
from pathlib import Path
import xml.etree.ElementTree as ET

from PIL import Image

def _find_dzi(dz_files_dir: Path) -> Path | None:
    # DeepZoom convention: <name>_files directory with sibling <name>.dzi
    if dz_files_dir.name.endswith("_files"):
        base = dz_files_dir.name[:-6]
        candidate = dz_files_dir.parent / f"{base}.dzi"
        if candidate.exists():
            return candidate
    # Fallback: if exactly one .dzi in parent, use it.
    dzi_files = list(dz_files_dir.parent.glob("*.dzi"))
    if len(dzi_files) == 1:
        return dzi_files[0]
    return None


def _read_dzi(dzi_path: Path) -> tuple[int, int, str]:
    tree = ET.parse(dzi_path)
    root = tree.getroot()
    tile_size = int(root.attrib.get("TileSize", 256))
    overlap = int(root.attrib.get("Overlap", 0))
    fmt = root.attrib.get("Format", "png")
    return tile_size, overlap, fmt


def _pad_and_save(src: Path, dst: Path, tile_size: int):
    with Image.open(src) as im:
        if im.size == (tile_size, tile_size):
            shutil.copyfile(src, dst)
            return

        # Pad edges to full tileSize instead of scaling; this prevents misalignment in Leaflet.
        if im.mode in ("RGBA", "LA", "P"):
            base = Image.new("RGBA", (tile_size, tile_size), (0, 0, 0, 0))
            base.paste(im.convert("RGBA"), (0, 0))
        else:
            base = Image.new("RGB", (tile_size, tile_size), (0, 0, 0))
            base.paste(im.convert("RGB"), (0, 0))
        base.save(dst)


def dz_to_xyz(dz_files_dir: Path, out_dir: Path, dzi_path: Path | None = None):
    """
    Convert DeepZoom tiles:
      <level>/<col>_<row>.<ext>
    to XYZ directory:
      <z>/<x>/<y>.<ext>

    Leaflet tileLayer expects z increases as you zoom in.
    DeepZoom level increases as you zoom in too, so z=level is fine.
    """
    if not dz_files_dir.exists():
        raise FileNotFoundError(f"DeepZoom tiles dir not found: {dz_files_dir}")

    out_dir.mkdir(parents=True, exist_ok=True)

    if dzi_path is None:
        dzi_path = _find_dzi(dz_files_dir)
    if dzi_path and dzi_path.exists():
        tile_size, overlap, _fmt = _read_dzi(dzi_path)
        if overlap != 0:
            print(f"Warning: DZI overlap={overlap} is not removed; tiles may misalign.")
    else:
        tile_size = 256
        overlap = 0

    # Match "col_row.ext"
    pat = re.compile(r'^(\d+)_([0-9]+)\.(png|jpg|jpeg|webp)$', re.IGNORECASE)

    for level_dir in sorted([p for p in dz_files_dir.iterdir() if p.is_dir()], key=lambda p: int(p.name)):
        z = int(level_dir.name)
        for f in level_dir.iterdir():
            if not f.is_file():
                continue
            m = pat.match(f.name)
            if not m:
                continue
            x = int(m.group(1))
            y = int(m.group(2))
            ext = m.group(3).lower()

            target = out_dir / str(z) / str(x)
            target.mkdir(parents=True, exist_ok=True)
            _pad_and_save(f, target / f"{y}.{ext}", tile_size)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dz", required=True, help="Path to *_files directory, e.g. assets/_dz/main_files")
    ap.add_argument("--out", required=True, help="Output dir, e.g. assets/tiles")
    ap.add_argument("--dzi", help="Optional .dzi file; if omitted tries to auto-detect")
    args = ap.parse_args()

    dz_to_xyz(Path(args.dz), Path(args.out), Path(args.dzi) if args.dzi else None)
    print("Done.")
