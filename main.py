from tkinter import *
from PIL import Image, ImageDraw, ImageFont
import tkinter.filedialog as fd
import os


def upload_files():
    files = fd.askopenfilenames(parent=root, title='Choose a file')

    desktop = os.path.expanduser("~/Desktop")
    newpath = f'{desktop}/watermarked-imgs'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    for file in files:
        file_path = file.title()
        filename = file_path.split('/')[-1].lower()
        filename_split = filename.split('.')
        new_filename = f"{filename_split[0]}_watermarked.{filename_split[1]}"

        with Image.open(file).convert("RGBA") as base:
            # make a blank image for the text, initialized to transparent text color
            txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

            base_width, base_height = base.size
            anchor_x = base_width * 0.95
            anchor_y = base_height * 0.95

            # get a font
            fnt = ImageFont.truetype("/System/Library/Fonts/Supplemental/Verdana.ttf", 40)
            # get a drawing context
            d = ImageDraw.Draw(txt)

            # Set Opacity
            opac = opacity_level.get() * 255 // 100

            # draw text
            d.multiline_text((anchor_x, anchor_y), watermark_text.get(), font=fnt, anchor="rd", fill=(255, 255, 255, opac))

            out = Image.alpha_composite(base, txt)

            out.save(f'{desktop}/watermarked-imgs/{new_filename}')

    root.destroy()


root = Tk()

window_width = 500
window_height = 300

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.title('Auto Watermarker')

watermark_text = StringVar()
opacity_level = IntVar()

watermark_interface = Frame(root)
watermark_interface.pack(padx=10, pady=10, fill='x', expand=True)

# watermark entry
watermark_prompt_label = Label(watermark_interface, text="Enter the watermark text:")
watermark_prompt_label.pack(fill='x', expand=True)

watermark_entry = Entry(watermark_interface, textvariable=watermark_text)
watermark_entry.pack(fill='x', expand=True)
watermark_entry.focus()

# opacity entry
opacity_prompt_label = Label(watermark_interface, text="Enter the opacity level out of 100:")
opacity_prompt_label.pack(fill='x', expand=True)

opacity_entry = Entry(watermark_interface, textvariable=opacity_level)
opacity_entry.pack(fill='x', expand=True)
opacity_entry.focus()

# upload files
upload_button = Button(watermark_interface, text="Import Files & Add Watermark!", command=upload_files)
upload_button.pack(fill='x', expand=True, pady=10)

# Notification of file save location
save_location_label = Label(watermark_interface, text="Files will be saved in a folder on your desktop named 'watermarked-imgs'.")
save_location_label.pack(fill='x', expand=True)

# keep the window displaying
root.mainloop()