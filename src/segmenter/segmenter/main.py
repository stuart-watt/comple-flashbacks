"""The main handler function which sends a stock report to discord"""

# pylint --extension-pkg-whitelist=cv2

from time import perf_counter

import tkinter as TK
import tkinter.messagebox as tkmb
from tkinter.filedialog import askopenfilename, asksaveasfilename
import cv2
from PIL import ImageTk, Image

# pylint: disable=import-error
from utils.utils import select_train_images


class Segmenter:
    """Doc"""

    # pylint: disable=no-member
    def __init__(self):
        self.model = None
        self.filename = None
        self.imgtk = None
        self.display = None
        self.w = None
        self.tiles = []

    def get_file(self):
        """doc"""

        self.filename = askopenfilename()
        print(self.filename)

        # Display the file path
        self.display.delete(0, TK.END)
        self.display.insert(0, self.filename)
        # Load an color image
        img = cv2.imread(self.filename)
        # Resize the image to fit the window height
        scale_f = max(img.shape) / 550
        img = cv2.resize(img, (0, 0), fx=1 / scale_f, fy=1 / scale_f)

        # Rearrang the color channel from BGR to RGB
        b, g, r = cv2.split(img)
        img = cv2.merge((r, g, b))

        # Convert to ImageTK object
        im = Image.fromarray(img)
        self.imgtk = ImageTk.PhotoImage(image=im)

        self.w.config(image=self.imgtk)

    def segment(self):
        """Doc"""

        if self.filename is not None:
            tkmb.showinfo(
                "Selecting training segments",
                """
                How to collect training data:\n
                    1. Click/drag to create box around plant segments.
                    2. Draw as many as required.
                    3. Press 'c' to save segments and continue.
                    4. Press 'r' to clear the selections and refresh.
                """,
            )
            self.tiles = select_train_images(self.filename)
            print(self.tiles)
        else:
            tkmb.showerror("Error", "No image selected")

    def save(self):
        """Doc"""

        if self.tiles is not None:
            save_file = asksaveasfilename()
            print(save_file)
            for t, tile in enumerate(self.tiles):
                file = save_file + f"_{t}.jpg"
                print("Saving to", file)
                cv2.imwrite(file, tile)
        else:
            tkmb.showerror("Error", "No segmenets selected!")

    def run(self):
        """Doc"""

        root = TK.Tk()

        self.filename = None

        root.title("PCC")

        # Create the whole window
        f1 = TK.Frame(root, bg="green", relief="ridge", bd=10, height=590, width=550)
        f2 = TK.Frame(f1, bg="white", height=590, width=550)

        # Create the toolbar and image window
        toolbar = TK.Frame(f2, bg="gray", height=40, width=550)
        image_window = TK.Frame(f2, bg="white", height=550, width=550)

        for frame in (f1, f2):
            frame.pack(side=TK.TOP)
            frame.pack_propagate(0)

        toolbar.place(height=40, width=550)
        image_window.place(y=40, height=550, width=550)
        image_window.pack_propagate(0)

        self.w = TK.Label(image_window, bg="white")
        self.w.place(height=550, width=550)

        # Define the buttons
        get_image = TK.Button(
            toolbar,
            text="Select image",
            font="Helvetica 10 bold",
            bg="blue",
            command=self.get_file,
        )

        select_segments = TK.Button(
            toolbar,
            text="Segment Image",
            font="Helvetica 10 bold",
            bg="green",
            command=self.segment,
        )

        save_words = TK.Button(
            toolbar,
            text="Save words",
            font="Helvetica 10 bold",
            bg="red",
            command=self.save,
        )

        get_image.pack(side=TK.LEFT, fill=TK.Y)
        select_segments.pack(side=TK.LEFT, fill=TK.Y)
        save_words.pack(side=TK.LEFT, fill=TK.Y)

        self.display = TK.Entry(root, font="Helvetica 10 bold")
        self.display.pack(side=TK.LEFT, fill=TK.X, expand=True)
        self.display.insert(0, "No file selected")

        root.mainloop()


##########
## Main ##
##########

if __name__ == "__main__":
    start = perf_counter()
    Segmenter().run()
    print(f"Execution time: {perf_counter() - start:.2f} seconds")
