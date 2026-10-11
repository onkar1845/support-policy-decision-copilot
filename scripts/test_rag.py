from app.rag.retrieval import retrieve_chunks
from app.rag.generation import generate_answer


question = "My purchase was 18 days ago. Can I still get a refund?"
product = "premium_subscription"

# 1. Retrieve relevant policy chunks
retrieved_chunks = retrieve_chunks(question, product)

print("Retrieved chunks:", len(retrieved_chunks))


# 2. If no reliable policy was found
if not retrieved_chunks:

    decision = "HUMAN_REVIEW"
    answer = "Relevant policy information was not found."

    print("\nDecision:")
    print(decision)

    print("\nAnswer:")
    print(answer)

else:

    # 3. Generate grounded structured response
    result = generate_answer(question, retrieved_chunks)

    # 4. Decide whether human review is required
    if result.requires_human:
        decision = "HUMAN_REVIEW"
    else:
        decision = "ANSWER"

    # Best retrieved evidence
    best_chunk = retrieved_chunks[0]

    print("\nDecision:")
    print(decision)

    print("\nAnswer:")
    print(result.answer)

    print("\nReason:")
    print(result.reason)

    print("\nEvidence:")
    print(best_chunk["text"])

    print("\nSource:")
    print(best_chunk["metadata"]["policy_name"])

    print("\nPolicy Version:")
    print(best_chunk["metadata"]["version"])

    print("\nDistance:")
    print(best_chunk["distance"])