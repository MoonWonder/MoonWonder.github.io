---
title: 如何输出指定内容
subtitle:
date: 2025-09-09T20:45:48+08:00
draft: false
author:
  name:
  link:
  email:
  avatar:
description:
keywords:
license:
comment: true
weight: 0
tags:
  - draft
categories:
  - draft
hiddenFromHomePage: false
hiddenFromSearch: false
hiddenFromRelated: false
hiddenFromFeed: false
summary:
resources:
  - name: featured-image
    src: featured-image.jpg
  - name: featured-image-preview
    src: featured-image-preview.jpg
toc: true
math: false
lightgallery: false
password:
message:

# See details front matter: https://fixit.lruihao.cn/documentation/content-management/introduction/#front-matter
lastmod: 2025-09-09T20:48:46+08:00
---

在调用LLM api时我们有时候想让他只输出指定的token

<!--more-->


1. 使用logit bias:
  ```python
  logit_bias = {
    'yes': 100,
    'no': 100,
  }
  response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": question}
        ],
        max_tokens=1,
        logit_bias=logit_bias,
        temperature=0.1
    )
  ```
2. 使用toplogprobs
  ```python
  response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": question}
    ],
    max_tokens=1,
    logprobs=True,
    top_logprobs=10,
    temperature=0.1
  )

  # 提取 logits 并根据大小排个序
  sorted_words = sorted(response.choices[0].logprobs.content[0].top_logprobs, key=lambda prob : prob.logprob, reverse=True)
  sorted_words

  ```
  #### output
  ```
  [TopLogprob(token='Yes', bytes=[89, 101, 115], logprob=0.0),
 TopLogprob(token='Most', bytes=[77, 111, 115, 116], logprob=-172.36865),
 TopLogprob(token='Whether', bytes=[87, 104, 101, 116, 104, 101, 114], logprob=-235.70471),
 TopLogprob(token='The', bytes=[84, 104, 101], logprob=-251.10486),
 TopLogprob(token='**', bytes=[42, 42], logprob=-304.20667),
 TopLogprob(token='B', bytes=[66], logprob=-338.26758),
 TopLogprob(token='Generally', bytes=[71, 101, 110, 101, 114, 97, 108, 108, 121], logprob=-339.76685),
 TopLogprob(token='Certainly', bytes=[67, 101, 114, 116, 97, 105, 110, 108, 121], logprob=-357.7478),
 TopLogprob(token='Not', bytes=[78, 111, 116], logprob=-391.34668),
 TopLogprob(token='In', bytes=[73, 110], logprob=-420.53528)]
  ```