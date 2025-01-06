import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def monthly_mortgage_payment(loan_amount, annual_interest_rate, loan_term):
    """Calculate the monthly mortgage payment for a fixed-rate mortgage."""
    monthly_interest_rate = (annual_interest_rate / 100) / 12
    loan_term_months = loan_term * 12

    # Monthly mortgage payment (using the formula for fixed-rate mortgages)
    monthly_payment = (
        loan_amount * monthly_interest_rate * (1 + monthly_interest_rate)**loan_term_months
    ) / ((1 + monthly_interest_rate)**loan_term_months - 1)
    return monthly_payment

def annual_property_expenses(purchase_price, property_tax_rate, maintenance_cost_rate):
    """Calculate the annual property expenses based on the purchase price."""
    annual_property_tax = purchase_price * (property_tax_rate / 100)
    annual_maintenance_cost = purchase_price * (maintenance_cost_rate / 100)
    return annual_property_tax + annual_maintenance_cost

def price_to_rent_ratio(purchase_price, annual_rent):
    """Calculate the price-to-rent ratio based on the purchase price and annual rent."""
    return purchase_price / annual_rent

def net_rental_yield(annual_rent, annual_expenses, purchase_price):
    """Calculate the net rental yield based on the annual rent, expenses, and purchase price."""
    return ((annual_rent - annual_expenses) / purchase_price) * 100

def cash_on_cash_return(annual_rent, annual_expenses, down_payment):
    """Calculate the cash-on-cash return based on the annual rent, expenses, and down payment."""
    return ((annual_rent - annual_expenses) / down_payment) * 100

def dti(monthly_mortgage_payment, annual_income):
    """Calculate the debt-to-income ratio based on the monthly mortgage payment and annual income."""
    return (monthly_mortgage_payment * 12 / annual_income) * 100

def roi(annual_rent, annual_expenses, down_payment):
    """Calculate the Return on Investment (ROI) based on annual rent, expenses, and down payment."""
    net_profit = annual_rent - annual_expenses
    return (net_profit / down_payment) * 100

def calculate_score(price_to_rent, roi_value, net_yield, dti_value):
    """Calculate the total score based on the metrics."""
    score = 0
    # Price-to-Rent Ratio
    if price_to_rent < 15:
        score += 1
    # ROI
    if roi_value > 10:
        score += 1
    # Net Rental Yield
    if net_yield > 5:
        score += 1
    # Debt-to-Income Ratio
    if dti_value < 36:
        score += 1
    return score

def create_2d_heatmap(data_matrix, purchase_prices, annual_rents, current_price, current_rent, title, x_label, y_label):
    """Generate a 2D heatmap to visualize metric performance with a highlighted cell."""
    # Create a DataFrame for better labeling in the heatmap
    df_matrix = pd.DataFrame(data_matrix, index=np.round(annual_rents, 0), columns=np.round(purchase_prices, 0))

    # Find the closest indices to the current values
    closest_price_idx = np.abs(purchase_prices - current_price).argmin()
    closest_rent_idx = np.abs(annual_rents - current_rent).argmin()

    # Generate the heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        df_matrix,
        annot=True,
        fmt=".2f",
        cmap=sns.diverging_palette(133, 10, as_cmap=True),  # Green-Red color scheme
        cbar=True,
        ax=ax,
    )

    # Highlight the current cell
    ax.add_patch(plt.Rectangle((closest_price_idx, closest_rent_idx), 1, 1, fill=False, edgecolor='yellow', lw=3))

    # Set labels and title
    ax.set_title(title, fontsize=14)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    return fig

def create_enhanced_horizontal_bar(score, max_score=4, sections=None, cmap='RdYlGn'):
    """
    Create an enhanced horizontal decision bar with dynamic annotations.
    
    Parameters:
        score (float): The current score to highlight on the bar.
        max_score (int): The maximum score on the scale.
        sections (list): Custom labels for decision ranges. Default is a 5-section scale.
        cmap (str): Colormap for the gradient. Default is 'RdYlGn'.
        
    Returns:
        fig: A matplotlib figure object.
    """
    # Default sections if none are provided
    if sections is None:
        sections = ['Don’t Buy', 'Consider', 'Neutral', 'Lean Buy', 'Strong Buy']
    
    num_sections = len(sections)
    gradient = np.linspace(0, 1, 500)
    gradient = np.vstack((gradient, gradient))

    # Setup the figure
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.imshow(gradient, extent=[0, max_score, -0.5, 0.5], aspect='auto', cmap=cmap)

    # Add a marker for the score
    ax.plot(score, 0, 'k^', markersize=12)  # Marker at the score position
    ax.text(score, 0.8, f'{score}/{max_score}', ha='center', va='bottom', fontsize=12, fontweight='bold', color='black')

    # Add labels for decision ranges
    for i, label in enumerate(sections):
        x = (i + 0.5) * (max_score / num_sections)  # Dynamically space the labels
        ax.text(x, -0.6, label, ha='center', va='center', fontsize=10, color='black')

    # Remove unnecessary elements
    ax.set_xlim(0, max_score)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_frame_on(False)

    ax.set_title('Decision Score', fontsize=14, pad=10)
    return fig

# Streamlit UI
st.title("Buy vs Rent Calculator")

