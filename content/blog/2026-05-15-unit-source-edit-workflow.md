+++
title = "Editing a Unit's Source Without Leaving the Build"
description = "How [yoe] flips a unit between a pinned release and a live development checkout — edit, build, deploy, then pin the result back into the recipe."
date = 2026-05-15
[taxonomies]
tags = ["videos", "productivity"]
+++

Editing the source of a unit is one of the most common things you do while
building an embedded Linux system. You hit a bug in an application, you need a
patch in the kernel, you want to try a change before it lands upstream. In most
build systems that means dropping out of the tool, cloning the repo somewhere
else, wiring up a patch or a local override, and rebuilding. The
[latest walkthrough](https://youtu.be/PgBKVJ3XZzU) shows `[yoe]` doing the whole
loop in place.

## Pinned by default, development on demand

Every unit pins to a release tag by default and checks out over HTTPS for
convenience. That is the right default for a reproducible build, but it is the
wrong shape for making a change: the source lives in `[yoe]`'s download cache,
and you can't push a fix back to a cache.

Pressing the dev-mode key switches the unit over. `[yoe]` re-points the checkout
at the upstream repository, optionally swaps the HTTPS remote for the SSH URL
most of us push through, and asks how much history you want. A shallow clone of
100 commits is plenty for a quick change — and for something like the Linux
kernel, skipping the full history saves a large download. Shell into the source
directory and you land on the upstream branch, connected to the remote you can
actually push to.

## The build follows the source

Once a unit is in development mode, the cache key comes from a `git diff` of the
working tree rather than the pinned tag. Change a line and the cache invalidates
on its own — no manual flag, no stale artifact. The unit's status moves from
pinned to `dev modified` to `dev dirty` as you switch modes and accumulate
uncommitted changes, so the state is always visible at a glance.

From there the loop is short: build the unit, deploy it with a single key to the
target you last deployed to, and watch the change land on the target instance.
Because `[yoe]` is built to run several sessions at once, the build and the
running target sit side by side while you iterate.

## Pinning the change back

When a change is worth keeping, commit it in the source tree — the status drops
out of `dev dirty` — and pin the recipe to the new commit. The pin command
writes the current `HEAD` back into the unit's tag field, preferring a real tag
over a raw hash when one exists at that commit. The unit is reproducible again,
now at your change, and the next build is back to a clean cached state.

## Why this matters

Two goals from [Hello, [yoe]](/blog/hello-yoe/) and
[What a Modern Embedded Linux Build System Could Look Like](/blog/next-gen-embedded-linux/)
were to shrink the idea-to-running-image loop and to keep the application
development experience tightly coupled to the system build. This workflow is
that idea applied to source: one tool, one screen, and a clean switch between a
pinned release and a live checkout for any unit — without the extra layers other
build systems put between you and the code.

What part of the development loop would you like to see demoed next?
[Open a discussion](https://github.com/orgs/yoebuild/discussions) or send a
[note](mailto:info@yoebuild.org?subject=%5Byoe%5D%20video%20feedback).
