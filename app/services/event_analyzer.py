import re
from typing import List

import torch
from transformers import DistilBertModel, AutoTokenizer

STOPWORDS = {
    "and",
    "the",
    "for",
    "to",
    "with",
    "that",
    "this",
    "from",
    "your",
    "about",
    "their",
    "event",
    "networking",
    "business",
    "professional",
    "meeting",
    "conference",
    "on",
    "in",
    "of",
    "a",
    "an",
    "is",
    "are",
    "at",
    "it",
    "as",
    "be",
    "we",
    "you",
    "our",
    "it",
}


class EventAnalyzer:
    """Analyze event descriptions and extract important themes using DistilBERT."""

    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        self.model = DistilBertModel.from_pretrained("distilbert-base-uncased")
        self.model.eval()

    def extract_themes(self, text: str, top_n: int = 10) -> List[str]:
        """Return the most relevant themes from a description."""
        text = text.strip()
        if not text:
            return []

        sentence_embedding = self._encode_sentence(text)
        candidates = self._collect_candidates(text)

        ranked = sorted(
            candidates,
            key=lambda phrase: self._phrase_similarity(phrase, sentence_embedding),
            reverse=True,
        )

        themes = []
        for phrase in ranked:
            if phrase and phrase not in themes:
                themes.append(phrase)
            if len(themes) >= top_n:
                break

        return themes

    def _encode_sentence(self, text: str) -> torch.Tensor:
        tokens = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=256,
            padding=True,
        )
        with torch.no_grad():
            output = self.model(**tokens)
        return output.last_hidden_state.mean(dim=1).squeeze()

    def _collect_candidates(self, text: str) -> List[str]:
        normalized = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
        normalized = re.sub(r"\s+", " ", normalized).strip()
        words = [word for word in normalized.split() if word not in STOPWORDS and len(word) > 2]

        phrases = set()
        for phrase in re.split(r"[\n\r]+", normalized):
            snippet = " ".join([word for word in phrase.split() if word not in STOPWORDS])
            if snippet and 1 < len(snippet.split()) <= 4:
                phrases.add(snippet)

        return list(dict.fromkeys(words + list(phrases)))

    def _phrase_similarity(self, phrase: str, sentence_embedding: torch.Tensor) -> float:
        phrase_embedding = self._encode_sentence(phrase)
        return self._cosine_similarity(sentence_embedding, phrase_embedding)

    @staticmethod
    def _cosine_similarity(a: torch.Tensor, b: torch.Tensor) -> float:
        if a.norm() == 0 or b.norm() == 0:
            return 0.0
        return float(torch.nn.functional.cosine_similarity(a.unsqueeze(0), b.unsqueeze(0)).item())
