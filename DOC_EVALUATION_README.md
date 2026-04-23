# 文档评估功能使用说明

## 概述

本功能用于评估图文相间的讲解文档（Markdown 格式），支持多维度评分和综合评分。

## 评估维度

根据 `eval_suite/doc_evaluation_rubric.json` 定义的**八个维度**：

### 文本类维度（type: text）

1. **解题步骤的正确性和完整性** (correctness_and_completeness)
   - 类型：text（仅评估文字）
   - 评分：0-5分
   - 参考信息：使用原题的 `format_answer` 字段作为标准答案参考

2. **讲解的逻辑连贯性** (logical_coherence)
   - 类型：text（仅评估文字）
   - 评分：0-5分

3. **讲解的易懂性和教学效果** (understandability_and_teaching_effect)
   - 类型：text（仅评估文字）
   - 评分：0-5分

4. **排版和视觉呈现的清晰度** (layout_and_visual_clarity)
   - 类型：text（仅评估文字）
   - 评分：0-5分

### 图文协同类维度（type: text_diagram / text_diagram_aa）

5. **图示与题目的匹配度** (diagram_match)
   - 类型：text_diagram（综合评估文字和图片，并与原题对比）
   - 评分：0-5分
   - 评估方式：**每个scene图片单独与原题示意图进行对比评估**，所有scene的分数通过几何平均得出该维度的最终分数
   - 参考信息：使用原题的 `img`（原示意图）和 `img_caption`（图片描述）字段作为参考标准

6. **图文协同的流畅性** (text_diagram_synergy)
   - 类型：text_diagram_aa（综合评估文字和图片，不与原题对比）
   - 评分：0-5分
   - 评估方式：评估图片与文字讲解的配合程度，包括引用明确性、位置邻近性、时机契合度等
   - 特点：**不使用原题参考信息**，只评估生成的文档本身的图文协同质量

### 图片独立评估类维度（type: diagram）

7. **图片元素布局质量** (element_layout_quality)
   - 类型：diagram（仅评估图片）
   - 评分：0-5分
   - 评估方式：**每张图片单独评估**，不传入文档文字内容，评估元素布局、尺寸协调性、重叠遮挡等，所有图片的分数通过几何平均得出该维度的最终分数

### 图片一致性评估类维度（type: diagram_aa）

8. **视觉一致性** (visual_consistency)
   - 类型：diagram_aa（仅评估图片）
   - 评分：0-5分
   - 评估方式：**所有图片与第一张图片对比**，不传入文档文字内容，评估绘图风格、配色方案、符号系统等的统一性，所有对比的分数通过几何平均得出该维度的最终分数
   - 特殊处理：如果只有一张图片，自动得5分（完美一致性）

**综合得分**：所有维度分数的几何平均值

### 评估类型说明

- **type: text** - 只传入文档的文字内容进行评估
- **type: text_diagram** - 传入文档的文字内容和图片，每张图与原题图对比，使用原题参考信息，分数取几何平均
- **type: text_diagram_aa** - 传入文档的文字内容和图片，**不传入原题图和原题参考信息**，只评估文档本身，分数取几何平均
- **type: diagram** - 只传入图片（不传入文字），每张图独立评估，分数取几何平均
- **type: diagram_aa** - 只传入图片（不传入文字），所有图与第一张图对比，分数取几何平均（第一张图作为基准自动得5分）

## 使用方法

### 1. 评估单个文档

```bash
python evaluate.py \
  --eval_type doc \
  --file_path "output/with_img_kimi/problem_6_physics_g12/doc/solution.md" \
  --output_folder "output/doc_evaluation" \
  --model_doc "Kimi-K25" \
  --retry_limit 3
```

### 2. 批量评估目录（查找所有包含 solution.md 文件的子目录）

```bash
python evaluate.py \
  --eval_type doc \
  --file_path "output/with_img_kimi" \
  --output_folder "output/doc_evaluation" \
  --model_doc "Kimi-K25" \
  --bulk_evaluate \
  --combine
```

**说明**: 此命令会遍历 `output/with_img_kimi` 目录及其所有子目录，自动找到包含 `solution.md` 文件的目录（在根目录或 `doc/` 子目录中），对每个找到的文档进行评估。

### 2.1 并发批量评估（加速处理）

```bash
python evaluate.py \
  --eval_type doc \
  --file_path "output/with_img_kimi" \
  --output_folder "output/doc_evaluation" \
  --model_doc "Kimi-K25" \
  --bulk_evaluate \
  --combine \
  --max_workers 4
```

