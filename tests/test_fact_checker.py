from app.services.fact_checker import FactChecker


def test_verify_topic_returns_summary():
    checker = FactChecker()
    result = checker.verify_topic("Python programming")
    assert result["status"] in {"verified", "ambiguous", "not_found", "error"}
    assert "topic" in result
    assert "summary" in result


def test_verify_topic_empty():
    checker = FactChecker()
    result = checker.verify_topic("")
    assert result["status"] == "invalid"
