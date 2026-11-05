# SupplyChain Insights
## Business Insights & Recommendations Report

**Project:** DataCo Smart Supply Chain Analysis  
**Analysis period:** January 2015 – January 2018  
**Tools:** Python, Pandas, NumPy, SQL, SQLite, Plotly, Streamlit  
**Project focus:** Delivery performance, operational efficiency, and business impact

---

## 1. Executive Summary

This project analyzes the DataCo Smart Supply Chain dataset to understand delivery performance and identify areas that may require operational improvement.

The analysis covers 180,519 order-item records, 65,752 unique orders, and 20,652 unique customers. It uses Python for data preparation and exploratory analysis, SQL for structured business queries, and Streamlit with Plotly for interactive visualization.

The analysis identifies a late delivery rate of **57.29% among non-canceled records**. Shipping-mode comparisons show particularly high late delivery rates for First Class (100%) and Second Class (79.83%). Regional analysis identifies Central Africa as having the highest late delivery rate (60.15%), while Central America contributes the highest number of late records (15,518).

The sales associated with late delivery records total approximately **$20.13 million**. This represents financial exposure associated with delayed records, not confirmed financial losses.

The findings suggest that management should investigate shipping schedules, regional delivery operations, and product categories with both substantial delivery volumes and elevated late rates.

## 2. Business Problem Statement

Supply-chain delivery performance is an important factor in customer satisfaction and operational efficiency.

Late deliveries can indicate possible issues with delivery scheduling, transportation operations, or regional logistics.

The objective of this project is to analyze historical supply-chain data and answer the following questions:

- How frequently do late deliveries occur?
- Which shipping modes have the highest late delivery rates?
- Which regions contribute the most late deliveries?
- Which product categories experience relatively high delivery delays?
- How does delivery performance change over time?
- What sales value is associated with late delivery records?
- What actions could management investigate to improve delivery performance?

## 3. Dataset Overview

The analysis uses the DataCo Smart Supply Chain dataset.

| Dataset attribute | Value |
|---|---:|
| Total order-item records | 180,519 |
| Unique orders | 65,752 |
| Unique customers | 20,652 |
| Total columns in original dataset | 53 |
| Analysis period | Jan 2015 – Jan 2018 |

Each row represents an order-item record. A single order can contain multiple items, which means the number of rows is not the same as the number of unique orders.

### Technologies used

- Python
- Pandas and NumPy
- Jupyter Notebook
- SQL
- SQLite
- Plotly
- Streamlit
- Git and GitHub

## 4. Overall Delivery Performance

The dataset contains the following delivery-status distribution:

| Delivery status | Records | Percentage |
|---|---:|---:|
| Late delivery | 98,977 | 54.83% |
| Advance shipping | 41,592 | 23.04% |
| Shipping on time | 32,196 | 17.84% |
| Shipping canceled | 7,754 | 4.30% |
| **Total** | **180,519** | **100%** |

Canceled records are excluded when calculating the delivery performance rate.

**Late delivery rate = (Late records / Non-canceled records) × 100**

= (98,977 / 172,765) × 100

= **57.29%**

### Business interpretation

More than half of the non-canceled order-item records are marked as late. This indicates a substantial delivery performance issue within the historical dataset.

Management should investigate delivery operations and scheduling practices to understand the reasons behind this pattern.

## 5. Shipping Mode Performance

The shipping-mode analysis identifies differences in late delivery rates.

| Shipping mode | Non-canceled records | Late records | Late rate |
|---|---:|---:|---:|
| First Class | 26,513 | 26,513 | 100.00% |
| Second Class | 33,806 | 26,987 | 79.83% |
| Same Day | 9,293 | 4,454 | 47.93% |
| Standard Class | 103,153 | 41,023 | 39.77% |

### Key observations

- First Class has a 100% late delivery rate.
- Second Class has a late delivery rate of 79.83%.
- Same Day has a late delivery rate of 47.93%.
- Standard Class has the lowest late delivery rate at 39.77%.
- Standard Class also accounts for the highest number of non-canceled records.

The average actual shipping duration is approximately two days for First Class against a scheduled duration of one day. Second Class averages approximately four days against a scheduled duration of two days.

### Business interpretation

The differences between scheduled and actual delivery durations indicate that First Class and Second Class delivery commitments deserve further investigation.

The business should examine whether the scheduled delivery targets are realistic and whether carrier transit times and warehouse processing are adequately reflected in delivery commitments.

These observations do not establish that shipping mode causes delays.

## 6. Regional Delivery Performance

Regional analysis highlights geographical differences in late delivery rates.

| Region | Late delivery rate |
|---|---:|
| Central Africa | 60.15% |
| Western Europe | 58.53% |
| South of USA | 58.52% |
| South Asia | 58.35% |
| East of USA | 58.17% |
| Southeast Asia | 57.98% |
| West Asia | 57.81% |
| Eastern Europe | 57.65% |
| US Center | 57.53% |

### Key observations

- Central Africa has the highest late delivery rate at 60.15%.
- Central America contributes the highest late delivery count, with 15,518 records.
- Canada has the lowest late delivery rate at 51.60%.
- Central Asia has a relatively small sample of 542 non-canceled records.

### Business interpretation

Central Africa should be investigated because of its high late delivery rate. Central America should also receive attention because of its large number of late records.

The business should distinguish between regions with high late percentages and regions contributing the largest number of delayed records.

## 7. Product Category Performance

The category analysis identifies product categories with relatively high late delivery rates.

| Product category | Late delivery rate |
|---|---:|
| Golf Bags & Carts | 68.85% |
| Lacrosse | 62.61% |
| Pet Supplies | 61.44% |
| Cameras | 61.21% |

