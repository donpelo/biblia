# -*- coding: utf-8 -*-
import os, json

DEFAULT_CFG = {
    "ui_lang": "es",
    "tts_rate": "180",
    "tts_volume": "1.0",
    "tts_voice": ""
}

def _read_json_bom(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def cfg_paths(base_dir=None):
    root = base_dir or repo_root()
    d = os.path.join(root, "config")
    return (
        os.path.join(d, "default.json"),
        os.path.join(d, "user.json")
    )

def load_config(base_dir=None):
    root = base_dir or repo_root()
    p_default, p_user = cfg_paths(root)

    cfg = dict(DEFAULT_CFG)

    if os.path.exists(p_default):
        try:
            cfg.update(_read_json_bom(p_default))
        except Exception:
            pass

    if os.path.exists(p_user):
        try:
            cfg.update(_read_json_bom(p_user))
        except Exception:
            pass

    for k in list(DEFAULT_CFG.keys()):
        if k not in cfg:
            cfg[k] = DEFAULT_CFG[k]

    return cfg

def save_user_config(cfg, base_dir=None):
    root = base_dir or repo_root()
    _, p_user = cfg_paths(root)
    os.makedirs(os.path.dirname(p_user), exist_ok=True)
    with open(p_user, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    return p_user
