+++
title = "What a Modern Embedded Linux Build System Could Look Like"
description = "Seven weeks in: where [yoe] stands on productivity, complex workloads, and scaling to anything."
date = 2026-05-11
[taxonomies]
tags = ["progress", "productivity", "containers"]
+++

Seven weeks ago we [started experimenting](https://yoebuild.org/) to find out.
The result is a tool that builds QEMU and Raspberry Pi images today, with Docker
support working. The goals driving the project, and where each one stands so
far:

1. **Drastically improve developer productivity** — shrink the loop between an
   idea and a running image. Today: one binary, no SDK to install.
   `yoe init && yoe` opens a TUI with a live build progress bar, and `yoe run`
   boots the image in QEMU. Background builds, search, and inline status sit in
   one screen.
2. **Easily integrate complex workloads** — let modern languages keep their own
   package managers, and let containers ride along. Today: Go modules build
   end-to-end, and Docker runs on the resulting image. Rust, Zig, and Python ML
   come next.
3. **Scale to build anything** — one tool, one mental model from small images to
   distributed systems. Today: two modules (`module-core`, `module-rpi`)
   covering x86_64 QEMU and Raspberry Pi, with QEMU user-mode emulation building
   ARM64 on x86 — no cross-toolchain. Zephyr, AI workloads, distributed builds,
   and farm-scale caching are still ahead.

There is a long way to go, and the risks are real. But seven weeks in — 38
releases, a working build flow — the path forward feels solid.

![](/images/yoe-build.png)
