from together import Together

client = Together(api_key= "c3258504c91d05e34ddd4582bce9557df8a336b1c2ad21be004974c77e1e1089")

response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3-8B-Instruct-Reference",
    messages=[{"role": "user", "content": "What are some fun things to do in New York?"}],
)

print(response.choices[0].message.content)