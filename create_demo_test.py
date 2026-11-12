import streamlit as st
import pandas as pd
import joblib
import tempfile
import os

from crypto_module import encrypt_file, decrypt_file


# =========================================================
# LOAD MODEL
# =========================================================

model = joblib.load("ransomware_model.pkl")
feature_names = joblib.load("feature_names.pkl")


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="AI Ransomware Detection & Prevention",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI-Based Ransomware Detection & Prevention")

st.write(
    "Random Forest detects ransomware behavior and "
    "AES-256-GCM protects important files through "
    "an encrypted recovery backup."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🛡️ Security System")

st.sidebar.write("### AI")
st.sidebar.write("Algorithm: Random Forest")
st.sidebar.write("Learning: Supervised Learning")
st.sidebar.write("Features: 19 behavioral features")

st.sidebar.write("### Cryptography")
st.sidebar.write("Algorithm: AES-256-GCM")
st.sidebar.write("Key Derivation: PBKDF2-SHA256")


# =========================================================
# TABS
# =========================================================

tab1, tab2 = st.tabs([
    "🧠 Detect & Protect",
    "🔓 Recover Backup"
])


# =========================================================
# TAB 1
# =========================================================

with tab1:

    st.header("🧠 Ransomware Detection & Automatic Protection")

    st.write(
        "Step 1: Upload behavioral activity data for AI analysis."
    )

    behavioral_file = st.file_uploader(
        "📊 Upload Behavioral CSV",
        type=["csv"],
        key="behavioral"
    )

    st.write(
        "Step 2: Select the important file that should be "
        "protected if ransomware is detected."
    )

    important_file = st.file_uploader(
        "📄 Upload Important File",
        key="important"
    )

    password = st.text_input(
        "🔐 Protection password",
        type="password",
        key="protection_password"
    )

    if behavioral_file is not None:

        data = pd.read_csv(behavioral_file)

        st.subheader("Behavioral Data Preview")
        st.dataframe(data.head())

        prediction_data = data.copy()

        # Remove label if present
        if "Ware Type" in prediction_data.columns:
            prediction_data = prediction_data.drop(
                "Ware Type",
                axis=1
            )

        # Check features
        missing_features = [
            feature
            for feature in feature_names
            if feature not in prediction_data.columns
        ]

        if missing_features:

            st.error(
                "Missing required behavioral features: "
                + ", ".join(missing_features)
            )

        else:

            prediction_data = prediction_data[
                feature_names
            ]

            if st.button(
                "🔍 Analyze & Protect",
                type="primary"
            ):

                # ---------------------------------------------
                # AI PREDICTION
                # ---------------------------------------------

                predictions = model.predict(
                    prediction_data
                )

                probabilities = model.predict_proba(
                    prediction_data
                )

                ransomware_count = int(
                    (predictions == 1).sum()
                )

                benign_count = int(
                    (predictions == 0).sum()
                )

                total_samples = len(predictions)

                # ---------------------------------------------
                # RESULTS
                # ---------------------------------------------

                st.subheader("Detection Summary")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Total Samples",
                        total_samples
                    )

                with col2:
                    st.metric(
                        "🟢 Benign",
                        benign_count
                    )

                with col3:
                    st.metric(
                        "🔴 Ransomware",
                        ransomware_count
                    )

                # ---------------------------------------------
                # THREAT DETECTED
                # ---------------------------------------------

                if ransomware_count > 0:

                    st.error(
                        "🚨 RANSOMWARE THREAT DETECTED"
                    )

                    st.warning(
                        f"Random Forest detected "
                        f"{ransomware_count} ransomware "
                        f"sample(s) in the uploaded behavioral data."
                    )

                    # -----------------------------------------
                    # AUTOMATIC BACKUP
                    # -----------------------------------------

                    if important_file is not None:

                        if password:

                            with tempfile.TemporaryDirectory() as temp_dir:

                                original_path = os.path.join(
                                    temp_dir,
                                    important_file.name
                                )

                                backup_path = os.path.join(
                                    temp_dir,
                                    important_file.name + ".enc"
                                )

                                # Save uploaded file temporarily
                                with open(
                                    original_path,
                                    "wb"
                                ) as file:

                                    file.write(
                                        important_file.getbuffer()
                                    )

                                # AES encryption
                                encrypt_file(
                                    original_path,
                                    backup_path,
                                    password
                                )

                                # Read encrypted backup
                                with open(
                                    backup_path,
                                    "rb"
                                ) as file:

                                    encrypted_backup = file.read()

                            st.success(
                                "🔐 AES-256-GCM encrypted backup "
                                "created successfully!"
                            )

                            st.info(
                                "🛡️ The original uploaded file "
                                "was not modified. A protected "
                                "encrypted recovery copy was created."
                            )

                            st.download_button(
                                "⬇️ Download Protected Backup",
                                encrypted_backup,
                                file_name=(
                                    important_file.name + ".enc"
                                ),
                                mime="application/octet-stream"
                            )

                        else:

                            st.warning(
                                "⚠️ Threat detected, but no "
                                "protection password was provided. "
                                "Enter a password and analyze again "
                                "to create the encrypted backup."
                            )

                    else:

                        st.warning(
                            "⚠️ Threat detected. Upload an important "
                            "file to create its protected recovery backup."
                        )

                    # -----------------------------------------
                    # PREVENTION RESPONSE
                    # -----------------------------------------

                    st.error(
                        "🛑 PREVENTION RESPONSE: "
                        "Suspicious activity has been flagged."
                    )

                    st.info(
                        "The system recommends stopping the "
                        "suspicious activity and recovering the "
                        "original file from the protected backup."
                    )

                # ---------------------------------------------
                # NO THREAT
                # ---------------------------------------------

                else:

                    st.success(
                        "🟢 NO RANSOMWARE THREAT DETECTED"
                    )

                    st.info(
                        "The analyzed behavioral activity "
                        "was classified as benign."
                    )

                # ---------------------------------------------
                # DETAILED RESULTS
                # ---------------------------------------------

                st.subheader("Detailed AI Results")

                results = prediction_data.copy()

                results["Prediction"] = [
                    "🔴 Ransomware"
                    if prediction == 1
                    else "🟢 Benign"
                    for prediction in predictions
                ]

                results["Confidence (%)"] = (
                    probabilities.max(axis=1) * 100
                ).round(2)

                st.dataframe(results)

                # Download results
                results_csv = results.to_csv(
                    index=False
                )

                st.download_button(
                    "⬇️ Download Detection Results",
                    results_csv,
                    file_name="detection_results.csv",
                    mime="text/csv"
                )


