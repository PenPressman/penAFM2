import pathlib
import tempfile
import pytest

from src.parser import parse_ibw
from src.flatten import plane_subtract
from src.visualize import plot_height_map

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "Image0000.ibw"


def test_plot_height_map_output():
    parsed = parse_ibw(FIXTURE)
    flattened = plane_subtract(parsed["data"])
    with tempfile.NamedTemporaryFile(suffix=".tiff", delete=False) as f:
        out = pathlib.Path(f.name)
    try:
        plot_height_map(flattened, parsed["pixel_scale_nm"], out)
        assert out.exists()
        assert out.stat().st_size > 0
    finally:
        out.unlink(missing_ok=True)
