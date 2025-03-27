#!/bin/bash

# Define the paths to your input, output, and score files
in_model='deepseek-chat'
prompt="fs"
rag="true"

input_file="./data/3.exam_aft_${in_model}_${prompt}_rag_${rag}.jsonl"
wrong_ans_path="./data/4.wrong_ans_${in_model}_${prompt}_rag_${rag}.json"
score_file="./data/4.score_${in_model}_${prompt}_rag_${rag}.json"

python 3.scorer.py --input_path "$input_file" --wrong_ans_path "$wrong_ans_path" --score_path "$score_file"

# python 3.scorer.py --input_path ./data/3.exam_aftgpt_mr.jsonl --wrong_ans_path ./data/4.wrong_ans_mr.json --score_path ./data/4.score_mr.json

