from pathlib import Path
import yaml


class ConfigError(RuntimeError):
    pass


def load_config(path: str | Path) -> dict:
    cfg_path = Path(path)
    if not cfg_path.exists():
        raise ConfigError(f"配置文件不存在: {cfg_path}")

    with cfg_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if "sources" not in data or not isinstance(data["sources"], list):
        raise ConfigError("配置文件缺少 sources 列表")
    return data
