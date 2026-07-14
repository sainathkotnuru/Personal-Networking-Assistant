import os
import tempfile

from app.services.feedback_manager import FeedbackManager


def test_feedback_store_and_average():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "feedback.json")
        manager = FeedbackManager(storage_path=path)
        record = manager.store_feedback("conv-123", 5, "Very helpful")
        assert record["conversation_id"] == "conv-123"
        assert manager.calculate_average_rating() == 5.0


def test_generate_statistics_empty():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "feedback.json")
        manager = FeedbackManager(storage_path=path)
        stats = manager.generate_statistics()
        assert stats["total_feedback"] == 0
        assert stats["average_rating"] == 0.0
