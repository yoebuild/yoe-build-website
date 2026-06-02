+++
title = "Qt Support in [yoe]"
description = "Qt now builds and runs under [yoe]. The interesting part isn't Qt itself — it's that the toolkit comes from Alpine binaries wrapped as units, and the whole graphical loop runs in QEMU on your workstation."
date = 2026-05-29
[taxonomies]
tags = ["videos", "progress"]
+++

`[yoe]` can now build and run a Qt application, shown in a short
[demo video](https://youtu.be/AOq5aZc9Ohw). Qt is worth supporting because it's
the mainstay graphical toolkit for embedded native apps — if your device has a
display and you want a polished interface, Qt is very often the answer. But the
toolkit is just the occasion. The parts worth talking about are how those
dependencies get into a build, and where the graphical app actually runs while
you develop it.

## Wrapping binaries instead of building them

A Qt app pulls in a pile of dependencies: `qtdeclarative`, `qtbase`, X11, fonts.
In a traditional embedded build you'd own a recipe for each — fetch source,
patch it, compile it. That's where a lot of the cost and fragility of building
embedded Linux lives.

`[yoe]` takes a different path: it pulls these packages straight from the Alpine
community repo (and hopefully Debian will be an option soon) and presents the
prebuilt binaries as virtual units. You figure out which Alpine package you
need, and the build system pulls it into your feed and wraps its assets
automatically. No custom recipes, no source builds for the toolkit itself.

This is the same mechanism behind the
[Python tooling for the Beagle Play BSP](/blog/running-on-beagle-play/) and
[pip and npm on the target](/blog/pip-and-npm-on-the-target/) — a flat list of
`pkg`-style dependencies that resolve against a maintained binary distribution.
Adding a graphical toolkit ends up looking like adding any other dependency:
name the packages, rebuild. The leverage is in not reinventing a package set
that Alpine or Debian already maintains.

## QEMU as a first-class development target

QEMU is a really useful tool that I hadn't used much before. I would
develop apps natively, and then build an image for embedded targets, but QEMU
sits between these domains and allows you to quickly and efficiently develop
your image build system. `[yoe]` makes running on QEMU easy.

In this development cycle support was added for enabling the QEMU display,
setting the memory allocated, and configuring the network port mapping from the
QEMU instance to the host.

## What's next

More toolkit and application coverage, and more targets to run it on. The
[Videos page](/videos/) has the full walkthrough set. If there's an app or
framework you'd like to see running under `[yoe]`,
[open a discussion](https://github.com/orgs/yoebuild/discussions) or send a
[note](mailto:info@yoebuild.org?subject=%5Byoe%5D%20Qt%20feedback).
