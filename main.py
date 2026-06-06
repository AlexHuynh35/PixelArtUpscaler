import tkinter as tk
from assets.upscaler import PixelArtUpscaler

def main():
    root = tk.Tk()

    root.title("Pixel Art Upscaler")
    root.geometry("800x500")

    upscaler_info = PixelArtUpscaler(root)

    root.mainloop()

if __name__ == "__main__":
    main()