# 机器人执行组件的外部依赖

平台仓库维护协议、客户端、mock 网关和硬件接入适配，不再复制遥操作项目源码。`esrobo_teleop` 中的驱动适配、轨迹、碰撞和详细执行诊断由外部项目提供；硬件路径仍使用这些组件，未删去运动保护。

## 固定来源

| 项目 | 来源 |
| --- | --- |
| 代码仓库 | `https://github.com/SaluteYan/esrobo.git` |
| 固定提交 | `f82c2ffdf55385ac48ee72c3de9f99c3f4151011` |
| Python 源码 | `teleoperation/src/esrobo_teleop/` |
| 机器人环境 | `teleoperation/environment.robot.yml` |
| 配置与手桥 | `teleoperation/config/teleop_config.yaml`、`teleoperation/bridges/hand_ros_bridge.py` |

## 安装布局

在平台仓库外单独检出执行组件，使用其固定版本，不把整份代码复制回平台仓库。以下在 `HUSTESROBO/ESROBO` 仓库根目录执行，目标目录须尚不存在：

```bash
git clone --no-checkout https://github.com/SaluteYan/esrobo.git ../esrobo-runtime
git -C ../esrobo-runtime checkout --detach f82c2ffdf55385ac48ee72c3de9f99c3f4151011
export ESROBO_RUNTIME="$(realpath ../esrobo-runtime)/teleoperation"
```

按固定运行时的 [机器人环境说明](https://github.com/SaluteYan/esrobo/blob/f82c2ffdf55385ac48ee72c3de9f99c3f4151011/teleoperation/README.md)准备 Python 及厂商 SDK；只读安装环境不等于实机部署完成。激活机器人环境后，最后安装本平台的通信包，以明确实际使用的网关来源：

```bash
python -m pip install --no-deps -e "$ESROBO_RUNTIME" -e ./robot_link
python -c 'import esrobo_teleop, esrobo_link; print(esrobo_teleop.__file__); print(esrobo_link.__file__)'
```

所有带 `--hardware` 的命令使用 `$ESROBO_RUNTIME/config/teleop_config.yaml`；手桥使用 `$ESROBO_RUNTIME/bridges/hand_ros_bridge.py`。两端须核对相同配置与模型。运行时自身的模型资源按其清单获取；平台独立模型见 [model](../model/README.md)，不要仅替换文件路径而忽略版本合同。

## 无硬件通信

不装上述外部包也能运行客户端和 mock 网关，二者仅依赖 Python 标准库。mock 保留普通网关 JSONL 日志；详细数值执行跟踪仅在硬件模式加载。缺失外部运行时而选择 `--hardware` 时，在设备初始化前报出安装提示，不自动降级为 mock。
