from timechart.util.util import set_auto_start, get_auto_start, is_snap
from timechart.views.base_view import BaseView
from timechart.views.components.check_box import TCheckBox


class SettingsView(BaseView):
    def __init__(self):
        BaseView.__init__(self)
        self.check_box = None
        self.auto_start = False

    def componentComplete(self):
        BaseView.componentComplete(self)
        self.check_box: TCheckBox = self.findChild(TCheckBox, "autostartCheckbox")
        self.check_box.on_checked = set_auto_start
        self.check_box.visible = is_snap()
        self.check_box.checked = get_auto_start()
