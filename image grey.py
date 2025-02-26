import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button, Text, Canvas
from PIL import Image, ImageTk

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        process_image(file_path)

def process_image(file_path):
    global img_tk, binary_image
    
    # Load the image in grayscale
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    
    # Convert to binary (0 = White, 1 = Black) and invert
    threshold = 127
    binary_image = (image < threshold).astype(int)  # Inverted
    
    # Convert binary matrix to text format
    binary_text = "\n".join("".join(map(str, row)) for row in binary_image)
    
    # Show binary data in text box
    binary_output.delete("1.0", tk.END)
    binary_output.insert(tk.END, binary_text)
    
    # Convert binary image for display
    display_image = (binary_image * 255).astype(np.uint8)
    img_pil = Image.fromarray(display_image)
    img_pil = img_pil.resize((250, 250))
    
    # Convert PIL image to Tkinter format and display
    img_tk = ImageTk.PhotoImage(img_pil)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.image = img_tk

def get_pixel_value(event):
    if binary_image is not None:
        x, y = event.x, event.y
        img_width, img_height = 250, 250  # Displayed image size
        rows, cols = binary_image.shape
        
        # Scale coordinates to match the original image size
        x = int(x * cols / img_width)
        y = int(y * rows / img_height)
        
        if 0 <= x < cols and 0 <= y < rows:
            pixel_value = binary_image[y, x]  # Read binary pixel value
            pixel_label.config(text=f"Pixel ({x}, {y}): {pixel_value}")

# Tkinter GUI Setup
root = tk.Tk()
root.title("Image to Binary Converter & Pixel Reader")

Button(root, text="Select Image", command=select_image).pack(pady=10)

# Canvas to display image
canvas = Canvas(root, width=250, height=250)
canvas.pack()
canvas.bind("<Motion>", get_pixel_value)

pixel_label = Label(root, text="Hover over the image to see pixel value")
pixel_label.pack()

Label(root, text="Binary Output (0 = White, 1 = Black):").pack()
binary_output = Text(root, height=15, width=50)
binary_output.pack(pady=10)

binary_image = None
root.mainloop()
