## Tool Specifications for Re-implementation

Here's a breakdown of the functionalities for `copy_horizontal_images` and `slideshow_tool`:

### 1. `copy_horizontal_images`

*   **Purpose**: This command-line tool copies image files that have a horizontal orientation (width greater than height) from a specified source folder to a destination folder.
*   **Core Functionality**:
    *   Accepts two command-line arguments:
        1.  `source_folder_path`: The path to the directory containing the original images.
        2.  `destination_folder_path`: The path to the directory where horizontal images should be copied.
    *   The tool should iterate through all files in the `source_folder_path`.
    *   For each file, it needs to determine if it's an image and its orientation.
        *   Supported image formats: JPG, JPEG, PNG.
        *   To determine orientation, the tool must read the image's metadata or pixel data to get its width and height. An image is considered horizontal if its width is strictly greater than its height.
    *   If an image is horizontal, it should be copied to the `destination_folder_path`.
    *   If the `destination_folder_path` does not exist, the tool should create it.
    *   The tool should provide feedback to the user, such as which files are being copied or if no horizontal images are found.
    *   Error handling:
        *   Report if the source folder doesn't exist or is not accessible.
        *   Handle potential errors during image file reading or copying.
        *   Report issues with creating the destination folder.

### 2. `slideshow_tool`

*   **Purpose**: This command-line tool displays images from a specified folder in a full-screen slideshow, offering various viewing options and controls.
*   **Core Functionality**:
    *   **Windowing**:
        *   Creates a full-screen, borderless window with a black background.
    *   **Image Loading & Display**:
        *   Accepts one mandatory command-line argument: `folder_path` (path to the image directory).
        *   Supported image formats: JPG, JPEG, PNG, GIF, BMP, TIFF.
        *   Images are displayed one at a time.
    *   **Command-line Arguments (Optional)**:
        *   `--interval <seconds>`: A floating-point number specifying the duration (in seconds) each image is displayed before automatically advancing to the next. Default: `5.0` seconds.
        *   `--original`: If present, starts the slideshow in "Original" display mode.
        *   `--cover`: If present, starts the slideshow in "Cover" display mode.
        *   If neither `--original` nor `--cover` is specified, the slideshow defaults to "Fit" display mode. These two arguments are mutually exclusive.
        *   `--random`: If present, images are displayed in a random order. After all images in the shuffled list have been shown once, the list is re-shuffled and playback continues.
        *   `--horizontal`: If present, only images with a horizontal orientation (width > height) are included in the slideshow.
        *   `--vertical`: If present, only images with a vertical orientation (height > width) are included in the slideshow. `--horizontal` and `--vertical` are mutually exclusive.
    *   **Display Modes** (Cycle through with `Enter` key: Original → Fit → Cover → Original):
        1.  **Original**:
            *   Image is displayed at its actual pixel dimensions, centered on the screen.
            *   If the image is larger than the screen, it will be cropped by the screen edges.
            *   The filename of the current image is displayed in the top-left corner of the screen (e.g., white text on a semi-transparent or black background).
        2.  **Fit (Default)**:
            *   Image is scaled down or up to fit entirely within the screen dimensions while maintaining its original aspect ratio.
            *   Black bars will appear if the image's aspect ratio does not match the screen's aspect ratio (letterboxing or pillarboxing).
        3.  **Cover**:
            *   Image is scaled (up or down) to cover the entire screen while maintaining its original aspect ratio.
            *   This may result in parts of the image being cropped if its aspect ratio differs from the screen's.
    *   **Keyboard Controls**:
        *   `Escape`: Quit the slideshow application.
        *   `Spacebar`: Pause or resume the automatic advancement of images. When paused, the current image remains displayed. When resumed, the slideshow continues from the current image, respecting the interval.
        *   `Right Arrow`: Manually advance to the next image. If paused, it shows the next image and remains paused. If running, it interrupts the current interval, shows the next image, and a new interval timer starts.
        *   `Left Arrow`: Manually go back to the previous image. Behavior similar to the right arrow but for the previous image.
        *   `Enter`: Cycle through the display modes (Original → Fit → Cover → Original). The current image should update to the new mode immediately.
    *   **Image Handling**:
        *   Recursively search for images in subdirectories is NOT a current feature.
        *   Images are typically sorted alphabetically by filename by default if not in random mode.
        *   If an image file is corrupted or cannot be opened, it should be skipped, and a message can be logged to the console. The slideshow should attempt to proceed to the next image.
        *   If no images are found in the specified folder (or after filtering), the tool should inform the user and exit gracefully.
    *   **Error Handling**:
        *   Report if the specified folder doesn't exist.
        *   Handle invalid interval values.
