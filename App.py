import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(page_title="Credit & Trade Line Manager Pro", layout="wide", page_icon="💳")

# Custom CSS
st.markdown("""
<style>
    /* Metric cards with black background and white text */
    .stMetric {
        background-color: #1a1a1a;
        color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .stMetric label {
        color: #cccccc !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    
    .stMetric [data-testid="stMetricDelta"] {
        color: #ffffff !important;
    }
    
    /* Expander cards with black background */
    div[data-testid="stExpander"] {
        background-color: #1a1a1a;
        color: #ffffff;
        border-radius: 10px;
        border: 1px solid #333333;
        margin-bottom: 10px;
    }
    
    div[data-testid="stExpander"] summary {
        color: #ffffff !important;
    }
    
    div[data-testid="stExpander"] p, 
    div[data-testid="stExpander"] span,
    div[data-testid="stExpander"] div {
        color: #ffffff !important;
    }
    
    /* All text inside expanders */
    .stExpander {
        color: #ffffff;
    }
    
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
        color: #ffffff !important;
    }
    
    /* Form elements inside expanders */
    div[data-testid="stExpander"] input,
    div[data-testid="stExpander"] select,
    div[data-testid="stExpander"] textarea {
        background-color: #2a2a2a;
        color: #ffffff;
        border: 1px solid #444444;
    }
    
    /* Markdown inside expanders */
    div[data-testid="stExpander"] .stMarkdown {
        color: #ffffff !important;
    }
    
    div[data-testid="stExpander"] h1,
    div[data-testid="stExpander"] h2,
    div[data-testid="stExpander"] h3,
    div[data-testid="stExpander"] h4 {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for data with comprehensive demo data
if 'accounts' not in st.session_state:
    st.session_state.accounts = pd.DataFrame({
        'Account Name': [
            'Chase Sapphire Reserve',
            'American Express Gold',
            'Capital One Venture X',
            'Citi Double Cash',
            'Discover It Cash Back',
            'Bank of America Premium Rewards',
            'Wells Fargo Active Cash',
            'Auto Loan - Toyota Camry',
            'Home Mortgage - Primary',
            'Personal Loan - Consolidation',
            'Chase Freedom Unlimited',
            'Apple Card',
            'Amazon Prime Visa',
            'Target RedCard',
            'Best Buy Credit Card'
        ],
        'Account Type': [
            'Credit Card', 'Credit Card', 'Credit Card', 'Credit Card', 'Credit Card',
            'Credit Card', 'Credit Card', 'Installment Loan', 'Mortgage', 'Personal Loan',
            'Credit Card', 'Credit Card', 'Credit Card', 'Credit Card', 'Credit Card'
        ],
        'Institution': [
            'Chase Bank', 'American Express', 'Capital One', 'Citibank', 'Discover',
            'Bank of America', 'Wells Fargo', 'Toyota Financial', 'Quicken Loans', 'SoFi',
            'Chase Bank', 'Goldman Sachs', 'Chase Bank', 'TD Bank', 'Citibank'
        ],
        'Credit Limit': [10000, 15000, 10000, 8000, 5000, 12000, 7500, 28000, 350000, 25000, 6000, 4000, 8500, 3000, 5000],
        'Current Balance': [2500, 4200, 3500, 1200, 800, 5500, 1100, 15600, 287000, 18500, 1800, 650, 2100, 450, 1200],
        'Statement Balance': [2800, 4500, 3800, 1350, 950, 5800, 1250, 15600, 287000, 18500, 2000, 750, 2300, 500, 1350],
        'Minimum Payment': [84, 135, 105, 40, 29, 165, 35, 485, 1847, 567, 60, 25, 69, 25, 38],
        'Due Date': [
            '2025-11-05', '2025-11-10', '2025-11-08', '2025-11-15', '2025-11-12',
            '2025-11-07', '2025-11-20', '2025-11-01', '2025-11-01', '2025-11-05',
            '2025-11-18', '2025-11-22', '2025-11-14', '2025-11-25', '2025-11-28'
        ],
        'Statement Date': [
            '2025-10-15', '2025-10-20', '2025-10-18', '2025-10-25', '2025-10-22',
            '2025-10-17', '2025-10-30', '2025-10-01', '2025-10-01', '2025-10-05',
            '2025-10-28', '2025-11-01', '2025-10-24', '2025-11-05', '2025-11-08'
        ],
        'Reporting Date': [
            '2025-10-20', '2025-10-25', '2025-10-23', '2025-10-28', '2025-10-27',
            '2025-10-22', '2025-11-02', '2025-10-05', '2025-10-05', '2025-10-08',
            '2025-11-01', '2025-11-04', '2025-10-28', '2025-11-08', '2025-11-11'
        ],
        'Last Payment Date': [
            '2025-09-28', '2025-10-05', '2025-10-02', '2025-09-20', '2025-09-25',
            '2025-09-30', '2025-10-10', '2025-10-01', '2025-10-01', '2025-10-01',
            '2025-10-08', '2025-10-15', '2025-10-05', '2025-10-12', '2025-10-18'
        ],
        'Last Payment Amount': [3200, 4100, 3900, 1500, 1100, 6000, 1400, 485, 1847, 567, 2200, 800, 2500, 600, 1400],
        'APR': [19.99, 21.24, 18.99, 15.99, 14.99, 17.49, 16.99, 4.29, 3.75, 9.99, 18.24, 13.99, 16.49, 24.99, 22.49],
        'Rewards Points': [45000, 82000, 38000, 0, 12500, 28000, 0, 0, 0, 0, 18000, 4200, 15000, 2800, 6500],
        'Points Value': [0.015, 0.012, 0.020, 0.0, 0.010, 0.010, 0.0, 0.0, 0.0, 0.0, 0.015, 0.010, 0.010, 0.010, 0.010],
        'Annual Fee': [550, 250, 395, 0, 0, 95, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'Status': ['Active'] * 15,
        'Open Date': [
            '2020-03-15', '2019-06-22', '2021-08-05', '2018-11-10', '2017-05-18',
            '2022-01-20', '2023-03-12', '2023-02-10', '2018-07-15', '2022-09-01',
            '2019-12-03', '2021-09-20', '2020-06-08', '2016-04-25', '2019-10-30'
        ],
        'Account Number': [
            '****1234', '****5678', '****9012', '****3456', '****7890',
            '****2345', '****6789', '****0123', '****4567', '****8901',
            '****2468', '****1357', '****9753', '****1593', '****7531'
        ],
        'Credit Bureau': [
            'All 3', 'All 3', 'All 3', 'All 3', 'All 3',
            'All 3', 'All 3', 'All 3', 'All 3', 'All 3',
            'All 3', 'All 3', 'All 3', 'All 3', 'All 3'
        ],
        'Payment History': [
            '100%', '100%', '100%', '98%', '100%',
            '100%', '100%', '100%', '100%', '100%',
            '100%', '97%', '100%', '95%', '100%'
        ],
        'Account Age (Months)': [
            68, 76, 50, 84, 101,
            46, 31, 32, 87, 37,
            70, 49, 64, 114, 72
        ],
        'Autopay Enabled': [
            'Yes', 'Yes', 'Yes', 'No', 'Yes',
            'Yes', 'No', 'Yes', 'Yes', 'Yes',
            'No', 'Yes', 'Yes', 'No', 'No'
        ],
        'Cashback Rate': [
            '0%', '0%', '0%', '2%', '5% rotating',
            '1.5-2.5%', '2%', '0%', '0%', '0%',
            '1.5%', '2% Apple/3% Apple', '3% Amazon', '5% Target', '5-6% Best Buy'
        ],
        'Notes': [
            'Primary travel card, TSA PreCheck credit',
            'Excellent for dining, 4x at restaurants',
            'New travel card with lounge access',
            'Simple cashback, no annual fee',
            'Rotating categories, good for groceries',
            'Premium banking rewards card',
            'Simple 2% cashback on everything',
            '60-month loan, excellent rate',
            '30-year fixed, refinanced 2021',
            'Debt consolidation, 5-year term',
            'Everyday spending card',
            'Apple purchases and Apple Pay bonus',
            'Amazon Prime benefits included',
            'Store card, occasional promotions',
            'Store card for electronics'
        ]
    })

# Calculate utilization
def calculate_utilization(balance, limit):
    if limit > 0:
        return round((balance / limit) * 100, 2)
    return 0

# Calculate credit age
def calculate_age_years(open_date):
    try:
        open = pd.to_datetime(open_date)
        today = pd.Timestamp.now()
        return round((today - open).days / 365.25, 1)
    except:
        return 0

# Add utilization column
st.session_state.accounts['Utilization %'] = st.session_state.accounts.apply(
    lambda row: calculate_utilization(row['Current Balance'], row['Credit Limit']), axis=1
)

# Calculate points value in dollars
st.session_state.accounts['Points Dollar Value'] = st.session_state.accounts['Rewards Points'] * st.session_state.accounts['Points Value']

# Title and description
st.title("💳 Credit & Trade Line Manager Pro")
st.markdown("**Comprehensive credit account tracking with payment scheduling, reporting dates, and rewards optimization**")
st.divider()

# Sidebar for navigation and quick actions
with st.sidebar:
    st.header("⚙️ Quick Actions")
    
    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()
    
    if st.button("📊 Generate Report", use_container_width=True):
        st.session_state['show_report'] = True
    
    if st.button("⚠️ Show Alerts", use_container_width=True):
        st.session_state['show_alerts'] = True
    
    st.divider()
    
    st.header("📈 Quick Stats")
    active_count = len(st.session_state.accounts[st.session_state.accounts['Status'] == 'Active'])
    st.metric("Active Accounts", active_count)
    
    avg_age = st.session_state.accounts['Account Age (Months)'].mean()
    st.metric("Avg Account Age", f"{avg_age:.0f} months")
    
    autopay_count = len(st.session_state.accounts[st.session_state.accounts['Autopay Enabled'] == 'Yes'])
    st.metric("Autopay Enabled", f"{autopay_count}/{active_count}")
    
    st.divider()
    st.markdown("### 💡 Tips")
    st.info("Keep utilization under 30% for optimal credit scores")
    st.success("Pay before reporting date to lower reported balance")
    st.warning("Set up autopay to never miss a payment")

# Dashboard Statistics
st.header("📊 Dashboard Overview")

col1, col2, col3, col4, col5, col6 = st.columns(6)

total_limit = st.session_state.accounts['Credit Limit'].sum()
total_balance = st.session_state.accounts['Current Balance'].sum()
total_points = st.session_state.accounts['Rewards Points'].sum()
total_points_value = st.session_state.accounts['Points Dollar Value'].sum()
avg_utilization = calculate_utilization(total_balance, total_limit)
total_min_payments = st.session_state.accounts['Minimum Payment'].sum()

with col1:
    st.metric("Total Credit Limit", f"${total_limit:,.0f}", help="Combined credit limit across all accounts")
with col2:
    st.metric("Total Balance", f"${total_balance:,.0f}", delta=f"-${total_min_payments:,.0f}", delta_color="inverse", help="Total current balance owed")
with col3:
    util_delta = "Good" if avg_utilization < 30 else "High"
    st.metric("Overall Utilization", f"{avg_utilization:.1f}%", delta=util_delta, delta_color="inverse" if avg_utilization >= 30 else "normal", help="Lower is better for credit score")
with col4:
    st.metric("Total Min Payments", f"${total_min_payments:,.2f}", help="Sum of all minimum payments due")
with col5:
    st.metric("Total Rewards Points", f"{total_points:,.0f}", help="Combined rewards points balance")
with col6:
    st.metric("Points Cash Value", f"${total_points_value:,.2f}", help="Estimated cash value of all points")

# Additional metrics row
col1, col2, col3, col4 = st.columns(4)

credit_cards = st.session_state.accounts[st.session_state.accounts['Account Type'] == 'Credit Card']
cc_limit = credit_cards['Credit Limit'].sum()
cc_balance = credit_cards['Current Balance'].sum()
cc_util = calculate_utilization(cc_balance, cc_limit)

loans = st.session_state.accounts[st.session_state.accounts['Account Type'].isin(['Installment Loan', 'Mortgage', 'Personal Loan'])]
total_loan_balance = loans['Current Balance'].sum()

with col1:
    st.metric("Credit Card Utilization", f"{cc_util:.1f}%", help="Utilization for credit cards only")
with col2:
    st.metric("Total Loan Balance", f"${total_loan_balance:,.0f}", help="Combined balance of all loans")
with col3:
    avg_apr = st.session_state.accounts[st.session_state.accounts['Current Balance'] > 0]['APR'].mean()
    st.metric("Weighted Avg APR", f"{avg_apr:.2f}%", help="Average APR across accounts with balance")
with col4:
    total_annual_fees = st.session_state.accounts['Annual Fee'].sum()
    st.metric("Annual Fees", f"${total_annual_fees:,.0f}", help="Total annual fees across all accounts")

st.divider()

# Visualization Section
st.header("📈 Analytics & Insights")

tab_viz1, tab_viz2, tab_viz3, tab_viz4 = st.tabs(["Utilization Analysis", "Balance Distribution", "Payment Timeline", "Rewards Tracking"])

with tab_viz1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Utilization by account
        util_df = st.session_state.accounts[st.session_state.accounts['Account Type'] == 'Credit Card'].copy()
        util_df = util_df.sort_values('Utilization %', ascending=True)
        
        fig_util = px.bar(util_df, 
                         x='Utilization %', 
                         y='Account Name',
                         title='Credit Card Utilization by Account',
                         color='Utilization %',
                         color_continuous_scale=['green', 'yellow', 'red'],
                         range_color=[0, 100])
        fig_util.add_vline(x=30, line_dash="dash", line_color="orange", annotation_text="30% Threshold")
        st.plotly_chart(fig_util, use_container_width=True)
    
    with col2:
        # Credit utilization gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_utilization,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Credit Utilization"},
            delta={'reference': 30},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "lightyellow"},
                    {'range': [70, 100], 'color': "lightcoral"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70}}))
        st.plotly_chart(fig_gauge, use_container_width=True)

with tab_viz2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Balance by account type
        type_summary = st.session_state.accounts.groupby('Account Type').agg({
            'Current Balance': 'sum',
            'Account Name': 'count'
        }).reset_index()
        type_summary.columns = ['Account Type', 'Total Balance', 'Count']
        
        fig_pie = px.pie(type_summary, 
                        values='Total Balance', 
                        names='Account Type',
                        title='Balance Distribution by Account Type',
                        hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Top 10 accounts by balance
        top_accounts = st.session_state.accounts.nlargest(10, 'Current Balance')
        fig_bar = px.bar(top_accounts,
                        x='Current Balance',
                        y='Account Name',
                        title='Top 10 Accounts by Balance',
                        orientation='h',
                        color='Account Type')
        st.plotly_chart(fig_bar, use_container_width=True)

with tab_viz3:
    # Payment timeline
    timeline_df = st.session_state.accounts[['Account Name', 'Due Date', 'Minimum Payment', 'Current Balance']].copy()
    timeline_df['Due Date'] = pd.to_datetime(timeline_df['Due Date'])
    timeline_df = timeline_df.sort_values('Due Date')
    
    fig_timeline = px.scatter(timeline_df,
                             x='Due Date',
                             y='Minimum Payment',
                             size='Current Balance',
                             color='Account Name',
                             title='Payment Timeline (size = current balance)',
                             hover_data=['Account Name', 'Minimum Payment', 'Current Balance'])
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Payment calendar table
    st.subheader("Detailed Payment Schedule")
    display_df = timeline_df[['Account Name', 'Due Date', 'Minimum Payment', 'Current Balance']].copy()
    display_df['Due Date'] = display_df['Due Date'].dt.strftime('%Y-%m-%d')
    display_df['Minimum Payment'] = display_df['Minimum Payment'].apply(lambda x: f"${x:,.2f}")
    display_df['Current Balance'] = display_df['Current Balance'].apply(lambda x: f"${x:,.2f}")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

with tab_viz4:
    col1, col2 = st.columns(2)
    
    with col1:
        # Rewards points by account
        rewards_df = st.session_state.accounts[st.session_state.accounts['Rewards Points'] > 0].copy()
        rewards_df = rewards_df.sort_values('Rewards Points', ascending=False)
        
        fig_rewards = px.bar(rewards_df,
                            x='Account Name',
                            y='Rewards Points',
                            title='Rewards Points by Account',
                            color='Points Dollar Value',
                            color_continuous_scale='Blues')
        fig_rewards.update_xaxis(tickangle=-45)
        st.plotly_chart(fig_rewards, use_container_width=True)
    
    with col2:
        # Points value comparison
        fig_value = px.bar(rewards_df,
                          x='Account Name',
                          y='Points Dollar Value',
                          title='Estimated Cash Value of Points',
                          color='Points Value',
                          color_continuous_scale='Greens')
        fig_value.update_xaxis(tickangle=-45)
        st.plotly_chart(fig_value, use_container_width=True)
    
    # Rewards summary
    st.subheader("Rewards Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Highest Point Balance", f"{rewards_df['Rewards Points'].max():,.0f}", 
                 rewards_df.loc[rewards_df['Rewards Points'].idxmax(), 'Account Name'])
    with col2:
        st.metric("Most Valuable Points", f"${rewards_df['Points Dollar Value'].max():,.2f}",
                 rewards_df.loc[rewards_df['Points Dollar Value'].idxmax(), 'Account Name'])
    with col3:
        avg_point_value = rewards_df['Points Value'].mean()
        st.metric("Avg Point Value", f"{avg_point_value:.3f}¢")

st.divider()

# Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📋 All Accounts", "➕ Add Account", "📅 Payment Calendar", "⚠️ Alerts & Reminders", "📊 Credit Score Insights", "💾 Import/Export"])

# Tab 1: Display All Accounts
with tab1:
    st.header("All Accounts")
    
    # Advanced Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        filter_type = st.multiselect("Filter by Account Type", 
                                     options=st.session_state.accounts['Account Type'].unique(),
                                     default=st.session_state.accounts['Account Type'].unique())
    with col2:
        filter_status = st.multiselect("Filter by Status",
                                       options=st.session_state.accounts['Status'].unique(),
                                       default=st.session_state.accounts['Status'].unique())
    with col3:
        filter_autopay = st.selectbox("Autopay Status", ['All', 'Enabled', 'Disabled'])
    with col4:
        sort_by = st.selectbox("Sort by", ['Account Name', 'Utilization %', 'Due Date', 'Current Balance', 
                                           'Rewards Points', 'APR', 'Account Age (Months)'])
    
    # Search functionality
    search_term = st.text_input("🔍 Search accounts", placeholder="Search by account name, institution, or notes...")
    
    # Apply filters
    filtered_df = st.session_state.accounts[
        (st.session_state.accounts['Account Type'].isin(filter_type)) &
        (st.session_state.accounts['Status'].isin(filter_status))
    ]
    
    if filter_autopay != 'All':
        autopay_val = 'Yes' if filter_autopay == 'Enabled' else 'No'
        filtered_df = filtered_df[filtered_df['Autopay Enabled'] == autopay_val]
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df['Account Name'].str.contains(search_term, case=False, na=False) |
            filtered_df['Institution'].str.contains(search_term, case=False, na=False) |
            filtered_df['Notes'].str.contains(search_term, case=False, na=False)
        ]
    
    filtered_df = filtered_df.sort_values(by=sort_by)
    
    st.write(f"Showing **{len(filtered_df)}** of **{len(st.session_state.accounts)}** accounts")
    
    # Display accounts with enhanced details
    if len(filtered_df) > 0:
        for idx, row in filtered_df.iterrows():
            util_color = "🟢" if row['Utilization %'] < 30 else "🟡" if row['Utilization %'] < 70 else "🔴"
            autopay_icon = "✅" if row['Autopay Enabled'] == 'Yes' else "❌"
            
            with st.expander(f"**{row['Account Name']}** - {row['Institution']} ({row['Account Type']}) {util_color} {autopay_icon}", expanded=False):
                # Main account information in columns
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown("**💼 Account Details**")
                    st.write(f"**Status:** {row['Status']}")
                    st.write(f"**Account #:** {row['Account Number']}")
                    st.write(f"**Open Date:** {row['Open Date']}")
                    st.write(f"**Account Age:** {row['Account Age (Months)']} months")
                    st.write(f"**Credit Bureau:** {row['Credit Bureau']}")
                    st.write(f"**Payment History:** {row['Payment History']}")
                
                with col2:
                    st.markdown("**💰 Balance Information**")
                    st.write(f"**Credit Limit:** ${row['Credit Limit']:,.2f}")
                    st.write(f"**Current Balance:** ${row['Current Balance']:,.2f}")
                    st.write(f"**Statement Balance:** ${row['Statement Balance']:,.2f}")
                    st.write(f"**Available Credit:** ${row['Credit Limit'] - row['Current Balance']:,.2f}")
                    util_emoji = "🟢" if row['Utilization %'] < 30 else "🟡" if row['Utilization %'] < 70 else "🔴"
                    st.write(f"**Utilization:** {row['Utilization %']:.1f}% {util_emoji}")
                    st.write(f"**Annual Fee:** ${row['Annual Fee']:.2f}")
                
                with col3:
                    st.markdown("**📅 Payment & Dates**")
                    st.write(f"**Minimum Payment:** ${row['Minimum Payment']:.2f}")
                    st.write(f"**Due Date:** {row['Due Date']}")
                    st.write(f"**Statement Date:** {row['Statement Date']}")
                    st.write(f"**Reporting Date:** {row['Reporting Date']}")
                    st.write(f"**Last Payment:** ${row['Last Payment Amount']:.2f}")
                    st.write(f"**Last Payment Date:** {row['Last Payment Date']}")
                    st.write(f"**APR:** {row['APR']:.2f}%")
                
                with col4:
                    st.markdown("**🎁 Rewards & Features**")
                    if row['Rewards Points'] > 0:
                        st.write(f"**Points:** {row['Rewards Points']:,.0f}")
                        st.write(f"**Points Value:** ${row['Points Dollar Value']:.2f}")
                        st.write(f"**Value per Point:** {row['Points Value']:.3f}¢")
                    else:
                        st.write(f"**Points:** N/A")
                    st.write(f"**Cashback:** {row['Cashback Rate']}")
                    st.write(f"**Autopay:** {row['Autopay Enabled']}")
                
                # Notes section
                if row['Notes']:
                    st.markdown("**📝 Notes**")
                    st.info(row['Notes'])
                
                # Calculate days until due
                days_until_due = (pd.to_datetime(row['Due Date']) - pd.Timestamp.now()).days
                if days_until_due <= 7 and days_until_due >= 0:
                    st.warning(f"⚠️ Payment due in {days_until_due} days!")
                elif days_until_due < 0:
                    st.error(f"🚨 Payment OVERDUE by {abs(days_until_due)} days!")
                
                # Action buttons
                col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{idx}"):
                        st.session_state[f'editing_{idx}'] = True
                with col2:
                    if st.button(f"💳 Pay", key=f"pay_{idx}"):
                        st.session_state[f'paying_{idx}'] = True
                with col3:
                    if st.button(f"🗑️ Delete", key=f"delete_{idx}"):
                        if st.session_state.get(f'confirm_delete_{idx}', False):
                            st.session_state.accounts = st.session_state.accounts.drop(idx).reset_index(drop=True)
                            st.success(f"Account '{row['Account Name']}' deleted!")
                            st.rerun()
                        else:
                            st.session_state[f'confirm_delete_{idx}'] = True
                            st.warning("Click delete again to confirm")
                
                # Payment form
                if st.session_state.get(f'paying_{idx}', False):
                    st.markdown("---")
                    st.markdown("**💳 Record Payment**")
                    with st.form(key=f"payment_form_{idx}"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            payment_amount = st.number_input("Payment Amount", min_value=0.0, 
                                                            value=float(row['Minimum Payment']), step=10.0)
                        with col2:
                            payment_date = st.date_input("Payment Date", value=datetime.now())
                        with col3:
                            payment_type = st.selectbox("Payment Type", ["Minimum Payment", "Statement Balance", "Full Balance", "Custom"])
                        
                        if st.form_submit_button("💾 Record Payment"):
                            new_balance = row['Current Balance'] - payment_amount
                            st.session_state.accounts.loc[idx, 'Current Balance'] = max(0, new_balance)
                            st.session_state.accounts.loc[idx, 'Last Payment Date'] = payment_date.strftime('%Y-%m-%d')
                            st.session_state.accounts.loc[idx, 'Last Payment Amount'] = payment_amount
                            st.session_state.accounts.loc[idx, 'Utilization %'] = calculate_utilization(new_balance, row['Credit Limit'])
                            st.session_state[f'paying_{idx}'] = False
                            st.success(f"Payment of ${payment_amount:.2f} recorded! New balance: ${new_balance:.2f}")
                            st.rerun()
                
                # Edit form
                if st.session_state.get(f'editing_{idx}', False):
                    st.markdown("---")
                    st.markdown("**✏️ Edit Account**")
                    with st.form(key=f"edit_form_{idx}"):
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            new_balance = st.number_input("Current Balance", value=float(row['Current Balance']))
                            new_limit = st.number_input("Credit Limit", value=float(row['Credit Limit']))
                            new_min_pay = st.number_input("Minimum Payment", value=float(row['Minimum Payment']))
                        with col2:
                            new_due_date = st.date_input("Due Date", value=pd.to_datetime(row['Due Date']))
                            new_statement_date = st.date_input("Statement Date", value=pd.to_datetime(row['Statement Date']))
                            new_reporting_date = st.date_input("Reporting Date", value=pd.to_datetime(row['Reporting Date']))
                        with col3:
                            new_points = st.number_input("Rewards Points", value=int(row['Rewards Points']))
                            new_apr = st.number_input("APR %", value=float(row['APR']))
                            new_annual_fee = st.number_input("Annual Fee", value=float(row['Annual Fee']))
                        with col4:
                            new_status = st.selectbox("Status", ['Active', 'Closed', 'Frozen'], 
                                                     index=['Active', 'Closed', 'Frozen'].index(row['Status']))
                            new_autopay = st.selectbox("Autopay", ['Yes', 'No'], 
                                                      index=['Yes', 'No'].index(row['Autopay Enabled']))
                            new_notes = st.text_area("Notes", value=row['Notes'])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Save Changes", use_container_width=True):
                                st.session_state.accounts.loc[idx, 'Current Balance'] = new_balance
                                st.session_state.accounts.loc[idx, 'Credit Limit'] = new_limit
                                st.session_state.accounts.loc[idx, 'Minimum Payment'] = new_min_pay
                                st.session_state.accounts.loc[idx, 'Due Date'] = new_due_date.strftime('%Y-%m-%d')
                                st.session_state.accounts.loc[idx, 'Statement Date'] = new_statement_date.strftime('%Y-%m-%d')
                                st.session_state.accounts.loc[idx, 'Reporting Date'] = new_reporting_date.strftime('%Y-%m-%d')
                                st.session_state.accounts.loc[idx, 'Rewards Points'] = new_points
                                st.session_state.accounts.loc[idx, 'APR'] = new_apr
                                st.session_state.accounts.loc[idx, 'Annual Fee'] = new_annual_fee
                                st.session_state.accounts.loc[idx, 'Status'] = new_status
                                st.session_state.accounts.loc[idx, 'Autopay Enabled'] = new_autopay
                                st.session_state.accounts.loc[idx, 'Notes'] = new_notes
                                st.session_state.accounts.loc[idx, 'Utilization %'] = calculate_utilization(new_balance, new_limit)
                                st.session_state.accounts.loc[idx, 'Points Dollar Value'] = new_points * row['Points Value']
                                st.session_state[f'editing_{idx}'] = False
                                st.success("Account updated successfully!")
                                st.rerun()
                        with col2:
                            if st.form_submit_button("❌ Cancel", use_container_width=True):
                                st.session_state[f'editing_{idx}'] = False
                                st.rerun()
    else:
        st.info("No accounts match the current filters.")

# Tab 2: Add New Account
with tab2:
    st.header("Add New Account")
    st.markdown("Fill in the details below to add a new credit account or trade line")
    
    with st.form("add_account_form"):
        st.subheader("Basic Information")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            account_name = st.text_input("Account Name*", placeholder="e.g., Chase Sapphire Reserve")
            account_type = st.selectbox("Account Type*", ['Credit Card', 'Installment Loan', 'Line of Credit', 'Mortgage', 'Personal Loan', 'Auto Loan'])
        with col2:
            institution = st.text_input("Institution*", placeholder="e.g., Chase Bank")
            account_number = st.text_input("Account Number (Last 4)", placeholder="****1234", max_chars=8)
        with col3:
            status = st.selectbox("Status", ['Active', 'Closed', 'Frozen'])
            open_date = st.date_input("Open Date", value=datetime.now())
        with col4:
            credit_bureau = st.selectbox("Reports To", ['All 3', 'Experian', 'Equifax', 'TransUnion', 'Multiple', 'Unknown'])
            payment_history = st.selectbox("Payment History", ['100%', '99%', '98%', '97%', '95%', '<95%'])
        
        st.subheader("Financial Details")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            credit_limit = st.number_input("Credit Limit*", min_value=0.0, value=5000.0, step=100.0)
            current_balance = st.number_input("Current Balance*", min_value=0.0, value=0.0, step=10.0)
        with col2:
            statement_balance = st.number_input("Statement Balance", min_value=0.0, value=0.0, step=10.0)
            minimum_payment = st.number_input("Minimum Payment*", min_value=0.0, value=0.0, step=1.0)
        with col3:
            apr = st.number_input("APR %*", min_value=0.0, max_value=100.0, value=15.0, step=0.1)
            annual_fee = st.number_input("Annual Fee", min_value=0.0, value=0.0, step=10.0)
        with col4:
            autopay_enabled = st.selectbox("Autopay Enabled", ['Yes', 'No'])
            cashback_rate = st.text_input("Cashback Rate", placeholder="e.g., 2% or 5% rotating")
        
        st.subheader("Important Dates")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            due_date = st.date_input("Due Date*", value=datetime.now() + timedelta(days=30))
        with col2:
            statement_date = st.date_input("Statement Date", value=datetime.now())
        with col3:
            reporting_date = st.date_input("Reporting Date", value=datetime.now() + timedelta(days=5))
        with col4:
            last_payment_date = st.date_input("Last Payment Date", value=datetime.now())
        
        col1, col2 = st.columns(2)
        with col1:
            last_payment_amount = st.number_input("Last Payment Amount", min_value=0.0, value=0.0, step=10.0)
        
        st.subheader("Rewards & Points")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            rewards_points = st.number_input("Rewards Points", min_value=0, value=0, step=100)
        with col2:
            points_value = st.number_input("Points Value (cents per point)", min_value=0.0, max_value=1.0, value=0.01, step=0.001, format="%.3f")
        with col3:
            points_dollar_value = rewards_points * points_value
            st.metric("Estimated Points Value", f"${points_dollar_value:.2f}")
        
        st.subheader("Additional Information")
        notes = st.text_area("Notes", placeholder="Add any notes about this account (benefits, features, strategies, etc.)", height=100)
        
        submitted = st.form_submit_button("➕ Add Account", use_container_width=True)
        
        if submitted:
            if account_name and institution:
                # Calculate account age
                account_age_months = round((datetime.now() - pd.to_datetime(open_date)).days / 30.44, 0)
                
                new_account = pd.DataFrame({
                    'Account Name': [account_name],
                    'Account Type': [account_type],
                    'Institution': [institution],
                    'Credit Limit': [credit_limit],
                    'Current Balance': [current_balance],
                    'Statement Balance': [statement_balance],
                    'Minimum Payment': [minimum_payment],
                    'Due Date': [due_date.strftime('%Y-%m-%d')],
                    'Statement Date': [statement_date.strftime('%Y-%m-%d')],
                    'Reporting Date': [reporting_date.strftime('%Y-%m-%d')],
                    'Last Payment Date': [last_payment_date.strftime('%Y-%m-%d')],
                    'Last Payment Amount': [last_payment_amount],
                    'APR': [apr],
                    'Rewards Points': [rewards_points],
                    'Points Value': [points_value],
                    'Annual Fee': [annual_fee],
                    'Status': [status],
                    'Open Date': [open_date.strftime('%Y-%m-%d')],
                    'Utilization %': [calculate_utilization(current_balance, credit_limit)],
                    'Points Dollar Value': [rewards_points * points_value],
                    'Account Number': [account_number if account_number else '****0000'],
                    'Credit Bureau': [credit_bureau],
                    'Payment History': [payment_history],
                    'Account Age (Months)': [account_age_months],
                    'Autopay Enabled': [autopay_enabled],
                    'Cashback Rate': [cashback_rate],
                    'Notes': [notes]
                })
                
                st.session_state.accounts = pd.concat([st.session_state.accounts, new_account], ignore_index=True)
                st.success(f"✅ Account '{account_name}' added successfully!")
                st.balloons()
                st.rerun()
            else:
                st.error("Please fill in all required fields (marked with *).")

# Tab 3: Payment Calendar
with tab3:
    st.header("📅 Payment Calendar & Schedule")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        calendar_view = st.selectbox("View", ["Upcoming Payments", "All Active", "This Month", "Next Month"])
    with col2:
        sort_calendar = st.selectbox("Sort By", ["Due Date", "Amount", "Account Name"])
    with col3:
        show_paid = st.checkbox("Show Accounts with $0 Balance", value=False)
    
    # Filter active accounts and sort by due date
    active_accounts = st.session_state.accounts[st.session_state.accounts['Status'] == 'Active'].copy()
    
    if not show_paid:
        active_accounts = active_accounts[active_accounts['Current Balance'] > 0]
    
    active_accounts['Due Date'] = pd.to_datetime(active_accounts['Due Date'])
    
    today = pd.Timestamp.now()
    
    if calendar_view == "This Month":
        active_accounts = active_accounts[active_accounts['Due Date'].dt.month == today.month]
    elif calendar_view == "Next Month":
        next_month = today + pd.DateOffset(months=1)
        active_accounts = active_accounts[active_accounts['Due Date'].dt.month == next_month.month]
    elif calendar_view == "Upcoming Payments":
        active_accounts = active_accounts[active_accounts['Due Date'] >= today]
    
    if sort_calendar == "Due Date":
        active_accounts = active_accounts.sort_values('Due Date')
    elif sort_calendar == "Amount":
        active_accounts = active_accounts.sort_values('Minimum Payment', ascending=False)
    else:
        active_accounts = active_accounts.sort_values('Account Name')
    
    # Summary metrics
    total_due = active_accounts['Minimum Payment'].sum()
    num_payments = len(active_accounts)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Minimum Payments", f"${total_due:,.2f}")
    with col2:
        st.metric("Number of Payments", num_payments)
    with col3:
        overdue_count = len(active_accounts[active_accounts['Due Date'] < today])
        st.metric("Overdue Accounts", overdue_count, delta="⚠️" if overdue_count > 0 else "✅")
    with col4:
        due_soon = len(active_accounts[(active_accounts['Due Date'] >= today) & (active_accounts['Due Date'] <= today + timedelta(days=7))])
        st.metric("Due Within 7 Days", due_soon)
    
    st.divider()
    
    # Payment timeline
    if len(active_accounts) > 0:
        for idx, row in active_accounts.iterrows():
            days_until_due = (row['Due Date'] - today).days
            
            if days_until_due < 0:
                color = "🔴"
                status_text = f"OVERDUE by {abs(days_until_due)} days"
                status_color = "error"
            elif days_until_due <= 3:
                color = "🔴"
                status_text = f"Due in {days_until_due} days - URGENT"
                status_color = "error"
            elif days_until_due <= 7:
                color = "🟠"
                status_text = f"Due in {days_until_due} days"
                status_color = "warning"
            elif days_until_due <= 14:
                color = "🟡"
                status_text = f"Due in {days_until_due} days"
                status_color = "info"
            else:
                color = "🟢"
                status_text = f"Due in {days_until_due} days"
                status_color = "success"
            
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 2, 1])
                
                with col1:
                    st.markdown(f"### {color} {row['Account Name']}")
                    st.caption(row['Institution'])
                
                with col2:
                    st.write("**Due Date**")
                    st.write(row['Due Date'].strftime('%Y-%m-%d'))
                
                with col3:
                    st.write("**Min Payment**")
                    st.write(f"${row['Minimum Payment']:,.2f}")
                
                with col4:
                    st.write("**Current Balance**")
                    st.write(f"${row['Current Balance']:,.2f}")
                
                with col5:
                    st.write("**Status**")
                    if status_color == "error":
                        st.error(status_text)
                    elif status_color == "warning":
                        st.warning(status_text)
                    elif status_color == "info":
                        st.info(status_text)
                    else:
                        st.success(status_text)
                
                with col6:
                    if st.button("💳 Pay", key=f"pay_cal_{idx}"):
                        st.session_state[f'paying_{idx}'] = True
                        st.rerun()
                
                st.divider()
    else:
        st.info("No payments scheduled for the selected view.")

# Tab 4: Alerts & Reminders
with tab4:
    st.header("⚠️ Alerts & Reminders")
    
    alerts = []
    
    # Check for overdue payments
    overdue = st.session_state.accounts[
        (pd.to_datetime(st.session_state.accounts['Due Date']) < pd.Timestamp.now()) &
        (st.session_state.accounts['Status'] == 'Active') &
        (st.session_state.accounts['Current Balance'] > 0)
    ]
    
    if len(overdue) > 0:
        st.error(f"🚨 **URGENT: {len(overdue)} Overdue Payments!**")
        for idx, row in overdue.iterrows():
            days_overdue = (pd.Timestamp.now() - pd.to_datetime(row['Due Date'])).days
            st.write(f"- **{row['Account Name']}**: ${row['Minimum Payment']:,.2f} - Overdue by {days_overdue} days")
        st.divider()
    
    # Check for payments due soon
    due_soon = st.session_state.accounts[
        (pd.to_datetime(st.session_state.accounts['Due Date']) >= pd.Timestamp.now()) &
        (pd.to_datetime(st.session_state.accounts['Due Date']) <= pd.Timestamp.now() + timedelta(days=7)) &
        (st.session_state.accounts['Status'] == 'Active') &
        (st.session_state.accounts['Current Balance'] > 0)
    ]
    
    if len(due_soon) > 0:
        st.warning(f"⏰ **{len(due_soon)} Payments Due Within 7 Days**")
        for idx, row in due_soon.iterrows():
            days_until = (pd.to_datetime(row['Due Date']) - pd.Timestamp.now()).days
            st.write(f"- **{row['Account Name']}**: ${row['Minimum Payment']:,.2f} - Due in {days_until} days ({row['Due Date']})")
        st.divider()
    
    # Check for high utilization
    high_util = st.session_state.accounts[
        (st.session_state.accounts['Utilization %'] > 70) &
        (st.session_state.accounts['Account Type'] == 'Credit Card') &
        (st.session_state.accounts['Status'] == 'Active')
    ]
    
    if len(high_util) > 0:
        st.warning(f"📊 **{len(high_util)} Accounts with High Utilization (>70%)**")
        for idx, row in high_util.iterrows():
            st.write(f"- **{row['Account Name']}**: {row['Utilization %']:.1f}% utilization - Consider paying down balance")
        st.divider()
    
    # Check for reporting dates coming up
    reporting_soon = st.session_state.accounts[
        (pd.to_datetime(st.session_state.accounts['Reporting Date']) >= pd.Timestamp.now()) &
        (pd.to_datetime(st.session_state.accounts['Reporting Date']) <= pd.Timestamp.now() + timedelta(days=5)) &
        (st.session_state.accounts['Status'] == 'Active') &
        (st.session_state.accounts['Utilization %'] > 30)
    ]
    
    if len(reporting_soon) > 0:
        st.info(f"📅 **{len(reporting_soon)} Accounts Reporting Soon (Pay Before Reporting Date to Lower Utilization)**")
        for idx, row in reporting_soon.iterrows():
            days_until = (pd.to_datetime(row['Reporting Date']) - pd.Timestamp.now()).days
            st.write(f"- **{row['Account Name']}**: Reports in {days_until} days ({row['Reporting Date']}) - Current utilization: {row['Utilization %']:.1f}%")
        st.divider()
    
    # Check for accounts without autopay
    no_autopay = st.session_state.accounts[
        (st.session_state.accounts['Autopay Enabled'] == 'No') &
        (st.session_state.accounts['Status'] == 'Active')
    ]
    
    if len(no_autopay) > 0:
        st.info(f"🔄 **{len(no_autopay)} Accounts Without Autopay Enabled**")
        st.write("Consider enabling autopay to avoid missed payments:")
        for idx, row in no_autopay.iterrows():
            st.write(f"- **{row['Account Name']}** ({row['Institution']})")
        st.divider()
    
    # Annual fee reminders
    current_month = pd.Timestamp.now().month
    annual_fee_accounts = st.session_state.accounts[
        (st.session_state.accounts['Annual Fee'] > 0) &
        (pd.to_datetime(st.session_state.accounts['Open Date']).dt.month == current_month)
    ]
    
    if len(annual_fee_accounts) > 0:
        st.info(f"💰 **Annual Fee Alert: {len(annual_fee_accounts)} Account(s)**")
        st.write("These accounts may have annual fees posting this month:")
        for idx, row in annual_fee_accounts.iterrows():
            st.write(f"- **{row['Account Name']}**: ${row['Annual Fee']:.2f} annual fee (Opened {row['Open Date']})")
        st.divider()
    
    if len(overdue) == 0 and len(due_soon) == 0 and len(high_util) == 0:
        st.success("✅ **All Clear!** No urgent alerts at this time.")
        st.balloons()

# Tab 5: Credit Score Insights
with tab5:
    st.header("📊 Credit Score Insights & Optimization")
    
    st.markdown("""
    This section provides insights into factors that affect your credit score and recommendations for improvement.
    """)
    
    # Credit utilization analysis
    st.subheader("💳 Credit Utilization Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Overall Utilization", f"{avg_utilization:.1f}%", 
                 help="Target: Under 30% for good scores, under 10% for excellent scores")
        
        if avg_utilization < 10:
            st.success("🌟 Excellent! Your utilization is optimal.")
        elif avg_utilization < 30:
            st.success("✅ Good! Your utilization is in a healthy range.")
        elif avg_utilization < 50:
            st.warning("⚠️ Consider paying down balances to improve your score.")
        else:
            st.error("🚨 High utilization may significantly impact your credit score.")
    
    with col2:
        # Calculate per-card utilization
        cc_accounts = st.session_state.accounts[st.session_state.accounts['Account Type'] == 'Credit Card']
        high_util_count = len(cc_accounts[cc_accounts['Utilization %'] > 30])
        
        st.metric("Cards Over 30% Utilization", f"{high_util_count} of {len(cc_accounts)}")
        
        if high_util_count == 0:
            st.success("🌟 All cards have healthy utilization!")
        else:
            st.info(f"💡 Focus on paying down the {high_util_count} card(s) with high utilization.")
    
    # Payment history
    st.subheader("📅 Payment History Impact")
    col1, col2, col3 = st.columns(3)
    
    perfect_history = len(st.session_state.accounts[st.session_state.accounts['Payment History'] == '100%'])
    total_accounts = len(st.session_state.accounts)
    
    with col1:
        st.metric("Perfect Payment History", f"{perfect_history}/{total_accounts} accounts")
    with col2:
        ontime_rate = (perfect_history / total_accounts * 100) if total_accounts > 0 else 0
        st.metric("On-Time Payment Rate", f"{ontime_rate:.1f}%")
    with col3:
        if ontime_rate == 100:
            st.success("🌟 Perfect!")
        elif ontime_rate >= 98:
            st.success("✅ Excellent")
        else:
            st.warning("⚠️ Needs Improvement")
    
    # Credit mix
    st.subheader("🎯 Credit Mix Analysis")
    
    credit_mix = st.session_state.accounts.groupby('Account Type').size()
    
    col1, col2 = st.columns(2)
    with col1:
        fig_mix = px.pie(values=credit_mix.values, names=credit_mix.index, 
                        title='Account Type Distribution',
                        hole=0.4)
        st.plotly_chart(fig_mix, use_container_width=True)
    
    with col2:
        st.write("**Credit Mix Breakdown:**")
        for acc_type, count in credit_mix.items():
            st.write(f"- {acc_type}: {count} account(s)")
        
        st.divider()
        has_credit_card = 'Credit Card' in credit_mix
        has_installment = any(x in credit_mix for x in ['Installment Loan', 'Mortgage', 'Personal Loan', 'Auto Loan'])
        
        if has_credit_card and has_installment:
            st.success("✅ Good credit mix with revolving and installment accounts")
        elif has_credit_card:
            st.info("💡 Consider adding an installment loan for better credit mix")
        else:
            st.info("💡 Having both revolving (credit cards) and installment loans helps your score")
    
    # Account age analysis
    st.subheader("⏳ Credit History Length")
    
    avg_age = st.session_state.accounts['Account Age (Months)'].mean()
    oldest_account = st.session_state.accounts['Account Age (Months)'].max()
    newest_account = st.session_state.accounts['Account Age (Months)'].min()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Account Age", f"{avg_age:.0f} months ({avg_age/12:.1f} years)")
    with col2:
        st.metric("Oldest Account", f"{oldest_account:.0f} months ({oldest_account/12:.1f} years)")
    with col3:
        st.metric("Newest Account", f"{newest_account:.0f} months ({newest_account/12:.1f} years)")
    
    if avg_age >= 84:  # 7 years
        st.success("🌟 Excellent credit history length")
    elif avg_age >= 36:  # 3 years
        st.success("✅ Good credit history length")
    elif avg_age >= 12:  # 1 year
        st.info("💡 Building credit history - keep accounts open")
    else:
        st.info("💡 New to credit - time will improve this factor")
    
    # Recommendations
    st.subheader("💡 Personalized Recommendations")
    
    recommendations = []
    
    if avg_utilization > 30:
        recommendations.append("🎯 **Pay down high balances**: Target accounts with >30% utilization first")
    
    if high_util_count > 0:
        recommendations.append(f"💳 **Focus on {high_util_count} card(s)**: These have utilization over 30%")
    
    reporting_this_month = st.session_state.accounts[
        (pd.to_datetime(st.session_state.accounts['Reporting Date']) >= pd.Timestamp.now()) &
        (pd.to_datetime(st.session_state.accounts['Reporting Date']) <= pd.Timestamp.now() + timedelta(days=30))
    ]
    
    if len(reporting_this_month) > 0:
        recommendations.append(f"📅 **{len(reporting_this_month)} account(s) reporting soon**: Pay before reporting date to lower reported balance")
    
    if no_autopay.shape[0] > 0:
        recommendations.append(f"🔄 **Enable autopay on {len(no_autopay)} account(s)**: Never miss a payment")
    
    if not has_installment and has_credit_card:
        recommendations.append("🎯 **Diversify credit mix**: Consider adding an installment loan when appropriate")
    
    if avg_age < 36:
        recommendations.append("⏳ **Keep old accounts open**: Your credit history will strengthen over time")
    
    if len(recommendations) > 0:
        for rec in recommendations:
            st.write(rec)
    else:
        st.success("🌟 Excellent credit management! Keep up the great work!")

# Tab 6: Import/Export
with tab6:
    st.header("💾 Import & Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 Import from CSV")
        st.markdown("""
        Upload a CSV file to import multiple accounts at once. The CSV should contain the following columns:
        - Account Name, Account Type, Institution, Credit Limit, Current Balance, and other fields
        """)
        
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        
        if uploaded_file is not None:
            try:
                imported_df = pd.read_csv(uploaded_file)
                
                st.write("**Preview of imported data:**")
                st.dataframe(imported_df.head(10), use_container_width=True)
                
                st.write(f"**Total rows to import:** {len(imported_df)}")
                
                # Validate required columns
                required_cols = ['Account Name', 'Account Type', 'Institution', 'Credit Limit', 'Current Balance']
                missing_cols = [col for col in required_cols if col not in imported_df.columns]
                
                if len(missing_cols) == 0:
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Confirm Import", use_container_width=True):
                            # Add missing columns with defaults if needed
                            default_values = {
                                'Statement Balance': 0,
                                'Minimum Payment': 0,
                                'Due Date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                                'Statement Date': datetime.now().strftime('%Y-%m-%d'),
                                'Reporting Date': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
                                'Last Payment Date': datetime.now().strftime('%Y-%m-%d'),
                                'Last Payment Amount': 0,
                                'APR': 0,
                                'Rewards Points': 0,
                                'Points Value': 0,
                                'Annual Fee': 0,
                                'Status': 'Active',
                                'Open Date': datetime.now().strftime('%Y-%m-%d'),
                                'Account Number': '****0000',
                                'Credit Bureau': 'Unknown',
                                'Payment History': '100%',
                                'Account Age (Months)': 0,
                                'Autopay Enabled': 'No',
                                'Cashback Rate': '0%',
                                'Notes': ''
                            }
                            
                            for col, default in default_values.items():
                                if col not in imported_df.columns:
                                    imported_df[col] = default
                            
                            # Calculate utilization
                            imported_df['Utilization %'] = imported_df.apply(
                                lambda row: calculate_utilization(row['Current Balance'], row['Credit Limit']), axis=1
                            )
                            
                            # Calculate points dollar value
                            if 'Points Dollar Value' not in imported_df.columns:
                                imported_df['Points Dollar Value'] = imported_df['Rewards Points'] * imported_df['Points Value']
                            
                            # Append to existing data
                            st.session_state.accounts = pd.concat([st.session_state.accounts, imported_df], ignore_index=True)
                            st.success(f"✅ Successfully imported {len(imported_df)} accounts!")
                            st.balloons()
                            st.rerun()
                    
                    with col2:
                        if st.button("❌ Cancel Import", use_container_width=True):
                            st.rerun()
                else:
                    st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
                    st.info("Please ensure your CSV contains at minimum: Account Name, Account Type, Institution, Credit Limit, Current Balance")
                    
            except Exception as e:
                st.error(f"Error reading CSV: {str(e)}")
                st.info("Make sure your CSV is properly formatted with comma-separated values")
    
    with col2:
        st.subheader("📤 Export to CSV")
        
        export_options = st.multiselect(
            "Select account types to export",
            options=st.session_state.accounts['Account Type'].unique(),
            default=st.session_state.accounts['Account Type'].unique()
        )
        
        export_df = st.session_state.accounts[st.session_state.accounts['Account Type'].isin(export_options)]
        
        st.write(f"**Total accounts to export:** {len(export_df)}")
        st.write(f"**Total columns:** {len(export_df.columns)}")
        
        # Create CSV download
        csv_buffer = io.StringIO()
        export_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="⬇️ Download Full CSV",
            data=csv_data,
            file_name=f"credit_accounts_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
            help="Download all account data with all fields"
        )
        
        # Simplified export
        simplified_cols = ['Account Name', 'Account Type', 'Institution', 'Credit Limit', 
                          'Current Balance', 'Due Date', 'APR', 'Status']
        simplified_df = export_df[simplified_cols]
        
        csv_buffer_simple = io.StringIO()
        simplified_df.to_csv(csv_buffer_simple, index=False)
        csv_data_simple = csv_buffer_simple.getvalue()
        
        st.download_button(
            label="⬇️ Download Simplified CSV",
            data=csv_data_simple,
            file_name=f"credit_accounts_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
            help="Download basic account information only"
        )
        
        st.divider()
        
        st.markdown("### 📋 Data Preview")
        st.dataframe(export_df.head(), use_container_width=True)
        
        st.divider()
        
        st.info("💡 **Tip:** You can edit the CSV in Excel or Google Sheets and re-import it to update multiple accounts at once.")
        
        # Export statistics
        st.markdown("### 📊 Export Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Export Size", f"{len(csv_data):,} bytes")
        with col2:
            st.metric("Rows × Columns", f"{len(export_df)} × {len(export_df.columns)}")

# Demo CSV Download
st.divider()
st.header("📁 Demo CSV Template")
st.markdown("Download a demo CSV file with sample data to see the expected format")

demo_csv_data = """Account Name,Account Type,Institution,Credit Limit,Current Balance,Statement Balance,Minimum Payment,Due Date,Statement Date,Reporting Date,Last Payment Date,Last Payment Amount,APR,Rewards Points,Points Value,Annual Fee,Status,Open Date,Account Number,Credit Bureau,Payment History,Account Age (Months),Autopay Enabled,Cashback Rate,Notes
Chase Sapphire Reserve,Credit Card,Chase Bank,10000,2500,2800,84,2025-11-05,2025-10-15,2025-10-20,2025-09-28,3200,19.99,45000,0.015,550,Active,2020-03-15,****1234,All 3,100%,68,Yes,0%,Primary travel card with TSA PreCheck credit
American Express Gold,Credit Card,American Express,15000,4200,4500,135,2025-11-10,2025-10-20,2025-10-25,2025-10-05,4100,21.24,82000,0.012,250,Active,2019-06-22,****5678,All 3,100%,76,Yes,0%,Excellent for dining - 4x points at restaurants
Capital One Venture X,Credit Card,Capital One,10000,3500,3800,105,2025-11-08,2025-10-18,2025-10-23,2025-10-02,3900,18.99,38000,0.020,395,Active,2021-08-05,****9012,All 3,100%,50,Yes,0%,New travel card with lounge access included
Auto Loan - Toyota,Installment Loan,Toyota Financial,28000,15600,15600,485,2025-11-01,2025-10-01,2025-10-05,2025-10-01,485,4.29,0,0.0,0,Active,2023-02-10,****0123,All 3,100%,32,Yes,0%,60-month loan with excellent interest rate
Home Mortgage,Mortgage,Quicken Loans,350000,287000,287000,1847,2025-11-01,2025-10-01,2025-10-05,2025-10-01,1847,3.75,0,0.0,0,Active,2018-07-15,****4567,All 3,100%,87,Yes,0%,30-year fixed rate - refinanced in 2021
"""

st.download_button(
    label="⬇️ Download Demo CSV Template",
    data=demo_csv_data,
    file_name="credit_accounts_demo_template.csv",
    mime="text/csv",
    help="Download this template to see the expected CSV format with sample data"
)

# Footer with tips
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 💡 Quick Tips")
    st.markdown("""
    - Keep utilization under 30%
    - Pay before reporting date
    - Never miss a payment
    - Keep old accounts open
    """)

with col2:
    st.markdown("### 🎯 Score Factors")
    st.markdown("""
    - Payment History (35%)
    - Utilization (30%)
    - Credit Age (15%)
    - Credit Mix (10%)
    - New Credit (10%)
    """)

with col3:
    st.markdown("### 📅 Important Dates")
    st.markdown("""
    - **Due Date**: Payment deadline
    - **Statement Date**: Balance is calculated
    - **Reporting Date**: Balance reports to bureaus
    - Pay before reporting to lower utilization
    """)

st.divider()

# Session info
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**📊 Total Accounts in Database**")
    st.code(f"{len(st.session_state.accounts)} accounts")
with col2:
    st.markdown("**💾 Data Storage**")
    st.code("Session State (In-Memory)")
with col3:
    st.markdown("**🔄 Last Updated**")
    st.code(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

st.markdown("---")
st.markdown("**Credit & Trade Line Manager Pro** | Professional credit account tracking and optimization | © 2025")
