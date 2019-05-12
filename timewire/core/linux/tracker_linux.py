import logging

import psutil
import pydbus

from timewire.core.models.process import Process
from timewire.core.models.window import Window

bus = pydbus.SessionBus()
shell = bus.get('org.gnome.Shell', '/org/gnome/Shell')


def get_process_data() -> (Process, Window):
    path = None

    title_eval = shell.Eval("global.get_display().get_focus_window().title;")

    title = None

    if title_eval[0]:
        title = title_eval[1][1:-1]

    # TODO: if title == ...

    # wm = method("global.screen.get_display().get_focus_window().get_wm_class();")[1][1:-1]
    try:
        pid_eval = shell.Eval("global.get_display().get_focus_window().get_pid();")

        pid = None

        if pid_eval:
            pid = int(pid_eval[1])
    except ValueError as e:
        pid = None
        pass

    if pid == -1:
        path = shell.Eval("global.get_display().get_focus_window().get_gtk_application_object_path();")
        logging.debug(shell.Eval("global.get_display().get_focus_window().get_gtk_unique_bus_name();"))
        logging.debug(shell.Eval("global.get_display().get_focus_window().get_gtk_window_object_path();"))
        logging.debug(shell.Eval("global.get_display().get_focus_window().get_gtk_application_id();"))
        logging.debug(shell.Eval("global.get_display().get_focus_window().get_gtk_app_menu_object_path();"))
        logging.debug(shell.Eval("global.get_display().get_focus_window().get_gtk_menubar_object_path();"))
    elif pid in psutil.pids():
        path = psutil.Process(pid).exe()

    return Process(path), Window(title)
