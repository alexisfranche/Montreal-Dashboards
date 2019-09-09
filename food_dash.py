import pandas as pd


def main():
    df = pd.read_excel("inspection-aliments-contrevenants.xlsx")

    print(df.head(20))


if __name__ == '__main__':
    main()