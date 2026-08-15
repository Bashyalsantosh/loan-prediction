 Loan Default Prediction SystemThis project leverages Machine Learning to predict the likelihood of loan defaults, enabling financial institutions to manage credit risk effectively. By analyzing key customer attributes, the model provides actionable insights for lending decisions.


 
 🚀 Project Overview:
 The core objective of this project is to assist banks in identifying high-risk loan applicants. Using a Random Forest Classifier, the system achieves an accuracy of 93%, significantly aiding in the reduction of Non-Performing Assets (NPAs).
 
 
 📊 Model Performance:
 The model has been evaluated using a classification report, highlighting the following metrics
 MetricScoreAccuracy93%Precision90%Recall77%


Tech StackLanguage: PythonMachine Learning: Scikit-LearnData Manipulation: Pandas, NumPyFrontend: StreamlitDeployment: Streamlit Cloud / AWS📂 Project StructurePlaintextloan-prediction/

 
Repository Structure
nrb-loan-risk-engine/
│
├── app.py                      # Interactive Streamlit Executive Dashboard
├── medallion_pipeline.py       # End-to-End PySpark Lakehouse & ML Engine
├── kafka_producer.py           # Real-Time Loan Application Stream Simulator
├── requirements.txt            # Python Package Dependencies
├── Pyspark.sql                  # Git Exclusion Rules & Checkpoint Masks
└── README.md                   # Complete System Documentation


Key Features:
* ⚡ **Streaming Ingestion:** Real-time stream processing using **Apache Kafka** and **PySpark Structured Streaming**.
* 🥉 **Bronze Layer:** Schema-enforced raw Parquet lakehouse storage.
* 🥈 **Silver Layer:** Feature engineering computing dynamic **Debt-to-Income (DTI)** and **Loan-to-Value (LTV)** ratios.
* 🥇 **Gold Layer:** Machine Learning classification powered by **PySpark Gradient Boosted Trees (GBT) / XGBoost**.
* 📊 **Executive Dashboard:** Dark-themed financial UI featuring real-time risk gauges, dataset visualizer, and live loan evaluator.


2. Running the AppLaunch the interactive web interface locally:Bashstreamlit run app.py
🤝 ContributingContributions are welcome! If you have suggestions for improving the model or the user interface, please fork the repository and submit a pull request.Developed as a Data Engineering Projects.
