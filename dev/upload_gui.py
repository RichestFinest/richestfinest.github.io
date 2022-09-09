import os
import base64
import io
import datetime

import PySimpleGUI as sg
import PIL
from PIL import Image

from upload import upload
import errors
import traceback


def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im


def convert_to_bytes(file_or_bytes, resize, fill=False):
    """
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :param fill: If True then the image is filled/padded so that the image is not distorted
    :type fill: (bool)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    """
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height / cur_height, new_width / cur_width)
        img = img.resize((int(cur_width * scale), int(cur_height * scale)), PIL.Image.ANTIALIAS)
    if fill:
        if resize is not None:
            img = make_square(img, resize[0])
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()


file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ],
    [
        sg.Button('Custom Date')
    ],
    [
        sg.Button("Upload")
    ]
]

window = sg.Window("Riche$t Fine$t Upload Wizard", layout, resizable=True)
try:
    while True:
        event, values = window.read()

        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except:
                file_list = []
    
            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".jpeg", ".jpg", ".png", ".svg", ".webp"))
            ]
            window["-FILE LIST-"].update(fnames)
    
        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                window["-TOUT-"].update(filename)
    
                with open(filename, 'rb') as f:
                    image_bytes = f.read()
    
                window["-IMAGE-"].update(data=convert_to_bytes(image_bytes, [504, 378]))
            except:
                pass
    
        elif event == "Custom Date":
            custom_date = sg.popup_get_date()
            custom_date = datetime.date(custom_date[2], custom_date[1], custom_date[0])


        elif event == "Upload" and "filename" in locals():
            if not "custom_date" in locals():
                custom_date = None

            try:
                upload(filename)
            except errors.OverrideWarning:
                override = sg.PopupOKCancel("Today's comic already exists. Override?") == 'OK'
    
                if override:
                    upload(filename, override=True)
    
        elif event == "Upload" and "filename" not in locals():
            sg.PopupOK("You must select a file first!", no_titlebar=True, background_color="red")
    
        elif event == "Exit" or event == sg.WIN_CLOSED:
            break

except Exception as e:
    traceback.print_exc()
    sg.popup_error_with_traceback("An error occurred! Send a screenshot of this window to Liam (Filajabob), and tell him what you were doing.", e)

window.close()