import pathlib
import numpy as np
import pytest

from src.parser import parse_ibw
from src.flatten import plane_subtract

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "Image0000.ibw"


@pytest.fixture(scope="module")
def flattened():
    parsed = parse_ibw(FIXTURE)
    return plane_subtract(parsed["data"])


def test_flattened_shape(flattened):
    assert flattened.shape == (256, 256)


def test_flattened_mean_near_zero(flattened):
    assert abs(flattened.mean()) < 1e-10
