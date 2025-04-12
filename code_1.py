#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
did_analysis.py

This script demonstrates a Difference-in-Differences (DiD) approach to estimate
the causal effect of union entry on wages, separately for men vs. women.

Steps:
1) Load PSID data
2) Identify (wave t-1, wave t) pairs where the individual was non-union at t-1.
   - treated=1 if union at t, control=0 if still non-union at t
3) Compute dwage = wage_post - wage_pre
4) Run a DiD regression: dwage ~ treated + female + treated*female
5) Visualize results
"""

import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import numpy as np

def main():
    
    df = pd.read_csv("PanelStudyIncomeDynamics.csv")  

    
    df = df.sort_values(by=["pernum68", "wave"]).reset_index(drop=True)

    
    df["female"] = df["sex"].apply(lambda x: 1 if x == 2 else 0)

    
    df["union_dummy"] = df["unjob"]

   
    
    if "realhrwage" not in df.columns:
        raise ValueError("Column 'realhrwage' not found. Adjust code to use the correct wage variable.")

    
    records = []
    grouped = df.groupby("pernum68")

    for pid, person_df in grouped:
        person_df = person_df.sort_values("wave").reset_index(drop=True)
        
        # Loop over consecutive observations for this person
        for i in range(1, len(person_df)):
            wave_prev = person_df.loc[i-1, "wave"]
            wave_curr = person_df.loc[i, "wave"]
            
            union_prev = person_df.loc[i-1, "union_dummy"]
            union_curr = person_df.loc[i, "union_dummy"]

            wage_prev = person_df.loc[i-1, "realhrwage"]
            wage_curr = person_df.loc[i, "realhrwage"]

            female_curr = person_df.loc[i, "female"]  
            
            if union_prev == 0:
                
                treated = 1 if union_curr == 1 else 0

                record = {
                    "pernum68":     pid,
                    "wave_pre":     wave_prev,
                    "wave_post":    wave_curr,
                    "female":       female_curr,
                    "treated":      treated,
                    "wage_pre":     wage_prev,
                    "wage_post":    wage_curr
                }
                records.append(record)

    did_df = pd.DataFrame(records)
    print("Number of (pre, post) pairs in DiD dataset:", len(did_df))
    print(did_df.head())

   
    did_df["dwage"] = did_df["wage_post"] - did_df["wage_pre"]

    
    did_df["gender"] = did_df["female"].map({0: "Male", 1: "Female"})

    
    did_df["group"] = did_df["treated"].map({0: "Control", 1: "Treated"})

    
    model = smf.ols("dwage ~ treated + female + treated:female", data=did_df).fit()
    print("\n================ Difference-in-Differences (Wide Format) ================")
    print(model.summary())

    grouped_bar = did_df.groupby(["gender", "group"])["dwage"].mean().reset_index()

    
    x_labels = ["Male-Control", "Male-Treated", "Female-Control", "Female-Treated"]
    mean_values = []
    for gend in ["Male", "Female"]:
        for grp in ["Control", "Treated"]:
            val = grouped_bar.loc[(grouped_bar["gender"]==gend) & (grouped_bar["group"]==grp), "dwage"]
            if len(val) > 0:
                mean_values.append(val.values[0])
            else:
                mean_values.append(np.nan)

    x_positions = np.arange(len(x_labels))
    plt.figure(figsize=(8,6))
    plt.bar(x_positions, mean_values, color=["blue","blue","magenta","magenta"], alpha=0.7)
    plt.xticks(x_positions, x_labels, rotation=15)
    plt.ylabel("Average Wage Change (After - Before)")
    plt.title("Average Wage Change by Gender & Treatment (DiD Setup)")
    plt.tight_layout()
    plt.show()

    
    grouped_line = did_df.groupby(["wave_post", "treated", "female"])["dwage"].mean().reset_index()

    plt.figure(figsize=(8,6))

    
    for f in [0, 1]:  
        for t in [0, 1]:  
            subset = grouped_line[(grouped_line["female"]==f) & (grouped_line["treated"]==t)]
            if len(subset) > 0:
                label = ("Male" if f==0 else "Female") + "-" + ("Control" if t==0 else "Treated")
                
                subset = subset.sort_values("wave_post")
                plt.plot(subset["wave_post"], subset["dwage"], marker='o', label=label)

    plt.title("Mean Wage Change by Wave, Gender, and Treatment (DiD)")
    plt.xlabel("Wave (Post Transition)")
    plt.ylabel("dwage (After - Before)")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
