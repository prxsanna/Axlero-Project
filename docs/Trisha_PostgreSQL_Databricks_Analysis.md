\## Task 3 — Databricks Suitability Analysis



\### 3.1 What is Databricks?



Databricks is a unified data and AI platform based on the lakehouse architecture. It provides capabilities for data engineering, large-scale data processing, analytics, machine learning, AI, streaming, data governance, and business intelligence.



Databricks uses technologies such as Apache Spark, Delta Lake, and Unity Catalog to support scalable data processing, reliable data storage, and data governance.



\### 3.2 What Databricks Provides



The main capabilities relevant to MetricMind are:



\- Large-scale data processing using Apache Spark.

\- ETL and data engineering pipelines.

\- Batch and streaming data processing.

\- SQL-based analytics and business intelligence.

\- Machine learning and AI workloads.

\- Data governance and data lineage.

\- Scalable data storage and processing.



\### 3.3 Does MetricMind Need Databricks?



The current MetricMind database contains:



\- Customers: 10,000 rows

\- Sales: 50,000 rows

\- Products: 20 rows

\- Customer Status: 10,000 rows



The current PostgreSQL database is already working and the backend successfully connects to it using SQLAlchemy.



For the current project, MetricMind does not have a requirement for:



\- Very large-scale distributed data processing.

\- Real-time streaming data.

\- Complex ETL pipelines.

\- Large-scale machine learning infrastructure.

\- Processing massive amounts of unstructured data.



Therefore, the current project does not require the main capabilities that Databricks is designed to provide.



\### 3.4 Would Databricks Improve MetricMind?



Databricks could provide benefits if MetricMind grows significantly and needs large-scale analytics, streaming, advanced machine learning, or complex data engineering.



However, for the current project, the existing PostgreSQL database is sufficient for storing and querying the structured business data.



Introducing Databricks at the current stage would not provide enough additional benefit to justify changing the architecture.



\### 3.5 Would Databricks Introduce Unnecessary Complexity?



Yes.



Adding Databricks would introduce another data platform and could require additional configuration, data integration, data pipelines, testing, maintenance, and backend changes.



The current architecture is simpler:



PostgreSQL → Backend → Semantic/Metric Layer → MetricMind



Adding Databricks would make the architecture more complicated without a current requirement for its large-scale capabilities.



\### 3.6 Does Databricks Fit the Current Architecture?



Databricks can integrate with databases and support many types of workloads, so it is technically possible to use it with MetricMind.



However, technical possibility does not mean that it is necessary.



The current PostgreSQL-based architecture is sufficient for the current dataset and application requirements.



\### 3.7 Final Assessment



Databricks is a powerful platform for large-scale data engineering, analytics, streaming, machine learning, AI, and data governance.



However, MetricMind currently has a relatively small structured dataset and does not require these large-scale capabilities.



Therefore:



\*\*Databricks is NOT recommended for the current version of MetricMind.\*\*



It can be reconsidered in the future if the project grows to require:



\- Much larger datasets.

\- Real-time data processing.

\- Complex ETL pipelines.

\- Advanced machine learning workloads.

\- Large-scale analytics.



\### Task 3 Recommendation



\*\*DO NOT ADD DATABRICKS AT THIS STAGE.\*\*



\*\*KEEP THE CURRENT POSTGRESQL ARCHITECTURE.\*\*

\## Task 4 — Online Dataset Investigation



\### 4.1 Objective



The purpose of this investigation is to identify existing online datasets that could potentially provide useful business or financial data for MetricMind.



The datasets are evaluated based on:



\- Business relevance.

\- Available columns.

\- Support for revenue, cost, profit and margin metrics.

\- Customer and product information.

\- Regional analysis.

\- Ease of integration.

\- Whether the dataset provides meaningful additional value compared with the current PostgreSQL database.



\### 4.2 Dataset 1 — UCI Online Retail



Source: UCI Machine Learning Repository



The UCI Online Retail dataset contains real-world online retail transaction data.



Important columns include:



\- InvoiceNo

\- StockCode

\- Description

\- Quantity

\- InvoiceDate

\- UnitPrice

\- CustomerID

\- Country



The dataset can support transaction, product, customer, quantity, price and geographical analysis.



However, it does not directly provide all the business metrics currently available in MetricMind. In particular, it does not directly contain cost, profit or margin columns.



Therefore, additional calculations or assumptions would be required to produce some of MetricMind's existing metrics.



\### 4.3 Dataset 2 — Superstore Sales Dataset



The Superstore dataset contains retail sales information across products, customers and regions.



Important columns include:



\- Order Date

\- Customer information

\- Customer Segment

\- Region

\- Product Category

\- Product Name

\- Sales

\- Profit

\- Discount

\- Quantity

\- Shipping information



This dataset is highly relevant to business analytics because it supports sales, profit, discount, product, customer and regional analysis.



However, MetricMind already contains similar structured business information in PostgreSQL.



Therefore, although the Superstore dataset is suitable for business analytics, it does not provide a strong enough reason to replace the existing MetricMind database.



\### 4.4 Dataset 3 — Global E-Commerce Sales \& Customer Data



This dataset contains:



\- Order Date

\- Customer Name

\- Customer Segment

\- Country

\- Region

\- Product Category

\- Product Name

\- Quantity

\- Unit Price

\- Discount

\- Total Sales

\- Shipping Cost

\- Profit

\- Payment Method



This dataset is highly relevant to MetricMind because it contains sales, profit, customer, product and regional information.



It could potentially be useful for additional experimentation or comparison.



However, the existing MetricMind PostgreSQL database already contains the major business metrics required by the project, including revenue, cost, profit and margin.



Therefore, this dataset does not justify replacing the current database.



\### 4.5 Dataset Comparison



| Dataset | Business Relevance | Revenue/Sales | Cost | Profit | Customer Data | Product Data | Region | Additional Value |

|---|---|---|---|---|---|---|---|---|

| UCI Online Retail | High | Yes/derivable | No | No | Yes | Yes | Country | Useful for retail experimentation |

| Superstore Sales | High | Yes | Limited | Yes | Yes | Yes | Yes | Similar to current data |

| Global E-Commerce Sales | High | Yes | Shipping cost | Yes | Yes | Yes | Yes | Useful for comparison |

| Current MetricMind PostgreSQL | Very High | Yes | Yes | Yes | Yes | Yes | Yes | Already integrated with backend |



\### 4.6 Integration Consideration



Any online dataset would need to be cleaned and transformed before being integrated into MetricMind.



Integration could require:



\- Mapping different column names.

\- Converting data types.

\- Handling missing values.

\- Creating relationships between customers, products and sales.

\- Calculating missing business metrics.

\- Updating backend queries.

\- Updating the semantic layer.

\- Testing the new data.



Therefore, simply adding an online dataset would introduce additional work.



\### 4.7 Does an Online Dataset Provide More Value?



The investigated datasets are useful for experimentation and comparison.



However, the current MetricMind PostgreSQL database already provides the structured data required for the project's current business metrics.



The online datasets do not provide enough additional value to justify replacing the current database.



They could potentially be used in the future for:



\- Testing.

\- Benchmarking.

\- Additional analytics.

\- Demonstrating the system with alternative datasets.



\### 4.8 Task 4 Conclusion



The investigation found several relevant online business and retail datasets.



The datasets are useful for business analytics, but none provides a sufficiently strong reason to replace the current PostgreSQL database.



Therefore, the recommended approach is:



\*\*KEEP THE CURRENT POSTGRESQL DATABASE.\*\*



Online datasets may be retained as optional sources for future experimentation and benchmarking.

