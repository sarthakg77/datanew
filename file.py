import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openai

st.title("Detailed Data Analysis")

# Move the OpenAI API key input to the sidebar
OPENAI_API_KEY = st.sidebar.text_input(label=":key: OpenAI Key:", 
                                       help="Please ensure you have an OpenAI API account with credit.",
                                       type="password")

# Check if the key is provided and set it for openai
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

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

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    # Displaying Customer Analysis Visualizations
    st.subheader("Customer Analysis")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    sns.countplot(data=data, x='gender', ax=ax1)
    ax1.set_title('Distribution by Gender')
    sns.countplot(data=data, x='country', ax=ax2)
    ax2.set_title('Distribution by Country')
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=data, x='churn', ax=ax)
    ax.set_title('Churn Distribution (1: Churned, 0: Retained)')
    st.pyplot(fig)

    # Sales Analysis Visualization
    st.subheader("Sales Analysis")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=data, x='country', y='balance', ax=ax)
    ax.set_title('Balance Distribution by Country')
    st.pyplot(fig)
    
    # Holistic Analysis Section
    st.subheader("Holistic Analysis")
    if st.button("Generate Holistic Analysis"):
        holistic_analysis_prompt = f"""
        Given the bank's customer data, provide a holistic analysis in bullet points:

        1. **Patterns and Trends**:
            - Identify patterns related to customer aging based on balance and credit average.
            - Discover any relationships between credit score, balance, and customer demographics.
            - Examine if a specific country or age group has a distinct pattern in terms of balance or credit score.

        2. **Optimal Balance and Credit Score**:
            - Determine the optimal balance with respect to the average credit score.
            - Consider a specific scenario where the customer is 85 years old with a credit score of 513.
            - Analyze how this might differ if we only consider customers from Germany.

        3. **Sample Size and Distribution**:
            - Evaluate the ideal sample size given that Germany accounts for 56% of the instances.
            - Discuss the significance of having 8014 customers distributed across 12 countries.

        4. **Regression and Correlation Insights**:
            - Elaborate on the potential reasons for customer churn, and if there's any correlation with other variables.
            - Examine correlations present in the data, especially with respect to customers from different countries.

        5. **Dimensionality and Data Points**:
            - Discuss the importance of dimensionality in the dataset.
            - Highlight key data points that provide the most valuable insights.

        6. **Customer Management and Integration**:
            - Describe the components of an integrated customer management system.
            - Discuss how such an integration can enhance customer support and maximize financial worth.

        7. **Data Models and Storage**:
            - Evaluate the efficiency of the data models in place.
            - Discuss the storage and retrieval mechanisms of the data, especially in terms of scalability and accessibility.

        Based on the above, provide a concise analysis that a financial analyst would find valuable.
        """
        holistic_analysis = get_gpt3_summary(holistic_analysis_prompt)
        st.write(holistic_analysis)
else:
    st.write("Please upload a CSV file.")
