import csv
import json
import time
import os
from db import DB  # Adını db.py yapmıştık

class PyCaskSampler:
    def __init__(self, db_path="database.data"):
        # Veritabanını başlat
        self.db = DB()
        print(f"Veritabanı motoru bağlandı. Mevcut Kayıt Sayısı: {len(self.db.index)}")

    def ingest_csv(self, csv_path):
        if not os.path.exists(csv_path):
            print(f"Hata: {csv_path} bulunamadı. Önce data_generator.py çalıştır.")
            return

        print(f"Ingestion başlıyor: {csv_path} -> Binary DB")
        start_time = time.time()

        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)

            count = 0
            for row in reader:
                key = f"ev_{row['id']}"

                value = json.dumps(row)

                self.db.yaz(key, value)

                count += 1
                if count % 100000 == 0:
                    print(f"   Writing... {count} satır işlendi.")

        duration = time.time() - start_time
        print(f"İşlem Tamamlandı! {count} kayıt veritabanına gömüldü.")
        print(f"Süre: {duration:.2f} saniye")

# Test Bloğu
if __name__ == "__main__":
    app = PyCaskSampler()
    app.ingest_csv("big_data.csv")
