+++
title = "Running [yoe] on a Beagle Play"
description = "The build system now boots a TI AM625 board through a four-stage bootloader — and Claude wrote most of the BSP from a single prompt."
date = 2026-05-21
[taxonomies]
tags = ["videos", "progress"]
+++

`[yoe]` now boots a Beagle Play. The
[latest video](https://youtu.be/pL3ze_LuJPc) walks through building the image,
flashing the SD card, and watching the TI AM625 step through its four-stage
boot. But the more interesting story is how the BSP got written: I pointed
Claude Code at the existing `meta-ti` Yocto layer, asked it to "create machine
support for a Beagle Play," and most of it landed in one shot.

## What's in the video

`yoe update` and `yoe sync` to refresh the modules, then `yoe` to open the TUI.
Pick `beagleplay` from the machine list, pick the development image, press `F`
to flash. `[yoe]` figures out which block devices are removable so you can't
accidentally write to your workstation's main disk, remembers the device you
used last time, and writes the SD card.

Hold the user button down while powering on the board and it boots from SD
instead of the on-board eMMC — useful so an old eMMC bootloader can't sneak into
the chain. The serial console then shows the boot stepping through its stages.

## Four stages of bootloader

The AM625 is not a simple part. The on-chip ROM brings up a 32-bit R5 core and
loads a first-stage SPL onto it. That hands control to the 64-bit A53 cores,
which load a second SPL, then U-Boot, then the kernel. So `[yoe]` needs two
U-Boot binaries (one 32-bit, one 64-bit), an extra 32-bit ARM toolchain
alongside the default 64-bit one, and a pile of Python build-time tools that the
TI build scripts call out to.

Those Python tools come straight from Alpine packages — no custom recipes, no
source builds. Hitting `e` on a unit pops you into your editor, and the
dependency list reads as a flat enumeration of `py3-*` packages.

The build itself runs in a `bwrap` sandbox against a per-unit sysroot.
Dependencies are hard-linked in, so it's fast, and the unit only sees what it
declared — nothing leaks from a sibling. That sandbox is what turns "add another
`py3-*` and rebuild" into a safe operation instead of a debugging adventure.

## The part that mattered

`[yoe]` rests on a bet: that an AI agent can take a Yocto BSP from a vendor's
layer and reshape it into a `[yoe]` module quickly. If that bet doesn't hold,
the project doesn't work — every new SoC becomes a multi-week porting job, and
the productivity case collapses.

The Beagle Play is the first real test. It's not a Raspberry Pi clone with a
mainline kernel and a one-line config. It's a current-generation TI part with
vendor-specific firmware, a 32-bit SPL stage, and a custom toolchain
requirement. Claude wrote most of it from a single prompt. The remaining work
was iterating on missing Python dependencies — a build would fail, the error
named a missing tool, the fix was another Alpine package. A handful of cycles
later, the image booted.

That's the kind of porting loop the project needs to be cheap, and right now it
looks like it is.

## What's next

More BSPs. The
[Beagle Play machine docs](https://docs.yoebuild.org/machine-beagleplay.html)
cover how to use this one, and the [Videos page](/videos/) has the full
walkthrough set. If there's a board you'd like to see ported next,
[open a discussion](https://github.com/orgs/yoebuild/discussions) or send a
[note](mailto:info@yoebuild.org?subject=%5Byoe%5D%20BSP%20feedback).
