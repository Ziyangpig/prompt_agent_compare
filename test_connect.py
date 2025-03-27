# from openai import OpenAI

# client = OpenAI(api_key="sk-f3084ab37eb34c789c726662029f5eab", base_url="https://api.deepseek.com")

# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": "Hello"},
#     ],
#     stream=False
# )

# print(response.choices[0].message.content)

from langchain_community.embeddings import DashScopeEmbeddings
import os
os.environ["DASHSCOPE_API_KEY"] = 'sk-688d4d088f2742dc9051785bbe2dc6a5'
embeddings = DashScopeEmbeddings(
    model="text-embedding-v2",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
)

text = "This is a test document."

query_result = embeddings.embed_query(text)
print(query_result)