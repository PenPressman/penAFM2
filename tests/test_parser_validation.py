import pathlib
import pytest

import src.parser as parser_module
from src.parser import parse_ibw

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "Image0000.ibw"


def test_corrupted_file_raises(tmp_path):
    bad = tmp_path / "bad.ibw"
    bad.write_bytes(b"\x00\xff\xde\xad\xbe\xef" * 20)
    with pytest.raises(ValueError, match="Cannot read.*as an IBW file"):
        parse_ibw(bad)


def test_truncated_file_raises(tmp_path):
    bad = tmp_path / "truncated.ibw"
    bad.write_bytes(b"\x05\x00" + b"\x00" * 10)  # valid version, body too short
    with pytest.raises(ValueError, match="Cannot read.*as an IBW file"):
        parse_ibw(bad)


def test_missing_scan_size_raises(monkeypatch):
    monkeypatch.setattr(parser_module, "_parse_note", lambda note_str: {})
    with pytest.raises(ValueError, match="missing required key 'ScanSize'"):
        parse_ibw(FIXTURE)
