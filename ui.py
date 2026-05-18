# Employee Attrition Risk Prediction System (Streamlit)


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AttriSight - Employee Retention Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f7fb;
    }

    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e6eaf1;
    }

    .risk-high {
        color: #ff4b4b;
        font-weight: bold;
        font-size: 24px;
    }

    .risk-medium {
        color: #ff9800;
        font-weight: bold;
        font-size: 24px;
    }

    .risk-low {
        color: #00c853;
        font-weight: bold;
        font-size: 24px;
    }

    .recommend-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #6c63ff;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("📊 AttriSight")
st.sidebar.markdown("### Employee Retention Analytics")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Predict Employee Risk",
        "Employee Insights",
        "Recommendations"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "This system predicts employee attrition risk and provides HR recommendations."
)

# --------------------------------------------------
# FAKE DASHBOARD DATA
# --------------------------------------------------
attrition_rate = 16.1
high_risk_employees = 132
average_risk = 24

# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------
if page == "Dashboard":

    st.title("Employee Attrition Dashboard")
    st.caption("Overview of employee retention risk")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class='metric-card'>
            <h4>Total Employees</h4>
            <h1>1470</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class='metric-card'>
            <h4>High Risk Employees</h4>
            <h1>{high_risk_employees}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class='metric-card'>
            <h4>Average Attrition Risk</h4>
            <h1>{average_risk}%</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class='metric-card'>
            <h4>Actual Attrition Rate</h4>
            <h1>{attrition_rate}%</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    col5, col6 = st.columns([2, 1])

    with col5:
        st.subheader("Attrition Risk by Department")

        dept_df = pd.DataFrame({
            'Department': ['Sales', 'R&D', 'HR', 'Marketing', 'Finance'],
            'Risk': [35, 20, 12, 15, 10]
        })

        fig = px.bar(
            dept_df,
            x='Department',
            y='Risk',
            text='Risk'
        )

        fig.update_layout(height=400)

        st.plotly_chart(fig, use_container_width=True)

    with col6:
        st.subheader("Top Risk Factors")

        st.warning("⚠ OverTime")
        st.warning("⚠ Low Monthly Income")
        st.warning("⚠ Long Distance From Home")
        st.warning("⚠ Low Job Involvement")
        st.warning("⚠ Low Work-Life Balance")

