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
        self.max_width = tk.IntVar(value=240)
        self.max_height = tk.IntVar(value=240)
        self.scale_factor = tk.IntVar(value=32)
        self.scale_factor.trace_add("write", self.onScaleChange)
        self.output_path = tk.StringVar()

        self.createApp(root)

    def createApp(self, root):
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.main_frame = tk.Frame(root)
        self.main_frame.grid(row=0, column=0)

        self.title_frame = tk.Frame(self.main_frame)
        self.title_frame.grid(row=0, column=0, pady=20)

        self.title_label_1 = tk.Label(
            self.title_frame,
            text="Pixel",
            font=("Helvetica", 60, "bold"),
            fg="red"
        )
        self.title_label_1.grid(row=0, column=0)
        self.title_label_2 = tk.Label(
            self.title_frame,
            text="Art",
            font=("Helvetica", 60, "bold"),
            fg="blue"
        )
        self.title_label_2.grid(row=0, column=1)
        self.title_label_3 = tk.Label(
            self.title_frame,
            text="Upscaler",
            font=("Helvetica", 60, "bold")
        )
        self.title_label_3.grid(row=0, column=2)

        self.sub_frame = tk.Frame(self.main_frame)
        self.sub_frame.grid(row=1, column=0, pady=20)

        self.browse_canvas = tk.Canvas(
            self.sub_frame,
            width=self.max_width.get(),
            height=self.max_height.get()
        )
        self.browse_canvas.grid(row=0, column=0, padx=10)

        self.browse_border = self.browse_canvas.create_rectangle(
            4,
            4,
            self.max_width.get() - 4,
            self.max_height.get() - 4,
            dash=(4, 4)
        )
        self.browse_text = self.browse_canvas.create_text(
            self.max_width.get() / 2,
            self.max_height.get() / 2,
            text="Browse Image",
            font=("Helvetica", 16),
        )
        self.browse_image = self.browse_canvas.create_image(
            self.max_width.get() / 2,
            self.max_width.get() / 2,
            anchor="center"
        )
        self.browse_canvas.bind(
            "<Button-1>",
            lambda e: self.browseImages()
        )

        self.side_frame = tk.Frame(self.sub_frame)
        self.side_frame.grid(row=0, column=1, padx=10)

        vcmd = (root.register(self.onScaleValidate))
        self.scale_entry = tk.Entry(
            self.side_frame,
            textvariable=self.scale_factor,
            font=("Helvetica", 16),
            width=20,
            validate='all',
            validatecommand=(vcmd, '%P')
        )
        self.scale_entry.grid(row=0, column=0, pady=10)
        self.scale_entry.bind(
            "<Return>",
            lambda e: self.updateScale()
        )

        self.res_frame = tk.Frame(self.side_frame)
        self.res_frame.grid(row=1, column=0, pady=10)

        self.before_label = tk.Label(
            self.res_frame,
            text="Original Resolution: ",
            font=("Helvetica", 16),
            anchor="e",
            justify="right",
            width=18
        )
        self.before_label.grid(row=0, column=0)
        self.before_res = tk.Label(
            self.res_frame,
            text="0 X 0",
            font=("Helvetica", 16),
            fg="red",
            anchor="w",
            justify="left",
            width=12
        )
        self.before_res.grid(row=0, column=1)

        self.after_label = tk.Label(
            self.res_frame,
            text="New Resolution: ",
            font=("Helvetica", 16),
            anchor="e",
            justify="right",
            width=18
        )
        self.after_label.grid(row=1, column=0)
        self.after_res = tk.Label(
            self.res_frame,
            text="0 X 0",
            font=("Helvetica", 16),
            fg="green",
            anchor="w",
            justify="left",
            width=12
        )
        self.after_res.grid(row=1, column=1)

        self.output_button = tk.Button(
            self.side_frame,
            text="Choose Output Folder",
            font=("Helvetica", 16),
            command=self.chooseOutputFolder,
            width=20,
            height=2
        )
        self.output_button.grid(row=2, column=0, pady=10)

        self.upscale_button = tk.Button(
            self.side_frame,
            text="Upscale",
            font=("Helvetica", 16),
            command=self.upscaleImage,
            width=20,
            height=2
        )
        self.upscale_button.grid(row=3, column=0, pady=10)

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
        self.browse_canvas.itemconfig(
            self.browse_image,
            image=photo
        )
        self.browse_canvas.image = photo
        self.browse_canvas.itemconfig(
            self.browse_text,
            text=""
        )
        self.browse_canvas.itemconfig(
            self.browse_border,
            fill="white",
            dash=()
        )

        self.before_res.config(
            text=str(self.image_width.get()) + " X " + str(self.image_height.get())
        )

        self.updateScale()

        return 0

    def onScaleValidate(self, P):
        return str.isdigit(P) or P == ""

    def onScaleChange(self, *args):
        self.updateScale()

    def updateScale(self):
        (output_width, output_height) = self.getOutputDimensions()
        self.after_res.config(
            text=str(output_width) + " X " + str(output_height)
        )

    def chooseOutputFolder(self):
        output_path = filedialog.askdirectory(parent=self.root)

        if not output_path:
            return -1

        self.output_path.set(output_path)

        self.output_button.config(
            text=self.output_path.get()[:10] + "..." + self.output_path.get()[-10:] if len(self.output_path.get()) > 20 else self.output_path.get()
        )

        return 0

    def upscaleImage(self):
        if not self.image_path.get():
            if self.browseImages() == -1:
                return -1

        img = Image.open(self.image_path.get())

        upscaled = img.resize(
            (
                img.width * self.getScaleFactor(),
                img.height * self.getScaleFactor()
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

    def getScaleFactor(self):
        try:
            scale = self.scale_factor.get() 
            return scale if scale >= 1 else 1
        except tk.TclError:
            return 1

    def getOutputDimensions(self):
        return (
            self.image_width.get() * self.getScaleFactor(),
            self.image_height.get() * self.getScaleFactor()
        )
