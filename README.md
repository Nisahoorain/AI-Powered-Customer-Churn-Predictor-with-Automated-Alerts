# AI-Powered Customer Churn Predictor with Automated Alerts

## Project Overview

This project is an end-to-end AI-powered customer churn prediction system that helps businesses identify at-risk customers and automatically trigger retention actions through Zapier integrations.

## Business Value

**Problem Solved:** Companies lose revenue when customers cancel subscriptions or stop using services. Traditional methods of identifying at-risk customers are reactive and often too late.

**Solution:** This system uses machine learning to predict churn probability in real-time, allowing businesses to proactively reach out to high-risk customers with retention offers before they cancel.

**ROI:** Companies can save $50,000-$200,000+ annually by retaining just 5-10% of customers who would have churned, while reducing customer acquisition costs by focusing retention efforts on the right customers.

## Features

- 🤖 **ML-Powered Predictions**: Trained model with ≥80% accuracy using Random Forest/XGBoost
- 📊 **Interactive Dashboard**: Streamlit web app for easy customer data upload and visualization
- 🚨 **Automated Alerts**: Zapier integration for instant Slack/Gmail/Google Sheets notifications
- 🎯 **Risk Highlighting**: Visual indicators for high-risk customers requiring immediate attention

## Tech Stack

- **Machine Learning**: scikit-learn, XGBoost/LightGBM
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Web App**: Streamlit
- **Automation**: Zapier Webhooks
- **Deployment**: Streamlit Community Cloud

## Project Structure

```
customer-churn-zapier/
├── 1_Train_Model.ipynb      # Model training notebook with EDA
├── churn_app.py             # Streamlit dashboard application
├── churn_model.pkl          # Trained model file
├── test_customers.csv       # Sample test data
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── .gitignore
```

## Live Demo

🔗 **Streamlit Dashboard**: [Your Streamlit App Link Here]

📹 **Demo Video**: [Your Loom Video Link Here]

## How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourname/customer-churn-zapier.git
   cd customer-churn-zapier
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app**
   ```bash
   streamlit run churn_app.py
   ```

5. **Access the dashboard**
   - Open your browser to `http://localhost:8501`

## Model Performance

- **Algorithm**: [Random Forest / XGBoost / LightGBM]
- **Accuracy**: [XX%]
- **Precision**: [XX%]
- **Recall**: [XX%]

## Zapier Integration

The app integrates with Zapier to send automated alerts when high-risk customers are identified. Configure your Zapier webhook URL in `churn_app.py` to enable:
- Slack channel notifications
- Gmail alerts with customer details
- Google Sheets logging
- Custom workflow automations

## Dataset

This project uses the [Telco Customer Churn dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) from Kaggle, containing customer information, services subscribed, account details, and churn status.

## License

MIT License

## Author

[Your Name]

---

*This project was built as part of a data science bootcamp assignment demonstrating real-world ML application and automation integration.*

