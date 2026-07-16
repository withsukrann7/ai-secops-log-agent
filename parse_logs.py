import re # search() re'ye ait.
import pandas as pd
from pathlib import Path
#re.match() sadece metnin başına bakar.

# ETL - STEP 1: EXTRACT (VERİ OKUMA)


log_path = Path("data") / "raw" / "auth.log" #güvenli veri okumak için 

if not log_path.exists():
    raise FileNotFoundError(f"[!] Hata: {log_path} dizininde ham log dosyası bulunamadı!")

raw_lines = []
with log_path.open("r", encoding="utf-8", errors="ignore") as file:
    for line in file:
        processed_line = line.strip()
        if processed_line:
            raw_lines.append(processed_line)

print(f"[+] Başarılı! Toplam {len(raw_lines)} satır log bellek üzerine alındı.")


# ETL - STEP 2: TRANSFORM (REGEX İLE AYRIŞTIRMA)

# 'for' kelimesini zorunlu yapıyoruz, sadece 'invalid user' kısmını opsiyonel (? ile) yapıyoruz:
LOG_PATTERN = re.compile(
    r"^(\w+\s+\d{1,2})\s+(\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\w+)\[(\d+)\]:\s+(Accepted|Failed|Accept)\s+password\s+for\s+(?:invalid\s+user\s+)?(\S+)\s+from\s+(\d+\.\d+\.\d+\.\d+)\s+port\s+(\d+)\s+ssh2"
)

parsed_data = [] #yapılandırılmış kayıtlar eklenecek.

for line in raw_lines: #ham logların her satırını geziyoruz.
    match = LOG_PATTERN.search(line) #bu satir uyuyor mu regexe ? uyuyorsa ekliyoruz
    if match: #match , regex eşlemesi anlamına gelir. değişken ismidir.
        status = match.group(6)
        status_code = 1 if status in ["Accepted", "Accept"] else 0 #basarili ise 1 basarisiz ise  0 
        
        parsed_data.append({ #listeye yeni kayit ekliyoruz
            "timestamp": f"{match.group(1)} {match.group(2)}",
            "hostname": match.group(3),
            "pid": int(match.group(5)),
            "status": status,
            "status_code": status_code,
            "username": match.group(7),
            "ip_address": match.group(8),
            "port": int(match.group(9))
        })

print(f"[+] Regex taraması bitti. {len(parsed_data)} satır başarıyla ayrıştırıldı.")


# ETL - STEP 3: LOAD (PANDAS VE CSV KAYDETME)  


# GÖREV 1: 'parsed_data' listesini Pandas DataFrame'e dönüştür.
df = pd.DataFrame(parsed_data)

# GÖREV 2: "data/processed" klasörü var mı kontrol et, yoksa otomatik oluştur.
processed_dir = Path("data") / "processed"
if not processed_dir.exists():

    processed_dir.mkdir(parents=True, exist_ok=True)#klasör oluşturmak için kullanilir.|parants=true eğer üst klasörler yoksa oluşturur.| exits_ok = true ise klasör varsa hata vermez.varsa oluşturur


# GÖREV 3: df tablosunu "data/processed/cleaned_auth_logs.csv" olarak kaydet (index=False olsun).
output_file = processed_dir / "cleaned_auth_logs.csv"
df.to_csv(output_file, index=False)

print(f"[+] Tebrikler! Temizlenmiş loglar başarıyla {output_file}  dosyasına kaydedildi.")
