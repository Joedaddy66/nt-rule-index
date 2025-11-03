# Microsoft Store Packaging - Assets Directory

This directory should contain the visual assets for your Microsoft Store listing.

## Required Assets

### Store Listing
- **StoreLogo.png** (50x50 px)
  - Used in the Microsoft Store listing
  - Transparent background recommended

### App Tiles
- **Square150x150Logo.png** (150x150 px)
  - Medium tile on Start menu
  - Most commonly used icon

- **Square44x44Logo.png** (44x44 px)
  - Small tile and app list icon
  - Used in notifications

- **Wide310x150Logo.png** (310x150 px)
  - Wide tile on Start menu
  - Optional but recommended

## Design Guidelines

1. **Format**: PNG with transparency support
2. **Sizing**: Exact pixel dimensions required
3. **Scaling**: Provide @1x, @1.25x, @1.5x, @2x, @4x variants (optional)
4. **Colors**: Use consistent branding
5. **Background**: Transparent preferred, or match your brand color

## Creating Assets

### Using Design Tools
- Adobe Illustrator/Photoshop
- Figma
- Sketch
- Inkscape (free)

### Quick Generation
Use [App Icon Generator](https://www.microsoft.com/store/productId/9NBLGGH4S3B4) or online tools.

### AI Generation
- Use DALL-E, Midjourney, or Stable Diffusion
- Export at required sizes
- Ensure consistency across sizes

## Placeholder Assets

For initial testing, you can use placeholder assets:

```bash
# Create simple colored squares (requires ImageMagick)
convert -size 50x50 xc:blue StoreLogo.png
convert -size 150x150 xc:blue Square150x150Logo.png
convert -size 44x44 xc:blue Square44x44Logo.png
convert -size 310x150 xc:blue Wide310x150Logo.png
```

## Validation

Before submission:
1. Check exact pixel dimensions
2. Verify transparency rendering
3. Test on different Windows themes (light/dark)
4. Preview in Microsoft Store listing

## Resources

- [Microsoft Design Guidelines](https://docs.microsoft.com/windows/apps/design/style/app-icons-and-logos)
- [Windows App Icon Generator](https://www.microsoft.com/store/productId/9NBLGGH4S3B4)
- [Asset Generator Tools](https://appicon.co/)

---

**Note**: These assets are required for Microsoft Store submission. The build will proceed without them, but you must add them before final submission.
