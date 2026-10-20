"""
SESI 1 — Analisis Pola dan Tren Data Lingkungan Menggunakan Python
Topik webinar: Make Sense of Data with Analysis and AI

CATATAN: Data di bawah adalah SIMULASI untuk demonstrasi, bukan data nyata.
Analisis anomali memakai aturan statistik sederhana, bukan model AI terlatih.
"""

from statistics import mean, median
from datetime import datetime

# 1. DATA SIMULASI
raw_data = [
    {"tanggal": "2026-01", "lokasi": "Lokasi A", "suhu_c": 29.1, "curah_hujan_mm": 310, "ndvi": 0.72},
    {"tanggal": "2026-02", "lokasi": "Lokasi A", "suhu_c": 29.4, "curah_hujan_mm": 280, "ndvi": 0.70},
    {"tanggal": "2026-03", "lokasi": "Lokasi A", "suhu_c": 30.0, "curah_hujan_mm": 245, "ndvi": 0.68},
    {"tanggal": "2026-04", "lokasi": "Lokasi A", "suhu_c": 30.2, "curah_hujan_mm": 190, "ndvi": 0.65},
    {"tanggal": "2026-05", "lokasi": "Lokasi A", "suhu_c": 30.8, "curah_hujan_mm": 135, "ndvi": 0.61},
    {"tanggal": "2026-06", "lokasi": "Lokasi A", "suhu_c": 31.3, "curah_hujan_mm": 90, "ndvi": 0.58},
    {"tanggal": "2026-07", "lokasi": "Lokasi A", "suhu_c": 32.0, "curah_hujan_mm": 42, "ndvi": 0.51},
    {"tanggal": "2026-08", "lokasi": "Lokasi A", "suhu_c": 32.4, "curah_hujan_mm": 25, "ndvi": 0.47},
    {"tanggal": "2026-09", "lokasi": "Lokasi A", "suhu_c": 31.7, "curah_hujan_mm": 55, "ndvi": 0.50},
    {"tanggal": "2026-10", "lokasi": "Lokasi A", "suhu_c": 30.9, "curah_hujan_mm": 145, "ndvi": 0.59},
    {"tanggal": "2026-11", "lokasi": "Lokasi A", "suhu_c": 29.8, "curah_hujan_mm": 230, "ndvi": 0.66},
    {"tanggal": "2026-12", "lokasi": "Lokasi A", "suhu_c": 29.3, "curah_hujan_mm": 295, "ndvi": 0.71},
    {"tanggal": "2026-08", "lokasi": "Lokasi A", "suhu_c": 32.4, "curah_hujan_mm": 25, "ndvi": 0.47},  # duplikat
    {"tanggal": "2026-11", "lokasi": "Lokasi B", "suhu_c": None, "curah_hujan_mm": 230, "ndvi": 0.66},  # nilai kosong
    {"tanggal": "2026-13", "lokasi": "Lokasi C", "suhu_c": 28.5, "curah_hujan_mm": -12, "ndvi": 1.4},  # tidak valid
]


def periksa_kualitas(data):
    """Memeriksa duplikat, nilai kosong, dan nilai di luar rentang."""
    seen = set()
    duplicate_count = 0
    missing_fields = []
    invalid_records = []

    for index, row in enumerate(data, start=1):
        key = (row.get("tanggal"), row.get("lokasi"))
        if key in seen:
            duplicate_count += 1
        seen.add(key)

        for field, value in row.items():
            if value is None or value == "":
                missing_fields.append((index, field))

        problems = []
        try:
            datetime.strptime(row.get("tanggal", ""), "%Y-%m")
        except (ValueError, TypeError):
            problems.append("format tanggal tidak valid")

        rain = row.get("curah_hujan_mm")
        if not isinstance(rain, (int, float)) or rain < 0:
            problems.append("curah hujan harus >= 0")

        ndvi = row.get("ndvi")
        if not isinstance(ndvi, (int, float)) or not -1 <= ndvi <= 1:
            problems.append("NDVI harus antara -1 sampai 1")

        temp = row.get("suhu_c")
        if temp is not None and (not isinstance(temp, (int, float)) or not 0 <= temp <= 60):
            problems.append("suhu di luar rentang pemeriksaan 0–60 °C")

        if problems:
            invalid_records.append((index, ", ".join(problems)))

    return {
        "jumlah_record_awal": len(data),
        "duplikat": duplicate_count,
        "nilai_kosong": missing_fields,
        "record_tidak_valid": invalid_records,
    }


def bersihkan_data(data):
    """Menghapus duplikat dan record tidak valid agar analisis lebih konsisten."""
    cleaned = []
    seen = set()

    for row in data:
        key = (row.get("tanggal"), row.get("lokasi"))
        if key in seen:
            continue
        seen.add(key)

        try:
            datetime.strptime(row.get("tanggal", ""), "%Y-%m")
        except (ValueError, TypeError):
            continue

        temp = row.get("suhu_c")
        rain = row.get("curah_hujan_mm")
        ndvi = row.get("ndvi")

        if temp is None or not isinstance(temp, (int, float)) or not 0 <= temp <= 60:
            continue
        if not isinstance(rain, (int, float)) or rain < 0:
            continue
        if not isinstance(ndvi, (int, float)) or not -1 <= ndvi <= 1:
            continue

        cleaned.append(dict(row))

    return cleaned


