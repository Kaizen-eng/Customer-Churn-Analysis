# Customer Churn - Data Quality & Exploratory Analysis

**Track:** Data Analytics
**Level:** Beginner-friendly

## Overview
This repository contains a complete workflow for auditing, cleaning, and exploring a customer churn dataset. It was built as a solution for a Data Analytics track assessment.

## Files included
- `customer_churn_sample.csv`: The original, raw dataset.
- `Customer_Churn_Analysis.ipynb`: A Jupyter Notebook containing the data profiling, cleaning steps, exploratory data analysis (EDA), and conclusions.
- `customer_churn_cleaned.csv`: The cleaned dataset ready for modeling or further analysis (Generated after running the notebook).
- `data_dictionary.md`: A detailed description of each feature in the dataset.

## Instructions
1. Make sure you have Python and Jupyter installed.
2. Install the necessary libraries if you haven't already:
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```
3. Open `Customer_Churn_Analysis.ipynb` using Jupyter Notebook, JupyterLab, or VS Code.
4. Run all cells to see the step-by-step cleaning process and the exploratory visualizations.
5. Once executed, the notebook will generate `customer_churn_cleaned.csv`.

## Key Findings
- Data cleaning steps handled missing values (median/mode imputation) and corrected data types.
- Exploratory analysis reveals strong correlations between `ContractType` (e.g., month-to-month) and high churn rates.
