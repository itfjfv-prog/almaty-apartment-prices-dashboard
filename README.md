# Almaty Apartment Prices: Data Cleaning and Dashboard

A small data project: cleaning a public real estate dataset and turning it into an interactive dashboard that shows what drives apartment prices in Almaty.

**Live dashboard:**https://claude.ai/artifact/Cvx5gXEFseVtmuvFVUc1UA

## What the dashboard shows

- Median price, median price per m², median area and number of listings
- Median price per m² by district, number of rooms, construction period and floor
- A district filter: pick a district in the list or click a bar, and every card updates

## Key findings

All figures are medians of price per m² after cleaning (currency assumed to be tenge, see notes below).

- **District matters most.** The most expensive district code is about 1.6 times more expensive per m² than the cheapest (about 871,000 vs 535,000).
- **Rooms barely change the price per m².** One-, two- and three-room apartments are all around 660,000. Total price grows mainly because the area grows.
- **First floors are cheaper.** Floor 1 is roughly 7% cheaper per m² than floors 2 to 5, and floors 11 and above are the most expensive group.
- **Construction year is a weak signal.** Buildings from 2015 or later are only slightly more expensive per m² than those built before 1970.

## Data

- Source: "Apartments in Almaty" by Altemir Omar on Kaggle, MIT licence. https://www.kaggle.com/datasets/altemiromar/apartments-in-almaty/data
- The raw file has 11,883 rows and 9 columns, with no missing values.
- Districts, building type and quality are stored as numeric codes with no legend, so districts appear as codes and building type and quality are not used.
- The source does not state a currency. The values are consistent with Kazakhstani tenge (KZT), which is an assumption.
- The data is a one-time snapshot and is not updated.

## Cleaning (`clean_data.py`)

| Step | Rows left |
| --- | --- |
| Raw file | 11,883 |
| Remove duplicate listings | 11,248 |
| Keep area between 12 and 300 m² | 11,186 |
| Keep floors up to 40 | 11,185 |
| Keep price per m² between 150,000 and 2,500,000 | 11,172 |

The script also adds `price_per_m2` and a construction-period column. Medians are used instead of averages because a few luxury listings would pull averages up.

## Run the cleaning script

1. Download `almaty_apartments_with_id.csv` from the Kaggle page and put it next to the script.
2. Install pandas: `pip install pandas`
3. Run: `python clean_data.py`

It creates `almaty_apartments_clean.csv` and prints how many rows each step removed.

## Tech

Python, pandas, interactive dashboard.
