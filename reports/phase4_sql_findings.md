# Phase 4 – SQL Analysis Findings

## 1. Objective

The objective of this phase was to perform structured SQL analysis on the cleaned DataCo Smart Supply Chain dataset using SQLite.

The analysis focused on identifying delivery performance patterns, evaluating shipping modes, comparing geographical regions, analysing product categories, examining monthly trends, and understanding the financial value associated with delayed deliveries.

A total of 15 SQL queries were executed to extract business insights from the dataset.

## 2. Database Overview

- Database: `supply_chain.db`
- Table: `supply_chain`
- Total order-item records: 180,519
- Unique orders: 65,752
- Unique order items: 180,519
- Unique customers: 20,652
- Total recorded sales: $36,784,735.01
- Total order-item value: $33,054,402.38
- Number of SQL queries: 15

Each row represents an order-item record, not necessarily a unique customer order.

## 3. Key Analysis Areas and Findings

### 3.1 Overall Delivery Performance

The dataset contains 98,977 late-delivery records, representing 54.83% of all records.

After excluding 7,754 canceled records, the late-delivery rate is 57.29% across 172,765 non-canceled records.

This indicates that more than half of the non-canceled order-item records experienced late delivery, highlighting a significant delivery-performance concern.

### 3.2 Shipping Mode Analysis

First Class shipping recorded the highest late-delivery rate at 100%, followed by Second Class at 79.83%.

Same Day shipping recorded a late-delivery rate of 47.93%, while Standard Class had the lowest rate at 39.77%.

Standard Class also accounted for the highest volume, with 103,153 non-canceled records.

Average shipping delays were:
- First Class: 1.00 day
- Second Class: 1.99 days
- Same Day: 0.48 days
- Standard Class: -0.01 days

The consistently high late-delivery rates for First Class and Second Class warrant further investigation.

### 3.3 Regional Delivery Performance

Central Africa recorded the highest late-delivery rate at 60.15%, followed by Western Europe at 58.53%.

However, Central America recorded the highest absolute number of late deliveries, with 15,518 records, followed by Western Europe with 15,140.

Canada recorded the lowest regional late-delivery rate at 51.60%.

Regional comparisons should consider the number of records in each region, as smaller sample sizes can make percentage rankings less stable.

### 3.4 Product Category Analysis

Golf Bags & Carts recorded the highest late-delivery percentage at 68.85%, followed by Lacrosse at 62.61% and Pet Supplies at 61.44%.

However, these categories have relatively small record volumes.

Among higher-volume categories, Cleats recorded 13,496 late records, Fishing recorded 9,516, and Indoor/Outdoor Games recorded 10,565.

This indicates that both the late-delivery percentage and the absolute number of affected records should be considered when prioritising product categories.

### 3.5 Monthly Trends

Monthly late-delivery rates remained relatively stable, generally ranging between approximately 55% and 59%.

Examples include:
- September 2015: 59.16%
- June 2016: 59.31%
- August 2017: 58.58%
- January 2018: 58.66%

The results indicate that late deliveries occurred consistently throughout the observed period rather than being restricted to a particular month.

A noticeable reduction in monthly record volume occurs from October 2017 onwards. This may reflect incomplete source coverage or a change in the available dataset and requires further investigation before drawing conclusions about business volume trends.

### 3.6 Financial Performance

Fishing generated the highest recorded category sales at $6,929,653.69, followed by Cleats at $4,431,942.78 and Camping & Hiking at $4,118,425.57.

At the regional level, Western Europe generated the highest recorded sales at $5,894,380.77, followed by Central America at $5,665,712.10.

The analysis of late-delivery records revealed:
- Late order-item records: 98,977
- Sales associated with late records: $20,126,395.27
- Item value associated with late records: $18,082,555.30
- Average shipping delay: 1.62 days

The sales associated with late records represent potential business exposure, not confirmed financial loss caused by delivery delays.

The profit metric should also be validated for its aggregation grain before treating summed values as definitive profit figures.

### 3.7 Order and Delivery Status

