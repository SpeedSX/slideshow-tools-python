'''
Image Slideshow Script

Usage:
python slideshow.py <folder_path> [--interval <seconds>] ([--original | --cover]) [--random] [--horizontal | --vertical]
'''
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import os
import argparse
import random

class Slideshow:
    def __init__(self, master, image_paths, interval, original_arg, fit_cover_arg, is_random_mode):
        self.master = master
        self.image_paths = image_paths
        self.interval_ms = int(interval * 1000)
        self.is_random_mode = is_random_mode
        self.current_image_index = 0
        self.paused = False
        self.after_id = None

        self.display_modes = ['original', 'fit', 'cover']
        # Default to 'fit' mode
        if original_arg: # --original explicitly chosen
            self.current_display_mode_index = self.display_modes.index('original')
        elif fit_cover_arg: # --cover explicitly chosen
            self.current_display_mode_index = self.display_modes.index('cover')
        else: # Neither --original nor --cover was specified, default to fit.
            self.current_display_mode_index = self.display_modes.index('fit')

        if not self.image_paths:
            print("No images found in the specified folder.")
            self.master.destroy()
            return

        self.master.attributes('-fullscreen', True)
        self.master.configure(bg='black')
        self.master.bind("<Escape>", self.quit_slideshow)
        self.master.bind("<space>", self.toggle_pause)
        self.master.bind("<Right>", self.next_image_manual)
        self.master.bind("<Left>", self.previous_image_manual)
        self.master.bind("<Return>", self.cycle_display_mode)  # Bind Enter key

        self.image_label = Label(master, bg='black')
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # Label for filename display
        self.filename_label = Label(master, text="", bg="black", fg="white", font=("Arial", 10))
        # This label will be shown/hidden and positioned in show_image

        self.show_image()

    def show_image(self, force_display=False):
        if self.paused and not force_display:
            return

        if not self.image_paths:
            self.quit_slideshow()
            return

        if self.current_image_index >= len(self.image_paths) or self.current_image_index < 0:
            self.current_image_index = 0
            if not self.image_paths:
                self.quit_slideshow()
                return

        image_path = self.image_paths[self.current_image_index]

        try:
            pil_image_original = Image.open(image_path)
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            img_width, img_height = pil_image_original.size

            pil_image_to_display = pil_image_original
            current_mode = self.display_modes[self.current_display_mode_index]

            # Update and manage filename label visibility
            if current_mode == 'original':
                basename = os.path.basename(image_path)
                self.filename_label.config(text=basename)
                self.filename_label.place(x=10, y=10)  # Position in top-left
            else:
                self.filename_label.place_forget()  # Hide if not in original mode

            if current_mode == 'fit':
                scale_ratio = min(screen_width / img_width, screen_height / img_height)
                new_w = int(img_width * scale_ratio)
                new_h = int(img_height * scale_ratio)
                pil_image_to_display = pil_image_original.resize((new_w, new_h), Image.Resampling.LANCZOS)

            elif current_mode == 'cover':
                scale_ratio = max(screen_width / img_width, screen_height / img_height)
                scaled_w = int(img_width * scale_ratio)
                scaled_h = int(img_height * scale_ratio)
                pil_image_scaled = pil_image_original.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
                crop_x = (scaled_w - screen_width) / 2
                crop_y = (scaled_h - screen_height) / 2
                left = int(crop_x)
                top = int(crop_y)
                right = int(left + screen_width)
                bottom = int(top + screen_height)
                pil_image_to_display = pil_image_scaled.crop((left, top, right, bottom))

            tk_image = ImageTk.PhotoImage(pil_image_to_display)
            self.image_label.config(image=tk_image)
            self.image_label.image = tk_image

        except Exception as e:
            print(f"Error opening image {image_path}: {e}")
            self.current_image_index += 1
            if self.current_image_index >= len(self.image_paths) and self.image_paths:
                self.current_image_index = 0

            if not self.paused:
                self.after_id = self.master.after(100, self.show_image)
            else:
                self.after_id = None
            return

        self.current_image_index += 1
        if self.current_image_index >= len(self.image_paths) and self.image_paths:
            if self.is_random_mode:
                random.shuffle(self.image_paths)
            self.current_image_index = 0

        if not self.paused:
            self.after_id = self.master.after(self.interval_ms, self.show_image)
        else:
            if self.after_id:
                self.master.after_cancel(self.after_id)
            self.after_id = None

    def toggle_pause(self, event=None):
        self.paused = not self.paused
        if not self.paused:
            self.show_image()
        elif self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

    def next_image_manual(self, event=None):
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None
        self.show_image(force_display=True)

    def previous_image_manual(self, event=None):
        if not self.image_paths:
            return
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

        self.current_image_index = (self.current_image_index - 2 + len(self.image_paths)) % len(self.image_paths)
        self.show_image(force_display=True)

    def cycle_display_mode(self, event=None):
        if not self.image_paths:
            return
        # It's good practice to clear the filename label immediately when mode changes
        # show_image will then re-evaluate if it needs to be shown.
        self.filename_label.place_forget()

        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

        self.current_display_mode_index = (self.current_display_mode_index + 1) % len(self.display_modes)

        if len(self.image_paths) > 0:
            self.current_image_index = (self.current_image_index - 1 + len(self.image_paths)) % len(self.image_paths)

        self.show_image(force_display=True)

    def quit_slideshow(self, event=None):
        self.master.destroy()

