from pathlib import Path
import pandas as pd


def split_csv_file():
    """This will split the original `creditcard.csv` file in two"""

    # get file path
    data_folder = (Path(__file__).parent / "../resources/data").resolve()
    file_path = (data_folder / "creditcard.csv").resolve()

    # read csv file
    print(f"reading file: {file_path.as_posix()}")
    df = pd.read_csv(file_path.as_posix())

    # split the file in two
    output_file1 = (data_folder / "creditcard_part1.csv").resolve()
    output_file2 = (data_folder / "creditcard_part2.csv").resolve()

    print(f"writing file: {output_file1.as_posix()}")
    df[: len(df) // 2].to_csv(output_file1.as_posix(), index=False)

    print(f"writing file: {output_file2.as_posix()}")
    df[len(df) // 2 :].to_csv(output_file2.as_posix(), index=False)


if __name__ == "__main__":
    split_csv_file()