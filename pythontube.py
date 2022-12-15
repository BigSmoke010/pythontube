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
        self.yt(self._args[0], self._args[1])


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
        boxsizr = wx.BoxSizer(wx.VERTICAL)
        gridsizr = wx.GridSizer(1,2,0,0)
        self.radiobutton1 = wx.RadioButton(panel, label='mp4')
        self.radiobutton2 = wx.RadioButton(panel, label='mp3')
        self.type = 'mp4'
        gridsizr.Add(self.radiobutton1, 0, wx.ALIGN_LEFT, 0)
        gridsizr.Add(self.radiobutton2, 0, wx.ALIGN_RIGHT, 0)
        boxsizr.Add(gridsizr, 0, wx.EXPAND)
        boxsizr.Add(wx.StaticText(panel, -1, 'Enter Link'), 0, wx.ALIGN_CENTER)
        self.txtctrl = wx.TextCtrl(panel, size=(200,30))
        boxsizr.Add(self.txtctrl,0, wx.ALIGN_CENTER)
        boxsizr.Add(wx.Button(panel, -1, 'Submit'), 0, wx.ALIGN_CENTER)
        panel.Bind(wx.EVT_BUTTON, self.YoutubeGetLink)
        panel.Bind(wx.EVT_RADIOBUTTON, self.mp)
        panel.SetSizerAndFit(boxsizr)

    def mp(self, event):
        if self.radiobutton1.GetValue():
            self.type = 'mp4'
        else:
            self.type = 'mp3'


    def YoutubeGetLink(self, event):
        ytthread(args=(self.txtctrl.GetValue(),self.type))

class myApp(wx.App):
    def OnInit(self):
        self.frame = myFrame(parent=None, title='pytube', size=(400,150))
        self.frame.Show()
        return True


app = myApp()
app.MainLoop()