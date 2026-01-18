import math
import random
import json
import pandas as pd
import time
from db import DB

class SmartSampler:
    def __init__(self):
        # 1. Veritabanını ayağa kaldır (Indexler RAM'e yüklenir)
        print("Veritabanına bağlanılıyor...")
        self.db = DB()
        self.population_size = len(self.db.index)
        print(f"Bağlandı! Evren Büyüklüğü (N): {self.population_size}")

    def calculate_sample_size(self, confidence_level=0.95, margin_error=0.05):
        """
        Cochran Formülü ile gerekli örneklem büyüklüğünü (n) hesaplar.
        """
        # Z-Skoru Tablosu (Güven Düzeyi -> Z Değeri)
        z_scores = {
            0.90: 1.645,
            0.95: 1.96,
            0.99: 2.576
        }
        z = z_scores.get(confidence_level, 1.96)
        p = 0.5
        N = self.population_size

        # n0 = (Z^2 * p * (1-p)) / e^2
        numerator = (z**2 * p * (1-p))
        denominator = margin_error**2
        n0 = numerator / denominator

        # (Finite Population Correction)
        # Bizim N değerimiz belli olduğu için bunu yapmak zorundayız.
        n = n0 / (1 + ((n0 - 1) / N))

        return math.ceil(n) # Küsuratlı çıkarsa yukarı yuvarla

    def create_sample_dataset(self, output_csv="orneklem.csv", confidence=0.95, error=0.05):
        n = self.calculate_sample_size(confidence, error)

        print("\n İSTATİSTİKSEL ANALİZ:")
        print(f"   - Hedef Güven Düzeyi: %{confidence*100}")
        print(f"   - Kabul Edilen Hata: %{error*100}")
        print(f"   - Gereken Örneklem (n): {n} adet")
        print("-" * 40)

        # 2. Tüm anahtarları al ve Rastgele Seç (Simple Random Sampling)
        # RAM'deki index listesinden rastgele seçim yapıyoruz (Çok hızlı).
        all_keys = list(self.db.index.keys())

        # Eğer istenen sayı eldeki maldan fazlaysa hepsini al
        if n > len(all_keys):
            n = len(all_keys)

        selected_keys = random.sample(all_keys, n)

        print(f"{n} adet veri diskten çekiliyor (Random Access)...")
        start_time = time.time()

        data_rows = []

        # 3. Seçilen anahtarları diskten tek tek çek
        for key in selected_keys:
            # O(1) Hızında okuma!
            raw_json = self.db.oku(key) 

            if raw_json:
                # JSON String -> Python Dict
                record = json.loads(raw_json)
                data_rows.append(record)

        duration = time.time() - start_time
        print(f"Çekme işlemi bitti! Süre: {duration:.4f} saniye")

        # 4. Pandas ile CSV'ye kaydet (Analiz için hazır hale getir)
        df_sample = pd.DataFrame(data_rows)
        df_sample.to_csv(output_csv, index=False)
        print(f"Örneklem dosyası kaydedildi: {output_csv}")
        
        return df_sample

# Test:
if __name__ == "__main__":
    sampler = SmartSampler()
    
    # %95 Güven, %3 Hata payı ile örneklem çekelim
    df = sampler.create_sample_dataset(confidence=0.95, error=0.03)
    
    print("\n Örneklemden ilk 5 satır:")
    print(df.head())
