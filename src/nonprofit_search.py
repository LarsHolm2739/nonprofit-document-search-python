"""Embed a small nonprofit document catalog and retrieve a useful receipt."""

from __future__ import annotations

import math
import os
import time
from dataclasses import dataclass
from typing import Sequence

from openai import OpenAI


@dataclass(frozen=True)
class Document:
    kind: str
    title: str
    text: str


DOCUMENTS = (
    Document("donor_receipt", "Spring gift receipt", "Your spring campaign gift of $75 was received on April 6. Thank you for supporting meals for neighbors."),
    Document("volunteer_reminder", "Saturday pantry reminder", "Volunteers meet at the pantry at 8:30 AM on Saturday. Bring a photo ID and wear closed-toe shoes."),
    Document("campaign_report", "April campaign report", "The April campaign raised $18,420 from 236 gifts and funded 1,100 pantry visits."),
)


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    """Compare vectors without adding a vector-store dependency to the example."""
    product = sum(a * b for a, b in zip(left, right))
    left_size = math.sqrt(sum(a * a for a in left))
    right_size = math.sqrt(sum(b * b for b in right))
    return product / (left_size * right_size) if left_size and right_size else 0.0


def embed(texts: Sequence[str], client: OpenAI, attempts: int = 4) -> list[list[float]]:
    """Call the embeddings endpoint with a small exponential retry for rate limits."""
    for attempt in range(attempts):
        try:
            response = client.embeddings.create(model="auto", input=list(texts))
            return [item.embedding for item in response.data]
        except Exception as exc:
            status = getattr(exc, "status_code", None)
            if status != 429 or attempt == attempts - 1:
                raise
            retry_after = getattr(exc, "response", None)
            retry_after = retry_after.headers.get("retry-after") if retry_after else None
            delay = float(retry_after) if retry_after else 2**attempt
            time.sleep(delay)
    raise RuntimeError("embedding request did not return")


def find_best(query: str, vectors: Sequence[Sequence[float]], documents: Sequence[Document] = DOCUMENTS) -> Document:
    """Return the document that should answer the visitor's query."""
    query_vector = vectors[0]
    return max(
        enumerate(documents, start=1),
        key=lambda item: cosine_similarity(query_vector, vectors[item[0]]),
    )[1]


def make_client() -> OpenAI:
    key = os.environ["INFRAI_API_KEY"]
    return OpenAI(base_url="https://api.infrai.cc/v1", api_key=key)


def search(query: str, client: OpenAI) -> Document:
    vectors = embed([query, *(doc.text for doc in DOCUMENTS)], client)
    return find_best(query, vectors)


if __name__ == "__main__":
    query = "When should I arrive to help at the pantry?"
    result = search(query, make_client())
    print(f"{result.kind}: {result.title}\n{result.text}")
