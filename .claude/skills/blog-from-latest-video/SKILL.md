---
name: blog-from-latest-video
description: Use when asked to write, draft, or create a [yoe] blog post from the latest (or a specific) YouTube walkthrough video on the yoebuild channel — turns a video into a Zola blog post matching house style, with the standard CTA and all-absolute links for email.
---

# Blog Post from Latest Video

## Overview

Turn a `[yoe]` walkthrough video into a `content/blog/` post that matches the
existing house style: a short essay that uses the video as a hook, not a
transcription. The transcript anchors the facts; the post supplies the framing.

**Two hard rules:**
1. **The transcript is required.** If captions aren't ready yet, wait for them —
   never write the post from the title and description alone.
2. **Every link must be absolute.** These posts go out by email, where relative
   links break. `/videos/` → `https://yoebuild.org/videos/`.

## Workflow

1. **Fetch the video + transcript** with the helper script:
   ```bash
   .claude/skills/blog-from-latest-video/fetch-video.sh
   ```
   Newest video by default; pass a video ID for a specific one; `--list` shows
   the playlist newest-first. It prints `VIDEO_ID`, `TITLE`, the `youtu.be` URL,
   `UPLOAD_DATE`, the description, and the transcript.

2. **If the transcript is NOT_READY (exit code 2): wait, then retry.**
   YouTube usually generates captions within an hour or two of upload. Use
   `ScheduleWakeup` (~1200s) to check back, and re-run the script. Repeat until
   the transcript is available. Do **not** proceed without it. Tell the user you
   are waiting for captions to be generated.

3. **Check it isn't already covered.** Skim `content/blog/` for a post about the
   same video/topic. If one exists, confirm with the user before writing another.

4. **Read 1–2 recent posts** in `content/blog/` (e.g. the most recent `videos`-
   tagged ones) to absorb the current voice before drafting.

5. **Draft the post** following the structure and rules below. Apply the
   `refactoring-english` skill for the prose.

6. **Verify links are absolute** (see Quick Reference grep) and that the file
   builds: `zola check` (or `zola build`) if available.

## Post structure

Create `content/blog/YYYY-MM-DD-slug.md` (date = today; slug = short, kebab-case
topic, no `[yoe]`).

```
+++
title = "Title Case, may include [yoe]"
description = "One sentence — the hook/payoff, not a summary of sections."
date = YYYY-MM-DD
[taxonomies]
tags = ["videos", "<one more: progress | productivity | platform | ...>"]
+++

Opening paragraph: the claim, with a link to the video early —
[latest video](https://youtu.be/VIDEO_ID) or [walkthrough](https://youtu.be/VIDEO_ID).
Then the more interesting angle.

## 2–4 sections

Explain the substance — why it matters, how it works — in the author's voice.
Pull facts from the transcript; do not transcribe it. Render the project name as
inline code: `[yoe]`. Use em dashes and tight, technical prose.

## Why this matters  (or "What's next")

Tie back to the project's larger goals; link to a related earlier post.

<CTA — see below>
```

## The CTA (always end with this, links absolute)

End every post with all six calls to action. Keep the inviting, non-hype voice;
adapt the lead-in to the post, but keep the six actions. The standard block:

```markdown
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
```

## Quick reference

| Need | Value |
|------|-------|
| Site base URL | `https://yoebuild.org` |
| Blog dir | `content/blog/` |
| Filename | `YYYY-MM-DD-slug.md` |
| Required tags | `videos` + one topic tag |
| Video link form | `https://youtu.be/VIDEO_ID` |
| Videos page | `https://yoebuild.org/videos/` |
| Internal post | `https://yoebuild.org/blog/<slug>/` |
| Getting Started / try a build | `https://docs.yoebuild.org/` |
| GitHub repo (star and watch) | `https://github.com/yoebuild/yoe` |
| Add a machine/image (AI skills) | `https://docs.yoebuild.org/ai-skills.html` |
| Newsletter signup | foot of every page on `https://yoebuild.org/` |
| Discussions | `https://github.com/orgs/yoebuild/discussions` |
| Docs site | `https://docs.yoebuild.org/...` |
| Feedback note | `mailto:info@yoebuild.org?subject=%5Byoe%5D%20video%20feedback` |

**Absolute-link check before finishing** — this must return nothing:
```bash
grep -nE '\]\(/' content/blog/YYYY-MM-DD-slug.md
```
(catches any `](/videos/)`-style relative link).

## Common mistakes

- **Relative internal links.** `/videos/`, `/blog/x/` break in email. Prefix
  every one with `https://yoebuild.org`. Existing posts use relative links — do
  not copy that; this skill supersedes it.
- **Transcribing the video.** The post is an essay with a point of view, not a
  play-by-play. Three or four `##` sections, not a timeline.
- **Writing without the transcript.** If captions aren't ready, wait — the
  description is not enough to write an accurate post.
- **Wrong/missing tags.** Always include `videos`; add exactly one topic tag.
- **Marketing voice.** Keep the CLAUDE.md tone: respectful, hopeful, inviting,
  technical — not hype.
```
