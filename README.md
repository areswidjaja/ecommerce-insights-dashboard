## 🛍️ E-Commerce Insights Dashboard

### 📌 Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis data transaksi pada **E-Commerce Public Dataset** menggunakan Python. Analisis difokuskan pada tren penjualan, kategori produk, serta performa transaksi, yang kemudian divisualisasikan melalui **dashboard interaktif berbasis Streamlit**.

---

### 🧮 Tools & Library

- **pandas** → manipulasi dan analisis data
- **matplotlib** → visualisasi dasar (grafik batang, garis, pie chart, dsb.)
- **seaborn** → visualisasi statistik yang lebih informatif dan menarik
- **streamlit** → pembuatan dashboard interaktif

---

### 📊 Dataset yang Digunakan

Dataset bersumber dari **E-Commerce Public Dataset**, dengan file utama:

- `orders_dataset.csv`
- `order_items_dataset.csv`
- `order_payments_dataset.csv`
- `order_reviews_dataset.csv`
- `sellers_dataset.csv`
- `products_dataset.csv`
- `product_category_name_translation.csv`

---

### 🧹 Tahapan Analisis

1. **Data Wrangling**
   - Pembersihan dan penggabungan data dari beberapa tabel
   - Penanganan missing values dan duplikasi

2. **Exploratory Data Analysis (EDA)**
   - Analisis tren transaksi, kategori produk terlaris, dan pola pembayaran
   - Visualisasi menggunakan `matplotlib` dan `seaborn`

3. **Dashboard Development**
   - Integrasi hasil analisis ke dalam dashboard **Streamlit**
   - Visualisasi interaktif untuk eksplorasi data dan insight

---

### 🖥️ Cara Menjalankan Dashboard

**Buat dan aktifkan environment baru:**
conda create --name main-ds python=3.9
conda activate main-ds

**Instal semua dependensi proyek:**
pip install -r requirements.txt

**Jalankan aplikasi Streamlit:**
streamlit run dashboard.py

Dashboard akan terbuka otomatis di browser.

---

### 📦 Struktur Folder

Struktur proyek final:

```
📁 submission/
├── 📁 dashboard/              # berisi file dashboard Streamlit dan data hasil olahan
│   ├── dashboard.py           # file utama Streamlit untuk visualisasi
│   ├── installment_summary.csv  # data agregasi metode pembayaran
│   ├── monthly_sales.csv        # data agregasi penjualan bulanan
│   ├── payment_summary.csv      # ringkasan transaksi per metode pembayaran
│   ├── review_summary.csv       # hasil analisis kepuasan pelanggan
│   ├── sales_by_category.csv    # ringkasan penjualan per kategori produk
│   └── seller_summary.csv       # performa penjual berdasarkan pendapatan dan pesanan
│
├── 📁 data/                   # berisi dataset mentah (raw data)
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── sellers_dataset.csv
│   ├── products_dataset.csv
│   └── product_category_name_translation.csv
│
├── 📄 notebook.ipynb          # notebook utama untuk analisis dan eksplorasi data
├── 📄 README.md               # dokumentasi proyek
├── 📄 requirements.txt        # daftar dependensi library Python
├── 📄 url.txt                  # tautan dashboard
```

📌 **Penjelasan:**
- Folder `data/` menyimpan data mentah yang belum diolah.
- Folder `dashboard/` berisi dataset hasil *cleaning* dan *aggregation* yang siap divisualisasikan di Streamlit.
- Struktur ini mengikuti standar proyek analisis data profesional — memisahkan *raw data*, *processed data*, dan *visualization logic*.

---

### 📈 Insight Utama

Selama periode analisis, performa bisnis menunjukkan pertumbuhan yang kuat dan stabil di berbagai aspek, termasuk penjualan, kinerja penjual, metode pembayaran, kepuasan pelanggan, dan tren waktu. Berikut rangkuman insight utamanya:

- **Penjualan per Kategori Produk:** Kategori *health_beauty*, *watches_gifts*, dan *bed_bath_table* menjadi penyumbang pendapatan tertinggi, dengan total revenue lebih dari 1 juta BRL. Kombinasi produk cepat laku dan premium menghasilkan pendapatan yang stabil serta profitabilitas jangka panjang.

- **Kinerja Penjual:** Penjual dengan ID `1025f0e2d44d7041d6cf58b6550e0bfa` mencatat pendapatan tertinggi (~115.000 BRL), sementara `6560211a19b47992c3666cc44a7e94c0` memiliki jumlah pesanan terbanyak (803 order). Korelasi rendah (-0.029) antara frekuensi penjualan dan skor ulasan menunjukkan kualitas layanan yang konsisten di berbagai skala penjual.

- **Metode Pembayaran:** Transaksi berbasis *credit card* mendominasi, dengan total nilai >9,45 juta BRL, diikuti oleh *boleto* (2,08 juta BRL). Sebagian besar pelanggan memilih pembayaran langsung (1x cicilan), menegaskan preferensi terhadap kenyamanan dan fleksibilitas kartu kredit.

- **Kepuasan Pelanggan:** Rata-rata skor ulasan mencapai **4,04/5**, menandakan kepuasan tinggi secara umum. Kategori seperti *cds_dvds_musicals* dan *books_imported* mencatat skor tertinggi (≥4,5), sementara *security_and_services* dan *office_furniture* lebih rendah (≤3,5). Peningkatan dibutuhkan pada layanan purna jual dan kecepatan respon.

- **Tren Penjualan Bulanan:** Dalam 18 bulan terakhir, penjualan meningkat konsisten hingga puncak pada **November 2017** (~1,15 juta BRL, 7.000 pesanan), didorong promosi akhir tahun seperti *Black Friday*. Stabilitas pasca puncak menandakan loyalitas pelanggan yang kuat dan strategi retensi efektif.

**Kesimpulan:**
Perusahaan menunjukkan fundamental bisnis yang solid dengan pertumbuhan positif di hampir semua dimensi. Transaksi kartu kredit menjadi motor utama ekonomi platform, kepuasan pelanggan tinggi, dan strategi promosi musiman efektif dalam mendorong performa tahunan. Potensi optimalisasi terletak pada penguatan kategori bernilai tinggi dan peningkatan pengalaman pelanggan.

---

### 👨‍💻 Pengembang

**Nama:** Ilfa Antaries Yusuf Wijaya  
**Proyek:** Dicoding — *Belajar Analisis Data dengan Python*  
**Tools:** Google Colab / Anaconda, Streamlit Cloud