import json
import requests
from colorama import Fore, Style, init
import os
import difflib

# Colorama başlat (canlı renkler)
init(autoreset=True)

# Biyoloji konu notları 'data/' klasöründe yer alıyor
data_dir = 'data/'

# Dosya isimlerine dayalı olarak olası konuları belirle
def get_available_subjects():
    return [f.replace(".txt", "") for f in os.listdir(data_dir) if f.endswith(".txt")]

# Konuyu en yakın eşleşme ile düzelt veya anlamadım mesajı ver
def correct_subject(subject):
    available_subjects = get_available_subjects()
    closest_matches = difflib.get_close_matches(subject, available_subjects, n=1, cutoff=0.6)
    if closest_matches:
        return closest_matches[0]
    else:
        return None

# Sistem mesajını assistant olarak ayarla ve dosyadan konu notlarını çek
def get_system_message(subject):
    corrected_subject = correct_subject(subject)
    if corrected_subject:
        with open(os.path.join(data_dir, f"{corrected_subject}.txt"), "r", encoding="utf-8") as file:
            subject_notes = file.read()
        return f"Sen bir biyoloji asistanısın ve sarmal model üzerine çalışıyorsun. İşte {corrected_subject} konusuyla ilgili bilgiler: {subject_notes}. Bu notları konu başlıkları ile önce bir giriş yap ardından sorulur ise ayrıntılı olarak anlat."
    else:
        return "Anlamadım. Lütfen geçerli bir konu başlığı giriniz."

def convert_to_special_format(system_message, user_message):
    output = "<|begin_of_text|>"
    output += f'<|start_header_id|>assistant<|end_header_id|>\n\n{system_message}<|eot_id|>'
    output += f'\n<|start_header_id|>user<|end_header_id|>\n\n{user_message}<|eot_id|>'
    output += "\n<|start_header_id|>assistant<|end_header_id|>"
    return output

url = "https://inference2.t3ai.org/v1/completions"

# Kullanıcıdan subject seçimini al
print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "Lütfen bir konu başlığı girin (örneğin, hücre bölünmeleri):")
subject = str(input(Fore.LIGHTGREEN_EX + "Konu: "))

# Seçilen konuya göre sistem mesajını ayarla
system_message = get_system_message(subject)

while True:
    # Sistem mesajını yazdır
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Sistem Mesajı:" + Style.RESET_ALL + Fore.LIGHTWHITE_EX, system_message)

    # Kullanıcıdan soru al
    print(Fore.LIGHTRED_EX + Style.BRIGHT + "Sorunuzu yazınız:")
    user_message = str(input(Fore.LIGHTGREEN_EX + "Soru: "))

    # Prompt'u özel formata dönüştür
    special_format_output = convert_to_special_format(system_message, user_message)

    # API'ye gönderilecek yükü hazırla
    payload = json.dumps({
        "model": "/home/ubuntu/hackathon_model_2/",
        "prompt": special_format_output,
        "temperature": 0.01,
        "top_p": 0.95,
        "max_tokens": 1024,
        "repetition_penalty": 1.1,
        "stop_token_ids": [128001, 128009],
        "skip_special_tokens": True
    })

    headers = {
        'Content-Type': 'application/json',
    }

    # API isteğini gönder
    response = requests.post(url, headers=headers, data=payload)
    pretty_response = json.loads(response.text)

    # Yanıtı yazdır
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "LLM Cevap:" + Style.RESET_ALL + Fore.LIGHTWHITE_EX, pretty_response['choices'][0]['text'])
