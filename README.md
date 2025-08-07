# 🧠 Deteksi Komunitas Menggunakan Algoritma PSO-Net

Sistem berbasis Python untuk mendeteksi komunitas dalam jaringan menggunakan algoritma **PSO-Net** (Particle Swarm Optimization for Community Detection). Dilengkapi dengan antarmuka visual interaktif menggunakan **Streamlit** serta fitur penyimpanan hasil deteksi.

---

## ✨ Fitur

- 🔍 Deteksi komunitas dari dataset jaringan (graph) berbasis algoritma PSO-Net
- 📊 Visualisasi graf komunitas secara interaktif
- 💾 Simpan hasil deteksi dalam format yang dapat diekspor
- 🤝 Open for contributions!

---

## 📂 Format Dataset

Pastikan dataset Anda dalam format **`.tsv` (Tab Separated Values)** dengan struktur kolom sebagai berikut:
...
```
source<TAB>target
A<TAB>B
B<TAB>C
```
> **Catatan:** Header tidak diwajibkan.

---

## 🚀 Cara Menjalankan

1. **Clone repositori ini:**

```bash
git clone https://github.com/rgustiann/Community-Detection-PSO-Net.git
cd Community-Detection-PSO-Net
````

2. **Install dependensi:**

```bash
pip install -r requirements.txt
```

3. **Jalankan aplikasi Streamlit:**

```bash
streamlit run main.py
```

4. **Upload file `.tsv`** dan mulai proses deteksi komunitas.

---

## 🛠 Teknologi yang Digunakan

* 🐍 Python 3
* 🎈 Streamlit
* 🕸️ NetworkX
* 📊 Matplotlib
* ⚙️ PSO (Particle Swarm Optimization) custom implementation

---

## 📌 Catatan Tambahan

* Dataset harus berupa file `.tsv` dengan kolom **source** dan **target** (tanpa header tidak masalah).
* Direkomendasikan untuk menggunakan dataset dengan ukuran kecil hingga menengah untuk performa optimal.
* Tersedia visualisasi jaringan interaktif dan hasil akhir dapat disimpan.

---

## 💡 Kontribusi

Proyek ini bersifat **open source** dan **terbuka untuk kontribusi**!

Silakan fork, pull request, atau diskusi melalui [Issues](https://github.com/rgustiann/Community-Detection-PSO-Net/issues).

---

