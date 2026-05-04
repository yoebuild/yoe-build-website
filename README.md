# yoe-build-web-site

Static website for [`[yoe]`](https://github.com/yoebuild/yoe), built with
[Zola](https://www.getzola.org/).

## Local development

```sh
zola serve              # http://127.0.0.1:1111, live reload
zola build              # output to public/
zola check              # validate links and templates
```

## Layout

- `config.toml` — site config
- `content/_index.md` — landing page (renders via `templates/index.html`)
- `content/blog/` — blog posts
- `templates/` — Tera templates (`base.html`, `index.html`, `page.html`, `section.html`)
- `sass/main.scss` — single SCSS bundle, compiled to `main.css`
- `static/images/` — logos and screenshots

## Theme

Custom dark theme based on the `[yoe]` amber-on-black logo. No external theme
dependency. Colors live as SCSS variables at the top of `sass/main.scss`.

## Deploying

Any static host: GitHub Pages, Netlify, Cloudflare Pages, S3 + CloudFront. The
site outputs to `public/` and has no runtime dependencies.
