import dash
from dash import html, dcc, Output, Input
import requests
from bs4 import BeautifulSoup
import yfinance as yf
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# Function to scrape news based on the selected ticker
def scrape_news(ticker):
    # Define mappings for tickers to their corresponding companies
    ticker_mappings = {'CEAB3': 'C&A', 'WEGE3': 'WEG', 'PETR4': 'Petrobras'}

    # Validate the provided ticker
    if ticker not in ticker_mappings:
        return [f"Invalid ticker: {ticker}"]

    # Construct the URL based on the selected ticker
    company_name = ticker_mappings[ticker]
    url = f'https://braziljournal.com/?s={company_name.lower()}'

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Assuming the news headlines are contained within elements with class '.boxarticle-infos-title'
        headlines = soup.find_all('h2', class_='boxarticle-infos-title')

        # Extract the links to the original site
        links = [headline.find('a')['href'] for headline in headlines]

        # Extract the text content from the headlines
        news_list = [headline.text.strip() for headline in headlines]

        # Combine news and links into a list of tuples
        news_with_links = list(zip(news_list, links))

        return news_with_links
    else:
        return [f"Failed to fetch news. Status code: {response.status_code}"]

# Function to fetch stock data
def fetch_stock_data(ticker, interval='1d', years_back=1):
    end_date = datetime.today().strftime('%Y-%m-%d')  # Set end_date to the current date
    start_date = (datetime.today() - timedelta(days=365 * years_back)).strftime('%Y-%m-%d')

    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        print(stock_data.head())  # Print the first few rows of the data for debugging
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Function to create candlestick chart with trend lines
def create_candlestick_chart(stock_data):
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, shared_yaxes=False)

    # Candlestick trace
    candlestick = go.Candlestick(x=stock_data.index,
                                 open=stock_data['Open'],
                                 high=stock_data['High'],
                                 low=stock_data['Low'],
                                 close=stock_data['Close'],
                                 name='Candlestick')

    # Add candlestick trace
    fig.add_trace(candlestick)

    # Calculate Simple Moving Average (SMA) for trend line
    stock_data['SMA'] = stock_data['Close'].rolling(window=20).mean()

    # Trend line trace
    trend_line = go.Scatter(x=stock_data.index, y=stock_data['SMA'],
                            mode='lines', name='Trend Line', line=dict(color='orange'))

    # Add trend line trace
    fig.add_trace(trend_line)

    fig.update_layout(xaxis_rangeslider_visible=False,
                      title='Stock Price Candlestick Chart with Trend Line',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      margin=dict(l=0, r=0, t=50, b=0),
                      template='plotly_white')

    return fig

# Dash app initialization with external stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Callback to update news headlines and candlestick chart based on selected ticker
@app.callback(
    [Output('news-headlines', 'children'),
     Output('candlestick-chart', 'figure')],
    [Input('ticker-dropdown', 'value')]
)
def update_content(selected_ticker):
    news_list_with_links = scrape_news(selected_ticker)

    # Create a list of HTML list items to display only the first three news headlines with links
    news_items = [html.Div([
        html.A(news, href=link, target='_blank', style={
            'textDecoration': 'none',
            'fontWeight': 'bold',
            'color': '#1F77B4',  # Blue color
            'fontSize': '18px',
            'transition': 'color 0.3s ease-in-out',
            'margin-bottom': '10px',
            'display': 'block'
        }),
    ]) for news, link in news_list_with_links[:10]]  # Display the first 10 news items

    # Fetch stock data
    stock_data = fetch_stock_data(selected_ticker + '.SA')  # Append '.SA' for stock data

    if stock_data is not None:
        candlestick_chart = create_candlestick_chart(stock_data)
    else:
        candlestick_chart = go.Figure()

    return news_items, candlestick_chart

# Layout of the dashboard with additional styling
app.layout = html.Div([
    html.Header(html.H1("Stock Analysis and News", className='text-center text-primary mb-4'), id='header', className='bg-light py-4'),

    html.Div([
        dcc.Dropdown(
            id='ticker-dropdown',
            options=[
                {'label': 'WEGE3', 'value': 'WEGE3'},
                {'label': 'PETR4', 'value': 'PETR4'},
                {'label': 'CEAB3', 'value': 'CEAB3'}
            ],
            value='WEGE3',  # Default selected ticker
            style={
                'width': '70%',  # Adjust width
                'margin': 'auto',
                'fontSize': '16px',
                'padding': '10px',
                'borderRadius': '10px',  # Add border radius for a rounded appearance
                'boxShadow': '0px 0px 10px 0px rgba(0, 0, 0, 0.1)'  # Add a subtle box shadow
            }
        ),
    ], className='container'),

    dcc.Graph(id='candlestick-chart', style={'margin': '20px'}, className='graph-container'),

    html.Div([
        html.H2("Financial News Journal", style={'textAlign': 'center', 'fontFamily': 'Georgia'}),

        # Display news headlines with journal styling
        html.Div(
            id='news-headlines',
            style={'margin': '20px', 'fontSize': '18px', 'color': 'black', 'fontWeight': 'normal', 'lineHeight': '1.6'}
        ),
    ], style={'fontFamily': 'Arial, sans-serif', 'maxWidth': '800px', 'margin': 'auto'}),
], id='main-container', style={'background-color': '#F4F4F4', 'color': 'black'})

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)