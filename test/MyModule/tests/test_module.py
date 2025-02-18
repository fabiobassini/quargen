import unittest
from MyModule import api_module, ui_module

class TestMymodule(unittest.TestCase):
    def test_api_status(self):
        mod = api_module.initialize_api({})
        self.assertIsNotNone(mod.get_blueprint())

    def test_ui_home(self):
        mod = ui_module.initialize_ui({})
        self.assertIsNotNone(mod.get_blueprint())

if __name__ == '__main__':
    unittest.main()
