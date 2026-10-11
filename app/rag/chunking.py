import json


def load_policies(file_path):
    # Open the JSON file
    with open(file_path, "r", encoding="utf-8") as file:

        # Convert JSON data into Python list/dictionaries
        policies = json.load(file)

    return policies


def create_chunks(policies):

    chunks = []

    # Take one policy at a time
    for policy in policies:

        # Split policy text into sentences
        sentences = policy["text"].split(". ")

        for index, sentence in enumerate(sentences):

            sentence = sentence.strip()

            # Skip empty text
            if not sentence:
                continue

            # Add full stop if missing
            if not sentence.endswith("."):
                sentence = sentence + "."

            chunk = {
                "chunk_id": f"{policy['policy_id']}-{policy['version']}-{index}",
                "text": sentence,

                "metadata": {
                    "policy_id": policy["policy_id"],
                    "policy_name": policy["policy_name"],
                    "version": policy["version"],
                    "effective_date": policy["effective_date"],
                    "product": policy["product"],
                    "category": policy["category"],
                    "status": policy["status"]
                }
            }

            chunks.append(chunk)

    return chunks