#! /usr/bin/env python
import gtk
import gobject
import os
import os.path
from string import rstrip
import sys

INTERVAL = 20000
BATT_FULL = "/sys/class/power_supply/BAT1/charge_full"
BATT_NOW = "/sys/class/power_supply/BAT1/charge_now"
BATT_STATE = "/sys/class/power_supply/BAT1/status"
IMAGE_LOC = os.path.join(os.path.dirname(sys.argv[0]), "images/battery")


class BatteryTray:
    def __init__(self):
        self.tray = gtk.StatusIcon()
        self.tray.connect('activate', self.refresh)

        # Create menu
        menu = gtk.Menu()
        i = gtk.MenuItem("About...")
        i.show()
        i.connect("activate", self.show_about)
        menu.append(i)
        i = gtk.MenuItem("Quit")
        i.show()
        i.connect("activate", self.quit)
        menu.append(i)
        self.tray.connect('popup-menu', self.show_menu, menu)

        # Initalise and start battery display
        self.refresh(None)
        self.tray.set_visible(True)
        gobject.timeout_add(INTERVAL, self.refresh, False)

    def show_menu(self, widget, event_button, event_time, menu):
        menu.popup(None, None,
            gtk.status_icon_position_menu,
            event_button,
            event_time,
            self.tray
        )

    def show_about(self, widget):
        dialog = gtk.MessageDialog(
            None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO,
            gtk.BUTTONS_OK,
            """
It's a battery meter
By Jamie Lentin
""")
        dialog.run()
        dialog.destroy()

    def quit(self, widget):
        gtk.main_quit()

    def refresh(self, widget):
        def slurp(filename):
            f = open(filename)
            return f.read()

        b_level = int(round(float(slurp(BATT_NOW)) / float(slurp(BATT_FULL)) * 100))
        b_file = IMAGE_LOC + "." + str(b_level / 10) + ".png"
        self.tray.set_tooltip(
            "%s: %d%%" %
            (rstrip(slurp(BATT_STATE)), b_level)
        )
        if os.path.exists(b_file):
            self.tray.set_from_file(b_file)
        self.tray.set_blinking(b_level <= 5)
        return True

###############################################################################
if __name__ == '__main__':
    app = BatteryTray()
    gtk.main()
