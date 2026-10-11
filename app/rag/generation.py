from pydantic import BaseModel
from google.genai import types
from app.config import client


class GenerationResult(BaseModel):
    answer: str
    requires_human: bool
    reason: str


def generate_answer(question, retrieved_chunks):

    if not retrieved_chunks:
        return None

    context_parts = []

    for chunk in retrieved_chunks:
        metadata = chunk["metadata"]

        context_parts.append(
            f"Policy: {metadata['policy_name']}\n"
            f"Version: {metadata['version']}\n"
            f"Evidence: {chunk['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a customer support policy assistant.

Use ONLY the policy context below.

Set requires_human to true when:
- the customer's case is outside an automatic policy rule,
- the policy says the case is not automatically eligible,
- the policy requires manual/human review,
- or the evidence is insufficient or uncertain.

Otherwise set requires_human to false.

Do not invent company rules.

Policy Context:
{context}

Customer Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=GenerationResult
        )
    )

    return GenerationResult.model_validate_json(response.text)