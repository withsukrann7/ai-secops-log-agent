import pandas as pd
from pathlib import Path
# Yapay zeka kütüphanemizden ihtiyacımız olan araçları çağırıyoruz
from sklearn.model_selection import train_test_split #sklearn makine öğrenmesi kütüphanesi,#train_test_split ise verimizi eğitim ve test olarak bölmek için kullandim hazir bir fonksiyon
from sklearn.ensemble import RandomForestClassifier #enseble algoritma topluluğu, #randomforestclassifier sınıflandırma problemi için kullanılan karar ağacı bulunan algoritma. saldırı0 güvenli 1.
from sklearn.metrics import accuracy_score #modelimizi ne kadar iyi çalıştığını ölçen matematiksel metrikler..accuracy_score ise doğrululuk oranını hesaplar.


# 1. ADIM: VERİYİ YÜKLEME

output_file = Path("data") / "processed" / "cleaned_auth_logs.csv"

if not output_file.exists():
    raise FileNotFoundError("[!] Temizlenmiş log dosyası bulunamadı! Önce parse_logs.py çalıştırılmalı.")

df = pd.read_csv(output_file)


# 2. ADIM: YAPAY ZEKA İÇİN HEDEF VE ÖZELLİKLERİ SEÇME

# Modelimizin tahmin etmesini istediğimiz siber güvenlik durumu (0: Başarısız, 1: Başarılı)
y = df['status_code']

# x , modeli besleyeceğin giriş verisi
X = df[['pid', 'port']]


# 3. ADIM: SINAV HAZIRLIĞI (VERİYİ BÖLME)

# Verinin %80'ini eğitime, %20'sini  sınavına ayırıyoruz
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"[*] Yapay Zeka Hazırlığı Tamamlandı!")
print(f"[*] Eğitim için {X_train.shape[0]} satır veri kullanılacak.")
print(f"[*] Test (Sınav) için {X_test.shape[0]} satır veri ayrıldı.")

model = RandomForestClassifier(random_state=42) #42 olmasının sebebi verilerin içinden rastgele örnekler seçerek yüzlerce farklı karar ağacı oluşturur.ağaç yapısının aynı kalması için 42 yazdim.
model.fit(X_train, y_train) #fit() burada eğitiyoruz. ipucları ve doğru cevapları vererek.

y_pred = model.predict(X_test) #predict() model artik eğitildi. şimdi onu sınava sokuyoruz.
accuracy = accuracy_score(y_test, y_pred)#gerçek cevap anahtarını ve yapay zeka sınav kağıdını yan yana koyup karşılaştırır.ve oran döndürür.

print(f"[+] Yapay Zekâ Eğitimi Başarıyla Tamamlandı!")
print(f"[+] Modelin Siber Saldırı Tespit Başarı Oranı: %{accuracy * 100:.2f}")


