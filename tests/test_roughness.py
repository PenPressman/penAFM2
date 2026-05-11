import pathlib
import pytest

from src.parser import parse_ibw
from src.flatten import plane_subtract
from src.roughness import compute_roughness

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "Image0000.ibw"

NM = 1e-9


@pytest.fixture(scope="module")
def roughness():
    parsed = parse_ibw(FIXTURE)
    flattened = plane_subtract(parsed["data"])
    return compute_roughness(flattened)


def test_ra_positive(roughness):
    assert roughness["Ra"] > 0


def test_rq_positive(roughness):
    assert roughness["Rq"] > 0


def test_rq_ge_ra(roughness):
    assert roughness["Rq"] >= roughness["Ra"]


def test_values_in_nm_range(roughness):
    for key, value in roughness.items():
        assert 0.01 * NM <= value <= 100 * NM, (
            f"{key} = {value / NM:.4f} nm is outside [0.01, 100] nm"
        )
