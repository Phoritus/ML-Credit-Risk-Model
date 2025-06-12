import streamlit as st
import pandas as pd
from prediction_helper import predict_risk

# Set page configuration
st.set_page_config(
    page_title="Lauki Finance - Credit Risk Assessment",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .section-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .info-box {
        background: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header with improved styling
st.markdown('<h1 class="main-header">🏦 Lauki Finance - Credit Risk Assessment</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar for additional info
with st.sidebar:
    st.markdown("### 📊 Risk Assessment Guide")
    st.info("""
    **Key Risk Factors:**
    - Credit History & Payment Behavior
    - Income vs Loan Amount Ratio
    - Existing Loan Obligations
    - Loan Purpose & Type
    """)
    
    st.markdown("### 🎯 Credit Score Scale")
    st.success("🟢 Excellent (750+)")
    st.info("🔵 Good (650-749)")
    st.warning("🟡 Average (500-649)")
    st.error("🔴 Poor (300-499)")

# Main content with improved layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="section-header">👤 Personal Information</div>', unsafe_allow_html=True)
    
    # Personal info inputs with better styling
    age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1, 
                         help="Customer's age in years")
    income = st.number_input("Monthly Income (THB)", min_value=0.0, value=50000.0, step=1000.0, format="%.0f",
                           help="Monthly income in Thai Baht")
    residence_type = st.selectbox("Residence Type", 
                                ["Owned", "Mortgage", "Rented"],
                                help="Type of residence ownership")
    
    st.markdown('<div class="section-header">💳 Credit Information</div>', unsafe_allow_html=True)
    
    avg_dpd = st.number_input("Average Days Past Due (Avg DPD)", min_value=0, value=0, step=1,
                             help="Average number of days past due on previous payments")
    delinquency_ratio = st.number_input("Delinquency Ratio (%)", min_value=0, max_value=100, value=30, step=1,
                                       help="Percentage of accounts with payment delays")
    credit_utilization_ratio = st.number_input("Credit Utilization Ratio (%)", min_value=0, max_value=100, value=30, step=1,
                                              help="Percentage of available credit being used")
    open_loan_accounts = st.number_input("Open Loan Accounts", min_value=0, value=1, step=1,
                                        help="Number of currently active loan accounts")

with col2:
    st.markdown('<div class="section-header">💰 Loan Details</div>', unsafe_allow_html=True)
    
    loan_amount = st.number_input("Loan Amount (THB)", min_value=0.0, value=100000.0, step=5000.0, format="%.0f",
                                 help="Requested loan amount in Thai Baht")
    loan_tenure = st.number_input("Loan Tenure (months)", min_value=1, max_value=360, value=12, step=1,
                                 help="Loan duration in months")
    loan_purpose = st.selectbox("Loan Purpose", 
                               ["Auto", "Home", "Personal", "Education"],
                               help="Primary purpose of the loan")
    loan_type = st.selectbox("Loan Type", 
                            ["Secured", "Unsecured"],
                            help="Whether the loan is backed by collateral")
    
    # Calculated metrics in a nice card
    if income > 0:
        loan_to_income_ratio = loan_amount / income
    else:
        loan_to_income_ratio = 0
    
    st.markdown('<div class="section-header">📊 Calculated Metrics</div>', unsafe_allow_html=True)
    
    # Create metrics display
    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.metric("💵 Loan to Income Ratio", f"{loan_to_income_ratio:.2f}",
                 delta="Higher = More Risk" if loan_to_income_ratio > 5 else "Acceptable Range")
    
    with metric_col2:
        monthly_payment = loan_amount / loan_tenure if loan_tenure > 0 else 0
        st.metric("📅 Est. Monthly Payment", f"฿{monthly_payment:,.0f}")

# Risk calculation section
st.markdown("---")
st.markdown('<div class="section-header">🚀 Risk Assessment</div>', unsafe_allow_html=True)

# Enhanced calculate button
if st.button("🔍 Calculate Credit Risk", type="primary", use_container_width=True):
    with st.spinner("🔄 Analyzing credit risk factors..."):
        # Get prediction results
        probability, credit_score, rating = predict_risk(age, income, loan_amount, loan_tenure,
                                                         avg_dpd, delinquency_ratio, 
                                                         credit_utilization_ratio, open_loan_accounts, 
                                                         residence_type, loan_purpose, loan_type)
    
    # Display results in enhanced cards
    st.success("✅ Risk assessment completed successfully!")
    
    # Main results in three columns
    result_col1, result_col2, result_col3 = st.columns(3)
    
    with result_col1:
        # Color-coded probability
        prob_color = "🔴" if probability > 20 else "🟡" if probability > 10 else "🟢"
        risk_level = "High" if probability > 20 else "Moderate" if probability > 10 else "Low"
        st.metric("🎯 Default Probability", f"{probability:.2f}%", 
                 delta=f"{prob_color} {risk_level} Risk")
    
    with result_col2:
        # Credit score with interpretation
        score_emoji = "🌟" if credit_score > 750 else "⭐" if credit_score > 650 else "💫" if credit_score > 500 else "❌"
        st.metric("📈 Credit Score", f"{credit_score}", 
                 delta=f"{score_emoji} {rating}")
    
    with result_col3:
        # Recommendation
        if probability < 10:
            recommendation = "🟢 Approve"
            rec_color = "success"
        elif probability < 20:
            recommendation = "🟡 Review"
            rec_color = "warning"
        else:
            recommendation = "🔴 Decline"
            rec_color = "error"
        
        if rec_color == "success":
            st.success(f"**Recommendation:** {recommendation}")
        elif rec_color == "warning":
            st.warning(f"**Recommendation:** {recommendation}")
        else:
            st.error(f"**Recommendation:** {recommendation}")

    # Detailed results in expandable sections
    with st.expander("📋 Detailed Input Summary", expanded=False):
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.markdown("**👤 Personal & Credit Information:**")
            st.write(f"• Age: {age} years")
            st.write(f"• Monthly Income: ฿{income:,.0f}")
            st.write(f"• Residence Type: {residence_type}")
            st.write(f"• Average DPD: {avg_dpd} days")
            st.write(f"• Delinquency Ratio: {delinquency_ratio}%")
            st.write(f"• Credit Utilization: {credit_utilization_ratio}%")
            st.write(f"• Open Loan Accounts: {open_loan_accounts}")
        
        with summary_col2:
            st.markdown("**💰 Loan Information:**")
            st.write(f"• Loan Amount: ฿{loan_amount:,.0f}")
            st.write(f"• Loan Tenure: {loan_tenure} months")
            st.write(f"• Loan Purpose: {loan_purpose}")
            st.write(f"• Loan Type: {loan_type}")
            st.write(f"• **Loan to Income Ratio: {loan_to_income_ratio:.2f}**")
            st.write(f"• **Est. Monthly Payment: ฿{monthly_payment:,.0f}**")

    # Risk analysis interpretation
    with st.expander("🧠 AI Risk Analysis & Insights", expanded=True):
        if probability < 5:
            st.success("""
            🟢 **Excellent Credit Profile**
            - Very low default risk
            - Strong repayment capability
            - Recommended for standard terms
            """)
        elif probability < 15:
            st.info("""
            🔵 **Good Credit Profile** 
            - Moderate risk level
            - Generally reliable borrower
            - Consider standard to slightly adjusted terms
            """)
        elif probability < 25:
            st.warning("""
            🟡 **Requires Careful Review**
            - Elevated risk factors present
            - May need additional documentation
            - Consider higher interest rates or collateral
            """)
        else:
            st.error("""
            🔴 **High Risk Profile**
            - Significant default probability
            - Multiple risk factors identified  
            - Recommend decline or require substantial collateral
            """)

# Enhanced footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #1f77b4, #ff7f0e); 
                border-radius: 10px; color: white; margin-top: 2rem;'>
        <h4>🏦 Lauki Finance Credit Risk Assessment System</h4>
        <p>Powered by Advanced AI & Machine Learning | Secure & Reliable</p>
    </div>
    """, 
    unsafe_allow_html=True
)



