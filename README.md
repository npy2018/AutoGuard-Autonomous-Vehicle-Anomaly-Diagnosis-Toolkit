<div align="center">

# 🛡️ AutoGuard AI

### Agent-Driven Autonomous Vehicle Anomaly Diagnosis Toolkit

面向自动驾驶研发团队的 OTA 影响分析、异常检测、根因诊断与反事实验证工具箱。

[![CI](https://github.com/npy2018/AutoGuard-Autonomous-Vehicle-Anomaly-Diagnosis-Toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/npy2018/AutoGuard-Autonomous-Vehicle-Anomaly-Diagnosis-Toolkit/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Competition%20MVP-orange)](#-project-status)

</div>

# AutoGuard AI

面向无人车研发团队的 **AI异常行为诊断工具箱 MVP**。项目采用“通用诊断底座 + OTA专项应用”思路，首个示例聚焦：

> OTA 调整行人识别阈值后，车辆在雨夜将广告牌误识别为行人并触发异常急刹。

AutoGuard AI 将一次异常诊断拆成六个可复用模块：

1. OTA 数字护照与影响分析
2. 行为异常检测与混杂因素过滤
3. 新旧版本回放差异定位
4. 基于证据的根因候选生成
5. 反事实实验与因果验证
6. 修复、回归测试与灰度决策报告

## 功能亮点

- 每个诊断结论都绑定时间戳、字段路径和版本变更编号
- 使用 TF-IDF 案例检索增强根因分析，不依赖外部服务即可运行
- 自动定位新旧版本的首个显著分歧
- 自动生成可证伪的反事实实验
- 提供 Web Demo、REST API、命令行脚本和自动化测试
- 预留大模型、向量数据库、真实回放引擎和车端模型接入接口

## 目录结构

```text
autoguard-ai/
├── app/
│   ├── api/routes.py              # REST API
│   ├── services/                  # 六大诊断模块
│   ├── static/index.html          # 无构建依赖的演示页面
│   ├── main.py                    # FastAPI 入口
│   └── schemas.py                 # 数据契约
├── data/                           # 雨夜广告牌急刹示例数据
├── docs/                           # 架构、数据协议与路线图
├── scripts/run_demo.py             # 命令行演示
├── tests/                          # 单元测试与 API 测试
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## 快速开始

### 1. 创建环境

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -e .[dev]
```

### 2. 运行命令行 Demo

```bash
python scripts/run_demo.py
```

报告将写入：

```text
outputs/demo_diagnosis_report.md
```

### 3. 启动 Web Demo

```bash
uvicorn app.main:app --reload
```

打开：

```text
http://127.0.0.1:8000
```

API 文档：

```text
http://127.0.0.1:8000/docs
```

### 4. 运行测试

```bash
pytest
```

## API

### 运行内置示例

```bash
curl -X POST http://127.0.0.1:8000/api/v1/demo
```

### 提交自定义诊断

```bash
curl -X POST http://127.0.0.1:8000/api/v1/analyze \
  -H 'Content-Type: application/json' \
  --data-binary @data/demo_request.json
```

## 当前 MVP 边界

当前版本用于竞赛演示和工程验证，以下部分采用可替换的轻量实现：

- OTA 影响分析：规则知识图谱 + 结构化推理
- 历史案例检索：TF-IDF 相似度
- 行为异常检测：可解释评分模型
- 反事实验证：可配置因果规则引擎

生产化时可逐步替换为：

- 企业级代码大模型与 RAG
- 向量数据库和时序数据库
- 真实 SIL/HIL/云端回放平台
- 车端蒸馏模型、OOD 模型和 fleet-level Bayesian drift detector
- 端到端模型的轨迹分布、注意力与表征漂移分析

## 安全原则

AutoGuard AI 只生成技术诊断建议，不自动修改生产车辆软件，也不代替研发、质量、安全或法规负责人作最终发布和责任判断。

## License

MIT
