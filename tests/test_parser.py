import pathlib
import numpy as np
import pytest

from src.parser import parse_ibw

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "Image0000.ibw"


@pytest.fixture(scope="module")
def parsed():
    return parse_ibw(FIXTURE)


def test_data_shape(parsed):
    assert parsed["data"].shape == (256, 256, 4)


def test_data_dtype(parsed):
    assert parsed["data"].dtype == np.float32


def test_scan_size_from_note(parsed):
    assert float(parsed["metadata"]["ScanSize"]) == pytest.approx(1e-05)


def test_pixel_scale_nm(parsed):
    assert parsed["pixel_scale_nm"] == pytest.approx(39.22, abs=0.005)


def test_data_units(parsed):
    assert parsed["data_units"] == "m"
