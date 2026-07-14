from app.services.topic_generator import TopicGenerator


def test_generate_conversation_starters():
    generator = TopicGenerator()
    output = generator.generate_conversation_starters(["product strategy", "team leadership"], count=1)
    assert isinstance(output, list)
    assert len(output) == 1
    assert output[0]


def test_generate_follow_up_questions():
    generator = TopicGenerator()
    output = generator.generate_follow_up_questions(["innovation", "creative collaboration"], count=1)
    assert isinstance(output, list)
    assert len(output) == 1
