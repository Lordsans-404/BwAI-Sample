# FastAPI-Streamlit Iris Classification Project Context

## 🌟 Project Overview
Proyek ini adalah aplikasi Machine Learning *end-to-end* yang menggabungkan **FastAPI** sebagai backend (API Service) dan **Streamlit** sebagai frontend (Interactive UI). Aplikasi ini dirancang untuk mengeksplorasi dataset Iris dan melakukan prediksi spesies bunga berdasarkan fitur morfologisnya.

---

## 🏗️ Architecture & Flow

### 1. Backend (FastAPI - `main.py`)
Bertindak sebagai otak aplikasi. Tugas utamanya adalah:
- **Serving Data**: Menyediakan endpoint `/iris` untuk mengambil dataset mentah dalam format JSON.
- **Model Inference**: Menyediakan endpoint `/predict` (POST) yang menerima fitur bunga dan mengembalikan prediksi spesies beserta tingkat kepercayaannya (*confidence score*).
- **Static Files**: Meng-mount direktori `src/app` sebagai file statis (opsional, tergantung cara deploy).

### 2. Frontend (Streamlit - `src/app/Home.py`)
Bertindak sebagai antarmuka pengguna. Terdiri dari beberapa halaman:
- **Home**: Halaman selamat datang.
- **About**: Informasi singkat tentang aplikasi.
- **Raw Dataset**: Mengambil data dari FastAPI `/iris` dan menampilkan statistik deskriptif.
- **Pair Plot**: Visualisasi hubungan antar fitur menggunakan Seaborn.
- **Classification**: Form input untuk prediksi yang berinteraksi dengan FastAPI `/predict` dan menampilkan visualisasi PCA (Principal Component Analysis).

### 3. Model Logic (`src/model/classifier.py`)
Modul untuk melatih model. Mendukung beberapa algoritma:
- Logistic Regression
- Random Forest
- XGBoost
- Decision Tree
Model yang dilatih disimpan di `data/saved_models/` dalam format `.joblib`.

---

## 🚀 Application Workflow
1. **User Interaction**: User membuka UI Streamlit.
2. **Data Request**: Saat User membuka halaman "Raw Dataset", Streamlit mengirimkan GET request ke `http://127.0.0.1:8000/iris`.
3. **Prediction**: Di halaman "Classification", User menginput nilai fitur. Saat tombol "Predict" ditekan, Streamlit mengirimkan POST request berisi data fitur ke `http://127.0.0.1:8000/predict`.
4. **Processing**: FastAPI menerima data, memprosesnya menggunakan model yang sudah di-load (sesuai konfigurasi di `main.yml`), dan mengirimkan hasilnya kembali.
5. **Visualization**: Streamlit menampilkan hasil prediksi dan memplot posisi data baru tersebut dalam ruang 2D menggunakan PCA.

---

## ⚙️ Configuration (`config/main.yml`)
Konfigurasi pusat aplikasi:
- `model.classifier`: Algoritma yang digunakan saat training.
- `app.use_model`: Model mana yang akan di-load oleh FastAPI untuk produksi/prediksi.
- `data.data_path`: Lokasi file CSV dataset.

---

## 📦 Deployment Considerations (Hal yang perlu diperhatikan)

Jika kamu berencana mendeploy aplikasi ini, perhatikan hal-hal berikut:

### 1. Dual-Process Management & Makefile
Aplikasi ini membutuhkan dua proses yang berjalan secara bersamaan:
- **Uvicorn** (FastAPI): `python main.py` (Default port 8000)
- **Streamlit**: `streamlit run src/app/Home.py` (Default port 8501)

Tersedia `Makefile` untuk mempermudah menjalankan aplikasi:
- `make backend`: Menjalankan FastAPI server.
- `make frontend`: Menjalankan Streamlit UI.
- `make run_app`: Menjalankan keduanya sekaligus.

### 2. URL Endpoints
Di kode saat ini (misal di `2_Raw_Dataset.py`), URL API di-hardcode ke `http://127.0.0.1:8000`. 
**PENTING**: Saat deploy, ubah ini menjadi environment variable atau gunakan URL relatif jika di-proxy oleh web server seperti Nginx.

### 3. Dependency Management
Pastikan semua library terdaftar di `requirements.txt`. Library kunci:
- `fastapi`, `uvicorn`, `pydantic`
- `streamlit`, `requests`, `pandas`, `seaborn`, `matplotlib`
- `scikit-learn`, `joblib`, `xgboost`

### 4. Model Persistence
Pastikan file `.joblib` di `data/saved_models/` ikut ter-upload. Tanpa file ini, backend akan gagal saat *startup*.

### 5. Dockerization (Recommended)
Buat `Dockerfile` yang menginstal dependensi dan mungkin menggunakan `supervisord` untuk menjalankan FastAPI dan Streamlit dalam satu container, atau buat dua container terpisah.

---

## 📂 Folder Structure Highlights
- `data/`: Dataset mentah dan model yang sudah dilatih.
- `notebooks/`: Tempat untuk eksplorasi data (EDA) awal.
- `src/utils/`: Fungsi pembantu untuk load config dan data agar kode tetap DRY (*Don't Repeat Yourself*).
- `main.py`: Entry point utama untuk Backend.
