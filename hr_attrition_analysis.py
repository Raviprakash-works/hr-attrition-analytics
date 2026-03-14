"""
=============================================================
HR Employee Attrition Analytics
IBM HR Dataset — Full EDA & Analysis Pipeline
=============================================================
Author : Ravi Prakash
Dataset: IBM HR Analytics Attrition Dataset (Kaggle)
Tools  : Python, Pandas, Matplotlib, Seaborn
Output : Cleaned CSV + charts (PNG) for Power BI & portfolio
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')

# ── Output folder ──────────────────────────────────────────
os.makedirs('outputs/charts', exist_ok=True)
os.makedirs('outputs/data',   exist_ok=True)

# ── Style ──────────────────────────────────────────────────
ACCENT   = '#c8f53a'
BG       = '#0f0f0f'
SURFACE  = '#1a1a1a'
TEXT     = '#edebe4'
MUTED    = '#888880'
PALETTE  = ['#c8f53a', '#4da6ff', '#ff6b6b', '#ffd93d', '#6bcb77', '#ff922b']

plt.rcParams.update({
    'figure.facecolor' : BG,
    'axes.facecolor'   : SURFACE,
    'axes.edgecolor'   : '#2a2a2a',
    'axes.labelcolor'  : MUTED,
    'axes.titlecolor'  : TEXT,
    'xtick.color'      : MUTED,
    'ytick.color'      : MUTED,
    'text.color'       : TEXT,
    'grid.color'       : '#222222',
    'grid.linestyle'   : '--',
    'grid.alpha'       : 0.5,
    'font.family'      : 'monospace',
    'axes.spines.top'  : False,
    'axes.spines.right': False,
})

def save(name):
    path = f'outputs/charts/{name}.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f'  ✓ Saved {path}')


# ═══════════════════════════════════════════════════════════
# 1. LOAD & INSPECT
# ═══════════════════════════════════════════════════════════
print('\n' + '═'*55)
print('  STEP 1 — Load & Inspect')
print('═'*55)

df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')

print(f'  Shape      : {df.shape[0]} rows × {df.shape[1]} columns')
print(f'  Nulls      : {df.isnull().sum().sum()}')
print(f'  Duplicates : {df.duplicated().sum()}')
print(f'\n  Columns:\n  {list(df.columns)}')
print(f'\n  Attrition counts:\n{df["Attrition"].value_counts()}')


# ═══════════════════════════════════════════════════════════
# 2. CLEAN & ENGINEER FEATURES
# ═══════════════════════════════════════════════════════════
print('\n' + '═'*55)
print('  STEP 2 — Clean & Feature Engineering')
print('═'*55)

# Drop constant columns (no analytical value)
drop_cols = ['EmployeeCount', 'EmployeeNumber', 'Over18', 'StandardHours']
df.drop(columns=drop_cols, inplace=True)
print(f'  Dropped constant columns: {drop_cols}')

# Binary encode Attrition & OverTime
df['AttritionBinary'] = (df['Attrition'] == 'Yes').astype(int)
df['OverTimeBinary']  = (df['OverTime']  == 'Yes').astype(int)

# Tenure bands
df['TenureBand'] = pd.cut(
    df['YearsAtCompany'],
    bins=[0, 2, 5, 10, 20, 40],
    labels=['0–2 yrs', '3–5 yrs', '6–10 yrs', '11–20 yrs', '20+ yrs'],
    right=True
)

# Age bands
df['AgeBand'] = pd.cut(
    df['Age'],
    bins=[17, 25, 35, 45, 60],
    labels=['18–25', '26–35', '36–45', '46–60']
)

# Salary bands (MonthlyIncome in USD)
df['SalaryBand'] = pd.cut(
    df['MonthlyIncome'],
    bins=[0, 3000, 6000, 10000, 20000],
    labels=['Low (<3K)', 'Mid (3–6K)', 'High (6–10K)', 'Very High (10K+)']
)

# Satisfaction score (average of 4 satisfaction metrics)
df['SatisfactionScore'] = df[[
    'JobSatisfaction', 'EnvironmentSatisfaction',
    'RelationshipSatisfaction', 'WorkLifeBalance'
]].mean(axis=1).round(2)

print(f'  New columns added: TenureBand, AgeBand, SalaryBand, SatisfactionScore, AttritionBinary, OverTimeBinary')
print(f'  Final shape: {df.shape}')

# Save cleaned data
df.to_csv('outputs/data/hr_attrition_cleaned.csv', index=False)
print('  ✓ Saved outputs/data/hr_attrition_cleaned.csv')


# ═══════════════════════════════════════════════════════════
# 3. KEY METRICS SUMMARY
# ═══════════════════════════════════════════════════════════
print('\n' + '═'*55)
print('  STEP 3 — Key Metrics')
print('═'*55)

total       = len(df)
attrited    = df['AttritionBinary'].sum()
rate        = attrited / total * 100
avg_age     = df['Age'].mean()
avg_tenure  = df['YearsAtCompany'].mean()
avg_income  = df['MonthlyIncome'].mean()
overtime_pct= df['OverTimeBinary'].mean() * 100

print(f'  Total Employees   : {total:,}')
print(f'  Left (Attrited)   : {attrited} ({rate:.1f}%)')
print(f'  Avg Age           : {avg_age:.1f} years')
print(f'  Avg Tenure        : {avg_tenure:.1f} years')
print(f'  Avg Monthly Income: ${avg_income:,.0f}')
print(f'  Work Overtime     : {overtime_pct:.1f}% of employees')


# ═══════════════════════════════════════════════════════════
# 4. VISUALISATIONS
# ═══════════════════════════════════════════════════════════
print('\n' + '═'*55)
print('  STEP 4 — Generating Charts')
print('═'*55)

# ── Chart 1: Overall Attrition Donut ───────────────────────
fig, ax = plt.subplots(figsize=(6,6))
sizes  = [total - attrited, attrited]
labels = [f'Retained\n{total - attrited}', f'Attrited\n{attrited}']
colors = [PALETTE[0], PALETTE[2]]
wedges, texts = ax.pie(sizes, labels=labels, colors=colors,
                       startangle=90, wedgeprops=dict(width=0.55))
ax.set_title(f'Overall Attrition Rate: {rate:.1f}%', fontsize=14, fontweight='bold', pad=20)
for t in texts:
    t.set_fontsize(11)
save('01_attrition_donut')

# ── Chart 2: Attrition by Department ───────────────────────
dept_attr = df.groupby('Department')['AttritionBinary'].mean().sort_values(ascending=False) * 100
fig, ax = plt.subplots(figsize=(8,5))
bars = ax.bar(dept_attr.index, dept_attr.values, color=PALETTE[:len(dept_attr)], width=0.5)
ax.set_title('Attrition Rate by Department (%)', fontsize=13, fontweight='bold')
ax.set_ylabel('Attrition Rate (%)')
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax.grid(axis='y')
for bar, val in zip(bars, dept_attr.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:.1f}%', ha='center', va='bottom', fontsize=10, color=TEXT)
save('02_attrition_by_department')

# ── Chart 3: Attrition by Tenure Band ──────────────────────
tenure_attr = df.groupby('TenureBand', observed=True)['AttritionBinary'].mean() * 100
fig, ax = plt.subplots(figsize=(9,5))
bars = ax.bar(tenure_attr.index.astype(str), tenure_attr.values,
              color=ACCENT, width=0.5, alpha=0.9)
ax.set_title('Attrition Rate by Tenure Band', fontsize=13, fontweight='bold')
ax.set_ylabel('Attrition Rate (%)')
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax.grid(axis='y')
for bar, val in zip(bars, tenure_attr.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
            f'{val:.1f}%', ha='center', va='bottom', fontsize=10, color=TEXT)
save('03_attrition_by_tenure')

# ── Chart 4: Attrition by Job Role ─────────────────────────
role_attr = df.groupby('JobRole')['AttritionBinary'].mean().sort_values(ascending=True) * 100
fig, ax = plt.subplots(figsize=(9,7))
bars = ax.barh(role_attr.index, role_attr.values,
               color=[PALETTE[2] if v > 20 else PALETTE[0] for v in role_attr.values],
               height=0.6)
ax.set_title('Attrition Rate by Job Role (%)', fontsize=13, fontweight='bold')
ax.set_xlabel('Attrition Rate (%)')
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax.grid(axis='x')
for bar, val in zip(bars, role_attr.values):
    ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}%', va='center', fontsize=9, color=TEXT)
save('04_attrition_by_jobrole')

# ── Chart 5: Attrition by Salary Band ──────────────────────
sal_attr = df.groupby('SalaryBand', observed=True)['AttritionBinary'].mean().sort_values(ascending=False) * 100
fig, ax = plt.subplots(figsize=(8,5))
bars = ax.bar(sal_attr.index.astype(str), sal_attr.values,
              color=PALETTE[:len(sal_attr)], width=0.5)
ax.set_title('Attrition Rate by Salary Band', fontsize=13, fontweight='bold')
ax.set_ylabel('Attrition Rate (%)')
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax.grid(axis='y')
for bar, val in zip(bars, sal_attr.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
            f'{val:.1f}%', ha='center', va='bottom', fontsize=10, color=TEXT)
save('05_attrition_by_salary')

# ── Chart 6: Overtime vs Attrition ─────────────────────────
ot_attr = df.groupby('OverTime')['AttritionBinary'].mean() * 100
fig, ax = plt.subplots(figsize=(6,5))
bars = ax.bar(['No Overtime', 'Works Overtime'], ot_attr.values,
              color=[PALETTE[0], PALETTE[2]], width=0.4)
ax.set_title('Attrition Rate: Overtime vs No Overtime', fontsize=13, fontweight='bold')
ax.set_ylabel('Attrition Rate (%)')
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax.grid(axis='y')
for bar, val in zip(bars, ot_attr.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
            f'{val:.1f}%', ha='center', va='bottom', fontsize=11, color=TEXT)
save('06_attrition_overtime')

# ── Chart 7: Age Distribution (Attrited vs Retained) ───────
fig, ax = plt.subplots(figsize=(10,5))
df[df['Attrition']=='No' ]['Age'].hist(bins=20, ax=ax, color=PALETTE[0], alpha=0.7, label='Retained')
df[df['Attrition']=='Yes']['Age'].hist(bins=20, ax=ax, color=PALETTE[2], alpha=0.7, label='Attrited')
ax.set_title('Age Distribution: Attrited vs Retained', fontsize=13, fontweight='bold')
ax.set_xlabel('Age'); ax.set_ylabel('Count')
ax.legend()
ax.grid(axis='y')
save('07_age_distribution')

# ── Chart 8: Satisfaction Score vs Attrition ───────────────
fig, ax = plt.subplots(figsize=(8,5))
sat_attr = df.groupby(pd.cut(df['SatisfactionScore'], bins=4))['AttritionBinary'].mean() * 100
sat_attr.index = [f'{i.left:.1f}–{i.right:.1f}' for i in sat_attr.index]
bars = ax.bar(sat_attr.index, sat_attr.values, color=PALETTE[:4], width=0.5)
ax.set_title('Attrition Rate by Satisfaction Score', fontsize=13, fontweight='bold')
ax.set_xlabel('Avg Satisfaction Score (1=Low, 4=High)')
ax.set_ylabel('Attrition Rate (%)')
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax.grid(axis='y')
for bar, val in zip(bars, sat_attr.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
            f'{val:.1f}%', ha='center', va='bottom', fontsize=10, color=TEXT)
save('08_satisfaction_vs_attrition')

# ── Chart 9: Correlation Heatmap ───────────────────────────
num_cols = [
    'AttritionBinary','Age','MonthlyIncome','YearsAtCompany',
    'JobSatisfaction','EnvironmentSatisfaction','WorkLifeBalance',
    'DistanceFromHome','NumCompaniesWorked','OverTimeBinary',
    'YearsWithCurrManager','PercentSalaryHike','SatisfactionScore'
]
corr = df[num_cols].corr()
fig, ax = plt.subplots(figsize=(12,9))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(
    corr, mask=mask, ax=ax,
    cmap=sns.diverging_palette(10, 120, as_cmap=True),
    center=0, annot=True, fmt='.2f', annot_kws={'size':8},
    linewidths=0.5, linecolor='#111',
    cbar_kws={'shrink':0.8}
)
ax.set_title('Correlation Matrix — Key Variables', fontsize=13, fontweight='bold', pad=16)
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.yticks(fontsize=8)
save('09_correlation_heatmap')


# ═══════════════════════════════════════════════════════════
# 5. SQL-READY AGGREGATION TABLES (saved as CSV)
# ═══════════════════════════════════════════════════════════
print('\n' + '═'*55)
print('  STEP 5 — Export SQL-Ready Summary Tables')
print('═'*55)

# Department summary
dept_summary = df.groupby('Department').agg(
    Total        = ('AttritionBinary', 'count'),
    Attrited     = ('AttritionBinary', 'sum'),
    AttritionRate= ('AttritionBinary', lambda x: round(x.mean()*100, 1)),
    AvgAge       = ('Age', lambda x: round(x.mean(), 1)),
    AvgIncome    = ('MonthlyIncome', lambda x: round(x.mean(), 0)),
    AvgTenure    = ('YearsAtCompany', lambda x: round(x.mean(), 1)),
    AvgSatisfaction = ('SatisfactionScore', lambda x: round(x.mean(), 2))
).reset_index()
dept_summary.to_csv('outputs/data/summary_by_department.csv', index=False)
print('  ✓ summary_by_department.csv')

# Job role summary
role_summary = df.groupby('JobRole').agg(
    Total        = ('AttritionBinary', 'count'),
    Attrited     = ('AttritionBinary', 'sum'),
    AttritionRate= ('AttritionBinary', lambda x: round(x.mean()*100, 1)),
    AvgIncome    = ('MonthlyIncome', lambda x: round(x.mean(), 0)),
    AvgSatisfaction = ('SatisfactionScore', lambda x: round(x.mean(), 2))
).reset_index().sort_values('AttritionRate', ascending=False)
role_summary.to_csv('outputs/data/summary_by_jobrole.csv', index=False)
print('  ✓ summary_by_jobrole.csv')

# Tenure band summary
tenure_summary = df.groupby('TenureBand', observed=True).agg(
    Total        = ('AttritionBinary', 'count'),
    Attrited     = ('AttritionBinary', 'sum'),
    AttritionRate= ('AttritionBinary', lambda x: round(x.mean()*100, 1)),
    AvgIncome    = ('MonthlyIncome', lambda x: round(x.mean(), 0))
).reset_index()
tenure_summary.to_csv('outputs/data/summary_by_tenure.csv', index=False)
print('  ✓ summary_by_tenure.csv')

# Salary band summary
salary_summary = df.groupby('SalaryBand', observed=True).agg(
    Total        = ('AttritionBinary', 'count'),
    Attrited     = ('AttritionBinary', 'sum'),
    AttritionRate= ('AttritionBinary', lambda x: round(x.mean()*100, 1))
).reset_index()
salary_summary.to_csv('outputs/data/summary_by_salary.csv', index=False)
print('  ✓ summary_by_salary.csv')


# ═══════════════════════════════════════════════════════════
# 6. KEY FINDINGS PRINTOUT
# ═══════════════════════════════════════════════════════════
print('\n' + '═'*55)
print('  STEP 6 — Key Findings')
print('═'*55)

top_dept   = dept_summary.sort_values('AttritionRate', ascending=False).iloc[0]
top_role   = role_summary.iloc[0]
top_tenure = tenure_summary.sort_values('AttritionRate', ascending=False).iloc[0]
ot_yes     = df[df['OverTime']=='Yes']['AttritionBinary'].mean()*100
ot_no      = df[df['OverTime']=='No' ]['AttritionBinary'].mean()*100

print(f"""
  1. Overall attrition rate         : {rate:.1f}% ({attrited} of {total} employees)
  2. Highest-attrition department   : {top_dept['Department']} ({top_dept['AttritionRate']}%)
  3. Highest-attrition job role     : {top_role['JobRole']} ({top_role['AttritionRate']}%)
  4. Most at-risk tenure band       : {top_tenure['TenureBand']} ({top_tenure['AttritionRate']}%)
  5. Overtime effect                : {ot_yes:.1f}% attrition (overtime) vs {ot_no:.1f}% (no overtime)
  6. Lowest income band attrition   : {salary_summary.sort_values('AttritionRate',ascending=False).iloc[0]['SalaryBand']}
""")

print('═'*55)
print('  ✅  All done!')
print('  Charts → outputs/charts/')
print('  Data   → outputs/data/')
print('  Load hr_attrition_cleaned.csv into Power BI next.')
print('═'*55 + '\n')
