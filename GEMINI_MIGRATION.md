# AI Study Coach - Groq to Gemini API Migration

## 🔄 Yapılan Değişiklikler

Proje başarılı bir şekilde **Groq API**'den **Google Gemini API**'ye migre edildi.

### 📝 Değiştirilen Dosyalar

#### 1. `ai_learning_ecosystem/settings.py`
- **Eski:** `GROQ_API_KEY = os.getenv('GROQ_API_KEY')`
- **Yeni:** `GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')`

#### 2. `core/ai_service.py`
- **Import Değişikliği:** 
  ```python
  # Eski
  from groq import Groq
  
  # Yeni
  import google.generativeai as genai
  ```

- **Model Değişikliği:** 
  ```python
  # Eski: "mixtral-8x7b-32768"
  # Yeni: "gemini-2.0-flash"
  ```

- **API Client:**
  ```python
  # Eski
  def _build_client(api_key):
      return Groq(api_key=api_key)
  
  # Yeni
  def _build_client(api_key):
      genai.configure(api_key=api_key)
      return genai.GenerativeModel(_MODEL_NAME)
  ```

- **API Çağrı Metodları:**
  ```python
  # Eski: client.chat.completions.create()
  # Yeni: model.generate_content()
  ```

- **Hata Yönetimi:** Gemini-specific hata kodları için güncellendi (RESOURCE_EXHAUSTED, UNAUTHENTICATED, etc.)

#### 3. `test_grok.py`
- Test başlığı "xAI Grok API" → "Google Gemini API" olarak güncellendi

#### 4. `.env.example` (Yeni Dosya)
- Gemini API anahtarı yapılandırması için örnek dosya oluşturuldu

---

## 🚀 Kurulum Adımları

### 1. Gemini API Anahtarı Alma

1. https://ai.google.dev adresine gidin
2. "Get API Key" butonuna tıklayın
3. Google hesabınızla giriş yapın
4. Yeni bir API anahtarı oluşturun

### 2. Ortam Değişkenini Ayarlayın

**Seçenek A: `.env` dosyası kullanarak**
```bash
cp .env.example .env
# .env dosyasını açıp GEMINI_API_KEY değerini yapıştırın
```

**Seçenek B: Sistem ortam değişkeni olarak**
```bash
# Windows PowerShell
$env:GEMINI_API_KEY = "your_api_key_here"

# Windows CMD
set GEMINI_API_KEY=your_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_api_key_here
```

### 3. Uygulamayı Çalıştırın

```bash
python manage.py runserver
```

---

## ✅ Test Etme

Test scriptini çalıştırarak API integasyonunun düzgün çalışıp çalışmadığını kontrol edin:

```bash
python test_grok.py
```

Başarılı çıktı:
```
============================================================
Testing Google Gemini API Integration
============================================================

Response length: XXXX chars
✅ SUCCESS!
   Program blocks: XX
   First block: Pazartesi - Matematik (08:00-09:00)
```

---

## 📊 API Karşılaştırması

| Özellik | Groq | Gemini |
|---------|------|--------|
| **Model** | mixtral-8x7b-32768 | gemini-2.0-flash |
| **Dil** | Python (groq) | Python (google-genai) |
| **Hız** | Yüksek | Çok Yüksek |
| **Maliyet** | Ücretsiz | Ücretsiz (limitli) |
| **Özellikler** | Chat API | Multimodal, Vision |

---

## 🔍 Önemli Notlar

- **Gemini API**: `gemini-2.0-flash` modeli en hızlı ve verimli seçenektir
- **Alternatif Modeller**: `gemini-1.5-pro`, `gemini-1.5-flash` da kullanılabilir
- **Token Limitleri**: Gemini'nin kendi rate limiting kuralları vardır - API panelinde kontrol edin
- **Hata Yönetimi**: Proje artık Gemini-specific hata kodlarını işliyor

---

## 🆘 Sorun Giderme

### "GEMINI_API_KEY is missing" hatası
- `.env` dosyasında `GEMINI_API_KEY` tanımlanmış mı kontrol edin
- Ortam değişkenlerini kontrol edin
- Django'yu yeniden başlatın

### API Bağlantı Hataları
- İnternet bağlantısını kontrol edin
- API anahtarının geçerli olup olmadığını kontrol edin
- https://ai.google.dev adresinde kota limitini kontrol edin

### JSON Parse Hataları
- Model yanıtının geçerli JSON formatında olduğundan emin olun
- Prompt'taki JSON formatı talimatlarını kontrol edin

---

## 📚 Kaynaklar

- [Google Gemini API Docs](https://ai.google.dev/docs)
- [google-generativeai Python SDK](https://github.com/google/generative-ai-python)
- [Django Environment Variables](https://docs.djangoproject.com/en/stable/)
