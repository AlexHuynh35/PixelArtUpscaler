from PIL import Image, ImageTk
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

class PixelArtUpscaler:
    def __init__(self, root):
        self.root = root
        self.image_path = tk.StringVar()
        self.image_width = tk.IntVar(value=0)
        self.image_height = tk.IntVar(value=0)
        self.max_width = tk.IntVar(value=160)
        self.max_height = tk.IntVar(value=240)
        self.scale_factor = tk.IntVar(value=32)
        self.output_path = tk.StringVar()

        self.createApp(root)

    def createApp(self, root):
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.main_frame = tk.Frame(root)
        self.main_frame.grid(row=0, column=0)

        self.title_label = tk.Label(
            self.main_frame,
            text="Pixel Art Upscaler",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.grid(row=0, column=0)

        pixel = tk.PhotoImage(width=1, height=1)
        self.browse_button = tk.Button(
            self.main_frame,
            text="Browse Image",
            image=pixel,
            compound="c",
            command=self.browseImages,
            width=self.max_width.get(),
            height=self.max_height.get()
        )
        self.browse_button.grid(row=1, column=0)
        self.browse_button.image = pixel

        self.scale_entry = tk.Entry(
            self.main_frame,
            textvariable=self.scale_factor
        )
        self.scale_entry.grid(row=2, column=0)

        self.output_frame = tk.Frame(self.main_frame)
        self.output_frame.grid(row=3, column=0)

        self.output_button = tk.Button(
            self.output_frame,
            text="Choose Output Folder",
            command=self.chooseOutputFolder
        )
        self.output_button.grid(row=0, column=0)

        self.output_label = tk.Label(
            self.output_frame,
            text="/",
            font=("Helvetica", 12, "bold")
        )
        self.output_label.grid(row=0, column=1)

        self.upscale_button = tk.Button(
            self.main_frame,
            text="Upscale",
            command=self.upscaleImage
        )
        self.upscale_button.grid(row=4, column=0)

    def browseImages(self):
        image_path = filedialog.askopenfilename(
            filetypes=[
                ("PNG Files", "*.png"),
                ("All Files", "*.*")
            ],
            parent=self.root
        )

        if not image_path:
            return -1

        self.image_path.set(image_path)

        img = Image.open(self.image_path.get())

        self.image_width.set(img.width)
        self.image_height.set(img.height)

        ratio = min(
            self.max_width.get() / self.image_width.get(),
            self.max_height.get() / self.image_height.get()
        )
        new_width = int(self.image_width.get() * ratio)
        new_height = int(self.image_height.get() * ratio)
        new_img = img.resize(
            (
                new_width,
                new_height
            ),
            Image.Resampling.NEAREST
        )
        
        bg_img = Image.new(
            'RGBA',
            (
                self.max_width.get(),
                self.max_height.get()
            ),
            (0, 0, 0, 0)
        )
        bg_img.paste(
            new_img,
            (
                (self.max_width.get() - new_width) // 2,
                (self.max_height.get() - new_height) // 2
            )
        )

        photo = ImageTk.PhotoImage(bg_img)
        self.browse_button.config(
            text="",
            image=photo
        )
        self.browse_button.image = photo

        return 0

    def chooseOutputFolder(self):
        output_path = filedialog.askdirectory(parent=self.root)

        if not output_path:
            return -1

        self.output_path.set(output_path)

        self.output_label.config(
            text=self.output_path.get()
        )

        return 0

    def upscaleImage(self):
        if not self.image_path.get():
            if self.browseImages() == -1:
                return -1

        img = Image.open(self.image_path.get())

        upscaled = img.resize(
            (
                img.width * self.scale_factor.get(),
                img.height * self.scale_factor.get()
            ),
            Image.NEAREST
        )

        if not self.output_path.get():
            if self.chooseOutputFolder() == -1:
                return -1

        output = (
            Path(self.output_path.get())
            / f"{Path(self.image_path.get()).stem}_upscaled.png"
        )

        upscaled.save(output)

        return 0

    def getOutputDimensions(self):
        return (
            self.image_width.get() * self.scale_factor.get(),
            self.image_height.get() * self.scale_factor.get()
        )
