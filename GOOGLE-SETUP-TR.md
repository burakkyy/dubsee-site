# Google yayına alma notları

## Hazır olanlar

31 dilde statik HTML ana sayfa, canonical/hreflang, 37 canonical URL içeren sitemap.xml, mobil düzen, responsive görseller, yapılandırılmış veri ve doğrudan dil adreslerini koruyan yönlendirme davranışı hazırdır. Bu, indeks veya sıralama garantisi değildir.

Kaynaklar: Google Search Central çok dilli site rehberi ve canonical rehberi.
https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites
https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls

## 1. GitHub Pages'e yayınla

Mevcut web sitesi tasarımı ve dosya yapısını yayınla. index.html ve assets ile bütün dil klasörleri birlikte aktarılmalı. Tek dosyalık DubSee-Preview.html inceleme içindir; ana site olarak yayınlama. Canlı GitHub reposuna bu çalışma sırasında push yapılmadı.

Alan adı veya /dubsee-site/ yolu değişirse config.json/base_url değerini güncelle, python3 scripts/build.py ve python3 scripts/check.py komutlarını çalıştır.

## 2. Search Console doğrulaması

Google Search Console'a kullanıcı hesabınla gir. https://burakkyy.github.io/dubsee-site/ URL öneki mülkünü ekle. HTML etiketi yönteminin verdiği gerçek google-site-verification content değerini config.json/google_site_verification alanına yaz. Sonra sayfaları yeniden oluştur ve yayınla. Ardından Search Console'da doğrula. Kod uydurulmadı; mülk doğrulaması henüz yapılmadı.

Alternatif doğrulama yöntemleri kullanılabilir; doğrulama dosyası yöntemi seçilirse Google'ın verdiği dosya yayın köküne eklenir.

## 3. Site haritası

Doğrulanan mülke şu tam adresi gönder:
https://burakkyy.github.io/dubsee-site/sitemap.xml

Site haritasında 31 dilde ana sayfa ve asıl İngilizce/Türkçe hukuki/destek sayfaları vardır. İngilizce metnin yerelleştirilmiş arayüzlerde tekrarlandığı diğer alt sayfalar sitemap'e dahil edilmedi. Erişimleri kapatılmadı; canonical İngilizce aslına bağlandı.

## 4. robots.txt ve GitHub proje yolu

Google robots.txt dosyasını alan adı kökünden okur:
https://burakkyy.github.io/robots.txt

/dubsee-site/robots.txt kök robots.txt yerine geçmez. Alan adı kökündeki ayrı GitHub Pages deposunu yönetiyorsan mevcut robots kurallarını koruyarak sitemap satırını oraya ekle. deployment/robots-domain-root.txt örnek içeriği gösterir. Mevcut kök robots.txt dosyasını incelemeden üzerine yazma. Kök robots.txt yoksa varsayılan olarak tarama engellenmiş sayılmaz; sitemap Search Console'a doğrudan gönderilebilir.

Özel alan adı ve site alan adı kökünde yayınlanırsa proje robots.txt dosyası kökte doğru konuma gelir; base_url yeni adrese göre üretilmelidir.

## 5. Yayın sonrası doğrulama

Search Console URL Denetimi ile ana sayfa, /tr/, /de/, /ja/ adreslerini ayrı ayrı denetle. Her birinin kendi dilinde kaldığını ve Google'ın canonical adreslerini nasıl seçtiğini gör. Canlı URL testinden sonra gerekiyorsa indeks iste.

Rich Results Test ile yapılandırılmış veriyi; PageSpeed Insights ile gerçek mobil performansı ölç. JSON-LD yerel olarak ayrıştırıldı ancak Google'ın canlı Rich Results testi henüz çalıştırılmadı. SoftwareApplication verisi temel ürün kimliğini açıklar; özel uygulama sonucu için gereken gerçek fiyat/değerlendirme bilgileri yoksa uygunluk uyarısı alınabilir. Sahte fiyat, puan veya yorum ekleme. FAQ işaretlemesi uygulama sitesi için zengin sonuç gösterimi garantisi değildir.

App Store bağlantısı henüz boş. Gerçek bağlantı geldiğinde app_store_url değerini ekle ve yeniden oluştur.

## Yapılan testler

python3 scripts/check.py
node scripts/check_language_routing.cjs

Bu testler canlı sunucunun HTTP cevaplarını, robots durumunu, Google indeksini veya gerçek cihaz performansını ölçmez. Site henüz bu çalışma kapsamında yayınlanmadı.
