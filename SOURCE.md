# 平台来源与发布范围

## 2026-10-26 初始平台整理

本平台是从 [SaluteYan/esrobo](https://github.com/SaluteYan/esrobo) 的固定提交 [`318b1d04786f1b6b11254e62b7628178910cd48c`](https://github.com/SaluteYan/esrobo/commit/318b1d04786f1b6b11254e62b7628178910cd48c) 导出的独立源码快照。原仓库和原分支保留；本仓库不转移其完整 Git 历史。

包含设备驱动 `src/`、手册 `document/`、通信模块 `robot_link/`、共用控制组件 `teleoperation/` 与硬件配置文件。平台文档按硬件、驱动、模型、通信及应用项目重新组织。运行源码从该提交保留，不在此次展示整理中修改算法。

应用 `laptop_teleop/` 留在原仓库，相关文档链接固定到来源提交。组织主页列出实机遥操作和现有 IsaacLab 仿真项目；它们尚未迁移为本组织中的新独立仓库。

## 公共组件与后续拆分

`robot_link` 硬件后端仍导入 `teleoperation/src/esrobo_teleop` 的配置、驱动、轨迹、碰撞和诊断组件，因此暂时保留这一完整包及旧文档。它不是可整体删除的仿真目录。应用侧的 IK/重定向和执行侧组件将来可分包，但需要同时修改依赖、模型资源、安装脚本和合同并进行回归。

## 固定依赖与模型

| 子模块 | 固定提交 |
| --- | --- |
| Ranger | `b6ea21a275ca5e7168130cc6470e61474681d679` |
| RealSense | `e11d3e154ce3817c8be73f36b87a75f287e080e5` |
| UGV SDK | `c3dfaf444f9bae10757e546acae055aaf4a13de7` |

本快照补齐原 `.gitmodules` 缺失的 UGV SDK 来源，保留全部 gitlink 版本。克隆后初始化子模块：

```bash
git submodule update --init --recursive
```

碰撞网格并未随此源码快照复制；来源、尺寸和 SHA256 见 [SOURCE.json](teleoperation/assets/esrobo_waist_with_head/SOURCE.json)，获取入口为 [fetch_collision_meshes.py](teleoperation/scripts/fetch_collision_meshes.py)。下载器按固定上游版本检查模型与网格。安装脚本中的旧机器路径需按部署环境配置。

## 验证与发布边界

本次只整理源码和文档，不连接机器人、重启服务或执行运动。原仓库部分回归仅保存在开发机器，不能将旧文档中的测试数量当作本次检出覆盖；当前环境也未完成完整 ROS 构建和实机验收。本次导出核对 1,389 个非 Markdown 文件（不含补齐的 `.gitmodules`）与来源工作区逐字节一致；61 个通信／控制 Python 文件 AST 解析及遥操作 URDF XML 解析通过。五份平台入口文档的 105 个本地链接通过存在性检查（子模块路径按固定 gitlink 处理），mock 网关 `--help` 启动通过。三个子模块清单可解析，尚未执行全新递归下载或实体控制。

保留第三方驱动、SDK、模型的原始来源及各目录许可证，不用新的统一许可证覆盖它们。导出仅取已跟踪内容与本次文档，没有复制密钥、标定、环境、运行日志或部署备份。