The analysis identified 34,199 records with COMPLETE order status and Late delivery status.

Additionally, 22,922 records had PENDING_PAYMENT order status and Late delivery status.

All 7,754 shipping-canceled records corresponded to either SUSPECTED_FRAUD or CANCELED order statuses.

This demonstrates that order processing status and delivery performance are separate dimensions and should be analysed independently.

### 3.8 Market-Level Analysis

Europe recorded the highest late-delivery rate at 57.69%, followed by USCA at 57.41% and Pacific Asia at 57.38%.

LATAM and Africa recorded rates of 56.87% and 56.84%, respectively.

The relatively small differences indicate that late-delivery performance is a concern across all five markets rather than being concentrated in a single market.

### 3.9 Region and Shipping Mode Combination

The region-and-shipping-mode analysis showed that First Class had a 100% late-delivery rate across all represented regions.

Second Class also demonstrated consistently high late-delivery rates, whereas Standard Class generally performed better.

This suggests that the First Class delivery pattern is not limited to one particular region and deserves further investigation.

### 3.10 Category-Level Financial Performance

Fishing, Cleats, Camping & Hiking, Cardio Equipment, and Women's Apparel were among the largest contributors to recorded category sales.

These categories represent important areas for further investigation because of their contribution to the overall recorded sales value.

## 4. Key Business Insights

1. **Overall delivery performance requires attention:** 57.29% of non-canceled order-item records were classified as late.

2. **First Class and Second Class are priority areas:** Their late-delivery rates were 100% and 79.83%, respectively.

3. **Regional priorities differ depending on the metric:** Central Africa had the highest late-delivery percentage, whereas Central America had the highest number of late records.

4. **High-volume product categories matter:** Cleats, Fishing, Indoor/Outdoor Games, and Women's Apparel contributed substantial numbers of late records.

5. **Late deliveries are associated with substantial sales value:** Approximately $20.13 million in recorded sales was associated with late-delivery records. This is potential business exposure, not confirmed financial loss.

6. **Delivery performance is consistently weak over time:** Monthly late-delivery rates remained mostly between 55% and 59%.

7. **Delivery issues appear across markets:** All five markets had late-delivery rates close to 57%.

8. **Monthly record volume needs further investigation:** A noticeable drop occurs from October 2017 onwards, so conclusions about changes in business volume should be made cautiously.

## 5. Business Recommendations

1. Investigate the consistently high late-delivery rates associated with First Class and Second Class shipping.

2. Review regional delivery operations, prioritising both high late-delivery percentages and high absolute late-record volumes.

3. Monitor product categories with high late-delivery percentages as well as categories contributing large numbers of delayed records.

4. Track monthly delivery performance to identify recurring patterns and changes in operational performance.

5. Monitor the sales value associated with late deliveries as an indicator of potential business exposure.

6. Investigate the sharp reduction in monthly record volume from October 2017 onwards to understand whether it reflects incomplete data coverage or a genuine change.

7. Validate the aggregation level of the profit metric before reporting total profit figures.

## 6. Limitations

- Each row represents an order-item record, not necessarily a unique customer order.
- Canceled records were excluded when calculating delivery-performance percentages.
- Sales associated with late deliveries represent potential business exposure, not confirmed financial loss.
- The dataset does not establish the causes of delivery delays.
- Regional and product-category comparisons should consider differences in record volumes.
- The monthly record volume drops noticeably from October 2017 onwards and requires further investigation.
- The profit metric should be checked for repeated order-level values before summing it across order-item records.
- The findings describe historical patterns and do not establish causation.

## 7. Conclusion

SQL analysis provided a structured way to examine supply-chain delivery performance, shipping-mode patterns, geographical differences, product categories, monthly trends, and financial metrics.

The analysis identified a substantial late-delivery rate, particularly for First Class and Second Class shipping. It also highlighted regional and product-category differences and the significant sales value associated with late-delivery records.

These findings provide a foundation for further exploratory analysis and the development of an interactive business intelligence dashboard using the analysed supply-chain data.