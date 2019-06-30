import pydbus

from timechart.core.settings import Settings

bus = pydbus.SessionBus()
shell = bus.get('org.gnome.Mutter.IdleMonitor', '/org/gnome/Mutter/IdleMonitor/Core')


def is_idle():
    return shell.GetIdletime() / 1000 > Settings().idle_time
