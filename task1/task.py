import pandas as pd
import sys

def get_cell_value(file_path, row, col):
    df = pd.read_csv(file_path, header=None)

    if row < 0 or row >= df.shape[0]:
        print(f"Строка {row} не валидна!")
        return
    if col < 0 or col >= df.shape[1]:
        print(f"Столбец {col} не валиден!")
        return

    cell_value = df.iloc[row, col]
    print(cell_value)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python task.py <file_path> <row> <col>")
        sys.exit(1)

    file_path = sys.argv[1]
    row = int(sys.argv[2])
    col = int(sys.argv[3])

    get_cell_value(file_path, row, col)