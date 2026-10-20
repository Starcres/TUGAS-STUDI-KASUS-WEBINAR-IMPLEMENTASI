"""
SESI 6 — Analisis Indikasi Perubahan Vegetasi dari Data Satelit
Topik webinar: Attributing Direct Drivers to Deforestation Alerts with Satellite Imagery and AI

Tujuan:
- Membaca data pengamatan vegetasi dari file CSV.
- Membandingkan nilai NDVI antarwaktu.
- Menandai titik dengan penurunan NDVI yang melewati ambang.
- Menghasilkan daftar prioritas untuk pemeriksaan lebih lanjut.

PENTING:
- File CSV contoh dibuat oleh program dan bersifat SIMULASI.
- Penurunan NDVI hanya indikasi perubahan vegetasi; tidak membuktikan penyebab deforestasi.
- Penentuan penyebab langsung (mis. pertanian, jalan, pertambangan, kebakaran)
  memerlukan citra yang sesuai, label terverifikasi, dan evaluasi model.
- Program ini bukan model AI terlatih dan tidak mengklaim mendeteksi penyebab deforestasi.

Jalankan:
    python analisis_perubahan_vegetasi.py

Opsional, gunakan file CSV sendiri:
    python analisis_perubahan_vegetasi.py data_vegetasi.csv

Format CSV:
    lokasi,ndvi_awal,ndvi_akhir
    Petak-01,0.78,0.63
"""

import csv
import sys
from pathlib import Path


CONTOH_CSV = [
    {"lokasi": "Petak-01", "ndvi_awal": "0.78", "ndvi_akhir": "0.63"},
    {"lokasi": "Petak-02", "ndvi_awal": "0.74", "ndvi_akhir": "0.71"},
    {"lokasi": "Petak-03", "ndvi_awal": "0.69", "ndvi_akhir": "0.42"},
    {"lokasi": "Petak-04", "ndvi_awal": "0.55", "ndvi_akhir": "0.58"},
    {"lokasi": "Petak-05", "ndvi_awal": "0.81", "ndvi_akhir": "0.60"},
    {"lokasi": "Petak-06", "ndvi_awal": "0.62", "ndvi_akhir": "0.59"},
]

AMBANG_PENURUNAN = 0.15


def buat_csv_contoh(path):
    """Membuat CSV simulasi jika pengguna tidak memberikan file."""
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["lokasi", "ndvi_awal", "ndvi_akhir"])
        writer.writeheader()
        writer.writerows(CONTOH_CSV)


