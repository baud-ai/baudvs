<div align="center">
  <img src="assets/vearch_logo.png">
  <p>
    <a href="https://github.com/vearch/vearch/blob/master/README_ZH_CN.md">简体中文</a> | <a href="https://github.com/vearch/vearch/blob/master/README.md">English</a>
  </p>
</div>

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](./LICENSE)
[![Build Status](https://github.com/vearch/vearch/actions/workflows/CI.yml/badge.svg)](https://github.com/vearch/vearch/actions/workflows/CI.yml)
[![Gitter](https://badges.gitter.im/vector_search/community.svg)](https://gitter.im/vector_search/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

## 简介

Vearch 是一个云原生分布式向量数据库，用于在 AI 应用程序中对向量进行高效的相似性搜索。

## 主要特性

- **混合检索**: 向量搜索和标量过滤。

- **性能**: 快速矢量检索 - 在几毫秒内搜索数百万个对象。

- **可扩展性和可靠性**: 弹性扩展和高可用。

## 文档

### Restful 接口

- [参考文档](https://vearch.readthedocs.io/zh_CN/latest)

### OpenAPIS

- [Tutorial](https://vearch.github.io/tools#/)

### 开发手册

- **[Python SDK](sdk/python/README.md)**

- **[Go SDK](sdk/go/README.md)**

- **[Java SDK(under development)](sdk/java/README.md)**

## 使用案例

### 大模型记忆后端

- **[Langchain](sdk/integrations/langchain/README.md)**

- **[LlamaIndex](sdk/integrations/llama-index/README.md)**

- **[Langchaingo](sdk/integrations/langchaingo/vearchREADME.md)**

### 实际场景

- **[图片检索插件](docs/Quickstart.md)**: Vearch 可用于构建完整的视觉搜索系统来索引数十亿张图像。 还需要用于对象检测和特征提取的图像检索插件。

## 快速开始

**[k8s 部署 Vearch 集群](https://vearch.github.io/vearch-helm/)**

**通过仓库添加 charts**

```
$ helm repo add vearch https://vearch.github.io/vearch-helm
$ helm repo update && helm install my-release vearch/vearch
```

**本地添加 charts**

```
$ git clone https://github.com/vearch/vearch-helm.git && cd vearch-helm
$ helm install my-release ./charts -f ./charts/values.yaml
```

**通过 docker-compose 使用 vearch**

单节点模式

```
$ cd cloud
$ cp ../config/config.toml .
$ docker-compose --profile standalone up -d
```

集群模式

```
$ cd cloud
$ cp ../config/config_cluster.toml .
$ docker-compose --profile cluster up -d
```

**Docker 编译部署**: 通过 vearch docker 镜像快速使用，请查看 [docker 编译部署](docs/DeployByDockerZH_CN.md).

**源码编译部署**: 通过源码快速编译部署，请查看 [源码编译部署](docs/SourceCompileDeploymentZH_CN.md).

## 组件

**Vearch 架构**

![arc](assets/architecture.excalidraw.png)

**Master**: 负责模式管理、集群级元数据和资源协调。

**Router**: 提供 RESTful API：`upsert`、`delete`、`search` 和 `query` ； 请求路由和结果合并。

**PartitionServer (PS)**: 使用基于 raft 的复制托管文档分区。 Gamma 是基于[faiss](https://github.com/facebookresearch/faiss)实现的核心矢量搜索引擎，提供了存储、索引和检索向量和标量的能力。

## 引用参考

在研究论文中使用 Vearch 时的引用参考：

```
@misc{li2019design,
      title={The Design and Implementation of a Real Time Visual Search System on JD E-commerce Platform},
      author={Jie Li and Haifeng Liu and Chuanghua Gui and Jianyu Chen and Zhenyun Ni and Ning Wang},
      year={2019},
      eprint={1908.07389},
      archivePrefix={arXiv},
      primaryClass={cs.IR}
}
```

## 社区

可以在[问题页面](https://github.com/vearch/vearch/issues)中报告错误或提出问题。

如需对 Vearch 进行公开讨论或提出问题，您还可以发送电子邮件至 vearch-maintainers@groups.io。

slack：https://vearchworkspace.slack.com

## 用户

欢迎在此 issue https://github.com/vearch/vearch/issues/230 中登记公司名称

![Users](assets/company_logos/all.jpg)

## 开源许可

根据 Apache 许可证 2.0 版本授权。详细请参见 [LICENSE and NOTICE](https://github.com/vearch/vearch/blob/master/LICENSE).
