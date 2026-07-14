from typing import List

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class TopicGenerator:
    """Generate conversation starters and networking suggestions using GPT-2."""

    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self.model = AutoModelForCausalLM.from_pretrained("gpt2")
        self.model.eval()
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def generate_conversation_starters(self, themes: List[str], count: int = 3) -> List[str]:
        """Generate a list of conversation starter sentences based on themes."""
        prompt = self._build_prompt("networking conversation starter", themes)
        return self._generate_text(prompt, count, max_length=80)

    def generate_follow_up_questions(self, themes: List[str], count: int = 2) -> List[str]:
        """Generate follow-up questions to continue the conversation."""
        prompt = self._build_prompt("follow-up question", themes)
        return self._generate_text(prompt, count, max_length=60)

    def generate_networking_suggestions(self, themes: List[str], count: int = 2) -> List[str]:
        """Generate practical networking suggestions for the event."""
        prompt = self._build_prompt("networking suggestion", themes)
        return self._generate_text(prompt, count, max_length=70)

    def _build_prompt(self, goal: str, themes: List[str]) -> str:
        if themes:
            theme_text = ", ".join(themes)
            return f"Create a polite {goal} for a professional event focusing on {theme_text}."
        return f"Create a polite {goal} for a professional networking event."

    def _generate_text(self, prompt: str, count: int, max_length: int) -> List[str]:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        generated = self.model.generate(
            **inputs,
            max_length=len(inputs["input_ids"][0]) + max_length,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.8,
            num_return_sequences=count,
            no_repeat_ngram_size=2,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        results = []
        for sequence in generated:
            text = self.tokenizer.decode(sequence, skip_special_tokens=True)
            cleaned = self._clean_generated_text(text, prompt)
            if cleaned:
                results.append(cleaned)
            if len(results) >= count:
                break

        if not results:
            results = [prompt]
        return results

    def _clean_generated_text(self, text: str, prompt: str) -> str:
        cleaned = text.replace(prompt, "").strip()
        cleaned = cleaned.replace("\n", " ")
        if not cleaned:
            return ""

        if "." in cleaned:
            cleaned = cleaned.split(".")[0] + "."
        return cleaned.strip()
