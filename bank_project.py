import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3

# ------------------- Variables -------------------

url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"

csv_path = "Largest_banks_data.csv"
db_name = "Banks.db"
table_name = "Largest_banks"

# ------------------- Logging -------------------

def log_progress(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("code_log.txt", "a") as f:
        f.write(f"{timestamp} : {message}\n")

# ------------------- Extract -------------------

def extract(url):

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    html_page = response.text

    soup = BeautifulSoup(html_page, "html.parser")

    df = pd.DataFrame(columns=["Name", "MC_USD_Billion"])

    tables = soup.find_all("tbody")
    rows = tables[0].find_all("tr")

    for row in rows:

        cols = row.find_all("td")

        if len(cols) == 0:
            continue

        bank_name = cols[1].text.strip()
        market_cap = float(cols[2].text.strip())

        data = {
            "Name": bank_name,
            "MC_USD_Billion": market_cap
        }

        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    return df

# ------------------- Transform -------------------

def transform(df):

    exchange_df = pd.read_csv("exchange_rate.csv")

    exchange_rate = exchange_df.set_index("Currency").to_dict()["Rate"]

    gbp_rate = float(exchange_rate["GBP"])
    eur_rate = float(exchange_rate["EUR"])
    inr_rate = float(exchange_rate["INR"])

    df["MC_GBP_Billion"] = [
        np.round(x * gbp_rate, 2)
        for x in df["MC_USD_Billion"]
    ]

    df["MC_EUR_Billion"] = [
        np.round(x * eur_rate, 2)
        for x in df["MC_USD_Billion"]
    ]

    df["MC_INR_Billion"] = [
        np.round(x * inr_rate, 2)
        for x in df["MC_USD_Billion"]
    ]

    return df

# ------------------- CSV -------------------

def load_to_csv(df, csv_path):

    df.to_csv(csv_path, index=False)

# ------------------- Database -------------------

def load_to_db(df, sql_connection, table_name):

    df.to_sql(table_name, sql_connection,
              if_exists="replace",
              index=False)

# ------------------- Queries -------------------

def run_query(query_statement, sql_connection):

    print("\nQuery:")
    print(query_statement)

    output = pd.read_sql(query_statement, sql_connection)

    print(output)

# ------------------- Main Program -------------------

def main():

    log_progress("Preliminaries complete. Initiating ETL process")

    df = extract(url)

    log_progress("Data extraction complete. Initiating Transformation process")

    df = transform(df)

    print(df)

    log_progress("Data transformation complete. Initiating Loading process")

    load_to_csv(df, csv_path)

    log_progress("Data saved to CSV file")

    connection = sqlite3.connect(db_name)

    log_progress("SQL Connection initiated")

    load_to_db(df, connection, table_name)

    log_progress("Data loaded to Database as a table, Executing queries")

    run_query("SELECT * FROM Largest_banks", connection)

    run_query("SELECT AVG(MC_GBP_Billion) FROM Largest_banks", connection)

    run_query("SELECT Name FROM Largest_banks ORDER BY MC_USD_Billion DESC LIMIT 5", connection)

    log_progress("Process Complete")

    connection.close()

    log_progress("Server Connection closed")


if __name__ == "__main__":
    main()