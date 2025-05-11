# Image Processing Tools

This repository contains two Python scripts for working with image files:

1. `copy_horizontal_images.py` - Copies images with horizontal orientation from a source folder to a destination folder
2. `slideshow.py` - Displays images from a folder as a full-screen slideshow with various display options

Both scripts require Python and the Pillow library. To install Pillow:

```
pip install Pillow
```

## Copy Horizontal Images

The `copy_horizontal_images.py` script copies only images with horizontal orientation (width > height) from a source folder to a destination folder.

### Features

- Copies JPG, JPEG, and PNG images with horizontal orientation
- Creates the destination folder if it doesn't exist
- Provides progress messages during the copy process

### Usage

```powershell
python copy_horizontal_images.py <source_folder> <destination_folder>
```

### Example

```powershell
python copy_horizontal_images.py "D:\Photos\Vacation" "D:\Photos\Horizontal"
```

If you have special characters in your path (like `!`), use single quotes or the stop-parsing symbol in PowerShell:

```powershell
python copy_horizontal_images.py 'D:\Photos\N!\Vacation' 'D:\Photos\N!\Horizontal'
```

or

```powershell
python copy_horizontal_images.py --% "D:\Photos\N!\Vacation" "D:\Photos\N!\Horizontal"
```

## Slideshow

The `slideshow.py` script displays images from a folder in a full-screen slideshow with multiple view options.

### Features

- Full-screen slideshow with configurable interval (default: 5 seconds)
- Three display modes:
  - **Original**: Shows images at their original size, centered (filenames shown in top-left corner)
  - **Fit**: Scales images to fit entirely within the screen while maintaining aspect ratio
  - **Cover**: Scales images to cover the entire screen, cropping if necessary while maintaining aspect ratio
- Random playback option that will re-shuffle after all images have been shown
- Pause/resume functionality
- Manual navigation between images
- Supports various image formats (JPG, JPEG, PNG, GIF, BMP, TIFF)
- Option to filter by image orientation (horizontal or vertical only)

### Usage

```powershell
python slideshow.py <folder_path> [--interval <seconds>] [--original | --cover] [--random] [--horizontal | --vertical]
```

### Command-line Options

- `folder_path`: Path to the folder containing images (required)
- `--interval <seconds>`: Time interval between images in seconds (default: 5)
- `--original`: Start in "Original" mode (images at their actual size, centered).
- `--cover`: Start in "Cover" mode (scales images to fill the screen, may crop).
- `--random`: Display images in random order, re-shuffling after each full cycle
- `--horizontal`: Show only horizontally oriented images (width > height)
- `--vertical`: Show only vertically oriented images (height > width)

### Keyboard Controls

- **Space**: Pause/Resume slideshow
- **Right Arrow**: Next image
- **Left Arrow**: Previous image
- **Enter**: Cycle through display modes (Original → Fit → Cover → Original)
- **Escape**: Exit slideshow

### Examples

```powershell
# Basic slideshow with default settings (Fit mode)
python slideshow.py "D:\Photos\Vacation"

# 3-second interval, start in Original mode
python slideshow.py "D:\Photos\Vacation" --interval 3 --original

# Cover screen, random order
python slideshow.py "D:\Photos\Vacation" --cover --random

# Show only horizontal images
python slideshow.py "D:\Photos\Vacation" --horizontal

# Show only vertical images, start in default Fit mode, 2-second interval
python slideshow.py "D:\Photos\Vacation" --vertical --interval 2
```

If you have special characters in your path (like `!`), use single quotes in PowerShell:

```powershell
python slideshow.py 'D:\Photos\N!\Vacation' --random
```

## Requirements

- Python 3.x
- Pillow library
