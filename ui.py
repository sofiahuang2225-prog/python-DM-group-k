# Employee Attrition Risk Prediction System (Streamlit)


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import joblib


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
# DASHBOARD PAGE
# --------------------------------------------------
#dashboard data
database = pd.read_csv("HR-Employee-Attrition.csv") #EDA result

if page == "Dashboard":

    st.title("Employee Attrition Dashboard")
    st.caption("Overview of employee retention risk from last year")
    #------------------------------
    #attrition distributution
    #------------------------------
    col1, col2 = st.columns(2, gap="large") 
    total_employees = len(database)  # number of rows (employees)
    attrition_rate = len(database[database['Attrition'] == 'Yes']) / len(database) * 100  #col2

    with col1:
        st.markdown(
            f"""
            <div class='metric-card'>
            <h4>Total Employees</h4>
            <h1>{total_employees}</h1>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class='metric-card'>
            <h4>Attrition Rate</h4>
            <h1>{attrition_rate:.2f}%</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

   
    st.markdown("---")
    #-----------------------------
    #top factors and visualization
    #-----------------------------
    st.subheader("Key Attrition Insights")

    #create an interactive dropdown to select which factor to visualize
    factor_options = [
        "Job Role Distribution",
        "Years in Current Role Distribution",
        "Monthly Income Distribution",
        "Age Distribution",
        "OverTime Distribution",
        "Stock Option Level Distribution",
        "Education Level Distribution",
        "Job Satisfaction Distribution",
        "Environment Satisfaction Distribution"
    ]
    selected_factor = st.selectbox("Select a factor to see the distribution", factor_options)


    #-----------------------------
    #1. Job Role Distribution
    #-----------------------------
    if selected_factor == "Job Role Distribution":
        fig1 = px.histogram(
            database, 
            x="JobRole",              # X 軸：職務角色
            color="Attrition",         # 顏色區分：是否離職
            barmode="stack",           # 設定為堆疊模式
            title="Attrition Risk by Job Role",
            category_orders={"Attrition": ["No", "Yes"]}, # 讓 Yes 顯示在上方或特定順序
            color_discrete_map={"Yes": "#d62728", "No": "#2ca02c"} # 自訂顏色：紅色代表離職、灰色代表留任
        )
        # 旋轉 X 軸文字角度（避免職務名稱太長重疊）
        fig1.update_layout(xaxis_tickangle=-45, yaxis_title="Head Count")

        fig1.update_layout(height=400)

        st.plotly_chart(fig1, use_container_width=True)

    #-----------------------------
    #2. Years in Current Role Distribution
    #-----------------------------
    elif selected_factor == "Years in Current Role Distribution":
        # 將留任與離職的數據分開成兩個 List
        hist_data = [
            database[database['Attrition'] == "No"]['YearsInCurrentRole'].dropna(),
            database[database['Attrition'] == "Yes"]['YearsInCurrentRole'].dropna()
        ]
        group_labels = ['Stayed', 'Left']
        colors = ['#2ca02c', '#d62728']
            
        # 使用 Figure Factory 繪製 Distplot (包含 KDE 曲線與直方圖)
        # show_hist=False 關閉長條圖，只留下純 KDE 曲線
        fig2 = ff.create_distplot(hist_data, group_labels, show_hist=False, show_rug=False, colors=colors)

        # 更新標題與佈局
        fig2.update_layout(
            title_text='Attrition Risk by Years In Current Role',
            xaxis_title='Years In Current Role',
            yaxis_title='Density',
            template='plotly_white'
        )

        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)

    #-----------------------------
    #3. Monthly Income Distribution
    #-----------------------------
    elif selected_factor == "Monthly Income Distribution":
        hist_data = [
            database[database['Attrition'] == "No"]['MonthlyIncome'].dropna(),
            database[database['Attrition'] == "Yes"]['MonthlyIncome'].dropna()
        ]
        group_labels = ['Stayed', 'Left']
        colors = ['#2ca02c', '#d62728']
                
        fig3 = ff.create_distplot(hist_data, group_labels, show_hist=False, show_rug=False, colors=colors)

        # 更新標題與佈局
        fig3.update_layout(
            title_text='Attrition Risk by Monthly Income',
            xaxis_title='Monthly Income (USD)',
            yaxis_title='Density',
            template='plotly_white'
        )

        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)

    #-----------------------------
    #4. Age Distribution
    #-----------------------------
    elif selected_factor == "Age Distribution":
        fig4 = px.histogram(
            database,
            x="Age",
            color="Attrition",
            barmode="stack",
            title="Attrition Risk by Age",
            category_orders={"Attrition": ["No", "Yes"]},
            color_discrete_map={"Yes": "#d62728", "No": "#2ca02c"}
        )
        fig4.update_layout(height=400, xaxis_title="Age", yaxis_title="Head Count")
        st.plotly_chart(fig4, use_container_width=True)

    #------------------------------
    #5. OverTime Distribution   
    #------------------------------
    elif selected_factor == "OverTime Distribution":
        fig5 = px.histogram(
            database,
            x="OverTime",
            color="Attrition",
            barmode="stack",
            title="Attrition Risk by OverTime",
            category_orders={"Attrition": ["No", "Yes"]},
            color_discrete_map={"Yes": "#d62728", "No": "#2ca02c"}
        )
        fig5.update_layout(height=400, xaxis_title="OverTime", yaxis_title="Head Count")
        st.plotly_chart(fig5, use_container_width=True)

    #-----------------------------
    #6. Stock Option Level Distribution
    #-----------------------------
    elif selected_factor == "Stock Option Level Distribution":
        fig6 = px.histogram(
            database,
            x="StockOptionLevel",
            color="Attrition",
            barmode="stack",
            title="Attrition Risk by Stock Option Level",
            category_orders={"Attrition": ["No", "Yes"]},
            color_discrete_map={"Yes": "#d62728", "No": "#2ca02c"}
        )
        fig6.update_layout(height=400, xaxis_title="Stock Option Level", yaxis_title="Head Count", bargap=0.2)  
        st.plotly_chart(fig6, use_container_width=True)

    #-----------------------------
    #7. Education Level Distribution
    #------------------------------
    elif selected_factor == "Education Level Distribution":
        fig7 = px.histogram(
            database,
            x="Education",
            color="Attrition",
            barmode="stack",
            title="Attrition Risk by Education Level",
            category_orders={"Attrition": ["No", "Yes"]},
            color_discrete_map={"Yes": "#d62728", "No": "#2ca02c"}
        )
        fig7.update_layout(height=400, xaxis_title="Education Level", yaxis_title="Head Count", bargap=0.2)
        st.plotly_chart(fig7, use_container_width=True)

    #-----------------------------
    #8. Job Satisfaction Distribution
    #-----------------------------
    elif selected_factor == "Job Satisfaction Distribution":
        fig8 = px.pie(
            database,
            names="JobSatisfaction",
            color="JobSatisfaction",
            title="Job Satisfaction",
            category_orders={"JobSatisfaction": [1, 2, 3, 4]},
            color_discrete_map={1: "#d62728", 2: "#ff7f0e", 3: "#1f77b4", 4: "#2ca02c"}
        )
        fig8.update_layout(height=400)
        st.plotly_chart(fig8, use_container_width=True)

    #-----------------------------
    #9. Environment Satisfaction Distribution
    #-----------------------------
    elif selected_factor == "Environment Satisfaction Distribution":
        fig9 = px.pie(
        database,
        names="EnvironmentSatisfaction",
        color="EnvironmentSatisfaction",
        title="Environment Satisfaction",
        category_orders={"EnvironmentSatisfaction": [1, 2, 3, 4]},
        color_discrete_map={1: "#d62728", 2: "#ff7f0e", 3: "#1f77b4", 4: "#2ca02c"}
    )
        fig9.update_layout(height=400)
        st.plotly_chart(fig9, use_container_width=True)

    #-----------------------------
    #feature importance visualization
    #-----------------------------
    #載入模型
    model = joblib.load("model_xgb.pkl")

    chosen_factors = ['YearsInCurrentRole','Age','Education','EnvironmentSatisfaction','JobSatisfaction','MonthlyIncome','StockOptionLevel','OverTime']

    # 取得 AutoML 模型的特徵重要度與特徵名稱
    importances = model.feature_importances_
    feature_names = model.feature_names_in_
    # Create a full DataFrame for all feature importances
    importance_df_full = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    })

    # Filter the DataFrame to include only the chosen factors and sort them
    importance_df = importance_df_full[importance_df_full['Feature'].isin(chosen_factors)].sort_values(by='Importance', ascending=False)

    # 繪製選定因素的重要性
    plt.figure(figsize=(10, 8))
    sns.barplot(x='Importance', y='Feature', data=importance_df, palette='viridis')
    plt.title('Impact of Each Factor on Attrition')
    plt.xlabel('Impact')
    plt.ylabel('Features')
    plt.tight_layout()
    fig = plt.gcf()
    st.pyplot(fig)

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
        st.subheader("👤 Employee Profile")
        age = st.slider(    
            "Age",
            18,
            60,
            30
        )

        job_role = st.selectbox(
            "Job Role",
            [
                "Sales Executive",
                "Research Scientist",
                "Laboratory Technician",
                "Manager",
                "Sales Representative",
                "Human Resources",
                "Manufacturing Director",
                "Research Director"
            ]
        )

        Education = st.selectbox(
            "Education Level",
            [
                "Below College",
                "College",
                "Bachelor",
                "Master",
                "Doctor"
            ]
        )

        #transform education level to numeric
        Education_map = {
            "Below College": 1,
            "College": 2,
            "Bachelor": 3,
            "Master": 4,
            "Doctor": 5
        }
        Education = Education_map[Education]

        monthly_income = st.text_input(
            "Monthly Income(USD)\n(enter range 5000-200000)",
            value=5000
        )
        monthly_income = float(monthly_income) if monthly_income else 5000
        if monthly_income:
            try:
                monthly_income = float(monthly_income)
                if monthly_income < 5000 or monthly_income > 200000:
                    st.error("Out of range. Please enter a number between 5000 and 200000.")
            except ValueError:
                st.error("Please enter a valid number")
        else:
            st.error("Please enter a value for Monthly Income.")

        years_current_role = st.slider(
            "Years In Current Role",
            0,
            20,
            2
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

        job_satisfaction = st.slider(
            "Job Satisfaction(1: Low, 4: Very High)",
            1,
            4,
            3
        )

        Environment_satisfaction = st.slider(
            "Environment Satisfaction(1: Low, 4: Very High)",
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



    st.markdown("---")

    # --------------------------------------------------
    # PREDICT BUTTON
    # --------------------------------------------------
    if st.button("🚀 Predict Attrition Risk"):

        # --------------------------------------------------
        # load model and calculate risk score
        # --------------------------------------------------
        #建立defult value和輸入資料
        default_df = pd.read_csv("X_default.csv")
        #將使用者輸入的值替換掉預設值
        input_df = default_df.copy()
        risk_score = model.predict_proba
        
        input_df['Age'] = age

        if job_role == "Sales Executive":
            input_df['JobRole_Sales Executive'] = 1
        elif job_role == "Research Scientist":
            input_df['JobRole_Research Scientist'] = 1
        elif job_role == "Laboratory Technician":
            input_df['JobRole_Laboratory Technician'] = 1
        elif job_role == "Manager":
            input_df['JobRole_Manager'] = 1
        elif job_role == "Sales Representative":
            input_df['JobRole_Sales Representative'] = 1
        elif job_role == "Human Resources":
            input_df['JobRole_Human Resources'] = 1
        elif job_role == "Manufacturing Director":
            input_df['JobRole_Manufacturing Director'] = 1
        elif job_role == "Research Director":
            input_df['JobRole_Research Director'] = 1
        
        input_df['Education'] = Education

        input_df['MonthlyIncome'] = monthly_income

        input_df['YearsInCurrentRole'] = years_current_role
        
        if overtime == "Yes":
            input_df['OverTime'] = 1
       
        input_df['JobSatisfaction'] = job_satisfaction
        
        input_df['EnvironmentSatisfaction'] = Environment_satisfaction
        
        input_df['StockOptionLevel'] = stock_option_level
        
        risk_score = model.predict_proba(input_df)[0][1] * 100


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
                <h1 class='{risk_class}'>{risk_score:.2f}%</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.progress(float(risk_score)/100)

        # --------------------------------------------------
        # RISK FACTORS
        # --------------------------------------------------
        st.subheader("⚠ Main Risk Factors")

        factors = []

        if overtime == "Yes":
            factors.append("Frequent OverTime")

        if monthly_income < 4000:
            factors.append("Low Monthly Income")

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

        if monthly_income < 4000:
            recommendations.append("Review compensation package")

        if years_current_role < 2:
            recommendations.append("Provide onboarding and mentorship")

        if job_satisfaction <= 2:
            recommendations.append("Schedule employee feedback discussion")


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
