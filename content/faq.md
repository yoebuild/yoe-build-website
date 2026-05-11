+++
title = "FAQ"
description = "Answers to common questions about the [yoe] next-generation build system."
template = "page.html"
+++

A running list of questions we've heard while sharing the work. If you have one
that isn't here, [open a discussion](https://github.com/orgs/yoebuild/discussions)
or send us a [note](mailto:info@yoebuild.org?subject=%5Byoe%5D%20question) —
we'll add it.

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
3. **Technical bets that may not pan out.** Native-only builds via QEMU
   user-mode emulation, Starlark plus AI as a primary interface for new units,
   and `apk` as the package format are all bets that look right today but
   haven't been tested across a wide variety of products at scale. Any of them
   could need a rethink.
4. **Scope.** A TUI, a CLI, AI workflows, multiple architectures, containers,
   OTA — it is a lot to do well. Staying focused on the goals above, and saying
   no to nearby-but-different problems, will be a constant discipline.

We'd rather name these risks than ignore them. If any resonate — especially if
you'd help mitigate one — [come talk to us](https://github.com/orgs/yoebuild/discussions).
