#!/usr/local/bin/python

import json
import os
import time
from typing import Any, Type, TypeVar


def update_config(**values: Any):
    fname = "common_site_config.json"
    if not os.path.exists(fname):
        with open(fname, "a") as f:
            json.dump({}, f)

    with open(fname, "r+") as f:
        config: dict[str, Any] = json.load(f)
        config.update(values)
        f.seek(0)
        f.truncate()
        json.dump(config, f)


_T = TypeVar("_T")


def env(name: str, type_: Type[_T] = str) -> _T:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f'Required environment variable "{name}" not set')
    try:
        value = type_(value)
    except Exception:
        raise RuntimeError(
            f'Cannot convert environment variable "{name}" to type "{type_}"'
        )
    return value


def generate_redis_url(url: str):
    return f"redis://{url}"


def main() -> int:
    update_config(
        db_host=env("DB_HOST"),
        db_port=env("DB_PORT", int),
        redis_cache=generate_redis_url(env("REDIS_CACHE")),
        redis_queue=generate_redis_url(env("REDIS_QUEUE")),
        redis_socketio=generate_redis_url(env("REDIS_SOCKETIO")),
        socketio_port=env("SOCKETIO_PORT", int),
    )
    time.sleep(10)
    os.system("bench new-site " + env("SITE_NAME") + " --mariadb-root-password " + env("MYSQL_ROOT_PASSWORD") + " --admin-password " + env("ADMIN_PASSWORD") + " --install-app erpnext --install-app erpnext_chinese --install-app erpnext_oob")
    os.system("bench --site " + env("SITE_NAME") + " migrate")
    os.system("bench --site " + env("SITE_NAME") + " clear-cache")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
