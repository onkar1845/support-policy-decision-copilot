from fastapi import FastAPI

from app.schemas import SupportRequest, SupportResponse
from app.rag.retrieval import retrieve_chunks
from app.rag.generation import generate_answer


app = FastAPI(
    title="AI Support Policy Decision Copilot"
)


@app.post("/ask", response_model=SupportResponse)
def ask_policy(request: SupportRequest):

    # 1. Retrieve relevant active policy chunks
    retrieved_chunks = retrieve_chunks(
        request.question,
        request.product
    )

    # 2. No reliable policy found
    if not retrieved_chunks:
        return SupportResponse(
            answer="Relevant policy information was not found.",
            decision="HUMAN_REVIEW",
            reason="No sufficiently relevant active policy was found.",
            evidence=[],
            source=None,
            policy_version=None,
            retrieval_distance=None
        )

    # 3. Generate grounded structured answer
    result = generate_answer(
        request.question,
        retrieved_chunks
    )

    # 4. Convert LLM result into business decision
    if result.requires_human:
        decision = "HUMAN_REVIEW"
    else:
        decision = "ANSWER"

    # Best retrieved chunk
    best_chunk = retrieved_chunks[0]

    # Keep all retrieved evidence used by the LLM
    evidence = []

    for chunk in retrieved_chunks:
        evidence.append(chunk["text"])

    # 5. Final API response
    return SupportResponse(
        answer=result.answer,
        decision=decision,
        reason=result.reason,
        evidence=evidence,
        source=best_chunk["metadata"]["policy_name"],
        policy_version=best_chunk["metadata"]["version"],
        retrieval_distance=best_chunk["distance"]
    )