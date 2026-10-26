# 平台来源与发布范围

## 当前内容

平台仓库维护 `src/` 设备驱动、`document/` 厂家手册、`model/` 机器人模型和 `robot_link/` 通信接口。遥操作项目由组织主页单独列出，本仓库不再包含其源码目录。

## 2026-10-26 移除遥操作副本并保留独立模型

- 删除初始平台快照中的整个 `teleoperation/`，包括旧单机程序、输入桥、重定向、IK、控制源码和重复说明。
- 将整机 URDF 与所需视觉／碰撞网格独立保存为 `model/esrobo_waist_with_head/`。URDF 来自原平台快照，未改动关节或几何；70 个引用网格均已复制，合计 370,783,661 字节，由 Git LFS 管理。61 个碰撞网格与旧固定清单逐个一致，另外 9 个 DAE 无外部纹理引用。来源与逐文件哈希见 [模型清单](model/esrobo_waist_with_head/SOURCE.json)。
- 模型包使用 ROS 2 ament 资源安装结构；源码模型的 BSD 包声明沿用上游元数据。运行 `python3 model/verify_model.py` 校验实际 LFS 内容、引用与连接。
- 硬件执行所需 `esrobo_teleop` 改为明确的外部依赖，固定到 `SaluteYan/esrobo@f82c2ffdf55385ac48ee72c3de9f99c3f4151011`，安装与路径见 [RUNTIME.md](robot_link/RUNTIME.md)。硬件后端仍使用原有运动保护，不用 mock 替代真实执行。
- mock 网关不再无条件加载外部数值诊断，保留标准库 JSONL 日志；详细执行追踪仅在硬件模式加载。缺少硬件运行时在设备初始化前明确拒绝。
- 新增 [通信冒烟](robot_link/check_mock.py)，使用 `python -S` 隔离第三方包，验证左臂带手、仅右手、双侧 mock 的实际 UDP 握手、IDLE 与正常退出，以及缺失硬件依赖时的拒绝行为。没有连接真实设备。
- 平台首页只展示基础资源；遥操作等项目入口统一放在 [组织主页](https://github.com/HUSTESROBO)，不在平台重复展开应用介绍。

## 初始来源

初始快照来自 [SaluteYan/esrobo](https://github.com/SaluteYan/esrobo) 的固定提交 [`318b1d04786f1b6b11254e62b7628178910cd48c`](https://github.com/SaluteYan/esrobo/commit/318b1d04786f1b6b11254e62b7628178910cd48c)。原仓库与历史保留；新平台不复制原仓库完整历史。

| 子模块 | 固定提交 |
| --- | --- |
| Ranger | `b6ea21a275ca5e7168130cc6470e61474681d679` |
| RealSense | `e11d3e154ce3817c8be73f36b87a75f287e080e5` |
| UGV SDK | `c3dfaf444f9bae10757e546acae055aaf4a13de7` |

初始整理补齐 UGV SDK 子模块地址，三个版本保持不变。克隆后执行 `git submodule update --init --recursive` 和 `git lfs pull` 分别获取驱动子模块与模型网格。

## 验证边界

本轮文件完整性、协议 mock 与 126 个本地文档链接核验通过。70 个 LFS 对象上传后，使用独立空缓存重新从远端下载，逐个核对大小及 SHA256 全部一致；公开平台首页已无 `teleoperation/` 目录，组织首页模型链接已切换到 `model/`。ROS 2 Humble 下独立模型包构建成功，安装后 `package://` 路径可解析全部 70 个网格；没有进行完整设备工作空间编译、硬件环境安装、实机运动或机器人服务重启。厂商驱动、SDK 与模型保留各自来源和许可；密钥、标定、日志和环境未加入发布。

## 2026-10-26 在线模型展示

[交互查看器](https://hustesrobo-model-viewer.abloom-kite-0335.chatgpt.site)由本平台 URDF 与网格派生，网站单独维护和托管，本仓库没有重新引入遥操作源码。显示资源约 9.2 MB；72 个部件、71 个关节节点、39 个主动关节，mimic 按源模型计算。NERO 选用同源、同原点的 STL 表面以避免 DAE 细节减面后闪烁，其余网格减面并调整显示法线／材质；显示近似不用于运动或碰撞认证。

已通过 4 组独立 SciPy 全树 FK 与 Three.js 对照、模型结构、姿态校验、静态资源与离线渲染检查；公开部署由 Sites 确认成功。当前无受控浏览器，未做浏览器逐项点击或真实硬件测试。
