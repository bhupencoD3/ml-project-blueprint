
# 🧠 Student Score Predictor

A machine learning web application that predicts a student's math score based on personal and academic attributes. Built with love, logic, and a sprinkle of statistical magic.

---

## 🚀 Live Demo

👉 [**Try it here**](http://bhupen.ap-south-1.elasticbeanstalk.com/)

---

## 📸 Screenshots

| Home Page | Input Form | Prediction Result |
|-----------|------------|-------------------|
| ![Home](https://github.com/bhupencoD3/ml-project-blueprint/blob/main/screenshots/home.jpg) | ![Form](https://github.com/bhupencoD3/ml-project-blueprint/blob/main/screenshots/form.jpg) | ![Result](https://github.com/bhupencoD3/ml-project-blueprint/blob/main/screenshots/prediction.jpg) |

| About Us Page |
|---------------|
| ![About Us](https://github.com/bhupencoD3/ml-project-blueprint/blob/main/screenshots/aboutus.jpg) |

---

## 🔍 Features

- 🎯 Predicts student math score using a trained machine learning model
- 📝 Clean, modern input form
- 📊 Displays predictions on a dedicated result page
- 📱 Mobile-friendly, responsive design
- ☁️ Deployed on AWS Elastic Beanstalk

---

## 🧪 Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **ML:** scikit-learn, pandas, numpy, joblib
- **Deployment:** AWS Elastic Beanstalk, GitHub, CodePipeline

---

## 🧠 How It Works

1. User inputs details via a form  
2. Backend loads a trained model and preprocessor  
3. Model processes input and predicts math score  
4. Result is shown on a new result page  

---

## 📂 Directory Structure

```
bhupencod3-ml-project-blueprint/
├── README.md
├── application.py
├── requirements.txt
├── runtime.txt
├── setup.py
├── artifacts/
│   ├── data.csv
│   ├── model.pkl
│   ├── model_scores.yaml
│   ├── preprocessor.pkl
│   ├── test.csv
│   └── train.csv
├── config/
│   └── hyperparams.yaml
├── notebook/
│   ├── EDA_STUDENT_PERFORMANCE.ipynb
│   ├── MODEL_TRAINING.ipynb
│   └── data/
│       └── StudentsPerformance.csv
├── src/
│   ├── __init__.py
│   ├── exception.py
│   ├── logger.py
│   ├── utils.py
│   ├── component/
│   │   ├── __init__.py
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   ├── model_hyperparameter_tuning.py
│   │   └── model_trainer.py
│   └── pipeline/
│       ├── __init__.py
│       ├── predict_pipeline.py
│       └── train_pipeline.py
├── static/
│   ├── script.js
│   └── style.css
├── templates/
│   ├── about.html
│   ├── home.html
│   ├── index.html
│   └── result.html
└── .ebextensions/
    └── python.config
```

---

## ⚙️ Installation

To run the project locally:

```bash
git clone https://github.com/bhupencoD3/ml-project-blueprint.git
cd ml-project-blueprint
pip install -r requirements.txt
python application.py
```

Open your browser and visit: `http://localhost:5000`

---

## 🔬 Model Info

- **Type:** Regression (Linear/Random Forest/etc.)
- **Target:** Math Score (0 - 100)
- **Features:**
  - Gender
  - Race/Ethnicity
  - Parental Education
  - Lunch Type
  - Test Preparation Course

---

## 📬 Contact

**Made by Bhupendra Parmar**  
📧 bhupenparmar192@gmail.com  
🌐 [CodeTheMatrix.com](https://codethematrix.com) *(coming soon)*  
👤 [LinkedIn](https://www.linkedin.com/in/bhupendra-parmar-275b29291/) | [GitHub](https://github.com/bhupencoD3)

---

## 📜 License

Licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more info.

---

> “We are not defined by what we know, but by how we learn to understand.”

