from rich import print
import sys
import os


def add_project_root():
    # Ensure the project root is in sys.path
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.append(project_root)


def test_file_listing():
    # Lazy loading
    from bot.helpers.utils import Utils
    print(Utils.list_files("cogs"))


def run_tests():
    add_project_root()
    test_file_listing()


if __name__ == '__main__':
    run_tests()
