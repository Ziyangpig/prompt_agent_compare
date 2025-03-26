import sys
import os

import jsonlines
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取当前文件的上一级目录（即project_root目录）
parent_dir = os.path.dirname(current_dir)

# 将langchain目录添加到sys.path中
sys.path.append(os.path.join(parent_dir,'langchain'))
sys.path.append(os.path.join(parent_dir,'langchain'))

import agent_get_start
import faiss_index

in_name="exam_demo"
prompt="fs"
rag="true"

input_path="./data/2.${in_name}_${prompt}_prepared.jsonl"
output_path="./data/3.exam_aft_agent_${model_name}_${prompt}_rag_${rag}.jsonl"


def process_item(item):
    # 使用agent处理item
    result = agent_executor.invoke({"input": input_text})
    agent_answer = result.get('output', '')
    processed_answer = get_ans(agent_answer)
    item["model_answer"] = processed_answer
    print(processed_answer)
  
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

    