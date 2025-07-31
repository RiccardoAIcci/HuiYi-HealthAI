# MiniMind2-Small LoRA微调脚本

这是一个完整的MiniMind2-Small模型LoRA微调脚本，支持自定义数据集进行微调，包含完整的训练流程和日志记录功能。

## 🚀 功能特性

- ✅ **自动模型下载**: 使用ModelScope SDK自动下载MiniMind2-PyTorch模型
- ✅ **数据集合并**: 支持按比例合并任务数据和自认知数据
- ✅ **LoRA微调**: 使用PEFT库进行高效的LoRA微调
- ✅ **训练监控**: 集成Weights & Biases进行训练过程监控
- ✅ **参数可配置**: 支持命令行参数配置所有训练参数
- ✅ **完整日志**: 详细的训练日志和时间统计

## 📋 环境要求

### Python版本
- Python 3.9+

### 硬件要求
- GPU: 推荐使用NVIDIA GPU (支持CUDA)
- 内存: 至少16GB RAM
- 存储: 至少10GB可用空间

### 依赖包
```bash
pip install -r requirements.txt
```

主要依赖包包括:
- torch >= 2.0.0
- transformers >= 4.35.0
- peft >= 0.6.0
- accelerate >= 0.20.0
- wandb >= 0.16.0
- modelscope >= 1.9.0

## 📁 数据格式

训练数据应为JSONL格式，每行一个JSON对象，结构如下：

```json
{"conversations": [{"role": "user", "content": "用户问题"}, {"role": "assistant", "content": "助手回答"}]}
```

例如：
```json
{"conversations": [{"role": "user", "content": "你叫什么名字？"}, {"role": "assistant", "content": "我叫慧医小助，是一名AI助手。"}]}
```

## 🎯 使用方法

### 1. 基本使用

```bash
python minimind_lora_finetune.py \
    --lora_name "my_chatbot_lora" \
    --task_data "./dataset/medical_data_formatted.jsonl" \
    --identity_data "./dataset/medical_identity.jsonl" \
    --epochs 20 \
    --batch_size 4 \
    --learning_rate 1e-4 \
    --use_wandb \
    --wandb_project "my_minimind_project"
```

### 2. 快速测试

```bash
python simple_train_example.py
```

### 3. 完整参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--lora_name` | str | `medical_chatbot_lora` | LoRA模型名称 |
| `--task_data` | str | `./dataset/medical_data_formatted.jsonl` | 任务数据路径 |
| `--identity_data` | str | `./dataset/medical_identity.jsonl` | 自认知数据路径 |
| `--merged_data` | str | `./dataset/merged_training_data.jsonl` | 合并后数据路径 |
| `--out_dir` | str | `./out` | 输出目录 |
| `--epochs` | int | `10` | 训练轮次 |
| `--batch_size` | int | `4` | 批次大小 |
| `--learning_rate` | float | `1e-4` | 学习率 |
| `--max_length` | int | `512` | 最大序列长度 |
| `--use_wandb` | flag | `False` | 使用Weights & Biases |
| `--wandb_project` | str | `minimind_medical_chatbot` | W&B项目名称 |
| `--ratio` | int | `3` | 任务数据与自认知数据比例 |
| `--skip_download` | flag | `False` | 跳过模型下载 |
| `--skip_merge` | flag | `False` | 跳过数据合并 |

## 📊 训练流程

### 1. 模型下载阶段
```
🔄 开始下载MiniMind2-PyTorch模型...
✅ 模型下载成功: /path/to/model
```

### 2. 数据准备阶段
```
🔄 开始合并数据集 (比例 3:1)...
📊 任务数据: 150000 条
📊 自认知数据: 96 条
✅ 数据合并完成: 150096 条数据保存到 ./dataset/merged_training_data.jsonl
```

### 3. 模型训练阶段
```
🚀 开始LoRA训练...
💻 使用设备: cuda
📋 训练参数:
  - LoRA名称: medical_chatbot_lora
  - 训练轮次: 20
  - 批次大小: 4
  - 学习率: 1e-4
🔄 加载模型和分词器...
✅ 模型加载完成
📊 模型参数数量: 26.5M
📊 可训练参数: 0.67M / 26.5M (2.53%)
🔥 开始训练...
```

### 4. 训练完成
```
✅ 模型保存到: ./out/medical_chatbot_lora
⏱️ 训练完成! 总耗时: 45.2 分钟
```

## 📈 监控训练

### Weights & Biases集成

脚本支持使用Weights & Biases进行训练监控：

1. 设置W&B账号：
```bash
wandb login
```

2. 启用W&B监控：
```bash
python minimind_lora_finetune.py --use_wandb --wandb_project "my_project"
```

### 监控指标

- 训练损失曲线
- 学习率变化
- 训练时间统计
- 模型参数统计

## 🔧 高级配置

### LoRA参数调整

可以通过修改脚本中的LoRA配置来调整微调效果：

```python
def setup_lora_config(lora_r: int = 8,        # LoRA rank，越大模型容量越大
                      lora_alpha: int = 32,    # LoRA alpha，影响学习强度
                      lora_dropout: float = 0.1):  # LoRA dropout，防止过拟合
```

### 目标模块配置

默认LoRA应用于注意力机制的投影层：
```python
target_modules=["q_proj", "v_proj", "k_proj", "o_proj"]
```

## 📝 最佳实践

### 1. 数据准备
- 确保训练数据质量高
- 保持自认知数据和任务数据的平衡
- 建议自认知数据占总数据的5-10%

### 2. 超参数调优
- 学习率：建议从1e-4开始尝试
- 批次大小：根据GPU内存调整
- 训练轮次：通常10-30轮即可

### 3. 监控训练
- 使用W&B监控损失变化
- 注意防止过拟合
- 定期评估模型效果

## 🚨 注意事项

1. **内存使用**: 训练过程中会占用大量GPU内存，建议使用至少8GB显存的GPU
2. **数据格式**: 确保数据严格按照指定的JSON格式
3. **路径设置**: 确保所有路径正确，特别是数据文件路径
4. **环境配置**: 确保CUDA环境正确配置

## 🔍 故障排除

### 常见问题

1. **CUDA内存不足**
   - 减小batch_size
   - 减小max_length
   - 使用gradient_accumulation_steps

2. **数据加载错误**
   - 检查JSONL文件格式
   - 确认文件编码为UTF-8
   - 验证JSON语法正确性

3. **模型加载失败**
   - 检查网络连接
   - 确认ModelScope访问正常
   - 验证磁盘空间充足

## 📞 支持与反馈

如有问题或建议，请通过以下方式联系：
- 创建Issue
- 发送邮件
- 参与讨论

## 📄 许可证

本项目遵循Apache License 2.0许可证。 