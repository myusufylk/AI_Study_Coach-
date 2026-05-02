"""
AI Service — Google Gemini API entegrasyonu

Tüm AI mantığı (program oluşturma, soru yanıtlama) Gemini modeli üzerinden çalışır.
"""

import json
import logging

import google.generativeai as genai
from django.conf import settings

logger = logging.getLogger(__name__)

# Google Gemini tarafından desteklenen modeller
_MODEL_NAME = "gemini-2.5-flash"  # Hızlı ve verimli model

_ERROR_QUOTA = "API kota limitiniz doldu. Lütfen bir süre bekleyip tekrar deneyin."
_ERROR_AUTH = "API anahtarı geçersiz. Lütfen yöneticiyle iletişime geçin."
_ERROR_NETWORK = (
    "AI servisine bağlanılamadı. "
    "İnternet bağlantınızı kontrol edip tekrar deneyin."
)
_ERROR_EMPTY = "AI boş bir yanıt döndü. Lütfen tekrar deneyin."
_ERROR_UNKNOWN = "Beklenemeyen bir hata oluştu. Lütfen tekrar deneyin."
_ERROR_NO_KEY = (
    "AI servisi şu an kullanılamıyor. Lütfen yöneticiyle iletişime geçin."
)


def _get_api_key():
    """Settings'ten GEMINI API anahtarını doğrulayarak döner; yoksa None."""
    key = getattr(settings, "GEMINI_API_KEY", None)
    if not key or str(key).strip() == "":
        return None
    # Tırnak işaretleri varsa kaldır
    return str(key).strip().strip('"')


def _build_client(api_key):
    """Gemini Client'ını yapılandırır."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(_MODEL_NAME)


def _classify_api_error(error):
    """
    Gemini exception'ını kullanıcı dostu mesaja çevirir.
    Dahili detaylar asla döndürülmez.
    """
    error_str = str(error)

    if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
        return _ERROR_QUOTA
    if "401" in error_str or "UNAUTHENTICATED" in error_str or "PERMISSION_DENIED" in error_str:
        return _ERROR_AUTH
    if "Connection" in error_str or "ConnectError" in error_str or "_InactiveRpcError" in error_str:
        return _ERROR_NETWORK
    
    return _ERROR_UNKNOWN


def ask_ai_coach(user_query):
    """
    Kullanıcının eğitimle ilgili sorusunu Gemini API'ye sorar.
    
    Returns:
        str: AI yanıtı veya kullanıcı dostu hata mesajı.
            Asla exception fırlatmaz.
    """
    if not user_query or not user_query.strip():
        return ""

    api_key = _get_api_key()
    if not api_key:
        logger.error("🚨 GROQ_API_KEY is missing — ask_ai_coach")
        return _ERROR_NO_KEY

    prompt = _build_coach_prompt(user_query)

    try:
        model = _build_client(api_key)
        logger.info("📡 Calling Gemini API for coaching...")
        
        response = model.generate_content(prompt)

        text = response.text.strip() if response.text else None
        
        if not text:
            logger.error("🚨 Gemini returned empty response in ask_ai_coach")
            return _ERROR_EMPTY
        
        logger.info("✅ Gemini coach response received successfully")
        return text

    except Exception as e:
        logger.error(f"🚨 Gemini API error in ask_ai_coach: {type(e).__name__}: {e}")
        return _classify_api_error(e)


def generate_study_program(target_exam, daily_hours, course_names=None):
    """
    Gemini API kullanarak haftalık ders programı oluşturur.

    Returns:
        str: JSON string — başarılı yanıt veya {"error": "..."} formatında
            hata mesajı. Asla exception fırlatmaz.
    """
    logger.info(f"🔍 generate_study_program called: target_exam='{target_exam}', daily_hours={daily_hours}")
    
    # ── Girdi doğrulama ─────────────────────────────────────────────────
    if not target_exam or str(target_exam).strip() == "":
        logger.warning("generate_study_program called with empty target_exam")
        return json.dumps({
            "error": "Hedef sınav bilgisi eksik. "
            "Lütfen profil ayarlarınızı kontrol edin."
        })

    try:
        daily_hours = int(daily_hours)
        if daily_hours <= 0 or daily_hours > 24:
            raise ValueError
    except (TypeError, ValueError):
        logger.warning(
            "generate_study_program called with invalid daily_hours: %s",
            daily_hours,
        )
        return json.dumps({
            "error": "Günlük çalışma saati geçersiz. "
            "Lütfen 1-24 arası bir değer girin."
        })

    # ── API anahtarı ────────────────────────────────────────────────────
    api_key = _get_api_key()
    if not api_key:
        logger.error("🚨 GEMINI_API_KEY is missing — generate_study_program")
        return json.dumps({"error": _ERROR_NO_KEY})
    
    logger.info("✅ API key found, building prompt...")

    # ── Prompt ──────────────────────────────────────────────────────────
    prompt = _build_study_prompt(target_exam, daily_hours, course_names)

    # ── API çağrısı ─────────────────────────────────────────────────────
    try:
        model = _build_client(api_key)
        logger.info("📡 Calling Gemini API for program generation...")
        
        response = model.generate_content(prompt)

        text = response.text.strip() if response.text else None
        
        if not text:
            logger.error("🚨 Gemini returned empty response for study program")
            return json.dumps({"error": _ERROR_EMPTY})
        
        logger.info(f"✅ Gemini program generated successfully ({len(text)} chars)")
        return text

    except Exception as e:
        logger.error(f"🚨 Gemini API error in generate_study_program: {type(e).__name__}: {e}")
        error_msg = _classify_api_error(e)
        return json.dumps({"error": error_msg})


# ─────────────────────────────────────────────────────────────────────────────
# Prompt builders (private)
# ─────────────────────────────────────────────────────────────────────────────
def _build_coach_prompt(user_query):
    """AI Study Coach için yapılandırılmış prompt oluşturur."""
    system_instruction = """Sen "AI Study Coach" adında, Türkçe konuşan, deneyimli bir eğitim koçusun.
