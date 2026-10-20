"""
SESI 5 — Dashboard Interaktif Pemantauan Lingkungan
Topik webinar: Human-Computer Interaction and Data Visualization

Tujuan:
- Menampilkan metrik lingkungan dalam dashboard.
- Memungkinkan pengguna memilih variabel untuk divisualisasikan.
- Memahami prinsip UI sederhana: judul jelas, pilihan pengguna, ringkasan, grafik, dan catatan.

Library yang dibutuhkan:
    python -m pip install streamlit pandas matplotlib

Jalankan:
    python -m streamlit run dashboard_visualisasi.py

Data yang ditampilkan adalah data SIMULASI, bukan pengukuran nyata.
"""

from datetime import datetime

try:
    import pandas as pd
    import streamlit as st
    import matplotlib.pyplot as plt
except ImportError as exc:
    raise SystemExit(
        "Library belum terpasang. Jalankan:\n"
        "python -m pip install streamlit pandas matplotlib"
    ) from exc


st.set_page_config(
    page_title="EcoTrend | Dashboard Lingkungan",
    page_icon="🌿",
    layout="wide",
)

st.title("🌿 EcoTrend — Dashboard Pemantauan Lingkungan")
st.caption("Sesi 5: Human-Computer Interaction dan Visualisasi Data")
st.warning(
    "Data di dashboard ini adalah SIMULASI untuk demonstrasi. "
    "Jangan gunakan sebagai laporan kondisi lingkungan nyata."
)

# Data contoh untuk dashboard
data = pd.DataFrame({
    "Bulan": [
        "Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
        "Jul", "Agu", "Sep", "Okt", "Nov", "Des"
    ],
    "Suhu (°C)": [29.1, 29.4, 30.0, 30.2, 30.8, 31.3, 32.0, 32.4, 31.7, 30.9, 29.8, 29.3],
    "Curah Hujan (mm)": [310, 280, 245, 190, 135, 90, 42, 25, 55, 145, 230, 295],
    "NDVI": [0.72, 0.70, 0.68, 0.65, 0.61, 0.58, 0.51, 0.47, 0.50, 0.59, 0.66, 0.71],
})

st.sidebar.header("Pengaturan Tampilan")
variabel = st.sidebar.selectbox(
    "Pilih variabel yang ingin dilihat",
    ["Suhu (°C)", "Curah Hujan (mm)", "NDVI"],
)
jenis_grafik = st.sidebar.radio(
    "Jenis grafik",
    ["Garis", "Batang"],
    horizontal=True,
)

# Metrik ringkas
col1, col2, col3 = st.columns(3)
col1.metric("Rata-rata Suhu", f"{data['Suhu (°C)'].mean():.1f} °C")
col2.metric("Total Curah Hujan", f"{data['Curah Hujan (mm)'].sum():.0f} mm")
col3.metric("Rata-rata NDVI", f"{data['NDVI'].mean():.2f}")

st.subheader(f"Tren Bulanan: {variabel}")
fig, ax = plt.subplots(figsize=(10, 4))
if jenis_grafik == "Garis":
    ax.plot(data["Bulan"], data[variabel], marker="o")
else:
    ax.bar(data["Bulan"], data[variabel])

ax.set_xlabel("Bulan")
ax.set_ylabel(variabel)
ax.grid(True, alpha=0.25)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

with st.expander("Lihat tabel data"):
    st.dataframe(data, use_container_width=True)

st.subheader("Interpretasi dan Catatan")
if variabel == "Suhu (°C)":
    st.write(
        "Pada data simulasi, suhu naik menuju pertengahan tahun lalu turun "
        "menjelang akhir tahun. Pola ini hanya menggambarkan data contoh."
    )
elif variabel == "Curah Hujan (mm)":
    st.write(
        "Pada data simulasi, curah hujan lebih rendah di pertengahan tahun "
        "dan lebih tinggi di awal serta akhir tahun."
    )
else:
    st.write(
        "NDVI simulasi turun di pertengahan tahun lalu meningkat kembali. "
        "NDVI nyata perlu dihitung dari citra satelit yang sesuai."
    )

st.info(
    "Prinsip antarmuka: pilihan variabel mudah ditemukan, metrik utama terlihat, "
    "grafik diberi label, dan keterbatasan data dijelaskan."
)
