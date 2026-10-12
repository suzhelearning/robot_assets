# Sharpa Wave 灵巧手

Sharpa Wave（`wave_01`）的官方仿真模型和专用触觉传感器数据。机器人描述按格式集中在 `models/body/`；左右手共用一份网格目录，标准、双手、浮动基座及高保真变体分别保留。

## 版本与日期

入库日期：**2026-10-12**。来源根目录：`/home/fcl/syz/sharpa`。

| 内容 | 上游仓库 | 来源版本（git describe） | 来源提交日期 |
| --- | --- | --- | --- |
| 仿真模型 | [sharpa-urdf-usd-xml](https://github.com/sharpa-robotics/sharpa-urdf-usd-xml) | `v1.0.0-3-g0d19cac` | `2026-09-17` |
| 触觉数据 | [sharpa-tactile-sensor-assets](https://github.com/sharpa-robotics/sharpa-tactile-sensor-assets) | `v1.0.0-2-g865530a` | `2026-05-20` |

上述版本均为 `v1.0.0` 标签之后的提交快照，不是新的正式发布版本；日期为来源 HEAD 提交日期，不是推测的发布日期。完整提交号、时区、本机来源和入库日期见 [versions.json](versions.json)。采集版本时两个来源 Git 工作区均干净。

## 目录与收录范围

| 目录 | 内容 |
| --- | --- |
| `models/body/` | 单个 ROS2 描述包 `sharpa_wave_description`；左手、右手、双手、浮动基座和高保真变体 |
| `body/urdf/{left,right,dual,float-base/}` | URDF 模型；网格以 `package://sharpa_wave_description/meshes/...` 引用 |
| `body/mjcf/{left,right,dual,float-base/}` | MuJoCo XML；通过相对路径共用网格 |
| `body/usd/{left,right,dual,float-base/,high-fidelity/}` | USD 入口、分层图层和专用纹理；高保真左右手的重复纹理由相对符号链接共享 |
| `body/meshes/{left,right}/` | 左右手 STL 网格；双手及浮动基座模型复用此处文件 |
| `body/launch/`、`body/config/{left,right}/` | 单包 ROS2 启动文件及左右手 RViz 配置 |
| `tactile/wave_01/` | 拇指及其余四指的触觉表面网格、点坐标与法线数组 |

`models/UPSTREAM_README.md` 保留上游原始说明，其中 `src/`、旧的左右手包名和示例路径指向上游目录，不是本仓库入口；实际位置和命令以下文为准。不迁入外围 SDK、训练框架、策略权重、训练输出、日志或缓存；外围项目中的模型副本不重复收录。
本仓库未启用 Git LFS。后续发布或频繁更新大型资源前，应按远端限制决定是否迁移至 LFS。

## 许可

- **仿真模型：Apache-2.0。** 原始声明见 `models/body/LICENSE.txt`，第三方声明见 `models/body/NOTICE.txt`；完整许可文本见 `models/body/APACHE-2.0.txt`（来自同一官方触觉资产仓库的完整许可证，保留原文）。
- **触觉数据：Apache-2.0。** 见 `tactile/LICENSE`。

## 加载入口

以下命令从本仓库根目录执行。

### MuJoCo

```bash
python -m mujoco.viewer --mjcf=robots/sharpa-wave/models/body/mjcf/right/right_sharpa_wave.xml
```

将路径中的 `right` 和文件前缀 `right_sharpa_wave` 换为 `left` / `left_sharpa_wave` 可加载左手。腕部、法兰变体使用 `*_with_wrist.xml`、`*_with_flange.xml`；浮动基座在 `body/mjcf/float-base/{left,right}/`，双手在 `body/mjcf/dual/`。

### URDF / ROS2

- 右手入口：`models/body/urdf/right/right_sharpa_wave.urdf`。
- 左手入口：`models/body/urdf/left/left_sharpa_wave.urdf`。
- 双手入口：`models/body/urdf/dual/dual_sharpa_wave.urdf`；浮动基座入口在 `body/urdf/float-base/{left,right}/`。
- ROS2 包根目录为 `models/body/`，包名 `sharpa_wave_description`。将它放入工作空间 `src/`，构建后以 `ros2 launch sharpa_wave_description left_display.launch.py` 或 `right_display.launch.py` 查看单手；Gazebo 启动文件为 `left_gazebo.launch.py`、`right_gazebo.launch.py`。若使用非 ROS 加载器，必须把 `package://sharpa_wave_description/meshes/...` 映射至 `body/meshes/...`，不能当作普通相对路径。

### USD / Isaac Sim

基础 USD 入口为 `models/body/usd/{left,right,dual}/{left,right,dual}_sharpa_wave.usda`；浮动基座位于 `body/usd/float-base/{left,right}/`，高保真入口位于 `body/usd/high-fidelity/{left,right}/`。每个入口的子目录和图层应保持在一起，高保真模型还须一同保留左右手纹理目录；`*_MITmode.usda` 为 MIT 控制模式变体，不是许可证标记。

上游说明要求 Isaac Lab 的 `IdealPDActuator` 使用 `stiffness=None`、`damping=None` 以沿用 USD 动力学参数；MIT 控制模式建议频率高于 80 Hz。此处记录上游建议，不将其视为本次硬件标定结果。

### 触觉数据

- `tactile/wave_01/tactileSensor_map_{4F,TH}_{point,normal}.npy`：使用 `numpy.load(path, allow_pickle=False)` 加载；每个数组形状为 `(240, 240, 3)`。
- `tactileSensor_{4F,TH}.obj`：对应传感器表面网格。

## 单位、坐标与依赖

- MJCF 明确使用弧度；URDF / MJCF 按米、千克及右手系的模型约定使用，不在入库时转换。
- 基础 USD 标记 `metersPerUnit = 1`、`upAxis = "Z"`；具体变体以其图层元数据为准。
- 指尖 `*_DP` 为 MDH 坐标系，`*_elastomer` 用于触觉，`*_fingertip` 用于 IK；三者不可混用。
- 触觉 NPY 的长度单位及坐标转换在随附 README 中未明确说明，不直接假定为米；与机器人模型拼接前需确认标定关系。
- 各套资源无其他本仓库资产依赖；运行分别需要 MuJoCo、ROS2 / URDF 加载器、Isaac Sim / Omniverse 或 NumPy。

## 目录调整与验证（2026-10-12）

- `models/body/` 保留全部 15 个 URDF、15 个 MJCF 和 34 个 USD 入口；共 274 个文件（271 个模型与配置文件、3 个许可/声明文件），另有 6 个未改动的触觉数据文件。上游 3 份旧 ROS 包清单、2 份旧 CMake 文件及 1 份生成的 Python 字节码已由单包布局取代或移除。
- 15 个 URDF、15 个 MJCF 和 4 个 ROS 启动文件仅改写了资源路径 / 包名；与上游原文逐项对照，其余内容包括关节、质量、惯量、驱动和摩擦参数均未改。其余 235 个保留的上游模型文件相对调整前逐文件 SHA-256 一致；其中两份高保真 USD 在此前已无损重打包。
- 15 个 URDF 完成 XML 解析和全部 1002 个网格引用存在性检查，新 ROS 包名映射统一为 `sharpa_wave_description`。本机没有 ROS2 / colcon，因此未执行包构建、RViz 或 Gazebo。
- MuJoCo **3.15.0**：全部 15 个 MJCF 实际加载并各推进 100 步，状态有限且无仿真警告；单手为 22 自由度、浮动基座为 28 自由度、双手为 62 自由度，执行器数量分别相同。此前 3 个双手 MJCF 的网格相对路径失效问题随目录重组一并修正，网格和物理参数未改。
- OpenUSD **26.8**：34 个 USDA 入口全部打开并完成依赖扫描；本地依赖可解析，仍需要 Isaac Sim / Omniverse 提供外部 `OmniPBR.mdl` 和高保真模型的 `OmniSurface.mdl`。未验证 PhysX 运行或材质渲染。
- 触觉 NPY 原有的 NumPy 加载检查仍适用；未执行 OBJ 渲染或图形界面验证。

迁移影响：原 `left_sharpa_wave`、`right_sharpa_wave` ROS2 包名和原 `models/wave_01/<型号>/` 路径不再存在。下游需将包依赖及 `package://` URI 改为 `sharpa_wave_description`，把模型入口改到 `body/{urdf,mjcf,usd}/` 下；不保留过时入口的副本或兼容别名。

## 无损精简

重组前，高保真模型的 `src/left_sharpa_wave_hiRes.usd` 和 `source/right_hand_HB_HiRes.usd` 使用 OpenUSD 26.8 无损重打包为 USDC；现在分别位于 `body/usd/high-fidelity/left/src/` 和 `body/usd/high-fidelity/right/source/`。与上游图层通过 `Sdf.Layer.ExportToString()` 对比，完整声明内容逐字一致；迁移目录时没有再次改写这两份 USD。原模型目录的当时体积由 304.05 MiB 降至 297.29 MiB，节省 7,094,370 字节（2.23%）。

保留 16 位/通道的高保真纹理原样：降为 8 位虽然明显缩小体积，但会改变纹理数值。为保持所有高保真模型与参数可用，不删除变体、网格或纹理；进一步显著缩小需要接受画质、精度或模型完整性的取舍。

高保真左右手有 11 个原先逐字节相同的纹理文件；当前右手对应路径是指向左手同名纹理的**仓库内相对符号链接**，原始像素与文件字节由左手文件保留。此次只替换重复文件，不修改 USD 图层或物理参数，移除了 30,107,668 字节（28.71 MiB）的重复文件内容；计入 542 字节的符号链接路径文本，`body/usd/` 的文件逻辑大小由 273.98 MiB 降至 245.27 MiB。34 个 USD 入口经 OpenUSD 26.8 打开并扫描依赖，高保真本地纹理可解析，未解析项仅为原有外部材质库。加载或打包高保真模型时必须保留整个 `body/usd/high-fidelity/`，不能单独复制右手目录；在不支持 Git 符号链接的系统上要确保链接正确检出。Git 历史及上游文件不会因此缩小。
