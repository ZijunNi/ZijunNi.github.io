#!/usr/bin/env python3

# 与目前的整个坐标系相配合的使用方法：
# 确保assets文件夹下存在一张尺寸为20000 × 16000像素的地图全图（whole.png），然后运行此脚本生成瓦片并更新tiles.json。
# 在项目根目录下执行：
# python3 genshin_map/assets/tools/one_click_tiles.py --image genshin_map/assets/whole.png --tile-size 256
# 这会生成 genshin_map/assets/tiles 目录，并更新 genshin_map/tiles.json 中的相关字段。
# 注意：实际的可缩放范围和真实存在的瓦片级别已经解耦，在tiles.json中的zoom字段可以单独配置最大最小的缩放范围，而不受生成的瓦片级别限制（但不能超过自然的最大级别）。如果需要调整生成的瓦片级别范围，可以修改代码中FIXED_TILE_MIN_ZOOM和FIXED_TILE_MAX_ZOOM常量。

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

# 在此处修改最大和最小的缩放级别
FIXED_TILE_MIN_ZOOM: int | None = 5
FIXED_TILE_MAX_ZOOM: int | None = 8


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Missing tool: {name}. Please install it first.")


def image_size(path: Path) -> tuple[int, int]:
    w = int(subprocess.check_output(["vipsheader", "-f", "width", str(path)]).strip())
    h = int(subprocess.check_output(["vipsheader", "-f", "height", str(path)]).strip())
    return w, h


def calc_max_zoom(w: int, h: int, tile_size: int) -> int:
    max_dim = max(w, h)
    if max_dim <= tile_size:
        return 0
    return max(0, math.ceil(math.log2(max_dim / tile_size)))


def parse_screen(value: str) -> tuple[int, int]:
    m = re.match(r"^\s*(\d+)\s*[xX]\s*(\d+)\s*$", value)
    if not m:
        raise SystemExit(f"Invalid --screen format: {value}. Use WIDTHxHEIGHT, e.g. 1920x1080.")
    return int(m.group(1)), int(m.group(2))


def fit_zoom_for_screen(
    w: int,
    h: int,
    max_zoom: int,
    screen_w: int,
    screen_h: int,
    overscan: float,
) -> float:
    # Find zoom where image covers the screen (slightly larger via overscan).
    scale_needed = max(screen_w / w, screen_h / h) * overscan
    if scale_needed <= 0:
        return float(max_zoom)
    return max_zoom + math.log2(scale_needed)


def swap_xy_tiles(src_dir: Path, dst_dir: Path) -> None:
    # vips dzsave --layout google writes z/x/y but x=row, y=col.
    # Swap to z/col/row for Leaflet (x=col, y=row).
    dst_dir.mkdir(parents=True, exist_ok=True)

    for item in src_dir.iterdir():
        if item.is_file():
            shutil.copy2(item, dst_dir / item.name)

    for zdir in src_dir.iterdir():
        if not zdir.is_dir():
            continue
        for xdir in zdir.iterdir():
            if not xdir.is_dir():
                continue
            x = xdir.name
            for f in list(xdir.iterdir()):
                if not f.is_file():
                    continue
                y = f.stem
                ext = f.suffix
                target = dst_dir / zdir.name / y / f"{x}{ext}"
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(f), str(target))


def update_tiles_json(
    path: Path,
    width: int,
    height: int,
    tile_size: int,
    tile_max_zoom: int,
    tile_min_zoom: int,
    suffix: str,
    zoom_min: int | None,
    zoom_max: int | None,
) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))

    image = data.setdefault("image", {})
    image["width"] = width
    image["height"] = height

    tiles = data.setdefault("tiles", {})
    tiles["tileSize"] = tile_size
    tiles["minZoom"] = tile_min_zoom
    tiles["maxZoom"] = tile_max_zoom
    tiles["tms"] = False
    tiles["urlTemplate"] = f"./assets/tiles/{{z}}/{{x}}/{{y}}{suffix}"

    if zoom_min is not None or zoom_max is not None:
        zoom = data.setdefault("zoom", {})
        if zoom_min is not None:
            zoom["min"] = zoom_min
        if zoom_max is not None:
            zoom["max"] = zoom_max

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def expected_tile_counts(w: int, h: int, tile_size: int, max_zoom: int, z: int) -> tuple[int, int]:
    scale = 2 ** (max_zoom - z)
    w_z = math.ceil(w / scale)
    h_z = math.ceil(h / scale)
    tiles_x = math.ceil(w_z / tile_size)
    tiles_y = math.ceil(h_z / tile_size)
    return tiles_x, tiles_y


def make_blank_tile(path: Path, tile_size: int, suffix: str) -> None:
    suf = suffix.lower()
    if suf in (".png", ".webp"):
        img = Image.new("RGBA", (tile_size, tile_size), (0, 0, 0, 0))
    else:
        img = Image.new("RGB", (tile_size, tile_size), (0, 0, 0))
    img.save(path)


def fill_missing_tiles(
    out_dir: Path,
    w: int,
    h: int,
    tile_size: int,
    min_zoom: int,
    max_zoom: int,
    suffix: str,
) -> None:
    blank = out_dir / f"_blank{suffix}"
    if not blank.exists():
        make_blank_tile(blank, tile_size, suffix)

    for z in range(min_zoom, max_zoom + 1):
        tiles_x, tiles_y = expected_tile_counts(w, h, tile_size, max_zoom, z)
        zdir = out_dir / str(z)
        for x in range(tiles_x):
            xdir = zdir / str(x)
            xdir.mkdir(parents=True, exist_ok=True)
            for y in range(tiles_y):
                tile = xdir / f"{y}{suffix}"
                if not tile.exists():
                    shutil.copy2(blank, tile)

    blank.unlink(missing_ok=True)


