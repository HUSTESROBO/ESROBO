# ESROBO 机器人模型

本目录独立保存整机模型，不包含采集、重定向、IK 或遥操作控制程序。

- [URDF](esrobo_waist_with_head/urdf/esrobo_waist_with_head.urdf)：底盘、腰部、头部、NERO 双臂、力传感器安装件和 L20Lite 双手；关节与 mimic 定义保持来源版本。
- [meshes](esrobo_waist_with_head/meshes/)：URDF 引用的全部 70 个视觉／碰撞网格，含 STL 和 DAE。
- [SOURCE.json](esrobo_waist_with_head/SOURCE.json)：模型来源、固定版本、每个文件的大小和 SHA256。

URDF 从平台原快照原样复制，网格从本地 `SaluteYan/Dual-arm-teleoperation` 源码检出复制。61 个碰撞网格逐一匹配原先固定版本的清单；其余 9 个 DAE 为显示模型，已记录当前检出版本和哈希。模型包的 BSD 声明沿用上游 `package.xml`，未为第三方模型追加新的授权声明。

## 获取与检查

网格合计约 370.8 MB，以 Git LFS 保存；普通 Git 对象只包含指针。克隆后执行：

```bash
git lfs install
git lfs pull
python3 model/verify_model.py
```

校验器检查每个文件的实际内容、URDF 网格引用及关节连接，未下载 LFS 内容时明确报错。DAE 文件不引用额外纹理文件。

## ROS 2 资源包

`esrobo_waist_with_head/` 是只安装资源的 ament 包。加载 ROS 2 Humble 环境后，在仓库根目录执行：

```bash
colcon build --base-paths model --packages-select esrobo_waist_with_head
source install/setup.bash
ros2 pkg prefix esrobo_waist_with_head
```

这样可解析 URDF 中的 `package://esrobo_waist_with_head/meshes/...`。本次整理校验文件完整性，不运行机器人或宣称完成 ROS 构建。应用应锁定模型与控制配置的匹配版本；机器人网关的配置合同仍需两端一致。
