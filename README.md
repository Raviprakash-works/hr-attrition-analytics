# 📊 HR Employee Attrition Analytics

> End-to-end data analytics project — Python EDA, SQL analysis, and interactive Power BI dashboard to uncover the drivers behind employee attrition.

---

## 🔍 Problem Statement

Employee attrition costs organizations significantly in recruitment, training, and lost productivity. This project analyzes IBM's HR dataset of **1,470 employees** to identify the key factors driving attrition and build an interactive dashboard that helps HR teams take data-backed action.

---

## 📁 Project Structure

```
hr-attrition-analytics/
│
├── data/
│   ├── WA_Fn-UseC_-HR-Employee-Attrition.csv     # Raw dataset (IBM HR)
│   └── hr_attrition_cleaned.csv                   # Cleaned & feature-engineered
│
├── outputs/
│   ├── charts/                                    # 9 EDA charts (PNG)
│   └── data/                                      # SQL-ready summary tables
│       ├── summary_by_department.csv
│       ├── summary_by_jobrole.csv
│       ├── summary_by_tenure.csv
│       └── summary_by_salary.csv
│
├── screenshots/
│   ├── page1-overview.png                         # Dashboard Page 1
│   ├── page2-deepdive.png                         # Dashboard Page 2
│   └── page3-riskprofile.png                      # Dashboard Page 3
│
├── hr_attrition_analysis.py                       # Python EDA script
├── hr_attrition_queries.sql                       # SQL analysis queries
├── HR_Attrition_Analytics_RaviPrakash.pbix        # Power BI dashboard
└── README.md
```

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| **Python** (Pandas, Matplotlib, Seaborn) | Data cleaning, feature engineering, EDA |
| **SQL** (SQLite) | Aggregation queries, cross-analysis |
| **Power BI** | Interactive 3-page dashboard |
| **Excel** | Data source, pivot exploration |

---

## 📊 Dashboard Pages

### Page 1 — Overview
![Overview](screenshots/page1-overview.png)
- Overall attrition rate KPI
- Attrition by Department
- Attrition by Job Role
- Retained vs Attrited donut chart

### Page 2 — Deep Dive
![Deep Dive](screenshots/page2-deepdive.png)
- Attrition by Tenure Band
- Attrition by Salary Band
- Overtime Impact
- Job Satisfaction vs Attrition
- Age Distribution by Attrition

### Page 3 — Risk Profile
![Risk Profile](screenshots/page3-riskprofile.png)
- Interactive slicers (Department, Job Role, Overtime, Tenure)
- KPI cards: Avg Satisfaction, Avg Tenure, Avg Income, Overtime %
- High-risk employee table (filtered: left + overtime + low satisfaction)

---

## 🔑 Key Findings

| # | Finding | Insight |
|---|---------|---------|
| 1 | Overall attrition rate is **16.1%** | Above the healthy 10% benchmark |
| 2 | **Sales Representatives** have 39.8% attrition | Highest of any job role |
| 3 | **0–2 year** employees leave the most (30%+) | Early tenure is the highest-risk window |
| 4 | **Low salary (<$3K/month)** band has ~26% attrition | Compensation is a key driver |
| 5 | Employees working **overtime** are 3x more likely to leave | Work-life balance critical |
| 6 | **Sales department** has 20.6% attrition vs R&D at 13.8% | Department culture matters |
| 7 | Lower job satisfaction correlates directly with higher attrition | Engagement drives retention |

---

## ⚙️ How to Run

### Python EDA
```bash
# Install dependencies
pip install pandas matplotlib seaborn numpy

# Run analysis
python hr_attrition_analysis.py
```
Output: 9 charts in `outputs/charts/` + cleaned CSV in `outputs/data/`

### SQL Queries
```bash
# Import hr_attrition_cleaned.csv into DB Browser for SQLite
# Run hr_attrition_queries.sql
# 11 queries covering attrition by department, role, tenure, salary, overtime
```

### Power BI Dashboard
```
1. Open HR_Attrition_Analytics_RaviPrakash.pbix in Power BI Desktop
2. If prompted, update data source path to your local outputs/data/ folder
3. Refresh data
4. Use slicers on Page 3 to filter by Department, Job Role, Overtime, Tenure
```

---

## 📂 Dataset

- **Source:** [IBM HR Analytics Attrition Dataset](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) via Kaggle
- **Records:** 1,470 employees
- **Features:** 35 columns — demographics, compensation, satisfaction scores, tenure, attrition status
- **License:** Open Database License (ODbL)

---

## 👤 Author

**Ravi Prakash**
- 📧 prakash.ravi.works@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/ravi-prakash-works)
- 🐙 [GitHub](https://github.com/raviprakash-works)
- 🌐 [Portfolio](https://raviprakash-works.github.io)

---

> *This project is part of my data analytics portfolio. Built to demonstrate end-to-end analytical thinking — from raw data to actionable business insights.*
