import datetime
import json
import os
import uuid
from typing import Dict, List, Optional


class HistoryManager:
    """Save and manage conversation history in a local JSON file."""

    def __init__(self, storage_path: str = "app/storage/history.json") -> None:
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            self._write_data([])

    def save_history(self, event_name: str, generated_prompt: str) -> Dict[str, str]:
        """Save a new conversation entry and return it."""
        history = self.load_history()
        record = {
            "history_id": str(uuid.uuid4()),
            "conversation_id": str(uuid.uuid4()),
            "event_name": event_name,
            "generated_prompt": generated_prompt,
            "date": datetime.datetime.utcnow().isoformat() + "Z",
        }
        history.append(record)
        self._write_data(history)
        return record

    def load_history(self) -> List[Dict[str, str]]:
        """Return the saved conversation history."""
        try:
            with open(self.storage_path, "r", encoding="utf-8") as file_handle:
                return json.load(file_handle)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def delete_history(self, conversation_id: str) -> bool:
        """Delete a history entry by conversation ID."""
        history = self.load_history()
        filtered = [item for item in history if item["conversation_id"] != conversation_id]
        if len(filtered) == len(history):
            return False
        self._write_data(filtered)
        return True

    def search_history(self, query: str) -> List[Dict[str, str]]:
        """Search history entries by keyword."""
        query_text = query.lower().strip()
        return [
            item
            for item in self.load_history()
            if query_text in item["event_name"].lower()
            or query_text in item["generated_prompt"].lower()
        ]

    def _write_data(self, history: List[Dict[str, str]]) -> None:
        with open(self.storage_path, "w", encoding="utf-8") as file_handle:
            json.dump(history, file_handle, indent=2)
