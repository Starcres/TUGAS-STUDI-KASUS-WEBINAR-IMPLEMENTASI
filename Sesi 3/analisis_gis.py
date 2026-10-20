"""
SESI 3 — Pemetaan Titik Fasilitas dan Analisis Jarak Sederhana
Topik webinar: Career and Competition in Industrial Era with GIS

Tujuan:
- Memahami representasi data lokasi dengan koordinat.
- Menghitung jarak garis-lurus antara titik lokasi.
- Mengelompokkan fasilitas berdasarkan kategori.
- Menghasilkan ringkasan yang dapat menjadi dasar eksplorasi GIS.

CATATAN:
- Semua koordinat di bawah adalah koordinat contoh/sintetis, bukan lokasi fasilitas nyata.
- Jarak yang dihitung adalah jarak garis-lurus (Haversine), bukan jarak jalan.
- Ini demonstrasi konsep GIS, belum menggunakan peta dasar atau data GIS resmi.
"""

from collections import Counter
from math import radians, sin, cos, asin, sqrt


LOKASI = [
    {"nama": "Fasilitas A", "kategori": "Kesehatan", "lat": -3.800, "lon": 102.265},
    {"nama": "Fasilitas B", "kategori": "Pendidikan", "lat": -3.810, "lon": 102.280},
    {"nama": "Fasilitas C", "kategori": "Kesehatan", "lat": -3.825, "lon": 102.250},
    {"nama": "Fasilitas D", "kategori": "Transportasi", "lat": -3.790, "lon": 102.300},
    {"nama": "Fasilitas E", "kategori": "Pendidikan", "lat": -3.835, "lon": 102.290},
    {"nama": "Fasilitas F", "kategori": "Ruang Publik", "lat": -3.805, "lon": 102.240},
]


def koordinat_valid(lat, lon):
    """Memastikan koordinat berada dalam rentang geografis."""
    return isinstance(lat, (int, float)) and isinstance(lon, (int, float)) and -90 <= lat <= 90 and -180 <= lon <= 180


def haversine_km(lat1, lon1, lat2, lon2):
    """Menghitung jarak garis-lurus permukaan bumi dalam kilometer."""
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6371.0 * 2 * asin(sqrt(a))


def validasi_lokasi(data):
    valid = []
    invalid = []
    seen = set()

    for item in data:
        nama = item.get("nama", "")
        lat = item.get("lat")
        lon = item.get("lon")
        if not nama:
            invalid.append((nama, "nama kosong"))
        elif nama in seen:
            invalid.append((nama, "nama duplikat"))
        elif not koordinat_valid(lat, lon):
            invalid.append((nama, "koordinat tidak valid"))
        else:
            valid.append(item)
            seen.add(nama)

    return valid, invalid


def hitung_jumlah_kategori(data):
    return Counter(item["kategori"] for item in data)


def cari_tetangga_terdekat(data):
    """Untuk setiap titik, temukan titik lain dengan jarak terdekat."""
    hasil = []
    for lokasi in data:
        kandidat = []
        for lain in data:
            if lain["nama"] == lokasi["nama"]:
                continue
            jarak = haversine_km(lokasi["lat"], lokasi["lon"], lain["lat"], lain["lon"])
            kandidat.append((jarak, lain["nama"]))
        if kandidat:
            jarak, nama_tetangga = min(kandidat)
            hasil.append({
                "nama": lokasi["nama"],
                "tetangga_terdekat": nama_tetangga,
                "jarak_km": jarak,
            })
    return hasil


def tampilkan_laporan():
    print("=" * 68)
    print("SESI 3: PEMETAAN TITIK FASILITAS DAN ANALISIS JARAK SEDERHANA")
    print("=" * 68)
    print("Data koordinat bersifat sintetis untuk demonstrasi GIS.")
    print()

    valid, invalid = validasi_lokasi(LOKASI)
    print("1. VALIDASI DATA KOORDINAT")
    print(f"- Jumlah lokasi awal : {len(LOKASI)}")
    print(f"- Lokasi valid       : {len(valid)}")
    print(f"- Lokasi tidak valid : {len(invalid)}")
    for nama, alasan in invalid:
        print(f"  - {nama}: {alasan}")
    print()

    print("2. JUMLAH FASILITAS PER KATEGORI")
    for kategori, jumlah in sorted(hitung_jumlah_kategori(valid).items()):
        print(f"- {kategori}: {jumlah}")
    print()

    print("3. TITIK TERDEKAT UNTUK SETIAP LOKASI")
    for item in cari_tetangga_terdekat(valid):
        print(f"- {item['nama']} -> {item['tetangga_terdekat']} ({item['jarak_km']:.2f} km)")
    print()

    print("4. INTERPRETASI")
    print("- Analisis koordinat dapat membantu memahami sebaran fasilitas.")
    print("- Jarak yang ditampilkan adalah jarak garis-lurus, bukan waktu tempuh.")
    print("- Untuk keputusan nyata, gunakan koordinat terverifikasi dan jaringan jalan.")
    print("=" * 68)


if __name__ == "__main__":
    tampilkan_laporan()