st.header("Enter Property Details")
purchase_price = st.number_input("Purchase Price ($):", min_value=0.0, value=140000.0)
down_payment_percentage = st.number_input("Down Payment (%):", min_value=0.0, max_value=100.0, value=20.0)
loan_term = st.number_input("Loan Term (years):", min_value=1, max_value=30, value=30)
interest_rate = st.number_input("Interest Rate (%):", min_value=0.0, max_value=100.0, value=4.0)
property_tax_rate = st.number_input("Property Tax Rate (%):", min_value=0.0, max_value=10.0, value=0.5)
maintenance_cost_rate = st.number_input("Maintenance Cost Rate (%):", min_value=0.0, max_value=10.0, value=1.5)

st.header("Enter Renting Details")
annual_rent = st.number_input("Annual Rent ($):", min_value=0.0, value=9000.0)
# rent_increase_rate = st.number_input("Annual Rent Increase Rate (%):", min_value=0.0, max_value=20.0, value=2.0)

st.header("Enter Your Financial Details")
annual_income = st.number_input("Annual Income ($):", min_value=0.0, value=60000.0)

# st.header("Enter Market Growth Details")
# annual_appreciation_rate = st.number_input("Annual Property Appreciation Rate (%):", min_value=0.0, max_value=20.0, value=2.0)


if st.button("Calculate"):

    st.subheader("Results")

    # Common Calculations
    down_payment = purchase_price * (down_payment_percentage / 100)
    loan_amount = purchase_price - down_payment
    annual_expenses = annual_property_expenses(purchase_price, property_tax_rate, maintenance_cost_rate)
    monthly_payment = monthly_mortgage_payment(loan_amount, interest_rate, loan_term)

    # Define dynamic ranges for Purchase Price and Annual Rent
    purchase_prices = np.linspace(purchase_price * 0.8, purchase_price * 1.2, 5)  # +/- 20% range
    annual_rents = np.linspace(annual_rent * 0.8, annual_rent * 1.2, 5)           # +/- 20% range

    # Precompute Price-to-Rent Ratio Matrix
    price_to_rent_matrix = np.array([
        [price_to_rent_ratio(price, rent) for price in purchase_prices]
        for rent in annual_rents
    ])

    # Precompute ROI Matrix
    roi_matrix = np.array([
        [
            roi(rent, annual_property_expenses(price, property_tax_rate, maintenance_cost_rate), price * (down_payment_percentage / 100))
            for price in purchase_prices
        ]
        for rent in annual_rents
    ])

    ### Price-to-Rent Ratio ###
    st.markdown("### Price-to-Rent Ratio")
    result_price_to_rent_ratio = price_to_rent_ratio(purchase_price, annual_rent)
    st.write(f"**Value:** {result_price_to_rent_ratio:.2f}")
    st.caption("The Price-to-Rent Ratio helps decide whether to buy or rent a property. A ratio below 15 favors buying, as the cost of purchasing is relatively low compared to renting. A ratio above 20 suggests renting might be better, as buying is significantly more expensive.")

    st.pyplot(create_2d_heatmap(
        data_matrix=price_to_rent_matrix,
        purchase_prices=purchase_prices,
        annual_rents=annual_rents,
        current_price=purchase_price,
        current_rent=annual_rent,
        title="Price-to-Rent Ratio Heatmap",
        x_label="Purchase Price ($)",
        y_label="Annual Rent ($)"
    ))

    ### ROI ###
    st.markdown("### Return on Investment (cash on cash)")
    result_roi = roi(annual_rent, annual_expenses, down_payment)
    st.write(f"**Value:** {result_roi:.2f}%")
    st.caption("ROI measures the profitability of your investment. A higher ROI indicates better returns. For example, an ROI above 8% - 10% is generally considered good for real estate, while a lower ROI may signal a need for further analysis of the investment.")

    st.pyplot(create_2d_heatmap(
        data_matrix=roi_matrix,
        purchase_prices=purchase_prices,
        annual_rents=annual_rents,
        current_price=purchase_price,
        current_rent=annual_rent,
        title="Return on Investment (ROI) Heatmap",
        x_label="Purchase Price ($)",
        y_label="Annual Rent ($)"
    ))

    ### Net Rental Yield ###
    st.markdown("### Net Rental Yield")
    net_yield = net_rental_yield(annual_rent, annual_expenses, purchase_price)
    st.write(f"**Value:** {net_yield:.2f}%")
    st.caption("Net Rental Yield indicates the return on the property's value after covering annual expenses. A yield above 5% is considered favorable.")

    ### Debt-to-Income Ratio (DTI) ###
    st.markdown("### Debt-to-Income Ratio (DTI)")
    debt_to_income = dti(monthly_payment, annual_income)
    st.write(f"**Value:** {debt_to_income:.2f}%")
    st.caption("DTI compares your monthly mortgage payments to your annual income. A DTI below 36% is generally considered healthy.")

    ### Monthly Mortgage Payment ###
    st.markdown("### Monthly Mortgage Payment")
    st.write(f"**Value:** ${monthly_payment:.2f}")
    st.caption("This is your estimated monthly mortgage payment based on the provided loan amount, interest rate, and loan term.")

    # Calculate Score
    total_score = calculate_score(result_price_to_rent_ratio, result_roi, net_yield, debt_to_income)

    # Display Gauge Chart
    st.markdown("### Decision Gauge")
    st.pyplot(create_enhanced_horizontal_bar(total_score))