**说明**:
- 使用 `--max_workers` 参数指定并发进程数（默认为4）
- 使用 `--max_workers 0` 自动使用CPU核心数
- 多个进程会并发评测不同的文档，通过文件锁机制自动避免重复评测
- 特别适合评测大量文档时使用，可显著提升速度

**并发安全性**：
- ✅ 使用文件锁（`fcntl.flock`）确保进度文件的原子读写
- ✅ 使用任务声明机制（`claim_task`）避免多进程重复评测同一文档
- ✅ 每个进程独立保存评测结果，互不干扰
- ✅ 支持多台机器同时运行（共享输出目录时）

**并发示例**：
```bash
# 使用8个并发进程
python evaluate.py \
  --eval_type doc \
  --file_path "output/with_img_kimi" \
  --output_folder "output/doc_evaluation" \
  --model_doc "Kimi-K25" \
  --bulk_evaluate \
  --max_workers 8

# 自动使用所有CPU核心
python evaluate.py \
  --eval_type doc \
  --file_path "output/with_img_kimi" \
  --output_folder "output/doc_evaluation" \
  --model_doc "Kimi-K25" \
  --bulk_evaluate \
  --max_workers 0
```

### 3. 评估目录（自动在目录或 doc/ 子目录中查找 solution.md 文件）

```bash
python evaluate.py \
  --eval_type doc \
  --file_path "output/with_img_kimi/problem_6_physics_g12" \
  --output_folder "output/doc_evaluation" \
  --model_doc "Kimi-K25"
```

**说明**: 此命令会在 `problem_6_physics_g12` 目录中查找 `solution.md` 文件，优先在根目录查找，如果没有则在 `doc/` 子目录中查找。

### 4. 使用自定义评分标准

```bash
python evaluate.py \
  --eval_type doc \
  --file_path "path/to/document.md" \
  --output_folder "output" \
  --model_doc "Kimi-K25" \
  --rubric_path "custom_rubric.json"
```

### 5. 使用原题数据进行评估（提供参考信息）

当题目目录名遵循 `problem_{index}_{subject}_{grade}` 格式（如 `problem_6_physics_g12`）时，可以通过 `--problem_data_path` 参数指定题目数据 JSON 文件，系统会自动：

1. 从目录名提取题目索引（如示例中的 `6`）
2. 从 JSON 文件中加载第 6 个题目（从 0 开始计数）
3. 提取原题的 `img`（原示意图）、`img_caption`（图片描述）、`format_answer`（标准答案）字段
4. 在评估时将这些参考信息提供给模型：
   - **图示与题目的匹配度** 维度：会同时输入原题示意图和图片描述，用于对比解题文档中的图示是否准确
   - **解题步骤的正确性和完整性** 维度：会提供标准解题步骤和答案，用于判断解题过程的准确性

**单个题目评估示例**：
```bash
python evaluate.py \
  --eval_type doc \
  --file_path "output/with_img_kimi_test/problem_6_physics_g12" \
  --output_folder "output/doc_evaluation3" \
  --model_doc "Kimi-K25" \
  --problem_data_path "data/science_problem/science-g12_samples.json"
```

**批量评估示例**：
```bash
python evaluate.py \
  --eval_type doc \
  --file_path "/inspire/hdd/project/ai4education/bishuzhen-CZXS24220022/edubench/TheoremExplainAgent/output/exp_gemini-3-pro-preview" \
  --output_folder "output/exp_gemini-3-pro-preview_result" \
  --model_doc "gemini-3-pro-preview" \
  --bulk_evaluate \
  --combine \
  --problem_data_path "/inspire/hdd/project/ai4education/bishuzhen-CZXS24220022/edubench/TheoremExplainAgent/data/testset/selected.json" \
  --max_workers 20
```

**说明**：
- `--problem_data_path` 参数是可选的，如果不提供，评估仍会正常进行，只是缺少原题参考信息
- 题目数据文件应该是包含题目数组的 JSON 文件，每个题目应包含 `img`、`img_caption`、`format_answer` 等字段
- 系统会根据目录名自动匹配题目索引，无需手动指定
- 对于批量评估，系统会自动缓存已加载的题目数据，避免重复读取文件

## 参数说明

