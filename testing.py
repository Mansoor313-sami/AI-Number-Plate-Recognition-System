import unittest

from helpers.yolo_model import load_model
from helpers.media_utils import process_image


class TestANPR(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.model, cls.classes = load_model()

    def test_plate_detection(self):

        result = process_image(
            "img/headimg.jpg",
            self.model,
            self.classes,
            "output"
        )

        self.assertIsNotNone(result)

    def test_result_type(self):

        result = process_image(
            "img/headimg.jpg",
            self.model,
            self.classes,
            "output"
        )

        self.assertTrue(isinstance(result, str))


if __name__ == "__main__":
    unittest.main()