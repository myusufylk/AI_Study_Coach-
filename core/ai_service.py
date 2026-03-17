from google import genai
from django.conf import settings


def generate_study_program(target_exam, daily_hours):
    """
    Generates a weekly study program for a student using the Gemini AI API.

    Args:
        target_exam (str): The exam the student is preparing for.
        daily_hours (int/float): The number of hours the student can study per day.

    Returns:
        str: The AI-generated weekly study plan, or a user-friendly error message.
    """
    try:
        client = genai.Client(api_key=settings.GOOGLE_API_KEY)

        prompt = f"""
        Bir öğrenci için haftalık çalışma programı oluştur.

        Hedef sınav: {target_exam}
        Günlük çalışma süresi: {daily_hours} saat

        Pazartesi - Pazar şeklinde plan yaz.
        """

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return getattr(response, "text", "AI cevap üretemedi.")

    except Exception as e:
        error_str = str(e)

        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            return (
                "⚠️ API kota limitiniz doldu. Lütfen şunları yapın:\n"
                "1. https://aistudio.google.com/app/apikey adresinden yeni bir API anahtarı oluşturun.\n"
                "2. settings.py dosyasındaki GOOGLE_API_KEY değerini güncelleyin.\n"
                "3. Veya Google Cloud'da billing aktifleştirin: https://console.cloud.google.com/billing"
            )
        elif "401" in error_str or "API_KEY_INVALID" in error_str or "invalid" in error_str.lower():
            return (
                "⚠️ API anahtarı geçersiz. Lütfen settings.py dosyasındaki "
                "GOOGLE_API_KEY değerini kontrol edin."
            )
        elif "404" in error_str or "not found" in error_str.lower():
            return "⚠️ Model bulunamadı. Lütfen yöneticinizle iletişime geçin."
        else:
            return f"⚠️ Çalışma programı oluşturulurken bir hata oluştu: {error_str}"