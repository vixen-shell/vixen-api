import threading
from .Gtk_imports import Gtk

class Gtk_main_loop:
    _thread = threading.Thread(target=Gtk.main)
    
    @staticmethod
    def run():
        Gtk_main_loop._thread.start()
        print('GTK:      Gtk main loop is started.')

    @staticmethod
    def quit():
        Gtk.main_quit()
        Gtk_main_loop._thread.join()
        print('GTK:      Gtk main loop is stopped.')