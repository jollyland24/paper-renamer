# Academic PDF Renamer

Automatically rename academic papers from random filenames to meaningful titles based on their content.

## 🎯 Problem Solved

Do you have academic papers with filenames like:
- `paper_download_123.pdf`

This script automatically extracts the actual paper titles and renames them to:
- `Feminist HCI: Taking Stock and Outlining an Agenda for Design.pdf`


## ✨ Features

- **Smart title extraction** using multiple strategies (metadata, content analysis)
- **Handles complex titles** with colons, subtitles, and special formatting
- **Avoids duplicates** with intelligent conflict resolution
- **Skips already renamed files** to prevent re-processing
- **Cross-platform** compatible (Windows, Mac, Linux)
- **Detailed logging** shows exactly what was processed
- **Safe operation** - preserves original files if extraction fails

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- PyPDF2 library

### Installation

1. **Clone or download** this script
2. **Install dependencies**:
   ```bash
   pip install PyPDF2
   ```

### Usage

1. **Update the folder path** in the script:
   ```python
   FOLDER_PATH = "/path/to/your/pdf/folder"  # Change this line
   ```

2. **Run the script**:
   ```bash
   python rename_papers.py
   ```

3. **Check the results** - your PDFs will be renamed with meaningful titles!

## ⚙️ Configuration

You can customize the script behavior by modifying these variables at the top:

```python
FOLDER_PATH = "path/to/your/pdf/folder"  # Your PDF folder
MAX_FILENAME_LENGTH = 120                # Maximum filename length
MIN_TITLE_LENGTH = 15                    # Minimum title length to consider
```

## 🔧 How It Works

The script uses a multi-step approach to extract titles:

1. **PDF Metadata**: First checks if the PDF has title metadata
2. **Content Analysis**: Analyzes the first page text for title patterns
3. **Pattern Recognition**: Looks for:
   - Lines with colons (common in academic titles)
   - Longer text blocks (likely titles)
   - Position-based detection (titles usually appear early)
4. **Fallback Strategy**: Uses the first substantial text line if other methods fail

## 📁 File Structure

```
your-project/
├── rename_papers.py          # Main script
├── README.md                 # This file
└── your-pdf-folder/          # Folder with PDFs to rename
    ├── random_name_1.pdf
    ├── random_name_2.pdf
    └── ...
```

## 🛡️ Safety Features

- **Non-destructive**: Only renames files, doesn't modify PDF content
- **Conflict handling**: Automatically handles duplicate names with numbering
- **Skip protection**: Won't re-process files that already have good names
- **Error handling**: Continues processing even if individual files fail
- **Validation**: Checks folder existence before processing

## 📄 License

MIT License - feel free to use, modify, and distribute.


---

**Happy organizing!** 📚✨
