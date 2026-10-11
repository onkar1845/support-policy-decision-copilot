from app.rag.retrieval import retrieve_chunks
from app.rag.generation import generate_answer


test_cases = [
    {
        "question": "Can I get a refund after 10 days?",
        "product": "premium_subscription",
        "expected_decision": "ANSWER",
        "expected_source": "Refund Policy"
    },
    {
        "question": "My purchase was 18 days ago. Can I still get a refund?",
        "product": "premium_subscription",
        "expected_decision": "HUMAN_REVIEW",
        "expected_source": "Refund Policy"
    },
    {
        "question": "I was charged twice. What should I do?",
        "product": "premium_subscription",
        "expected_decision": "HUMAN_REVIEW",
        "expected_source": "Billing and Duplicate Charge Policy"
    },
    {
        "question": "Can I cancel my subscription now?",
        "product": "premium_subscription",
        "expected_decision": "ANSWER",
        "expected_source": "Subscription Cancellation Policy"
    },
    {
        "question": "I think someone accessed my account.",
        "product": "premium_subscription",
        "expected_decision": "HUMAN_REVIEW",
        "expected_source": "Account Security Policy"
    },
    {
        "question": "What is the CEO salary?",
        "product": "premium_subscription",
        "expected_decision": "HUMAN_REVIEW",
        "expected_source": None
    }
]

passed = 0

for index, test in enumerate(test_cases, start=1):

    chunks = retrieve_chunks(
        test["question"],
        test["product"]
    )

    # No relevant knowledge
    if not chunks:
        actual_decision = "HUMAN_REVIEW"
        actual_source = None

    else:
        result = generate_answer(
            test["question"],
            chunks
        )

        if result.requires_human:
            actual_decision = "HUMAN_REVIEW"
        else:
            actual_decision = "ANSWER"

        actual_source = chunks[0]["metadata"]["policy_name"]

    # Check expected result
    decision_correct = (
        actual_decision == test["expected_decision"]
    )

    source_correct = (
        actual_source == test["expected_source"]
    )

    if decision_correct and source_correct:
        status = "PASS"
        passed += 1
    else:
        status = "FAIL"

    print(f"\nTest {index}: {status}")
    print("Question:", test["question"])
    print("Expected decision:", test["expected_decision"])
    print("Actual decision:", actual_decision)
    print("Expected source:", test["expected_source"])
    print("Actual source:", actual_source)


print("\n--------------------")
print(f"Passed: {passed}/{len(test_cases)}")