def analisis_deskriptif(data):
    """Menghitung ringkasan statistik dan perubahan awal ke akhir."""
    if not data:
        return {}

    suhu = [row["suhu_c"] for row in data]
    hujan = [row["curah_hujan_mm"] for row in data]
    ndvi = [row["ndvi"] for row in data]

    return {
        "jumlah_pengamatan": len(data),
        "suhu_rata_rata": mean(suhu),
        "suhu_median": median(suhu),
        "curah_hujan_rata_rata": mean(hujan),
        "curah_hujan_total": sum(hujan),
        "ndvi_rata_rata": mean(ndvi),
        "perubahan_suhu": suhu[-1] - suhu[0],
        "perubahan_hujan": hujan[-1] - hujan[0],
        "perubahan_ndvi": ndvi[-1] - ndvi[0],
    }


def deteksi_anomali(data):
    """Menandai nilai yang berjarak lebih dari 2 simpangan baku dari rata-rata."""
    anomalies = []
    for field in ("suhu_c", "curah_hujan_mm", "ndvi"):
        values = [row[field] for row in data]
        avg = mean(values)
        variance = sum((value - avg) ** 2 for value in values) / len(values)
        std_dev = variance ** 0.5

        for row in data:
            if std_dev > 0 and abs(row[field] - avg) > 2 * std_dev:
                anomalies.append({
                    "tanggal": row["tanggal"],
                    "lokasi": row["lokasi"],
                    "variabel": field,
                    "nilai": row[field],
                    "rata_rata": avg,
                })
    return anomalies


def buat_rekomendasi(stats):
    recommendations = []
    if stats["perubahan_hujan"] < -100:
        recommendations.append(
            "Curah hujan awal dan akhir periode berbeda cukup besar; "
            "periksa pola musim dan kebutuhan pemantauan air."
        )
    if stats["perubahan_ndvi"] < -0.10:
        recommendations.append(
            "NDVI menurun antara pengamatan pertama dan terakhir; "
            "periksa kondisi vegetasi dengan data lapangan atau citra satelit."
        )
    if stats["perubahan_suhu"] > 1:
        recommendations.append(
            "Suhu meningkat antara pengamatan pertama dan terakhir; "
            "bandingkan dengan periode lain sebelum menarik kesimpulan."
        )
    if not recommendations:
        recommendations.append("Lanjutkan pemantauan berkala untuk melihat pola perubahan.")
    recommendations.append(
        "Kesimpulan hanya berdasarkan data simulasi dan tidak membuktikan sebab-akibat."
    )
    return recommendations


def tampilkan_laporan():
    print("=" * 68)
    print("SESI 1: ANALISIS POLA DAN TREN DATA LINGKUNGAN")
    print("=" * 68)
    print("CATATAN: seluruh data merupakan SIMULASI untuk latihan.\n")

    quality = periksa_kualitas(raw_data)
    print("1. PEMERIKSAAN KUALITAS DATA")
    print(f"- Jumlah record awal     : {quality['jumlah_record_awal']}")
    print(f"- Record duplikat        : {quality['duplikat']}")
    print(f"- Nilai kosong           : {len(quality['nilai_kosong'])}")
    print(f"- Record tidak valid     : {len(quality['record_tidak_valid'])}")
    print()

    cleaned = bersihkan_data(raw_data)
    stats = analisis_deskriptif(cleaned)
    print("2. HASIL PEMBERSIHAN")
    print(f"- Record valid           : {len(cleaned)}")
    print()

    print("3. ANALISIS DESKRIPTIF")
    print(f"- Suhu rata-rata         : {stats['suhu_rata_rata']:.2f} °C")
    print(f"- Median suhu            : {stats['suhu_median']:.2f} °C")
    print(f"- Curah hujan rata-rata  : {stats['curah_hujan_rata_rata']:.2f} mm")
    print(f"- Total curah hujan      : {stats['curah_hujan_total']:.2f} mm")
    print(f"- NDVI rata-rata         : {stats['ndvi_rata_rata']:.3f}")
    print()

    print("4. PERUBAHAN PENGAMATAN PERTAMA KE TERAKHIR")
    print(f"- Perubahan suhu         : {stats['perubahan_suhu']:+.2f} °C")
    print(f"- Perubahan curah hujan  : {stats['perubahan_hujan']:+.2f} mm")
    print(f"- Perubahan NDVI         : {stats['perubahan_ndvi']:+.3f}")
    print()

    print("5. ANOMALI STATISTIK SEDERHANA")
    anomalies = deteksi_anomali(cleaned)
    if anomalies:
        for item in anomalies:
            print(
                f"- {item['tanggal']} ({item['lokasi']}): {item['variabel']}="
                f"{item['nilai']}; rata-rata={item['rata_rata']:.3f}"
            )
    else:
        print("- Tidak ada nilai yang melewati ambang 2 simpangan baku.")
    print("Catatan: anomali statistik bukan otomatis berarti kesalahan data.\n")

    print("6. REKOMENDASI")
    for number, recommendation in enumerate(buat_rekomendasi(stats), start=1):
        print(f"{number}. {recommendation}")

    print("\n7. KETERBATASAN")
    print("- Data simulasi; bukan pengukuran lingkungan nyata.")
    print("- NDVI contoh bukan hasil pemrosesan citra Sentinel-2.")
    print("- Perubahan dua titik waktu tidak cukup untuk menyimpulkan tren iklim.")
    print("=" * 68)


if __name__ == "__main__":
    tampilkan_laporan()
