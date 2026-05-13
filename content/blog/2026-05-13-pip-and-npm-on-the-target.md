+++
title = "Pip and Npm Belong on the Target too"
description = "How [yoe] packages Python virtual environments and Node/Bun dependency trees so application developers keep the workflow they already use."
date = 2026-05-13
[taxonomies]
tags = ["videos", "productivity"]
+++

Application developers reach for `pip install` or `npm install` without
thinking. The moment that code needs to land on an embedded Linux target, the
same one-line dependency install usually becomes a hand-written recipe per
package. That's the friction the
[third walkthrough](https://youtu.be/c2G9NdEi_p4) aims to remove.

## The idea

Let the language's own package manager do the resolution. Capture its output.
Ship it.

`[yoe]` now has units for three runtimes:

- **[Python](https://docs.yoebuild.org/python.html)** — a virtual-environment
  class creates a venv named after the unit, runs `pip install`, and packages
  the resulting venv as an `.apk` that the target installs directly. Each
  application gets its own venv, so dependencies stay isolated.
- **[Node.js](https://docs.yoebuild.org/nodejs.html)** — `npm install` runs at
  build time, and `node_modules/` rides along with the app in the same package.
- **[Bun](https://docs.yoebuild.org/bun.html)** — same flow as Node, but with
  the lighter-weight Zig-based runtime. Worth a look if you want a smaller
  footprint than full Node on the target.

The unit author writes the same dependency manifest they'd write on their laptop
— `requirements.txt`, `package.json`. The build system handles the rest.

## Why this matters

Two of the goals in [Hello, [yoe]](/blog/hello-yoe/) and
[What a Modern Embedded Linux Build System Could Look Like](/blog/next-gen-embedded-linux/)
were: don't reinvent dependency resolution, and don't force application
developers to learn a second packaging system to ship what they already wrote.
This is what that looks like in practice — pip, npm, and bun composed in rather
than replaced.

## What's next

Rust and Zig units are queued up next, along with Python ML workloads where the
dependency graph gets a lot more interesting. The
[YouTube playlist](https://www.youtube.com/playlist?list=PL3XJli5z9VFd5c0xlrFZkqm_N0dOeWhPP)
is the place to subscribe for new walkthroughs as features land.

What scripting-language workflow would you like to see demoed next?
[Open a discussion](https://github.com/orgs/yoebuild/discussions) or send a
[note](mailto:info@yoebuild.org?subject=%5Byoe%5D%20video%20feedback).
