# OptiCore — 通用优化计算引擎（General-Purpose Optimization Engine）

> **Status**: 立项 2026-09-06 · 骨架阶段（内容随母项目 Task 2/3 落地迁入）
> **定位**: 三层架构的第三层（"后端方言"）：**零领域语义**的求解与搜索引擎集——元启发式骨架、精确求解驱动、列生成循环框架。对应五段纪律中的 `solve`。
> **依赖**: 无（标准库 + ortools 等求解器绑定）。**禁含**: 任何 visit/contract/calendar 概念——领域逻辑一律经接口注入。

## 职责（What belongs here）

| 组件 | 内容 | 种子来源（母项目） |
|---|---|---|
| **ALNS 骨架** | 毁坏-修复循环、SA 退火接受、轮盘赌选择、迭代统计——合法域/增量估价经回调注入 | `algos/alns_v3.py` 循环骨架 |
| **遗传骨架** |种群/交叉/变异框架 | `algos/hgs_pvrp.py` 骨架 |
| **列生成循环框架** | LP→定价→回灌→收敛判据的通用编排（定价子问题定义由调用方给） | `column_generate` 编排段 |
| **精确驱动** | CP-SAT 封装：限时、status 凭证（OPTIMAL/FEASIBLE/…）、best_bound/gap 日志契约 | `tsp_engine._exact_open_tsp_status` |
| **构造启发** | NN+2opt、最优插入 | `_nn2opt_open`、`best_insert` |
| **运行骨架** | 算法注册/计时/种子管理/复现契约 | `algos/registry.py` |

## 接口草案（零领域语义）

```python
class Objective(Protocol):            # 全量重算（真值）
    def __call__(self, solution) -> float: ...
class Delta(Protocol):                # 增量估价（可错，受不变量测试约束）
    def __call__(self, solution, move) -> float: ...
class Legality(Protocol):             # 领域合法域（如合同槽位集）
    def moves(self, solution) -> Iterable[Move]: ...
```

**不变量**：`|Obj_incremental − Obj_recompute| < ε` 随机移动对拍（2026-09-06 ChatGPT 共研采纳项 #6，直接针对母项目 `cur_km += delta` 漂移风险）。

## 铁律

1. 引擎不含任何 visit/contract/calendar 词汇（grep 可验）；
2. 同种子逐位可复现是引擎契约，不是可选特性；
3. 每个求解凭证必带 status——禁止把启发式输出统称"精确"；
4. 领域特化 = 接口实现（放 VisitModel/应用层），永不进本仓库。

## 关联项目

- 上游接口消费方：[`VisitModel`](/Users/ghb/VisitModel)（数学方言）、母项目（应用）
- 平级：[`VisitIR`](/Users/ghb/VisitIR)（语义层——本仓库不依赖它）
