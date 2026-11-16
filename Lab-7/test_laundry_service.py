import math

from hypothesis import given, strategies as st
from laundry_service import parse_order, weight_average, payable_charge


@given(st.text() | st.none())
def test_parse_order_no_crash(s):
    result = parse_order(s)
    assert result is None or (isinstance(result, tuple) and len(result) == 2)


@given(st.text() | st.none())
def test_weight_average_no_crash(s):
    result = weight_average(s)
    assert result is None or (isinstance(result, float) and math.isfinite(result))


@given(st.text() | st.none())
def test_payable_charge_no_crash(s):
    result = payable_charge(s)
    assert result is None or (isinstance(result, float) and math.isfinite(result))


@given(st.text(min_size=1).filter(lambda s: ':' not in s and s.strip() != ''),
       st.floats(min_value=0, max_value=100000, allow_nan=False, allow_infinity=False))
def test_valid_order(garment, weight):
    result = parse_order(f'{garment}:{weight}')
    assert result is not None
    assert result[0] == garment.strip().title()
    assert result[1] == weight


@given(st.lists(st.integers(min_value=0, max_value=1000), min_size=1, max_size=20))
def test_valid_average(values):
    result = weight_average(','.join(map(str, values)))
    assert math.isclose(result, sum(values) / len(values))


@given(st.floats(min_value=0, max_value=100000, allow_nan=False, allow_infinity=False),
       st.floats(min_value=0, max_value=100000, allow_nan=False, allow_infinity=False))
def test_valid_charge(charge, discount):
    result = payable_charge(f'{charge}|{discount}')
    assert result is not None
    assert math.isclose(result, max(charge * 1.18 - discount, 0), rel_tol=1e-9, abs_tol=1e-8)
