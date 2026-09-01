+++
title = "When Debian fits better than Yocto"
description = "A well-written article about why Debian may be a viable alternative to Yocto for some systems."
date = 2026-09-01
[taxonomies]
tags = ["yocto", "debian"]
+++

The following article is a well-written description of the tradeoffs between
Yocto and Debian for embedded systems by Richard Weinberger.

[You probably don’t need Yocto, and that’s fine](https://sigma-star.at/blog/2026/05/you-probably-dont-need-yocto-and-thats-fine/)

From the conclusion in the above post:

> - “Your own distribution” really means your own maintenance. The CRA and
>   similar regulations make that bill come due.
> - A heavily modified Yocto build doesn’t inherit upstream fixes for free.
>   Every maintenance release becomes review and rework.
> - An established distribution like Debian, assembled into an image with mkosi,
>   ELBE, or debos, covers the common case with a fraction of the per-project
>   effort.
> - When you need surgical control over the system, Yocto wins. When you don’t,
>   picking it is a long, expensive way of solving a problem you don’t have.

These are good points and exactly why [\[yoe\] build](https://yoebuild.org/)
exists.

The BSP is still a big question as these are getting quite complex. I'm
currently betting that LLMs can help us
[port BSPs](https://yoebuild.org/blog/running-on-beagle-play/) with a reasonable
effort, but that is an ongoing experiment.
