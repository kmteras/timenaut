from typing import Dict

import psutil
import pydbus
import logging

bus = pydbus.SessionBus()
shell = bus.get('org.gnome.Shell', '/org/gnome/Shell')


def get_process_data() -> Dict:
    data = {
        'path': None,
        'title': None
    }

    title = shell.Eval("global.screen.get_display().get_focus_window().title;")[1][1:-1]

    # TODO: if title == ...

    data['title'] = title
    # wm = method("global.screen.get_display().get_focus_window().get_wm_class();")[1][1:-1]
    try:
        pid = int(shell.Eval("global.screen.get_display().get_focus_window().get_pid();")[1])
    except ValueError as e:
        pid = None
        pass

    if pid == -1:
        data['path'] = shell.Eval("global.screen.get_display().get_focus_window().get_gtk_application_object_path();")
        logging.debug(shell.Eval("global.screen.get_display().get_focus_window().get_gtk_unique_bus_name();"))
        logging.debug(shell.Eval("global.screen.get_display().get_focus_window().get_gtk_window_object_path();"))
        logging.debug(shell.Eval("global.screen.get_display().get_focus_window().get_gtk_application_id();"))
        logging.debug(shell.Eval("global.screen.get_display().get_focus_window().get_gtk_app_menu_object_path();"))
        logging.debug(shell.Eval("global.screen.get_display().get_focus_window().get_gtk_menubar_object_path();"))
    elif pid in psutil.pids():
        data['path'] = psutil.Process(pid).exe()

    return data
