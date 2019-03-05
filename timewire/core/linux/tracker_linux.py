import logging

import psutil
import pydbus

from timewire.core.models.process import Process
from timewire.core.models.window import Window

bus = pydbus.SessionBus()
shell = bus.get('org.gnome.Shell', '/org/gnome/Shell')


def get_process_data() -> (Process, Window):
    path = None

    title = shell.Eval("global.screen.get_display().get_focus_window().title;")[1][1:-1]

    # TODO: if title == ...

    # wm = method("global.screen.get_display().get_focus_window().get_wm_class();")[1][1:-1]
    try:
        pid = int(shell.Eval("global.screen.get_display().get_focus_window().get_pid();")[1])
    except ValueError as e:
        pid = None
        pass

    if pid == -1:
        path = shell.Eval("global.screen.get_display().get_focus_window().get_gtk_application_object_path();")
        logging.debug(shell.Eval("global.screen.get_display().get_focus_window().get_gtk_unique_bus_name();"))
        logging.debug(shell.Eval("global.screen.get_display().get_focus_window().get_gtk_window_object_path();"))
        logging.debug(shell.Eval("global.screen.get_display().get_focus_window().get_gtk_application_id();"))
        logging.debug(shell.Eval("global.screen.get_display().get_focus_window().get_gtk_app_menu_object_path();"))
        logging.debug(shell.Eval("global.screen.get_display().get_focus_window().get_gtk_menubar_object_path();"))
    elif pid in psutil.pids():
        path = psutil.Process(pid).exe()

    return Process(path), Window(title)
