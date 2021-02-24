import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog, Tk, Frame, Label, Button


class Program:
    def __init__(self, master):
        self.master = master
        master.title("Transparency program")
        self.master_width, self.master_height = (500, 450)
        master.geometry(f"{self.master_width}x{self.master_height}")

        self.image_path = None
        self.loaded_image_rgb = None
        self.loaded_image_transparent = None
        self.panel_a = None
        self.panel_b = None

        self.top_frame = Frame(master, width=self.master_width, height=self.master_height/10, pady=5)
        self.top_frame.grid(row=0, columnspan=2)
        self.center_frame = Frame(master, width=self.master_width, height=self.master_height/10*7, pady=5)
        self.center_frame.grid(row=1, columnspan=2)
        self.bottom_frame = Frame(master, width=self.master_width, height=self.master_height/10*2, pady=5)
        self.bottom_frame.grid(row=2, columnspan=2)

        self.label = Label(self.top_frame, text="Look at this transparency...")
        self.path_file_label = Label(self.bottom_frame, wraplength=250)
        self.open_file_button = Button(self.bottom_frame, text="Open File...", command=self.load_image)

        self.label.grid(row=0, columnspan=2)
        self.path_file_label.grid(row=0, columnspan=2)
        self.open_file_button.grid(row=1, column=1)

    def load_image(self):
        self.image_path = filedialog.askopenfilename(
            initialdir="/",
            title="Select file",
            filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*"))
        )

        try:
            self.loaded_image_rgb = cv2.cvtColor(cv2.imread(self.image_path), cv2.COLOR_BGR2RGB)
            self.loaded_image_transparent = self.cvt_transparent(self.loaded_image_rgb)

            self.path_file_label["text"] = self.image_path

            self.panel_a = self.update_panel(self.panel_a, self.loaded_image_rgb, "left")
            self.panel_b = self.update_panel(self.panel_b, self.loaded_image_transparent, "right")

            self.panel_a.grid(row=0, column=0)
            self.panel_b.grid(row=0, column=1)
        except cv2.error:
            print("no file loaded!")
        except:
            print("error!")

    def update_panel(self, panel, image, side):
        height, width, channels = image.shape
        constraint = height if height > width else width
        ratio = (self.master_width/2-30)/constraint
        tk_preview_image = ImageTk.PhotoImage(Image.fromarray(cv2.resize(image, (0, 0), fx=ratio, fy=ratio)))
        if panel is None:
            panel = Label(self.center_frame, image=tk_preview_image)
            panel.image = tk_preview_image
        else:
            panel.configure(image=tk_preview_image)
            panel.image = tk_preview_image

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
        # cv2.imshow("mask", mask)
        # cv2.imwrite("./transparent.png", cv2.bitwise_and(image, image, mask=mask))
        return cv2.bitwise_and(image, image, mask=mask)


root = Tk()
my_program = Program(root)
root.mainloop()

