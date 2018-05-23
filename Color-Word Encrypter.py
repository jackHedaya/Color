# Copyright Jack Hedaya (c) 2017 Copyright Holder All Rights Reserved.

from tkinter import *
from tkinter import filedialog
from enum import Enum
from PIL import ImageGrab, ImageTk, Image
from pathlib import Path
import os

class WindowType:
    NONE = 1
    ENCRYPT = 2
    DECRYPT = 3

def negToZero(i):
    if i < 0:
        return 0
    else:
        return i

def getLocationUnder( window ):
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    w = window.winfo_width()
    h = window.winfo_height()
    return ('+%d+%d' % (x, y + h))

def last(array):
    return array[len(array) - 1]

def numsToIndex(im, pos):
    arr = im.getdata()
    return (im.width * pos[1]) + pos[0]

def droplast(tup):
    rTup = ()

    for x in range(0, len(tup)):
        rTup = rTup + (tup[x],)

    return rTup

def encrpytMode():
    global winType

    if winType is WindowType.ENCRYPT:
        return

    def runEncrypt():
        encrypt(messE.get())

    tk.wm_title("Word Encrypter")

    encryptB.pack_forget()
    label = Label(tk, text = "Message:")

    messE = Entry(tk)
    messE.focus_set()

    eB = Button(tk, text = "Encrypt", width = 15, command = runEncrypt)

    label.pack()
    messE.pack()
    eB.pack()

    winType = WindowType.ENCRYPT

def decryptMode():
    filepath = None

    def browse():
        filepath =  filedialog.askopenfilename(initialdir = "~/", title = "Select Image File", filetypes = (("png files", "*.png"), ("all files","*.*")))
        ent.delete(0,END)
        ent.insert(0, filepath)

    global winType

    if winType is WindowType.DECRYPT:
        return

    decryptB.pack_forget()

    tk.wm_title("Color Decrypter")

    label = Label(tk, text = "Select Image File:")
    ent = Entry(tk)
    selB = Button(text = "Browse...", command = browse)
    decrB = Button(tk, text = "Decrypt Image", command = lambda: decrypt(ent.get()))

    label.pack()
    ent.pack()
    selB.pack()
    decrB.pack()

def encrypt(m):
    global latestC
    global saveNums
    global encsIn

    if not m:
        return

    if encsIn < 3:
        eTk.withdraw()
        encsIn += 1
        encrypt(m)

        return

    saveNums = 0

    colorVals = []
    chars = list(m)

    for l in chars:
        num = ord(l)

        if len(colorVals) is 0 or len(colorVals[len(colorVals) - 1]) % 3 is 0:
            colorVals.append([num])
        else:
            colorVals[len(colorVals) - 1].append(num)

    while len(last(colorVals)) < 3:
        last(colorVals).append(0)

    print(colorVals)
    saveB.pack_forget()

    eTk.deiconify()

    eTk.geometry(getLocationUnder(tk))
    eTk.wm_title("Encrypted Image")

    c = Canvas(eTk, width=tk.winfo_width(), height=106)
    c.configure(background = "#F4EDF9")
    c.pack()

    latestC = c

    for ind, val in enumerate(colorVals):
        color = '#%02x%02x%02x' % (val[0], val[1], val[2])

        c.create_rectangle(eTk.winfo_width() / len(colorVals) * (ind), 0, eTk.winfo_width() / len(colorVals) * (ind + 1), eTk.winfo_height(), fill=color)

    for i in range(0, len(colorVals)):
        saveNums += 1

    saveB.pack()

def decrypt(path):

    if not path:
        return

    message = None

    col = (244, 237, 249, 255)

    im = Image.open(path)
    im.load()
    img = ImageTk.PhotoImage(im)

    pix_vals = im.getdata()

    if pix_vals[numsToIndex(im, (29, 0))] == col and pix_vals[numsToIndex(im, (0, 35))] == col and pix_vals[numsToIndex(im, (0, 8))] == col:
        dTk.deiconify()
        dTk.wm_title("Decrypted Message")

        l = Canvas(dTk, width=tk.winfo_width(), height=106)

        im2 = Image.new('RGB', (dTk.winfo_width(), tk.winfo_height()))
        im2.putdata(pix_vals)

        f = True
        amount = 1

        colors = []

        while f:
            if pix_vals[numsToIndex(im, (0, 75 + amount))] == col:
                amount += 1
            else:
                f = False

        for i in range(0, amount):
            colors.append(pix_vals[int((im.width * (im.height / 2)) + (im.width / amount / 2) + ((i - 1) * (im.width / amount)) )])

        change = colors.pop(0)
        colors.append(change)

        for ind, val in enumerate(colors):
            color = '#%02x%02x%02x' % (val[0], val[1], val[2])

            l.create_rectangle(dTk.winfo_width() / len(colors) * (ind), 0, dTk.winfo_width() / len(colors) * (ind + 1), dTk.winfo_height(), fill=color)

        for (a, b, c, d) in colors:
            print(a)
            print(b)
            print(c)

            print(chr(a))
            print(chr(b))

            if not c == 0:
                print(chr(c))

        l.pack()
    else:
        lab = Label(tk, text = "Image is not an encrypted message in color", fg = "red")
        lab.pack()

        panel = Label(dTk, image = img)
        panel.image = img
        panel.pack()

        dTk.wm_title("Failure Image")
        dTk.deiconify()

        return

def saveImage(root, widget):
    global saveNums

    x=root.winfo_rootx()+widget.winfo_x()
    y=root.winfo_rooty()+widget.winfo_y()
    x1=x+widget.winfo_width()
    y1=y+widget.winfo_height()

    image = ImageGrab.grab().crop((x,y,x1,y1))

    col = (244, 237, 249)
    image.putpixel((0, 35), col)
    image.putpixel((29, 0), col)
    image.putpixel((0, 8), col)

    for i in range(0, saveNums):
        image.putpixel((0, 75 + i), col)

    """
        num = 1
        if Path(os.getcwd() + "/EncryptedImage.png").is_file():
            while Path(os.getcwd() + "/EncryptedImage%d.png" % (num)).is_file():
                num += 1

            image.save("EncryptedImage%d.png" % (num))
        else:
    """

    image.save("EncryptedImage.png")

def eTkQuit():
    for i in eTk.winfo_children():
        i.pack_forget()

    eTk.withdraw()

def dTkQuit():
    for i in dTk.winfo_children():
        i.pack_forget()

    dTk.withdraw()

tk = Tk()
eTk = Toplevel()
dTk = Toplevel()

tk.resizable(0,0)
eTk.resizable(0, 0)
dTk.resizable(0, 0)

latestC = None

encsIn = 0

saveNums = 0

saveB = Button(eTk, text = "Save Image", width = 15, command = lambda: saveImage(eTk, latestC))

dTk.withdraw()
dTk.protocol("WM_DELETE_WINDOW", dTkQuit)
eTk.withdraw()
eTk.protocol("WM_DELETE_WINDOW", eTkQuit)

winType = WindowType.NONE

tk.wm_title("Color-Word Encrypter/Decrypter")

encryptB = Button(tk, text = "Encrpypt Message", width = 20, command = encrpytMode)
encryptB.pack()

decryptB = Button(tk, text = "Decrypt Colors", width = 20, command = decryptMode)
decryptB.pack()

mainloop()
