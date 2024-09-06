import json
import requests
from colorama import Fore, Style, init

# Colorama başlat
init(autoreset=True)

# Biyoloji teması için sistem mesajı
biology_system_message = """
Sen yardımcı bir asistansın ve biyoloji konularında bilgi sağlayacaksın. İşte 11. sınıf biyoloji konuları:
1. Hücre Bölünmeleri: Mitoz ve mayoz bölünme arasındaki farklar, genetik çeşitlilik.
2. Kalıtım ve Genetik: Mendel Genetiği, çaprazlama problemleri, eşeye bağlı kalıtım.
3. Ekosistem Ekolojisi: Popülasyon dinamikleri, besin zinciri ve enerji akışı, madde döngüleri.
4. Bitki Biyolojisi ve Fizyolojisi: Bitkilerde taşınma, fotosentez, bitki hormonları.
5. Hayvan Fizyolojisi: Sinir, endokrin, sindirim, dolaşım, solunum ve boşaltım sistemleri.
6. İnsan Genetiği ve Genetik Hastalıklar: Mutasyonlar, genetik hastalıklar, biyoteknoloji.
7. Evrim ve Doğal Seçilim: Doğal seçilim, adaptasyon, türleşme.
Bu konulara dair soruları yanıtlayacaksın.
"""

# Fizik teması için sistem mesajı
physics_system_message = """
Sen yardımcı bir asistansın ve fizik konularında bilgi sağlayacaksın. İşte 11. sınıf fizik konuları:
1. Kuvvet ve Hareket: Newton'un hareket yasaları ve kuvvet ile hareket arasındaki ilişkiler.
2. İş, Güç ve Enerji: İş, güç ve enerji kavramları, enerji dönüşümleri.
3. Dönme Hareketi ve Açısal Momentum: Dönme hareketi, açısal hız, ivme ve momentum kavramları.
4. Basit Harmonik Hareket: Denge noktası etrafında tekrarlayan hareketler, yay ve sarkaç örnekleri.
5. Dalga Mekaniği: Dalga hareketi, dalga türleri, yansıma, kırınım, girişim.
6. Elektrostatik: Durağan elektrik yükleri, Coulomb yasası, elektrik alanı ve potansiyel.
7. Elektrik Akımı ve Devreler: Elektrik akımı, devre elemanları, Ohm yasası, seri ve paralel devreler.
8. Manyetizma: Manyetik alan, elektromıknatıslar, manyetik kuvvetler.
9. Alternatif Akım ve Elektromanyetik İndüksiyon: Alternatif akımın özellikleri, elektromanyetik indüksiyon prensipleri.
Bu konulara dair soruları yanıtlayacaksın.
"""

# Sistem mesajını temaya göre dinamik olarak ayarlayacak fonksiyon
def get_system_message(theme):
    if theme == "biyoloji":
        return biology_system_message
    elif theme == "fizik":
        return physics_system_message
    else:
        return "Sen yardımcı bir asistansın. Kullanıcıya genel bilgiler sağlayacaksın."

def convert_to_special_format(system_message, user_message):
    output = "<|begin_of_text|>"
    output += f'<|start_header_id|>system<|end_header_id|>\n\n{system_message}<|eot_id|>'
    output += f'\n<|start_header_id|>user<|end_header_id|>\n\n{user_message}<|eot_id|>'
    output += "\n<|start_header_id|>assistant<|end_header_id|>"
    return output

url = "https://inference2.t3ai.org/v1/completions"

# Kullanıcıdan tema seçimini al
print(Fore.CYAN + "Lütfen bir tema seçin (biyoloji veya fizik):")
theme = str(input(Fore.GREEN + "Tema: "))

# Seçilen temaya göre sistem mesajını ayarla
system_message = get_system_message(theme)

while True:
    # Kullanıcıdan soru al
    print(Fore.RED + "Sorunuzu yazınız:")
    user_message = str(input(Fore.GREEN + "Soru: "))

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
    print(Fore.YELLOW + "LLM Cevap:" + Fore.WHITE, pretty_response['choices'][0]['text'])
