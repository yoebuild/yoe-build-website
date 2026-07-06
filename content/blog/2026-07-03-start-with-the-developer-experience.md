+++
title = "Start with the Developer Experience"
description = "The [yoe] build project prioritizes one thing above all else — the day-to-day embedded Linux developer experience. Every other concern is secondary."
date = 2026-07-03
[taxonomies]
tags = ["strategy", "productivity", "philosophy"]
+++

For the [`[yoe]` build](https://yoebuild.org/) project, I am prioritizing one
thing above all else: the day-to-day embedded Linux developer experience. That
includes every developer on the project (system, kernel, application, etc.),
which on many projects is one person.

## Perspective

When building systems, we can start from many perspectives: security,
reproducibility, reliability, LTS (long-term support), control, immutability,
scalability, BSP compatibility, and more. As technologists, we all have
technology preferences and priorities that shape our work, and it is natural to
start there. Steve Jobs started somewhere else: the customer experience. After
receiving a scathing insult, he
[made the following comment](https://youtu.be/oeqPrUmVz-o):

> You’ve got to start with the customer experience and work backwards to the
> technology. You can’t start with the technology and try to figure out where
> you’re going to try to sell it.

## Fast, transparent, efficient, and approachable

I've received [many](https://news.ycombinator.com/item?id=48588247) good
[critiques](https://lobste.rs/s/4hcq97/is_it_time_for_new_embedded_linux_build)
about the project to date. This feedback is useful and shapes the implementation
going forward. But I need to state the project's goals more clearly, so it's
obvious why `[yoe]` exists rather than reaching for an existing alternative. The
first priority: the system must be **fast, transparent, efficient, and
approachable** for small teams. A great small-team developer experience lets us
solve the real problem, building the product, without fuss or meta-work (work
around the work) that doesn't move us toward the goal.

`[yoe]` must start fast and do its job quickly with almost no overhead. The UI
(both command-line and TUI) must be intuitive, discoverable, and pleasant to
use. The build system's metadata should be obvious and easy to read. Problems
should be easy to debug. Information about a component should stay in one place,
not scattered across the system where it's hard to piece together. The same
process application developers use should translate directly into building the
product software, with no extra work. SDK snapshots must disappear; rather the
build system should dynamically construct the needed build environment for any
component. We must reuse the work others have done (building, packaging,
security updates, etc.). Nothing should be built more than once, unless
something has changed. It should be painless to move around the system, make,
build, deploy, and capture changes. This tool must help small teams move fast
and get things done. All other concerns, such as 100% build from source, binary
reproducibility, etc., are secondary.

## The importance of iteration speed

One of the most important ingredients for innovation is iteration. The faster
you iterate, the more you can innovate. This is critical for startups, where the
entire point is innovation. Yocto does many things well, but fast iteration is
not one of them, especially when things change or problems occur. `[yoe]` build
trades some of this control and flexibility for speed.

## Do the simplest thing well

There are many advanced things you can do with Linux: containers, advanced
file-system techniques such as overlays, immutability, OSTree, Nix
builds/stores, etc. However, the immediate goal of the `[yoe]` build project is
to deliver the best possible developer experience for building and deploying a
simple **read/write Embedded Linux system root file system** including the
bootloader, kernel, and applications. We are starting at ground zero with the
simplest case that is more than adequate for many projects. Immutability,
containers, extensions, and other things will follow, but the foundational piece
must be right - an efficient way to create a custom root file system for an
embedded device.

## Technology tradeoffs

[Go and Starlark](https://docs.yoebuild.org/language-choices.html) are pragmatic
choices that reflect the project's values. While they will never be as safe and
reproducible as technologies like Rust and Nix, they are easier to read and
understand. We may switch to something else later _if_ we can maintain the
developer experience. But the bet is that we can borrow good ideas (caching,
hashing, etc.) from other systems to reach an acceptable level. Most technology
decisions are a compromise. Reaching near 100% in one area often requires
significant compromises in another. For example, the Nix language is powerful
and excellent at completely specifying a system. It is straightforward to use
existing packages and configs, but writing new Nix expressions or debugging
problems is hard. There is a steep learning curve. This is the trade-off - if
you want the Nix level guarantees and flexibility when specifying a system, then
you also need to accept its costs and complexities. The same can be said for
Rust. If you need Rust level guarantees with memory safety, then you need to
deal with the complexities of the borrow checker and slow compile time. It is
fine to insist on 100% security, reproducibility, compile from source, etc.
**_if_** these are real needs and you have the resources to do it (time,
dedicated people, and skills). Small teams often don't have any of these three
luxuries.

Maybe none of this matters, because AI can figure out and handle complex
systems. AI is effective. I've debugged some genuinely hard problems in Yocto
with Claude Code. However, it's still slow. Requiring AI to do everything makes
for a slow, miserable development experience. Making things simpler for humans
also makes it easier for AI. Efficiency, iteration speed, and context size
matter, even in the world of AI. Although AI can work on large tasks
autonomously, the speed from human idea to working result is still the
bottleneck for innovation. If we have to wait minutes/hours/days for AI and the
build system to do its work for every iteration, that is too slow.

`[yoe]` build is similar to Go in that it aims to be pretty good at most things,
but likely not the best at any particular technical requirement. Go is not the
fastest, safest, most expressive, ... language. But it is pretty good at
everything and the developer experience is amazing. Likewise, `[yoe]` will not
be the most secure, controlled, extensible, ... build system, but it will be
good enough in all of these areas, and the developer experience will be amazing.
There is a risk that without focusing on a technical requirement, such as
security, up front, we won't be able to get to where we need to be. However,
there is an even greater risk that if we focus exclusively on a single technical
requirement, the developer experience will suffer.

## Other systems exist for other reasons

Other systems accommodate other priorities:

- If BSP compatibility and building from source is your top priority, then _use
  Yocto_ - it does this very well.
- If package count or absolute reproducibility is your top priority, then _use
  Nix_ - it is amazing.
- If containers are your focus, then _check out Torizon_.
- If you want to leverage the mobile ecosystem, then _use Android_.
- If you want a clean way to manage application layers, _check out Avocado OS_.
- If you want enterprise backing and guarantees, then use _Ubuntu Core_.

But don't say "just use X." If X had the developer experience I wanted, I would
already be using it. However, we can always learn from other systems, and
`[yoe]` build is mostly just a combination of
[good ideas from existing systems](https://docs.yoebuild.org/comparisons.html)
in a different balance.

Here is one example of navigating this tension: support for upstream
distribution packages. Tool startup time matters, so the tool had to be written
in a fast compiled language. I also wanted to use the vast package ecosystem
from distributions like Alpine and Debian. Instantiating a unit for every
package in these ecosystems was too expensive and slow, and it bloated the
dependency graph. We could have stopped and said - well, if we want lots of
packages, startup time will be slow. Instead, we compromised on only creating
virtual units for the packages we actually use (a dependency of any image), but
the full package repository is still available for inclusion in an image. As a
bonus, the UI is not cluttered with packages we are not using. There are
solutions to most problems if we are creative in finding them. But we must
preserve the overriding values and goals through this process; otherwise we soon
get locked into a situation where attaining them is impossible.

## Summary

In summary, `[yoe]` build is a pragmatic tool for fast iterations and an
excellent day-to-day developer experience. Everything else is secondary. It will
likely never be the best at any single technical requirement, but it balances
them well enough to help small teams iterate quickly and build innovative edge
products they can maintain. `[yoe]` lets developers focus on the problem they
are solving, not the details of the build system. Like the Go language, the
tooling and build system is nearly invisible,
[even boring](https://www.nazarboyko.com/articles/go-is-boring-in-the-best-possible-way).

In your day-to-day development of edge/embedded systems, what is important to
you? What would you like to see different?
