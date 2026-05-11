import argparse
import csv
import logging
import pathlib

from .parser import parse_ibw
from .flatten import plane_subtract
from .roughness import compute_roughness
from .visualize import plot_height_map

log = logging.getLogger(__name__)

_CSV_FIELDS = ["filename", "Ra", "Rq", "Rz", "pixel_scale_nm"]


def batch_run(directory):
    """Process all .ibw files in *directory*.

    For each file: parse → flatten → roughness → plot (TIFF saved alongside
    the source file). Writes summary.csv into *directory*. Files that fail
    to parse are logged as warnings and skipped; the run continues.

    Returns a list of row dicts for the files that succeeded.
    """
    directory = pathlib.Path(directory)
    ibw_files = sorted(directory.glob("*.ibw"))

    if not ibw_files:
        log.warning("No .ibw files found in %s", directory)

    rows = []
    for path in ibw_files:
        try:
            parsed = parse_ibw(path)
            flattened = plane_subtract(parsed["data"])
            roughness = compute_roughness(flattened)
            plot_height_map(flattened, parsed["pixel_scale_nm"],
                            path.with_suffix(".tiff"))
            rows.append({
                "filename": path.name,
                "Ra": roughness["Ra"],
                "Rq": roughness["Rq"],
                "Rz": roughness["Rz"],
                "pixel_scale_nm": parsed["pixel_scale_nm"],
            })
            log.info("OK  %s", path.name)
        except Exception as exc:
            log.warning("SKIP %s — %s", path.name, exc)

    csv_path = directory / "summary.csv"
    with csv_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=_CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    log.info("Wrote %s (%d/%d files)", csv_path, len(rows), len(ibw_files))
    return rows


def main():
    parser = argparse.ArgumentParser(
        description="Batch-process IBW AFM files: flatten, roughness, plot."
    )
    parser.add_argument("--dir", required=True,
                        help="Directory containing .ibw files to process")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    batch_run(args.dir)


if __name__ == "__main__":
    main()
