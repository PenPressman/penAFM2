import numpy as np
import igor2.binarywave as bw


def parse_ibw(path):
    """Load an IBW file and return a dict with data and metadata."""
    raw = bw.load(path)
    wave = raw["wave"]
    header = wave["wave_header"]

    data = wave["wData"].astype(np.float32)

    note_bytes = wave.get("note", b"")
    note_str = note_bytes.decode("latin-1") if isinstance(note_bytes, bytes) else note_bytes
    metadata = _parse_note(note_str)

    data_units_raw = header.get("dataUnits", [b""])
    if isinstance(data_units_raw, (list, np.ndarray)):
        data_units = data_units_raw[0]
    else:
        data_units = data_units_raw
    if isinstance(data_units, bytes):
        data_units = data_units.decode("latin-1").rstrip("\x00")

    sfa = header["sfA"]

    return {
        "data": data,
        "metadata": metadata,
        "data_units": data_units,
        "sfA": sfa,
        "pixel_scale_nm": float(sfa[0]) * 1e9,
    }


def _parse_note(note_str):
    """Parse \r-delimited key:value pairs from an IBW wave note."""
    result = {}
    for line in note_str.split("\r"):
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result
