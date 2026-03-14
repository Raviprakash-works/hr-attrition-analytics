-- =============================================================
-- HR Employee Attrition Analytics — SQL Queries
-- Author : Ravi Prakash
-- Tool   : SQLite / PostgreSQL / MySQL compatible
-- Note   : Import hr_attrition_cleaned.csv as table 'hr'
-- =============================================================


-- ─────────────────────────────────────────────────────────────
-- 0. CREATE TABLE (SQLite / run once)
-- ─────────────────────────────────────────────────────────────
/*
CREATE TABLE hr AS
SELECT * FROM read_csv_auto('hr_attrition_cleaned.csv');
*/


-- ─────────────────────────────────────────────────────────────
-- 1. OVERVIEW — Headcount & Attrition Rate
-- ─────────────────────────────────────────────────────────────
SELECT
    COUNT(*)                                            AS TotalEmployees,
    SUM(AttritionBinary)                                AS TotalAttrited,
    ROUND(AVG(AttritionBinary) * 100.0, 1)             AS AttritionRate_Pct,
    ROUND(AVG(Age), 1)                                  AS AvgAge,
    ROUND(AVG(MonthlyIncome), 0)                        AS AvgMonthlyIncome,
    ROUND(AVG(YearsAtCompany), 1)                       AS AvgTenure
FROM hr;


-- ─────────────────────────────────────────────────────────────
-- 2. ATTRITION BY DEPARTMENT
-- ─────────────────────────────────────────────────────────────
SELECT
    Department,
    COUNT(*)                                            AS Total,
    SUM(AttritionBinary)                                AS Attrited,
    ROUND(AVG(AttritionBinary) * 100.0, 1)             AS AttritionRate_Pct,
    ROUND(AVG(MonthlyIncome), 0)                        AS AvgIncome,
    ROUND(AVG(YearsAtCompany), 1)                       AS AvgTenure,
    ROUND(AVG(SatisfactionScore), 2)                    AS AvgSatisfaction
FROM hr
GROUP BY Department
ORDER BY AttritionRate_Pct DESC;


-- ─────────────────────────────────────────────────────────────
-- 3. ATTRITION BY JOB ROLE
-- ─────────────────────────────────────────────────────────────
SELECT
    JobRole,
    COUNT(*)                                            AS Total,
    SUM(AttritionBinary)                                AS Attrited,
    ROUND(AVG(AttritionBinary) * 100.0, 1)             AS AttritionRate_Pct,
    ROUND(AVG(MonthlyIncome), 0)                        AS AvgIncome,
    ROUND(AVG(JobSatisfaction), 2)                      AS AvgJobSatisfaction
FROM hr
GROUP BY JobRole
ORDER BY AttritionRate_Pct DESC;


-- ─────────────────────────────────────────────────────────────
-- 4. ATTRITION BY TENURE BAND
-- ─────────────────────────────────────────────────────────────
SELECT
    TenureBand,
    COUNT(*)                                            AS Total,
    SUM(AttritionBinary)                                AS Attrited,
    ROUND(AVG(AttritionBinary) * 100.0, 1)             AS AttritionRate_Pct,
    ROUND(AVG(MonthlyIncome), 0)                        AS AvgIncome
FROM hr
GROUP BY TenureBand
ORDER BY AttritionRate_Pct DESC;


-- ─────────────────────────────────────────────────────────────
-- 5. OVERTIME IMPACT ON ATTRITION
-- ─────────────────────────────────────────────────────────────
SELECT
    OverTime,
    COUNT(*)                                            AS Total,
    SUM(AttritionBinary)                                AS Attrited,
    ROUND(AVG(AttritionBinary) * 100.0, 1)             AS AttritionRate_Pct
FROM hr
GROUP BY OverTime
ORDER BY AttritionRate_Pct DESC;


-- ─────────────────────────────────────────────────────────────
-- 6. ATTRITION BY SALARY BAND
-- ─────────────────────────────────────────────────────────────
SELECT
    SalaryBand,
    COUNT(*)                                            AS Total,
    SUM(AttritionBinary)                                AS Attrited,
    ROUND(AVG(AttritionBinary) * 100.0, 1)             AS AttritionRate_Pct,
    ROUND(AVG(MonthlyIncome), 0)                        AS AvgIncome
