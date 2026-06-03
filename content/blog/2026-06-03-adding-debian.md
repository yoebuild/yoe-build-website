+++
title = "Adding Debian — and what it weighs"
description = "[yoe] now builds Debian images alongside Alpine. Each backend is a real tradeoff — Debian brings a far larger package catalog, Alpine a much smaller and faster image — measured side by side on the same target."
date = 2026-06-03
[taxonomies]
tags = ["progress", "platform"]
+++

`[yoe]` started Alpine-first: musl, busybox, OpenRC, and `apk`. That stack is
small, fast, and clean to wrap, and it remains the default for new projects. But
not every workload fits it. Some binaries are built for glibc and never ported
to musl — CUDA, vendor camera and radio drivers, a lot of enterprise software.
Some teams already run a Debian/Ubuntu-based fleet and want their edge devices
to match it. And the apt ecosystem is vast.

So `[yoe]` now has a second backend: Debian. The
[latest video](https://youtu.be/16pxjZaw-Wo) walks through it. The same project
can build Alpine and Debian images side by side, choosing the distro per image.
A unit's source build runs in whichever toolchain the consuming image needs —
musl for an Alpine image, glibc for a Debian one — and produces a libc-correct
binary either way. You pick the platform the workload requires, image by image.

## The same machinery, a much bigger feed

Under the hood, the Debian backend reuses the unit model Alpine already runs on.
`[yoe]` targets Trixie, Debian's current stable release, and Debian main alone
exposes nearly 69,000 packages — against roughly 25,000 in Alpine's `main` and
`community` repos combined. Rather than ingest all of that up front, `[yoe]`
parses the package index files on startup and materializes units on demand,
exactly as it does for Alpine. Even against a feed that size, the TUI still
comes up in about a second.

The one place the two worlds diverge is naming. The same library often goes by a
different package name on each base — Python is `python3` on Alpine but
`python3.11` on Debian — so a unit now carries per-distro build and runtime
dependencies, and the build system resolves the right ones for the image it's
assembling. Some source packages needed adjusting to compile cleanly against
either base, but once that's done a single unit builds on both. Picking a
platform is then just a project setting: flip the default distro between Alpine
and Debian and rebuild.

## Choose per image, pay only where you need it

`[yoe]` lets you reach for the base distribution without committing the whole
project to it. If you don't have a hard reason for Debian — a glibc-only
library, a vendor binary, an existing Debian fleet — Alpine keeps the image
small and the defaults work. If you do, Debian's plumbing is there: feeds
resolve, packages mirror, the rootfs assembles in a single `mmdebstrap` pass,
and the project's own repo emits a signed index.

The pattern this enables is mixing the two in one project — a glibc Debian host
image running vendor agents and a container runtime, with small musl Alpine
application containers deployed inside it. The host pays for compatibility where
it needs it; the workloads stay lean. You spend the extra megabytes exactly
once, exactly where they earn their place, instead of across the whole device.

## The tradeoff is size

Debian buys compatibility, and it costs space. To measure that honestly, we
built the same minimal image on each backend: the smallest thing that boots and
accepts an SSH login, with no extra developer tooling on either side. Just a
kernel, an init system, libc, a shell, the package manager, `sshd`, DHCP
networking, and a login user. Same job, same `qemu-x86_64` target.

| Backend | Packages available | Minimal `ssh-image` rootfs | Dev image assembly |
| ------- | ------------------ | -------------------------- | ------------------ |
| Alpine  | ~25,000            | 85 MB                      | ~10 s              |
| Debian  | ~69,000            | 405 MB                     | ~100 s             |

Debian's draw is the catalog — about 69,000 packages in `main`, against Alpine's
~25,000 across `main` and `community`. The cost is size and time: roughly 4.8×
on disk — the apples-to-apples platform floor for a real device you can log into
— and close to 10× in assembly. The build-time column is the cached
image-assembly step for the dev image, a notch up from this minimal one; the
sections below break down where each gap comes from.

## Where the difference comes from

Two things, and most of it is the kernel.

**The kernel.** Most of the gap is the stock `linux-image-amd64` package — its
module tree alone is about 107 MB, because a distribution kernel ships a driver
for every machine it might ever run on. Alpine here boots a kernel `[yoe]` built
from source, tailored to the target, so its modules are a few megabytes rather
than a hundred-plus. This part of the gap isn't really "Debian vs Alpine" — it's
"stock distribution kernel vs tailored build," and a production Debian image on
`[yoe]` can swap in a tailored kernel too. Out of the box, though, the distro
kernel brings everything.

**The userland.** The remainder is the platform itself: glibc and its multiarch
libraries, systemd and NetworkManager, the full apt and dpkg stack, complete
coreutils instead of busybox applets, locales, udev rules. musl plus busybox
plus OpenRC is simply a lighter foundation, and on a device that difference
compounds.

## Size isn't the only difference — assembly is heavier too

The two images are also assembled differently, and it comes down to what a
package _does_ when it installs.

Assembling the Alpine image is essentially one step: `apk` extracts the packages
into the root filesystem, resolves their dependencies, and checks for file
conflicts. Alpine packages are largely self-contained — the install-time logic
is minimal, mostly busybox wiring up its own applet symlinks. Few moving parts,
and it's fast.

A Debian `.deb` carries maintainer scripts — `preinst`, `postinst` — that have
to run to finish the install: creating users, enabling systemd services, running
`ldconfig`, registering alternatives. So `[yoe]` assembles the Debian rootfs
with `mmdebstrap` driving `apt` and `dpkg`, then runs every package's scripts to
reach a fully configured state. And because those scripts assume a complete base
system is already in place, assembly carries ordering subtleties the Alpine path
never hits. A concrete one: `openssh-server`'s post-install reaches for `awk`
before the package that provides it has been configured, so the assembler
pre-stages the `awk` alternative ahead of time to keep the script from failing.
For a foreign architecture, all of those scripts run under QEMU emulation as
well.

None of this is a knock on Debian — that maintainer-script model is exactly what
makes the broad apt ecosystem drop in and _just work_, users and services
configured the way the package author intended. It's the same tradeoff as the
size: the richness that earns Debian its place is also what makes it heavier to
assemble. Alpine does less at install time, so there's less to do at build time.

It shows up on the clock, too. With every dependency package already built and
cached — so the timer captures only the image-assembly step, not the source
builds behind it — reassembling the dev image (a working image with editors and
diagnostics, a notch up from the minimal one measured above) on the same
`qemu-x86_64` target takes about **10 seconds on Alpine and roughly 100 on
Debian**: close to a 10× gap. Alpine's side is a single `apk` extract; Debian's
is `mmdebstrap` plus `dpkg` configuring every package and running its maintainer
scripts, under QEMU for a foreign architecture. The Debian time also wanders
more from run to run (90–120 s), because it leans on apt and dpkg doing real
work rather than a near-deterministic unpack.

## Where it stands

Debian support is experimental but real: the image measured above boots and
accepts SSH, so it's a device you can log into and work on, not a paper target.
The build path is solid and the size numbers are measurements, not estimates.
There's still plenty to harden, and honest comparisons — like this one — are how
we keep the tradeoffs in view as it matures.

## What's next

Hardening the Debian path from experimental toward production — tailoring the
kernel down from the stock one, and proving it out across more targets. The
[Videos page](/videos/) has the full walkthrough set.

If you have a workload that needs glibc, we'd love to hear how it goes —
[open a discussion](https://github.com/orgs/yoebuild/discussions) or send a
[note](mailto:info@yoebuild.org?subject=%5Byoe%5D%20Debian%20feedback). To
follow `[yoe]` as it grows,
[star and watch the repo](https://github.com/yoebuild/yoe) and
[subscribe for updates](/atom.xml) — there's an email signup at the foot of
every page, too.
