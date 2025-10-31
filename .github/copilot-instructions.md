# Copilot Instructions for NT Rule Index

## Project Overview
This is a local-first repository that links Drive artifacts to **Number-Theory Rule Packs** and publishes a MkDocs site. The project indexes number theory rules and research artifacts, organizing them by topic tags.

## Project Structure
- `scripts/build_index.py` - Python script that generates the documentation index from CSV data
- `data/index.csv` - Source data containing rule entries with titles, URLs, tags, and metadata
- `RULE_PACKS.json` - Configuration defining rule pack categories and descriptions
- `docs/` - MkDocs documentation directory (auto-generated content goes here)
- `mkdocs.yml` - MkDocs configuration
- `.github/workflows/site-deploy.yml` - GitHub Actions workflow for building and deploying the site

## Build Process
1. Run `python scripts/build_index.py` to generate `docs/index.md` from the CSV data
2. Install MkDocs dependencies: `pip install -r requirements.txt`
3. Build the site: `mkdocs build` or serve locally: `mkdocs serve`

## Key Conventions
- The CSV file (`data/index.csv`) is the single source of truth for rule entries
- Tags in the CSV should match keys in `RULE_PACKS.json` for proper categorization
- Multiple tags can be separated by semicolons (`;`)
- The build script auto-generates markdown with proper formatting and links
- Generated files should not be manually edited

## Working with Data
- **Adding new rule packs**: Update `RULE_PACKS.json` with the new category key, title, and description
- **Adding new entries**: Add rows to `data/index.csv` with appropriate tags, titles, and Drive URLs
- **Tags**: Use existing tag keys from `RULE_PACKS.json` for consistency

## Code Style
- Python code follows standard conventions with 4-space indentation
- Use `utf-8` encoding for all file operations
- Keep functions focused and maintainable

## Testing
- Verify the build script runs successfully: `python scripts/build_index.py`
- Check that generated markdown is properly formatted
- Test the MkDocs site builds without errors: `mkdocs build --strict`

## Important Notes
- Some source files may have UTF-8 BOM markers; handle with `utf-8-sig` encoding when needed
- The site is deployed automatically via GitHub Actions on push to main/master
- The docs index is auto-generated; only edit the source CSV and JSON files
