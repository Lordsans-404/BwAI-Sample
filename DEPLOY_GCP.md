# 🚀 Panduan Deploy FastAPI & Streamlit ke Google Cloud Run

Tutorial ini dibuat khusus untuk mendeploy aplikasi Machine Learning (FastAPI sebagai Backend dan Streamlit sebagai Frontend) ke **Google Cloud Run**.

**Kenapa Cloud Run?**
Cloud Run bersifat *Serverless*, artinya jika tidak ada yang membuka aplikasimu, instances-nya akan mati (Scale to Zero) dan **kamu tidak akan dicharge**.

---

## 🛠️ Persiapan Awal (Prerequisites)
1. **Akun Google Cloud Platform (GCP)** dengan billing yang sudah aktif.
2. Pastikan API **Cloud Run** dan **Cloud Build** sudah diaktifkan di Console GCP.
3. Install **Google Cloud CLI (`gcloud`)** di komputermu. Jika belum, [Download di sini](https://cloud.google.com/sdk/docs/install).
4. Login ke gcloud dari terminal:
   ```bash
   gcloud auth login
   gcloud config set project [PROJECT_ID_KAMU]
   ```

---

## 🏗️ Langkah 1: Penyesuaian Kode & Docker (✅ Sudah Disiapkan!)
Sebelum deploy, Streamlit dan FastAPI harus di-*containerize*.
Kabar baiknya, aku sudah membantu membuatkan **dua file** di project ini:
- `Dockerfile.backend` (Untuk FastAPI)
- `Dockerfile.frontend` (Untuk Streamlit)

Aku juga sudah mengubah kode Streamlit kamu (di `2_Raw_Dataset.py`, `3_Pair_Plot.py`, dan `4_Classification.py`) agar URL Backend tidak lagi di-*hardcode* ke `localhost`, melainkan membaca dari *Environment Variable* `API_URL`.

---

## 🌐 Langkah 2: Deploy Backend (FastAPI)
Kita akan deploy backend terlebih dahulu agar kita mendapatkan URL-nya untuk dihubungkan ke frontend.

Jalankan perintah ini di terminal (pastikan kamu berada di folder root project):
```bash
gcloud run deploy fastapi-backend \
  --source . \
  --dockerfile Dockerfile.backend \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --max-instances 1 \
  --memory 512Mi \
  --min-instances 0
```

**Penjelasan (Untuk menghemat Credits $5):**
- `--region asia-southeast2`: Region Jakarta (Bisa diganti `us-central1` jika ingin masuk Free Tier murni, tapi Jakarta lebih cepat diakses dari Indonesia).
- `--max-instances 1`: Membatasi agar maksimal hanya ada 1 instance yang berjalan secara bersamaan. (Mencegah tagihan bengkak jika ada spike traffic).
- `--memory 512Mi`: RAM 512MB sudah cukup untuk model Iris.
- `--min-instances 0`: **Super Penting!** Memastikan server mati total (scale-to-zero) saat tidak ada pengunjung. Tagihan = $0 saat sepi.

⏳ **Tunggu hingga selesai.** Nanti kamu akan mendapatkan Service URL, contoh:
`https://fastapi-backend-xxxxxx-et.a.run.app`

*(Copy URL ini untuk Langkah 3)*

---

## 🎨 Langkah 3: Deploy Frontend (Streamlit)
Sekarang, mari kita deploy UI-nya dan sambungkan dengan Backend yang sudah hidup.

Jalankan perintah ini (Ganti `<URL_DARI_LANGKAH_2>` dengan URL backend kamu sebelumnya):
```bash
gcloud run deploy streamlit-frontend \
  --source . \
  --dockerfile Dockerfile.frontend \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --max-instances 1 \
  --memory 512Mi \
  --min-instances 0 \
  --set-env-vars API_URL="<URL_DARI_LANGKAH_2>"
```

**Penjelasan:**
- Parameter `--set-env-vars API_URL=...` akan memberi tahu Streamlit kemana ia harus mengambil data model dan API. Jangan akhiri URL dengan tanda slash `/`.

⏳ **Tunggu hingga selesai.** Kamu akan mendapatkan Service URL untuk frontend.

---

## 🎉 Selesai!
Sekarang kamu bisa membagikan URL Frontend dari Langkah 3 ke teman-temanmu.

### 💡 Tips Keamanan Tagihan (Biar $5 Awet):
1. **Selalu Set Max Instances = 1**. Jika aplikasi tidak dibuat untuk ribuan orang sekaligus, angka ini akan menahan lonjakan biaya.
2. **Setup Billing Alert**. Masuk ke halaman **Billing** di GCP, buat Budget Alert di angka $4. Kamu akan dapat email jika tagihan mau habis.
3. Karena kita menset `--min-instances 0`, setiap kali aplikasi pertama kali dibuka (Cold Start), mungkin loadingnya agak lama sekitar 5-10 detik. Ini wajar karena GCP sedang "membangunkan" server-nya.
