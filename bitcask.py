import struct

class DB:
    def __init__(self) -> None:
        self.dosya = open("database.data","ab+")
        self.index = {}
        
        self.yukle()

    def yaz(self,key,value):
        key_bytes = key.encode("utf-8")
        val_bytes = value.encode("utf-8")

        key_len = len(key_bytes)
        val_len = len(val_bytes)

        # Packet:
        header = struct.pack("II",key_len,val_len)
        tam_veri = header + key_bytes + val_bytes
        
        konum = self.dosya.tell()
        self.dosya.write(tam_veri)
        self.dosya.flush()

        self.index[key] = konum

    def oku(self,key):
        if key not in self.index:
            return None

        konum = self.index[key]
        self.dosya.seek(konum)

        header_data = self.dosya.read(8)

        key_len, val_len = struct.unpack("II",header_data)
        
        self.dosya.read(key_len)
        value_bytes = self.dosya.read(val_len)

        return value_bytes.decode("utf-8")

    def yukle(self):
        self.dosya.seek(0)

        while True:
            baslangic_konum = self.dosya.tell()

            header_data = self.dosya.read(8)
            if len(header_data) < 8:
                break

            
            key_len, val_len = struct.unpack("II",header_data)
            key_bytes = self.dosya.read(key_len)
            self.dosya.read(val_len)
            key = key_bytes.decode(("utf-8"))

            self.index[key] = baslangic_konum

db = DB()

print("Girdiler:")
db.yaz("kullanici_1", "Ali")
db.yaz("kullanici_2", "Veli")

print("Okunuyor")
gelen_veri = db.oku("kullanici_1")
print(f"kullanici_1: {gelen_veri}")
print(f"kullanici_1 için veritabanından gelen değer: {gelen_veri}")

print(f"Olmayan veri testi: {db.oku("mehmet")}")

print("--- Hafıza Testi ---")
print(f"kullanici_1: {db.oku('kullanici_2')}")
