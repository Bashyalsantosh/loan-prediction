 Loan Default Prediction SystemThis project leverages Machine Learning to predict the likelihood of loan defaults, enabling financial institutions to manage credit risk effectively. By analyzing key customer attributes, the model provides actionable insights for lending decisions.


 
 🚀 Project OverviewThe core objective of this project is to assist banks in identifying high-risk loan applicants. Using a Random Forest Classifier, the system achieves an accuracy of 93%, significantly aiding in the reduction of Non-Performing Assets (NPAs).
 
 📊 Model PerformanceThe model has been evaluated using a classification report, highlighting the following metrics:MetricScoreAccuracy93%Precision90%Recall77%
 🛠 Tech StackLanguage: PythonMachine Learning: Scikit-LearnData Manipulation: Pandas, NumPyFrontend: StreamlitDeployment: Streamlit Cloud / AWS📂 Project StructurePlaintextloan-prediction/

 
├── app.py              # Main Streamlit web application
├── loan_model.pkl      # Pre-trained Random Forest model
├── requirements.txt    # Python dependencies
└── loandata.csv        # Dataset used for training

💡 Key InsightsOur feature importance analysis revealed the top three drivers of loan defaults:Previous Loan Defaults: Historical repayment behavior is the strongest indicator of future risk.Loan-to-Income Ratio: High debt burden relative to income significantly increases risk.Interest Rates: Higher interest rates often correlate with riskier borrower profiles.💻 Getting Started1. InstallationClone the repository and install the required dependencies:Bashgit clone https://github.com/your-username/loan-prediction.git
cd loan-prediction
pip install -r requirements.txt
2. Running the AppLaunch the interactive web interface locally:Bashstreamlit run app.py
🤝 ContributingContributions are welcome! If you have suggestions for improving the model or the user interface, please fork the repository and submit a pull request.Developed as a Data Engineering Projects.
