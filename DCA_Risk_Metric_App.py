# main page.py
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import hmean, percentileofscore
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import io

# st.set_page_config(layout="wide")

def main():

    # Your existing functions (prepare_data_for_analysis, plot_historical_percentile_risk, plot_simplified_risk) go here
    def prepare_data_for_analysis(scrip, interval, window):
        def calculate_harmonic_mean(data):
            return data['Close'].rolling(window=window).apply(hmean, raw=True)

        def calculate_ln_close_hm(data):
            return np.log(data['Close'] / data['Harmonic_Mean'])

        def calculate_historical_percentiles(data, column):
            historical_percentiles = []
            for i in range(len(data)):
                current_slice = data[column].iloc[:i+1].dropna()
                current_value = data[column].iloc[i]
                if not np.isnan(current_value):
                    percentile_rank = percentileofscore(current_slice, current_value, kind='weak')
                    historical_percentiles.append(percentile_rank)
                else:
                    historical_percentiles.append(np.nan)
            return pd.Series(historical_percentiles, index=data.index)

        # Download data with auto-adjust for dividends and splits
        # data = yf.download(scrip, interval=interval, auto_adjust=True)[['Close']]
        data = yf.download(scrip, interval=interval, auto_adjust=True).loc[:,['Close']] 

        # Apply calculations
        data['Harmonic_Mean'] = calculate_harmonic_mean(data)
        data['Ln_Close_HM'] = calculate_ln_close_hm(data)
        data['deviation_percentile'] = calculate_historical_percentiles(data, 'Ln_Close_HM')
        data['percentile_risk'] = calculate_historical_percentiles(data, 'deviation_percentile')
        
        return data

    def plot_historical_percentile_risk_plotly(data, scrip):
        fig = go.Figure()

        # Add traces for closing prices and harmonic mean
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Closing Price'))
        fig.add_trace(go.Scatter(x=data.index, y=data['Harmonic_Mean'], mode='lines', name='Harmonic Mean'))

        # Add scatter trace for percentile risk
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=data['Close'], 
            mode='markers', 
            name='Closing Price (Scatter)',
            marker=dict(color=data['percentile_risk'], colorscale='Viridis'),
            hoverinfo='text',
            text=[f'Close: {close}<br>Risk Score: {risk:.2f}' for close, risk in zip(data['Close'], data['percentile_risk'])]
        ))

        fig.update_layout(
            title=f'{scrip} Closing Price with Historical Percentile Risk Score (0 to 100)',
            xaxis_title='Date',
            yaxis_title='Closing Price',
            legend=dict(x=0.01, y=0.99, orientation='v', xanchor='left', yanchor='top'),
            margin=dict(l=100, r=0, t=40, b=0)
        )

        return fig

    def plot_simplified_risk_plotly(data, scrip):
        # Define discrete color scale with category names
        category_colors = {
            'Very Low Risk': 'blue',
            'Low Risk': 'green',
            'Neutral': 'yellow',
            'High Risk': 'orange',
            'Very High Risk': 'red'
        }

        # Map percentile risk to category names
        data['Risk_Category'] = pd.cut(data['percentile_risk'], 
                                       bins=[0, 20, 40, 60, 80, 100], 
                                       labels=list(category_colors.keys()),
                                       right=False)

        fig = go.Figure()

        # Add a line plot for harmonic mean
        fig.add_trace(go.Scatter(x=data.index, y=data['Harmonic_Mean'], mode='lines', name='Harmonic Mean', line=dict(color='darkred', width=1)))

        # Add a line plot for closing prices
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Closing Price', line=dict(color='grey', width=1)))

        # Add scatter plot for risk categories
        for category, color in category_colors.items():
            category_data = data[data['Risk_Category'] == category]
            fig.add_trace(go.Scatter(x=category_data.index, y=category_data['Close'], mode='markers', name=category,
                                     marker=dict(color=color)))

        # Update layout
        fig.update_layout(
            title=f'{scrip} Closing Price with Simplified Risk Categories',
            xaxis_title='Date',
            yaxis_title='Closing Price',
            legend=dict(x=0.01, y=0.99, orientation='v', xanchor='left', yanchor='top'),
            margin=dict(l=100, r=0, t=40, b=0)
        )

        return fig


    # Define a list of tuples with (alias, actual_value)
    # scrip_options = [
    #     ('Bitcoin USD', 'BTC-USD'),
    #     ('Gold Futures (USD)', 'GC=F'),
    #     ('Gold Bees ETF', 'GOLDBEES.NS'),
    #     ('Nifty 50 Index', '^NSEI'),
    #     ('Nifty Bank Index', '^NSEBANK'),
    #     ('NASDAQ 100', '^NDX'),
    #     ('S&P 500', '^SPX'),
    #     ('Dow Jones Industrial', '^DJI')
    # ]
    scrip_options = [
        ('Bitcoin-USD', 'BTC-USD'),
        # ('Ethereum USD', 'ETH-USD'),
        ('Gold Futures (USD)', 'GC=F'),
        ('Silver Futures (USD)', 'SI=F'),
        ('US 10-Year Treasury', '^TNX'),
        ('S&P 500', '^GSPC'),
        ('Dow Jones Industrial Average', '^DJI'),
        ('NASDAQ 100', '^NDX'),
        ('Nifty 50 Index', '^NSEI'),
        ('Sensex', '^BSESN'),
        ('Nifty Bank', '^NSEBANK'),
        # ('Nifty IT', '^CNXIT'),
        # ('Nifty Pharma', '^CNXPHARMA'),
    ]


    # Streamlit app layout
    st.title("DCA/SIP Risk Metric")

    # Convert the tuple list to a dictionary for easy lookup
    scrip_dict = dict(scrip_options)

    # Sidebar for user inputs
    
    # Asset Selection
    selected_scrip_alias = st.sidebar.selectbox('Select Asset', options=list(scrip_dict.keys()))
    scrip = scrip_dict[selected_scrip_alias]  # Get the actual value associated with the alias

    # Interval selection
    interval_options = ['1d', '1wk']  # List of interval options
    default_interval_index = interval_options.index('1wk')  # Default to '1wk'

    interval = st.sidebar.selectbox('Select Interval', interval_options, index=default_interval_index)

    st.sidebar.write("Select Moving Average Window Size (between 5 and 2000)")
    # Number input with hidden label
    window_input = st.sidebar.number_input('Window Input', min_value=5, max_value=2000, value=200, step=1, key='window_input', label_visibility="collapsed")
    # # Slider with hidden label
    # window_slider = st.sidebar.slider('Window Slider', 5, 500, 200, step=1, key='window_slider', label_visibility="collapsed")
    # # Use whichever input was most recently changed
    # window = window_slider if st.session_state['window_slider'] == st.session_state['window_input'] else window_input
    window = window_input


    # Function to plot within Streamlit
    def st_plot(fig):
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.image(buf)

    # Fetch and display data based on user input
    if st.button('Show Analysis'):
        btc_data = prepare_data_for_analysis(scrip, interval, window)

        fig2 = plot_simplified_risk_plotly(btc_data, selected_scrip_alias)
        st.plotly_chart(fig2)

        fig1 = plot_historical_percentile_risk_plotly(btc_data, selected_scrip_alias)
        st.plotly_chart(fig1)
        

        # Download as CSV
        csv = btc_data.to_csv(index=True)
        b = io.BytesIO(csv.encode())
        st.download_button("Download data as CSV", b, "btc_data.csv", "text/csv")


if __name__ == "__main__":
    main()