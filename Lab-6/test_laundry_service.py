import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status


def test_within_included_weight():
    assert extra_weight_charge("regular", 4, "standard", False) == 0


def test_standard_extra_weight():
    assert extra_weight_charge("regular", 8, "standard", False) == 90


def test_member_allowance():
    assert extra_weight_charge("delicate", 6, "standard", True) == 30


def test_express_charge():
    assert extra_weight_charge("regular", 8, "express", False) == 150


def test_heavy_express_charge():
    assert extra_weight_charge("regular", 16, "express", False) == 825



def test_unknown_garment():
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge("shoes", 3, "standard", False)


def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -1, "standard", False)


def test_order_acceptable():
    assert order_acceptable(10, 20, False) is True


def test_delicate_order_limit():
    assert order_acceptable(10, 6, True) is False


def test_heavy_order_rejected():
    assert order_acceptable(26, 2, False) is False


def test_dropoff_accepted():
    assert dropoff_status(120, True, True) == "accepted"

def test_dropoff_rejected():
    assert dropoff_status(50, False, True) == "rejected"

def test_heavy_standard_charge():
    assert extra_weight_charge("bedding", 20, "standard", True) == 540


def test_dropoff_late():
    assert dropoff_status(45, False, False) == "late"
