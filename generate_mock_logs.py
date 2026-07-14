import os 
import random
from datetime import datetime, timedelta 

import os
import random
from datetime import datetime, timedelta

# KURUMSAL VERİ LİSTELERİ (MOCK DATA CONFIG)


# Sistemde kayıtlı olan normal, yasal şirket çalışanları
VALID_USERS = ["sukriye", "ahmet", "mehmet", "ayse", "can", "fatma"]

# Saldırganların tahmin etmeye çalışacağı tehlikeli/geçersiz kullanıcı adları
INVALID_USERS = ["root", "admin", "administrator", "test", "guest", "oracle"]

# Şirket içi güvenli yerel ağ (LAN) IP adresleri
CORPORATE_IPS = ["10.0.2.15", "192.168.1.10", "192.168.1.25", "10.10.5.40"]

# Dış dünyadan gelen ve saldırı simülasyonunda kullanacağımız zararlı IP'ler
MALICIOUS_IPS = ["185.220.101.5", "45.134.22.11", "91.230.44.88"]

# Logların üretileceği sahte sunucu (hostname) isimleri
HOSTNAMES = ["medya-web-prod", "medya-db-ssh", "medya-iam-server"]

def generate_successful_log(current_time : datetime) -> str:
    """
    sistemde kayıtlı yasal bir kullanıcının başarılı giriş logunu üretir.
    Format: Jul 9 14:30:15 hostaneme sshd[PID]: Accepted password for username from IP port PORT ssh2
    """
    timestamp = current_time.strftime("%b %e %H:%M:%S")
    hostname = random.choice(HOSTNAMES)
    pid = random.randint(1000,9999)
    username = random.choice(VALID_USERS)
    ip = random.choice(CORPORATE_IPS)
    port = random.randint(30000,65000)

    return f"{timestamp} {hostname} sshd[{pid}]: Accept password for {username} from {ip} port {port} ssh2\n"
def generate_failed_log(current_time: datetime, is_invalid_user: bool = False, custom_ip: str = None) -> str:
    """
    Başarısız bir giriş denemesi logu üretir. 
    İsteğe bağlı olarak geçersiz kullanıcı (invalid user) ve özel IP adresi alabilir.
    Format: Jul  9 14:32:00 hostname sshd[PID]: Failed password for [invalid user] username from IP port PORT ssh2
    """
    timestamp = current_time.strftime("%b %e %H:%M:%S")
    hostname = random.choice(HOSTNAMES)
    pid = random.randint(10000,99999)
    port = random.randint(30000,65000)

    ip = custom_ip if custom_ip else random.choice(CORPORATE_IPS)

    if is_invalid_user:
        username = random.choice(INVALID_USERS)
        return f"{timestamp} {hostname} sshd[{pid}]: Failed password for invalid user {username} from {ip} port {port} ssh2\n"
    else:
        username = random.choice(VALID_USERS)
        return f"{timestamp} {hostname} sshd[{pid}]: Failed password for {username} from {ip} port {port} ssh2\n"
    

def main() -> None:
    """
    5000 satırlık sentetik auth.log verisi üretir.
    Logların %95'ini normal kurumsal rutinler oluştururken,
    aralara Brute Force ve Zaman Anomalisi senaryoları enjekte edilir.
    """
    # Çıktı klasörünün varlığını kontrol et, yoksa oluştur
    output_dir = os.path.join("data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, "auth.log")
    
    # Başlangıç zamanını bugünün 3 gün öncesi sabah 09:00 olarak ayarlayalım
    start_time = datetime.now() - timedelta(days=3)
    current_time = start_time.replace(hour=9, minute=0, second=0)
    
    logs = []
    total_lines = 5000
    
    print(f"[*] {total_lines} satırlık kurumsal log üretimi başlatıldı...")
    
    i = 0
    while i < total_lines:
        # Rastgelelik kontrolü için 0 ile 100 arasında bir sayı seçiyoruz
        chance = random.randint(0, 100)
        
        # 1. SENARYO: %3 ihtimalle Brute Force (Kaba Kuvvet) Saldırısı Enjekte Et
        if chance < 3 and (total_lines - i) >= 40:
            malicious_ip = random.choice(MALICIOUS_IPS)
            print(f"[!] Saldırı Enjeksiyonu: {malicious_ip} IP adresinden Brute Force simüle ediliyor.")
            
            for _ in range(40):
                # Saldırı logları peş peşe, 1-3 saniye aralıklarla geliyor
                current_time += timedelta(seconds=random.randint(1, 3))
                # Brute force genellikle geçersiz kullanıcı adlarıyla (root, admin) yapılır
                log_line = generate_failed_log(current_time, is_invalid_user=True, custom_ip=malicious_ip)
                logs.append(log_line)
                i += 1
                
        # 2. SENARYO: %2 ihtimalle Gece Sıra Dışı Giriş Anomalisi Enjekte Et
        elif chance >= 3 and chance < 5:
            # Zamanı aniden gece yarısına (02:00 - 05:00) çekiyoruz
            anomaly_time = current_time.replace(hour=random.randint(2, 4), minute=random.randint(0, 59))
            target_user = random.choice(VALID_USERS)
            corporate_ip = random.choice(CORPORATE_IPS)
            
            log_line = f"{anomaly_time.strftime('%b %e %H:%M:%S')} medya-web-prod sshd[{random.randint(10000,99999)}]: Accepted password for {target_user} from {corporate_ip} port {random.randint(30000,65000)} ssh2\n"
            logs.append(log_line)
            i += 1
            
            # Zaman akışını normal düzenine geri almak için küçük bir kaydırma yapıyoruz
            current_time += timedelta(minutes=random.randint(5, 15))
            
        # 3. SENARYO: %95 Normal Kurumsal Trafik (Mesai Saatleri İçi)
        else:
            # Zamanı mesai saatleri içinde tut (09:00 - 18:00)
            if current_time.hour < 9 or current_time.hour > 18:
                current_time = current_time.replace(hour=9)
                
            # Normal trafikte çoğunlukla başarılı, nadiren de şifresini unutan çalışan logu üret
            if random.random() > 0.05:
                log_line = generate_successful_log(current_time)
            else:
                log_line = generate_failed_log(current_time)
                
            logs.append(log_line)
            current_time += timedelta(minutes=random.randint(1, 10))
            i += 1

    # Üretilen logları dosyaya yazalım
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.writelines(logs)
        
    print(f"[+] Başarılı! Sahte log dosyası oluşturuldu: {output_file_path}")


# Kurumsal Python standardı: Script doğrudan çalıştırıldığında main() tetiklensin
if __name__ == "__main__":
    main()