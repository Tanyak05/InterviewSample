from unittest import TestCase

from api.app import spectrum


class Test(TestCase):
    def test_spectrum(self):
        result = spectrum();
        self.assertEqual(1123, result)
