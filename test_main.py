from unittest import TestCase
from main import get_record, set_record
from pathlib import Path


class Test(TestCase):
    def test_get_record(self):
        Path('record').write_text('1234')
        temp = get_record()

        self.assertEqual(
            '1234', temp
        )

    def test_set_record(self):
        save = int(get_record())
        set_record(save + 1, save + 1)

        self.assertEqual(
            save + 1, int(get_record())
        )

        set_record(save, save)

        self.assertEqual(
            save, int(get_record())
        )
