"""
SESI 4 — Klasifikasi Jenis Bunga Menggunakan Machine Learning
Topik webinar: Introduction to Machine Learning

Tujuan:
- Melatih model klasifikasi Random Forest.
- Membagi data menjadi data latih dan data uji.
- Mengukur accuracy, precision, recall, F1-score, dan confusion matrix.
- Menunjukkan alur kerja machine learning end-to-end.

Dataset:
- Dataset Iris bawaan scikit-learn.
- Data ini nyata dan umum digunakan untuk pembelajaran; bukan data buatan proyek.

Instalasi:
    python -m pip install scikit-learn

Jalankan:
    python klasifikasi_ml.py
"""

def main():
    try:
        from sklearn.datasets import load_iris
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import (
            accuracy_score,
            classification_report,
            confusion_matrix,
        )
    except ImportError:
        print("Library scikit-learn belum terpasang.")
        print("Pasang dengan perintah: python -m pip install scikit-learn")
        return

    # 1. Memuat dataset
    iris = load_iris()
    X = iris.data
    y = iris.target
    class_names = iris.target_names

    print("=" * 64)
    print("SESI 4: KLASIFIKASI JENIS BUNGA MENGGUNAKAN RANDOM FOREST")
    print("=" * 64)
    print("Dataset: Iris (150 sampel, 4 fitur pengukuran)")
    print(f"Fitur: {', '.join(iris.feature_names)}")
    print()

    # 2. Membagi data menjadi data latih dan data uji
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # 3. Membuat dan melatih model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
    )
    model.fit(X_train, y_train)

    # 4. Melakukan prediksi pada data yang tidak digunakan saat pelatihan
    y_pred = model.predict(X_test)

    # 5. Evaluasi model
    accuracy = accuracy_score(y_test, y_pred)

    print("1. RINGKASAN DATA")
    print(f"- Data latih: {len(X_train)} sampel")
    print(f"- Data uji  : {len(X_test)} sampel")
    print()

    print("2. HASIL EVALUASI")
    print(f"- Accuracy: {accuracy:.3f} ({accuracy * 100:.1f}%)")
    print()
    print("Classification report:")
    print(classification_report(
        y_test,
        y_pred,
        target_names=class_names,
        zero_division=0,
    ))

    print("Confusion matrix (baris = label asli, kolom = prediksi):")
    print(confusion_matrix(y_test, y_pred))
    print()

    # 6. Contoh prediksi untuk satu sampel uji
    sample = X_test[0].reshape(1, -1)
    prediction = model.predict(sample)[0]
    print("3. CONTOH PREDIKSI")
    print(f"- Pengukuran sampel: {X_test[0].tolist()}")
    print(f"- Label sebenarnya : {class_names[y_test[0]]}")
    print(f"- Prediksi model   : {class_names[prediction]}")
    print()

    print("4. INTERPRETASI")
    print("- Accuracy menunjukkan proporsi prediksi yang benar pada data uji.")
    print("- Precision, recall, dan F1-score ditampilkan untuk setiap kelas.")
    print("- Confusion matrix membantu melihat kelas yang tertukar.")
    print("- Hasil bisa berubah jika dataset, pembagian data, atau parameter diubah.")
    print("- Ini contoh pembelajaran machine learning, bukan model tutupan lahan.")
    print("=" * 64)


if __name__ == "__main__":
    main()
