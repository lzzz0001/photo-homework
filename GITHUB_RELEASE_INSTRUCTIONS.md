# GitHub Release Instructions

This document provides step-by-step instructions for creating GitHub releases for the Photo Watermark Application.

## Prerequisites

1. Ensure all changes are committed and pushed to the main branch
2. Update version numbers in relevant files if needed
3. Create and test the executable locally

## Creating a Release

### 1. Prepare Release Assets

Run the release creation script:
```bash
python create_release.py
```

This will create:
- A source code ZIP file in the release directory
- A source-only release package with documentation

### 2. Create the Executable (Optional)

If you want to include a Windows executable:
```bash
pyinstaller --onefile --windowed main.py
```

This creates `dist/PhotoWatermark.exe`.

### 3. Create GitHub Release

1. Go to the GitHub repository releases page:
   https://github.com/lzzz0001/photo-homework/releases

2. Click "Draft a new release"

3. Create a new tag:
   - Tag version: `v1.0.X` (increment the number)
   - Target: `main` branch

4. Set release title:
   - Format: "Photo Watermark Application v1.0.X"
   - Include a brief description of major changes

5. Upload release assets:
   - The source-only ZIP file created by `create_release.py`
   - The executable (if created) as a separate asset
   - Any other relevant files

6. Write release notes:
   - Summarize key features or fixes
   - Mention any breaking changes
   - Include installation instructions if needed

7. Publish release

## Best Practices

- Keep release packages under 100MB (GitHub limit)
- Use semantic versioning (v1.0.0 format)
- Include both source code and executables when possible
- Write clear, helpful release notes
- Test the release process in a private repository first if unsure

## Troubleshooting

### Large Files
If your release assets are too large:
- Compress files further
- Split into multiple smaller assets
- Consider using Git LFS for large binary files

### Authentication Issues
If you have trouble pushing releases:
- Check your GitHub credentials
- Use personal access tokens instead of passwords
- Verify you have write access to the repository

## Automated Release Process (Advanced)

For frequent releases, consider setting up GitHub Actions to automate the process:

1. Create `.github/workflows/release.yml`
2. Configure the workflow to build and upload releases automatically
3. Trigger on tag creation or other events

This ensures consistent, reproducible releases without manual steps.