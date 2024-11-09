import pandas as pd
import numpy as np

def main():
    data = pd.read_csv('условная-энтропия-данные.csv', index_col='Возрастная группа').to_numpy()
    data = data/data.sum()

    # Энтропия совместного события
    entropy_general = - (data * np.log2(data)).sum()

    # Пусть событие A - возраст, B - категории
    probs_A = np.sum(data, axis = 1)
    probs_B = np.sum(data, axis = 0)

    entropy_A = - (probs_A * np.log2(probs_A)).sum()
    entropy_B = - (probs_B * np.log2(probs_B)).sum()

    entropy_B_when_A = entropy_general - entropy_B

    information_value = entropy_A - entropy_B_when_A

    return([round(entropy_general, 2),
            round(entropy_B, 2),
            round(entropy_A, 2),
            round(entropy_B_when_A, 2),
            round(information_value, 2)])

if __name__ == "__main__":
    print(main())