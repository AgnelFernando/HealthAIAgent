
def create_embeddings(client, text):
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
        dimensions=384,  
    )
    return resp.data[0].embedding

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