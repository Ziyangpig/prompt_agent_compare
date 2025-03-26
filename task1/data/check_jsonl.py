import json


def check_jsonl_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                if line_number > 3:
                    break
                item=json.loads(line)
                print(item['model_answer'])
            except json.JSONDecodeError as e:
                print(f"Error in line {line_number}: {str(e)}")
                # 如果你希望在发现错误时停止检查其他行，可以使用break语句
                # break


# 替换'your_file.jsonl'为你的jsonl文件路径
check_jsonl_file("/Users/ziyangzhu/code/nlp/prompt_agent/NLP-course-cuhksz/Assignments/Assignment2/task1/data/3.exam_aft_deepseek-chat.jsonl")
