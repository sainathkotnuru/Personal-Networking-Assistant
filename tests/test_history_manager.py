import os
import tempfile

from app.services.history_manager import HistoryManager


def test_history_save_and_load():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "history.json")
        manager = HistoryManager(storage_path=path)
        record = manager.save_history("Test Event", "Test prompt")
        assert record["event_name"] == "Test Event"
        loaded = manager.load_history()
        assert len(loaded) == 1
        assert loaded[0]["history_id"] == record["history_id"]


def test_delete_history():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "history.json")
        manager = HistoryManager(storage_path=path)
        record = manager.save_history("Test Event", "Test prompt")
        deleted = manager.delete_history(record["conversation_id"])
        assert deleted is True
        assert manager.load_history() == []
