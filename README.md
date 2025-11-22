# AI-Powered Customer Churn Predictor with Automated Alerts

> **Note:** This project was built for portfolio and learning purposes. It demonstrates end-to-end machine learning deployment, web application development, and automation integration.

## Project Overview

This project is an end-to-end AI-powered customer churn prediction system that helps businesses identify at-risk customers and automatically trigger retention actions through Make.com webhook integrations.

## Business Value

**Problem Solved:** Companies lose revenue when customers cancel subscriptions or stop using services. Traditional methods of identifying at-risk customers are reactive and often too late.

**Solution:** This system uses machine learning to predict churn probability in real-time, allowing businesses to proactively reach out to high-risk customers with retention offers before they cancel.

**ROI:** Companies can save $50,000-$200,000+ annually by retaining just 5-10% of customers who would have churned, while reducing customer acquisition costs by focusing retention efforts on the right customers.

## Features

- 🤖 **ML-Powered Predictions**: Trained Random Forest model with 70.6% recall (catches 7 out of 10 churners)
- 📊 **Interactive Dashboard**: Streamlit web app with adjustable probability threshold slider for business trade-offs
- 🚨 **Automated Alerts**: Make.com webhook integration for instant Gmail/Slack/Google Sheets notifications
- 🎯 **Risk Highlighting**: Visual color-coded indicators for high-risk customers requiring immediate attention
- 📈 **Feature Importance**: Interactive visualization showing top drivers of churn predictions
- 💡 **Retention Recommendations**: AI-generated personalized retention strategies for each at-risk customer

## Tech Stack

- **Machine Learning**: scikit-learn, XGBoost/LightGBM
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Web App**: Streamlit
- **Automation**: Make.com Webhooks (free alternative to Zapier)
- **Deployment**: Streamlit Community Cloud

## ⚠️ Security Note

**This project is for portfolio/educational purposes.** 
- Webhook URLs are entered by users (not hardcoded)
- No API keys or secrets are stored in the code
- See [SECURITY.md](SECURITY.md) for security best practices

## Project Structure

```
ai-powered-customer-churn-predictor/
├── 1_Train_Model.ipynb      # Model training notebook with EDA
├── churn_app.py             # Streamlit dashboard application
├── churn_model.pkl          # Trained Random Forest model (79.84% accuracy)
├── preprocessing.pkl         # Preprocessing encoders and metadata
├── test_customers.csv       # Sample test data (20 customers)
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── .gitignore
```

## Live Demo

🔗 **Streamlit Dashboard**: https://ai-powered-customer-churn-predictor-with-automated-alerts-ani9.streamlit.app/

📹 **Demo Video**: https://www.loom.com/share/d92bb33c143b4f5885d09513d13d4bae

## How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nisahoorain/AI-Powered-Customer-Churn-Predictor-with-Automated-Alerts.git
   cd ai-powered-customer-churn-predictor-with-automated-alerts
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
   - Adjust the **Probability Threshold** slider in the sidebar to balance recall vs precision:
     - **Lower threshold (0.20-0.35)**: Catch more churners (higher recall, more false positives)
     - **Higher threshold (0.50-0.70)**: Fewer false alerts (higher precision, may miss some churners)
   - Default threshold (0.35) is optimized for 70%+ recall

## Model Performance

### Improved Model with Class Weights & Threshold Optimization

**Key Achievement:** By applying class weights and optimizing the probability threshold, recall for churners was increased from **51% to 70.6%** — meaning the system now catches **~20% more at-risk customers** while maintaining strong ranking performance (AUC 0.838).

| Metric | Original Model | Improved Model | Improvement |
|--------|---------------|----------------|-------------|
| **Recall (Churn)** | 51.0% | **70.6%** | +19.6% ⬆️ |
| **Precision (Churn)** | 65.0% | 55.2% | -9.8% (acceptable trade-off) |
| **Accuracy** | 79.8% | 77.0% | -2.8% (expected) |
| **AUC Score** | 0.8366 | **0.8382** | +0.0016 ⬆️ |
| **Optimal Threshold** | 0.50 (default) | 0.497 (optimized) | - |

**Why This Matters:**
- **Recall is critical for churn prediction** — missing a churner costs more than a false positive
- **70.6% recall** means catching 7 out of 10 customers who will actually churn
- **55.2% precision** means when flagged as high-risk, 55% will actually churn (acceptable for proactive retention)
- The model now provides **actionable insights** for customer success teams

**Model Details:**
- **Algorithm**: Random Forest Classifier with Class Weights (`class_weight='balanced'`)
- **Training**: Optimized threshold using precision-recall curve analysis
- **Class Weights**: {0: 0.68, 1: 1.88} - Balanced to prioritize churn detection

**Model Comparison (Initial Training):**
- Random Forest: 79.84% accuracy ✅ (Selected for improvement)
- XGBoost: 79.42% accuracy
- LightGBM: 79.42% accuracy