# --------------------------------------------------
# PREDICTION PAGE
# --------------------------------------------------
elif page == "Predict Employee Risk":

    st.title("Predict Employee Attrition Risk")
    st.caption("Enter employee information to predict attrition probability")

    st.markdown("---")

    col1, col2 = st.columns(2)

    # --------------------------------------------------
    # LEFT SIDE INPUTS
    # --------------------------------------------------
    with col1:

        st.subheader("👤 Personal Information")

        age = st.slider("Age", 18, 60, 30)

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        marital_status = st.selectbox(
            "Marital Status",
            ["Single", "Married", "Divorced"]
        )

        st.markdown("---")

        st.subheader("💼 Work Information")

        job_role = st.selectbox(
            "Job Role",
            [
                "Sales Executive",
                "Research Scientist",
                "Laboratory Technician",
                "Manager",
                "Sales Representative",
                "Human Resources"
            ]
        )

        monthly_income = st.number_input(
            "Monthly Income",
            min_value=1000,
            max_value=50000,
            value=5000,
            step=500
        )

        years_current_role = st.slider(
            "Years In Current Role",
            0,
            20,
            2
        )

        distance_from_home = st.slider(
            "Distance From Home",
            1,
            50,
            10
        )

    # --------------------------------------------------
    # RIGHT SIDE INPUTS
    # --------------------------------------------------
    with col2:

        st.subheader("🏢 Work Conditions")

        overtime = st.selectbox(
            "OverTime",
            ["No", "Yes"]
        )

        business_travel = st.selectbox(
            "Business Travel",
            [
                "Travel_Rarely",
                "Travel_Frequently",
                "Non-Travel"
            ]
        )

        job_satisfaction = st.slider(
            "Job Satisfaction",
            1,
            4,
            3
        )

        work_life_balance = st.slider(
            "Work Life Balance",
            1,
            4,
            3
        )

        job_involvement = st.slider(
            "Job Involvement",
            1,
            4,
            3
        )

        stock_option_level = st.slider(
            "Stock Option Level",
            0,
            3,
            1
        )

        percent_salary_hike = st.slider(
            "Percent Salary Hike",
            10,
            30,
            15
        )

    st.markdown("---")

    # --------------------------------------------------
    # PREDICT BUTTON
    # --------------------------------------------------
    if st.button("🚀 Predict Attrition Risk"):

        # --------------------------------------------------
        # FAKE MODEL LOGIC
        # Replace this later with ML model
        # --------------------------------------------------
        risk_score = 10

        if overtime == "Yes":
            risk_score += 25

        if monthly_income < 4000:
            risk_score += 20

        if work_life_balance <= 2:
            risk_score += 15

        if job_satisfaction <= 2:
            risk_score += 15

        if distance_from_home > 20:
            risk_score += 10

        if years_current_role < 2:
            risk_score += 10

        if stock_option_level == 0:
            risk_score += 10

        risk_score = min(risk_score, 100)

        # --------------------------------------------------
        # RISK LEVEL
        # --------------------------------------------------
        if risk_score >= 70:
            risk_level = "HIGH RISK"
            risk_class = "risk-high"
        elif risk_score >= 40:
            risk_level = "MEDIUM RISK"
            risk_class = "risk-medium"
        else:
            risk_level = "LOW RISK"
            risk_class = "risk-low"

        st.markdown("# Prediction Result")

        st.markdown(
            f"""
            <div class='metric-card'>
                <h2>{risk_level}</h2>
                <h1 class='{risk_class}'>{risk_score}%</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(risk_score / 100)

        # --------------------------------------------------
        # RISK FACTORS
        # --------------------------------------------------
        st.subheader("⚠ Main Risk Factors")

        factors = []

        if overtime == "Yes":
            factors.append("Frequent OverTime")

        if monthly_income < 4000:
            factors.append("Low Monthly Income")

        if work_life_balance <= 2:
            factors.append("Poor Work-Life Balance")

        if distance_from_home > 20:
            factors.append("Long Distance From Home")

        if job_satisfaction <= 2:
            factors.append("Low Job Satisfaction")

        if years_current_role < 2:
            factors.append("Short Tenure In Current Role")

        if len(factors) == 0:
            st.success("No major risk factors detected")
        else:
            for factor in factors:
                st.error(f"⚠ {factor}")

        # --------------------------------------------------
        # RECOMMENDATIONS
        # --------------------------------------------------
        st.subheader("💡 HR Recommendations")

        recommendations = []

        if overtime == "Yes":
            recommendations.append("Reduce overtime workload")

        if work_life_balance <= 2:
            recommendations.append("Offer flexible work arrangements")

        if monthly_income < 4000:
            recommendations.append("Review compensation package")

        if years_current_role < 2:
            recommendations.append("Provide onboarding and mentorship")

        if job_satisfaction <= 2:
            recommendations.append("Schedule employee feedback discussion")

        if distance_from_home > 20:
            recommendations.append("Consider hybrid or remote work options")

        for rec in recommendations:
            st.markdown(
                f"""
                <div class='recommend-box'>
                ✓ {rec}
                </div>
                """,
                unsafe_allow_html=True
            )

# --------------------------------------------------
# EMPLOYEE INSIGHTS PAGE
# --------------------------------------------------
elif page == "Employee Insights":

    st.title("Employee Insights")

    insight_df = pd.DataFrame({
        'Feature': [
            'OverTime',
            'Monthly Income',
            'Distance From Home',
            'Job Involvement',
            'Work Life Balance'
        ],
        'Impact': [18, 12, 9, 7, 6]
    })

    fig = px.bar(
        insight_df,
        x='Impact',
        y='Feature',
        orientation='h',
        text='Impact'
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "OverTime and Monthly Income are currently the strongest predictors of employee attrition."
    )

# --------------------------------------------------
# RECOMMENDATIONS PAGE
# --------------------------------------------------
elif page == "Recommendations":

    st.title("HR Recommendations")

    st.markdown(
        """
        ## Recommended Retention Strategies

        ### 1. Reduce OverTime Burden
        Employees working overtime are significantly more likely to leave.

        ### 2. Improve Work-Life Balance
        Employees with poor work-life balance show elevated attrition risk.

        ### 3. Compensation Review
        Lower-income employees demonstrate higher attrition probability.

        ### 4. Career Development
        Employees with slow promotion progression may become disengaged.

        ### 5. Hybrid Work Opportunities
        Long commute distance correlates with higher attrition.
        """
    )
