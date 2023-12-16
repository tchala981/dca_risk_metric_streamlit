# instructions.py
import streamlit as st

def main():
    st.title('Instructions and FAQ')

    # General introduction or overview
    st.write('Welcome to the DCA/SIP Risk Metric Dashboard! This page is designed to help you navigate and use the app effectively.')

    # Specific Instructions
    with st.expander("Getting Started"):
        st.write("""
            **Step 1: Select an Asset**
            - In the sidebar, choose an asset from the dropdown menu.
            - Available assets include Bitcoin-USD, Gold Futures, Nifty 50 Index, S&P 500 etc.

            **Step 2: Choose Data Interval and Window Size**
            - Select the interval for data analysis (e.g., weekly).
            - Choose the window size for the moving average calculation using the input box.

            **Step 3: Analyze Data**
            - Click on 'Show Analysis' to generate the charts.
            - The app will display two interactive charts based on the selected parameters.
        """)

    with st.expander("Understanding DCA and SIP Strategies"):
        st.write("""
            **Dollar Cost Averaging (DCA) and Systematic Investment Plans (SIP)**
            
            - DCA and SIP are strategies designed to mitigate market volatility risks by regularly investing a fixed amount into an asset.
            - They are effective for avoiding market timing risks, benefiting from compounding, and maintaining emotional discipline in investment.
            - These strategies are ideal for passive investors as they require less frequent trading decisions and market monitoring.

            **Applicability of This App**
            
            - The app provides historical percentile risk scores and simplified risk categories, aiding in informed decision-making.
            - It's useful for scaling into and out of positions, offering insights into potentially lower-risk opportunities.
            - Users can tailor their investment strategies to align with their risk tolerance and goals.
        """)

    with st.expander("About the App's Risk Metric"):
        st.write("""
            **Why Harmonic Moving Average?**
            
            - The app uses the Harmonic Moving Average as a baseline, combined with other techniques to provide a simple risk metric for various assets.
            - The HMA represents the average cost basis for someone investing a fixed dollar amount over a period of time (the window length) and is thus, especially relevant for DCA strategies.

            **Notes, Guidelines, Warnings for Usage**

            - The names of the risk categories, like "Very Low Risk" or "Very High Risk" are simply an indication of the deviation of the price from mean value, NOT a signal to buy or sell.
            - As you will notice, an asset can stay in a zone like "Very High Risk" for a very long time, so the price simply entering these zones does not mean you have to exit your whole position.
            - Predicting tops and bottoms are neither the goal nor the intention of this app.
            - Instead, these categories are meant as guidelines for risk management. Allowing the user to follow along a chosen systematic gradual entry and exit strategy in an informed manner.
            - The actual entry and exit strategy (and investment instrument) is for the user to choose after conducting their due diligence. This could be something like, aggressive entry, moderate entry, do nothing, gradual scaling out, at appropriate zones.
            - The risk categories are guides for understanding the asset's price relative to its historical performance.
            - They should be used as part of a broader strategy considering the user's specific circumstances and risk tolerance.
            - The app DOES NOT endorse any specific entry or exit strategy.
            - Users should conduct their due diligence before investing.
            - The default settings for the interval (weekly data) and window (200 (weeks)) will be useful for the primary intented use-case for this app: long-term investing.
            - General guideline is that these 2 parameters should be adjusted to your expected average holding period.
            
            **Disclaimer**
            
            - The app is for informational purposes and does not endorse any specific trading or investing strategy.
        """)

    # FAQs Section
    st.markdown("## Frequently Asked Questions (FAQ)")
    with st.expander("Q: How do I expand the charts?"):
        st.write("A: Hover over one of the two charts. On the top left corner, you'll see an arrow. Click on it to expand the chart.")

    with st.expander("Q: How do I zoom in/out, move the chart around, rescale, etc.?"):
        st.write("A: Upon hovering over the chart, on the top left corner you'll see the tool-box for all these controls.")

    with st.expander("Q: How do I zoom in/out over only one axis easily?"):
        st.write("""A: - After selecting the zoom tool from the toolbox, drag vertically or horizontally from the point you clicked initially. This will enable zooming across one axis.  
        - If you're not dragging exactly vertically or horizontally, a box will open up zooming across both axes.  
        - After zooming to the required level, select the 'Pan' tool from the toolbox to move the chart around to your desired spot.""")

    with st.expander("Q: Why are the initial few datapoints in the charts gray/de-coloured?"):
        st.markdown("""A: - To calculate the moving Harmonic Average, you need atleast enough points equal to the Window length (chosen by the User). So you can't have a classification for those initial points.   
        - Also, since the calculation of the risk metric involves taking rolling percentiles (multiple times), even the earliest 100 or so Coloured data-points shouldn't be taken seriously. Which shouldn't be a problem, as the User is usually only concerned with the latest status.   
        - Another point is that the User should use their judgement in making sure the Window length should be much smaller than the number of datapoints available.""")

    with st.expander("Q: Can I download the data used in this app?"):
        st.write("A: Yes. Intended for research and educational purposes, for personal use only. After the user runs an analysis (after clicking on 'Show Analysis') a button opens at the bottom to: 'Download data as CSV'")

    with st.expander("Q: How frequently is the data updated?"):
        st.write("""A: The source of the data is Yahoo Finance. You can expect daily updates.   
            - https://github.com/ranaroussi/yfinance
            """)

    # Contact Information
    st.markdown("### Contact Information")
    st.markdown("For further queries or feedback:")
    st.markdown('<a href="mailto:jothe3inv@gmail.com">Email (Atanu Gayen): jothe3inv@gmail.com</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
