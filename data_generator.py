from sklearn.datasets import fetch_california_housing
import pandas as pd
import os

def generate_data():

    # Gerçek veriyi çekme:
    data = fetch_california_housing()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['Price'] = data.target

    # Big Data Simülasyonu veriyi 50 kat büyütme:
    print("Veri şişiriliyor (Big Data Simülasyonu)...")
    df_big = pd.concat([df] * 50, ignore_index=True)

    # CSV Olarak Kaydetme:
    output_file = "big_data.csv"
    if os.path.exists(output_file):
        os.remove(output_file)

    # İndexleme:
    df_big.to_csv(output_file, index_label="id")

    print("İşlem Sonuçlandı:")
    print(f"Toplam Satır: {len(df_big)}")
    print(f"Dosya Boyutu: {os.path.getsize(output_file) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    generate_data()
