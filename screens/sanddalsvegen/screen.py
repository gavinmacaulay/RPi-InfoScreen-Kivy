from datetime import datetime
import pytz
import tzlocal

from re import sub
from time import sleep
import requests

from kivy.clock import Clock
from kivy.properties import StringProperty

from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

class SanddalsvegenTemperatures(Screen):
    """Display the temperatures measured around Sanddalsvegen 31."""
    outsideTemp = StringProperty('')
    compostTemp = StringProperty('')
    otherTemp = StringProperty('')
    timestamp = StringProperty('')
    degreeSym = u'\N{degree sign}C'

    def __init__(self, **kwargs):
        super(SanddalsvegenTemperatures, self).__init__(**kwargs)
        self.timer = None
        self.outsideTemp = 'Getting temperatures...'

    def on_enter(self):
        self.timer = Clock.schedule_interval(self.update, 120)
        self.update()

    def on_leave(self):
        Clock.unschedule(self.timer)

    def update(self, *args):
        try:
            t = requests.get('http://192.168.20.15/~pi/query_service.php').json()
        except ValueError:
            # We just try again a short time later
            sleep(0.1)
            t = requests.get('http://192.168.20.15/~pi/query_service.php').json()
        except requests.exceptions.ConnectionError:
            self.outsideTemp = 'Connection error!'
            t = list()

        self.compostTemp = ''
        self.otherTemp = ''

        for m in t:
            print(m)

            if m['value'] is None:
                value_str = ''
            else:
                value_str = '{:.1f}'.format(m['value'])

            if m['name'] == 'OutsideAir':
                self.outsideTemp = value_str + self.degreeSym
		if m['value'] is not None:
                    if m['value'] <= -10:
		        self.outsideTemp += ', Arctic!!!'
                    elif m['value'] <= -5:
                        self.outsideTemp += ', brrrr.....'
            elif m['name'] == 'CpuTemp':
                pass
            elif m['name'].startswith('Compost'):
                name = sub(r'([A-Z])', r' \1', str(m['name'])).split() # split on capital letters
                name = [word.lower() for word in name] # make all lower case
                name[0] = name[0].capitalize() # capitalise the first word

                self.compostTemp =  self.compostTemp + '\n' + ' '.join(name) + ': ' + value_str + ' ' + self.degreeSym
            else:
                self.otherTemp = self.otherTemp + '\n' + str(m['name']) + ': ' + value_str + ' ' + self.degreeSym

        if len(t) > 0:
            # The time is UTC, and we want it in local time
            local_timezone = tzlocal.get_localzone()
            utc_time = datetime.strptime(t[0]['time'], "%Y-%m-%d %H:%M:%S")
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
            self.timestamp = 'Updated ' + local_time.strftime('%a %b %d %H:%M:%S')

        

