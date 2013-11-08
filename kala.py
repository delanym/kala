#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import wx
import data


class Kala(wx.App):
    def OnInit(self):
        self.frame = KalaFrame(None, title="Kala - Revised Astrology")
        self.SetTopWindow(self.frame)
        self.frame.SetWindowStyle(wx.MAXIMIZE)
        self.frame.Show()
        return True

class KalaFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=[0,0], size=[700,300], style=wx.DEFAULT_FRAME_STYLE, name="KalaFrame"):
        super(KalaFrame, self).__init__(parent, id, title, pos, size, style, name)
        
        icon = wx.Icon("./kala.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Event IDs
        self.ID_Exit = 0
        self.ID_NewPerson, self.ID_NewEvent = range(1,3)
        self.ID_Signs, self.ID_Nakshatras, self.ID_Animals, self.ID_Tithis = range(11,15)
        #self.ID_Private, self.ID_Public = 


        # Menus
        self.mfile = wx.Menu()
        self.mchronicle = wx.Menu()
        self.mview = wx.Menu()
        
        self.mfile.Append(self.ID_Exit, "Exit")
        self.mchronicle.Append(self.ID_NewPerson, "New Person")
        self.mchronicle.Append(self.ID_NewEvent, "New Event")
        self.mview.Append(self.ID_Signs, "Signs")
        self.mview.Append(self.ID_Nakshatras, "Nakshatras")
        self.mview.Append(self.ID_Animals, "Animals")
        self.mview.Append(self.ID_Tithis, "Tithis")

        menubar = wx.MenuBar()
        menubar.Append(self.mfile, "File")
        menubar.Append(self.mchronicle, "Chronicle")
        menubar.Append(self.mview, "View")
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_Exit)
        self.Bind(wx.EVT_MENU, self.onNewPerson, id=self.ID_NewPerson)
        self.Bind(wx.EVT_MENU, self.onNewEvent, id=self.ID_NewEvent)
        self.Bind(wx.EVT_MENU, self.onSigns, id=self.ID_Signs)
        self.Bind(wx.EVT_MENU, self.onNakshatras, id=self.ID_Nakshatras)
        self.Bind(wx.EVT_MENU, self.onAnimals, id=self.ID_Animals)
        self.Bind(wx.EVT_MENU, self.onTithis, id=self.ID_Tithis)

        # Layout
        self.CreateStatusBar()

    def onExit(self, event):
        self.Destroy()

    def onNewPerson(self, event):
        dlg = PersonDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    def onNewEvent(self, event):
        dlg = EventDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    def onSigns(self, event):
        pass

    def onNakshatras(self, event):
        pass

    def onAnimals(self, event):
        pass

    def onTithis(self, event):
        pass


class PersonDialog(wx.Dialog):
    def __init__(self, parent, title="Create New Person", style=wx.DEFAULT_DIALOG_STYLE):
        super(PersonDialog, self).__init__(parent, title=title)

        self.name = wx.TextCtrl(self)
        self.public = wx.RadioButton(self, label="Public", style=wx.RB_GROUP)
        self.private = wx.RadioButton(self, label="Private")
        self.url = wx.TextCtrl(self)
        self.getURL = wx.Button(self, label="Get Details")
        self.notes = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.addEvent = wx.Button(self, label="Add Event")
        self.accept = wx.Button(self, wx.ID_OK, "Accept")
        self.cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        sizer = wx.GridBagSizer(vgap=8, hgap=8)
        sizer.Add(wx.StaticText(self, label="Name"), (0, 1))
        sizer.Add(self.name, (0, 2), (1, 14), wx.EXPAND)

        sizer.Add(self.public, (1, 2), (1, 1))
        sizer.Add(self.private, (1, 3), (1, 1))
        sizer.Add(wx.StaticText(self, label="Astrodienst URL"), (2, 1))
        sizer.Add(self.url, (2, 2), (1, 12), wx.EXPAND)
        sizer.Add(self.getURL, (2, 14))

        sizer.Add(wx.StaticText(self, label="Notes"), (3, 1))
        sizer.Add(self.notes, (3, 2), (6, 14), wx.EXPAND)
        sizer.Add(self.addEvent, (9, 2))
        sizer.Add(self.accept, (9, 3))
        sizer.Add(self.cancel, (9, 4))

        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mvsizer.Add(sizer, 0, wx.GROW|wx.ALL, 10)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        self.name.SetFocus()

        self.Bind(wx.EVT_RADIOBUTTON, self.onPrivate, id=self.private.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.onPublic, id=self.public.GetId())
        self.Bind(wx.EVT_BUTTON, self.onAccept, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, parent.onNewEvent, id=self.addEvent.GetId())
        

    def onPrivate(self, event):
        self.url.Enable(False)
        self.getURL.Enable(False)

    def onPublic(self, event):
        self.url.Enable(True)
        self.getURL.Enable(True)

    def onAccept(self, event):
        self.Destroy()


