import json
import requests

def convert_to_special_format(system_message, user_message):
    output = "<|begin_of_text|>"
    output += f'<|start_header_id|>system<|end_header_id|>\n\n{system_message}<|eot_id|>'
    output += f'\n<|start_header_id|>user<|end_header_id|>\n\n{user_message}<|eot_id|>'
    output += "\n<|start_header_id|>assistant<|end_header_id|>"
    return output

url = "https://inference2.t3ai.org/v1/completions"

# Sabit sistem mesajı
system_message = """Sen yardımcı bir asistansın ve sana verilen talimatlar doğrultusunda en iyi cevabı üretmeye çalışacaksın. Türkçe cevap vereceksin. Türkiye'nin ilk büyük Türkçe dil modeli olarak, T3AI'LE projesi kapsamında Baykar Teknoloji ve T3 Vakfı tarafından geliştirilmiş bir yapay zeka asistanıyım. Kullanıcıların sorularına Türkçe olarak doğru ve etkili yanıtlar vermek için tasarlandım.

### 1. **Hücre Bölünmeleri**
Hücre bölünmeleri konusu, mitoz ve mayoz olmak üzere iki ana bölünme türünü içerir. Mitoz bölünme, vücut hücrelerinde gerçekleşir ve canlının büyümesini, gelişmesini ve hasar görmüş dokuların onarılmasını sağlar. Tek hücreli canlılarda mitoz, üremeyi gerçekleştirir. Mitoz bölünme sonucunda oluşan hücreler, ana hücre ile aynı genetik yapıya sahip olur ve kromozom sayısı sabit kalır. Mayoz bölünme ise üreme hücrelerinde (gametlerde) meydana gelir ve kromozom sayısının yarıya inmesini sağlar. Bu süreç, genetik çeşitliliği artıran çaprazlama ve bağımsız dağılım gibi mekanizmalar içerir. Mayoz sonucunda dört yeni hücre oluşur ve her biri genetik olarak farklıdır. Mitoz ve mayoz arasındaki temel farklar, hücre sayısı, kromozom sayısı ve genetik yapıda ortaya çıkar.

### 2. **Kalıtım ve Genetik**
Genetik bilimi, canlıların genetik materyallerinin bir sonraki nesillere nasıl aktarıldığını inceler. Mendel Genetiği bu alandaki temel kuralları koyar. Gregor Mendel, bezelye bitkileriyle yaptığı deneylerde baskın (dominant) ve çekinik (resesif) genlerin nasıl nesilden nesile geçtiğini göstermiştir. Monohibrit çaprazlama, tek bir özellik üzerinden yapılan çaprazlamayı incelerken, dihibrit çaprazlama iki özellik üzerinden yapılan çaprazlamaları kapsar. Kan grupları gibi çok alelli özellikler de kalıtımın farklı bir yönüdür. ABO kan grubu sistemi, hem baskın hem de çekinik genlerin nasıl birlikte çalıştığını gösterir. Eşeye bağlı kalıtımda ise, X ve Y kromozomları aracılığıyla aktarılan özellikler bulunur. Renk körlüğü ve hemofili gibi hastalıklar, X kromozomu üzerinde taşınan genlerle alakalıdır.

### 3. **Ekosistem Ekolojisi**
Ekosistem ekolojisi, canlıların yaşadığı ortamlarla etkileşimlerini ve popülasyonların dinamiklerini inceler. Popülasyon ekolojisi, bir bölgede yaşayan aynı türe ait bireylerin büyüklüğünü, dağılımını ve bu popülasyonların taşıma kapasitesini analiz eder. Ayrıca, besin zinciri ve enerji akışı konusu ekosistemlerde üreticilerden (bitkiler), tüketicilere (hayvanlar) ve ayrıştırıcılara kadar enerji ve maddelerin nasıl aktarıldığını açıklar. Enerji akışı, ekosistemlerin işleyişinin temelidir. Bunun yanında, karbon, su, azot ve fosfor döngüsü gibi maddelerin ekosistem içindeki hareketi ve insan faaliyetlerinin bu döngülere etkisi önemli konular arasındadır.

### 4. **Bitki Biyolojisi ve Fizyolojisi**
Bitkilerde taşınma, su ve minerallerin köklerden yapraklara taşınmasını sağlayan ksilem ve floem dokularıyla gerçekleşir. Ksilem suyu taşırken, floem organik maddeleri bitkinin her yerine taşır. Bitkilerde suyun buharlaşarak yapraklardan dışarı atılması transpirasyon olarak adlandırılır ve bu süreç bitkilerin su kaybını kontrol eder. Bitkilerde fotosentez ise, kloroplastlarda güneş enerjisinin kimyasal enerjiye dönüştürülmesi sürecidir. Bu süreç iki aşamada gerçekleşir: ışık reaksiyonları ve Calvin döngüsü. Bitki büyümesini kontrol eden hormonlar arasında auksin, giberellin, sitokinin, absisik asit ve etilen yer alır. Bu hormonlar, bitkilerin büyümesini, gelişmesini ve çevresel uyarıcılara karşı tepkilerini düzenler.

### 5. **Hayvan Fizyolojisi**
Hayvan fizyolojisi, canlıların yaşamsal faaliyetlerini yöneten sistemleri inceler. Sinir sistemi, nöronlar aracılığıyla sinyallerin iletilmesini sağlar ve merkezi sinir sistemi (beyin ve omurilik) ile periferik sinir sistemi olarak ikiye ayrılır. Endokrin sistem ise hormonları salgılayarak vücut içindeki birçok sürecin düzenlenmesini sağlar. Hipofiz, tiroid ve adrenal bezler gibi organlar hormon üretir. Sindirim sistemi, besinlerin sindirilmesi ve emilmesi sürecini içerir. Ağızdan başlayarak anüse kadar olan süreçte mide, bağırsaklar ve çeşitli enzimler rol alır. Dolaşım sistemi, kalp ve kan damarları aracılığıyla vücuttaki oksijen ve besin maddelerinin taşınmasını sağlar. Solunum sistemi ise oksijenin alınması ve karbondioksitin vücuttan atılması görevini üstlenir. Boşaltım sistemi, böbrekler aracılığıyla vücuttaki atık maddeleri uzaklaştırarak iç dengeyi korur.

### 6. **İnsan Genetiği ve Genetik Hastalıklar**
İnsan genetiği, insanlarda genetik materyalin nasıl aktarıldığını ve mutasyonların nasıl gerçekleştiğini inceler. Genetik materyalde meydana gelen kalıcı değişiklikler mutasyon olarak adlandırılır ve bu değişiklikler genetik hastalıklara yol açabilir. Örneğin, Down sendromu, Turner sendromu ve orak hücre anemisi gibi hastalıklar, genetik mutasyonların sonucu olarak ortaya çıkar. Genetik mühendisliği ve biyoteknoloji, günümüzde hızla gelişen alanlardır ve gen terapisi, gen klonlama ve DNA parmak izi gibi teknolojilerle insan genetiğine müdahale edilebilmektedir. Bu alanda yapılan çalışmalar, hastalıkların tedavi edilmesi ve genetik bozuklukların düzeltilmesi için umut verici çözümler sunmaktadır.

### 7. **Evrim ve Doğal Seçilim**
Evrim konusu, canlıların zaman içinde değişimini ve bu değişimlerin nedenlerini inceler. Charles Darwin'in doğal seçilim teorisi, ortama en iyi uyum sağlayan bireylerin hayatta kalıp üreme şanslarının arttığını ve bu bireylerin özelliklerinin sonraki nesillere aktarıldığını savunur. Evrimsel süreçlerde, canlıların çevreye uyum sağlaması için geçirdiği yapısal, işlevsel ve davranışsal değişiklikler adaptasyon olarak adlandırılır. Türleşme, coğrafi izolasyon ve adaptif radyasyon gibi mekanizmalar da evrimsel sürecin bir parçasıdır. Bu mekanizmalar, yeni türlerin oluşmasına ve biyolojik çeşitliliğin artmasına yol açar."""

while True:
    # Kullanıcıdan soru al
    user_message = str(input("Sorunuzu yazınız: "))

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
    print(pretty_response)
    # Yanıtı yazdır
    print("LLM Cevap:", pretty_response['choices'][0]['text'])
