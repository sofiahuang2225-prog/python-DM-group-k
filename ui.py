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
#載入模型
model = joblib.load("model_xgb.pkl")

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
# creat risk levels to show different colors for differen levels of risk in prediction page
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

    .metric-card h2 {
        margin: 0 0 10px 0;
        font-size: 1.4rem;
    }

    .metric-card h1 {
        margin: 0;
        font-size: 3rem;
    }

    .risk-low {
        color: #1f8a3f !important;
    }

    .risk-medium {
        color: #d4a017 !important;
    }

    .risk-high {
        color: #d13212 !important;
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
database_final = pd.read_csv("final_HR-Employee-Attrition.csv") #model input data

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

    prob = model.predict_proba(database_final)[:, 1]
    
    x = list(range(0, 101))
    y = np.percentile(prob, np.arange(0, 101)) * 100
    df = pd.DataFrame({"x": x, "y": y})

    fig = px.line(
        df,
        x="x",
        y="y",
        title="Attrition Risk Percentiles",
        labels={"x": "Employee Percentile", "y": "Attrition Risk Probability (%)"}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "This cumulative percentile curve plots all employees sorted from the lowest predicted attrition probability to the highest, mapping out the exact mathematical inflection points of the workforce's risk distribution:\n\n"
        "The Baseline Plateau (0 to 75th Percentile): The curve rises gently and linearly from 0% up to 51.23% probability at the 75th percentile mark. This represents the vast majority of stable employees whose baseline attrition metrics remain well-controlled.\n\n"
        "The Volatility Surge (75th to 100th Percentile): Beyond the 75th percentile, the curve undergoes an obvious upward inflection, growing increasingly steep. The final 10% of the workforce (90th to 100th percentile) experiences an absolute spike, skyrocketing aggressively from 74.2% toward nearly 100% attrition probability."
    )

    st.markdown("---")
    #-----------------------------
    #top factors and visualization
    #-----------------------------
    st.subheader("Key Attrition Insights")
    st.caption("With our data analysis and machine learning model, we summarize 10 key factors that contribute to employee attrition.\n\n")
    #create an interactive dropdown to select which factor to visualize
    factor_options = [
        "Job Role Distribution",
        "Years in Current Role Distribution",
        "Monthly Income Distribution",
        "Age Distribution",
        "OverTime Distribution",
        "Stock Option Level Distribution",
        "Education Level Distribution",
        "Business Travel Distribution",
        "Job Satisfaction Distribution",
        "Environment Satisfaction Distribution",

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

        #簡短圖說
        st.info(
            "**Quick Summary**\n\n"
            "**Highest Absolute Attrition:** Found in Sales Executive, Research Scientist, and Laboratory Technician due to large baseline headcounts.\n\n"
            "**Highest Relative Risk:** Sales Representatives and Laboratory Technicians display the highest percentage of turnover, demanding urgent HR workflow intervention.\n\n"
            "**Most Stable Roles:** Managers and Research Directors demonstrate nearly zero attrition, showcasing strong organizational loyalty."

        )

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

        #簡短圖說
        st.info(
            "**Quick Summary**\n\n"
            "**Peak Attrition:** Occurs within the first 0 to 2 years, identifying a critical window for HR onboarding interventions.\n\n"
            "**Retention Zone:** Employees successfully crossing the 2-year threshold enter a highly stable phase with a peak retention rate around 2.5 years.\n\n"
            "**Career Plateau Alert:** A secondary attrition wave emerges at 7 years, suggesting the need for job rotations or promotional advancements to prevent mid-career stagnation."
        )
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

        # 簡短圖說
        st.info(
            "**Quick Summary**\n\n"
            "**Financial Danger Zone:** Attrition peaks aggressively for employees earning below \$4,000 USD, with the highest risk concentrated around $2,500 USD.\n\n"
            "**The Income Sweet Spot:** Crossing the $4,500 USD baseline triggers a strong stabilization effect where retention consistently outpaces turnover.\n\n"
            "**Golden Handcuffs Effect:** High-earning positions over $15,000 USD exhibit near-zero attrition."
        )

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

        # 簡短圖說
        st.info(
            "**Quick Summary**\n\n"
            "**Youth Attrition Peak:** Employees aged **18 to 32** present the highest relative turnover risk, marking a critical demographic that requires tailored engagement strategies.\n\n"
            "**Mid-Career Stabilization:** A strong retention effect stabilizes the workforce starting at age **34**, where organizational loyalty peaks alongside headcount density.\n\n"
            "**Senior Workforce Retention:** Beyond the age of **40**, active turnover drops to minimal levels, indicating exceptionally high career and role stability among senior staff."
        )

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

        # 簡短圖說
        st.info(
            "**Quick Summary**\n\n"
            "Employees who work overtime have a disproportionately high attrition rate.\n\n"
            "Employees who do not work overtime exhibit excellent retention stability representing the vast majority of the workforce."
        )

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

        # 簡短圖說
        st.info(
            "**Quick Summary**\n\n"
            "**Equity Vulnerability Peak:** Employees with no equity incentives (Level 0) exhibit the highest absolute and relative turnover risk.\n\n"
            "**The Optimal Incentive Sweet Spot:** Employees with Level 1 equity incentives have much higher retention than level 0, drastically slashing the attrition ratio.\n\n"
            "**Perfect Retention:** Level 2 and 3 equity demonstrate near-perfect retention stability, securing absolute talent lock-in."
        )

    #-----------------------------
    #7. Education Level Distribution
    #------------------------------
    elif selected_factor == "Education Level Distribution":
        database['Education'] = database['Education'].replace({
            1:"Below College",
            2:"College",
            3:"Bachelor",
            4:"Master",
            5:"Doctor"
        })
        fig7 = px.histogram(
            database,
            x="Education",
            color="Attrition",
            barmode="stack",
            title="Attrition Risk by Education Level",
            category_orders={
                "Education": ["Below College", "College", "Bachelor", "Master", "Doctor"],
                "Attrition": ["No", "Yes"]},
            color_discrete_map={"Yes": "#d62728", "No": "#2ca02c"}
        )
        fig7.update_layout(height=400, xaxis_title="Education Level", yaxis_title="Head Count", bargap=0.2)
        st.plotly_chart(fig7, use_container_width=True)

        # 簡短圖說
        st.info(
            "**Quick Summary**\n\n"
            "The absolute vast majority of the company's workforce is heavily concentrated in the Bachelor and Master tiers, holding well over 900 employees combined. While the Bachelor category shows the highest total volume of resignations (the largest red block) due to its massive baseline size, the proportional visual ratio of attrition stays visually modest and uniform across these middle categories.The Extremes: Below College and College levels represent steady operational workforces with low baseline counts. At the furthest right, Doctor represents a tiny micro-population (around 50 staff members) displaying an almost entirely green column, visually indicating exceptional baseline retention.\n\n"
            "**★Machine Learning Model Insight:** Please note a crucial divergence—while this chart visually shows high retention for advanced degrees due to low absolute headcounts, our **XGBoost model identifies that higher education levels actually carry an elevated risk of attrition** once other compounding variables are held constant."
        )

    #-----------------------------
    #8. Business Travel Distribution
    #-----------------------------
    elif selected_factor == "Business Travel Distribution":
        fig8 = px.histogram(
            database,
            x="BusinessTravel",
            color="Attrition",
            barmode="stack",
            title="Attrition Risk by Business Travel Frequency",
            category_orders={"Attrition": ["No", "Yes"]},
            color_discrete_map={"Yes": "#d62728", "No": "#2ca02c"}
        )
        fig8.update_layout(height=400, xaxis_title="Business Travel Frequency", yaxis_title="Head Count", bargap=0.2)
        st.plotly_chart(fig8, use_container_width=True)

        st.info(
            "**Quick Summary**\n\n"
            " Employees who **Travel_Frequently** exhibit the highest relative attrition ratio(33.17%). The vast majority of the company falls under **Travel_Rarely** and has 17.59% attrition rate. The **Non-Travel** demographic shows only 8.70%  attrition rate.\n\n"
        )

    #-----------------------------
    #9. Job Satisfaction Distribution
    #-----------------------------
    elif selected_factor == "Job Satisfaction Distribution":
        fig9 = px.pie(
            database,
            names="JobSatisfaction",
            color="JobSatisfaction",
            title="Job Satisfaction",
            category_orders={"JobSatisfaction": [1, 2, 3, 4]},
            color_discrete_map={1: "#d62728", 2: "#ff7f0e", 3: "#1f77b4", 4: "#2ca02c"}
        )
        fig9.update_layout(height=400)
        st.plotly_chart(fig9, use_container_width=True)

        # 簡短圖說
        st.info(
            "**Quick Summary**\n\n"
            "**Positive Workforce Core:** Over **61%** of employees report high to maximum job satisfaction (Levels 3 & 4), serving as the organization's stable cultural anchor.\n\n"
            "**The Dissatisfaction Undercurrent:** Nearly **39%** of the workforce operates under suboptimal satisfaction (Levels 1 & 2), marking a highly vulnerable retention segment.\n\n"
            "**Early-Warning Indicator:** Employees scoring **Level 1 and 2** in satisfaction are heavily weighted by the XGBoost model as prime candidates for active turnover risk."
        )

    #-----------------------------
    #10. Environment Satisfaction Distribution
    #-----------------------------
    elif selected_factor == "Environment Satisfaction Distribution":
        fig10 = px.pie(
            database,
            names="EnvironmentSatisfaction",
            color="EnvironmentSatisfaction",
            title="Environment Satisfaction",
            category_orders={"EnvironmentSatisfaction": [1, 2, 3, 4]},
            color_discrete_map={1: "#d62728", 2: "#ff7f0e", 3: "#1f77b4", 4: "#2ca02c"}
        )
        fig10.update_layout(height=400)
        st.plotly_chart(fig10, use_container_width=True)

        # 簡短圖說
        st.info(
            "**Quick Summary**\n\n"
            " Over **61%** of employees express strong satisfaction with their working environment (Levels 3 & 4) while nearly **39%** of staff experience poor environmental satisfaction (Levels 1 & 2), identifying teams that require facility or cultural audits."
        )

    st.markdown("---")

    #-----------------------------
    #feature importance visualization
    #-----------------------------

    factor_options = list(model.feature_names_in_)
    # Keys for session_state widgets
    select_all_key = "select_all_factors"
    multiselect_key = "chosen_factors_multiselect"

    # Initialize session state defaults
    if select_all_key not in st.session_state:
        st.session_state[select_all_key] = True
    if multiselect_key not in st.session_state:
        st.session_state[multiselect_key] = factor_options.copy() if st.session_state[select_all_key] else []

    # Checkbox to toggle select-all behavior. When checked, ensure the multiselect contains all options.
    select_all = st.checkbox("Select all factors", value=st.session_state[select_all_key], key=select_all_key)
    if select_all and set(st.session_state.get(multiselect_key, [])) != set(factor_options):
        st.session_state[multiselect_key] = factor_options.copy()

    # Multiselect shows current selection from session_state (editable even if select-all is active)
    chosen_factors = st.multiselect(
        'Choose factors to visualize',
        options=factor_options,
        default=st.session_state.get(multiselect_key, []),
        key=multiselect_key
    )

    # If user deselects any item while select-all was active, clear the checkbox
    if st.session_state.get(select_all_key) and set(chosen_factors) != set(factor_options):
        st.session_state[select_all_key] = False

    # 取得 AutoML 模型的特徵重要度與特徵名稱
    importances = model.feature_importances_
    feature_names = model.feature_names_in_
    # Create a full DataFrame for all feature importances
    importance_df_full = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    })

    if not chosen_factors:
        st.warning('Please select at least one factor to visualize.')
    else:
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
        age = st.text_input(
            "Age(18-60)",
            value=""
        )

        job_role = st.selectbox(
            "Job Role",
            [
                "Select job role",
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

        years_current_role = st.text_input(
            "Years In Current Role(0-20)",
            value=""
        )

        Education = st.selectbox(
            "Education Level",
            [
                "Select education level",
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
        if Education != "Select education level":
            Education = Education_map[Education]

        monthly_income = st.text_input(
            "Monthly Income(USD)\n(enter range 2000-200000)",
            value=""
        )

    # --------------------------------------------------
    # RIGHT SIDE INPUTS
    # --------------------------------------------------
    with col2:

        st.subheader("🏢 Work Conditions")

        overtime = st.selectbox(
            "OverTime",
            ["Select overtime", "No", "Yes"]
        )

        businesstravel_frequency = st.selectbox(
            "Business Travel Frequency",
            ["Select travel frequency", "Non Travel", "Travel Rarely", "Travel Frequently"]
        )

        job_satisfaction = st.text_input(
            "Job Satisfaction(1: Low, 4: Very High)",
            value=""
        )

        Environment_satisfaction = st.text_input(
            "Environment Satisfaction(1: Low, 4: Very High)",
            value=""
        )

        stock_option_level = st.text_input(
            "Stock Option Level (0-3)",
            value=""
        )


    # --------------------------------------------------
    # validate user input
    # --------------------------------------------------
    validation_errors = []

    if job_role == "Select job role":
        validation_errors.append("Job Role")
    if Education == "Select education level":
        validation_errors.append("Education Level")
    if overtime == "Select overtime":
        validation_errors.append("OverTime")
    if businesstravel_frequency == "Select travel frequency":
        validation_errors.append("Business Travel Frequency")

    try:
        age = int(age)
        if age < 18 or age > 60:
            validation_errors.append("Age must be between 18 and 60")
    except ValueError:
        if age.strip() == "":
            validation_errors.append("Age")
        else:
            validation_errors.append("Age must be a valid integer")

    try:
        years_current_role = int(years_current_role)
        if years_current_role < 0 or years_current_role > 20:
            validation_errors.append("Years In Current Role must be between 0 and 20")
    except ValueError:
        if years_current_role.strip() == "":
            validation_errors.append("Years In Current Role")
        else:
            validation_errors.append("Years In Current Role must be a valid integer")

    try:
        monthly_income = float(monthly_income)
        if monthly_income < 2000 or monthly_income > 200000:
            validation_errors.append("Monthly Income must be between 2000 and 200000")
    except ValueError:
        if monthly_income.strip() == "":
            validation_errors.append("Monthly Income")
        else:
            validation_errors.append("Monthly Income must be a valid number")

    try:
        job_satisfaction = int(job_satisfaction)
        if job_satisfaction < 1 or job_satisfaction > 4:
            validation_errors.append("Job Satisfaction must be between 1 and 4")
    except ValueError:
        if job_satisfaction.strip() == "":
            validation_errors.append("Job Satisfaction")
        else:
            validation_errors.append("Job Satisfaction must be a valid integer")

    try:
        Environment_satisfaction = int(Environment_satisfaction)
        if Environment_satisfaction < 1 or Environment_satisfaction > 4:
            validation_errors.append("Environment Satisfaction must be between 1 and 4")
    except ValueError:
        if Environment_satisfaction.strip() == "":
            validation_errors.append("Environment Satisfaction")
        else:
            validation_errors.append("Environment Satisfaction must be a valid integer")

    try:
        stock_option_level = int(stock_option_level)
        if stock_option_level < 0 or stock_option_level > 3:
            validation_errors.append("Stock Option Level must be between 0 and 3")
    except ValueError:
        if stock_option_level.strip() == "":
            validation_errors.append("Stock Option Level")
        else:
            validation_errors.append("Stock Option Level must be a valid integer")

    if validation_errors:
        st.error("Please complete all fields correctly before prediction: " + ", ".join(validation_errors))
        st.stop()


    # --------------------------------------------------
    # calculate risk score
    # --------------------------------------------------
    #建立defult value和輸入資料
    default_df = pd.read_csv("X_default.csv")
    #所有必田項目的default value都是0
    #將使用者輸入的值替換掉預設值
    input_df = default_df.copy()
        
    input_df['Age'] = age

    input_df[f'JobRole_{job_role}'] = 1
        
    input_df['Education'] = Education

    input_df['MonthlyIncome'] = monthly_income

    input_df['YearsInCurrentRole'] = years_current_role
        
    if overtime == "Yes":
        input_df['OverTime'] = 1
       
    input_df['JobSatisfaction'] = job_satisfaction
        
    input_df['EnvironmentSatisfaction'] = Environment_satisfaction
        
    input_df['StockOptionLevel'] = stock_option_level

    if businesstravel_frequency == "Travel Rarely":
        input_df['BusinessTravel_Travel_Rarely'] = 1
    elif businesstravel_frequency == "Travel Frequently":
        input_df['BusinessTravel_Travel_Frequently'] = 1

    # --------------------------------------------------
    # ADVANCED SETTINGS (for higher accuracy demands to adjust the rest of the features)
    # --------------------------------------------------
    with st.expander("⚙️ Advanced Settings", expanded=False):

        col3, col4 = st.columns(2)
        #--------------------------------------------------
        #LEFT SIDE ADVANCED SETTINGS
        #--------------------------------------------------
        with col3:

            gender = st.selectbox(
                "Gender",
                ["Male", "Female"]
            )
            
            marital_status = st.selectbox(
                "Marital Status",
                [ "Married","Single","Divorced"]
            )

            distance_from_home = st.slider(
                "Distance From Home (miles)",
                min_value=0,
                max_value=50,
                value=10
            )

            work_life_balance = st.slider(
                "Work Life Balance (1: Bad, 4: Best)",
                min_value=1,
                max_value=4,
                value=2
            )

            education_field = st.selectbox(
                "Education Field",
                [
                    "Life Sciences",
                    "Medical",
                    "Marketing",
                    "Technical Degree",
                    "Human Resources",
                    "Other"
                ]
            )

            department = st.selectbox(
                "Department",
                [
                    "Research & Development",
                    "Sales",
                    "Human Resources"
                ]
            )

            relationship_satisfaction = st.slider(
                "Relationship Satisfaction",
                min_value = 1,
                max_value = 4,
                value = 3
            )

            num_companies_worked = st.slider(
                "Number of Companies Worked",
                min_value = 0,
                max_value = 10,
                value = 2
            )

        with col4:

            promotion_stagnation = st.number_input(
                "Promotion Stagnation(Years Since Last Promotion/Years at Company,0.0-1.0)",
                min_value = 0.0,
                max_value = 1.0,
                value = 0.0
            )

            company_tenure_ratio = st.number_input(
                "Company Tenure Ratio (Years at Company / Total Working Years,0.0-1.0)",
                min_value = 0.0,
                max_value = 1.0,
                value = 0.0
            )

            income_per_year_exp = st.slider(
                "Income Per Year of Experience (Monthly Income / Total Working Years)",
                min_value = 0,
                max_value = 2500,
                value = 549
            )

            percent_salary_hike = st.slider(
                "Percent Salary Hike",
                min_value = 0,
                max_value = 30,
                value = 15
            )

            training_times_last_year = st.slider(
                "Training Times Last Year",
                min_value = 0,
                max_value = 6,
                value = 3
            )

            job_involvement = st.slider(
                "Job Involvement (1: Low, 4: High)",
                min_value = 1,
                max_value = 4,
                value = 3
            )

            performance_rating = st.slider(
                "Performance Rating (1: Low, 4: Excellent)",
                min_value = 1,
                max_value = 4,
                value = 3
            )

        # Update input_df with advanced settings    #advanced settings features
        if gender == "Male":
            input_df['Gender_Male'] = 1
        elif gender == "Female":
            input_df['Gender_Male'] = 0
        
        if marital_status == "Married":
            input_df['MaritalStatus_Married'] = 1
        elif marital_status == "Single":
            input_df['MaritalStatus_Single'] = 1
            input_df['MaritalStatus_Married'] = 0
        elif marital_status == "Divorced":
            input_df['MaritalStatus_Single'] = 0
            input_df['MaritalStatus_Married'] = 0

        input_df['DistanceFromHome'] = distance_from_home

        input_df['WorkLifeBalance'] = work_life_balance

        if education_field != "Other":
            input_df[f'EducationField_{education_field}'] = 1
            input_df['EducationField_Other'] = 0

        if department != "Research & Development":
            input_df[f'Department_{department}'] = 1
            input_df['Department_Research & Development'] = 0

        input_df['RelationshipSatisfaction'] = relationship_satisfaction

        input_df['NumCompaniesWorked'] = num_companies_worked

        input_df['PromotionStagnation'] = promotion_stagnation

        input_df['CompanyTenureRatio'] = company_tenure_ratio

        input_df['IncomePerYearExp'] = income_per_year_exp

        input_df['PercentSalaryHike'] = percent_salary_hike

        input_df['TrainingTimesLastYear'] = training_times_last_year

        input_df['JobInvolvement'] = job_involvement

        input_df['PerformanceRating'] = performance_rating

    risk_score = model.predict_proba(input_df)[0][1] * 100

    st.markdown("---")


    # --------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------
    if risk_score >= 74.197:  #90%的百分位數
        risk_level = "HIGH RISK"
        risk_class = "risk-high"
    elif risk_score >= 51.23:  # 75%的百分位數
        risk_level = "MEDIUM RISK"
        risk_class = "risk-medium"
    else:
        risk_level = "LOW RISK"
        risk_class = "risk-low"

    st.markdown("# Prediction Result")

    st.markdown(
        f"""
        <div class='metric-card'>
            <h2 class='{risk_class}'>{risk_level}</h2>
            <h1 class='{risk_class}'>{risk_score:.2f}%</h1>
            <p>Attrition Risk Percentiles</p>
        </div>
        """,
        unsafe_allow_html=True
    )
        
    st.progress(float(risk_score)/100,)

    # --------------------------------------------------
    # RISK FACTORS
    # --------------------------------------------------
    st.subheader("⚠ Main Risk Factors")

    factors = []

    if overtime == "Yes":
        factors.append("Frequent OverTime")

    if monthly_income < 4000:
        factors.append("Low Monthly Income")

    if stock_option_level == 0:
        factors.append("No Stock Option")

    if job_satisfaction <= 2:
        factors.append("Low Job Satisfaction")

    if Environment_satisfaction <= 2:
        factors.append("Low Environment Satisfaction")

    if years_current_role < 2:
        factors.append("Short Tenure In Current Role")
    elif years_current_role == 7:
        factors.append("Stagnation In Current Role")

    if businesstravel_frequency == "Travel Frequently":
        factors.append("Frequent Business Travel")

    if risk_class == "risk-high" and (Education in [4,5]):
        factors.append("High Education Level")  
        #如dashboard的education level distribution註解，高學歷在高風險時更有機會轉職，可以建議HR先處理

    if len(factors) == 0:
        st.success("No major risk factors detected")
    else:
        for factor in factors:
            st.error(f"⚠ {factor}")

    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------
    st.subheader("💡 HR Recommendations")
    st.caption(
        "Based on the main risk factors, here are some recommendations to improve employee retention.\n\n"
        "For more information, please refer to the dashboard's feature importance analysis"
    )
    recommendations = []

    if overtime == "Yes":
        recommendations.append("Reduce overtime workload")

    if monthly_income < 4000 or stock_option_level == 0:
        recommendations.append("Review compensation package")

    if years_current_role < 2:
        recommendations.append("Provide onboarding and mentorship")

    if years_current_role == 7:
        recommendations.append("Provide career development opportunities")

    if job_satisfaction <= 2:
        recommendations.append("Schedule employee feedback discussion")

    if Environment_satisfaction <2:
        recommendations.append("Enhance working environment")


    for rec in recommendations:
        st.markdown(
            f"""
            <div class='recommend-box'>
            ✓ {rec}
            </div>
            """,
            unsafe_allow_html=True
        )


