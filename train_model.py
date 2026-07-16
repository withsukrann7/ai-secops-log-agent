import pandas as pd
from pathlib import Path
# Yapay zeka kütüphanemizden ihtiyacımız olan araçları çağırıyoruz
from sklearn.model_selection import train_test_split #sklearn makine öğrenmesi kütüphanesi,#train_test_split ise verimizi eğitim ve test olarak bölmek için kullandim hazir bir fonksiyon
from sklearn.ensemble import RandomForestClassifier #enseble algoritma topluluğu, #randomforestclassifier sınıflandırma problemi için kullanılan karar ağacı bulunan algoritma. saldırı0 güvenli 1.
from sklearn.metrics import accuracy_score #modelimizi ne kadar iyi çalıştığını ölçen matematiksel metrikler..accuracy_score ise doğrululuk oranını hesaplar.
import pickle #python nesnelerini diske bir dosya olarak yazmamızı sağlar
import matplotlib.pyplot as plt

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

#modeli diske kaydetmek

model_path = Path("data") / "processed" / "security_model.pkl"
with open(model_path,"wb") as file:
    pickle.dump(model,file)
print(f"yapay zeka modeli başarıyla diske kaydedildi:{model_path}")

yeni_log_saldiri = {
    "pid": 72734,
    "port":52971
}
yeni_log_guvenli = {
    "pid":1915,
    "port":37349
    
}
yeni_veri = pd.DataFrame([yeni_log_saldiri, yeni_log_guvenli])

with open(model_path,"rb") as file:
    loaded_model = pickle.dump = pickle.load(file)

tahminler = loaded_model.predict(yeni_veri)

for i, tahmin in enumerate(tahminler):
    log_tipi = "Saldırı Logu" if i == 0 else "Normal Log"
    if tahmin == 0:
        print(f"⚠️ [TEHLİKE] {log_tipi} Analiz Edildi -> SONUÇ: ŞÜPHELİ SIZMA GİRİŞİMİ TESPİT EDİLDİ!")
    else:
        print(f"✅ [GÜVENLİ] {log_tipi} Analiz Edildi -> SONUÇ: Başarılı Giriş Yetkilendirildi.")


# =====================================================================
# 8. ADIM: VERİ GÖRSELLEŞTİRME (VISUALIZATION)
# =====================================================================
# Log verilerimizdeki 0 (saldırı) ve 1 (başarılı giriş) sayılarını sayıyoruz
durum_sayilari = df['status_code'].value_counts()

# Grafik alanını oluşturuyoruz (Genişlik: 6, Yükseklik: 4 inç)
plt.figure(figsize=(6, 4))

# Çubuk grafiği (Bar Plot) çizdiriyoruz. 
# 0 için kırmızı (Tehlike), 1 için yeşil (Güvenli) renk veriyoruz.
durum_sayilari.plot(kind='bar', color=['red', 'green'])

# Grafiğin başlık ve eksen isimlerini yazıyoruz
plt.title('Log Dağılım Grafiği (Yapay Zeka Analizi)')
plt.xlabel('Giriş Durumu')
plt.ylabel('Log Satır Sayısı')

# Eksen üzerindeki 0 ve 1 sayılarını daha okunur kelimelerle değiştiriyoruz
plt.xticks(ticks=[0, 1], labels=['Saldırı / Başarısız (0)', 'Güvenli / Başarılı (1)'], rotation=0)

# Arkaya hafif kesikli çizgilerden bir ızgara (grid) ekliyoruz ki sayılar rahat okunsun
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Oluşan bu harika grafiği "data/processed/log_distribution_chart.png" adıyla kaydediyoruz
chart_path = Path("data") / "processed" / "log_distribution_chart.png"
plt.savefig(chart_path)
print(f"[+] Görsel grafik başarıyla kaydedildi: {chart_path}")

# Grafiği bilgisayar ekranında canlı olarak açıyoruz
plt.show()