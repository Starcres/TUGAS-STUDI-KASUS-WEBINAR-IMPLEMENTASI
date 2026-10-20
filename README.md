# TUGAS-STUDI-KASUS-WEBINAR-IMPLEMENTASI
Sesi 1 — Analisis Pola dan Tren Data Lingkungan
Topik webinar: Make Sense of Data with Analysis and AI
File: Sesi 1/analisis_lingkungan.py
Studi kasus
Analisis data lingkungan bulanan untuk mempelajari pola suhu, curah hujan, dan indeks vegetasi (NDVI). Dataset di dalam program merupakan data simulasi untuk latihan.
Implementasi
- Memeriksa data duplikat, nilai kosong, dan nilai tidak valid.
- Membersihkan data sebelum analisis.
- Menghitung rata-rata dan median suhu serta ringkasan curah hujan dan NDVI.
- Menghitung perubahan dari pengamatan pertama ke terakhir.
- Menandai kemungkinan anomali dengan aturan statistik sederhana.
- Menampilkan rekomendasi dan keterbatasan analisis.
Cara menjalankan
Dari direktori utama repository:
python "Sesi 1/analisis_lingkungan.py"
Jika python tidak dikenali, coba py sebagai pengganti.
Catatan
Data adalah simulasi, bukan pengukuran lingkungan nyata. NDVI contoh tidak berasal dari citra satelit.
Sesi 2 — Perbandingan Pemrosesan Serial dan Paralel
Topik webinar: Bridging Global Infrastructure to Address Local Challenges with HPC
File: Sesi 2/benchmark_hpc.py
Studi kasus
Membandingkan waktu pemrosesan serial dengan pemrosesan paralel pada kumpulan angka sintetis.
Implementasi
- Membuat data sintetis untuk pengujian.
- Menghitung ringkasan data dengan satu proses.
- Menghitung ringkasan menggunakan beberapa proses melalui ProcessPoolExecutor.
- Membandingkan waktu eksekusi dan menghitung speedup.
- Memeriksa apakah hasil kedua metode identik.
Cara menjalankan
python "Sesi 2/benchmark_hpc.py"
Catatan
Tidak memerlukan library tambahan. Hasil waktu bergantung pada perangkat keras, beban sistem, dan overhead proses paralel. Paralel tidak selalu lebih cepat.
Sesi 3 — Analisis Sebaran Fasilitas Menggunakan GIS
Topik webinar: Career and Competition in Industrial Era with GIS
File: Sesi 3/analisis_gis.py
Studi kasus
Menganalisis koordinat dan kedekatan beberapa titik fasilitas menggunakan data koordinat sintetis.
Implementasi
- Memvalidasi koordinat lintang dan bujur.
- Menghitung jumlah fasilitas berdasarkan kategori.
- Menghitung jarak garis-lurus dengan rumus Haversine.
- Menentukan tetangga terdekat untuk setiap lokasi.
- Menampilkan interpretasi hasil analisis spasial sederhana.
Cara menjalankan
python "Sesi 3/analisis_gis.py"
Catatan
Koordinat merupakan data sintetis. Jarak Haversine adalah jarak garis-lurus, bukan jarak jalan atau waktu tempuh. Tidak ada peta dasar yang digunakan pada versi ini.
Sesi 4 — Klasifikasi Jenis Bunga dengan Random Forest
Topik webinar: Introduction to Machine Learning
File: Sesi 4/klasifikasi_ml.py
Studi kasus
Melatih model Random Forest untuk mengklasifikasikan tiga jenis bunga dalam dataset Iris berdasarkan empat fitur pengukuran.
Implementasi
- Memuat dataset Iris dari scikit-learn.
- Membagi data menjadi data latih dan data uji.
- Melatih model RandomForestClassifier.
- Melakukan prediksi pada data uji.
- Mengukur accuracy, precision, recall, dan F1-score.
- Menampilkan confusion matrix dan satu contoh prediksi.
Instalasi dependensi
python -m pip install scikit-learn
Cara menjalankan
python "Sesi 4/klasifikasi_ml.py"
Catatan
Dataset Iris digunakan untuk demonstrasi pembelajaran machine learning; model ini bukan model klasifikasi tutupan lahan.
Sesi 5 — Dashboard Interaktif Data Lingkungan
Topik webinar: Human-Computer Interaction and Data Visualization
File: Sesi 5/dashboard_visualisasi.py
Studi kasus
Dashboard untuk menjelajahi data simulasi suhu, curah hujan, dan NDVI melalui antarmuka interaktif.
Implementasi
- Menampilkan metrik ringkas.
- Memilih variabel yang akan ditampilkan.
- Mengubah jenis grafik antara garis dan batang.
- Menampilkan tabel data.
- Menyajikan interpretasi dan catatan keterbatasan.
Instalasi dependensi
python -m pip install streamlit pandas matplotlib
Cara menjalankan
python -m streamlit run "Sesi 5/dashboard_visualisasi.py"
Setelah dijalankan, buka alamat lokal yang ditampilkan Streamlit di browser.
Catatan
Dashboard memakai data simulasi dan tidak memantau lingkungan secara real-time.
Sesi 6 — Analisis Perubahan Indeks Vegetasi
Topik webinar: Attributing Direct Drivers to Deforestation Alerts with Satellite Imagery and AI
File: Sesi 6/analisis_perubahan_vegetasi.py
Studi kasus
Membandingkan nilai NDVI awal dan akhir untuk menandai lokasi yang perlu diperiksa lebih lanjut.
Implementasi
- Membaca data NDVI dari file CSV.
- Memvalidasi kolom dan nilai NDVI.
- Menghitung perubahan NDVI antara dua waktu.
- Menandai lokasi yang penurunannya melewati ambang yang ditentukan.
- Mengurutkan lokasi berdasarkan besar perubahan.
- Menyimpan hasil analisis ke CSV.
Cara menjalankan dengan data contoh
python "Sesi 6/analisis_perubahan_vegetasi.py"
Program membuat data_vegetasi_simulasi.csv dan hasil_analisis_vegetasi.csv di direktori kerja saat ini.
Cara menjalankan dengan CSV sendiri
CSV harus memiliki kolom lokasi, ndvi_awal, dan ndvi_akhir.
python "Sesi 6/analisis_perubahan_vegetasi.py" "data_vegetasi.csv"
Catatan penting
Data bawaan adalah simulasi. Penurunan NDVI tidak membuktikan bahwa deforestasi terjadi atau mengidentifikasi penyebabnya. Analisis penyebab langsung membutuhkan citra satelit yang sesuai, data berlabel, validasi, dan model yang dilatih.
