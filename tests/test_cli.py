import csv
import pathlib
import shutil

import pytest

from src.cli import batch_run

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "Image0000.ibw"


@pytest.fixture()
def ibw_dir(tmp_path):
    shutil.copy(FIXTURE, tmp_path / "Image0000.ibw")
    return tmp_path


def test_summary_csv_created(ibw_dir):
    batch_run(ibw_dir)
    assert (ibw_dir / "summary.csv").exists()


def test_summary_csv_one_row(ibw_dir):
    batch_run(ibw_dir)
    with (ibw_dir / "summary.csv").open() as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 1


def test_summary_csv_columns(ibw_dir):
    batch_run(ibw_dir)
    with (ibw_dir / "summary.csv").open() as fh:
        reader = csv.DictReader(fh)
        assert set(reader.fieldnames) == {"filename", "Ra", "Rq", "Rz", "pixel_scale_nm"}


def test_summary_csv_values(ibw_dir):
    batch_run(ibw_dir)
    with (ibw_dir / "summary.csv").open() as fh:
        row = list(csv.DictReader(fh))[0]
    assert row["filename"] == "Image0000.ibw"
    assert float(row["pixel_scale_nm"]) == pytest.approx(39.22, abs=0.005)
    assert float(row["Ra"]) > 0
    assert float(row["Rq"]) >= float(row["Ra"])


def test_tiff_written(ibw_dir):
    batch_run(ibw_dir)
    assert (ibw_dir / "Image0000.tiff").exists()
    assert (ibw_dir / "Image0000.tiff").stat().st_size > 0


def test_bad_file_skipped_without_abort(ibw_dir):
    (ibw_dir / "corrupt.ibw").write_bytes(b"\x00\xff" * 30)
    rows = batch_run(ibw_dir)
    filenames = [r["filename"] for r in rows]
    assert "Image0000.ibw" in filenames
    assert "corrupt.ibw" not in filenames
