# Warehouse Operations Analytics

End-to-end warehouse operations analytics project using **PostgreSQL, SQL, Python, and Power BI** to analyse productivity, order accuracy, labour utilisation, shift performance, SLA compliance, and operational bottlenecks.

## Project Goal

The aim of this project is to simulate a realistic warehouse operations environment and demonstrate how operational data can be transformed into business insights and management recommendations.

## Business Questions

- Which shifts perform best and worst?
- When does warehouse productivity decline?
- Which warehouse zones generate the most picking errors?
- Are higher workloads associated with lower accuracy?
- Which teams consistently miss productivity targets?
- Where is overtime increasing?
- Are orders being completed within SLA?
- Which days or months create operational bottlenecks?
- Does completed training correlate with improved productivity or accuracy?

## Tech Stack

- **SQL:** PostgreSQL
- **Python:** Pandas, NumPy, Matplotlib
- **BI:** Power BI
- **Version Control:** Git & GitHub

## Project Workflow

```text
Synthetic Warehouse Data
        ↓
      CSV
        ↓
   PostgreSQL
        ↓
      SQL
        ↓
 Python / Pandas
        ↓
 Exploratory Analysis
        ↓
     Power BI
        ↓
 KPI Dashboard
        ↓
Business Recommendations
```

## Planned KPIs

- Units Picked per Labour Hour
- Picking Accuracy %
- Target Achievement %
- SLA Compliance %
- Total Overtime Hours
- Overtime as % of Labour Hours
- Total Units Picked
- Orders Completed
- Picking Error Rate

## Repository Structure

```text
Warehouse-Operations-Analytics/
│
├── README.md
├── .gitignore
├── requirements.txt
│
├── data/
│   ├── raw/
│   └── processed/
│
├── sql/
│   ├── database_setup.sql
│   ├── data_cleaning.sql
│   ├── kpi_analysis.sql
│   ├── shift_analysis.sql
│   └── workforce_analysis.sql
│
├── python/
│   ├── generate_dataset.py
│   └── exploratory_analysis.py
│
├── powerbi/
├── screenshots/
│
└── docs/
    ├── data_dictionary.md
    ├── business_questions.md
    └── insights_and_recommendations.md
```

## Current Status

- [x] Repository structure created
- [x] Business questions defined
- [x] Data model designed
- [x] Starter SQL files created
- [x] Synthetic data generator added
- [ ] Generate warehouse dataset
- [ ] Load data into PostgreSQL
- [ ] Complete SQL KPI analysis
- [ ] Perform Python exploratory analysis
- [ ] Build Power BI dashboard
- [ ] Document business insights and recommendations

## Portfolio Focus

This project is designed to demonstrate:

**SQL • Python • Power BI • KPI Analysis • Operational Analytics • Business Analysis • Data Storytelling**

## Author

**Nikunj Mirajkar**  
Cloud, Platform & Data Engineer  
LinkedIn: https://www.linkedin.com/in/nikunjmirajkar/  
Portfolio: https://nikunjmirajkar.com/
