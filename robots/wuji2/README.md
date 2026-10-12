# Wuji2 灵巧手

Wuji Technology 二代灵巧手资产，用于机器人仿真、可视化和机械安装集成。每只手有 20 个驱动关节。

## 来源与许可

- 上游仓库：https://github.com/wuji-technology/wuji-description
- 本次来源：本机 `/home/fcl/syz/wuji-description` 的 `hand2/` 目录。
- 许可：MIT，原始版权声明和完整条款见 [LICENSE](LICENSE)。
- 仅收录二代手；不包含一代手、手套、上游 CI 和发布记录。
- `hand2_1`、`hand2_2` 是上游已有的型号目录，保留其名称、包名和内部结构，避免破坏引用。版本与日期记录在下表，不另建日期副本。

## 版本与日期

| 项目 | 记录 |
| --- | --- |
| 资产型号 | Wuji Hand 2.1、Wuji Hand 2.2，均包含左右手 |
| 上游发布版本 | `2026.10.12`（来源仓库 `CHANGELOG.md`） |
| 上游版本日期 | `2026-10-12` |
| 入库核验日期 | `2026-10-12` |
| 来源提交 | `829c9aa27cb12c3a49d5b8d63c9869dd8f656702` |
| 来源状态 | 核验时来源 Git 工作区干净；本仓库 174 个资产文件与来源 `hand2/` 逐文件 SHA-256 一致，许可证一致 |

型号编号与发布版本分别记录；后续更新时同步更新版本、日期和来源提交，不改变模型内部引用路径。

## 资产组织

| 目录 | 内容 |
| --- | --- |
| `hand2_1/body/` | 基础型号左右手的 URDF、MJCF、USD、STL 和 ROS2 包描述 |
| `hand2_2/body/` | 带指尖触觉传感器垫型号的同类资源 |
| `hand2_1/attachment/` | 左右手掌安装接口 STEP 和 PDF 图纸 |
| `hand2_2/attachment/` | 对应型号的左右手掌安装接口 STEP 和 PDF 图纸 |

安装接口 STEP 为手掌及线束组件，不是完整灵巧手 CAD。两种型号的模型均以安装座为根节点，包含腕部 IMU 坐标系及指尖查询坐标系。触觉传感器垫的质量在上游说明中仍为暂定值。

## 加载入口

以下命令从本仓库根目录执行；将 `hand2_1` 替换为 `hand2_2` 可加载另一型号，将 `right` 替换为 `left` 可加载左手。

### MuJoCo

```bash
python -m mujoco.viewer --mjcf=robots/wuji2/hand2_1/body/mjcf/right.xml
```

### URDF

普通工具使用 `hand2_1/body/urdf/{left,right}.urdf`，网格路径相对于 URDF 文件解析。例如安装 `urdf-viz` 后：

```bash
urdf-viz robots/wuji2/hand2_1/body/urdf/right.urdf
```

ROS2 使用 `*-ros.urdf`，通过 `package://` 引用对应包的网格。两个包的根目录分别为 `hand2_1/body/` 和 `hand2_2/body/`，包名分别为 `wuji_hand2_1_description` 和 `wuji_hand2_2_description`。在配置好的 ROS2 工作空间中构建对应包后加载。机械安装附件位于包目录外，不随 ROS2 包安装。

### USD / Isaac Sim

入口分别为：

- `hand2_1/body/usd/{left,right}/wujihand2_1.usd`
- `hand2_2/body/usd/{left,right}/wujihand2_2.usd`

保持入口旁的 `configuration/`、`textures/` 及原始配置文件完整。材质引用外部 `OmniPBR.mdl`，需要提供该材质库的 Isaac Sim / Omniverse 环境；本仓库不包含此依赖。

## 单位与坐标

- URDF / MJCF 使用米、千克、弧度及右手坐标系；MJCF 明确采用弧度。
- USD 的 `metersPerUnit` 为 1，向上轴为 Z。
- 安装座根节点为 `l_mount` / `r_mount`；具体关节轴和安装位姿以模型定义为准，不在入库时转换坐标。
- STEP / PDF 按原始文件保留，机械单位及尺寸以 CAD 和图纸标注为准，未做 CAD 导入验证。

## 验证状态

- 174 个源资产文件逐一通过 SHA-256 一致性检查，原始资产内容未修改。
- 8 个 URDF 完成 XML 解析和网格引用存在性检查；ROS 包路径按对应 `package.xml` 解析。未执行 ROS2 构建或 RViz 可视化。
- 4 个 MJCF 均在 MuJoCo 中实际加载并推进 100 步；每个模型有 20 个关节自由度和 20 个执行器，状态有限且无仿真警告。
- 4 个 USD 入口均通过 OpenUSD 图层组合检查，本地纹理依赖可解析；独立 OpenUSD 环境无法解析外部 `OmniPBR.mdl`。
- 未验证 Isaac Sim / PhysX 运行、材质渲染和图形界面效果；不将 OpenUSD 组合检查等同于 Isaac Sim 兼容性验证。

### 2026-10-12 入库复核

- 本次重新核验：174 个资产文件与指定来源逐文件 SHA-256 一致，无缺失、内容差异或额外资产文件，MIT 许可证一致。
- 本次重新解析全部 8 个 URDF 并检查普通路径与 ROS `package://` 网格引用，均存在。
- 上述 MuJoCo / OpenUSD 结果为既有入库记录；本次仅补充版本日期，未重新执行仿真或 USD 加载。
