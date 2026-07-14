from typing import Dict

import wikipedia
from wikipedia import DisambiguationError, PageError

wikipedia.set_lang("en")


class FactChecker:
    """Verify conversational topics using the Wikipedia API."""

    def verify_topic(self, topic: str) -> Dict[str, str]:
        """Return a short factual summary for a topic."""
        topic = topic.strip()
        if not topic:
            return {
                "topic": topic,
                "summary": "No topic was provided for fact checking.",
                "status": "invalid",
            }

        try:
            search_results = wikipedia.search(topic, results=3)
            if not search_results:
                raise PageError(topic)

            page_title = search_results[0]
            summary = wikipedia.summary(page_title, sentences=2, auto_suggest=False)
            return {"topic": page_title, "summary": summary, "status": "verified"}

        except DisambiguationError as exc:
            choice = exc.options[0] if exc.options else topic
            try:
                summary = wikipedia.summary(choice, sentences=2, auto_suggest=False)
                return {"topic": choice, "summary": summary, "status": "verified"}
            except Exception:
                return {
                    "topic": topic,
                    "summary": "The topic returned multiple options and could not be verified automatically.",
                    "status": "ambiguous",
                }

        except PageError:
            return {
                "topic": topic,
                "summary": "No verified Wikipedia summary was found for this topic.",
                "status": "not_found",
            }

        except Exception:
            return {
                "topic": topic,
                "summary": "An error occurred while checking facts on Wikipedia.",
                "status": "error",
            }
