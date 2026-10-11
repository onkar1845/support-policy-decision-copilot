# AI Support Policy Decision Copilot

A RAG-based decision-support API that helps customer-support agents retrieve current company policies, generate grounded responses, and route uncertain cases for human review.

## Problem

Customer-support agents often need to search multiple policy documents before responding to customers.

Problems can occur when:

- Outdated policies are used
- Relevant information is difficult to find
- AI generates unsupported answers
- Uncertain cases are handled automatically

This project uses Retrieval-Augmented Generation (RAG) to retrieve current policy information and generate evidence-backed responses.

## Key Features

- Semantic policy retrieval using embeddings
- ChromaDB vector database
- Active/inactive policy version filtering
- Product-specific policy filtering
- Top-K semantic retrieval
- Retrieval-distance filtering
- Grounded Gemini responses
- Structured LLM output using Pydantic
- `ANSWER` or `HUMAN_REVIEW` decision
- Evidence, source, and policy version in the response
- Fallback when relevant policy information is unavailable
- FastAPI REST API
- Evaluation test cases

## Architecture

```text
Customer Question
        ↓
FastAPI Request Validation
        ↓
Query Embedding
        ↓
ChromaDB Retrieval
        ↓
Active Policy Filter
        ↓
Product Filter
        ↓
Top-K Semantic Search
        ↓
Retrieval Distance Filter
        ↓
Relevant Policy Evidence
        ↓
Gemini Grounded Generation
        ↓
ANSWER / HUMAN_REVIEW
        ↓
Evidence + Source + Policy Version
```

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

**POST** `/ask`

```json
{
  "customer_id": 101,
  "question": "My purchase was 18 days ago. Can I still get a refund?",
  "product": "premium_subscription"
}
```

## Example Response

```json
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
```

## Reliability

The system does not automatically trust every retrieved result.

It applies:

- Active-policy filtering
- Product filtering
- Retrieval-distance filtering
- Grounded generation
- Human-review fallback

Retrieval distance is treated as a distance metric where a lower value represents a closer retrieved result.

It is not presented as an AI confidence percentage.

## Evaluation

The project was tested on 6 curated scenarios covering:

- Valid refund request
- Refund outside the automatic window
- Duplicate billing
- Subscription cancellation
- Suspected unauthorized account access
- Question not covered by the knowledge base

**Result:** `6/6 test scenarios passed`

This result applies only to the defined evaluation set and is not a claim of universal accuracy.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Environment File

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key
```

### 3. Index Policies

```bash
python -m scripts.index_policies
```

### 4. Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

### 5. Open Swagger API Documentation

```text
http://127.0.0.1:8000/docs
```

## Project Structure

```text
support-policy-decision-copilot/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   └── rag/
│       ├── __init__.py
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
```

## What I Learned

Through this project, I learned how to:

- Build an end-to-end RAG pipeline
- Generate and store embeddings
- Perform semantic search using a vector database
- Use metadata filtering for policy versioning
- Filter policies based on product applicability
- Handle weak or missing retrieval results
- Ground an LLM using retrieved evidence
- Validate structured LLM responses using Pydantic
- Build `ANSWER` and `HUMAN_REVIEW` decision logic
- Expose a RAG workflow through FastAPI
- Evaluate retrieval and decision behavior