FROM hr
GROUP BY SalaryBand
ORDER BY AttritionRate_Pct DESC;


-- ─────────────────────────────────────────────────────────────
-- 7. HIGH-RISK EMPLOYEE PROFILE
--    (Attrited employees: who are they?)
-- ─────────────────────────────────────────────────────────────
SELECT
    ROUND(AVG(Age), 1)                                  AS AvgAge,
    ROUND(AVG(MonthlyIncome), 0)                        AS AvgIncome,
    ROUND(AVG(YearsAtCompany), 1)                       AS AvgTenure,
    ROUND(AVG(DistanceFromHome), 1)                     AS AvgDistanceFromHome,
    ROUND(AVG(JobSatisfaction), 2)                      AS AvgJobSatisfaction,
    ROUND(AVG(WorkLifeBalance), 2)                      AS AvgWorkLifeBalance,
    ROUND(AVG(OverTimeBinary) * 100.0, 1)              AS OvertimePct,
    ROUND(AVG(NumCompaniesWorked), 1)                   AS AvgCompaniesWorked
FROM hr
WHERE AttritionBinary = 1;


-- ─────────────────────────────────────────────────────────────
-- 8. RETAINED EMPLOYEE PROFILE (for comparison)
-- ─────────────────────────────────────────────────────────────
SELECT
    ROUND(AVG(Age), 1)                                  AS AvgAge,
    ROUND(AVG(MonthlyIncome), 0)                        AS AvgIncome,
    ROUND(AVG(YearsAtCompany), 1)                       AS AvgTenure,
    ROUND(AVG(DistanceFromHome), 1)                     AS AvgDistanceFromHome,
    ROUND(AVG(JobSatisfaction), 2)                      AS AvgJobSatisfaction,
    ROUND(AVG(WorkLifeBalance), 2)                      AS AvgWorkLifeBalance,
    ROUND(AVG(OverTimeBinary) * 100.0, 1)              AS OvertimePct,
    ROUND(AVG(NumCompaniesWorked), 1)                   AS AvgCompaniesWorked
FROM hr
WHERE AttritionBinary = 0;


-- ─────────────────────────────────────────────────────────────
-- 9. SATISFACTION SCORE VS ATTRITION
-- ─────────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN SatisfactionScore >= 3.5 THEN 'High (3.5–4.0)'
        WHEN SatisfactionScore >= 2.5 THEN 'Medium (2.5–3.4)'
        WHEN SatisfactionScore >= 1.5 THEN 'Low (1.5–2.4)'
        ELSE 'Very Low (<1.5)'
    END AS SatisfactionBand,
    COUNT(*)                                            AS Total,
    SUM(AttritionBinary)                                AS Attrited,
    ROUND(AVG(AttritionBinary) * 100.0, 1)             AS AttritionRate_Pct
FROM hr
GROUP BY SatisfactionBand
ORDER BY AttritionRate_Pct DESC;


-- ─────────────────────────────────────────────────────────────
-- 10. DEPARTMENT × OVERTIME CROSS-ANALYSIS
-- ─────────────────────────────────────────────────────────────
SELECT
    Department,
    OverTime,
    COUNT(*)                                            AS Total,
    SUM(AttritionBinary)                                AS Attrited,
    ROUND(AVG(AttritionBinary) * 100.0, 1)             AS AttritionRate_Pct
FROM hr
GROUP BY Department, OverTime
ORDER BY Department, AttritionRate_Pct DESC;


-- ─────────────────────────────────────────────────────────────
-- 11. TOP 10 HIGHEST-RISK EMPLOYEES (still active)
--     For HR intervention targeting
-- ─────────────────────────────────────────────────────────────
SELECT
    JobRole,
    Department,
    Age,
    MonthlyIncome,
    YearsAtCompany,
    OverTime,
    JobSatisfaction,
    SatisfactionScore,
    DistanceFromHome
FROM hr
WHERE
    AttritionBinary = 0              -- still active
    AND OverTimeBinary = 1           -- working overtime
    AND JobSatisfaction <= 2         -- low job satisfaction
    AND YearsAtCompany <= 3          -- early tenure (high-risk window)
ORDER BY SatisfactionScore ASC, MonthlyIncome ASC
LIMIT 10;
