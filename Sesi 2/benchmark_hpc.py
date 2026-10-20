"""
SESI 2 — Benchmark Pemrosesan Data: Serial vs Paralel
Topik webinar: Bridging Global Infrastructure to Address Local Challenges with HPC

Tujuan:
- Memproses kumpulan data simulasi dengan operasi numerik sederhana.
- Membandingkan waktu eksekusi serial dan paralel.
- Memeriksa apakah kedua metode menghasilkan ringkasan yang sama.

PENTING:
- Data yang dihasilkan adalah data sintetis, bukan data riset nyata.
- Benchmark dipengaruhi spesifikasi komputer, jumlah proses, dan beban sistem.
- Untuk dataset kecil, paralel bisa lebih lambat karena overhead pembagian tugas.
"""

from concurrent.futures import ProcessPoolExecutor
from time import perf_counter
import os
import statistics


def buat_data(jumlah):
    """Membuat data numerik sintetis yang deterministik."""
    # Menghasilkan angka berulang agar tidak perlu pustaka eksternal.
    return [(i * 17 + 23) % 100_003 for i in range(jumlah)]


def hitung_ringkasan(chunk):
    """Menghitung ringkasan pada satu potongan data."""
    return {
        "jumlah_item": len(chunk),
        "total": sum(chunk),
        "kuadrat_total": sum(value * value for value in chunk),
        "nilai_minimum": min(chunk) if chunk else None,
        "nilai_maksimum": max(chunk) if chunk else None,
    }


def gabungkan_ringkasan(ringkasan):
    """Menggabungkan hasil dari beberapa potongan data."""
    valid = [item for item in ringkasan if item["jumlah_item"] > 0]
    return {
        "jumlah_item": sum(item["jumlah_item"] for item in valid),
        "total": sum(item["total"] for item in valid),
        "kuadrat_total": sum(item["kuadrat_total"] for item in valid),
        "nilai_minimum": min(item["nilai_minimum"] for item in valid) if valid else None,
        "nilai_maksimum": max(item["nilai_maksimum"] for item in valid) if valid else None,
    }


def bagi_data(data, jumlah_bagian):
    """Membagi data menjadi beberapa bagian dengan ukuran seimbang."""
    if not data:
        return []
    jumlah_bagian = max(1, min(jumlah_bagian, len(data)))
    ukuran = (len(data) + jumlah_bagian - 1) // jumlah_bagian
    return [data[start:start + ukuran] for start in range(0, len(data), ukuran)]


def jalankan_serial(data):
    mulai = perf_counter()
    hasil = hitung_ringkasan(data)
    durasi = perf_counter() - mulai
    return hasil, durasi


def jalankan_paralel(data, jumlah_proses):
    bagian = bagi_data(data, jumlah_proses)
    mulai = perf_counter()

    # ProcessPoolExecutor membagi pekerjaan ke beberapa proses.
    with ProcessPoolExecutor(max_workers=jumlah_proses) as executor:
        hasil_bagian = list(executor.map(hitung_ringkasan, bagian))

    hasil = gabungkan_ringkasan(hasil_bagian)
    durasi = perf_counter() - mulai
    return hasil, durasi


def format_detik(durasi):
    return f"{durasi:.4f} detik"


def main():
    print("=" * 68)
    print("SESI 2: BENCHMARK PEMROSESAN DATA SERIAL VS PARALEL")
    print("=" * 68)
    print("Data sintetis; hasil waktu bergantung pada komputer yang digunakan.")
    print()

    # Ubah angka ini untuk menguji ukuran data yang berbeda.
    jumlah_data = 1_000_000
    jumlah_proses = max(2, min(4, os.cpu_count() or 2))

    print(f"Jumlah data : {jumlah_data:,} angka")
    print(f"Proses paralel yang diminta: {jumlah_proses}")
    print(f"CPU logis terdeteksi: {os.cpu_count() or 'tidak diketahui'}")
    print()

    data = buat_data(jumlah_data)

    serial_result, serial_time = jalankan_serial(data)
    parallel_result, parallel_time = jalankan_paralel(data, jumlah_proses)

    print("1. HASIL PEMROSESAN")
    print(f"- Jumlah item : {serial_result['jumlah_item']:,}")
    print(f"- Total       : {serial_result['total']:,}")
    print(f"- Minimum     : {serial_result['nilai_minimum']:,}")
    print(f"- Maksimum    : {serial_result['nilai_maksimum']:,}")
    print()

    print("2. PERBANDINGAN WAKTU")
    print(f"- Serial  : {format_detik(serial_time)}")
    print(f"- Paralel : {format_detik(parallel_time)}")

    if parallel_time > 0:
        speedup = serial_time / parallel_time
        print(f"- Speedup : {speedup:.2f}x")
        if speedup > 1:
            print("- Interpretasi: paralel lebih cepat pada pengujian ini.")
        elif speedup < 1:
            print("- Interpretasi: serial lebih cepat pada pengujian ini.")
        else:
            print("- Interpretasi: waktu kedua metode hampir sama.")
    print()

    print("3. VALIDASI HASIL")
    if serial_result == parallel_result:
        print("- LULUS: hasil serial dan paralel identik.")
    else:
        print("- PERINGATAN: hasil berbeda; periksa implementasi.")
    print()

    print("4. KESIMPULAN")
    print("- Paralelisasi membagi pekerjaan ke beberapa proses.")
    print("- Overhead pembuatan proses dan pemindahan data dapat memengaruhi waktu.")
    print("- Lakukan beberapa kali pengujian dan bandingkan median untuk evaluasi lebih kuat.")
    print("- Benchmark ini demonstrasi konsep HPC, bukan pengukuran superkomputer.")
    print("=" * 68)


if __name__ == "__main__":
    # Blok ini penting untuk Windows agar proses anak tidak menjalankan main lagi.
    main()
