import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from bot.helpers.utils import Utils  # Updated import statement


class TestUtils(unittest.TestCase):

    # Mock Path to control the file system interactions
    @patch('bot.helpers.utils.Path')
    @patch('bot.helpers.utils.logging.error')
    def test_list_files(self, mock_logging, mock_path):
        # Setup mock
        mock_file1 = MagicMock(is_file=MagicMock(return_value=True))
        mock_file1.name = 'file1.txt'
        mock_file2 = MagicMock(is_file=MagicMock(return_value=True))
        mock_file2.name = 'file2.txt'
        mock_path.return_value.iterdir.return_value = [mock_file1, mock_file2]

        # Test valid directory
        self.assertEqual(Utils.list_files('some_directory'),
                         ['file1.txt', 'file2.txt'])

        # Test directory not found
        mock_path.side_effect = FileNotFoundError
        self.assertEqual(Utils.list_files('invalid_directory'), [])
        mock_logging.assert_called_once_with(
            'The directory "invalid_directory" does not exist.')

    @patch('bot.helpers.utils.Path')
    def test_get_bot_dir_path(self, mock_path):
        # Setup mock
        mock_path.resolve.return_value = mock_path
        mock_path.name = 'bot'
        mock_path.parent = Path('/path/to')
        self.assertEqual(Utils.get_bot_dir_path(), '/path/to/bot')

    def test_format_num(self):
        self.assertEqual(Utils.format_num(1000), '1,000')
        self.assertEqual(Utils.format_num(1000000), '1,000,000')
        self.assertEqual(Utils.format_num(999), '999')
        self.assertEqual(Utils.format_num(0), '0')
        self.assertEqual(Utils.format_num(123456789.123), '123,456,789.123')

    def test_get_color(self):
        self.assertEqual(Utils.get_color('red'), 0xFF0000)
        self.assertEqual(Utils.get_color('nonexistent_color'),
                         0x800080)  # Default color is purple
        self.assertEqual(Utils.get_color('pink'), 0xFFC0CB)

    @patch('bot.helpers.utils.random.randint')
    def test_get_random_color(self, mock_randint):
        mock_randint.return_value = 2  # Index for 'yellow'
        self.assertEqual(Utils.get_random_color(), 0xFFFF00)


if __name__ == '__main__':
    unittest.main()