class EventDialog(wx.Dialog):
    def __init__(self, parent, title="Create New Event", style=wx.DEFAULT_DIALOG_STYLE):
        super(EventDialog, self).__init__(parent, title=title)

        self.event = wx.ComboBox(self, choices=["Born", "Died", "Personal Event", "Historical Event", "Astronomical / Astrological"])
        self.event.SetStringSelection("Born")
        self.description = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.addPoint = wx.Button(self, label="Add Point")
        self.addRange = wx.Button(self, label="Add Range")
        self.timesNotebook = Times(self)

        # Layout
        msizer = wx.BoxSizer(wx.VERTICAL)
        
        gbsizer = wx.GridBagSizer(vgap=8, hgap=8)
        gbsizer.Add(wx.StaticText(self, label="Type"), (0, 1))
        gbsizer.Add(self.event, (0, 2), (1, 3))
        gbsizer.Add(wx.StaticText(self, label="Description"), (1, 1))
        gbsizer.Add(self.description, (1, 2), (4, 13), wx.EXPAND)
        gbsizer.Add(self.addPoint, (5, 2))
        gbsizer.Add(self.addRange, (5, 3))

        
        msizer.Add(gbsizer, 0, wx.GROW|wx.ALL, 10)
        msizer.Add(self.timesNotebook, 0, wx.GROW|wx.ALL, 10)
        self.SetSizer(msizer)
        msizer.Fit(self)
        self.description.SetFocus()


class Times(wx.Notebook):
    def __init__(self, parent):
        super(Times, self).__init__(parent)
        self.ptime = PointPanel(self)
        self.rtime = RangePanel(self)
        self.AddPage(self.ptime, "Point")
        self.AddPage(self.rtime, "Range")

