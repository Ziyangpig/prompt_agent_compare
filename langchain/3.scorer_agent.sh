#!/bin/bash

# Define the paths to your input, output, and score files
in_model='deepseek-chat'
prompt="fs"
rag="true"

input_file="./data/3.exam_aft_agent_${in_model}_${prompt}_rag_${rag}.jsonl"
wrong_ans_path="./data/4.wrong_ans_agent_${in_model}_${prompt}_rag_${rag}.json"
score_file="./data/4.score_agent_${in_model}_${prompt}_rag_${rag}.json"

python 3.score_agent.py --input_path "$input_file" --wrong_ans_path "$wrong_ans_path" --score_path "$score_file"

# python 3.scorer.py --input_path ./data/3.exam_aftgpt.jsonl --wrong_ans_path ./data/4.wrong_ans.json --score_path ./data/4.score.json

