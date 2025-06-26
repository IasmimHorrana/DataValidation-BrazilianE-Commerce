from src.extract import ler_csv_customers
from src.transform import transformar_customers


def main():
    df = ler_csv_customers("data/olist_customers_dataset.csv")
    df_limpo = transformar_customers(df)

    print(df_limpo.head())


if __name__ == "__main__":
    main()
