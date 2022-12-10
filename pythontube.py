from pytube import YouTube
from pytube import Playlist
from tkinter import *
from tkinter.ttk import *
import os

root = Tk()
option = IntVar()
option.set(0)
vidtru = 0


def changevarz():
    global vidtru
    vidtru = 0


def changevary():
    global vidtru
    vidtru = 1


vdio_format = Radiobutton(root,
                          variable=option,
                          value=0,
                          text='mp4',
                          command=changevarz)
vdio_format.grid(row=0, column=0)

plylist_format = Radiobutton(root,
                             variable=option,
                             value=1,
                             text='mp3',
                             command=changevary)
plylist_format.grid(row=0, column=2)

lbl = Label(root, text='Please input the Video link')
lbl.grid(row=0, column=1)

inpt = Entry(root, width=50)
inpt.grid(row=1, column=1)

root.columnconfigure(0, minsize=100)
root.rowconfigure(0, minsize=50)
root.columnconfigure(2, minsize=100)
root.rowconfigure(3, minsize=50)


def submitvideo():
    vd = YouTube(inpt.get())
    print("Downloading : " + vd.title)
    if vidtru == 0:
        vd.streams.get_highest_resolution().download(output_path='downloads/')
        print('succesfully downloaded')

    else:
        vid = vd.streams.filter(only_audio=True).first()
        outvid = vid.download(output_path='downloads/')
        base, ext = os.path.splitext(outvid)
        new_file = base + '.mp3'
        os.rename(outvid, new_file)
        print('succesfully downloaded')


sbmit = Button(root, text='Submit', command=submitvideo)
sbmit.grid(row=2, column=1)

lbl = Label(root, text='Please input the Playlist link')
lbl.grid(row=3, column=1)
inputt = Entry(root, width=50)
inputt.grid(row=4, column=1)


def submitplaylist():
    vd = Playlist(inputt.get())
    for i in vd.videos:
        print('Downloading : ' + i.title)

        if vidtru == 0:
            i.streams.get_highest_resolution().first().download(
                output_path='downloads/')
            print('succesfully downloaded')

        else:
            vid = i.streams.filter(only_audio=True).first()
            outvid = vid.download(output_path='downloads/')
            base, ext = os.path.splitext(outvid)
            new_file = base + '.mp3'
            os.rename(outvid, new_file)
            print('succesfully downloaded')


sbmit = Button(root, text='Submit', command=submitplaylist)
sbmit.grid(row=5, column=1)

root.mainloop()
