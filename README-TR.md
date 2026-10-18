# DUBSEE — mobil web sitesi, v7

Mobil öncelikli, açık temalı, GitHub Pages üzerinde sunulabilecek statik web sitesi. Ana mesaj: **YouTube videolarını 30+ dilde anlık dublajla izle.**

## Bu sürümde

- Sayfa dilleri Supertonic 3 resmî desteğindeki 31 dille eşleştirildi; tanıtım metinlerinde 30+ kullanıldı.
- Tüm görünen metinlerde marka DUBSEE olarak yazıldı.
- Yakında mesajları kaldırıldı; App Store simgeli bağlantı alanları hazır.
- Mobil başlık küçültüldü, ortalandı, mavi/kırmızı görsel vurgular eklendi. DUBSEE adı ve simgesi üst çubukta sabittir.
- Mobilde öğrenci/marangoz bölümünün iki kartı ve özelliklerin üç kartı yatay kaydırılır. Masaüstünde kartlar aynı sayfada görünür.
- YouTube logolarının tamamı kaldırıldı; YouTube metinleri ve ana ürün mesajı korundu.
- Ana İngilizce giriş adresinde telefon/tarayıcı dili seçilir. Doğrudan /tr/, /de/ gibi dil sayfaları ve hukuki/destek adresleri kendi içeriğinde kalır. Elle yapılan tercih ana girişte hatırlanır. Desteklenmeyen dillerde İngilizce kullanılır.
- Önizlemede ortak görseller ve tüm dillerin metinleri bulunur. Üst menü native HTML yapısındadır; dil/alt sayfa geçişleri JavaScript ile yapılır.
- Özellik etiketleri mobilde tek satırda yana kaydırılır.
- DUBSEE altına seçilen dile çevrilen Real-Time Video Dubbing açıklaması eklendi.
- Başlığın iki parçası arasındaki nokta kaldırıldı.
- Gizlilik, kullanım şartları ve destek için her dil dizininde ayrı HTML sayfaları oluşturuldu. Kaynak sitenin Türkçe ve İngilizce metinleri korundu; diğer 29 dilde başlık/navigasyon yerelleştirilirken hukuki içerik İngilizce gösterilir. Hukuki metinlerin diğer dillere çevrildiği iddia edilmez.

## İnceleme dosyası

Ayrı sunulan DubSee-Preview.html yaklaşık 3,7 MB boyutundadır. 31 dildeki metinler ve üç alt sayfa dosyanın içindedir; görseller ortak kopyalardan kullanılır. İlk açılış görselleri ayrıca JavaScript gerektirmeden gömülüdür.

Normal Safari/Chrome’da telefon/tarayıcı dili otomatik seçilir; elle yapılan seçim saklanır. Dil ve alt sayfa geçişleri hafif JavaScript yönlendiricisiyle çalışır. WhatsApp/iOS dosya önizlemesi JavaScript’i kapatırsa bu geçişler ve otomatik dil algılama çalışmayabilir. Bu, yayındaki normal web sitesinin dil desteğini değiştirmez. Önizlemenin tam kullanımı için Safari/Chrome’da açın.

Mobil üst çubukta uygulama simgesi 38 px, DUBSEE yazısı 23 px, alt açıklama 10 px olarak büyütüldü. Apple kısayolu tekrar görünürdür; App Store URL’si eklenene kadar indirme bölümüne gider.

Bu tek dosyalık önizleme incelemek içindir; üretimde bu klasördeki index.html ve assets kullanılır.

## Yayın

Bu paket henüz GitHub’a yüklenmedi. Ana index.html, dil klasörleri, assets/, privacy.html, terms.html, support.html, sitemap.xml, robots.txt ve .nojekyll dosyalarını mevcut dubsee-site deposunun yayınlanan kök dizinine aktarın. CNAME, .github ve ilgisiz dosyaları koruyun.

Önceki 44 dilli sürüm aktarılmışsa artık desteklenmeyen şu eski dil klasörlerini kaldırın: no, is, be, sr, bs, cnr, mk, sq, ca, ga, mt, lb, rm, hy, ka, az, la. Pakette yalnızca yeni 31 dil bulunur.