class PointPanel(wx.Panel):
    def __init__(self, parent):
        super(PointPanel, self).__init__(parent)

        self.source = wx.TextCtrl(self, size=(300, 48), style=wx.TE_MULTILINE)
        self.calendar = wx.ComboBox(self, size=(150,-1), choices=["Julian", "Gregorian"])
        self.julianDayUT = wx.TextCtrl(self, size=(150,-1))
        self.method = wx.ComboBox(self, size=(150,-1), choices=["Local Mean", "Zone", "No location"])
        self.zone = wx.ComboBox(self, size=(75,-1), choices=data.ZONES)
        self.delta = wx.TextCtrl(self, size=(50,-1))
        self.longitude = wx.ComboBox(self, size=(150,-1), choices=["Decimal", "Degree"])
        self.longdecdeg = wx.TextCtrl(self, size=(50,-1))
        self.longmin = wx.TextCtrl(self, size=(50,-1))
        
        self.year = wx.TextCtrl(self, size=(50,-1))
        self.month = wx.TextCtrl(self, size=(50,-1))
        self.day = wx.TextCtrl(self, size=(50,-1))
        self.hour = wx.TextCtrl(self, size=(50,-1))
        self.minute = wx.TextCtrl(self, size=(50,-1))
        self.margin = wx.TextCtrl(self, size=(50,-1))

        self.calendar.SetStringSelection("Gregorian")
        self.method.SetStringSelection("Zone")
        self.delta.SetToolTipString = "Daylight saving is usually +1 and wartime +2."
        self.margin.SetToolTipString = "If you don't know the time enter 12. If you don't know the time or location enter 24."
        self.longdecdeg.SetToolTipString = "Negative value for western hemisphere."

        # Layout
        flags = wx.SizerFlags(1)
        flags.Expand().Border(wx.ALL, 2)
        
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(self, label="Source", size=(120,-1)), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
        hsizer.Add(self.source, wx.EXPAND)
        vsizer.AddF(hsizer, flags)
        
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(self, label="Calendar", size=(120,-1)), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
        hsizer.Add(self.calendar)
        hsizer.Add(self.julianDayUT)
        vsizer.AddF(hsizer, flags)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(self, label="Method", size=(120,-1)), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
        hsizer.Add(self.method)
        hsizer.Add(self.zone)
        hsizer.Add(wx.StaticText(self, label="Daylight"), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
        hsizer.Add(self.delta)
        vsizer.AddF(hsizer, flags)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(self, label="Longitude", size=(120,-1)), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
        hsizer.Add(self.longitude)
        hsizer.Add(wx.StaticText(self, label="Degree"), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
        hsizer.Add(self.longdecdeg)
        hsizer.Add(wx.StaticText(self, label="Minutes"), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
        hsizer.Add(self.longmin)
        vsizer.AddF(hsizer, flags)

        prsizer = wx.BoxSizer(wx.HORIZONTAL)
        gbsizer = wx.GridBagSizer(vgap=2, hgap=4)
        gbsizer.Add(wx.StaticText(self, label="Year"), (1, 1))
        gbsizer.Add(wx.StaticText(self, label="Month"), (1, 2))
        gbsizer.Add(wx.StaticText(self, label="Day"), (1, 3))
        gbsizer.Add(self.year, (2, 1), (1, 1))
        gbsizer.Add(self.month, (2, 2), (1, 1))
        gbsizer.Add(self.day, (2, 3), (1, 1))
        gbsizer.Add(wx.StaticText(self, label="Hour"), (3, 1))
        gbsizer.Add(wx.StaticText(self, label="Minute"), (3, 2))
        gbsizer.Add(wx.StaticText(self, label="Margin"), (3, 4))
        gbsizer.Add(self.hour, (4, 1), (1, 1))
        gbsizer.Add(self.minute, (4, 2), (1, 1))
        gbsizer.Add(self.margin, (4, 4), (1, 1))
        prsizer.Add(gbsizer)
        
        vsizer.AddF(hsizer, flags)
        
        #vsizer.Add(tsizer, 0, wx.GROW|wx.ALL, 10)
        self.SetSizer(vsizer)
        vsizer.Fit(self)


class RangePanel(wx.Panel):
    def __init__(self, parent):
        super(RangePanel, self).__init__(parent)

        self.calendar = wx.ComboBox(self, choices=["Julian", "Gregorian"])
        self.calendar.SetStringSelection("Gregorian")
        self.calibration = wx.ComboBox(self, choices=["Local Mean", "Zone"])
        self.calibration.SetStringSelection("Zone")
        self.source = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        self.year1 = wx.TextCtrl(self, size=(50,-1))
        self.month1 = wx.TextCtrl(self, size=(50,-1))
        self.day1 = wx.TextCtrl(self, size=(50,-1))
        self.hour1 = wx.TextCtrl(self, size=(50,-1))
        self.minute1 = wx.TextCtrl(self, size=(50,-1))
        self.delta1 = wx.TextCtrl(self, size=(50,-1))
        self.margin1 = wx.TextCtrl(self, size=(50,-1))

        self.year2 = wx.TextCtrl(self, size=(50,-1))
        self.month2 = wx.TextCtrl(self, size=(50,-1))
        self.day2 = wx.TextCtrl(self, size=(50,-1))
        self.hour2 = wx.TextCtrl(self, size=(50,-1))
        self.minute2 = wx.TextCtrl(self, size=(50,-1))
        self.delta2 = wx.TextCtrl(self, size=(50,-1))
        self.margin2 = wx.TextCtrl(self, size=(50,-1))


        tsizer = wx.BoxSizer(wx.VERTICAL)
        gbsizer = wx.GridBagSizer(vgap=8, hgap=8)
        gbsizer.Add(wx.StaticText(self, label="Calendar"), (0, 1))
        gbsizer.Add(self.calendar, (0, 2), (1, 3))
        gbsizer.Add(wx.StaticText(self, label="Calibration"), (1, 1))
        gbsizer.Add(self.calibration, (1, 2), (1, 3))
        gbsizer.Add(wx.StaticText(self, label="Source"), (2, 1))
        gbsizer.Add(self.source, (2, 2), (3, 15), wx.EXPAND)
        tsizer.Add(gbsizer)

        prsizer = wx.BoxSizer(wx.HORIZONTAL)
        gbsizer = wx.GridBagSizer(vgap=2, hgap=4)
        gbsizer.Add(wx.StaticText(self, label="Year"), (1, 1))
        gbsizer.Add(wx.StaticText(self, label="Month"), (1, 2))
        gbsizer.Add(wx.StaticText(self, label="Day"), (1, 3))
        gbsizer.Add(self.year1, (2, 1), (1, 1))
        gbsizer.Add(self.month1, (2, 2), (1, 1))
        gbsizer.Add(self.day1, (2, 3), (1, 1))
        gbsizer.Add(wx.StaticText(self, label="Hour"), (3, 1))
        gbsizer.Add(wx.StaticText(self, label="Minute"), (3, 2))
        gbsizer.Add(self.hour1, (4, 1), (1, 1))
        gbsizer.Add(self.minute1, (4, 2), (1, 1))
        gbsizer.Add(wx.StaticText(self, label="Delta"), (5, 1))
        gbsizer.Add(wx.StaticText(self, label="Margin"), (5, 2))
        gbsizer.Add(self.delta1, (6, 1), (1, 1))
        gbsizer.Add(self.margin1, (6, 2), (1, 1))
        prsizer.Add(gbsizer)

        gbsizer = wx.GridBagSizer(vgap=2, hgap=4)
        gbsizer.Add(wx.StaticText(self, label="Year"), (1, 1))
        gbsizer.Add(wx.StaticText(self, label="Month"), (1, 2))
        gbsizer.Add(wx.StaticText(self, label="Day"), (1, 3))
        gbsizer.Add(self.year2, (2, 1), (1, 1))
        gbsizer.Add(self.month2, (2, 2), (1, 1))
        gbsizer.Add(self.day2, (2, 3), (1, 1))
        gbsizer.Add(wx.StaticText(self, label="Hour"), (3, 1))
        gbsizer.Add(wx.StaticText(self, label="Minute"), (3, 2))
        gbsizer.Add(self.hour2, (4, 1), (1, 1))
        gbsizer.Add(self.minute2, (4, 2), (1, 1))
        gbsizer.Add(wx.StaticText(self, label="Delta"), (5, 1))
        gbsizer.Add(wx.StaticText(self, label="Margin"), (5, 2))
        gbsizer.Add(self.delta2, (6, 1), (1, 1))
        gbsizer.Add(self.margin2, (6, 2), (1, 1))
        prsizer.Add(gbsizer)

        tsizer.Add(prsizer)
        
        msizer = wx.BoxSizer(wx.VERTICAL)
        msizer.Add(tsizer, 0, wx.GROW|wx.ALL, 10)
        self.SetSizer(msizer)
        msizer.Fit(self)
        
if __name__ == "__main__":
    app = Kala(False)
    app.MainLoop()



