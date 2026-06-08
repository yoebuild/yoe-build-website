+++
title = "Adding Ubuntu — almost for free"
description = "[yoe] now builds Ubuntu images too. Because it's apt underneath, the second distro in the family cost a fraction of the first — the backend isn't Debian support, it's apt-family support."
date = 2026-06-08
[taxonomies]
tags = ["videos", "platform"]
+++

Standing up the Debian backend was real work — `mmdebstrap` rootfs assembly,
`.deb` packaging, on-device apt, a glibc toolchain alongside the musl one. Adding
Ubuntu on top of that was almost free. The
[latest video](https://youtu.be/VeKhu03FqBE) walks through it, and the headline
is how little there was to do: Ubuntu is apt, so it rides the same machinery, and
a `[yoe]` project can now build Alpine, Debian, and Ubuntu images side by side.

## One backend, a family of distros

The interesting part isn't Ubuntu itself — it's what Ubuntu proves. The
[Debian work](https://yoebuild.org/blog/adding-debian/) built out the apt
plumbing: the `mmdebstrap` assembly pass, the `.deb` packaging path, the apt feed
resolver, the on-device package manager. None of that is Debian-specific. It's
apt-family machinery, and Ubuntu is the first test of whether it generalizes.

It does. The Ubuntu module is thin — what differs from Debian is the feed
identity, the suite (`[yoe]` pins Ubuntu's Resolute Raccoon / 26.04 LTS), and the
mirror. The packaging mechanism, the dependency model, the rootfs assembly are
all shared. The clearest sign of that is in the code itself: the old
`debian_feed` class generalized into an `apt_feed` class, with Debian and Ubuntu
as two configurations of it rather than two implementations. That's the bet
paying off — the second backend wasn't "Debian support," it was "apt support,"
and the marginal cost of the next distro in the family turns out to be small.

## The one place they diverge: zstd

Not quite zero, though. Ubuntu compresses its `.deb` payloads with zstd where
Debian leans on xz, and that surfaced a bug in the packaging path — the kind of
detail that stays hidden until a second distro in the same family exercises it.
Once fixed, the rest fell into line. A useful reminder that "almost the same" is
where the sharp edges live, and that a second consumer of shared code is the
cheapest way to find them.

## Three distros, one project

In the demo, switching from Debian to Ubuntu is a settings change — pick the
distro, pick the dev image, build. Underneath, all three bases now coexist in a
single project: a `yoe build-distro` against Alpine, Debian, and Ubuntu each
resolves and builds from cache, and the build tree keeps a separate directory and
package feed per distro. The Debian and Ubuntu feeds look nearly identical — which
is exactly the point. You choose the base image by image, and the build system
assembles whichever one the workload asks for.

## Mixing our own source into an Ubuntu base

One deliberate stress test in the video: rather than pull `bash`, `coreutils`,
`ca-certificates`, and `file` straight from Ubuntu's feeds, this build still
compiles them from `[yoe]`'s own source units — against Ubuntu's libraries, in
the same per-unit sandbox the rest of the system uses. Each unit builds under
`bwrap` against a sysroot hard-linked with only its declared dependencies, so it
sees Ubuntu's headers and shared libraries and nothing from the host. It's the
isolation model `[yoe]` borrows from Yocto, pointed at an Ubuntu base.

You wouldn't ship it this way — for a production image you'd pin those packages to
Ubuntu's own binaries and let the distro maintain them. The point of building them
from source here is to exercise the whole mechanism end to end: our source
packages compiling cleanly against an apt-family base, with the dependency
resolution and sandboxing doing their jobs.

## Where it stands

Honest status: the base image boots in QEMU on Ubuntu's own stock kernel, and the
foundation is solid enough to build and run a development image. It's `main` only
for now — a little over 6,000 packages — with universe, where most of Ubuntu's
catalog actually lives, still to be wired in.

It's also big. Building the same development image on each backend, against the
same `qemu-x86_64` target, the assembled rootfs comes out to:

| Backend | Dev-image rootfs |
| ------- | ---------------- |
| Alpine  | ~230 MB          |
| Debian  | ~390 MB          |
| Ubuntu  | ~1,130 MB        |

That Ubuntu figure looks alarming next to the others, but it's mostly low-hanging
fruit. Two directories account for the bulk of it: `linux-firmware` ships **677
MB** of vendor blobs for every device the distro might ever boot on, and the
stock kernel's module tree adds another **154 MB** — together about 70% of the
image. A real device needs the firmware and modules for its own silicon, not the
entire catalog, so trimming `linux-firmware` to the target's blobs and swapping
the distro kernel for a tailored build cuts the image roughly in half before
touching anything else. Locales, docs, and man pages are easy wins on top of
that. It's the same
[size story Debian tells](https://yoebuild.org/blog/adding-debian/) — most of the
weight is stock-distribution generality, and most of it comes off once you know
the target.

The encouraging result is the one the video opens with: supporting another
distribution in this family was not a lot of work. The next focus is moving past
QEMU onto real hardware, and trading the stock distro kernel for a custom one —
which is where embedded Linux gets interesting.

## Get involved

The full set of walkthroughs is on the
[Videos page](https://yoebuild.org/videos/). A few ways to go further:

- **Try a build** — the [Getting Started guide](https://docs.yoebuild.org/)
  covers install and your first image.
- **Star and watch the repo** — star it and click Watch to follow progress on
  [GitHub](https://github.com/yoebuild/yoe).
- **Subscribe to the newsletter** — occasional progress notes; the email signup
  is at the foot of every page on [yoebuild.org](https://yoebuild.org/).
- **Add a machine or image** — the
  [`/new-machine` and `/new-module` AI skills](https://docs.yoebuild.org/ai-skills.html)
  scaffold support for new boards and distros.
- **Open a discussion** — questions, ideas, or a board you'd like ported next go
  in [GitHub Discussions](https://github.com/orgs/yoebuild/discussions).
- **Send a note** — reach the team at
  [info@yoebuild.org](mailto:info@yoebuild.org?subject=%5Byoe%5D%20Ubuntu%20feedback).
