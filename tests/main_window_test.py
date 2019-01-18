from unittest import TestCase

from timewire.views.main_window import MainWindow


class MainWindowTest(TestCase):
    def setUp(self):
        super(MainWindowTest, self).setUp()
        self.main_window = MainWindow()

    def tearDown(self):
        super(MainWindowTest, self).tearDown()
        del self.main_window
