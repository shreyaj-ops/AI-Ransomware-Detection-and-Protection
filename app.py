import streamlit as st
import pandas as pd
import joblib
import tempfile
import os

from crypto_module import encrypt_file, decrypt_file


# ==============================
# PAGE CONFIGURATION
# ==============================

st.set_page_config(
    page_title="AI Ransomware Detection",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI-Based Ransomware Detection & Prevention")
st.write(
    "Random Forest detects ransomware-like behavior and "
    "AES-256-GCM protects important files."
)


# ==============================
# LOAD MODEL
# ==============================

model = joblib.load("ransomware_model.pkl")
feature_names = joblib.load("feature_names.pkl")


# ==============================
# TABS
# ==============================

tab1, tab2 = st.tabs([
    "🧠 Detect & Protect",
    "🔓 Recover Backup"
])


# ==========================================================
# TAB 1 — DETECT & PROTECT
# ==========================================================

with tab1:

    st.header("🧠 Ransomware Detection & Protection")

    # --------------------------
    # STEP 1 — BEHAVIORAL DATA
    # --------------------------

    st.subheader("1️⃣ Upload Behavioral Dataset")

    csv_file = st.file_uploader(
        "Upload ransomware behavioral data",
        type=["csv"],
        key="behavior_csv"
    )

    # --------------------------
    # STEP 2 — IMPORTANT FILE
    # --------------------------

    st.subheader("2️⃣ Select Important File to Protect")

    important_file = st.file_uploader(
        "Upload an important file for protected backup",
        type=None,
        key="important_file"
    )

    if important_file is not None:
        st.success(
            f"📄 Selected file: **{important_file.name}**"
        )

    # --------------------------
    # PASSWORD
    # --------------------------

    st.subheader("3️⃣ Set Backup Password")

    password = st.text_input(
        "Password for AES-256-GCM backup",
        type="password"
    )

    # --------------------------
    # ANALYZE BUTTON
    # --------------------------

    if st.button(
        "🔍 Analyze & Protect",
        type="primary",
        use_container_width=True
    ):

        if csv_file is None:
            st.warning("⚠️ Please upload the behavioral CSV dataset.")
            st.stop()

        if important_file is None:
            st.warning("⚠️ Please upload an important file to protect.")
            st.stop()

        if not password:
            st.warning("⚠️ Please enter a backup password.")
            st.stop()

        # ==============================
        # READ CSV
        # ==============================

        df = pd.read_csv(csv_file)

        st.info(
            f"📊 Dataset loaded: {len(df):,} behavioral samples"
        )

        # Check features
        missing_features = [
            feature for feature in feature_names
            if feature not in df.columns
        ]

        if missing_features:
            st.error(
                "❌ Dataset does not contain the required behavioral features."
            )
            st.stop()

        X = df[feature_names]

        # ==============================
        # RANDOM FOREST PREDICTION
        # ==============================

        predictions = model.predict(X)

        ransomware_count = int((predictions == 1).sum())
        benign_count = int((predictions == 0).sum())

        # ==================================================
        # THREAT DETECTED
        # ==================================================

        if ransomware_count > 0:

            # ----------------------------------------------
            # FIRST: ALERT USER
            # ----------------------------------------------

            st.error(
                f"🚨 RANSOMWARE THREAT DETECTED!\n\n"
                f"{ransomware_count:,} suspicious behavioral samples detected."
            )

            st.warning(
                "⚠️ The system detected ransomware-like behavior. "
                "Creating a protected recovery backup of your selected file..."
            )

            # ----------------------------------------------
            # SECOND: CREATE AES BACKUP
            # ----------------------------------------------

            file_bytes = important_file.getvalue()

            # Save uploaded file temporarily
            temp_input = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=os.path.splitext(important_file.name)[1]
            )

            temp_input.write(file_bytes)
            temp_input.close()

            # Create encrypted backup
            encrypted_path = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".enc"
            ).name

            encrypt_file(
                temp_input.name,
                encrypted_path,
                password
            )

            # ----------------------------------------------
            # BACKUP CREATED
            # ----------------------------------------------

            st.success(
                "🔐 AES-256-GCM encrypted backup created successfully!"
            )

            st.info(
                "🛡️ Your original file has not been modified. "
                "The encrypted copy can be used for recovery."
            )

            # Read encrypted backup
            with open(encrypted_path, "rb") as f:
                encrypted_bytes = f.read()

            backup_name = important_file.name + ".enc"

            st.download_button(
                label="⬇️ Download Protected Backup",
                data=encrypted_bytes,
                file_name=backup_name,
                mime="application/octet-stream",
                use_container_width=True
            )

            # Clean temporary files
            try:
                os.remove(temp_input.name)
                os.remove(encrypted_path)
            except:
                pass

        # ==================================================
        # NO THREAT
        # ==================================================

        else:

            st.success(
                "✅ No ransomware behavior detected."
            )

            st.info(
                "No protected backup was created because "
                "no ransomware threat was detected."
            )

        # ==============================
        # RESULTS
        # ==============================

        st.divider()

        st.subheader("📊 Detection Results")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Benign Samples",
                f"{benign_count:,}"
            )

        with col2:
            st.metric(
                "Ransomware Samples",
                f"{ransomware_count:,}"
            )


# ==========================================================
# TAB 2 — RECOVER BACKUP
# ==========================================================

with tab2:

    st.header("🔓 Recover Protected File")

    st.write(
        "Upload the AES-256-GCM encrypted backup and enter "
        "the password used during protection."
    )

    encrypted_file = st.file_uploader(
        "Upload encrypted backup (.enc)",
        type=["enc"],
        key="encrypted_file"
    )

    recovery_password = st.text_input(
        "Enter backup password",
        type="password",
        key="recovery_password"
    )

    if st.button(
        "🔓 Decrypt & Recover",
        use_container_width=True
    ):

        if encrypted_file is None:
            st.warning("⚠️ Please upload an encrypted backup.")

        elif not recovery_password:
            st.warning("⚠️ Please enter the password.")

        else:

            encrypted_path = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".enc"
            ).name

            with open(encrypted_path, "wb") as f:
                f.write(encrypted_file.getvalue())

            recovered_name = encrypted_file.name.replace(
                ".enc",
                ""
            )

            recovered_path = tempfile.NamedTemporaryFile(
                delete=False
            ).name

            success = decrypt_file(
                encrypted_path,
                recovered_path,
                recovery_password
            )

            if success:

                st.success(
                    "✅ File successfully recovered!"
                )

                with open(recovered_path, "rb") as f:
                    recovered_bytes = f.read()

                st.download_button(
                    label="⬇️ Download Recovered File",
                    data=recovered_bytes,
                    file_name=recovered_name,
                    use_container_width=True
                )

            else:

                st.error(
                    "❌ Decryption failed. "
                    "Check your password or encrypted file."
                )

            try:
                os.remove(encrypted_path)
                os.remove(recovered_path)
            except:
                pass