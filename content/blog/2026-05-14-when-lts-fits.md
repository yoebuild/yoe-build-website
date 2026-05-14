+++
title = "When LTS fits — and when it doesn't"
description = "Long-Term Support makes sense for static embedded systems. Dynamic edge systems need a different model — and a different build tool."
date = 2026-05-14
[taxonomies]
tags = ["lifecycle", "platform"]
+++

LTS stands for Long-Term Support, which refers to software versions that receive
updates, bug fixes, and security patches for an extended period, typically aimed
at providing stability and reliability. For deeply embedded, single-purpose
systems, or locked-down enterprise laptops where users are not allowed
to install software, LTS makes sense.

For dynamic software systems (the browser is a good example), the only path is
forward. It's hard to predict exactly what pages
need loading tomorrow, where the user will go next, what problems will occur,
what security issues need patching, what new features need supporting, etc. Edge
systems are trending in that direction. They are capable, expandable platforms
whose future needs are hard to predict.

Trying to keep an operating system pinned to an LTS release while continuously
evolving everything on top is a bit like freezing a creature's skeleton while
expecting the rest of its body to grow and adapt around it. The structure may be
stable, but over time the muscles, organs, and connective tissue stop fitting
cleanly. Eventually, the mismatch creates friction, limits movement, and makes
further growth harder instead of easier.

When implementing an embedded OS, it's important to decide: is this 1) a
traditional static embedded system, or 2) a dynamic edge system? These are different
problems and require different tool-sets. `[yoe]` is being built for the
second case — see [What a Modern Embedded Linux Build System Could Look Like](/blog/next-gen-embedded-linux/)
for where that's headed.

![When LTS fits](/images/when-lts-fits.png)
