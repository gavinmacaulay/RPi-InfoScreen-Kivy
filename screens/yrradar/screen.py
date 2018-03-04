from kivy.clock import Clock
from kivy.properties import (StringProperty, ObjectProperty)

from kivy.uix.screenmanager import Screen
from kivy.animation import Animation

class YrRadarMap(Screen):
    """Display a map of radar reflections from rain"""
    mapURL = StringProperty('')
    map = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        self.params = kwargs["params"]
        super(YrRadarMap, self).__init__(**kwargs)
        self.timer = None

    def on_enter(self):
        self.mapURL = self.params["mapURL"]
        self.timer = Clock.schedule_interval(self.update, self.params["updateInterval"])

    def on_leave(self):
        pass

    def update(self, *args):
        self.map.reload()

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            anim = Animation(pos=(0,0), duration=0.5)
            anim &= Animation(scale=1, duration=0.5)
            anim.start(self.layout)
        else:
            # we need to pass events on to children so that other things still work
            touch.push()
            touch.apply_transform_2d(self.to_local)    
            ret = super(YrRadarMap, self).on_touch_down(touch)
            touch.pop()
            return ret

