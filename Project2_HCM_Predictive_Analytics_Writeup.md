# Project 2: High-Cost Member Predictive Analytics & Care Navigation ROI
**Organization:** Manulife Financial
**Analyst:** Nicholas Steven | nicholassteven@dal.ca | github.com/nicholasstevenr

---

## Business Context

Manulife's Vitality and care navigation programs aim to identify high-cost group benefit members before they generate catastrophic claims and connect them to proactive care management (nurse navigator, chronic disease coaching, mental health referral). The top 5% of members by claims generate 52.4% of total group benefit spend. Early identification (using prior claims, diagnostic codes, drug fill patterns, and disability history) enables targeted intervention 6-12 months before cost crystallization. Analytics mandate: (1) build and monitor a high-cost member (HCM) predictive model, and (2) measure the care navigation ROI in terms of avoided claims and PMPM differential.

---

## Analytical Approach

### Chart 2 (Left): High-Cost Member Predictive Model Performance XmR (Monthly AUC, 24 Months)

**Objective:** Monitor the monthly AUC (area under the ROC curve) of Manulife's HCM predictive model to detect model drift -- the degradation in predictive accuracy as the member population and claims environment shift.

**Method -- XmR on Monthly AUC:**
- Model features: prior-year total claims PMPM, specialty drug flag, disability episode history, paramedical utilization intensity, diagnostic code flags (diabetes, CHF, COPD, cancer, MH), demographic features
- X-bar AUC = 0.824; MR-bar = 0.018
- sigma = MR-bar/1.128 = 0.016
- UCL = 0.824 + 3(0.016) = 0.872 | LCL = 0.824 - 3(0.016) = 0.776

**OOC Events (3):**
- Month 7: Below LCL (AUC=0.764) -- COVID claims disruption: pandemic suppressed routine claims (planned surgeries, elective care) for high-cost members, masking true risk signals; model trained on pre-COVID patterns underperformed on pandemic-year data; model retrained with COVID-year claims in Month 9
- Month 15: Above UCL (AUC=0.884) -- Feature engineering enhancement: Manulife added LTD conversion flag and GLP-1 prescription flag as predictive features; both features carry high signal for catastrophic cost trajectory
- Month 22: Below LCL (AUC=0.771) -- GLP-1 off-label prescribing shift: explosive GLP-1 growth created a new high-cost member phenotype (obesity-primary, low prior utilization) that pre-GLP-1 model features did not capture; triggered GLP-1 cohort sub-model development

**Model Metrics at Month 24:**
- AUC: 0.824 (good discrimination)
- Sensitivity (top-10% flag captures % of actual top-10% cost members): 72.4%
- Positive Predictive Value: 64.2% (of flagged members, 64.2% indeed in top 10% actual cost)
- Top-10% flagged members = 68.4% of subsequent 12-month claims

### Chart 2 (Right): Care Navigation ROI -- Claims PMPM Comparison

**Objective:** Compare 12-month forward claims PMPM for members who accepted care navigation intervention vs. matched controls who declined, to quantify the program ROI.

**Care Navigation Cohort (n=4,200 members):**
- Enrolled (accepted care navigator): avg $2,184 PMPM forward claims
- Declined / control: avg $3,842 PMPM forward claims
- PMPM differential: -$1,658 PMPM (-43.2% relative reduction)
- Annual avoided claims per enrolled member: $19,896
- Program cost (nurse navigator + digital coaching): $842/member/year
- Net ROI per enrolled member: $19,054 (22.6:1 ROI)

**Claims PMPM by Intervention Tier:**
- Tier 1 (low-touch digital coaching only): $2,842 PMPM vs control $3,842 (-26.0%)
- Tier 2 (nurse navigator + coaching): $2,184 PMPM vs control $3,842 (-43.2%)
- Tier 3 (intensive case management + nurse): $1,684 PMPM vs control $3,842 (-56.2%)
- Non-engaged / declined all: $3,842 PMPM (control)

**c-Chart: Monthly Care Navigation Escalations (members escalated from Tier 1 to Tier 2/3):**
- c-bar = 84.2 escalations/month; UCL = 84.2 + 3*sqrt(84.2) = 111.7; LCL = 56.7
- Month 11: c = 124 (above UCL) -- Cancer diagnosis surge in cohort (Q3 oncology claims pattern); 42 members escalated from digital coaching to intensive case management
- Month 19: c = 48 (below LCL) -- Successful tier-down: members who completed 12-month intensive case management were stepped down to Tier 1; escalation count dropped as cohort stabilized

---

## Key Findings

1. **HCM model provides strong ROI foundation:** AUC=0.824 with 68.4% of flagged members generating top-decile actual costs; at 22.6:1 ROI, care navigation is Manulife's highest-return group benefit investment per dollar spent.
2. **GLP-1 cohort requires sub-model:** Month 22 AUC drift below LCL is a specific GLP-1 phenotype gap; obesity-primary high-cost members with low prior utilization are structurally different from the chronic disease/disability-primary members the base model was trained on.
3. **Intensive case management delivers the highest PMPM reduction:** Tier 3 (-56.2%) vs Tier 1 (-26.0%); investment in nurse case managers for the highest-risk members generates the greatest return; the escalation c-chart enables real-time monitoring of case load intensity.
4. **COVID model drift is a proof-of-concept for ongoing monitoring:** Month 7 AUC dip demonstrates that XmR-based model performance monitoring detected the COVID disruption faster than quarterly validation cycles; monthly AUC surveillance is now standard Manulife practice.

---

## Tools & Standards
Python (scikit-learn, numpy, matplotlib), logistic regression, gradient boosting (XGBoost), AUC/ROC, ICD-10-CA, ATC drug classification, DIN, Manulife group claims data, SPC (XmR for AUC monitoring + c-chart), care navigation program analytics, IQVIA/CIHI benchmarking
