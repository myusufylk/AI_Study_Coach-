import google.generativeai as genai
from django.conf import settings

def generate_study_program(target_exam, daily_hours):
    """
    Öğrenci için Gemini AI kullanarak haftalık ders programı oluşturur.
    """
    try:
        # HATA DÜZELTME: 'genai.Client' yerine yapılandırma ve model seçimi kullanılır.
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = f"""
        Bir öğrenci için haftalık çalışma programı oluştur. 
        Yanıtı SADECE ve SADECE geçerli bir JSON formatında döndür. 
        Başına veya sonuna ```json gibi işaretler veya hiçbir açıklama ekleme.

        Hedef sınav: {target_exam}
        Günlük çalışma süresi: {daily_hours} saat

        JSON Şeması şu şekilde OLMALIDIR:
        {{
          "program": [
            {{"gun": "Pazartesi", "ders": "Matematik", "baslangic": "09:00", "bitis": "11:00"}},
            {{"gun": "Salı", "ders": "Fizik", "baslangic": "10:00", "bitis": "12:00"}}
          ]
        }}
        
        Kurallar:
        1. Pazartesi, Salı, Çarşamba, Perşembe, Cuma, Cumartesi, Pazar günlerini içermelidir.
        2. Her gün için {daily_hours} saatlik ders dağılımı yap.
        3. Saatleri HH:MM (Örn: 09:00) formatında yaz.
        """

        # Yeni kütüphane yapısına göre içerik üretimi
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            )
        )

        return response.text

    except Exception as e:
        error_str = str(e)
        
        # Senin yazdığın o başarılı hata kontrollerini buraya entegre ediyoruz
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            return '{"error": "API kota limitiniz doldu. Lütfen yeni bir anahtar oluşturun."}'
        elif "401" in error_str or "API_KEY_INVALID" in error_str:
            return '{"error": "API anahtarı geçersiz."}'
        else:
            # Hata durumunda da boş bir program dönerek JS'in çökmesini engelliyoruz
            return f'{{"error": "Hata oluştu: {error_str}"}}'