# =========================================================
# TAB 2 — RECOVERY
# =========================================================

with tab2:

    st.header("🔓 Recover Protected Backup")

    st.write(
        "Use the AES-256-GCM protected backup and the "
        "correct password to recover the original file."
    )

    encrypted_file = st.file_uploader(
        "Upload encrypted .enc backup",
        type=["enc"],
        key="recovery_file"
    )

    recovery_password = st.text_input(
        "Enter protection password",
        type="password",
        key="recovery_password"
    )

    if encrypted_file is not None:

        if st.button(
            "🔓 Recover Original File",
            type="primary"
        ):

            if not recovery_password:

                st.warning(
                    "Please enter the protection password."
                )

            else:

                with tempfile.TemporaryDirectory() as temp_dir:

                    encrypted_path = os.path.join(
                        temp_dir,
                        encrypted_file.name
                    )

                    original_name = encrypted_file.name[:-4]

                    recovered_path = os.path.join(
                        temp_dir,
                        original_name
                    )

                    with open(
                        encrypted_path,
                        "wb"
                    ) as file:

                        file.write(
                            encrypted_file.getbuffer()
                        )

                    success = decrypt_file(
                        encrypted_path,
                        recovered_path,
                        recovery_password
                    )

                    if success:

                        with open(
                            recovered_path,
                            "rb"
                        ) as file:

                            recovered_data = file.read()

                        st.success(
                            "✅ Original file recovered successfully!"
                        )

                        st.download_button(
                            "⬇️ Download Recovered File",
                            recovered_data,
                            file_name=original_name,
                            mime="application/octet-stream"
                        )

                    else:

                        st.error(
                            "❌ Recovery failed. Check the password "
                            "or verify that the backup has not been modified."
                        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI-Based Ransomware Detection & Prevention | "
    "Random Forest + AES-256-GCM"
)