- `--eval_type doc`：指定评估类型为文档评估
- `--file_path`：文档路径或目录路径（必需）
- `--output_folder`：评估结果输出目录（必需）
- `--model_doc`：使用的模型，默认 `Kimi-K25`
- `--rubric_path`：评分标准 JSON 文件路径（可选，默认使用 `eval_suite/doc_evaluation_rubric.json`）
- `--retry_limit`：每个维度评估失败后的重试次数（可选，默认3次）
- `--bulk_evaluate`：批量评估模式，遍历所有子目录
- `--combine`：将所有评估结果合并到一个 JSON 文件
- `--reset_progress`：清除之前的进度，从头开始评估（可选）
- `--problem_data_path`：题目数据 JSON 文件路径（可选），用于提供原题参考信息（原示意图、标准答案等）
- `--max_workers`：并发进程数（可选，默认4）
  - 设置为 1：顺序执行（无并发）
  - 设置为 N (N>1)：使用 N 个并发进程
  - 设置为 0：自动使用CPU核心数

## 断点续传功能

### 功能说明

评估过程支持**自动断点续传**，即使评估过程中断（手动停止、网络错误、程序崩溃等），再次运行时会自动从上次中断的地方继续，不会重复评估已完成的文档。

### 工作原理

1. **实时保存**: 每完成一个文档的评估，立即保存结果文件
2. **进度跟踪**: 在 `output_folder` 中创建 `evaluation_progress.json` 记录已完成的文档
3. **自动恢复**: 重新运行时自动检查进度文件，跳过已完成的文档
4. **结果合并**: 最终合并所有已保存的结果（包括之前完成的）
5. **并发安全**: 使用文件锁（`fcntl.flock`）和任务声明机制确保多进程并发时不会重复评测

### 使用示例

#### 顺序执行示例

```bash
# 第一次运行（评估了3个文档后中断）
python evaluate.py \
  --eval_type doc \
  --file_path "output/with_img_kimi" \
  --output_folder "output/doc_evaluation" \
  --bulk_evaluate \
  --combine
# 输出:
# [1/5] Evaluating problem_0_math_g12...
# [2/5] Evaluating problem_1_math_g12...
# [3/5] Evaluating problem_2_math_g12...
# ^C (用户中断)

# 再次运行（自动从第4个开始）
python evaluate.py \
  --eval_type doc \
  --file_path "output/with_img_kimi" \
  --output_folder "output/doc_evaluation" \
  --bulk_evaluate \
  --combine
# 输出:
# Found 3 completed evaluations. Resuming from checkpoint...
#   - problem_0_math_g12
#   - problem_1_math_g12
#   - problem_2_math_g12
# Processing 5 directories (already completed: 3)
# [1/5] Skipping problem_0_math_g12 (already completed)
# [2/5] Skipping problem_1_math_g12 (already completed)
# [3/5] Skipping problem_2_math_g12 (already completed)
# [4/5] Evaluating problem_6_physics_g12...
# [5/5] Evaluating problem_2_physics_g12...

# 清除进度重新开始
python evaluate.py \
  --eval_type doc \
  --file_path "output/with_img_kimi" \
  --output_folder "output/doc_evaluation" \
  --bulk_evaluate \
  --combine \
  --reset_progress
# 输出:
# Previous progress cleared. Starting fresh evaluation...
```

#### 并发执行示例

```bash
# 使用4个并发进程评测
python evaluate.py \
  --eval_type doc \
  --file_path "output/with_img_kimi" \
  --output_folder "output/doc_evaluation" \
  --bulk_evaluate \
  --combine \
  --max_workers 4
# 输出:
# Processing 10 directories (already completed: 0)
# Using 4 parallel workers for evaluation
# [1/10] Worker 12345: Evaluating problem_0_math_g12...
# [2/10] Worker 12346: Evaluating problem_1_math_g12...
# [3/10] Worker 12347: Evaluating problem_2_math_g12...
# [4/10] Worker 12348: Evaluating problem_6_physics_g12...
# ...
# Worker 12345: ✓ Completed and saved: problem_0_math_g12
# Worker 12346: ✓ Completed and saved: problem_1_math_g12
# ...

# 中断后继续（并发安全，不会重复评测）
python evaluate.py \
  --eval_type doc \
  --file_path "output/with_img_kimi" \
  --output_folder "output/doc_evaluation" \
  --bulk_evaluate \
  --combine \
  --max_workers 4
# 输出:
# Found 6 completed evaluations. Resuming from checkpoint...
# Processing 10 directories (already completed: 6)
# Using 4 parallel workers for evaluation
# [1/10] Worker 12350: Skipping problem_0_math_g12 (already claimed/completed)
# [7/10] Worker 12351: Evaluating problem_7_chemistry_g12...
# ...
```

