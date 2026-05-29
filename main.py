import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

import database
import user_db

# Initialize user database
user_db.init_db()

app = FastAPI(title="Otomobil Danışmanı Chatbot", description="Kullanıcı tercihlerine göre araç önerileri sunan asistan.")

# Statik dosyaları sunmak için klasörü kontrol et ve yoksa oluştur
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# İstek ve Yanıt Şemaları
class RegisterRequest(BaseModel):
    adSoyad: str
    email: str
    sifre: str

class LoginRequest(BaseModel):
    email: str
    sifre: str

class FilterRequest(BaseModel):
    budget: Optional[int] = None
    body_types: Optional[List[str]] = None
    fuel_types: Optional[List[str]] = None
    transmissions: Optional[List[str]] = None
    priorities: Optional[List[str]] = None

class ChatMessage(BaseModel):
    role: str  # "user" veya "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []
    api_key: Optional[str] = None

class CompareRequest(BaseModel):
    car_ids: List[int]

# Verification Dependency
def verify_user(x_user_id: Optional[str] = Header(None)):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Oturum açmanız gerekiyor.")
    try:
        uid = int(x_user_id)
        user = user_db.get_user_by_id(uid)
        if not user:
            raise HTTPException(status_code=401, detail="Geçersiz kullanıcı.")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Geçersiz kullanıcı.")

# Auth API Uç Noktaları

@app.post("/api/auth/register")
def register(request: RegisterRequest):
    try:
        res = user_db.register_user(request.adSoyad, request.email, request.sifre)
        return {
            "id": res["id"],
            "adSoyad": res["name"],
            "email": res["email"],
            "message": "Kayıt başarıyla tamamlandı!"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Kayıt sırasında beklenmedik bir hata oluştu.")

@app.post("/api/auth/login")
def login(request: LoginRequest):
    try:
        res = user_db.login_user(request.email, request.sifre)
        return {
            "id": res["id"],
            "adSoyad": res["name"],
            "email": res["email"],
            "message": "Giriş başarılı!"
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Giriş sırasında beklenmedik bir hata oluştu.")

# API Uç Noktaları

@app.get("/api/cars")
def get_all_cars(user: dict = Depends(verify_user)):
    """Tüm otomobillerin listesini döner."""
    return database.CAR_DATABASE

@app.get("/api/status")
def get_status():
    """Sistemde varsayılan bir Gemini API anahtarı olup olmadığını bildirir."""
    has_env_key = bool(os.environ.get("GEMINI_API_KEY"))
    return {"has_env_key": has_env_key}

@app.get("/api/cars/{car_id}")
def get_car(car_id: int, user: dict = Depends(verify_user)):
    """Belirli bir otomobilin detaylarını döner."""
    car = database.get_car_by_id(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Otomobil bulunamadı")
    return car

@app.post("/api/recommend")
def recommend_cars(request: FilterRequest, user: dict = Depends(verify_user)):
    """Kriterlere göre filtrelenmiş ve puanlanmış otomobilleri döner."""
    return database.filter_cars(
        budget=request.budget,
        body_types=request.body_types,
        fuel_types=request.fuel_types,
        transmissions=request.transmissions,
        priorities=request.priorities
    )

@app.post("/api/chat")
def chat_endpoint(request: ChatRequest, user: dict = Depends(verify_user)):
    """Kullanıcı mesajına göre sohbet yanıtı döner (Gemini veya Kural Tabanlı)."""
    # Sohbet geçmişini database modülüne uygun formata dönüştür
    history_list = [{"role": msg.role, "content": msg.content} for msg in request.history]
    response_text = database.get_ai_response(request.message, history_list, api_key=request.api_key)
    return {"response": response_text}

# Statik web arayüzünü sunma
@app.get("/")
def read_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Arayüz dosyası bulunamadı. Lütfen index.html dosyasını oluşturun."}

# Statik dosyaları bağla
app.mount("/static", StaticFiles(directory=static_dir), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
