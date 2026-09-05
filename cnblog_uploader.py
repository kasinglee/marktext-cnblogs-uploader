#!/usr/bin/env python3
"""Upload an image directly to cnblogs for MarkText's CLI Script uploader."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import xmlrpc.client
from pathlib import Path
from typing import Any


VERSION = "1.0.0"


class UploadError(RuntimeError):
    """A user-facing configuration or upload error."""


def config_path() -> Path:
    configured = os.environ.get("CNBLOG_CONFIG")
    if configured:
        return Path(configured).expanduser().resolve()
    base = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
    return base / "config.json"


def load_config(path: Path | None = None) -> dict[str, str]:
    path = path or config_path()
    try:
        data: Any = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise UploadError(f"找不到配置文件: {path}，请创建并填写 config.json。") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise UploadError(f"配置文件无法读取: {path}: {exc}") from exc

    required = ("blog_url", "blog_id", "username", "access_token")
    missing = [key for key in required if not str(data.get(key, "")).strip()]
    if missing:
        raise UploadError(f"配置缺少必填项: {', '.join(missing)}")
    return {key: str(data[key]).strip() for key in required}


def upload_image(image: Path, config: dict[str, str], server: Any | None = None) -> str:
    if not image.is_file():
        raise UploadError(f"图片不存在或不可读: {image}")
    try:
        content = image.read_bytes()
    except OSError as exc:
        raise UploadError(f"无法读取图片: {image}: {exc}") from exc

    payload = {
        "bits": xmlrpc.client.Binary(content),
        "name": image.name,
        "type": mimetypes.guess_type(image.name)[0] or "application/octet-stream",
    }
    try:
        if server is None:
            server = xmlrpc.client.ServerProxy(config["blog_url"], allow_none=True)
        result = server.metaWeblog.newMediaObject(
            config["blog_id"], config["username"], config["access_token"], payload
        )
    except xmlrpc.client.Fault as exc:
        raise UploadError(
            f"博客园接口拒绝请求 (XML-RPC {exc.faultCode}): {exc.faultString}"
        ) from exc
    except (OSError, xmlrpc.client.Error) as exc:
        raise UploadError(f"博客园图片上传失败: {exc}") from exc

    url = result.get("url") if isinstance(result, dict) else None
    if not isinstance(url, str) or not url.strip():
        raise UploadError(f"博客园返回结果中没有图片 URL: {result!r}")
    return url.strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="将图片直接上传到博客园，供 MarkText 使用。")
    parser.add_argument("--version", action="version", version=f"cnblog_uploader {VERSION}")
    parser.add_argument("image", type=Path, help="MarkText 传入的本地图片路径")
    parser.add_argument("--config", type=Path, help="配置文件路径，优先于 CNBLOG_CONFIG")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        print(upload_image(args.image.expanduser().resolve(), config), flush=True)
    except UploadError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