Golf Bags & Carts has only 61 non-canceled records, so its high percentage should be interpreted cautiously.

Other significant-volume categories, including Cleats, Fishing, Women's Apparel, and Men's Footwear, have late delivery rates around 57%.

### Top product categories by sales

| Product category | Total sales |
|---|---:|
| Fishing | $6,929,653.69 |
| Cleats | $4,431,942.78 |
| Camping & Hiking | $4,118,425.57 |
| Cardio Equipment | $3,694,843.20 |
| Women's Apparel | $3,147,800.00 |

### Business interpretation

Product categories should be prioritized using delivery rate, record volume, number of late records, and associated sales value together.

This helps avoid giving excessive attention to categories with high percentages but very small sample sizes.

## 8. Time-Based Delivery Analysis

The monthly analysis indicates that late delivery rates generally remain within approximately 55%–59% throughout the available historical period.

Some examples include:

| Month | Late delivery rate |
|---|---:|
| September 2015 | 59.16% |
| June 2016 | 59.31% |
| August 2017 | 58.58% |
| January 2018 | 58.66% |

### Business interpretation

The relatively stable monthly late delivery rate suggests that the delivery issue persisted across the historical period rather than appearing only during one unusual month.

The final months have lower order volumes in parts of the dataset, so changes in volume should not automatically be interpreted as a decline in business activity.

## 9. Market-Level Delivery Performance

The market-level analysis shows the following late delivery rates:

| Market | Late delivery rate |
|---|---:|
| Europe | 57.69% |
| USCA | 57.41% |
| Pacific Asia | 57.38% |
| LATAM | 56.87% |
| Africa | 56.84% |

### Business interpretation

Europe has the highest late delivery rate among the analyzed markets. However, the differences are relatively small.

The findings suggest that late delivery performance is a broader issue across the markets represented in the dataset rather than being restricted to a single market.

## 10. Financial Exposure Associated with Late Deliveries

The financial analysis identifies the following values:

| Metric | Amount |
|---|---:|
| Total sales | $36,784,735.01 |
| Sales associated with late records | $20,126,395.27 |
| Order-item value associated with late records | $18,082,555.30 |

### Business interpretation

A substantial amount of sales value is associated with records marked as late.

However, these figures should not be interpreted as actual financial losses. The dataset does not establish whether late deliveries resulted in refunds, customer compensation, lost sales, or additional logistics expenses.

Further information would be required to calculate the actual financial impact of late deliveries.

## 11. Business Recommendations

Based on the analysis, the following recommendations are proposed.

### Recommendation 1: Investigate First Class and Second Class delivery operations

First Class has a 100% late delivery rate, while Second Class has a rate of 79.83%.

Management should investigate:

- Whether scheduled delivery targets are realistic.
- Whether warehouse processing time is included in delivery schedules.
- Whether carrier transit times match delivery commitments.
- Whether shipping service targets require revision.

### Recommendation 2: Prioritize regional delivery investigations

Central Africa has the highest late delivery rate, while Central America contributes the highest late delivery count.

Management should investigate regional carrier performance, logistics constraints, and differences between scheduled and actual delivery durations.

### Recommendation 3: Prioritize product categories using multiple metrics

Product categories should be evaluated using:

- Total order-item records.
- Number of late records.
- Late delivery percentage.
- Associated sales value.

This will help management identify categories where operational improvements could affect a substantial number of records or significant sales value.

### Recommendation 4: Monitor delivery performance regularly

Management should monitor:

- Late delivery rate.
- Average shipping delay.
- Cancellation rate.
- Regional delivery performance.
- Shipping-mode performance.
- Monthly delivery trends.

The Streamlit dashboard developed in this project provides a starting point for this monitoring.

### Recommendation 5: Investigate actual financial impact

The business should connect delivery information with refund records, customer complaints, compensation payments, logistics costs, and repeat-purchase information.

This would help determine whether delayed deliveries create measurable financial losses or customer-retention problems.

## 12. Limitations of the Analysis

The following limitations should be considered when interpreting the findings:

1. **Historical data:** The dataset covers January 2015 to January 2018 and does not represent current operational conditions.
2. **Order-item-level records:** Each row represents an order item, not necessarily a unique order.
3. **Missing values:** Some fields, including product descriptions and many postal codes, contain missing information.
4. **Limited operational information:** The dataset does not provide sufficient details about individual carriers, warehouses, weather conditions, or specific logistics disruptions.
5. **No causal proof:** The analysis identifies patterns and associations but does not establish the causes of late deliveries.
6. **Financial interpretation:** Sales associated with late records cannot be treated as actual financial losses.
7. **Small sample sizes:** Some category and regional percentages are based on relatively few records.
8. **Shipping-day definitions:** Supplied shipping-day fields and timestamp-derived durations have some discrepancies. The supplied actual and scheduled shipping-day fields are retained for delivery performance analysis, with the discrepancy documented.

## 13. Conclusion

The SupplyChain Insights project demonstrates how data analytics can be used to investigate delivery performance and identify operational areas requiring further attention.

The analysis of 180,519 order-item records identifies a 57.29% late delivery rate among non-canceled records. First Class and Second Class show particularly high late delivery rates, while regional analysis highlights Central Africa and Central America as important areas for investigation.

The analysis also identifies approximately $20.13 million in sales associated with late delivery records. Although this is not a measure of confirmed financial losses, it demonstrates the scale of sales value connected to delayed records.

By combining Python-based data analysis, SQL queries, and an interactive Streamlit dashboard, the project provides a structured view of supply-chain delivery performance and actionable recommendations for further investigation.

**The overall objective is to help management move from simply observing delivery delays to identifying where operational improvements should be investigated and prioritized.**

---

**End of Report**