from PIL import Image
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

class PixelArtUpscaler:
    def __init__(self, root):
        self.image_path = tk.StringVar()
        self.image_width = tk.IntVar(value=0)
        self.image_height = tk.IntVar(value=0)
        self.scale_factor = tk.IntVar(value=32)
        self.output_path = tk.StringVar()

        self.createApp(root)

    def createApp(self, root):
        self.title_label = tk.Label(
            root,
            text="Pixel Art Upscaler",
            font=("Helvetica", 16, "bold")
        )
        self.title_label.pack()

        self.browse_button = tk.Button(
            root,
            text="Browse Image",
            command=self.browseImages
        )
        self.browse_button.pack()

        self.scale_entry = tk.Entry(
            root,
            textvariable=self.scale_factor
        )
        self.scale_entry.pack()

        self.output_button = tk.Button(
            root,
            text="Choose Output Folder",
            command=self.chooseOutputFolder
        )
        self.output_button.pack()

        self.output_label = tk.Label(
            root,
            text="/",
            font=("Helvetica", 12, "bold")
        )
        self.output_label.pack()

        self.upscale_button = tk.Button(
            root,
            text="Upscale",
            command=self.upscaleImage
        )
        self.upscale_button.pack()

    def browseImages(self):
        self.image_path.set(
            filedialog.askopenfilename(
                filetypes=[
                    ("PNG Files", "*.png"),
                    ("All Files", "*.*")
                ]
            )
        )

        img = Image.open(self.image_path.get())

        self.image_width.set(img.width)
        self.image_height.set(img.height)

    def chooseOutputFolder(self):
        self.output_path.set(
            filedialog.askdirectory()
        )

        self.output_label.config(
            text=self.output_path.get()
        )

    def upscaleImage(self):
        img = Image.open(self.image_path.get())

        upscaled = img.resize(
            (
                img.width * self.scale_factor.get(),
                img.height * self.scale_factor.get()
            ),
            Image.NEAREST
        )

        output = (
            Path(self.output_path.get()) / f"{Path(self.image_path.get()).stem}_upscaled.png"
        )

        upscaled.save(output)

    def getImageDimensions(self):
        return (self.image_width.get(), self.image_height.get())

    def getOutputDimensions(self):
        return (self.image_width.get() * self.scale_factor.get(), self.image_height.get() * self.scale_factor.get())