## App Store URL’si

config.json içindeki app_store_url boş. Şimdilik simgeli bağlantılar sayfanın indirme bölümüne gider; uydurma mağaza adresi yoktur. Gerçek https://apps.apple.com/... adresini ekledikten sonra:

```bash
python3 scripts/build.py
python3 scripts/check.py
```

Tüm dil sayfaları ve üst çubuktaki App Store bağlantısı güncellenir. base_url değişirse aynı komutları çalıştırın. Hukuki sayfaların canonical adreslerini de yeni alan adına uyarlayın. Üretim için sunucu/Python/Node gerekmez; Python yalnızca hazır sayfaları tekrar üretmek içindir.

## Diller

İngilizce, Türkçe, Almanca, Fransızca, İspanyolca, İtalyanca, Portekizce, Felemenkçe, Lehçe, İsveççe, Danca, Fince, Yunanca, Çekçe, Slovakça, Slovence, Hırvatça, Macarca, Romence, Bulgarca, Estonca, Letonca, Litvanca, Rusça, Ukraynaca, Arapça, Japonca, Korece, Hintçe, Endonezce ve Vietnamca.

Kaynak: https://github.com/supertone-oss-archive/supertonic#-supported-languages-31 — 17 Ekim 2026 tarihinde kontrol edildi. Özellikle yeni çevirilere reklam trafiği göndermeden önce editoryal kontrol yapın. Uygulama ekran görüntülerinin özgün İngilizce metinleri korunur.

## Dosyalar

