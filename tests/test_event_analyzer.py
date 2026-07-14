from app.services.event_analyzer import EventAnalyzer


def test_extract_themes_returns_list():
    analyzer = EventAnalyzer()
    themes = analyzer.extract_themes("A conference about AI product design and career growth.")
    assert isinstance(themes, list)
    assert len(themes) > 0


def test_extract_themes_empty_text():
    analyzer = EventAnalyzer()
    themes = analyzer.extract_themes("")
    assert themes == []
