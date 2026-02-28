
def retrieve_chunks(question, model, conn, k=5):
    query_embedding = model.encode(
        [question],
        normalize_embeddings=True
    )[0]

    vec_str = "[" + ",".join(map(str, query_embedding.tolist())) + "]"

    cur = conn.cursor()
    cur.execute("select * from match_knowledge_chunks(%s::vector(384), %s)", (query_embedding.tolist(), k))

    rows = cur.fetchall()
    cur.close()
    return rows

def build_prompt(question, retrieved_chunks):
    context = "\n\n".join(
        [f"[Source: {r[3]}]\n{r[2]}" for r in retrieved_chunks]
    )

    return f"""
You are a medical information assistant.

Answer the question ONLY using the provided context.
If the answer is not in the context, say:
"I do not have enough information from the provided sources."

Cite the source title in parentheses.

Context:
{context}

Question:
{question}
"""


def generate_answer(client, prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are a helpful medical assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content