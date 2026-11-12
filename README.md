🔐 AI-Based Ransomware Detection and Secure File Protection
An intelligent cybersecurity application that combines Machine Learning-based ransomware detection with AES-256-GCM encryption and decryption to provide an additional layer of file protection.
📌 Project Overview
Ransomware is a type of malicious software that encrypts or restricts access to files, demanding payment to restore access.
This project aims to develop a system that uses Machine Learning to identify potentially malicious ransomware-related data and provides secure file encryption and decryption functionality.
The application uses a Streamlit-based interface, making the system accessible through a web browser.
🎯 Objectives

Detect ransomware-related activity using Machine Learning.
Classify data using a trained Random Forest model.
Provide secure file encryption using AES-256-GCM.
Enable file decryption and recovery using the appropriate key.
Provide an interactive cybersecurity dashboard.

🛠️ Technologies Used



Technology
Purpose




Python
Core programming language


Streamlit
Web application interface


Scikit-learn
Machine Learning


Random Forest
Classification algorithm


Pandas
Data processing


NumPy
Numerical computation


Cryptography
AES encryption and decryption


Joblib
Model serialization



🚀 Key Features
1. AI-Based Ransomware Detection

Upload CSV datasets.
Analyse input features using a trained Random Forest model.
Generate classification predictions.
Display detection results.

2. Secure File Encryption

Upload files for encryption.
Encrypt file contents using AES-256-GCM.
Generate authenticated encrypted output.

3. File Decryption

Upload encrypted files.
Provide the corresponding recovery key.
Decrypt files and recover their original contents.

🧠 Machine Learning Model
Algorithm: Random Forest Classifier
Reported Model Accuracy: 98.19%
The model was trained using ransomware-related dataset features to distinguish between benign and ransomware-labelled samples.
Note: Accuracy is a reported experimental result and should be reproduced using the provided training pipeline before being treated as independently verified performance.
🔒 Encryption Methodology
The application uses AES-256-GCM.
Key characteristics:

256-bit encryption key.
Authenticated encryption.
Integrity verification.
Secure decryption using the correct key.

Encryption keys must be stored securely and must never be committed to the public repository.
📂 Project Structure
ransomware/
│
├── app.py
├── train_model.py
├── save_model.py
├── crypto_module.py
├── feature_importance.py
├── inspect_dataset.py
├── test_crypto.py
│
├── ransomware_model.pkl
├── feature_names.pkl
│
├── requirements.txt
├── README.md
└── .gitignore

⚙️ Installation and Setup
Prerequisites

Python
pip
Git

1. Clone the repository
git clone YOUR_REPOSITORY_URL

2. Navigate to the project directory
cd ransomware

3. Install dependencies
pip install -r requirements.txt

4. Run the application
streamlit run app.py

The application will open in your default web browser.
⚠️ Security Disclaimer
This project is developed for educational and research purposes.

Do not test with real ransomware.
Do not upload sensitive personal files.
Keep encryption keys private.
Never execute suspicious files.
Do not treat ML predictions as a guarantee of malware detection.

👩‍💻 Project Purpose
This project demonstrates the practical application of Machine Learning and cryptography in cybersecurity, combining intelligent classification with secure file protection.
