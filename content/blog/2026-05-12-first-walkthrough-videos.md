+++
title = "First Walkthroughs: Overview and Package Deploy"
description = "Two short videos covering what [yoe] feels like to use day-to-day — the build loop, and pushing a package to a running target."
date = 2026-05-12
[taxonomies]
tags = ["videos", "productivity"]
+++

A build system is easier to evaluate when you can watch it in motion. The first
two walkthroughs are up on the [Videos page](/videos/), and they cover the parts
of `[yoe]` that are most different from what you'd expect coming from Yocto or
Buildroot.

## Video 1 — Overview

A tour of the build system end-to-end: `yoe init` to scaffold a project, the
TUI with its live progress bar, background builds, search, and inline status —
all in one screen. Then `yoe run` to boot the resulting image in QEMU. The aim
is to show the full idea-to-running-image loop without an SDK install, a
cross-toolchain, or generated shell scripts to read through.

If you've only seen the
[earlier post](/blog/next-gen-embedded-linux/), this is the version where the
claims become concrete.

## Video 2 — Deploying packages

The iteration loop, zoomed in. Once an image is running, the interesting
question is how fast you can change a package on the target and try the new
version. This video walks through building a package, resolving its
dependencies, and pushing the result to a live target in a single step — no
full image rebuild, no manual `scp` dance.

This is the part of the experience that most rewards the design decisions in
[Hello, [yoe]](/blog/hello-yoe/): one binary, language-native package managers
composed in, and content-addressed `.apk` outputs that the target can install
directly.

## What's next

More videos are planned as features land — Docker on the target, Go and Rust
units, BSP authoring, and the AI-assisted workflows. The full playlist lives on
the [Videos page](/videos/), and the YouTube
[playlist](https://www.youtube.com/playlist?list=PL3XJli5z9VFd5c0xlrFZkqm_N0dOeWhPP)
is the place to subscribe if you'd like a ping when new ones go up.

Feedback is welcome — what would you want to see demoed next?
[Open a discussion](https://github.com/orgs/yoebuild/discussions) or send a
[note](mailto:info@yoebuild.org?subject=%5Byoe%5D%20video%20feedback).
