# import mysql.connector as mysql

# --------------------------------
# 1. DATABASE CONNECTION
# --------------------------------

# connection = mysql.connect(
#     host="localhost",
#     user="root",
#     password="Kamal@2007",
#     database="new_emp"
# )

# print("Database connected successfully!")

# cursor = connection.cursor()

# --------------------------------
# 2. SELECT
# --------------------------------

# print("\n--- ALL EMPLOYEES ---")

# query = "SELECT * FROM emp"

# cursor.execute(query)

# rows = cursor.fetchall()

# for row in rows:
#     print(row)

# # --------------------------------
# # 3. INSERT
# # --------------------------------

# # print("\n--- INSERT ---")

# query = """
# INSERT INTO emp
# (emp_name, emp_id, job_role, salary, gender, age, company)
# VALUES (%s, %s, %s, %s, %s, %s, %s)
# """

# values = ('sima', 159, 'IT', 54000, 'F', 37, 'Techno')

# cursor.execute(query, values)

# connection.commit()

# print("Employee inserted successfully!")


# --------------------------------
# 4. UPDATE
# --------------------------------

# print("\n--- UPDATE ---")

# query = """
# UPDATE emp
# SET salary = %s
# WHERE emp_id = %s
# """

# values = (55000, 104)

# cursor.execute(query, values)

# connection.commit()

# print("Salary updated successfully!")


# --------------------------------
# 5. DELETE
# --------------------------------

# print("\n--- DELETE ---")

# query = "DELETE FROM emp WHERE emp_id = %s"

# values = (105,)

# cursor.execute(query, values)

# connection.commit()

# print("Employee deleted successfully!")


# --------------------------------
# 6. CLOSE CONNECTION
# --------------------------------

# cursor.close()
# connection.close()

# print("\nDatabase connection closed!")


# import os
# from dotenv import load_dotenv
# import requests

# load_dotenv()

# # response = requests.get("https://amazon.com")
# # print(response.status_code)
# # print(response.text)
# url = "https://www.google.com/search?sourceid=chrome&nseg=jiohotstar&q=jiohotstar"
# import requests

# try:
#     response = requests.get(
#         url,
#         timeout=10
#     )

#     response.raise_for_status()

#     data = response.json()

#     print(data)

# except requests.exceptions.Timeout:
#     print("Request timed out")

# except requests.exceptions.HTTPError as e:
#     print("HTTP error:", e)

# except requests.exceptions.RequestException as e:
#     print("API error:", e)

# from transformers import AutoTokenizer

# tokenizer = AutoTokenizer.from_pretrained("distilgpt2")

# text = "I love learning Generative AI."

# tokens = tokenizer.tokenize(text)

# print("Tokens:")
# print(tokens)

# token_ids = tokenizer.encode(text)

# print("\nToken IDs:")
# print(token_ids)

# decoded = tokenizer.decode(token_ids)

# print("\nDecoded text:")
# print(decoded)

# import torch 
# import torch.nn as nn

# vocab_size = 10
# embedding_dim = 4
# embedding = nn.Embedding(vocab_size, embedding_dim)
# token_ids = torch.tensor([1,3,5])
# vectors = embedding(token_ids)

# print(token_ids)
# print(vectors)

# import numpy as np

# def positional_encoding(seq_len, d_model):

#     position = np.arange(seq_len)[:, np.newaxis]

#     dimension = np.arange(d_model)[np.newaxis, :]

#     angle_rates = 1 / np.power(
#         10000,
#         (2 * (dimension // 2)) / np.float32(d_model)
#     )

#     angles = position * angle_rates

#     encoding = np.zeros((seq_len, d_model))

#     encoding[:, 0::2] = np.sin(angles[:, 0::2])

#     encoding[:, 1::2] = np.cos(angles[:, 1::2])

#     return encoding

# encoding = positional_encoding(
#     seq_len=10,
#     d_model=8
# )

# print(encoding)

# import torch 
# import torch.nn as nn
# d_model = 64
# num_heads = 8
# seq_len = 10

# x = torch.randn(1, seq_len, d_model )

# attention = nn.MultiheadAttention(
#     embed_dim = d_model,
#     num_heads= num_heads,
#     batch_first =True
# )

# casual_mask = torch.triu(torch.ones(seq_len , seq_len),
#                          diagonal=1).bool()

# o , w = attention(x , x, x, attn_mask = casual_mask)
# print(o.shape)

# from transformers import pipeline

# generator = pipeline(
#     "text-generation",
#     model="distilgpt2"
# )

# prompt = "restoring a file creates too much memory consumption"

# result = generator(
#     prompt,
#     max_new_tokens=100,
#     do_sample=True,
#     temperature= 1.5,
#     top_p=0.8
# )


# print(result[0]["generated_text"])


text = """
A giant neon flamingo flickered softly outside the diner window.
The ancient library smelled faintly of dried lavender and old parchment.
He found an origami crane tucked neatly inside his winter coat pocket.
The coffee shop playlist suddenly switched to a heavy metal track.
Clouds gathered over the mountains like a gathering of silent giants.
She noticed that the clock on the wall was running exactly backwards.
A stray cat sat on the mailbox, watching the morning traffic go by.
The rusty old key turned in the lock with a satisfying click.
A sudden gust of wind scattered the neatly stacked papers across the lawn.
The astronaut stared down at the blue marble suspended in deep darkness.
"""

import torch
chars = sorted(list(set(text)))
vocab_size = len(chars)
print(chars)
print(vocab_size)

stoi = {ch:i
        for i , ch in enumerate(chars)}

itos = {
    i:ch for i,ch in enumerate(chars)
}

def encode(text ):
    return [stoi[ch] for ch in text]

def decode(num):
    return "".join(itos[i] for i in num)

print(encode("Hello, my dog is cute"))

