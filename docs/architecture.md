# Architecture

## One data foundation, six modules

```mermaid
flowchart LR
  A[OTA数字护照] --> B[影响分析与测试选样]
  B --> C[车端异常发现与混杂过滤]
  C --> D[版本对照与首个分歧]
  D --> E[证据化根因Agent]
  E --> F[反事实实验引擎]
  F --> G[修复/回归/灰度决策]
  G --> H[知识库与测试库]
  H --> B
```

## Runtime layers

### Vehicle-side observer

- Read-only shadow observer
- Behavior envelope
- Time-series anomaly detection
- OOD scoring
- Sensor and hardware health checks
- Event snapshot trigger

### Cloud diagnosis plane

- OTA passport and change graph
- Module replay or end-to-end trajectory comparison
- Historical case retrieval
- Evidence-grounded multi-agent diagnosis
- Counterfactual experiment orchestration
- Technical evidence package generation

## Current repository implementation

The repository implements the full contract and an executable vertical slice. Components that require vehicle proprietary systems are represented by stable adapters or deterministic MVP engines so that the workflow can be demonstrated offline.
