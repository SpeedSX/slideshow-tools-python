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
    def __init__(self, master, image_paths, interval, original_arg, fit_cover_arg, is_random_mode, filter_horizontal_arg, filter_vertical_arg):
        self.master = master
        self.image_paths = image_paths
        self.interval_ms = int(interval * 1000)
        self.is_random_mode = is_random_mode
        self.filter_horizontal = filter_horizontal_arg
        self.filter_vertical = filter_vertical_arg
        self.current_image_index = 0
        self.last_successfully_shown_index = -1
        self.paused = False
        self.after_id = None

        self.display_modes = ['original', 'fit', 'cover']
        if original_arg:
            self.current_display_mode_index = self.display_modes.index('original')
        elif fit_cover_arg:
            self.current_display_mode_index = self.display_modes.index('cover')
        else:
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
        self.master.bind("<Return>", self.cycle_display_mode)

        self.image_label = Label(master, bg='black')
        self.image_label.pack(fill=tk.BOTH, expand=True)

        self.filename_label = Label(master, text="", bg="black", fg="white", font=("Arial", 10))

        self.show_image()

    def show_image(self, force_display=False):
        if self.paused and not force_display:
            return

        if not self.image_paths:
            self.quit_slideshow()
            return

        found_image_to_display_path = None
        actual_shown_idx = -1
        start_search_index = self.current_image_index

        for i in range(len(self.image_paths)):
            idx_to_check = (start_search_index + i) % len(self.image_paths)
            path_candidate = self.image_paths[idx_to_check]
            
            image_is_suitable = True
            if not self.is_random_mode and (self.filter_horizontal or self.filter_vertical):
                try:
                    with Image.open(path_candidate) as img:
                        width, height = img.size
                        if self.filter_horizontal and not (width > height):
                            image_is_suitable = False
                        elif self.filter_vertical and not (height > width):
                            image_is_suitable = False
                except Exception as e:
                    print(f"Warning: Could not read {os.path.basename(path_candidate)} for orientation check: {e}")
                    image_is_suitable = False

            if image_is_suitable:
                found_image_to_display_path = path_candidate
                actual_shown_idx = idx_to_check
                break
        
        if not found_image_to_display_path:
            print("No suitable images found to display (or all remaining images are unreadable/filtered).")
            self.quit_slideshow()
            return

        try:
            pil_image_original = Image.open(found_image_to_display_path)
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            img_width, img_height = pil_image_original.size

            pil_image_to_display = pil_image_original
            current_mode = self.display_modes[self.current_display_mode_index]

            if current_mode == 'original':
                basename = os.path.basename(found_image_to_display_path)
                self.filename_label.config(text=basename)
                self.filename_label.place(x=10, y=10)
            else:
                self.filename_label.place_forget()

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

            self.last_successfully_shown_index = actual_shown_idx

        except Exception as e:
            print(f"Error opening image {found_image_to_display_path}: {e}")
            self.current_image_index = (actual_shown_idx + 1) % len(self.image_paths) if len(self.image_paths) > 0 else 0
            if not self.paused:
                self.after_id = self.master.after(100, lambda: self.show_image(force_display=force_display))
            else:
                self.after_id = None
            return

        if self.is_random_mode and (actual_shown_idx + 1) >= len(self.image_paths) and len(self.image_paths) > 0:
            random.shuffle(self.image_paths)
            self.current_image_index = 0
        elif len(self.image_paths) > 0:
            self.current_image_index = (actual_shown_idx + 1) % len(self.image_paths)
        else:
            self.current_image_index = 0

        if not self.paused:
            self.after_id = self.master.after(self.interval_ms, self.show_image)

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

        num_images = len(self.image_paths)
        if num_images == 0: return

        # Determine the starting point for our backward search.
        # If an image has been shown, start searching backward from the one before it.
        # Otherwise (e.g., at startup), start from the logical end of the list.
        start_search_back_idx = (self.last_successfully_shown_index - 1 + num_images) % num_images \
                                if self.last_successfully_shown_index != -1 else (num_images - 1)

        found_suitable_prev_image = False
        for i in range(num_images): # Iterate at most num_images times
            idx_to_check = (start_search_back_idx - i + num_images) % num_images # Go backwards
            path_candidate = self.image_paths[idx_to_check]
            
            image_is_suitable = True
            # Perform on-the-fly orientation check if not in random mode and a filter is active
            if not self.is_random_mode and (self.filter_horizontal or self.filter_vertical):
                try:
                    with Image.open(path_candidate) as img:
                        width, height = img.size
                        if self.filter_horizontal and not (width > height):
                            image_is_suitable = False
                        elif self.filter_vertical and not (height > width):
                            image_is_suitable = False
                except Exception as e:
                    print(f"Warning: Could not read {os.path.basename(path_candidate)} for orientation check (previous): {e}")
                    image_is_suitable = False 

            if image_is_suitable:
                self.current_image_index = idx_to_check # Set this so show_image displays it
                found_suitable_prev_image = True
                break
        
        # If no suitable previous image was found after checking all,
        # show_image will be called with the current_image_index, 
        # which might lead to it re-evaluating the same image or searching forward if that index is unsuitable.
        # This behavior is acceptable; it won't get stuck.

        self.show_image(force_display=True)

    def cycle_display_mode(self, event=None):
        if not self.image_paths:
            return
        self.filename_label.place_forget()

        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

        self.current_display_mode_index = (self.current_display_mode_index + 1) % len(self.display_modes)

        # To re-display the current image with the new mode:
        if self.last_successfully_shown_index != -1 and len(self.image_paths) > 0:
            self.current_image_index = self.last_successfully_shown_index
        # else: if no image was successfully shown, show_image will start from current_image_index (e.g. 0)

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

    if args.random and (args.horizontal or args.vertical):
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
                print(f"Warning: Could not read dimensions for {os.path.basename(image_path)} during pre-filtering: {e}")
        image_paths = filtered_paths

    if args.random:
        random.shuffle(image_paths)

    if not image_paths:
        print(f"No supported image files found in '{args.folder_path}'.")
        return

    root = tk.Tk()
    app = Slideshow(root, image_paths, args.interval, args.original, args.cover, args.random, args.horizontal, args.vertical)
    root.mainloop()

if __name__ == "__main__":
    main()
