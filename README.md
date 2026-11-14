# Largest Banks ETL Pipeline

An ETL pipeline that scrapes the list of the world's largest banks by market
capitalization, converts the values into multiple currencies, and loads the
results into CSV and SQLite.

> Guided project based on the IBM Data Engineering course structure. I wrote
> and tested the code myself and extended it with [add your extension here].

## Pipeline

1. **Extract**: scrapes the table from an archived Wikipedia page
   (requests + BeautifulSoup). An archived URL is used so results are
   reproducible.
2. **Transform**: converts market cap from USD to GBP, EUR and INR using
   rates in `exchange_rate.csv` (static sample rates, not live data).
3. **Load**: saves the result to `Largest_banks_data.csv` and to a SQLite
   table in `Banks.db`.
4. **Query**: runs SQL queries on the loaded table.
5. **Log**: every stage is timestamped in `code_log.txt`.

## Project structure

- `bank_project.py`: the full pipeline
- `exchange_rate.csv`: currency rates
- `requirements.txt`: dependencies

## How to run

pip install -r requirements.txt
python bank_project.py

## Sample output

Top 5 banks by market cap (USD billions):

| Bank | MC_USD_Billion |
|---|---|
| JPMorgan Chase | 432.92 |
| Bank of America | 231.52 |
| Industrial and Commercial Bank of China | 194.56 |
| Agricultural Bank of China | 160.68 |
| HDFC Bank | 157.91 |

Average market cap: 151.987 billion GBP across the 10 banks.
<img width="1042" height="357" alt="image" src="https://github.com/user-attachments/assets/5f1a993a-425d-43e7-be4d-09609c171ad7" />
<img width="1055" height="600" alt="image" src="https://github.com/user-attachments/assets/39ffffc3-f231-4984-8372-d846f8decba5" />

## Future improvements

- Schedule the pipeline with Airflow
- Add data validation checks and error logging
- Fetch live exchange rates from an API
- Build the DataFrame from a list instead of concatenating in a loop
