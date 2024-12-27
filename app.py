import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_buy_vs_rent(
    purchase_price, down_payment_percentage, loan_term, interest_rate,
    property_tax_rate, maintenance_cost_rate, annual_rent, rent_increase_rate, annual_appreciation_rate
):
    down_payment = purchase_price * (down_payment_percentage / 100)
    loan_amount = purchase_price - down_payment
    monthly_interest_rate = (interest_rate / 100) / 12
    loan_term_months = loan_term * 12

    # Monthly mortgage payment (using the formula for fixed-rate mortgages)
    monthly_mortgage_payment = (
        loan_amount * monthly_interest_rate * (1 + monthly_interest_rate)**loan_term_months
    ) / ((1 + monthly_interest_rate)**loan_term_months - 1)

    # Annual property tax and maintenance costs
    annual_property_tax = purchase_price * (property_tax_rate / 100)
    annual_maintenance_cost = purchase_price * (maintenance_cost_rate / 100)

    # Calculate costs over the loan term
    total_buying_costs = 0
    total_renting_costs = 0
    property_value = purchase_price

    yearly_buying_costs = []
    yearly_renting_costs = []
    property_values = []

    for year in range(1, loan_term + 1):
        annual_mortgage_cost = monthly_mortgage_payment * 12
        total_buying_costs += annual_mortgage_cost + annual_property_tax + annual_maintenance_cost

        # Update property value with appreciation
        property_value *= (1 + annual_appreciation_rate / 100)

        # Update rent with yearly increase
        annual_rent *= (1 + rent_increase_rate / 100)
        total_renting_costs += annual_rent

        # Append yearly costs and property value for chart
        yearly_buying_costs.append(total_buying_costs)
        yearly_renting_costs.append(total_renting_costs)
        property_values.append(property_value)

    return total_buying_costs, total_renting_costs, property_value, yearly_buying_costs, yearly_renting_costs, property_values

# Streamlit UI
st.title("Buy vs Rent Calculator")

st.header("Enter Property Details")
purchase_price = st.number_input("Purchase Price ($):", min_value=0.0, value=300000.0)
down_payment_percentage = st.number_input("Down Payment (%):", min_value=0.0, max_value=100.0, value=20.0)
loan_term = st.number_input("Loan Term (years):", min_value=1, max_value=30, value=30)
interest_rate = st.number_input("Interest Rate (%):", min_value=0.0, max_value=100.0, value=3.5)
property_tax_rate = st.number_input("Property Tax Rate (%):", min_value=0.0, max_value=10.0, value=1.0)
maintenance_cost_rate = st.number_input("Maintenance Cost Rate (%):", min_value=0.0, max_value=10.0, value=1.0)

st.header("Enter Renting Details")
annual_rent = st.number_input("Annual Rent ($):", min_value=0.0, value=15000.0)
rent_increase_rate = st.number_input("Annual Rent Increase Rate (%):", min_value=0.0, max_value=20.0, value=2.0)

st.header("Enter Market Growth Details")
annual_appreciation_rate = st.number_input("Annual Property Appreciation Rate (%):", min_value=0.0, max_value=20.0, value=3.0)

if st.button("Calculate"):
    total_buying_costs, total_renting_costs, property_value, yearly_buying_costs, yearly_renting_costs, property_values = calculate_buy_vs_rent(
        purchase_price, down_payment_percentage, loan_term, interest_rate,
        property_tax_rate, maintenance_cost_rate, annual_rent, rent_increase_rate, annual_appreciation_rate
    )

    st.subheader("Results")
    st.write(f"Total Costs of Buying Over {loan_term} Years: ${total_buying_costs:,.2f}")
    st.write(f"Total Costs of Renting Over {loan_term} Years: ${total_renting_costs:,.2f}")
    st.write(f"Estimated Property Value After {loan_term} Years: ${property_value:,.2f}")

    if total_buying_costs < total_renting_costs:
        st.success("Buying is better than renting based on the given inputs.")
    else:
        st.warning("Renting is better than buying based on the given inputs.")

    # Plotting the results
    st.subheader("Cost Comparison Over Time")
    fig, ax = plt.subplots()
    years = list(range(1, loan_term + 1))
    ax.plot(years, yearly_buying_costs, label="Buying Costs", linestyle="--")
    ax.plot(years, yearly_renting_costs, label="Renting Costs", linestyle="-")
    ax.plot(years, property_values, label="Property Value", linestyle="-")

    ax.set_xlabel("Years")
    ax.set_ylabel("Cost / Value ($)")
    ax.set_title("Buy vs Rent Analysis")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
