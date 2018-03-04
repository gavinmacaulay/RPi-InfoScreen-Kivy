from datetime import datetime

from kivy.properties import DictProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from os import system

class ClockShutdownScreen(Screen):
    """Simple plugin screen to show digital clock of current time."""
    # String Property to hold time
    timedata = DictProperty(None)
    btn_text = StringProperty('Shutdown')

    def __init__(self, **kwargs):
        self.get_time()
        super(ClockShutdownScreen, self).__init__(**kwargs)
        self.timer = None

    def get_time(self):
        """Sets self.timedata to current time."""
        n = datetime.now()
        self.timedata["h"] = n.hour
        self.timedata["m"] = n.minute
        self.timedata["s"] = n.second

    def update(self, dt):
        self.get_time()

    def on_enter(self):
        # We only need to update the clock every second.
        self.timer = Clock.schedule_interval(self.update, 1)

    def on_pre_enter(self):
        self.get_time()

    def on_pre_leave(self):
        # Save resource by unscheduling the updates.
        Clock.unschedule(self.timer)

    def shut_down(self):
        self.btn_text = 'Shutting down in 5 seconds...'
        Clock.schedule_once(self.do_shut_down, 5)

    def do_shut_down(self, dt):
        os.system('sudo shutdown -h now')
