#!/bin/bash

# Set the paths for input and output files
in_name="exam"
prompt="fs"
input_path="./data/1.${in_name}.json"
output_path="./data/2.${in_name}_multirole_${prompt}_prepared.jsonl"

# run Python scripts
python 1.prepare_data.py --input_path "$input_path" --output_path "$output_path"

# python 1.prepare_data.py --input_path ./data/1.exam.json --output_path ./data/2.exam_multirole_fs_prepared.jsonl