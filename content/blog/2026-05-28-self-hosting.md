+++
title = "[yoe] Is Now Self-Hosting"
description = "The build system can build itself — boot a [yoe] image, run [yoe] on it, and build another image inside. The payoff is native ARM64 builds on a Raspberry Pi 5."
date = 2026-05-28
[taxonomies]
tags = ["videos", "progress"]
+++

`[yoe]` can now build itself. The [latest video](https://youtu.be/7KT3dWuFrx8)
walks through a short proof: build a `selfhost-image` with `[yoe]`, boot it in
QEMU, SSH in, and run `[yoe]` to build another image. The demo runs two levels
deep — host workstation, a QEMU instance built by `[yoe]`, and another `[yoe]`
build running inside that.

## What's in the image

The `selfhost-image` carries everything needed to develop with `[yoe]` on the
target: the `yoe` CLI, Docker with `buildx` and `containerd`, the Go
toolchain, `git`, `bubblewrap` for sandboxing, and the developer toolkit —
Helix, Yazi, Zellij. A first-boot service grows the rootfs to fill the
storage device.

## Two levels deep

The video runs `[yoe]` inside a QEMU instance that `[yoe]` built. SSH in from
another tab — the terminal behaves better than the QEMU console — and the
inner `base-image` build is already complete. Running the result needs a
port remap to avoid colliding with the outer QEMU and a memory cap below the
host's 4 GB. KVM is not available in the nested setup, so the inner boot is
a bit slower, but it boots and runs.

## Why it matters

The interesting case is not nested QEMU. It's a Raspberry Pi 5 with an NVMe
HAT acting as a standalone `[yoe]` build host. Builds run natively on ARM64
— no QEMU user-mode emulation in the loop — and right now that is the
fastest way to build an ARM image with `[yoe]`. It is also a step toward a
build farm of cheap ARM nodes.

The [self-host docs](https://docs.yoebuild.org/selfhost.html) cover the
hardware: Pi 5 with 8 GB of RAM (16 GB if you want concurrent kernel or LLVM
builds), NVMe via PCIe HAT for 10–20× the throughput of microSD, and a 27 W
USB-PD supply to drive it.

## What's next

V1 of `selfhost-image` is single-arch, with no A/B partitioning or headless
install yet. The [Videos page](/videos/) has the full walkthrough set. If
you'd like to see this run on different hardware or in a build-farm
configuration,
[open a discussion](https://github.com/orgs/yoebuild/discussions) or send a
[note](mailto:info@yoebuild.org?subject=%5Byoe%5D%20self-host%20feedback).
