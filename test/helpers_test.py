from rich import print
import sys
import os

# TODO: Clean this up


def add_project_root():
    # Ensure the project root is in sys.path
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.append(project_root)


def test_utils():
    # Lazy loading
    from bot.helpers.utils import Utils
    print(Utils.list_files("cogs"))

    COLOR_TEST_COUNT = 10
    colors = []
    for i in range(COLOR_TEST_COUNT):
        colors.append(Utils.get_random_color())
    print(colors)


def run_tests():
    add_project_root()
    test_utils()


if __name__ == '__main__':
    run_tests()
