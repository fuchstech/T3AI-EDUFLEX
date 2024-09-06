from flask import Flask, jsonify, render_template, request  # Flask modüllerini içe aktarıyoruz
import json
import os
import requests  # Dış API çağrıları için requests modülünü kullanıyoruz
from datetime import datetime
from colorama import init

# Colorama başlat
init(autoreset=True)

# Flask uygulaması oluştur
app = Flask(__name__)

# Biyoloji konu notları 'data/' klasöründe yer alıyor
data_dir = 'data/'
feedback_file = 'feedback.json'  # Geri bildirimlerin kaydedileceği JSON dosyası

# Dosya isimlerine dayalı olarak olası konuları belirle
def get_available_subjects():
    return [f.replace(".txt", "") for f in os.listdir(data_dir) if f.endswith(".txt")]

# Sistem mesajını assistant olarak ayarla ve dosyadan konu notlarını çek
def get_system_message(subject):
    corrected_subject = subject
    if corrected_subject:
        with open(os.path.join(data_dir, f"{corrected_subject}.txt"), "r", encoding="utf-8") as file:
            subject_notes = file.read()
        return f"Sen Lise Düzeyinde bir biyoloji asistanısın ve sarmal model üzerine odaklanacaksın. Sarmal model, öğrenmenin sürekli bir süreç olarak görüldüğü, bilginin önce basit düzeyde, sonra karmaşıklaştırılarak öğretilmesini amaçlayan bir yaklaşımdır. Bu modelde, kullanıcıya ilk olarak temel bilgiler verilecek, daha sonra soruların zorluk seviyesi kademeli olarak artırılacaktır. Aşağıdaki konulara dair rehberlik edeceksin: {subject_notes}"
    else:
        return "Anlamadım. Lütfen geçerli bir konu başlığı giriniz."

# Prompt'u özel formata dönüştüren fonksiyon
def convert_to_special_format(system_message, user_message):
    output = "<|begin_of_text|>"
    output += f'<|start_header_id|>assistant<|end_header_id|>\n\n{system_message}<|eot_id|>'
    output += f'\n<|start_header_id|>user<|end_header_id|>\n\n{user_message}<|eot_id|>'
    output += "\n<|start_header_id|>assistant<|end_header_id|>"
    return output

# Ana sayfa route'u, form girişiyle konu ve sorunun alınması
@app.route('/')
def index():
    subjects = get_available_subjects()  # Mevcut dosya isimlerini dropdown için al
    return render_template('index.html', subjects=subjects)  # Template'e gönder

url = "https://inference2.t3ai.org/v1/completions"

@app.route('/get_response', methods=['POST'])
def get_response():
    subject = request.form.get('subject')
    user_message = request.form.get('question')
    
    # Sistem mesajını al
    system_message = get_system_message(subject)
    
    # Prompt'u özel formata dönüştür
    special_format_output = convert_to_special_format(system_message, user_message)

    # API'ye gönderilecek yükü requests ile hazırla
    payload = {
        "model": "/home/ubuntu/hackathon_model_2/",
        "prompt": special_format_output,
        "temperature": 0.01,
        "top_p": 0.95,
        "max_tokens": 1024,
        "repetition_penalty": 1.1,
        "stop_token_ids": [128001, 128009],
        "skip_special_tokens": True
    }

    headers = {
        'Content-Type': 'application/json',
    }

    # API isteğini gönder
    response = requests.post(url, headers=headers, json=payload)
    pretty_response = response.json()

    # Yanıtı döndür
    return jsonify({
        'response': pretty_response['choices'][0]['text'],
        'llm_response': pretty_response  # LLM yanıtı da döndürülüyor
    })

# Geri bildirimleri kaydetme fonksiyonu
def save_feedback(feedback):
    if not os.path.exists(feedback_file):
        with open(feedback_file, 'w', encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)  # Eğer dosya yoksa, boş bir JSON listesi oluştur

    with open(feedback_file, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data.append(feedback)  # Gelen geri bildirimi JSON listesine ekle
        f.seek(0)  # Dosyanın başına git ve güncel veriyi yaz
        json.dump(data, f, indent=4, ensure_ascii=False)

# Geri bildirim almak için yeni bir route
@app.route('/feedback', methods=['POST'])
def feedback():
    feedback_data = request.get_json()

    # Kullanıcı geri bildirimiyle ilgili özel JSON formatını hazırlıyoruz
    feedback_entry = {
        "interaction_id": feedback_data.get('interaction_id', '12345'),
        "user_id": feedback_data.get('user_id', 'user_001'),
        "timestamp": datetime.utcnow().isoformat() + "Z",  # ISO 8601 formatı
        "content_generated": {
            "input_prompt": feedback_data.get('input_prompt', ''),
            "response": feedback_data.get('response', '')
        },
        "user_feedback": {
            "rating": feedback_data.get('rating', 'dislike'),  # default dislike
            "feedback_text": feedback_data.get('feedback_text', ''),
            "preferred_response": feedback_data.get('preferred_response', '')
        },
        "feedback_metadata": {
            "device": feedback_data.get('device', 'unknown'),  # Cihaz bilgisi alınıyor
            "location": feedback_data.get('location', 'unknown'),  # Konum bilgisi alınıyor
            "session_duration": feedback_data.get('session_duration', 0)
        }
    }

    save_feedback(feedback_entry)  # Geri bildirimi JSON dosyasına kaydet
    return jsonify({"status": "success", "message": "Feedback saved!"})

# Flask uygulamasını başlat
if __name__ == '__main__':
    app.run(debug=True)
