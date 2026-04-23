import json
from google import genai
from django.conf import settings

def generate_study_program(target_exam, daily_hours):
    """
    Öğrenci için Gemini AI kullanarak haftalık ders programı oluşturur.
    """
    prompt = f"""
    Sen uzman bir eğitim planlama koçusun. Hedefi '{target_exam}' olan ve günde '{daily_hours}' saat çalışmak isteyen bir öğrenci için haftalık ders çalışma programı hazırla.
    
    LÜTFEN SADECE AŞAĞIDAKİ JSON FORMATINDA CEVAP VER. Markdown (```json) kullanma, sadece saf JSON döndür.
    Format tam olarak şöyle olmalı:
    {{
        "program": [
            {{"gun": "Pazartesi", "baslangic": "08:00", "bitis": "09:00", "ders": "Matematik"}},
            {{"gun": "Pazartesi", "baslangic": "09:00", "bitis": "10:00", "ders": "Fizik"}},
            ...
        ]
    }}
    Günler şunlardan biri olmalıdır: Pazartesi, Salı, Çarşamba, Perşembe, Cuma, Cumartesi, Pazar.
    Saatler 08:00 ile 22:00 arasında olmalıdır.
    """

    try:
        # YENİ KULLANIM: Artık Client üzerinden istek atıyoruz
        client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )

        return response.text

    except Exception as e:
        error_str = str(e)

        # Senin yazdığın o başarılı hata kontrolleri
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            return json.dumps({
                "error": "API kota limitiniz doldu. Lütfen Google Cloud Console'dan proje kota bilgilerinizi ve faturalandırmayı kontrol edin.",
                "details": error_str
            })
        elif "401" in error_str or "API_KEY_INVALID" in error_str:
            return json.dumps({
                "error": "API anahtarı geçersiz veya yetkili değil.",
                "details": error_str
            })
        else:
            # Hata durumunda da boş bir program dönerek JS'in çökmesini engelliyoruz
            return json.dumps({
                "error": f"Hata oluştu: {error_str}",
                "details": error_str
            })