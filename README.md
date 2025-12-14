# Postman Collection Converter

A lightweight Python tool that converts Postman collection JSON files into organized folder structures with API endpoint documentation. Available in both GUI and command-line versions, supporting single file format export (TXT, JSON, or Markdown) to prevent duplication.

## Features

- Converts Postman collections to organized folder structures
- Exports to only one format at a time to prevent duplication
- Supports three output formats:
  - Plain Text (.txt)
  - Raw JSON (.json)
  - Markdown (.md)
- Preserves the hierarchical structure of Postman collections
- Available in both GUI and command-line versions
- Cross-platform compatibility (Windows, macOS, Linux)

## Installation

1. Ensure you have Python 3.6+ installed on your system
2. Download either `single_format_converter.py` (CLI) or `gui_postman_converter.py` (GUI)
3. Make sure your Postman collection is exported as a JSON file

## Usage

### Graphical User Interface

Run the GUI version for an easy-to-use interface:

```bash
python gui_postman_converter.py
```

1. Select your Postman collection JSON file
2. Choose an output directory
3. Select your preferred format (TXT, JSON, or MD)
4. Click "Convert Collection"

### Command Line Interface

```bash
python single_format_converter.py [collection_file] [output_dir] [format]
```

#### Arguments

- `collection_file` - Path to the Postman collection JSON file (default: d:/printify_postman_collection.json)
- `output_dir` - Output directory path (default: ./output)
- `format` - Output format: `txt`, `json`, or `md` (default: txt)

#### Examples

```bash
# Convert with default settings
python single_format_converter.py

# Convert a specific collection to default format (txt)
python single_format_converter.py my_collection.json

# Convert to a specific output directory with Markdown format
python single_format_converter.py my_collection.json ./api_docs md

# Convert with all parameters specified
python single_format_converter.py d:/collections/api.json ./documentation json
```

## Output Structure

The tool creates a folder structure that mirrors your Postman collection:

```
output_directory/
└── Collection Name/
    ├── Folder 1/
    │   ├── Subfolder/
    │   │   ├── Endpoint 1.md
    │   │   └── Endpoint 2.md
    │   ├── Endpoint 3.md
    │   └── Endpoint 4.md
    └── Folder 2/
        ├── Endpoint 5.md
        └── Endpoint 6.md
```

## Format Examples

### Markdown Output (.md)
```markdown
# Get Users

**Method:** `GET`  
**URL:** `https://api.example.com/users`

## Description
Retrieve a list of all users

## Headers
| Key | Value |
|-----|-------|
| Authorization | Bearer token |
| Content-Type | application/json |
```

### Plain Text Output (.txt)
```
API Endpoint: Get Users
==================================================
Method: GET
URL: https://api.example.com/users

Description:
Retrieve a list of all users

Headers:
  Authorization: Bearer token
  Content-Type: application/json
```

### JSON Output (.json)
Exports the raw Postman request object in formatted JSON.

## Requirements

- Python 3.6 or higher
- No external dependencies

## License

MIT License - see LICENSE file for details