### 进度文件

进度文件 `evaluation_progress.json` 格式：
```json
{
    "problem_0_math_g12": true,
    "problem_1_math_g12": true,
    "problem_2_math_g12": true
}
```

### 注意事项

1. **不要手动修改进度文件**: 系统会自动维护，手动修改可能导致问题
2. **更换输出目录**: 如果更换了 `--output_folder`，会创建新的进度文件
3. **强制重新评估**: 使用 `--reset_progress` 参数可以清除进度，从头开始
4. **结果文件**: 即使中断，已完成的评估结果文件仍然保存在 `output_folder` 中
5. **并发安全**:
   - 使用文件锁确保多进程并发时的数据一致性
   - 支持同时运行多个评测进程（相同的 `output_folder`）
   - 自动避免重复评测同一文档
   - 每个进程独立初始化模型，互不干扰
6. **并发性能建议**:
   - 对于 I/O 密集型任务（大量 API 调用），可以使用较多的并发进程（如 8-16）
   - 对于 CPU 密集型任务，建议并发数不超过 CPU 核心数
   - 注意 API 限流，避免并发数过高导致请求失败

## 输出格式

评估结果保存为 JSON 文件，格式如下：

```json
{
  "document": "文档路径",
  "evaluation": {
    "correctness_and_completeness": {
      "score": 4,
      "name": "解题步骤的正确性和完整性"
    },
    "logical_coherence": {
      "score": 5,
      "name": "讲解的逻辑连贯性"
    },
    "diagram_match": {
      "score": 4,
      "name": "图示与题目的匹配度"
    },
    "understandability_and_teaching_effect": {
      "score": 4,
      "name": "讲解的易懂性和教学效果"
    },
    "layout_and_visual_clarity": {
      "score": 5,
      "name": "排版和视觉呈现的清晰度"
    },
    "element_layout_quality": {
      "score": 4.2,
      "name": "图片元素布局质量"
    },
    "visual_consistency": {
      "score": 4.5,
      "name": "视觉一致性"
    },
    "text_diagram_synergy": {
      "score": 4.3,
      "name": "图文协同的流畅性"
    },
    "overall_score": {
      "score": 4.36,
      "name": "综合得分"
    }
  },
  "dimension_details": {
    "correctness_and_completeness": {
      "dimension": "correctness_and_completeness",
      "score": 4,
      "justification": "详细的评分理由...",
      "identified_issues": ["问题1", "问题2"]
    },
    "diagram_match": {
      "dimension": "diagram_match",
      "score": 4.2,
      "justification": "Scene 1 (得分: 4): ...\n\nScene 2 (得分: 5): ...\n\nScene 3 (得分: 4): ...",
      "identified_issues": ["Scene 1: 问题1", "Scene 2: 问题2"],
      "scene_details": [
        {
          "scene_index": 1,
          "scene_path": "path/to/scene1.png",
          "result": {
            "dimension": "diagram_match",
            "score": 4,
            "justification": "该scene的评分理由...",
            "identified_issues": ["问题1"]
          }
        },
        {
          "scene_index": 2,
          "scene_path": "path/to/scene2.png",
          "result": {
            "dimension": "diagram_match",
            "score": 5,
            "justification": "该scene的评分理由...",
            "identified_issues": []
          }
        }
      ],
      "scene_scores": [4, 5, 4]
    },
    "element_layout_quality": {
      "dimension": "element_layout_quality",
      "score": 4.2,
      "justification": "Image 1 (得分: 4): ...\n\nImage 2 (得分: 5): ...\n\nImage 3 (得分: 4): ...",
      "identified_issues": ["Image 1: 问题1", "Image 3: 问题2"],
      "image_details": [
        {
          "image_index": 1,
          "image_path": "path/to/image1.png",
          "result": {
            "dimension": "element_layout_quality",
            "score": 4,
            "justification": "该图片的评分理由...",
            "identified_issues": ["问题1"]
          }
        },
        {
          "image_index": 2,
          "image_path": "path/to/image2.png",
          "result": {
            "dimension": "element_layout_quality",
            "score": 5,
            "justification": "该图片的评分理由...",
            "identified_issues": []
          }
        }
      ],
      "image_scores": [4, 5, 4]
    },
    "visual_consistency": {
      "dimension": "visual_consistency",
      "score": 4.5,
      "justification": "Image 1 (得分: 5): 参考图片（基准）\n\nImage 2 (得分: 4): 与参考图片对比结果...\n\nImage 3 (得分: 5): 与参考图片对比结果...",
      "identified_issues": ["Image 2: 配色方案略有不同"],
      "image_details": [
        {
          "image_index": 1,
          "image_path": "path/to/image1.png",
          "result": {
            "dimension": "visual_consistency",
            "score": 5,
            "justification": "参考图片（基准）",
            "identified_issues": []
          }
        },
        {
          "image_index": 2,
          "image_path": "path/to/image2.png",
          "result": {
            "dimension": "visual_consistency",
            "score": 4,
            "justification": "与第一张图对比的评分理由...",
            "identified_issues": ["配色方案略有不同"]
          }
        }
      ],
      "image_scores": [5, 4, 5]
    }
  }
}
```

