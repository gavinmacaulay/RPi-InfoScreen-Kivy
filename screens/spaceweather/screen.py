from kivy.clock import Clock
from kivy.properties import (StringProperty, ObjectProperty)

from kivy.uix.screenmanager import Screen
from kivy.animation import Animation

#from threading import thread
#from subprocess import Popen
#import shlex

class SpaceWeatherMap(Screen):
    """Display a map of predicted auroral activity"""
    mapURL = StringProperty('')
    map = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        self.params = kwargs["params"]
        super(SpaceWeatherMap, self).__init__(**kwargs)
        self.timer = None

    def on_enter(self):
        self.mapURL = self.params["mapURL"]
        self.timer = Clock.schedule_interval(self.update, self.params["updateInterval"])

        #self.t = TimeoutProcess("python generate_aurora_map.py", 120)
        #self.t.runProcess()
        #self.timer = Clock.schedule_interval(self.update, 1)

    def on_leave(self):
        #Clock.unschedule(self.timer)
        pass

    def update(self, *args):
        self.map.reload()
	#if self.t.isRunning:
        #    pass
        #else:
        #    
        #    self.map.reload()        

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            anim = Animation(pos=(0,0), duration=0.5)
            anim &= Animation(scale=1, duration=0.5)
            anim.start(self.layout)
        else:
            # we need to pass events on to children so that other things still work
            touch.push()
            touch.apply_transform_2d(self.to_local)    
            ret = super(SpaceWeatherMap, self).on_touch_down(touch)
            touch.pop()
            return ret

#class TimeoutProcess(Thread):
#    """Class that calls a subprocess but terminates it if the process has
#       not completed within the necessary time period.
#
#       Takes two parameters:
#         process: (string) command to be run
#         timeout: (int) number of seconds until process is killed
#    """
#
#    def __init__(self, process, timeout):
#        Thread.__init__(self)
#        # We use shlex.split to turn the command into something that the
#        # subprocess module likes to use
#        self.process = shlex.split(process)
#
#        # Make sure the timeout is an integer
#        self.timeout = int(timeout)
#
#    def runProcess(self):
#        # Create an object that runs the process
#        self.proc = Popen(self.process)
#
#        # Set a flag to show the process is running
#        self.running = True
#
#    def isRunning(self):
#        # We'll check the status of the process every second
#        if self.proc.poll() is not None:
#            self.running = False
#        return self.running
#
#    def junk():
#        # The loop's exited so we've either reached the timeout period
#        # or the process has already finished.
#        # Have a look at the flag to see which is true
#        if running:
#
#            # Process is still running so let's kill it
#            self.proc.terminate()
#
#            #print "Process killed"