Görevin öğrencilere ders çalışma, sınav hazırlığı, motivasyon ve zaman yönetimi konularında rehberlik etmek.

KİŞİLİK KURALLARI:
- Samimi ama profesyonel bir dil kullan; öğrenciyle "sen" diye konuş.
- Empati kur: öğrencinin stresini, kaygısını anladığını hissettir.
- Her yanıtın somut ve uygulanabilir olsun; genel geçer klişelerden kaçın.
- Gerektiğinde küçük örnekler veya senaryolar ver.

YANIT FORMATI:
1. Kısa ve empatik bir giriş cümlesi (1-2 cümle).
2. Sorunun özüne yönelik açıklama veya tavsiyeler — madde işaretleri kullan:
   • Her madde tek bir fikre odaklansın.
   • Somut adımlar sun ("Şunu yap" formatında).
3. Varsa mini günlük/haftalık plan önerisi.
4. Motivasyon veren kısa bir kapanış cümlesi.

ÖNEMLİ KISITLAR:
- Sadece düz metin yaz, Markdown biçimlendirmesi (**, ##, ```) kullanMA.
- Madde işareti olarak sadece "•" karakterini kullan.
- Yanıtını 300 kelimeyi aşmayacak şekilde tut.
- Tıbbi, hukuki veya psikolojik teşhis koyma; gerekirse uzmana yönlendir."""
    
    return f"{system_instruction}\n\n## ÖĞRENCİNİN SORUSU\n{user_query}"


def _build_study_prompt(target_exam, daily_hours, course_names=None):
    """Haftalık program promptunu oluşturur."""
    courses_rule = ""
    if course_names:
        courses_rule = f"\n\n🚨 ÇOK ÖNEMLİ KURAL: PROGRAMA SADECE ŞU DERSLERİ EKLE: {', '.join(course_names)}.\nBU LİSTEDE OLMAYAN HİÇBİR DERSİ KESİNLİKLE PROGRAMA ALMA!"

    return f"""## ROL
Sen Türkiye'nin en başarılı eğitim planlama uzmanlarından birisin.
Görevin: '{target_exam}' sınavına hazırlanan ve günde {daily_hours} saat çalışabilen bir öğrenci için bilimsel temelli, uygulanabilir bir haftalık ders programı oluşturmak.

## PLANLAMA KURALLARI
1. Haftanın 7 gününü de kapsa: Pazartesi, Salı, Çarşamba, Perşembe, Cuma, Cumartesi, Pazar.
2. Günlük toplam ders saati tam olarak {daily_hours} saat olmalı.
3. Her ders bloğu en az 1, en fazla 2 saat olsun.
4. Saatler 08:00 ile 22:00 arasında olmalı.
5. Ardışık 2 saatten fazla aynı ders olmasın — dikkat dağılmasını önle.
6. Her 2 saatlik çalışma bloğundan sonra EN AZ 30 DAKİKA mola planla (molayı "Mola" adıyla ekle).
7. Zor dersleri sabah saatlerine; ezbere dayalı dersleri öğleden sonraya koy.
8. Cumartesi veya Pazar'dan birinde hafif bir tekrar / deneme sınavı günü yap.
9. "ders" değeri Türkçe ders adı olmalı.{courses_rule}
10. Dersleri ve molaları zaman olarak ASLA birbiriyle çakıştırma. Her bir blok birbirini sırasıyla takip etmeli.

## JSON FORMAT — ZORUNLU
Sadece aşağıdaki JSON formatında yanıt ver. Markdown (```json) veya açıklama metni YAZMA.

{{
  "program": [
    {{
      "gun": "Pazartesi",
      "baslangic": "08:00",
      "bitis": "09:00",
      "ders": "Matematik",
      "konu": "Türev — Temel Kurallar",
      "oncelik": "yüksek",
      "tavsiye": "Önce konu anlatımını izle, sonra 10 soru çöz."
    }}
  ]
}}

Alan açıklamaları:
- "gun"       : Günün adı (Pazartesi..Pazar)
- "baslangic" : Başlangıç saati (HH:MM)
- "bitis"     : Bitiş saati (HH:MM)
- "ders"      : Ders adı
- "konu"      : O blokta çalışılacak alt konu başlığı
- "oncelik"   : "yüksek", "orta" veya "düşük"
- "tavsiye"   : O blok için kısa çalışma önerisi (1 cümle)
"""