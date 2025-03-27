#!/bin/bash

# Set the path to the Python script
python_script="../langchain_datagen_multithread.py"
max_workers=10
# set parameter
keys_path="../gpt3keys.txt"


in_name="exam_demo"
prompt="fs"
rag="True"

model_name="gpt-4o"
base_url="https://apix.ai-gaochao.cn/v1"
# deepseek
model_name="deepseek-chat"
base_url="https://api.deepseek.com/v1"


input_path="./data/2.${in_name}_${prompt}_prepared.jsonl"
output_path="./data/3.exam_aft_${in_name}_${model_name}_${prompt}_rag_${rag}.jsonl"

python "$python_script" --model_name "$model_name" --keys_path "$keys_path" --input_path "$input_path" --output_path "$output_path" --max_workers $max_workers --base_url $base_url --rag $rag

# python ../langchain_datagen_multithread.py --model_name deepseek-chat --keys_path ../gpt3keys.txt --input_path ./data/2.exam_multirole_fs_prepared.jsonl --output_path ./data/3.exam_aftgpt_mr.jsonl --max_workers 10
