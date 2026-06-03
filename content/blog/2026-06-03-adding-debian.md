+++
title = "Adding Debian — and what it weighs"
description = "[yoe] now builds Debian images alongside Alpine. Picking between them is a real tradeoff, so here is the same dev image on both backends and the size difference between them."
date = 2026-06-03
[taxonomies]
tags = ["progress", "platform"]
+++

`[yoe]` started Alpine-first: musl, busybox, OpenRC, and `apk`. That stack is
small, fast, and clean to wrap, and it remains the default for new projects. But
not every workload fits it. Some binaries are built for glibc and never ported
to musl — CUDA, vendor camera and radio drivers, a lot of enterprise software.
Some teams already run a Debian-based fleet and want their edge devices to match
it. And the apt ecosystem is vast.

So `[yoe]` now has a second backend: Debian. The same project can build Alpine
images and Debian images side by side, choosing the distro per image. A unit's
source build runs in whichever toolchain the consuming image needs — musl for an
Alpine image, glibc for a Debian one — and produces a libc-correct binary either
way. You pick the platform the workload requires, image by image.

## The tradeoff is size

Debian buys compatibility, and it costs space. To measure that honestly, we
built the same minimal image on each backend: the smallest thing that boots and
accepts an SSH login, with no extra developer tooling on either side. Just a
kernel, an init system, libc, a shell, the package manager, `sshd`, DHCP
networking, and a login user. Same job, same `qemu-x86_64` target.

| Minimal boot + SSH image | Root filesystem |
| ------------------------ | --------------- |
| Alpine `ssh-image`       | 85 MB           |
| Debian `ssh-image`       | 731 MB          |

That's about 8.6× — and it's the apples-to-apples number, the platform floor for
a real device you can log into.

## Where the difference comes from

Two things, in roughly equal measure.

**The kernel.** About 440 MB of Debian's 731 MB — 60% of the image — is the stock
`linux-image-amd64` package. Its module tree alone is 395 MB, because a
distribution kernel ships a driver for every machine it might ever run on. Alpine
here boots a kernel `[yoe]` built from source, tailored to the target, so its
modules are a few megabytes rather than hundreds. This part of the gap isn't
really "Debian vs Alpine" — it's "stock distribution kernel vs tailored build,"
and a production Debian image on `[yoe]` can swap in a tailored kernel too. Out
of the box, though, the distro kernel brings everything.

**The userland.** The other ~290 MB is the platform itself: glibc and its
multiarch libraries, systemd and NetworkManager, the full apt and dpkg stack,
complete coreutils instead of busybox applets, locales, udev rules. Alpine's
entire 85 MB — tailored kernel included — is smaller than Debian's userland alone.
musl plus busybox plus OpenRC is simply a lighter foundation, and on a device
that difference compounds.

## Size isn't the only difference — assembly is heavier too

The two images are also built in very different ways, and it comes down to what a
package *does* when it installs.

Assembling the Alpine image is essentially one step: `apk` extracts the packages
into the root filesystem, resolves their dependencies, and checks for file
conflicts. Alpine packages are largely self-contained — the install-time logic is
minimal, mostly busybox wiring up its own applet symlinks. Few moving parts, and
it's fast.

A Debian `.deb` carries maintainer scripts — `preinst`, `postinst` — that have to
run to finish the install: creating users, enabling systemd services, running
`ldconfig`, registering alternatives. So `[yoe]` assembles the Debian rootfs with
`mmdebstrap` driving `apt` and `dpkg`, then runs every package's scripts to reach
a fully configured state. And because those scripts assume a complete base system
is already in place, assembly carries ordering subtleties the Alpine path never
hits. A concrete one: `openssh-server`'s post-install reaches for `awk` before
the package that provides it has been configured, so the assembler pre-stages the
`awk` alternative ahead of time to keep the script from failing. For a foreign
architecture, all of those scripts run under QEMU emulation as well.

None of this is a knock on Debian — that maintainer-script model is exactly what
makes the broad apt ecosystem drop in and *just work*, users and services
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

## Choose per image, pay only where you need it

The takeaway isn't "Alpine wins." It's that the two are genuinely different
tools, and `[yoe]` lets you reach for the right one without committing the whole
project to it. If you don't have a hard reason for Debian — a glibc-only library,
a vendor binary, an existing Debian fleet — Alpine keeps the image small and the
defaults work. If you do, Debian's plumbing is there: feeds resolve, packages
mirror, the rootfs assembles in a single `mmdebstrap` pass, and the project's
own repo emits a signed index.

The pattern this really enables is mixing the two in one project — a glibc Debian
host image running vendor agents and a container runtime, with small musl Alpine
application containers deployed inside it. The host pays for compatibility where
it needs it; the workloads stay lean. You spend the extra megabytes exactly once,
exactly where they earn their place, instead of across the whole device.

## Where it stands

Debian support is experimental but real: the image measured above boots and
accepts SSH, so it's a device you can log into and work on, not a paper target.
The build
path is solid and the size numbers are measurements, not estimates. There's still
plenty to harden, and honest comparisons — like this one — are how we keep the
tradeoffs in view as it matures. If you have a workload that needs glibc and want
to try it, we'd love to hear how it goes.
