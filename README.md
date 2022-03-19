
[![Build Stable](https://github.com/frappe/frappe_docker/actions/workflows/build_stable.yml/badge.svg)](https://github.com/frappe/frappe_docker/actions/workflows/build_stable.yml)
[![Build Develop](https://github.com/frappe/frappe_docker/actions/workflows/build_develop.yml/badge.svg)](https://github.com/frappe/frappe_docker/actions/workflows/build_develop.yml)


# 官方docker file基础上修改了部分内容

## 一、复制配置模版 并修改.env 参数
```sh
cp example.env .env
```

## 二、生成 docker-compose.yml
```sh
docker-compose -f compose.yaml -f overrides/compose.erpnext_oob.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.redis.yaml -f overrides/compose.noproxy.yaml config > ./erpnext-oob/docker-compose.yml
```

## 三、启动 docker
```sh
docker-compose -f ./erpnext-oob/docker-compose.yml up -d
```

## PS  -如需更改其他 参见下方文档 
🔥🔥🔥 [erpnext_oob 汉化版仓库地址](https://gitee.com/yuzelin/erpnext_oob) 

Everything about [Frappe](https://github.com/frappe/frappe) and [ERPNext](https://github.com/frappe/erpnext) in containers.

# Getting Started

To get started, you need Docker, docker-compose and git setup on your machine. For Docker basics and best practices. Refer Docker [documentation](http://docs.docker.com).
After that, clone this repo:

```sh
git clone https://github.com/frappe/frappe_docker
cd frappe_docker
```

# Development

We have baseline for developing in VSCode devcontainer with [frappe/bench](https://github.com/frappe/bench). [Start development](development).

# Production

We provide simple and intuitive production setup with prebuilt Frappe and ERPNext images and compose files. To learn more about those, [read the docs](docs/images-and-compose-files.md).

Also, there's docs to help with deployment:

- [setup options](docs/setup-options.md),
- in cluster:
  - [Docker Swarm](docs/docker-swarm.md),
  - [Kubernetes (frappe/helm)](https://helm.erpnext.com),
- [site operations](docs/site-operations.md).
- Other
  - [add custom domain using traefik](docs/add-custom-domain-using-traefik.md)
  - [backup and push cron jobs](docs/backup-and-push-cronjob.md)
  - [bench console and vscode debugger](docs/bench-console-and-vscode-debugger.md)
  - [build version 10](docs/build-version-10-images.md)
  - [connect to localhost services from containers for local app development](docs/connect-to-localhost-services-from-containers-for-local-app-development.md)
  - [patch code from images](docs/patch-code-from-images.md)
  - [port based multi tenancy](docs/port-based-multi-tenancy.md)
- [Troubleshoot](docs/troubleshoot.md)

# Custom app

Learn how to containerize your custom Frappe app in [this guide](custom_app/README.md).

# Contributing

If you want to contribute to this repo refer to [CONTRIBUTING.md](CONTRIBUTING.md)

This repository is only for Docker related stuff. You also might want to contribute to:

- [Frappe framework](https://github.com/frappe/frappe#contributing),
- [ERPNext](https://github.com/frappe/erpnext#contributing),
- or [Frappe Bench](https://github.com/frappe/bench).
