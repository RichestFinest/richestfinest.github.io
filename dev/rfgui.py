import os
import base64
import io
import datetime
import traceback

import PySimpleGUI as sg
import PIL
from PIL import Image

from upload import upload
import errors
from update import update
from send_emails import send_custom_emails

print("This is the Riche$t Fine$t Console. This is where you can see the details of the processes that are running, and any error tracebacks that may occur.")


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




def setup_upload_wizard():
    file_list_column = [
        [
            sg.Text("Image Folder"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(button_text="Select Parent Folder"),
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

    upload_layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(image_viewer_column),
        ],
        [
            sg.Button('Custom Date')
        ],
        [
            sg.Button("Upload"), sg.Button("Menu")
        ]
    ]

    upload_window = sg.Window("Richest Finest Upload Wizard", upload_layout, resizable=True)

    while True:
        event, values = upload_window.read()

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
            upload_window["-FILE LIST-"].update(fnames)
    
        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                upload_window["-TOUT-"].update(filename)
    
                with open(filename, 'rb') as f:
                    image_bytes = f.read()
    
                upload_window["-IMAGE-"].update(data=convert_to_bytes(image_bytes, [504, 378]))
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
                sg.popup_ok("Upload suite completed. You can close the application, or upload more comics.")
            except errors.OverrideWarning:
                override = sg.PopupOKCancel("Today's comic already exists. Override?") == 'OK'
    
                if override:
                    upload(filename, override=True)
                    sg.popup_ok("Upload suite completed. You can close the application, or upload more comics.")
    
        elif event == "Upload" and "filename" not in locals():
            sg.PopupOK("You must select a file first!", no_titlebar=True, background_color="red")

        elif event == "Menu":
            upload_window.close()
            setup_main_menu()

            return
    
        elif event == "Exit" or event == sg.WIN_CLOSED:
            break

    upload_window.close()

def setup_subscriber_notifier():
    notifier_layout = [
            [sg.Text("Subject: "), sg.InputText(key="subject")],
            [sg.Multiline(size=(150, 30), key="email_text_content")],
            [sg.Text("Tip: \"[name]\" will be replaced by the recipent's name. Ex: Hello, [name]")],
            [sg.Button("Send"), sg.Button("Menu")]
        ]

    notifier_window = sg.Window("Richest Finest Subscriber Notifier", notifier_layout, resizable=True)
    while True:
        event, values = notifier_window.read()

        if event == "Send":
            email_text_content = values["email_text_content"]
            subject = values["subject"]

            send_custom_emails(subject, email_text_content)

            sg.popup_ok("Emails were sent successfully.")

        elif event == "Menu":
            notifier_window.close()
            setup_main_menu()

            return

        elif event == "Exit" or event == sg.WIN_CLOSED:
            break

    notifier_window.close()

def setup_main_menu():
    # Main menu
    menu_layout = [
        [sg.Text("Richest Finest GUI Main Menu")],
        [sg.Button("Upload Comic"), sg.Button("Update"), sg.Button("Send Emails to Subscribers")]
    ]

    menu_window = sg.Window("Richest Finest GUI Main Menu", menu_layout, resizable=True)

    while True:
        event, values = menu_window.read()

        if event == "Upload Comic":
            menu_window.close()
            setup_upload_wizard()

            return

        elif event == "Update":
            ok = sg.popup_ok_cancel("Are you sure you want to update?") == 'OK'

            if ok:
                update()
                sg.popup_ok(
                    f"Update completed. Please close the application and run {os.path.abspath('dev/build.py')} with Python before doing anything else. "
                    "(Ignore this if the console says \"Already up to date.\""
                )

        elif event == "Send Emails to Subscribers":
            menu_window.close()
            setup_subscriber_notifier()

            return


        elif event == "Exit" or event == sg.WIN_CLOSED:
            break

        menu_window.close()

    
try:
    setup_main_menu()
except Exception as e:
    traceback.print_exc()
    sg.popup_error_with_traceback("An error occurred! Send a screenshot of this upload_window to Liam (Filajabob), and tell him what you were doing.", e)
