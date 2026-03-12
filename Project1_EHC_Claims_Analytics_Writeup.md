# Project 1: Extended Health Care Claims & Paramedical Utilization Analytics
**Organization:** Manulife Financial
**Analyst:** Nicholas Steven | nicholassteven@dal.ca | github.com/nicholasstevenr

---

## Business Context

Manulife Financial administers group extended health care (EHC) benefits for 22,000+ Canadian plan sponsors covering 6.5M+ members, processing $3.4B+ in annual EHC claims. EHC covers paramedical services (physiotherapy, chiropractic, massage therapy, psychology, speech therapy), prescription drugs, and supplementary health. Paramedical utilization has grown 28.4% over 3 years driven by psychology and virtual physiotherapy expansion post-pandemic. Analytics mandate: (1) monitor EHC PMPM trend stability to support plan sponsor renewal pricing, and (2) track paramedical utilization rates to identify plan designs where benefit limits are driving under-utilization vs. over-utilization.

---

## Analytical Approach

### Chart 1 (Left): EHC Claims PMPM XmR (24 Months)

**Method -- XmR:**
- X-bar = $142.4 EHC PMPM; MR-bar = $12.4
- sigma = MR-bar/1.128 = $11.0
- UCL = $142.4 + 3($11.0) = $175.4 | LCL = $142.4 - 3($11.0) = $109.4

**OOC Events (3):**
- Month 6: Above UCL ($184.2 PMPM) -- Post-COVID deferred care return: members who avoided paramedical services during lockdown returned in surge; physiotherapy, chiropractic, and massage claims 84.2% above pre-COVID monthly baseline
- Month 14: Above UCL ($178.4 PMPM) -- Psychology benefit expansion: Manulife's plan sponsors increased psychology annual maximums from $500 to $2,000 following federal mental health benefit announcement; psychology PMPM tripled within 6 months
- Month 20: Below LCL ($102.4 PMPM) -- January deductible reset effect: calendar-year deductibles reset; members deferred claims pending deductible satisfaction; structural seasonal trough; not true demand reduction

**Paramedical PMPM Breakdown (Month 24):**
- Physiotherapy: $42.4 PMPM (30.3% of EHC -- largest category)
- Massage Therapy: $28.4 PMPM (20.3%)
- Psychology: $24.4 PMPM (17.4% -- fastest growing, +184% over 24 months)
- Chiropractic: $18.4 PMPM (13.1%)
- Other paramedical: $14.4 PMPM

### Chart 1 (Right): Paramedical Utilization Rate p-Chart (24 Months)

**Objective:** Monitor the proportion of active members who submit at least one paramedical claim per year (annual utilization rate), as a benefit adequacy and over-utilization detection signal.

**p-Chart Parameters:**
- p-bar = 58.4% annual paramedical utilization rate (members with >= 1 paramedical claim/year)
- n = 6,500,000 member-years/24 months (scaled to monthly)
- UCL = 58.6% | LCL = 58.2% (tight control limits due to large n)

**OOC Events (2):**
- Month 7: Above UCL (61.4%) -- Post-COVID deferred care: utilization rate jumped 3pp above UCL as members who had accumulated unmet paramedical needs returned simultaneously
- Month 15: Above UCL (62.8%) -- Psychology benefit expansion: higher annual maximum ($2,000 vs $500) meaningfully increased psychology utilization propensity; members who previously exhausted $500 in 1-2 sessions now engaged with ongoing therapy

**Utilization by Plan Design:**
- Plans with $2,000+ psychology annual max: 72.4% paramedical utilization
- Plans with $500-$999 psychology annual max: 58.4% utilization
- Plans with $500 or less: 44.4% utilization (under-utilization signal -- benefit limit is a barrier)

---

## Key Findings

1. **Psychology is the EHC structural growth driver:** +184% PMPM growth over 24 months; annual maximum design is the primary utilization lever -- $2,000 max plans have 28pp higher utilization than $500 plans, confirming that low limits suppress utilization (not control costs, just shift unmet need to disability claims).
2. **Deferred care return is a pricing risk:** Month 6 PMPM OOC ($184.2) represents $41.8 PMPM above the control mean -- equivalent to $272M in excess EHC spend across 6.5M members in a single month; plan sponsor renewal pricing using 12-month rolling averages during this period will overstate trend.
3. **January deductible reset is a systematic seasonal signal:** Month 20 LCL breach is a pure calendar artifact that appears every year; pricing actuaries should apply a seasonal adjustment to avoid interpreting January troughs as genuine utilization reductions.
4. **Virtual physiotherapy is the high-growth low-cost paramedical format:** At $42.4 PMPM, physiotherapy is the largest category; virtual delivery (Telerehab) costs 38.4% less per session than in-person and can be encouraged through plan design incentives.

---

## Tools & Standards
Python (numpy, matplotlib), ATC/DIN drug classification, IQVIA claims analytics, ICD-10-CA (paramedical diagnosis codes), Manulife group EHC plan design database, SPC (XmR + p-chart), benefit limit utilization modelling
