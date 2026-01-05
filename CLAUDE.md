# Everfresh Pricelist - Claude Code Rules

## Project Overview
Single-page web app for managing wholesale produce price lists. Built with vanilla HTML/CSS/JavaScript (no framework). Deployed via GitHub Pages.

## Key Files
- `index.html` - Main application (all HTML, CSS, JS in one file)
- `index-test.html` - Copy of index.html for testing
- `logo.png` - Company logo (needs transparent version for export)
- `EXPORT_FEATURE_SPEC.md` - Detailed spec for export/sharing features

## Important Code Sections (in index.html)
| Section | Approximate Line | Purpose |
|---------|------------------|---------|
| CSS Styles | 21-1100 | All styling |
| HTML Structure | 1100-1700 | DOM elements, modals |
| priceData | ~1711 | Initial product data |
| renderCategories() | ~2000 | Main UI rendering |
| downloadImage() | ~4200 | Export to PNG |
| generateImageBlob() | ~5200 | Generate image for sharing |
| Share functions | ~4700-5200 | iMessage, WhatsApp, etc. |

## Code Conventions
- All code in single index.html file (no build process)
- localStorage keys prefixed with `everfresh_`
- Canvas exports at 3600px width (UHD quality)
- Sydney timezone for effective dates

## Rules for This Project

<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific file, you MUST read the file before answering. Make sure to investigate and read relevant files BEFORE answering questions about the codebase. Never make any claims about code before investigating unless you are certain of the correct answer - give grounded and hallucination-free answers.
</investigate_before_answering>

<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the tool calls, make all of the independent tool calls in parallel. Prioritize calling tools simultaneously whenever the actions can be done in parallel rather than sequentially. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into context at the same time. Maximize use of parallel tool calls where possible to increase speed and efficiency. However, if some tool calls depend on previous calls to inform dependent values like the parameters, do NOT call these tools in parallel and instead call them sequentially. Never use placeholders or guess missing parameters in tool calls.
</use_parallel_tool_calls>

<testing_changes>
After modifying index.html, always copy to index-test.html and push both files so the user can test on mobile via GitHub Pages.
</testing_changes>

<export_image_functions>
There are TWO canvas drawing functions that must stay in sync:
1. downloadImage() - for direct download
2. generateImageBlob() - for sharing features
When modifying canvas drawing code, update BOTH functions.
</export_image_functions>

<ios_limitations>
- Clipboard API for images does NOT work on iOS Safari
- Web Share API is the primary method for iOS sharing
- iOS Shortcuts can be triggered via URL scheme: shortcuts://run-shortcut?name=...
</ios_limitations>
