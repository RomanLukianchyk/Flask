from main_functions.CLI import main_cli
from pathlib import Path

if __name__ == "__main__":
    main_cli(files=Path("../data"), sort_order=None, driver_name=None)
