+++
title = "AI in the Build Loop [yoe]"
description = "[yoe] installs Claude Code skills into your project. When a unit fails to build, press `d` and the agent reads the build log and fixes it."
date = 2026-06-11
[taxonomies]
tags = ["videos", "productivity"]
+++

A build system is a lot of small pieces — feeds, units, dependencies, task
steps, sandboxes. None of it is hard on its own. The hard part is holding all of
it in your head at once, which is exactly what humans are bad at and agents are
good at. The [latest video](https://youtu.be/nfG_UTerYeo) shows how `[yoe]` uses
that: it ships Claude Code skills you install into your project, and wires a
diagnose step into the build loop.

## Two ways to install the skills

The [AI skills page](https://docs.yoebuild.org/ai-skills.html) covers both
paths.

Run `yoe skills install` inside your project and it drops the skills into your
`.claude/` folder. `yoe init` now does this by default. Keeping them local lets
you list, update, and diff them against your own edits. Note that `update`
overwrites, so rename a skill first if you've customized it.

The other path is the Claude Code plugin marketplace: add the `[yoe]`
marketplace, reload, and skills like `diagnose` and `new-unit` show up as
plugins.

Several skills ship in the set. Many are still ideas, but `diagnose` and
`new-unit` are in daily use, and the rest will fill in over time.

## Press `d` to diagnose

The demo: add a bad `echo make error` task step to the `ca-certificates` unit.
`[yoe]` sees the unit is no longer cached, rebuilds it, and the build fails on
the first step. You could shell out and hunt for the problem yourself. Instead,
press **`d`**.

That runs the `diagnose` skill and hands it the build log, so the agent starts
from the evidence instead of searching for it. It reads the log, finds the bad
line, removes it from the unit, and the rebuild succeeds — all without leaving
the `[yoe]` terminal UI.

You can also run it from a Claude session: say "diagnose the unit that fails to
build" and get the same result. The TUI path keeps you in the build loop; the
Claude path keeps your agent and build side by side. Either way, the agent gets
the log instead of guessing.

## What's next

This is a trivial example on purpose — a one-line error, a one-line fix. The
point is the wiring, not the bug. The same pattern reaches harder problems as
the skills mature: porting BSPs from Yocto, expanding `new-unit`, and pulling
units across from Alpine, Debian, and other systems.

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
  [info@yoebuild.org](mailto:info@yoebuild.org?subject=%5Byoe%5D%20video%20feedback).
