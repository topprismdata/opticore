# OptiCore 设计草案 · 2026-09-06

## 1. 边界

**进来**：ALNS/HGS 循环骨架、SA 接受、列生成编排、精确驱动封装、构造启发、注册/种子/复现契约。
**不进来**：合同/日历/义务/走廊等一切领域语义；距离矩阵来源；数据解析；报告。

## 2. 迁移映射（母项目 → OptiCore）

| 母项目现址 | 去向 | 领域逻辑剥离方式 |
|---|---|---|
| `alns_v3.py` 主循环（退火/接受/统计） | `engines/alns.py` | 合法域与估价以 Legality/Delta 接口注入 |
| `r2_alns.move_candidates` 的"枚举-估价"外壳 | `engines/alns.py` | 候选生成本身（合同槽位集）→ VisitModel 邻域规格 |
| `hgs_pvrp.py` 骨架（交叉/多样/短促退火） | `engines/hgs.py` | 同上 |
| `column_generate` 编排（LP→定价→回灌→收敛） | `engines/column_generation.py` | 定价定义由调用方注入 |
| `tsp_engine._exact_open_tsp_status` 封装 | `engines/exact.py` | 公式 → VisitModel；驱动留此 |
| `_nn2opt_open` / `best_insert` | `heuristics/` | 纯几何，天然无领域 |
| `registry.py` 注册/计时/种子 | `harness/` | — |

## 3. 抽离就绪要求（母项目 Task 2/3 编码时即遵守）

1. 新增引擎代码禁止出现 contract/phase/obligation 词汇；
2. 增量估价与全量重算分离为两个可注入实现（不变量测试在引擎层跑通一次，全领域受益）;
3. 随机性只经 harness 的种子通道（保证同种子逐位复现）。

## 4. 待定

- Legality/Delta/Move 协议的最小形态（dataclass vs Protocol）；
- 并行评估（多解并行）是否进 v0（母项目 exp_09_rep 已有并行先例）；
- 与 ortools 参数体系的解耦深度。
