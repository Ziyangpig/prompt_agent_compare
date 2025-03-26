import json
import argparse

prompt = '''
你作为资深执业药师考试专家（Pharmaceutical Care Specialist, PCS），需严格遵循《中国药典》、《临床用药指南》、《药学综合知识与技能》、《药事管理与法规》、及药学专业知识进行分析。
请一步步仔细慎重思考，并按以下专业流程处理试题：

1. **题型识别与考点定位**
   - 明确本题属于（药理/药剂/法规/临床决策/临床用药/）
   - 明确本题 question_type 属于（最佳选择题/配伍选择题/综合分析选择题/多项选择题），
   - 关联2015-2024年真题高频考点数据库
   
   针对不同的类型，采用以下不同策略
    题型	 正确选项数	典型考查内容	答题策略
    最佳选择题	1	单一知识点记忆	直接排除法，聚焦关键词
    配伍选择题	1	知识点关联与区分	先解决明确匹配项，再处理模糊项
    综合分析选择题	1（每题）	临床推理与综合应用	结合病例整体分析，避免孤立看问题
    多项选择题	≥2	复杂知识体系全面性	使用“分类排除法”，标注存疑选项

2. **知识提取与交叉验证**
   • 关键概念：提取题干中3个核心术语（如：首过效应/治疗窗/DDD值）
   • 法规依据：若涉及药事管理，需引用《药品管理法》第X章第Y条或其他相关法规
   • 数值验证：剂量计算需双重核对《临床剂量速查手册》

3. **选项分析矩阵**
   | 选项 | 合理性 | 常见错误类型 | 相关指南条款 |
   |------|--------|--------------|--------------|

4. **决策树推演**
   → 若为配伍禁忌题：
       1) 检查pH相容性 
       2) 验证溶媒选择（NS/GS）
       3) 输注速度影响因子
   → 若为ADR案例分析：
       1) 应用Naranjo量表评估
       2) 肝肾功能代谢路径分析

请按以下格式输出：
【问题解构】
• 核心考点：...[标注考试大纲条目号]
• 关键陷阱：...[识别题干迷惑点]

【专业分析】
1. 药理机制：...[含首过效应/蛋白结合率等参数]
2. 临床考量：...[特殊人群调整方案]
3. 法规关联：...[GMP/GSP相关要求]

【选项评估】 
A) ✓ 正确：...[支持性文献]
B) ✗ 错误：...[典型认知误区]
C) ✗ 错误：...[与USP标准冲突处]

【结论】 
正确答案：选项X（置信度95%） 
需复核：...[如需实验室数据验证]

下面是一道{question_type}，请先按以上步骤详细分析问题，最后给出选项。
{question}
{option}
'''

def generate_query(data):
    chatgpt_query = prompt
    question = data['question']
    option = '\n'.join([k+'. '+v for k,v in data['option'].items() if v != ''])
    chatgpt_query = chatgpt_query.format_map({'question':question,'option':option,'question_type':data['question_type']})
    return chatgpt_query


def Prepare_data(args):
    data = []
    # 读取上传的JSON文件
    with open(args.input_path, encoding='utf-8') as f:
        data = json.load(f)

    print(f"len:{len(data)}")
    # 根据要求转换
    jsonl_data = []


    for id, item in enumerate(data):
        jsonl_data.append(
            {
                "id":id,
                "query": generate_query(item),
                "model_answer": "",
                "question_type": item['question_type'],
                "groundtruth": item['answer']
            }
        )

    # 将转换后的数据保存为JSONL文件
    with open(args.output_path, "w", encoding="utf-8") as file:
        for entry in jsonl_data:
            file.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    print(f"Prepare finished, output to '{args.output_path}'")
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Prepare data for OpenAIGPT generation")
    parser.add_argument("--input_path", type=str, required=True, help="Path to the input JSON file.")
    parser.add_argument("--output_path", type=str, required=True, help="Path to the output JSONL file.")
    args = parser.parse_args()
    Prepare_data(args)
