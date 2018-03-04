from kivy.clock import Clock
from kivy.properties import (StringProperty, ObjectProperty)

from kivy.uix.screenmanager import Screen

class YrGraphs(Screen):
    """Display two weather graphs from Yr.no"""
    graph1URL = StringProperty('')
    graph2URL = StringProperty('')
    graph1 = ObjectProperty(None)
    graph2 = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        self.params = kwargs["params"]
        super(YrGraphs, self).__init__(**kwargs)
        self.timer = None

    def on_enter(self):
        self.graph1URL = self.params["baseURL"] + '/' + self.params["location1Name"] + '/' + self.params["imageName"]
        self.graph2URL = self.params["baseURL"] + '/' + self.params["location2Name"] + '/' + self.params["imageName"]
        self.timer = Clock.schedule_interval(self.update, self.params["updateInterval"])

    def on_leave(self):
        #Clock.unschedule(self.timer)
        pass

    def update(self, *args):
        self.graph1.reload()
        self.graph2.reload()        

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            anim = Animation(pos=(0,0), duration=0.5)
            anim &= Animation(scale=1, duration=0.5)
            anim.start(self.layout)
        else:
            # we need to pass events on to children so that other things still work
            touch.push()
            touch.apply_transform_2d(self.to_local)
            ret = super(YrGraphs, self).on_touch_down(touch)
            touch.pop()
            return ret

