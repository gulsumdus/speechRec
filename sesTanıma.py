import speech_recognition as sr
from gtts import gTTS
import os
import json
from rapidfuzz import process
import playsound

file_path= "sorular.json"
# Metin dosyasını oku (JSON formatı)
def load_qa_data(file_path):
    if not os.path.exists(file_path):
        print("Soru-cevap veritabanı bulunamadı.")
        return {}

    with open(file_path, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print("Dosya bozuk veya yanlış formatta.")
            return {}


# Kullanıcının sesli sorusunu al (STT)
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Bir şeyler söyleyin...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="tr-TR")
        print(f"Tanınan metin: {text}")
        return text
    except sr.UnknownValueError:
        print("Ses anlaşılamadı. Lütfen tekrar deneyin.")
        return None
    except sr.RequestError:
        print("STT servisine erişilemedi. İnternet bağlantınızı kontrol edin.")
        return None


# En uygun cevabı bul
def find_best_answer(question, qa_dict):
    if not qa_dict:
        return "Üzgünüm, şu anda veritabanım boş."

    questions = list(qa_dict.keys())
    best_match, score, _ = process.extractOne(question, questions)
    if score > 80:
        return qa_dict[best_match]
    return "Üzgünüm, bu soruya uygun bir cevabım yok."


# Yanıtı sesli oku (TTS - Google TTS kullanımı)
def speak_text(text):
    tts = gTTS(text=text, lang="tr")
    file_path = "response.mp3"
    tts.save(file_path)
    playsound.playsound(file_path)
    os.remove(file_path)  # Geçici dosyayı sil


# Ana program
if __name__ == "__main__":
    qa_data = load_qa_data("sorular.json")  # JSON formatı

    while True:
        print("\nSorunuzu sesli söyleyin veya çıkış için 'çıkış' deyin.")
        question = recognize_speech()

        if question:
            if question.lower() in ["çıkış", "kapat", "bitir"]:
                print("Programdan çıkılıyor...")
                speak_text("Görüşmek üzere!")
                break

            answer = find_best_answer(question, qa_data)
            print(f"Cevap: {answer}")
            speak_text(answer)
