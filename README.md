# Belialhun/SR2hun – Technical and Documentation Overview

This project supports the Hungarian localization of **Legacy of Kain: Soul Reaver 2**, focusing on converting and editing the game’s textual and graphical assets. The repository includes 3 key Python scripts and a web-based HTML tool to aid this technical localization process.

---

## ✨ GeneratedPNG.py

**Purpose**:  
This script converts `.tpng` text files (containing dialog or narration with formatting tags) into 512x448 PNG images, which are used as subtitle textures in the game.

**Features:**
- Parses `.tpng` lines containing tags like `[title]`, `[dialogue]`, `[narrator]`, `[centered]`, `[pn]`, `[NLA]`, `[NRA]`
- Automatically applies font, alignment, and color formatting
- Output: PNG image (512x448) including:
  - The formatted Hungarian text
  - Navigation arrows ("Előző / Következő")
  - Page number from `[pn]` tag
- Embeds original text as metadata in the PNG ("Description" field) for verification
- Uses Pillow and Arial fonts for rendering

---

## 📁 pngtoraw.py

**Purpose**:  
Converts PNG images into `.raw` files in the ARGB1555 format (16-bit color), as required by the game.

**Features:**
- Tkinter-based GUI
- Supports:
  - Single PNG conversion
  - Batch folder conversion
  - Required input: a PNG image and a `.raw` header file (128 bytes)
- Output file has a fixed size (458,880 bytes = 512x448)
- Useful for inserting modified text textures back into the game

---

## 👁️ rawtopng.py

**Purpose**:  
Converts `.raw` image files from the game back into editable PNGs.

**Features:**
- Simple GUI with Tkinter
- Assumes `.raw` file structure:
  - 128-byte header
  - ARGB1555 pixel data
  - Fixed resolution: 512x448 (229,376 pixels)
- Saves PNG outputs to an output directory
- Logs errors into `conversion_errors.log` if file size is invalid

---

## 🗃️ DOCTYPE5.html

**Purpose**:  
A browser-based interactive HTML5 tool for visually generating `.tpng` files compatible with `GeneratedPNG.py`.

**Features:**
- Create 10–20 text boxes dynamically
- Assign formatting to each: `[dialogue]`, `[narrator]`, `[centered]`, `[title]`, etc.
- Add page number `[pn]`
- Two optional checkboxes:
  - Hide "previous" arrow → `[NLA]`
  - Hide "next" arrow → `[NRA]`
- Button: **Generate Text** – displays output
- Button: **Save File** – downloads `.tpng` file

**Usage:**
1. Open `DOCTYPE5.html` in a browser
2. Choose number of boxes, fill in text and style
3. Set page number, toggle arrows as needed
4. Click **Generate Text**, preview output
5. Click **Save File**, browser downloads `.tpng`

---

## 🔧 Localization Workflow

1. **Extract original textures** with `rawtopng.py`  
2. **Edit and generate subtitles** using `DOCTYPE5.html` and `GeneratedPNG.py`  
3. **Convert back to .raw format** using `pngtoraw.py`  

---

## 🔗 Dependencies
- Python 3.x
- Pillow (PIL)
- Tkinter (standard in Python)

---
