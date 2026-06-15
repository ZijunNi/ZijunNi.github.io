#!/usr/bin/env python3
"""Compress PNG/JPG/JPEG images to JPEG files under a target byte size.

Edit the settings below, then run from the project root:
  python3 genshin_map/assets/tools/compress_images_to_png.py

Relative paths are resolved from this script's directory.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

# =========================
# Settings
# =========================

# Input can be a folder or a single image file. Examples:
#   Path("../photos")          -> genshin_map/assets/photos
#   Path("../photos/demo.jpg") -> one image
INPUT_PATH = Path("../raw_photo")

# Output folder. It will be created automatically.
OUTPUT_PATH = Path("../photos")

# Output JPEG filename template. Available fields:
#   {stem}: original filename without extension
#   {name}: original filename with extension
#   {index}: 1-based sequence number
#   {ext}: original extension without dot
OUTPUT_FILENAME = "{stem}.jpg"

# Max output file size. Examples:
#   200 * 1024      -> 200 KiB
#   1_000_000       -> about 1 MB
SIZE_THRESHOLD_BYTES = 300 * 1024

# Whether to include images in subfolders of INPUT_PATH.
RECURSIVE = False

# Whether to replace existing output files.
OVERWRITE = False

# JPEG quality range. The script first tries the largest quality in this range
# at the original image size. If even JPEG_MIN_QUALITY is too large, it resizes
# the image proportionally and repeats the quality search.
JPEG_MIN_QUALITY = 55
JPEG_MAX_QUALITY = 92

# JPEG cannot store transparency. Transparent PNG pixels are composited over
# this RGB background before saving.
JPEG_BACKGROUND_RGB = (255, 255, 255)

# JPEG encoder options.
JPEG_PROGRESSIVE = True
JPEG_OPTIMIZE = True
JPEG_SUBSAMPLING = 2  # 0=4:4:4 best color detail, 1=4:2:2, 2=4:2:0 smaller

# Stop resizing once either side reaches this many pixels. If the JPEG is still
# larger than SIZE_THRESHOLD_BYTES, the script reports a warning for that image.
MIN_SIDE_PIXELS = 16

# Number of binary-search iterations when finding the largest fitting size.
RESIZE_SEARCH_STEPS = 18

# Number of binary-search iterations when finding the largest fitting JPEG
# quality for a given image size.
QUALITY_SEARCH_STEPS = 8


SCRIPT_DIR = Path(__file__).resolve().parent
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def resolve_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return (SCRIPT_DIR / path).resolve()


def format_size(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f"{num_bytes} B"
    if num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.1f} KiB"
    return f"{num_bytes / (1024 * 1024):.2f} MiB"


def iter_input_images(input_path: Path) -> list[Path]:
    if input_path.is_file():
        if input_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise SystemExit(f"Unsupported input image type: {input_path}")
        return [input_path]

    if not input_path.is_dir():
        raise SystemExit(f"Input path does not exist: {input_path}")

    pattern = "**/*" if RECURSIVE else "*"
    return sorted(
        path
        for path in input_path.glob(pattern)
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def has_alpha(image: Image.Image) -> bool:
    if image.mode in ("RGBA", "LA"):
        return True
    if image.mode == "P" and "transparency" in image.info:
        return True
    return False


def normalize_image_for_jpeg(image: Image.Image) -> Image.Image:
    image = ImageOps.exif_transpose(image)

    if has_alpha(image):
        rgba = image.convert("RGBA")
        background = Image.new("RGBA", rgba.size, (*JPEG_BACKGROUND_RGB, 255))
        background.alpha_composite(rgba)
        return background.convert("RGB")

    return image.convert("RGB")


def jpeg_bytes(image: Image.Image, quality: int) -> bytes:
    buffer = BytesIO()
    image.save(
        buffer,
        format="JPEG",
        quality=quality,
        optimize=JPEG_OPTIMIZE,
        progressive=JPEG_PROGRESSIVE,
        subsampling=JPEG_SUBSAMPLING,
    )
    return buffer.getvalue()


def resize_keep_ratio(image: Image.Image, scale: float) -> Image.Image:
    width, height = image.size
    new_width = max(MIN_SIDE_PIXELS, round(width * scale))
    new_height = max(MIN_SIDE_PIXELS, round(height * scale))

    if new_width == width and new_height == height:
        return image.copy()

    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def best_jpeg_for_size(image: Image.Image) -> tuple[bytes, int, bool]:
    min_quality = max(1, min(95, JPEG_MIN_QUALITY))
    max_quality = max(min_quality, min(95, JPEG_MAX_QUALITY))

    low = min_quality
    high = max_quality
    smallest_bytes = jpeg_bytes(image, min_quality)
    best_bytes = smallest_bytes
    best_quality = min_quality
    found_fit = len(smallest_bytes) <= SIZE_THRESHOLD_BYTES

    for _ in range(QUALITY_SEARCH_STEPS):
        quality = (low + high) // 2
        candidate_bytes = jpeg_bytes(image, quality)

        if len(candidate_bytes) <= SIZE_THRESHOLD_BYTES:
            best_bytes = candidate_bytes
            best_quality = quality
            found_fit = True
            low = quality + 1
        else:
            high = quality - 1

        if low > high:
            break

    return best_bytes, best_quality, found_fit


def compress_to_limit(image: Image.Image) -> tuple[bytes, tuple[int, int], int, bool]:
    original_bytes, original_quality, original_fits = best_jpeg_for_size(image)
    if original_fits:
        return original_bytes, image.size, original_quality, True

    width, height = image.size
    min_scale = max(MIN_SIDE_PIXELS / width, MIN_SIDE_PIXELS / height)
    min_scale = min(1.0, max(0.0, min_scale))

    low = min_scale
    high = 1.0
    smallest_candidate = resize_keep_ratio(image, low)
    best_bytes, best_quality, smallest_fits = best_jpeg_for_size(smallest_candidate)
    best_size = smallest_candidate.size
    best_fits = smallest_fits

    for _ in range(RESIZE_SEARCH_STEPS):
        mid = (low + high) / 2
        candidate = resize_keep_ratio(image, mid)
        candidate_bytes, candidate_quality, candidate_fits = best_jpeg_for_size(candidate)

        if candidate_fits:
            best_bytes = candidate_bytes
            best_quality = candidate_quality
            best_size = candidate.size
            best_fits = True
            low = mid
        else:
            high = mid

    return best_bytes, best_size, best_quality, best_fits


def output_file_for(src: Path, input_path: Path, output_path: Path, index: int) -> Path:
    filename = OUTPUT_FILENAME.format(
        stem=src.stem,
        name=src.name,
        index=index,
        ext=src.suffix.lstrip("."),
    )

    if input_path.is_dir():
        return output_path / src.relative_to(input_path).parent / filename
    return output_path / filename


def main() -> None:
    input_path = resolve_path(INPUT_PATH)
    output_path = resolve_path(OUTPUT_PATH)
    images = iter_input_images(input_path)

    if not images:
        raise SystemExit(f"No PNG/JPG/JPEG files found in: {input_path}")

    if len(images) > 1 and "{" not in OUTPUT_FILENAME:
        raise SystemExit(
            "OUTPUT_FILENAME must include a placeholder such as {stem} when "
            "processing multiple images."
        )

    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"Threshold: {format_size(SIZE_THRESHOLD_BYTES)}")
    print(f"Found {len(images)} image(s).")

    for index, src in enumerate(images, start=1):
        dst = output_file_for(src, input_path, output_path, index)
        dst.parent.mkdir(parents=True, exist_ok=True)

        if dst.exists() and not OVERWRITE:
            print(f"[skip] {dst} already exists")
            continue

        with Image.open(src) as opened:
            image = normalize_image_for_jpeg(opened)

        compressed, output_size, quality, within_limit = compress_to_limit(image)
        dst.write_bytes(compressed)

        status = "ok" if within_limit else "warn"
        print(
            f"[{status}] {src.name} -> {dst.name} "
            f"{image.size[0]}x{image.size[1]} -> {output_size[0]}x{output_size[1]}, "
            f"quality={quality}, "
            f"{format_size(src.stat().st_size)} -> {format_size(len(compressed))}"
        )

        if not within_limit:
            print(
                f"       Could not reach {format_size(SIZE_THRESHOLD_BYTES)} "
                f"before hitting MIN_SIDE_PIXELS={MIN_SIDE_PIXELS}."
            )


if __name__ == "__main__":
    main()
