# AI Support Policy Decision Copilot

A RAG-based decision-support API that helps customer-support agents retrieve current company policies, generate grounded responses, and escalate uncertain cases for human review.

## Problem

Customer-support agents often need to search multiple policy documents before responding to customers.

Problems can occur when:
- outdated policies are used
- relevant information is difficult to find
- AI generates unsupported answers
- uncertain cases are handled automatically

This project uses Retrieval-Augmented Generation (RAG) to retrieve current policy information and generate evidence-backed responses.

## Key Features

- Semantic policy retrieval using embeddings
- ChromaDB vector database
- Active/inactive policy version filtering
- Product-specific policy filtering
- Top-K semantic retrieval
- Retrieval distance threshold
- Grounded Gemini responses
- Structured LLM output using Pydantic
- `ANSWER` or `HUMAN_REVIEW` decision
- Evidence, policy source, and version returned with every supported answer
- Fallback when relevant policy information is unavailable
- FastAPI REST API
- Evaluation test cases

## Architecture

Customer Question
→ FastAPI Request Validation
→ Query Embedding
→ ChromaDB Retrieval
→ Active Policy Filter
→ Product Filter
→ Top-K Search
→ Distance Filtering
→ Retrieved Evidence
→ Gemini Grounded Generation
→ ANSWER / HUMAN_REVIEW
→ Evidence + Source + Policy Version

## Tech Stack

- Python
- FastAPI
- Pydantic
- Google Gemini API
- Gemini Embeddings
- ChromaDB
- python-dotenv
- Uvicorn

## Example Request

POST `/ask`

```json
{
  "customer_id": 101,
  "question": "My purchase was 18 days ago. Can I still get a refund?",
  "product": "premium_subscription"
}

Example Response
{
  "answer": "Refund requests submitted after 14 days are not automatically eligible for a refund.",
  "decision": "HUMAN_REVIEW",
  "reason": "The purchase is outside the 14-day automatic eligibility window and requires manual review.",
  "evidence": [
    "Refund requests submitted after 14 days are not automatically eligible for a refund.",
    "Premium Subscription customers can request a refund within 14 days of purchase."
  ],
  "source": "Refund Policy",
  "policy_version": "2026-v2",
  "retrieval_distance": 0.4437
}

Reliability
The system does not automatically trust every retrieved result.
It applies:
- active-policy filtering
- product filtering
- retrieval-distance filtering
- grounded generation
- human-review fallback
Retrieval distance is treated as a distance metric, where a lower value represents a closer retrieved result. It is not presented as an AI confidence percentage.
Evaluation
The project was tested on 6 curated scenarios covering:
- valid refund request
- refund outside automatic window
- duplicate billing
- subscription cancellation
- suspected account access
- question not covered by the knowledge base
Result:
6/6 test scenarios passed
This result applies only to the defined evaluation set and is not a claim of universal accuracy.
Setup
Create a virtual environment and install dependencies:
pip install -r requirements.txt

Create a .env file:
GEMINI_API_KEY=your_api_key

Index policies:
python -m scripts.index_policies

Start the API:
uvicorn app.main:app --reload

Open Swagger documentation:
http://127.0.0.1:8000/docs
Project Structure

support-policy-decision-copilot/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   └── rag/
│       ├── chunking.py
│       ├── embeddings.py
│       ├── vector_store.py
│       ├── retrieval.py
│       └── generation.py
├── data/
│   └── policies.json
├── scripts/
│   ├── index_policies.py
│   ├── test_retrieval.py
│   └── test_rag.py
├── tests/
│   └── evaluation.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

What I Learned
Through this project I learned how to:
- build an end-to-end RAG pipeline
- generate and store embeddings
- perform semantic search with a vector database
- use metadata filtering for policy versioning
- handle weak or missing retrieval
- ground an LLM using retrieved evidence
- validate structured LLM responses using Pydantic
- expose a RAG workflow through FastAPI
- evaluate retrieval and decision behavior