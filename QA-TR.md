# DUBSEE v7 — Google teknik kontrolü

- 31 dilde 130 HTML dosyası: ana sayfalar, hukuki/destek arayüzleri ve İngilizce/Türkçe rehberler.
- 43 canonical URL içeren XML site haritası. Site haritasındaki her URL yereldeki canonical etiketiyle karşılaştırıldı.
- Tüm ana sayfalarda karşılıklı 31 dil + x-default hreflang doğrulandı. Dil menüsü canonical klasör URL’lerini kullanır.
- Hukuki sayfalarda yalnızca gerçek en/tr içerik sürümlerinin hreflang adresleri bulunur. İngilizce metni gösteren diğer arayüzlerin canonical ve og:url değerleri İngilizce aslına eşittir.
- Hukuki/destek meta açıklamaları kendi içeriğine özgüdür. Kaynak hukuki metinler değiştirilmedi.
- Zorunlu dil yönlendirmesi yoktur. Kayıtlı tercih veya tarayıcı dili yalnızca bir öneri bağlantısı gösterir. 31 dil adresi ve alt sayfalar doğrudan açılır. Kontrol: python scripts/check_language_routing.py.
- JSON-LD ayrıştırıldı; SSS verisi görünür metinle eşleşir. Fiyat, yorum ve puan uydurulmadı.
- İçerik normal durumda görünürdür; kaydırma gözlemcisi hiç tetiklenmese de metin görünmez kalmaz. Güçlü animasyonların son görsel düzeni korunur.
- Önizlemenin dil/alt sayfa yönlendiricisi ve kaydırma sayaç regresyon testleri geçti.
- Opsiyonel gerçek Search Console doğrulama kodu için config alanı mevcut.

## Yapılmayanlar

GitHub yayını, Search Console hesabı/mülk doğrulaması, Google indeks talebi, canlı Rich Results testi, PageSpeed/Lighthouse ölçümü ve gerçek mobil tarayıcı render testi yapılmadı. Bu paket teknik SEO hazırlığıdır; Google onayı veya sıralama garantisi değildir.