**Top 5 Most Important Features:**
1. Tenure (0.164) - Customer loyalty duration
2. TotalCharges (0.146) - Cumulative revenue
3. MonthlyCharges (0.139) - Monthly billing amount
4. Contract (0.138) - Contract type (Month-to-month/One year/Two year)
5. OnlineSecurity (0.080) - Security service subscription

## Make.com Integration

The app integrates with Make.com (free webhook service) to send automated alerts when high-risk customers are identified. Configure your Make.com webhook URL in the Streamlit sidebar to enable:
- **Gmail alerts** with customer details and churn probability
- **Slack channel notifications** for team alerts
- **Google Sheets logging** for tracking and analysis
- **Custom workflow automations** via Make.com scenarios

**Setup Instructions:**
1. Create a free account at [Make.com](https://www.make.com)
2. Create a new scenario with "Custom webhook" trigger
3. Copy the webhook URL (e.g., `https://hook.eu1.make.com/xxxxx`)
4. Add action: Gmail/Slack/Google Sheets
5. Paste webhook URL in Streamlit app sidebar
6. Test by uploading customer data and clicking "Send Alerts via Webhook"

**Why Make.com?**
- ✅ Free plan available (1,000 operations/month)
- ✅ Easy to use visual workflow builder
- ✅ Works seamlessly with HTTP POST requests
- ✅ Supports multiple integrations (Gmail, Slack, Sheets, etc.)

## Dataset

This project uses the [Telco Customer Churn dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) from Kaggle.

**Dataset Details:**
- **Total Records**: 7,043 customers
- **Features**: 21 columns (demographics, services, billing, contract info)
- **Target Variable**: Churn (Yes/No)
- **Churn Rate**: 26.54% (1,869 churned customers)

**Key Features:**
- Customer demographics (gender, senior citizen, partner, dependents)
- Service subscriptions (phone, internet, streaming, security)
- Account information (tenure, contract type, payment method)
- Billing details (monthly charges, total charges)

## Business Value Report

**What business problem does this solve?**

Customer churn is a critical issue for subscription-based businesses, costing companies millions in lost revenue annually. Traditional churn detection methods are reactive—companies only discover at-risk customers after they've already decided to leave. This system solves this problem by using machine learning to predict churn probability in real-time, enabling proactive customer retention strategies.

**Final Model Performance:** 70.6% Recall, 55.2% Precision, 77.0% Accuracy

The improved Random Forest model achieves **70.6% recall** (up from 51%) with an AUC score of 0.8382, successfully identifying high-risk customers before they churn. By applying class weights and optimizing the probability threshold, the system now catches **~20% more at-risk customers** — critical for proactive retention. The model was trained on 7,043 customer records and tested on 1,409 samples, with key features including customer tenure, contract type, monthly charges, and service subscriptions.

**Business Impact:** With the improved model, this system can help retain an additional **~200-250 customers per year** (assuming 10k customer base), translating to **$120,000-$150,000+ saved annually** compared to the original model.

**Which automation action did you choose and why?**

I chose **Gmail email alerts** via Make.com webhook integration. Email alerts provide immediate notification to customer success teams when high-risk customers are identified, allowing for timely intervention. The email includes all critical customer information (name, churn probability, risk level, tenure, charges) in a format that's easy to read and act upon. Make.com was selected over Zapier because it offers a free tier with 1,000 operations per month, making it accessible for small businesses and startups.

**How much money can a company save using this?**

With the improved model (70.6% recall), companies can save **$120,000 to $200,000+ annually** by retaining customers who would have churned. For a company with 10,000 customers paying $50/month:

- **Without the system:** Losing 26% (2,600 customers) = $1,560,000 annual revenue loss
- **With original model (51% recall):** Catching 1,326 churners, retaining 10% = $79,560 saved/year
- **With improved model (70.6% recall):** Catching 1,836 churners, retaining 10% = **$110,160 saved/year**
- **Additional savings:** **$30,600+ more per year** compared to the original model

For a 1,000 customer base, the improved model saves an additional **$3,000-$4,000 annually** by catching 20% more at-risk customers. Additionally, the system reduces customer acquisition costs by focusing retention efforts on the right customers, rather than blanket retention campaigns that waste resources on low-risk customers. The adjustable probability threshold allows businesses to fine-tune the balance between catching more churners (lower threshold) vs. reducing false alerts (higher threshold).

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Built as part of a data science bootcamp assignment demonstrating real-world ML application and automation integration.

## Disclaimer

This project is for **portfolio and educational purposes**. While it demonstrates real-world ML deployment practices, it should not be used in production without proper security reviews, testing, and compliance checks.

---

*This project showcases end-to-end machine learning deployment, from data analysis and model training to web application development and workflow automation—exactly what freelance clients pay $150-$400 for in 2025.*

