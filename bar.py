from tidal import *
import wifi
import urequests
import ujson
from app import TextApp

class ClubMateApp(TextApp):
    TITLE = "Club Mate Level"
    BG = BLACK
    FG = color565(0xF0, 0xF0, 0xF0)

    def attempt_wifi(self):
        tries = 5
        
        while tries > 0:
            tries -= 1
            if not wifi.status():
                self.window.println("Connecting WiFi")
                wifi.connect()
                wifi.wait(5*1000)
            if not wifi.status():
                self.window.println("WiFi fail, retrying")
        self.window.println("WiFi fail, gave up")

    def update(self):
        self.attempt_wifi()
        if wifi.status():
            self.window.println("Getting latest CM status")
            dept_uri = 'https://bar.emf.camp/api/department/75.json'
            resp = urequests.get(dept_uri).json()
            wifi.disconnect()
            items = {}
            for item in resp['stocktypes']:
                items[item['fullname']] = item
            self.window.cls()
            self.window.println(f"There are {items['Club Mate Regular 500ml']['base_units_remaining']}")
            self.window.println("bottles of CM left")
            self.window.println(f"There are {items['Club Mate Granat 500ml']['base_units_remaining']}")
            self.window.println("bottles of Granat")

    def on_activate(self):
        super().on_activate()
        self.timer = self.after(900000, self.update)
        self.update()

main = ClubMateApp
