from observability.timing import fields_since, timing_fields


def test_timing_fields_includes_duration_and_rate() -> None:
    assert timing_fields(duration_s=2.5, rows=100) == {
        "duration_ms": 2500,
        "rows_per_sec": 40.0,
    }


def test_timing_fields_omits_rate_when_no_rows() -> None:
    assert timing_fields(duration_s=1.0, rows=0) == {"duration_ms": 1000}


def test_timing_fields_omits_rate_when_duration_is_zero() -> None:
    assert timing_fields(duration_s=0.0, rows=10) == {"duration_ms": 0}


def test_fields_since_uses_elapsed_clock() -> None:
    fields = fields_since(started=10.0, rows=50, now=12.5)
    assert fields == {"duration_ms": 2500, "rows_per_sec": 20.0}
