# AI-SecOps: Intelligent Log Anomaly & Incident Response System

## 📌 Proje Hakkında
Bu proje, Demirören Medya Bilgi Güvenliği ve Risk Yönetimi departmanı bünyesinde, kurumsal altyapıların güvenliğini artırmak amacıyla geliştirilen **Yapay Zekâ Destekli Otomatik Log Anomali ve Olay Müdahale (Incident Response) Sistemi**'dir.

Sistem, geleneksel kural tabanlı (SIEM) yapıların kaçırabileceği yapısal olmayan log anomalilerini Makine Öğrenmesi (ML) algoritmaları ile tespit eder. Tesit edilen tehditleri LLM (Large Language Model) tabanlı bir Siber Güvenlik Ajanı (Agentic AI) ve RAG (Retrieval-Augmented Generation) mimarisi vasıtasıyla analiz ederek otomatik müdahale planları (Playbook) ve dinamik risk skorları üretir.

## 🛠️ Teknolojik Altyapı
* **Backend & API:** FastAPI (Asenkron Python Mikroservis)
* **Machine Learning:** Scikit-Learn (Unsupervised Anomaly Detection - Isolation Forest)
* **AI & LLM Orkestrasyonu:** LangChain / LangGraph, Ollama / OpenAI API
* **Vektör Veri Tabanı:** FAISS (Semantik Tehdit İstihbaratı Araması)
* **Veri Yönetimi & DB:** Pandas, NumPy, PostgreSQL, SQLAlchemy
* **Konteynerleştirme:** Docker, Docker Compose

## 🚀 Mevcut Durum (Geliştirme Aşaması)
