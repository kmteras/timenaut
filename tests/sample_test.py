from tests.main_window_test import MainWindowTest


class SampleTest(MainWindowTest):
    def test(self):
        self.assertEqual(self.main_window.applicationName(), "Timewire")
