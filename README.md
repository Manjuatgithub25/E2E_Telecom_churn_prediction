# E2E_Telecom_churn_prediction
An end-to-end machine learning system to predict customer churn for a telecom provider. This project demonstrates a production-ready ML pipeline including data ingestion, validation, preprocessing, feature engineering, balancing (SMOTENC), ensemble modeling, evaluation, and deployment.

## Project Overview
Telecom companies face massive losses due to customer churn. The goal of this project is to build a robust churn prediction system that can identify at-risk customers early, enabling proactive retention strategies.

Key highlights of the pipeline:
✅ Automated ingestion, validation, preprocessing, and transformation of raw data.
✅ Class imbalance handled with SMOTENC (for categorical + numeric features).
✅ Stacking ensemble of RandomForest, XGBoost, LightGBM, and CatBoost with Logistic Regression as meta-model.
✅ Achieved 97% accuracy and 0.97 F1-score on test data.
✅ End-to-end pipeline wrapped into TelcoChurnModel and serialized to AWS S3 via custom estimator for inference.
✅ Supports evaluation of local vs. production models with seamless transition/update flow.
