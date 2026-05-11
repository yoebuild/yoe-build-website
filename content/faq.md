+++
title = "FAQ"
description = "Answers to common questions about the [yoe] next-generation build system."
template = "page.html"
+++

A running list of questions we've heard while sharing the work. If you have one
that isn't here,
[open a discussion](https://github.com/orgs/yoebuild/discussions) or send us a
[note](mailto:info@yoebuild.org?subject=%5Byoe%5D%20question) — we'll add it.

## Why the name "yoe build"?

The name is purely a convenience for now. This project has no formal
relationship with the well-established
[Yoe Distribution](https://yoedistro.org/), other than taking inspiration from
its principles. If you're looking for that project, head over to
[yoedistro.org](https://yoedistro.org/).

## What are the biggest risks this project faces?

Plenty — this is an experiment, and being honest about what could derail it
feels more useful than pretending otherwise.

1. **Adoption.** A build system is only useful if people use it. Yocto has two
   decades of vendor BSPs and community momentum. Growing an ecosystem of
   `[yoe]` units and BSPs from scratch is the single largest open question, and
   the path is long.
2. **Sustainability.** Today this is a small team supported by
   [BEC Systems](https://bec-systems.com/). If the work doesn't attract
   collaborators, sponsors, or users who depend on it, it could stall before it
   matures.
3. **Technical bets that may not pan out.** Native-only builds, Starlark plus AI
   as a primary interface for new units, and `apk` as the package format are all
   bets that look right today but haven't been tested across a wide variety of
   products at scale. Any of them could need a rethink.
4. **Scope.** A TUI, a CLI, AI workflows, multiple architectures, containers,
   OTA — it is a lot to do well. Staying focused on the goals above, and saying
   no to nearby-but-different problems, will be a constant discipline.

We'd rather name these risks than ignore them. If any resonate — especially if
you'd help mitigate one —
[come talk to us](https://github.com/orgs/yoebuild/discussions).

## How slow is QEMU user-mode emulation? Is it usable?

Yes, it's slower than native — roughly **5–20× slower** depending on the
workload. CPU-bound C/C++ compilation pays the largest tax; I/O-heavy steps
like unpacking sources and assembling images feel closer to native. For
day-to-day iteration on x86_64, it's a reasonable trade for not having to
manage a cross-toolchain.

A few ways to mitigate when emulation overhead starts to bite:

- **Build natively on ARM hardware.** Apple Silicon Macs, Raspberry Pi 5,
  NVIDIA Jetson, or any ARM64 dev board build at full clock. Same `yoe` binary,
  same config — just faster.
- **Use ARM cloud instances.** AWS Graviton, Hetzner CAX, Oracle Ampere, and
  arm64 GitHub Actions runners run native ARM at sensible prices. A common
  pattern: iterate on x86 with QEMU, run CI and release builds on native ARM.
- **Let the cache do the work.** Every unit produces a content-addressed
  `.apk`. Once any machine has built a unit, every other developer pulls from
  the local, team, or shared cache instead of rebuilding. Most developers never
  run QEMU for unchanged units.

For a **small codebase or a handful of packages under active development**,
QEMU emulation on its own is usually fine. For a **large codebase or full
image builds**, combine the three above: develop on x86 with QEMU, run CI on
native ARM, and lean on the cache so nobody rebuilds anything they don't have
to.
