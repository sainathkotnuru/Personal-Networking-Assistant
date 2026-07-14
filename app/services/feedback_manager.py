import json
import os
from statistics import mean
from typing import Dict, List, Optional


class FeedbackManager:
    """Manage feedback data stored in a local JSON file."""

    def __init__(self, storage_path: str = "app/storage/feedback.json") -> None:
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            self._write_data([])

    def store_feedback(self, conversation_id: str, rating: int, comment: Optional[str] = None) -> Dict[str, str]:
        """Save new feedback for a conversation."""
        feedback = self.load_feedback()
        record = {
            "feedback_id": str(os.urandom(8).hex()),
            "conversation_id": conversation_id,
            "rating": rating,
            "comment": comment or "",
        }
        feedback.append(record)
        self._write_data(feedback)
        return record

    def load_feedback(self) -> List[Dict[str, str]]:
        """Return saved feedback records."""
        try:
            with open(self.storage_path, "r", encoding="utf-8") as file_handle:
                return json.load(file_handle)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def calculate_average_rating(self) -> float:
        """Compute the average rating from all stored feedback."""
        feedback = self.load_feedback()
        ratings = [item["rating"] for item in feedback if isinstance(item.get("rating"), int)]
        return float(mean(ratings)) if ratings else 0.0

    def generate_statistics(self) -> Dict[str, object]:
        """Return basic feedback statistics."""
        feedback = self.load_feedback()
        ratings = [item["rating"] for item in feedback if isinstance(item.get("rating"), int)]
        return {
            "total_feedback": len(feedback),
            "average_rating": float(mean(ratings)) if ratings else 0.0,
            "ratings": ratings,
        }

    def _write_data(self, feedback: List[Dict[str, str]]) -> None:
        with open(self.storage_path, "w", encoding="utf-8") as file_handle:
            json.dump(feedback, file_handle, indent=2)
