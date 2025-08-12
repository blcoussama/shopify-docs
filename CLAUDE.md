# Shopify Documentation Formatting Project

## Project Overview

This project converts Shopify official documentation pages to well-formatted markdown files optimized for Claude Code usage. The goal is to create a comprehensive, searchable documentation library for AI-assisted Shopify development.

## Content Processing Approach

**ALWAYS use manual copy-paste method** - this captures dynamic content that automated scraping misses, including:

- JavaScript-rendered tabbed interfaces  
- Multi-file code blocks with separate tabs
- Dynamic content that only appears on user interaction
- Complex nested structures
- Hidden tutorial steps and prerequisites
- Interactive examples and live demos

## Code Block Formatting Rules

### Filenames and Paths

- **ALWAYS** include filenames using `**📁 filename**` format
- Include file paths when available: `**📁 QRCode.server.js**` followed by `` `/app/models/QRCode.server.js` ``
- This information is critical for developers to know which files to create/edit
- **NEVER miss filenames** - they are essential for practical implementation

### Terminal Commands

- **ALWAYS** label all terminal/command blocks as `**Terminal**`
- Use `bash` language tag for shell commands
- This applies to ALL bash commands: npm, shopify, cd, git, etc.
- Example:

  ```
  **Terminal**
  ```bash
  shopify app dev
  ```

  ```

### Configuration Files

- Use descriptive labels from source content:
  - `**Cursor configuration**`
  - `**Alternative configuration for Windows**`  
  - `**Claude Desktop configuration**`
  - `**Disable instrumentation**`
  - `**Enable Polaris support**`

### Code Language Tags

- `javascript` for JS/JSX files
- `json` for JSON config files
- `toml` for TOML config files
- `prisma` for Prisma schema files
- `bash` for terminal commands

### Directory Structures

- **ALWAYS** use ASCII tree characters for directory structures
- Use standard ASCII tree format: `├──`, `│`, `└──` characters
- Example:

  ```
  <App name>/
  ├── shopify.app.toml
  ├── package.json
  ├── extensions/
  │   ├── my-extension/
  │   │   ├── shopify.extension.toml
  │   │   └── ...
  │   └── ...
  └── .env
  ```

## Content Structure Standards

### Multi-File Code Sections

- Capture ALL files mentioned in tutorials
- Include complete code for each file
- Preserve file relationships and imports
- Example: QR code tutorial has 6 files (schema.prisma, QRCode.server.js, app.qrcodes.$id.jsx, app._index.jsx, qrcodes.$id.jsx, qrcodes.$id.scan.jsx)
- **Dynamic Multi-File Containers**: For tabbed code interfaces that show multiple files, user will provide main content first, then individual file contents with paths separately

### Documentation Organization

- Follow existing Shopify folder structure
- Create comprehensive sections with proper headings
- Include all technical details and explanations
- Preserve original section ordering and hierarchy

### Tables and Lists

- Format tables with proper markdown syntax
- Use clear headers and consistent column alignment
- Convert complex lists to proper markdown lists
- Maintain technical accuracy of all data

## Quality Checklist

Before considering any file complete, verify:

- [ ] All code blocks have proper filenames and language tags
- [ ] **ALL** terminal commands are labeled as **Terminal**
- [ ] Configuration blocks have descriptive names from source
- [ ] All multi-file examples are captured completely
- [ ] File paths are included where available
- [ ] Tables are properly formatted
- [ ] Directory structures use ASCII tree format
- [ ] Section hierarchy is maintained
- [ ] No dynamic content was missed
- [ ] No missing prerequisites or setup steps

## File Naming Conventions

- Use kebab-case for filenames (build-an-app.md)
- Follow Shopify's URL structure for consistency
- Place files in corresponding folder structure
- Create nested directories as needed (shopify-cli-for-apps/)

## CRITICAL RULES - NEVER VIOLATE

### Content Integrity Rules

- **NEVER ADD CONTENT** - Only format what's provided, never add code, examples, or content from your knowledge
- **NEVER MODIFY CONTENT** - Don't change, improve, or enhance the original content in any way
- **COMPLETE CAPTURE ONLY** - Include every single element from the original exactly as provided

### Systematic Verification Process

Before responding, ALWAYS verify:

1. ✅ All terminal commands labeled as **Terminal**
2. ✅ All filenames labeled as **📁 filename**  
3. ✅ Directory structures use ASCII characters (├── │ └──)
4. ✅ All file paths included where mentioned
5. ✅ Multi-file code sections fully captured
6. ✅ No content added from your knowledge

### Content Verification Reporting

ALWAYS report back:

- What content was received
- What might be missing
- Any files referenced but not provided
- Confirmation of complete capture

## Working Session Guidelines

- Process one file at a time completely
- Ask for content to be pasted directly
- Format immediately with all requirements
- Confirm critical elements like filenames and terminal labels are captured
- Continue with established workflow without re-explaining rules
- Use TodoWrite tool to track progress on complex multi-step tasks

## Speed Commands for User

To speed up the formatting process, user can use these commands after I complete a file:

**"fix format"** - I will immediately run the standard fixes:

- Add missing **Terminal** labels to bash code blocks
- Add missing **📁 filename** labels with file paths
- Fix any other systematic formatting issues

**"check file"** - I will verify the file meets all formatting standards

## Post-Processing Fix Commands

After completing all documentation files, run these Linux commands to fix any Unicode/file icon corruption:

**All-in-One Fix Command:**

```bash
find . -name "*.md" -type f -exec sed -i \
-e 's/\x14\x00\x00/└──/g' \
-e 's/\x1c\x00\x00/├──/g' \
-e 's/\x02/│/g' \
-e 's/ \x00\x00//g' \
-e 's/\x00\x00//g' \
-e 's/=\xEF\xBF\xBD/📁/g' {} \;
```

**Individual Fix Commands:**

```bash
# Fix DC4NULNUL (end branches)
find . -name "*.md" -type f -exec sed -i 's/\x14\x00\x00/└──/g' {} \;

# Fix FS NULNUL (branch connectors)  
find . -name "*.md" -type f -exec sed -i 's/\x1c\x00\x00/├──/g' {} \;

# Fix STX (vertical lines)
find . -name "*.md" -type f -exec sed -i 's/\x02/│/g' {} \;

# Remove NULNUL with leading space
find . -name "*.md" -type f -exec sed -i 's/ \x00\x00//g' {} \;

# Remove remaining NULNUL
find . -name "*.md" -type f -exec sed -i 's/\x00\x00//g' {} \;

# Fix corrupted file icons
find . -name "*.md" -type f -exec sed -i 's/=\xEF\xBF\xBD/📁/g' {} \;
```

## Success Metrics

- Complete capture of all technical content
- Proper formatting for Claude Code optimization
- All code examples are executable/usable
- Clear file structure for developers
- Consistent formatting across all files
- Clean ASCII directory structures without Unicode corruption
