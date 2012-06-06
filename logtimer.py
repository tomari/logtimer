#!/usr/bin/python
# Logging timer - 2012 H.Tomari. Public Domain.
# Confirmed to run on python 3.2.1 and python 2.7.2
# requires PyGObject GTK+-3 bindings
# -*- coding: utf-8 -*-
import signal
from datetime import datetime,timedelta
from gi.repository import Gtk,GObject
class LogTimer(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="LogTimer")
        #
        vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        self.mainlabel=Gtk.Label()
        vbox.pack_start(self.mainlabel,False,True,0)
        #
        ctrlbox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.startbutton=Gtk.ToggleButton("Start")
        self.startbutton.connect("toggled",self.startClicked)
        ctrlbox.pack_start(self.startbutton,True,True,0)
        self.resetbutton=Gtk.Button("Reset")
        self.resetbutton.connect("clicked",self.resetClicked)
        ctrlbox.pack_start(self.resetbutton,True,True,0)
        vbox.pack_start(ctrlbox,False,True,0)
        #
        logbox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        notelabel=Gtk.Label("Note")
        notelabel.set_justify(Gtk.Justification.RIGHT)
        logbox.pack_start(notelabel,False,False,0)
        self.noteentry=Gtk.Entry()
        self.noteentry.connect("activate",self.logClicked)
        logbox.pack_start(self.noteentry,True,True,0)
        self.notebutton=Gtk.Button("Log")
        self.notebutton.connect("clicked",self.logClicked)
        logbox.pack_start(self.notebutton,False,False,0)
        vbox.pack_start(logbox,False,True,0)
        #
        sw=self.create_logview()
        self.starttime=False
        self.logcounter=1
        vbox.pack_start(sw,True,True,0)
        self.update_mainlabel(False)
    def create_logview(self):
        scrolledWindow=Gtk.ScrolledWindow()
        scrolledWindow.set_hexpand(False)
        scrolledWindow.set_vexpand(True)
        self.logView=Gtk.TextView()
        self.logView.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        scrolledWindow.add(self.logView)
        return scrolledWindow
    def update_mainlabel(self,user_data):
        if self.starttime:
            rdelta=self.getdelta()
        else:
            rdelta=timedelta(seconds=0)
        self.mainlabel.set_markup('<span size="xx-large" weight="heavy">'+str(rdelta)+'</span>')
        return self.startbutton.get_active()
    def add_timeout(self):
        self.timeout_id=GObject.timeout_add(100,self.update_mainlabel,None)
    def startClicked(self,widget):
        if self.startbutton.get_active():
            if self.starttime:
                tnow=datetime.now()
                delta=tnow-self.stoptime
                self.starttime+=delta
            else:
                self.starttime=datetime.now()
            self.add_timeout()
        else:
            self.stoptime=datetime.now()
        return True
    def resetClicked(self,widget):
        self.starttime=False
        self.update_mainlabel(False)
        self.startbutton.set_active(False)
        self.logcounter=1
        return True
    def logClicked(self,widget):
        txt=self.noteentry.get_text()+"\n"
        if self.startbutton.get_active():
            ctrtxt='{0:3} '.format(self.logcounter)
            tnow=datetime.now()
            txt=ctrtxt+str(self.getdelta())+" "+txt
            self.logcounter=self.logcounter+1
        self.logView.get_buffer().insert_at_cursor(txt)
        itr=self.logView.get_buffer().get_end_iter()
        self.logView.scroll_to_iter(itr,0.0,False,True,True)
        self.noteentry.select_region(0,len(txt))
        return True
    def getdelta(self):
        timenow=datetime.now()
        delta=timenow-self.starttime
        rdelta=timedelta(days=delta.days, seconds=delta.seconds)
        return rdelta
#
signal.signal(signal.SIGINT,signal.SIG_DFL)
win=LogTimer()
win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()
