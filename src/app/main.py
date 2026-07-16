import os
import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from src.app.schemas.log import LogInputSchema

# FastAPI uygulamasını başlattık
app = FastAPI(
    title="AI-Powered SecOps Log Agent",
    description="Demirören Medya Bilgi Güvenliği Anomali Tespit API'si",
    version="1.0.0"
)

# Eğittiğin modeli yükleyelim (security_model.pkl nerede duruyorsa ona göre yolunu ayarladık)
MODEL_PATH = "data/processed/security_model.pkl" if os.path.exists("data/processed/security_model.pkl") else "security_model.pkl"

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
else:
    model = None
    print(f"UYARI: Model dosyası {MODEL_PATH} konumunda bulunamadı!")

@app.get("/")
def read_root():
    return {
        "status": "running", 
        "message": "SecOps Log Agent API'sine Hoş Geldiniz!"
    }

# Dinamik olarak log gönderip anomali tespiti yapacağımız endpoint
@app.post("/api/v1/analyze-log")
def analyze_single_log(log_data: LogInputSchema):
    if model is None:
        raise HTTPException(status_code=500, detail="Sistemde eğitilmiş bir ML modeli bulunamadı!")
    
    # 1. Gelen veriyi Pandas DataFrame formatına dönüştürüyoruz (Tıpkı modelin eğitiminde olduğu gibi)
    input_df = pd.DataFrame([log_data.model_dump()])
    
    # 2. Model tahmini: Isolation Forest modelinde -1 anomali, 1 ise normal anlamına gelir
    prediction = model.predict(input_df)[0]
    
    # 3. Sonucu insan diline ve SecOps standartlarına çeviriyoruz
    is_anomaly = bool(prediction == -1)
    status = "SALDIRI/ŞÜPHELİ (Anomaly)" if is_anomaly else "GÜVENLİ (Normal)"
    risk_score = 0.95 if is_anomaly else 0.05  # Şimdilik basit bir risk skoru
    
    return {
        "status": "success",
        "result": {
            "is_anomaly": is_anomaly,
            "classification": status,
            "risk_score": risk_score,
            "received_data": log_data
        }
    }