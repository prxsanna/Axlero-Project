from backend.semantic_engine import calculate_metric


def test_europe_revenue():

    result = calculate_metric(
        metric="revenue",
        region="Europe"
    )

    assert result["value"] == 710000


def test_europe_cost():

    result = calculate_metric(
        metric="cost",
        region="Europe"
    )

    assert result["value"] == 495000


def test_europe_profit():

    result = calculate_metric(
        metric="profit",
        region="Europe"
    )

    assert result["value"] == 215000


def test_europe_margin():

    result = calculate_metric(
        metric="margin",
        region="Europe"
    )

    expected = 215000 / 710000

    assert abs(
        result["value"] - expected
    ) < 0.0001