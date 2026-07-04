# Marketing Images

This directory contains SVG marketing images for social media and promotional use.

## Images

### social-banner.svg
- **Size**: 1500x500 pixels
- **Use**: Social media headers, website banners
- **Content**: Project title, key features, performance stats

### feature-card.svg
- **Size**: 600x400 pixels
- **Use**: Feature highlights, social media posts
- **Content**: 5-Tier Priority System feature showcase

### install-card.svg
- **Size**: 600x400 pixels
- **Use**: Installation guides, quick start posts
- **Content**: Installation steps and compatibility info

### github-promo.svg
- **Size**: 600x400 pixels
- **Use**: GitHub promotion, repository announcements
- **Content**: GitHub repository information and call-to-action

## Usage

These SVG images can be:
- Used directly in websites (HTML `<img>` tags)
- Converted to PNG/JPG for platforms that don't support SVG
- Scaled to any size without quality loss
- Customized by editing the SVG source code

## Theme

All images use a consistent sci-fi theme with:
- Dark backgrounds (#0a0a0f, #050508)
- Neon accent colors (cyan #00f0ff, purple #7b2cbf, pink #ff006e)
- Grid patterns and glow effects
- Professional typography

## Conversion

To convert SVG to PNG using ImageMagick:
```bash
convert social-banner.svg social-banner.png
convert feature-card.svg feature-card.png
convert install-card.svg install-card.png
convert github-promo.svg github-promo.png
```

To convert using Inkscape:
```bash
inkscape --export-type=png social-banner.svg
inkscape --export-type=png feature-card.svg
inkscape --export-type=png install-card.svg
inkscape --export-type=png github-promo.svg
```
