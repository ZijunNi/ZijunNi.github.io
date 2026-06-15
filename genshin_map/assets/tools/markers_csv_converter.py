#!/usr/bin/env python3
"""Convert between genshin_map/data/markers.js and CSV.

Usage:
  python3 ./genshin_map/assets/tools/markers_csv_converter.py to-csv --in ./genshin_map/data/markers.js --out ./genshin_map/data/markers.csv
  python3 ./genshin_map/assets/tools/markers_csv_converter.py to-js  --in ./genshin_map/data/markers.csv --out ./genshin_map/data/markers.js
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
from typing import Any

CSV_COLUMNS = [
    "id",
    "name",
    "x",
    "y",
    "min_zoom",
    "url",
    "size",
    "anchor",
    "type",
    "description",
    "location",
    "photo",
]

CSV_REQUIRED_COLUMNS = [
    "id",
    "name",
    "x",
    "y",
    "min_zoom",
    "url",
    "size",
    "anchor",
    "type",
    "description",
    "location",
]

CSV_EXPORT_ENCODING = "utf-8-sig"
CSV_IMPORT_ENCODINGS = ("utf-8-sig", "utf-8", "gb18030")

FIXED_TYPE_DEFAULTS = { # 在此处设置常用固定类型
    "city_center": {
        "min_zoom": 5,
        "url": "./assets/city_center.png",
        "size": [26.1, 40.25],
        "anchor": [13.05, 40.25],
        "level": 1,
        "tags": ["info", "panel"],
    },
    "anchor": {
        "min_zoom": 7,
        "url": "./assets/anchor.png",
        "size": [20.06, 30.62],
        "anchor": [10.03, 30.92],
        "level": 1,
        "tags": ["info", "panel"],
    },
    "mountain": {
        "min_zoom": 7,
        "url": "./assets/mountain.png",
        "size": [26,26],
        "anchor": [13, 13],
        "level": 1,
        "tags": ["info", "panel"],
    },
    "airport": {
        "min_zoom": 7,
        "url": "./assets/special_spot/jichang.png",
        "size": [45,32],
        "anchor": [22.5,16],
        "level": 1,
        "tags": ["info", "panel"],
    },
    "restaurant": {
        "min_zoom": 7,
        "url": "./assets/special_spot/canting.png",
        "size": [28,33],
        "anchor": [14,33],
        "level": 1,
        "tags": ["info", "panel"],
    },
    "market": {
        "min_zoom": 7,
        "url": "./assets/special_spot/gouwudian.png",
        "size": [32,32],
        "anchor": [16,32],
        "level": 1,
        "tags": ["info", "panel"],
    },
    "port": {
        "min_zoom": 7,
        "url": "./assets/port.png",
        "size": [32,32],
        "anchor": [16,16],
        "level": 1,
        "tags": ["info", "panel"],
    },
    }

GENERIC_DEFAULTS = {
    "min_zoom": 7,
    "url": "./assets/location.png",
    "size": [30, 30],
    "anchor": [15, 30],
    "level": 8,
    "tags": ["demo"],
}


def strip_js_comments(text: str) -> str:
    out: list[str] = []
    i = 0
    in_string = False
    quote = ""
    escaping = False

    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""

        if in_string:
            out.append(ch)
            if escaping:
                escaping = False
            elif ch == "\\":
                escaping = True
            elif ch == quote:
                in_string = False
                quote = ""
            i += 1
            continue

        if ch in ('"', "'", "`"):
            in_string = True
            quote = ch
            out.append(ch)
            i += 1
            continue

        if ch == "/" and nxt == "/":
            i += 2
            while i < len(text) and text[i] not in "\r\n":
                i += 1
            continue

        if ch == "/" and nxt == "*":
            i += 2
            while i + 1 < len(text) and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue

        out.append(ch)
        i += 1

    return "".join(out)


def extract_markers_array_literal(js_source: str) -> str:
    idx = js_source.find("window.markers")
    if idx < 0:
        raise ValueError("Cannot find 'window.markers' in JS file.")

    eq = js_source.find("=", idx)
    if eq < 0:
        raise ValueError("Cannot find '=' after 'window.markers'.")

    start = js_source.find("[", eq)
    if start < 0:
        raise ValueError("Cannot find '[' for markers array.")

    in_string = False
    quote = ""
    escaping = False
    depth = 0

    for i in range(start, len(js_source)):
        ch = js_source[i]

        if in_string:
            if escaping:
                escaping = False
            elif ch == "\\":
                escaping = True
            elif ch == quote:
                in_string = False
                quote = ""
            continue

        if ch in ('"', "'", "`"):
            in_string = True
            quote = ch
            continue

        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return js_source[start : i + 1]

    raise ValueError("Cannot find matching closing ']' for markers array.")


def quote_unquoted_object_keys(js_text: str) -> str:
    out: list[str] = []
    i = 0
    in_string = False
    quote = ""
    escaping = False

    def is_ident_start(c: str) -> bool:
        return c == "_" or c == "$" or c.isalpha()

    def is_ident_continue(c: str) -> bool:
        return c == "_" or c == "$" or c.isalnum()

    while i < len(js_text):
        ch = js_text[i]

        if in_string:
            out.append(ch)
            if escaping:
                escaping = False
            elif ch == "\\":
                escaping = True
            elif ch == quote:
                in_string = False
                quote = ""
            i += 1
            continue

        if ch in ('"', "'", "`"):
            in_string = True
            quote = ch
            out.append(ch)
            i += 1
            continue

        if ch in "{,":
            out.append(ch)
            i += 1

            ws_start = i
            while i < len(js_text) and js_text[i].isspace():
                i += 1
            out.append(js_text[ws_start:i])

            if i >= len(js_text) or not is_ident_start(js_text[i]):
                continue

            j = i + 1
            while j < len(js_text) and is_ident_continue(js_text[j]):
                j += 1

            k = j
            while k < len(js_text) and js_text[k].isspace():
                k += 1

            if k < len(js_text) and js_text[k] == ":":
                ident = js_text[i:j]
                out.append(f'"{ident}"')
                out.append(js_text[j:k])
                out.append(":")
                i = k + 1
            continue

        out.append(ch)
        i += 1

    return "".join(out)


def remove_trailing_commas(js_text: str) -> str:
    out: list[str] = []
    i = 0
    in_string = False
    quote = ""
    escaping = False

    while i < len(js_text):
        ch = js_text[i]

        if in_string:
            out.append(ch)
            if escaping:
                escaping = False
            elif ch == "\\":
                escaping = True
            elif ch == quote:
                in_string = False
                quote = ""
            i += 1
            continue

        if ch in ('"', "'", "`"):
            in_string = True
            quote = ch
            out.append(ch)
            i += 1
            continue

        if ch == ",":
            j = i + 1
            while j < len(js_text) and js_text[j].isspace():
                j += 1
            if j < len(js_text) and js_text[j] in "]}":
                i += 1
                continue

        out.append(ch)
        i += 1

    return "".join(out)


def load_markers_from_js(path: Path) -> list[dict[str, Any]]:
    source = path.read_text(encoding="utf-8")
    no_comments = strip_js_comments(source)
    arr = extract_markers_array_literal(no_comments)
    arr = quote_unquoted_object_keys(arr)
    arr = remove_trailing_commas(arr)

    try:
        data = json.loads(arr)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to parse markers array as JSON: {exc}") from exc

    if not isinstance(data, list):
        raise ValueError("markers payload is not a list.")
    return data


def parse_number(raw: str, label: str, item_id: str, fallback: float | None = None) -> float:
    text = (raw or "").strip()
    if text == "":
        if fallback is not None:
            return fallback
        raise ValueError(f"Missing {label} for row id={item_id or '(empty)'}")
    try:
        return float(text)
    except ValueError as exc:
        raise ValueError(f"Invalid {label} for row id={item_id or '(empty)'}: {raw}") from exc


def parse_pair(raw: str, label: str, item_id: str, fallback: list[float]) -> list[float]:
    text = (raw or "").strip()
    if not text:
        return [float(fallback[0]), float(fallback[1])]

    if text.startswith("[") and text.endswith("]"):
        try:
            val = json.loads(text)
            if isinstance(val, list) and len(val) >= 2:
                return [float(val[0]), float(val[1])]
        except (json.JSONDecodeError, ValueError, TypeError):
            pass

    parts = [p.strip() for p in text.split(",")]
    if len(parts) >= 2:
        try:
            return [float(parts[0]), float(parts[1])]
        except ValueError:
            pass

    raise ValueError(f"Invalid {label} pair for row id={item_id or '(empty)'}: {raw}")


def marker_type(marker: dict[str, Any]) -> str:
    info = marker.get("info") if isinstance(marker.get("info"), dict) else {}
    return str(info.get("type") or "").strip()


def pair_to_string(value: Any) -> str:
    if not isinstance(value, list) or len(value) < 2:
        return ""
    try:
        return json.dumps([float(value[0]), float(value[1])], ensure_ascii=False)
    except (ValueError, TypeError):
        return ""

def read_csv_with_fallback(csv_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    last_error: Exception | None = None

    for encoding in CSV_IMPORT_ENCODINGS:
        try:
            with csv_path.open("r", newline="", encoding=encoding) as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames or []
                rows = list(reader)
            return fieldnames, rows
        except UnicodeDecodeError as exc:
            last_error = exc

    tried = ", ".join(CSV_IMPORT_ENCODINGS)
    raise ValueError(f"CSV decode failed. Tried encodings: {tried}") from last_error


def markers_to_csv(markers_js: Path, csv_path: Path) -> None:
    markers = load_markers_from_js(markers_js)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", newline="", encoding=CSV_EXPORT_ENCODING) as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, lineterminator="\r\n")
        writer.writeheader()

        for m in markers:
            info = m.get("info") if isinstance(m.get("info"), dict) else {}
            icon = m.get("icon") if isinstance(m.get("icon"), dict) else {}

            writer.writerow(
                {
                    "id": m.get("id", ""),
                    "name": m.get("name", ""),
                    "x": m.get("x", ""),
                    "y": m.get("y", ""),
                    "min_zoom": m.get("min_zoom", ""),
                    "url": icon.get("url", ""),
                    "size": pair_to_string(icon.get("size")),
                    "anchor": pair_to_string(icon.get("anchor")),
                    "type": marker_type(m),
                    "description": info.get("description", ""),
                    "location": info.get("location", ""),
                    "photo": info.get("photo", ""),
                }
            )


def csv_to_markers(csv_path: Path, markers_js: Path) -> None:
    fieldnames, rows = read_csv_with_fallback(csv_path)

    missing_cols = [col for col in CSV_REQUIRED_COLUMNS if col not in fieldnames]
    if missing_cols:
        raise ValueError(f"CSV missing columns: {', '.join(missing_cols)}")

    updated_at = dt.date.today().isoformat()
    markers: list[dict[str, Any]] = []

    for row in rows:
        row_id = (row.get("id") or "").strip()
        name = (row.get("name") or "").strip()
        mtype = (row.get("type") or "").strip()

        if not any((v or "").strip() for v in row.values()):
            continue
        if not row_id:
            raise ValueError("CSV row has empty id")
        if not name:
            raise ValueError(f"CSV row id={row_id} has empty name")
        if not mtype:
            raise ValueError(f"CSV row id={row_id} has empty type")

        x = parse_number(row.get("x", ""), "x", row_id)
        y = parse_number(row.get("y", ""), "y", row_id)

        fixed = FIXED_TYPE_DEFAULTS.get(mtype)
        defaults = fixed if fixed is not None else GENERIC_DEFAULTS

        min_zoom = fixed["min_zoom"] if fixed else parse_number(
            row.get("min_zoom", ""), "min_zoom", row_id, float(GENERIC_DEFAULTS["min_zoom"])
        )
        icon_url = fixed["url"] if fixed else ((row.get("url") or "").strip() or GENERIC_DEFAULTS["url"])
        icon_size = fixed["size"] if fixed else parse_pair(
            row.get("size", ""), "size", row_id, GENERIC_DEFAULTS["size"]
        )
        icon_anchor = fixed["anchor"] if fixed else parse_pair(
            row.get("anchor", ""), "anchor", row_id, GENERIC_DEFAULTS["anchor"]
        )

        description = (row.get("description") or "").strip() or "占位符"
        location = (row.get("location") or "").strip() or "未填写"
        photo = (row.get("photo") or "").strip()

        info: dict[str, Any] = {
            "type": mtype,
            "description": description,
            "tags": list(defaults["tags"]),
            "updatedAt": updated_at,
            "location": location,
        }
        if photo:
            info["photo"] = photo

        marker = {
            "id": row_id,
            "name": name,
            "level": int(defaults["level"]),
            "x": x,
            "y": y,
            "min_zoom": min_zoom,
            "icon": {
                "url": icon_url,
                "size": [float(icon_size[0]), float(icon_size[1])],
                "anchor": [float(icon_anchor[0]), float(icon_anchor[1])],
            },
            "info": info,
        }
        markers.append(marker)

    markers_js.parent.mkdir(parents=True, exist_ok=True)
    content = "window.markers = " + json.dumps(markers, ensure_ascii=False, indent=2) + ";\n"
    markers_js.write_text(content, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert markers.js <-> CSV")
    sub = parser.add_subparsers(dest="command", required=True)

    p_to_csv = sub.add_parser("to-csv", help="markers.js -> CSV")
    p_to_csv.add_argument("--in", dest="input_path", required=True, help="Input markers.js")
    p_to_csv.add_argument("--out", dest="output_path", required=True, help="Output CSV")

    p_to_js = sub.add_parser("to-js", help="CSV -> markers.js")
    p_to_js.add_argument("--in", dest="input_path", required=True, help="Input CSV")
    p_to_js.add_argument("--out", dest="output_path", required=True, help="Output markers.js")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    inp = Path(args.input_path).expanduser().resolve()
    out = Path(args.output_path).expanduser().resolve()

    if args.command == "to-csv":
        markers_to_csv(inp, out)
        print(f"Converted markers.js -> CSV: {out}")
        return

    if args.command == "to-js":
        csv_to_markers(inp, out)
        print(f"Converted CSV -> markers.js: {out}")
        return

    raise RuntimeError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    main()