def main():
    parser = argparse.ArgumentParser(description="Display images from a folder in a slideshow.")
    parser.add_argument("folder_path", help="Path to the folder containing images.")
    parser.add_argument("--interval", type=float, default=5.0, 
                        help="Time interval between images in seconds (default: 5).")
    
    display_mode_group = parser.add_mutually_exclusive_group()
    display_mode_group.add_argument("--original", action="store_true",
                        help="Start in \"Original\" mode (images at their actual size, centered).")
    display_mode_group.add_argument("--cover", action="store_true",
                        help="Start in \"Cover\" mode (scales images to cover the entire screen, cropping if necessary).")

    parser.add_argument("--random", action="store_true",
                        help="Display images in a random order.")

    orientation_group = parser.add_mutually_exclusive_group()
    orientation_group.add_argument("--horizontal", action="store_true",
                                help="Show only horizontally oriented images (width > height).")
    orientation_group.add_argument("--vertical", action="store_true",
                                help="Show only vertically oriented images (height > width).")

    args = parser.parse_args()

    if not os.path.isdir(args.folder_path):
        print(f"Error: Folder '{args.folder_path}' not found.")
        return

    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    image_paths = sorted([
        os.path.join(args.folder_path, f) 
        for f in os.listdir(args.folder_path) 
        if f.lower().endswith(image_extensions) and os.path.isfile(os.path.join(args.folder_path, f))
    ])

    # Filter by orientation if specified
    if args.horizontal or args.vertical:
        filtered_paths = []
        for image_path in image_paths:
            try:
                with Image.open(image_path) as img:
                    width, height = img.size
                    if args.horizontal and width > height:
                        filtered_paths.append(image_path)
                    elif args.vertical and height > width:
                        filtered_paths.append(image_path)
            except Exception as e:
                # Print a warning but continue, in case some images are unreadable
                print(f"Warning: Could not read dimensions for {os.path.basename(image_path)} to check orientation: {e}")
        image_paths = filtered_paths

    if args.random:
        random.shuffle(image_paths)

    if not image_paths:
        print(f"No supported image files found in '{args.folder_path}'.")
        return

    root = tk.Tk()
    app = Slideshow(root, image_paths, args.interval, args.original, args.cover, args.random)
    root.mainloop()

if __name__ == "__main__":
    main()
