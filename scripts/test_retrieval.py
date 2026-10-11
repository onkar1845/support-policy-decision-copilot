from app.rag.retrieval import retrieve_chunks


question = "I was charged twice. What should I do?"
product = "premium_subscription"

# question = "What is the CEO's salary?"

results = retrieve_chunks(question, product)

print(results)