**说明**：
- 对于 **text_diagram** 类型的维度（如 `diagram_match`, `text_diagram_synergy`），输出结果中会包含：
  - `scene_details`: 每个scene的详细评估结果
  - `scene_scores`: 所有scene的分数列表
  - `score`: 所有scene分数的几何平均值
  - `justification`: 汇总所有scene的评分理由
  - `identified_issues`: 汇总所有scene识别出的问题

- 对于 **diagram** 类型的维度（如 `element_layout_quality`），输出结果中会包含：
  - `image_details`: 每张图片的详细评估结果
  - `image_scores`: 所有图片的分数列表
  - `score`: 所有图片分数的几何平均值
  - `justification`: 汇总所有图片的评分理由
  - `identified_issues`: 汇总所有图片识别出的问题

- 对于 **diagram_aa** 类型的维度（如 `visual_consistency`），输出结果中会包含：
  - `image_details`: 每张图片与第一张图对比的详细结果（第一张图自动得5分作为基准）
  - `image_scores`: 所有对比的分数列表（包括第一张图的5分）
  - `score`: 所有分数的几何平均值
  - `justification`: 汇总所有对比的评分理由
  - `identified_issues`: 汇总所有对比识别出的问题

## 文档结构要求

1. **Markdown 格式**：文档必须是 `.md` 格式
2. **图片引用**：支持标准 Markdown 图片语法 `![alt](image.png)`
3. **图片路径**：
   - 支持相对路径（相对于 .md 文件）
   - 支持绝对路径
   - 图片文件必须实际存在

## 评分标准自定义

评分标准文件 `eval_suite/doc_evaluation_rubric.json` 的格式：

```json
{
  "dimensions": {
    "dimension_key": {
      "name": "维度名称",
      "type": "text 或 text_diagram",
      "description": "维度描述",
      "scoring": {
        "5": {
          "score": 5,
          "description": "5分标准描述",
          "typical_defects": "典型缺陷",
          "impact_on_students": "对学生的影响"
        },
        ...其他分数标准
      }
    }
  }
}
```

**注意**：
- `type: "text"` - 仅使用文字内容评估
- `type: "text_diagram"` - 使用文字、图片和原题参考信息（原题图、img_caption、format_answer）评估
- `type: "text_diagram_aa"` - 使用文字和图片评估，**不使用原题参考信息**
- `type: "diagram"` - 仅使用图片评估，每张图独立评分
- `type: "diagram_aa"` - 仅使用图片评估，所有图与第一张对比

## 故障排除

### 1. JSON 解析错误
如果评分标准文件有语法错误，可以运行：
```bash
python -m json.tool eval_suite/doc_evaluation_rubric.json
```

### 2. 图片未找到
检查 Markdown 文件中的图片路径是否正确，确保图片文件存在。

### 3. 模型调用失败
- 检查模型名称是否正确（`Kimi-K25`）
- 检查 API key 等环境变量配置
- 增加 `--retry_limit` 参数值

## 示例输出文件

单个文档评估：
```
output/doc_evaluation/evaluation_solution.md_20260312_083500.json
```

批量评估（使用 `--combine`）：
```
output/doc_evaluation/evaluation_20260312_083500.json
```

## 技术实现

- **解析器**：`eval_suite/doc_utils.py`
- **异步模型调用**：使用 `asyncio.run()` 处理 LiteLLMWrapper
- **多模态支持**：文字+图片同时传给模型（对于 `text_diagram` 类型）
- **评分计算**：几何平均值（避免某个维度得0分导致整体为0）
