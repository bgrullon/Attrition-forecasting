# Attrition-Forecasting

**PreReqs**
- Install [Terraform](https://developer.hashicorp.com/terraform/install?product_intent=terraform)
- Start Docker
```
docker build -t flask-api .
docker run -p 5000:5000 flask-api
```
# Requirements
**Data Model Implementation**
- A Python script initializes, trains, and evaluates a model
- The data is cleaned, normalized, and standardized prior to modeling
- The model utilizes data retrieved from SQL or Spark
- The model demonstrates meaningful predictive power at least 75% classification accuracy or 0.80 R-squared.

**Data Model Optimization**
- The model optimization and evaluation process showing iterative changes made to the model and the resulting changes in model performance is documented in either a CSV/Excel table or in the Python script itself
- Overall model performance is printed or displayed at the end of the script