def baca_csv(path):
    """Membaca dan memvalidasi kolom serta nilai NDVI."""
    hasil = []
    with path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required = {"lokasi", "ndvi_awal", "ndvi_akhir"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError(
                "CSV harus memiliki kolom: lokasi, ndvi_awal, ndvi_akhir"
            )

        for nomor_baris, row in enumerate(reader, start=2):
            nama = (row.get("lokasi") or "").strip()
            try:
                awal = float(row["ndvi_awal"])
                akhir = float(row["ndvi_akhir"])
            except (TypeError, ValueError):
                print(f"Peringatan: baris {nomor_baris} dilewati karena NDVI tidak numerik.")
                continue

            if not nama:
                print(f"Peringatan: baris {nomor_baris} dilewati karena nama lokasi kosong.")
                continue
            if not (-1 <= awal <= 1 and -1 <= akhir <= 1):
                print(f"Peringatan: baris {nomor_baris} dilewati karena NDVI di luar rentang -1 hingga 1.")
                continue

            hasil.append({"lokasi": nama, "ndvi_awal": awal, "ndvi_akhir": akhir})

    return hasil


def analisis_perubahan(data, ambang=AMBANG_PENURUNAN):
    """Menghitung perubahan NDVI dan mengurutkan penurunan terbesar."""
    hasil = []
    for row in data:
        perubahan = row["ndvi_akhir"] - row["ndvi_awal"]
        hasil.append({
            "lokasi": row["lokasi"],
            "ndvi_awal": row["ndvi_awal"],
            "ndvi_akhir": row["ndvi_akhir"],
            "perubahan": perubahan,
            "indikasi_penurunan": perubahan <= -ambang,
        })
    return sorted(hasil, key=lambda item: item["perubahan"])


def simpan_hasil(data, path):
    """Menyimpan hasil analisis ke file CSV baru."""
    fields = [
        "lokasi", "ndvi_awal", "ndvi_akhir",
        "perubahan_ndvi", "indikasi_penurunan",
    ]
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in data:
            writer.writerow({
                "lokasi": row["lokasi"],
                "ndvi_awal": f"{row['ndvi_awal']:.3f}",
                "ndvi_akhir": f"{row['ndvi_akhir']:.3f}",
                "perubahan_ndvi": f"{row['perubahan']:.3f}",
                "indikasi_penurunan": "Ya" if row["indikasi_penurunan"] else "Tidak",
            })


def main():
    print("=" * 72)
    print("SESI 6: ANALISIS INDIKASI PERUBAHAN VEGETASI DARI DATA SATELIT")
    print("=" * 72)
    print("PENTING: data contoh bersifat SIMULASI; ini bukan deteksi deforestasi nyata.")
    print(f"Ambang penurunan NDVI yang digunakan: {AMBANG_PENURUNAN:.2f}")
    print()

    if len(sys.argv) > 1:
        input_path = Path(sys.argv[1])
        if not input_path.exists():
            print(f"Error: file tidak ditemukan: {input_path}")
            raise SystemExit(1)
        print(f"Membaca file pengguna: {input_path}")
    else:
        input_path = Path("data_vegetasi_simulasi.csv")
        buat_csv_contoh(input_path)
        print(f"File contoh dibuat: {input_path.resolve()}")

    try:
        data = baca_csv(input_path)
    except (OSError, ValueError) as error:
        print(f"Error membaca data: {error}")
        raise SystemExit(1)

    if not data:
        print("Tidak ada baris data valid untuk dianalisis.")
        raise SystemExit(1)

    hasil = analisis_perubahan(data)
    print()
    print("1. HASIL ANALISIS (diurutkan dari penurunan terbesar)")
    print("-" * 72)
    print(f"{'Lokasi':<14} {'NDVI awal':>10} {'NDVI akhir':>11} {'Perubahan':>11} {'Indikasi':>12}")
    print("-" * 72)
    for row in hasil:
        status = "Periksa" if row["indikasi_penurunan"] else "Tidak"
        print(
            f"{row['lokasi']:<14} {row['ndvi_awal']:>10.3f} "
            f"{row['ndvi_akhir']:>11.3f} {row['perubahan']:>+11.3f} {status:>12}"
        )

    prioritas = [row for row in hasil if row["indikasi_penurunan"]]
    print()
    print("2. RINGKASAN")
    print(f"- Jumlah lokasi valid       : {len(hasil)}")
    print(f"- Lokasi untuk diperiksa    : {len(prioritas)}")
    if prioritas:
        print("- Prioritas pemeriksaan     : " + ", ".join(row["lokasi"] for row in prioritas))
    else:
        print("- Tidak ada lokasi melewati ambang penurunan pada data ini.")

    output_path = Path("hasil_analisis_vegetasi.csv")
    simpan_hasil(hasil, output_path)
    print()
    print(f"3. File hasil disimpan ke: {output_path.resolve()}")
    print()
    print("4. INTERPRETASI DAN BATASAN")
    print("- Penurunan NDVI dapat mengindikasikan perubahan kondisi vegetasi.")
    print("- Penurunan NDVI tidak membuktikan bahwa deforestasi terjadi atau menjelaskan penyebabnya.")
    print("- Perlu citra satelit bertanggal, pemeriksaan kualitas, dan validasi lapangan.")
    print("- Untuk mengklasifikasikan penyebab langsung, diperlukan data berlabel dan model yang dilatih.")
    print("=" * 72)


if __name__ == "__main__":
    main()