def prune_zoom_levels(out_dir: Path, min_zoom: int, max_zoom: int) -> None:
    for item in out_dir.iterdir():
        if not item.is_dir():
            continue
        if not item.name.isdigit():
            continue
        z = int(item.name)
        if z < min_zoom or z > max_zoom:
            shutil.rmtree(item)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="One-click tiling for genshin_map (vips dzsave + screen-fit zoom)."
    )
    ap.add_argument(
        "--image",
        default="genshin_map/assets/whole.jpg",
        help="Input image path.",
    )
    ap.add_argument(
        "--out",
        default="genshin_map/assets/tiles",
        help="Tiles output directory.",
    )
    ap.add_argument(
        "--tiles-json",
        default="genshin_map/tiles.json",
        help="tiles.json path to update.",
    )
    ap.add_argument("--tile-size", type=int, default=256, help="Tile size in pixels.")
    ap.add_argument(
        "--suffix",
        default=".png",
        help="Tile filename suffix, e.g. .png or .jpg.",
    )
    ap.add_argument("--overlap", type=int, default=0, help="Tile overlap in pixels.")
    ap.add_argument(
        "--skip-blanks",
        type=int,
        default=0,
        help="Skip tiles nearly equal to background (0 disables skipping).",
    )
    ap.add_argument(
        "--screen",
        default="1920x1080",
        help="Target desktop size for fit (WIDTHxHEIGHT).",
    )
    ap.add_argument(
        "--overscan",
        type=float,
        default=1.08,
        help="Fit overscan ratio (>1 means slightly larger than screen).",
    )
    ap.add_argument(
        "--fit",
        choices=["min", "max", "none"],
        default="min",
        help="Fit zoom level to screen: min=limit zoomed-out view, max=limit zoomed-in view.",
    )
    ap.add_argument(
        "--no-swap-xy",
        action="store_true",
        help="Do not swap x/y indices after dzsave.",
    )
    ap.add_argument(
        "--no-fill-blanks",
        action="store_true",
        help="Do not fill missing tiles with blank images.",
    )
    ap.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not remove existing tiles output directory.",
    )
    ap.add_argument(
        "--no-update-json",
        action="store_true",
        help="Do not update tiles.json.",
    )
    args = ap.parse_args()

    require_tool("vips")
    require_tool("vipsheader")

    image_path = Path(args.image)
    out_dir = Path(args.out)
    tiles_json = Path(args.tiles_json)

    if not image_path.exists():
        raise SystemExit(f"Input image not found: {image_path}")

    screen_w, screen_h = parse_screen(args.screen)
    w, h = image_size(image_path)
    natural_max_zoom = calc_max_zoom(w, h, args.tile_size)
    tile_max_zoom = natural_max_zoom
    tile_min_zoom = 0

    if FIXED_TILE_MAX_ZOOM is not None:
        tile_max_zoom = max(0, min(FIXED_TILE_MAX_ZOOM, natural_max_zoom))
    if FIXED_TILE_MIN_ZOOM is not None:
        tile_min_zoom = max(0, FIXED_TILE_MIN_ZOOM)
    if tile_min_zoom > tile_max_zoom:
        raise SystemExit(
            f"Invalid fixed zoom range: min={tile_min_zoom} > max={tile_max_zoom}"
        )

    if not args.no_clean and out_dir.exists():
        shutil.rmtree(out_dir)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_out = Path(tmp) / "tiles_raw"
        tmp_out.mkdir(parents=True, exist_ok=True)
        run(
            [
                "vips",
                "dzsave",
                str(image_path),
                str(tmp_out),
                "--layout",
                "google",
                "--tile-size",
                str(args.tile_size),
                "--overlap",
                str(args.overlap),
                "--skip-blanks",
                str(args.skip_blanks),
                "--suffix",
                args.suffix,
            ]
        )
        if args.no_swap_xy:
            out_dir.mkdir(parents=True, exist_ok=True)
            for item in tmp_out.iterdir():
                shutil.move(str(item), str(out_dir / item.name))
        else:
            swap_xy_tiles(tmp_out, out_dir)

    if FIXED_TILE_MIN_ZOOM is not None or FIXED_TILE_MAX_ZOOM is not None:
        prune_zoom_levels(out_dir, tile_min_zoom, tile_max_zoom)

    if not args.no_fill_blanks:
        fill_missing_tiles(
            out_dir,
            w,
            h,
            args.tile_size,
            tile_min_zoom,
            tile_max_zoom,
            args.suffix,
        )

    zoom_min = tile_min_zoom
    zoom_max = tile_max_zoom

    if args.fit != "none":
        fit_zoom = fit_zoom_for_screen(
            w, h, tile_max_zoom, screen_w, screen_h, args.overscan
        )
        fit_zoom_int = max(0, min(tile_max_zoom, math.ceil(fit_zoom)))
        if args.fit == "min":
            if FIXED_TILE_MIN_ZOOM is None:
                tile_min_zoom = fit_zoom_int
                zoom_min = fit_zoom_int
        else:
            if FIXED_TILE_MAX_ZOOM is None:
                zoom_max = fit_zoom_int

    if not args.no_update_json:
        if not tiles_json.exists():
            raise SystemExit(f"tiles.json not found: {tiles_json}")
        update_tiles_json(
            tiles_json,
            w,
            h,
            args.tile_size,
            tile_max_zoom,
            tile_min_zoom,
            args.suffix,
            zoom_min,
            zoom_max,
        )

    print("Done.")


if __name__ == "__main__":
    main()
