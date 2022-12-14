import os
import wx
from pytube import YouTube
import time
from threading import Thread

class ytthread(Thread):
    def __init__(self, args):
        super().__init__(args=args)
        self.start()

    def run(self):
        time.sleep(5)
        wx.CallAfter(self.yt(self._args[0], self._args[1]))

    def yt(self, link, type):
        vd = YouTube(link)
        print("Downloading : " + vd.title)

        if type == 'mp4':
            vd.streams.get_highest_resolution().download(output_path='downloads/')
            print('succesfully downloaded')

        else:
            vid = vd.streams.filter(only_audio=True).first()
            outvid = vid.download(output_path='downloads/')
            base = os.path.splitext(outvid)
            new_file = base + '.mp3'
            os.rename(outvid, new_file)
            print('succesfully downloaded')


class myFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(myFrame, self).__init__(*args, **kw)
        panel = wx.Panel(self)
        gridsizr = wx.GridSizer(3,3,0,0)
        self.radiobutton1 = wx.RadioButton(panel, label='mp4')
        radiobutton2 = wx.RadioButton(panel, label='mp3')
        self.type = 'mp4'
        gridsizr.Add(self.radiobutton1, 0, wx.LEFT, 0)
        gridsizr.Add(wx.StaticText(panel, -1, 'Enter Link'), 0, wx.ALIGN_CENTER)
        gridsizr.Add(radiobutton2, 0, wx.ALIGN_RIGHT, 0)
        gridsizr.Add((0,0), 1, wx.EXPAND)
        self.txtctrl = wx.TextCtrl(panel, size=(200,30))
        gridsizr.Add(self.txtctrl,0, wx.ALIGN_CENTER)
        gridsizr.Add((0,0), 1, wx.EXPAND)
        gridsizr.Add((0,0), 1, wx.EXPAND)
        gridsizr.Add(wx.Button(panel, -1, 'Submit'), 0, wx.ALIGN_CENTER)
        panel.Bind(wx.EVT_BUTTON, self.YoutubeGetLink)
        panel.Bind(wx.EVT_RADIOBUTTON, self.mp)
        panel.SetSizerAndFit(gridsizr)

    def mp(self, event):
        if self.radiobutton1.GetValue():
            self.type = 'mp4'
        else:
            self.type = 'mp3'


    def YoutubeGetLink(self, event):
        ytthread(args=(self.txtctrl.GetValue(),self.type))

class myApp(wx.App):
    def OnInit(self):
        self.frame = myFrame(parent=None, title='pytube', size=(450, 135))
        self.frame.Show()
        return True


app = myApp()
app.MainLoop()