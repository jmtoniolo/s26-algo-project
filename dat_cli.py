#!/usr/bin/env python3

import argparse
import os
import time
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read a .dat file and print runtime plus formatted tabular data."
    )
    parser.add_argument("dat_file", help="Path to the input .dat file")
    return parser.parse_args()


def format_runtime(seconds: float) -> str:
    total_centiseconds = int(round(seconds * 100))
    centiseconds = total_centiseconds % 100
    total_seconds = total_centiseconds // 100
    secs = total_seconds % 60
    mins = (total_seconds // 60) % 60
    hours = total_seconds // 3600
    return f"{hours:02d}::{mins:02d}::{secs:02d}.{centiseconds:02d}"


def read_dat_rows(path: str) -> List[List[str]]:
    with open(path, "r", encoding="utf-8") as file:
        return [line.strip().split() for line in file if line.strip()]


def format_table(rows: List[List[str]]) -> str:
    if not rows:
        return "(no data)"

    column_count = max(len(row) for row in rows)
    headers = [f"COL{i + 1}" for i in range(column_count)]

    normalized_rows = [row + [""] * (column_count - len(row)) for row in rows]
    widths = [len(header) for header in headers]

    for row in normalized_rows:
        for idx, value in enumerate(row):
            widths[idx] = max(widths[idx], len(value))

    def render_row(values: List[str]) -> str:
        cells = [value.ljust(widths[idx]) for idx, value in enumerate(values)]
        return "| " + " | ".join(cells) + " |"

    separator = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    lines = [separator, render_row(headers), separator]
    lines.extend(render_row(row) for row in normalized_rows)
    lines.append(separator)
    return "\n".join(lines)


def main() -> int:
    args = parse_args()

    if not args.dat_file.lower().endswith(".dat"):
        raise SystemExit("Error: input file must have a .dat extension")
    if not os.path.isfile(args.dat_file):
        raise SystemExit(f"Error: file not found: {args.dat_file}")

    start = time.perf_counter()
    rows = read_dat_rows(args.dat_file)
    runtime = format_runtime(time.perf_counter() - start)

    print(f"Runtime: {runtime}")
    print("Data:")
    print(format_table(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
