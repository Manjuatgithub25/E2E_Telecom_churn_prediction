# E2E_Telecom_churn_prediction

An end-to-end machine learning system to predict customer churn for a telecom provider. This project demonstrates a production-ready ML pipeline including data ingestion, validation, preprocessing, feature engineering, balancing (SMOTENC), ensemble modeling, evaluation, and deployment.


## Project Overview

Telecom companies face massive losses due to customer churn. The goal of this project is to build a robust churn prediction system that can identify at-risk customers early, enabling proactive retention strategies.

Key highlights of the pipeline:
* Automated ingestion, validation, preprocessing, and transformation of raw data.
* Class imbalance handled with SMOTENC (for categorical + numeric features).
* Stacking ensemble of RandomForest, XGBoost, LightGBM, and CatBoost with Logistic Regression as meta-model.Achieved 97% accuracy and 0.97 F1-score on test data.
* End-to-end pipeline wrapped into TelcoChurnModel and serialized to AWS S3 via custom estimator for inference.
* Supports evaluation of local vs. production models with seamless transition/update flow.

## Repository Structure

E2E_Telecom_churn_prediction/
│
├── Telecom_churn_prediction/       # Core ML pipeline code (ingestion, validation, transformation, training)
├── notebooks/                      # Jupyter notebooks for EDA and experimentation
├── app.py                          # Web API (Flask/FastAPI/Streamlit) for inference
├── Dockerfile                      # Containerization for deployment
├── requirements.txt                # Python dependencies
├── setup.py                        # Packaging script
├── template.py / tcp.json          # Config templates
├── Telco_Customer_Churn.csv        # Raw dataset (optional / example data)
└── README.md                       # Project documentation

## Dataset

* Source: Telco Customer Churn Dataset (Kaggle)
* Size: ~14,000 rows × 21 features
* Target variable: Churn (Yes/No)
* Features include: demographics, contract type, billing info, tenure, services subscribed
* Preprocessing:
  * Handle missing values & inconsistent types (TotalCharges)
  * Encode categorical features
  * Normalize numerical variables
  * Apply SMOTENC to balance classes

## Pipeline & Workflow

* ### Data Ingestion
  Reads raw CSV, validates schema, handles missing values
* ### Data Validation & Transformation
  Encodes categorical + scales numerical features
  Handles outliers and type conversions
* ### Balancing
  Uses SMOTENC to oversample churn class without breaking categorical features
* ### Model Training
  Base models: RandomForest, XGBoost, LightGBM, CatBoost
  Meta-model: Logistic Regression (stacking ensemble)
* ### Evaluation
  Metrics: Accuracy, Precision, Recall, F1, ROC-AUC
  Confusion matrix comparison: Local vs Production models
* ### Model Packaging & Deployment
  TelcoChurnModel wraps preprocessing + model in one pipeline
  Serialized with pickle and stored in AWS S3
  Served via FastAPI (app.py) and Dockerized

## Results

* Test Accuracy: ~97%
* F1-Score: 0.97
* Recall (Churn class): ~0.96

Outperformed baseline models and provided stable generalization.
These metrics indicate that the model is reliable for identifying churners, which is often more valuable than overall accuracy.

## Technologies Used

* Languages & Libraries: Python, Pandas, NumPy, Scikit-learn, XGBoost, LightGBM, CatBoost, imbalanced-learn, Matplotlib, Seaborn
* Model Management: Custom Estimator, Pickle, AWS S3
* Deployment: FastAPI, Docker
* Tools: Jupyter, Git, VS Code

## Local Setup

* Clone repo
  git clone https://github.com/Manjuatgithub25/E2E_Telecom_churn_prediction.git
  cd E2E_Telecom_churn_prediction

* Create venv
  python3 -m venv venv
  source venv/bin/activate  # (Linux/Mac)
  venv\Scripts\activate     # (Windows)

* Install dependencies
  pip install -r requirements.txt

* Run the app
  python app.py

## AWS-CICD-Deployment-with-Github-Actions

* Create IAM user for deployment
  * Policy:
    AmazonEC2ContainerRegistryFullAccess
    AmazonEC2FullAccess
    AmazonS3FullAccess
* Create ECR repo to store/save docker image
* Create EC2 machine (Ubuntu). Connect EC2 instance and Install docker in EC2 Machine:
  * curl -fsSL https://get.docker.com -o get-docker.sh
  * sudo sh get-docker.sh
  * sudo usermod -aG docker ubuntu
  * newgrp docker
* Configure EC2 as self-hosted runner:
  Create a new self-hosted runner in Github settings -> Action -> runners -> create self-hosted and run the given comments in docker.
* Setup github secrets:
  AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY
  AWS_DEFAULT_REGION
  ECR_REPO

## License

This project is licensed under the MIT License.
