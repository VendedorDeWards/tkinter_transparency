import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog, Tk, Label, Button


class Program:
    def __init__(self, master):
        self.master = master
        master.title("Transparency program")
        master.geometry("300x250")

        self.image_path = None
        self.loaded_image_rgb = None
        self.preview_image_rgb = None
        self.tk_image_rgb = None
        self.loaded_image_transparent = None
        self.preview_image_transparent = None
        self.tk_image_transparent = None

        self.panel_a = None
        self.panel_b = None

        self.label = Label(master, text="Look at this transparency...")
        self.label.pack()

        self.open_file_label = Label(master)
        self.open_file_label.pack()

        self.open_file_button = Button(master, text="Open File...", command=self.load_image)
        self.open_file_button.pack()

    def load_image(self):
        self.image_path = filedialog.askopenfilename(
            initialdir="/",
            title="Select file",
            filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*"))
        )

        self.loaded_image_rgb = cv2.cvtColor(cv2.imread(self.image_path), cv2.COLOR_BGR2RGB)
        self.preview_image_rgb = cv2.resize(self.loaded_image_rgb, (0, 0), fx=0.2, fy=0.2)
        self.tk_image_rgb = Image.fromarray(self.preview_image_rgb)
        self.tk_image_rgb = ImageTk.PhotoImage(self.tk_image_rgb)

        self.loaded_image_transparent = self.cvt_transparent(self.loaded_image_rgb)
        self.preview_image_transparent = cv2.resize(self.loaded_image_transparent, (0, 0), fx=0.2, fy=0.2)
        self.tk_image_transparent = Image.fromarray(self.preview_image_transparent)
        self.tk_image_transparent = ImageTk.PhotoImage(self.tk_image_transparent)

        self.open_file_label["text"] = self.image_path

        self.panel_a = self.update_panel(self.panel_a, self.tk_image_rgb, "left")
        self.panel_b = self.update_panel(self.panel_b, self.tk_image_transparent, "right")

    @staticmethod
    def update_panel(panel, image, side):
        if panel is None:
            panel = Label(image=image)
            panel.image = image
            panel.pack(side=side, padx=10, pady=10)
        else:
            panel.configure(image=image)
            panel.image = image

        return panel

    # def update_panels(self, image_a, image_b):
    #     if self.panel_a is None or self.panel_b is None:
    #         self.panel_a = Label(image=image_a)
    #         self.panel_a.image = image_a
    #         self.panel_a.pack(side="left", padx=10, pady=10)
    #
    #         self.panel_b = Label(image=image_b)
    #         self.panel_b.image = image_b
    #         self.panel_b.pack(side="right", padx=10, pady=10)
    #
    #     else:
    #         self.panel_a.configure(image=image_a)
    #         self.panel_b.configure(image=image_b)
    #
    #         self.panel_a.image = image_a
    #         self.panel_b.image = image_b

    @staticmethod
    def cvt_transparent(image):
        loaded_image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        ret, mask = cv2.threshold(loaded_image_gray, 220, 255, cv2.THRESH_BINARY_INV)
        cv2.imshow("mask", mask)
        # mask_inv = cv2.bitwise_not(mask)
        cv2.imwrite("./transparent.png", cv2.bitwise_and(image, image, mask=mask))
        return cv2.bitwise_and(image, image, mask=mask)


root = Tk()
my_program = Program(root)
root.mainloop()

