import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openai

# Initialize OpenAI with your API key
OPENAI_API_KEY = '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'  # Replace with your API key and remember to keep it secure!
openai.api_key = OPENAI_API_KEY

st.title("Detailed Data Analysis")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

def get_gpt3_summary(prompt):
    """
    Use OpenAI's GPT-3 to generate a summary based on a prompt.
    """
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=250
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.write("Error with OpenAI API call:", str(e))
        return None

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    # Convert 'Date' to datetime and extract month
    data['Date'] = pd.to_datetime(data['Date'])
    data['Month'] = data['Date'].dt.month

    # 1. Customer Behavior:
    payment_distribution = data['Payment'].value_counts(normalize=True) * 100
    most_preferred_payment = payment_distribution.idxmax()
    avg_spend_per_transaction = data['Total'].mean()

    # 2. Sales Analysis:
    product_sales = data.groupby('Product line')['Total'].sum()
    highest_selling_product = product_sales.idxmax()
    lowest_selling_product = product_sales.idxmin()
    total_revenue = data['Total'].sum()

    # 3. Churn Analysis:
    customer_type_distribution = data['Customer type'].value_counts(normalize=True) * 100
    member_percentage = customer_type_distribution['Member']
    avg_products_per_transaction = data['Quantity'].mean()

    # Create a summary for GPT-3
    summary_prompt = f"""
    Provide a summary based on the following information:
    The majority of customers prefer {most_preferred_payment} for transactions, accounting for approximately {payment_distribution[most_preferred_payment]:.2f}% of all transactions. 
    On average, customers spend ${avg_spend_per_transaction:.2f} per transaction. The top-selling product is {highest_selling_product}, 
    while {lowest_selling_product} has the least sales. The total revenue is ${total_revenue:,.2f}. 
    {member_percentage:.2f}% of customers are members. Provide insights and recommendations based on this data.
    """

    # Get summary from GPT-3
    gpt3_summary = get_gpt3_summary(summary_prompt)

    # Displaying the GPT-3 generated summary
    st.write(gpt3_summary)

    # Customer Behavior Analysis Visualizations
    st.subheader("Customer Behavior Analysis")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    sns.countplot(data=data, x='Customer type', ax=ax1)
    ax1.set_title('Distribution by Customer Type')

    sns.countplot(data=data, x='Gender', ax=ax2)
    ax2.set_title('Distribution by Gender')
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=data, x='Payment', ax=ax, order=data['Payment'].value_counts().index)
    ax.set_title('Distribution by Payment Method')
    st.pyplot(fig)

    # Sales Analysis Visualizations
    st.subheader("Sales Analysis")

    # Ensure the 'Total' column is of numeric type
    data['Total'] = pd.to_numeric(data['Total'], errors='coerce')
    sales_data_branch = data.groupby('Branch')['Total'].sum().reset_index()
    sales_data_city = data.groupby('City')['Total'].sum().reset_index()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    sns.barplot(data=sales_data_branch, x='Branch', y='Total', errorbar=None, ax=ax1)
    ax1.set_title('Total Sales per Branch')

    sns.barplot(data=sales_data_city, x='City', y='Total', errorbar=None, ax=ax2)
    ax2.set_title('Total Sales per City')
    st.pyplot(fig)

else:
    st.write("Please upload a CSV file.")
