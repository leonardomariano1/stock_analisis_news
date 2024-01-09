# Stock Analysis and News Dashboard

This Python script creates a web-based dashboard using Dash, a framework for building interactive web applications. The dashboard provides a combination of financial news headlines and a candlestick chart for stock analysis. It leverages various libraries, including BeautifulSoup for web scraping, yfinance for fetching stock data, and Plotly for creating interactive charts.


https://github.com/leonardomariano1/stock_analisis_news/assets/143562678/66a52d57-fd40-4cb8-9651-455df78e01b5


## Prerequisites

Before running the script, make sure you have the following Python libraries installed:

- Dash
- requests
- bs4 (BeautifulSoup)
- yfinance
- plotly

You can install these libraries using the following command:

```bash
pip install dash requests beautifulsoup4 yfinance plotly
```

## Usage

1. Run the script:

    ```bash
    python script_name.py
    ```

2. Open a web browser and navigate to [http://127.0.0.1:8050/](http://127.0.0.1:8050/) to view the dashboard.

3. Use the dropdown menu to select a stock ticker (WEGE3, PETR4, or CEAB3) to see relevant financial news and a candlestick chart.

## Features

- **Financial News Section**: Scrapes financial news headlines related to the selected stock ticker from the Brazil Journal website. The headlines are displayed with links to the original articles.

- **Candlestick Chart**: Fetches historical stock data using yfinance and generates a candlestick chart with a 20-day Simple Moving Average (SMA) trend line. The chart provides insights into the stock's price movements over time.

- **Styling and User Interface**: The dashboard incorporates external stylesheets for an enhanced visual appearance. It features a light background color, subtle box shadows, and a rounded appearance for the dropdown menu, creating a clean and user-friendly interface.

## Dashboard Layout

- **Header**: Displays the title "Stock Analysis and News."

- **Dropdown Menu**: Allows users to select a stock ticker (WEGE3, PETR4, or CEAB3) from a dropdown list.

- **Candlestick Chart**: Shows the interactive candlestick chart with a trend line.

- **Financial News Journal Section**: Displays financial news headlines with a clean and readable design.

- **External Stylesheets**: Enhance the overall visual aesthetics of the dashboard, providing a professional and user-friendly experience.

## Customization

Feel free to customize the script or extend its functionality based on your specific requirements. You can modify the list of available stock tickers, change the external stylesheets, or add additional features to suit your needs. The modular structure of the script allows for easy expansion and customization.
