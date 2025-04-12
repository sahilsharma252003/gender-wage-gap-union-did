# 📊 Gender Wage Gap & Union Membership – A Difference-in-Differences Study

This project analyzes the impact of union membership on the gender wage gap using the Panel Study of Income Dynamics (PSID) dataset. Using a Difference-in-Differences (DiD) framework, we estimate how joining a union influences wage growth for men and women differently.

---

## 🧠 Objective

To determine whether union membership leads to a greater increase in wages for women than for men — and whether this reduces the gender wage gap.

---

## 🧪 Methodology

- **Dataset**: Panel Study of Income Dynamics (PSID)
- **Approach**: Difference-in-Differences (DiD)
- **Treatment**: Individuals transitioning from non-union to union jobs
- **Control Group**: Individuals remaining non-union
- **Key Variables**: 
  - `realhrwage`: Hourly wage
  - `sex`: Gender identifier
  - `unjob`: Union membership status

---

## 🧾 Files Included

- `did_union_wage_analysis.py`: Python script that:
  - Prepares the panel dataset
  - Applies DiD regression
  - Visualizes results with bar and line plots

- `Econometric case comp.pdf`:  
  Full research report including background, empirical model, results, and policy recommendations.

---

## 📈 Key Results

- Women who joined unions experienced an average wage increase of **$4.80**, while men gained **$1.44**
- DiD regression showed a **statistically significant interaction effect** (p < 0.01)
- Suggests that unions reduce gender-based pay disparities by amplifying women’s wage gains

---

## ⚠️ Note on Data

The `PanelStudyIncomeDynamics.csv` file used in this analysis is not included here due to licensing.  
You must obtain the data directly from the [PSID website](https://psidonline.isr.umich.edu/).

---

## 📄 Citation

This project was conducted as part of the **Econometrics Competition 2025** by team *Fanatiks*.  
Report authored by Sahil Sharma and team.

---

## 🧾 License

For academic and educational use only. Attribution required if reused.

