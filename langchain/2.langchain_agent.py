import sys
import os

import jsonlines
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


import re
import json
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from langchain.agents import create_tool_calling_agent, create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import DashScopeEmbeddings


in_name="exam_demo"
prompt="fs"
rag="true"
model_name="deepseek-chat"

input_path=f"./data/2.{in_name}_{prompt}_prepared.jsonl"
output_path=f"./data/3.exam_aft_agent_{in_name}_{model_name}_{prompt}_rag_{rag}.jsonl"


os.environ["TAVILY_API_KEY"] = 

# os.environ["OPENAI_API_KEY"] = ""
# os.environ["OPENAI_BASE_URL"] = "https://apix.ai-gaochao.cn/v1"
# model = ChatOpenAI(model="gpt-4o", temperature=0)

os.environ["DEEPSEEK_API_KEY"] = 
os.environ["DEEPSEEK_BASE_URL"] = "https://api.deepseek.com/v1"
model = ChatDeepSeek(model="deepseek-chat", temperature=0)

def get_ans(ans):
    match = re.findall(r'.*?([A-E]+(?:[、, ]+[A-E]+)*)', ans)
    if match:
        last_match = match[-1]
        return ''.join(re.split(r'[、, ，]+', last_match))
    return ''

# %%
# prepare the retrieval tool

# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
os.environ["DASHSCOPE_API_KEY"] = 
embeddings = DashScopeEmbeddings(
    model="text-embedding-v2",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
)
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

retrieval_tool = create_retriever_tool(
    retriever,
    "medical_document_retriever",
    "A tool for retrieving information from the medical document"
)

# %%
# prepare the search tool
search_tool = TavilySearchResults(max_results=4)

tools = [retrieval_tool, search_tool]

# %%
# prepare the agent
prompt = hub.pull("hwchase17/openai-functions-agent")
print(prompt.messages)

# 使用 create_openai_functions_agent 替代 create_tool_calling_agent
agent = create_openai_functions_agent(model, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def process_item(item):
    # 使用agent处理item
    result = agent_executor.invoke({"input": item['query']})
    agent_answer = result.get('output', '')
    processed_answer = get_ans(agent_answer)
    item["model_answer"] = processed_answer
    print(processed_answer)
    return item
  
# 收集已处理项目的ID
processed_ids = set()
if os.path.exists(output_path):
    with jsonlines.open(output_path, "r") as f:
        for item in f:
            processed_ids.add(item.get("id", None))

items_to_process = []
with jsonlines.open(input_path, "r") as reader:
    for item in reader:
        item_id = item.get("id", None)
        if item_id is not None and item_id in processed_ids:
            continue
        items_to_process.append(item)


 # 多线程并行处理
with jsonlines.open(
    output_path, "a" if os.path.exists(output_path) else "w") as writer:
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(process_item, item): item for item in items_to_process
        }
        
        # 使用tqdm显示进度
        for future in tqdm(
            futures, total=len(items_to_process), desc="处理项目中"
        ):
            try:
                writer.write(future.result())
            except Exception as e:
                print(
                    f"处理项目时出错: {futures[future]['id']}. 错误: {e}"
                )

    
