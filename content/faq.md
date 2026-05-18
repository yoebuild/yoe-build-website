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

[Naming is hard](https://martinfowler.com/bliki/TwoHardThings.html), and I don't
want to get distracted with hard things right now - that will hopefully come
later.

## What are the biggest risks this project faces?

Plenty — this is an experiment, and being honest about what could derail it
feels more useful than pretending otherwise.

1. **Adoption.** A build system is only useful if people use it. Yocto has two
   decades of vendor BSPs and community momentum. Growing an ecosystem of
   `[yoe]` units and BSPs from scratch is the single largest open question, and
   the path is long.
2. **Sustainability.** Today `[yoe]` is developed and funded by
   [BEC Systems](https://bec-systems.com/), who uses it for product development.
   If the work doesn't attract collaborators, sponsors, or users who depend on
   it, it could stall before it matures.
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
workload. CPU-bound C/C++ compilation pays the largest tax; I/O-heavy steps like
unpacking sources and assembling images feel closer to native. For day-to-day
iteration on x86_64, it's a reasonable trade for not having to manage a
cross-toolchain.

A few ways to mitigate when emulation overhead starts to bite:

- **Build natively on ARM hardware.** Apple Silicon Macs, Raspberry Pi 5, NVIDIA
  Jetson, or any ARM64 dev board build at full clock. Same `yoe` binary, same
  config — just faster.
- **Use ARM cloud instances.** AWS Graviton, Hetzner CAX, Oracle Ampere, and
  arm64 GitHub Actions runners run native ARM at sensible prices. A common
  pattern: iterate on x86 with QEMU, run CI and release builds on native ARM.
- **Let the cache do the work.** Every unit produces a content-addressed `.apk`.
  Once any machine has built a unit, every other developer pulls from the local,
  team, or shared cache instead of rebuilding. Most developers never run QEMU
  for unchanged units.

For a **small codebase or a handful of packages under active development**, QEMU
emulation on its own is usually fine. For a **large codebase or full image
builds**, combine the three above: develop on x86 with QEMU, run CI on native
ARM, and lean on the cache so nobody rebuilds anything they don't have to.

## Who is the customer?

A few overlapping audiences — and we're deliberately not optimizing for only one
of them yet:

- **Small product teams building edge devices.** Today's primary user. Teams who
  would otherwise stand up Yocto or Buildroot but want a faster loop and don't
  have a dedicated platform engineer to feed the build system.
- **Application developers on embedded teams.** Engineers writing Go, Rust, or
  Python services that run on a device, who need to integrate with the base
  image without learning a separate SDK.
- **System integrators and BSP authors.** Silicon vendors and consultancies
  shipping board support, looking for a clean place to publish units alongside
  others.

We pay most attention to the first group; when `[yoe]` makes their day faster,
the rest tends to follow. We are not targeting deep-compliance, frozen-SDK
shops, or teams of 1000s of engineers. — Bazel or Yocto may remain the right
choice there.

The problems a startup or ten-person product team faces aren't a smaller
version of an enterprise's — they're often different problems entirely. Tools built for
Google scale import that operational cost without the payoff (the
[_You Are Not Google_](https://blog.bradfieldcs.com/you-are-not-google-84912cf44afb)
point — and why so many small teams end up running Kubernetes to deploy three
containers). `[yoe]` is calibrated for the problems small teams and startups
actually have.

Optimizing for small teams isn't a niche bet. Small and independent businesses
are the foundation of the global economy —
[over 90% of all firms and roughly 70% of employment worldwide](https://www.ifc.org/en/what-we-do/msme-day)
(IFC / World Bank Group) — and new business formation sits at historic highs in
many markets. Connected-hardware teams ride the same curve as silicon and
tooling keep getting cheaper. Building the best tool for that group aims at
where the work is heading, not a corner of it.

## Is this fully open source? What is the business strategy?

Apache 2.0, intentionally. The aim is closer to
[Zephyr](https://zephyrproject.org/) than to a startup exit: a vendor-neutral
project that multiple companies depend on, contribute to, and ship products
with. Concretely:

- **The team developing `[yoe]` today is
  [BEC Systems](https://bec-systems.com/),** who uses it to accelerate their own
  embedded product work. Sponsorship, support, and consulting around `[yoe]` are
  part of how the work is funded.
- **No exit plan, no IP holdback.** The code, units, and docs are all open.
  There is no proprietary tier we're holding back to sell later.
- **Potential collaborators** roughly: silicon vendors who want a clean way to
  ship BSPs, OTA / update vendors (Mender, RAUC, ostree-based teams) who want a
  build system that composes with their update story, edge-AI platforms that
  need to integrate ML workloads cleanly, and consultancies who would rather
  build on a shared base than maintain a private fork.
- **Lateral technologies that might trade interestingly:** container runtimes on
  the device, shared artifact / apk feed infrastructure, AI workflows that span
  dev / devops / oncall, and bridges to the larger distribution package
  ecosystems.
- **Hosting of build services:** once a distributed build mechanism is
  implemented, it would be useful to have accessed to cloud build services for
  ARM/RISC-V components that don't build easily on your local computer. This is
  a useful commercial service that may be provided by BEC and other companies in
  the future.

If any of that resonates and you'd like to help fund or steer a piece of it,
[come talk to us](mailto:info@yoebuild.org?subject=%5Byoe%5D%20collaboration).

## How will LLM costs be controlled with so much build data?

A few design choices keep the cost bounded:

- **The LLM isn't in the build loop.** Routine builds are deterministic Go and
  Starlark with no model calls. Cache hits, full rebuilds, image assembly — none
  of those invoke a model. The AI shows up for specific developer actions:
  creating a unit, diagnosing a failed build, asking why a package is in the
  image, auditing for CVEs.
- **Structured inputs, not raw logs.** Starlark units, a queryable dependency
  graph, and structured build logs let the model work against compact,
  semantically rich representations. "Diagnose this build failure" ships the
  relevant unit, the failing step, and a focused window of the error — not the
  entire log.
- **The user supplies the model.** API keys (and, increasingly, locally hosted
  models) come from the developer. The project doesn't need to absorb model
  costs centrally to be useful.
- **Smaller models for routine tasks.** Many workflows (CVE checks, license
  audits, "why is this package here?") run fine against a smaller, cheaper
  model. We try to default to the cheapest model that gives a good answer for
  each task.

We don't claim cost is solved. As more AI workflows ship, the right defaults
will shift, and we'll lean on open metrics to keep them honest.

## What about glibc, systemd, Debian, or Ubuntu?

A fair question — these are the defaults most engineers know from servers and
desktops, and they're worth supporting on edge devices too.

The current focus is the **tooling and build architecture** — the unit model,
the TUI/CLI/AI interfaces, caching, and the iteration loop. Getting that
foundation right matters more right now than covering every base ecosystem on
day one. Once the core is solid, adding bases is a much smaller lift.

We're starting with an **Alpine base** because it's simple and lightweight: a
small musl rootfs, the `apk` package format, and a clean set of well-maintained
packages to compose from. That makes the early iterations of `[yoe]` easy to
reason about and quick to build.

The architecture isn't tied to Alpine, though. A unit defines how its inputs
turn into outputs; the base distribution is just another set of inputs. Once the
foundation is in shape, we plan to add a **Debian / Ubuntu base** following the
same pattern we use for Alpine — pulling packages from the upstream archive and
composing them into images. That brings glibc, systemd, and the broader Debian
package ecosystem within reach for products that want them.

Further out, **building entirely from source** is also on the table for teams
who need maximum control over toolchains, patches, and provenance — closer in
spirit to a Yocto-style build, but using the same units and graph model `[yoe]`
already provides.

The short version: tooling first, then Alpine today, Debian / Ubuntu next, fully
from source eventually. Same build system, same units, different bases.

## How will the global cache be implemented?

The cache design already has three layers: **local** (in the project tree),
**team** (a private or shared apk feed), and **global / community** (the long
tail of prebuilt units that anyone can pull). The local layer is straightforward
and works today. The global layer is the harder part — and it's fundamentally an
operational and funding problem, not a technical one.

It's the same problem Debian, Alpine, Arch, NixOS, and the language registries
have all had to solve: someone has to pay for storage, bandwidth, and a CDN that
scales with adoption. The answers vary — university and ISP mirror networks,
foundations funded by donations, donated infrastructure from cloud providers
(Fastly for PyPI, AWS for cache.nixos.org), corporate sponsors — but the
principle is the same: **the artifacts are free, but the hosting isn't.**

For `[yoe]` we plan to start small and let demand pull the model into shape:

- **Today** — projects publish their unit modules to GitHub and their `.apk`
  packages to any HTTP-reachable feed. That's enough for individual teams and
  early users.
- **Next** — a community apk feed for common units (base system, popular BSPs,
  language toolchains) so most users don't have to rebuild from source. We're
  prototyping what this looks like.
- **Eventually** — a sustained hosting arrangement funded by the organizations
  that benefit most from the project. That likely means a mix of corporate
  sponsors, mirror donations, and possibly a foundation or fiscal host. This is
  not something one company can — or should — carry alone.

If your team would depend on, or be willing to contribute to, a community apk
cache for `[yoe]`, [tell us](mailto:info@yoebuild.org?subject=%5Byoe%5D%20cache)
— that signal helps us figure out when to invest in it.