- assets/site.css: ana tasarım; assets/mobile-refinement.css: ikinci sürüm mobil düzenlemeleri.
- assets/site.js: menü, manuel dil tercihi ve galeri/kart kontrolleri.
- scripts/locales.py: yalnızca desteklenen dillerde metinler.
- scripts/extras.py: özellik etiketleri.
- scripts/build.py: sayfa ve SEO üretimi.
- scripts/make_preview.py: gömülü görselli, ortak görselleri kullanan hafif inceleme dosyası üretimi (Pillow gerekir).
- scripts/taglines.py: 31 dilde marka alt açıklaması.
- scripts/legal_pages.py ve content/*.source: kaynak metinlerden alt sayfa üretimi.
- scripts/check.py: dosya/SEO kontrolleri.
- QA-TR.md: yapılan kontroller ve sınırları.

## SEO

Her dilde statik HTML içerik, canonical/hreflang, sosyal paylaşım meta verileri, Organization/WebSite/WebPage/SoftwareApplication/FAQPage yapılandırılmış verileri ve XML site haritası bulunur. Destek koşulları açık yazılmıştır; doğrulanmamış %95 başarı iddiası yoktur.

Yayın sonrası Google Search Console ve Bing Webmaster Tools’a https://burakkyy.github.io/dubsee-site/sitemap.xml adresini gönderin. robots.txt alan adı kökünden okunur; /dubsee-site/robots.txt tek başına alan adı kökü için kural koymaz. Üst düzey /robots.txt taramayı engellememelidir. SEO/GEO altyapısı indekslenme veya yapay zekâ aramalarında önerilme garantisi vermez. Harici takip/analiz kodu eklenmedi.

## Cursor talimatı

> Bu DUBSEE v7 tasarımını mevcut GitHub Pages depoma aktar. README-TR.md dosyasını oku. 31 dil sayfası, assets, hukuki sayfalar ve site haritasını kullan. Önceki sürümden kalan ve README’de listelenen 17 dil klasörünü kaldır. Mevcut CNAME, .github ve ilgisiz dosyaları koru. App Store URL’si boş; sahte link ekleme. Mobil düzeni ve marka yazımını koru. Yerel kontrolleri yap, değişiklik özetini göster ve mevcut GitHub çalışma akışıma uygun şekilde push et.

## v5 — görsel kalite ve hareket

Öğrenci ve marangoz görselleri üretimde 800/1600 px WebP seçenekleriyle sunulur. Önizlemede bu iki görsel 1200 px JPEG olarak bulunur; diğer görsellerin boyutu değiştirilmedi. Canlı sayfada bu bölüm loading=lazy ve decoding=async ile yüklenir. Görsellerin kalite artışı sıfır ek veri anlamına gelmez; bölümün yüklenmesi ana içerikten ayrılmıştır.

Yatay kartların göstergesi görünür alandaki karta göre hesaplanır. Noktalara ek olarak 1 / 2 ve 1 / 3 sayacı vardır; scroll, touchend, scrollend, IntersectionObserver ve boyut değişiminden güncellenir. Arapça yönü de desteklenir.

Kısa ilk açılış, bölüm belirmesi ve düğme basma geçişleri eklendi. Animasyonlar sürekli dönmez; yalnızca opacity/transform kullanılır. prefers-reduced-motion tercihinde belirme animasyonları kapatılır. Dil değiştirildiğinde önceki gözlemciler ve olay dinleyicileri kaldırılır. WhatsApp dosya önizlemesi JavaScript’i kapatırsa sayaç ve giriş animasyonları çalışmayabilir; gerçek mobil web davranışı için Safari/Chrome kullanın.

## v6 — daha belirgin animasyonlar

Başlık, vurgu, açıklama ve butonlar kısa aralıklarla sıralı açılır. Telefon görseli dönüş ve yakınlaşmayla, yanındaki küçük kartlar iki yandan gelir. Ses çubuklarında bir defalık açılış vurgusu vardır. Bölümler 34 px yükselme ve küçük ölçek geçişiyle açılır; yan yana kartlar hafif gecikmeyle sıralanır. Kaydırma sırasında yeni kartın görseli ve sayacı kısa vurgu alır.

Sürekli animasyon döngüsü, harici kütüphane, yeni görsel veya video eklenmedi. Geçişler opacity/transform ağırlıklıdır. Hareketi Azalt tercihi korunur; dil değişiminde gözlemciler, dinleyiciler ve aktif kart efektleri temizlenir. Tasarım ve içerik yerleşimi korunmuştur. Gerçek cihazda FPS testi yapılmadı.

## v7 — Google için teknik düzeltmeler

- Otomatik dil yönlendirmesi yalnızca ana giriş /dubsee-site/ ve /dubsee-site/index.html adreslerinde uygulanır. Doğrudan dil ve alt sayfa adreslerinde devre dışıdır.
- Dil menüsünün ana sayfa bağlantıları canonical klasör adreslerini kullanır. 31 dilin karşılıklı hreflang bağlantıları korunur.
- Site haritasında 37 canonical adres bulunur: 31 ana sayfa + gerçekten İngilizce/Türkçe içeriği bulunan 6 hukuki/destek sayfası.
- Diğer 29 dilin İngilizce içerik gösteren hukuki arayüzleri erişilebilir kalır; canonical ve Open Graph URL İngilizce aslına gider. Bu sayfalarda yalnızca gerçek en/tr çeviri sürümleri hreflang ile belirtilir.
- Her dilde arama başlığı anlık video dublajı, YouTube ve iPhone bağlamıyla düzenlendi. Hukuki/destek sayfalarının meta açıklamaları kendi içeriklerini açıklar.
- Uygulamanın yapılandırılmış verisinde gerçek özellik açıklamaları ve yayıncı ilişkisi kullanılır. Sahte fiyat, yorum veya puan yoktur.
- İçerik, kaydırma animasyonunun tetiklenmesine bağlı olarak görünmez bırakılmaz. Mevcut güçlü animasyonlar ekrana girince oynatılır.
- Tek dosyalık inceleme önizlemesine noindex eklendi; Google'a sunulacak asıl site klasörlü statik HTML sürümüdür.
- config.json içinde isteğe bağlı google_site_verification alanı vardır. Gerçek Search Console doğrulama kodu eklendikten sonra build.py çalıştırılmalıdır. Boşken meta etiket üretilmez.

Yayın adımları ve alan adı kökündeki robots.txt ayrıntısı GOOGLE-SETUP-TR.md dosyasındadır. Yeni yönlendirme testi: node scripts/check_language_routing.cjs.
