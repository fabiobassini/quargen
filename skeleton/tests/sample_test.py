"""
Test di esempio per SampleModel.
"""

import unittest
from models.domain.sample_model import SampleModel

class TestSampleModel(unittest.TestCase):
    def test_process(self):
        model = SampleModel("dati di test")
        self.assertIn("dati di test", model.process())

if __name__ == '__main__':
    unittest.main()
