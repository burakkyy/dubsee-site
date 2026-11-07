"""English and Turkish guides. Other languages are not machine-copied."""
import json
from html import escape
from pathlib import Path
from taglines import TAGLINES

PAIRS = [
    {
        'key': 'translator',
        'en': {
            'slug': 'youtube-video-translator',
            'title': 'YouTube Video Translator for iPhone | DUBSEE',
            'description': 'DUBSEE translates the speech in supported YouTube videos and plays it with AI dubbing on iPhone. Shorts and live streams are not included.',
            'h1': 'YouTube video translator for iPhone',
            'other': 'Bu sayfayı Türkçe oku',
        },
        'tr': {
            'slug': 'youtube-videolarini-turkce-dinleme',
            'title': 'YouTube Videolarını Türkçe Dinleme | DUBSEE',
            'description': 'DUBSEE, desteklenen YouTube videolarının konuşmasını Türkçe ve diğer dillere çevirip iPhone’da yapay zekâ sesiyle dinletir. Shorts ve canlı yayın yok.',
            'h1': 'YouTube videolarını Türkçe dinleme',
            'other': 'Read this page in English',
        },
    },
    {
        'key': 'howto',
        'en': {
            'slug': 'how-to-translate-youtube-videos-on-iphone',
            'title': 'How to Translate YouTube Videos on iPhone | DUBSEE',
            'description': 'Copy a supported YouTube link, paste it into DUBSEE, choose a language, and listen on your iPhone. What to try if the dubbing does not start.',
            'h1': 'How to translate YouTube videos on iPhone',
            'other': 'Bu sayfayı Türkçe oku',
        },
        'tr': {
            'slug': 'iphone-youtube-video-cevirisi',
            'title': 'iPhone’da YouTube Video Çevirisi | DUBSEE',
            'description': 'Desteklenen bir YouTube bağlantısını DUBSEE’ye yapıştırın, dili seçin ve iPhone’da dinleyin. Dublaj başlamazsa bakılacak yerler burada.',
            'h1': 'iPhone’da YouTube video çevirisi',
            'other': 'Read this page in English',
        },
    },
    {
        'key': 'dubbing',
        'en': {
            'slug': 'ai-video-dubbing',
            'title': 'AI Video Dubbing for YouTube on iPhone | DUBSEE',
            'description': 'How DUBSEE turns supported YouTube speech into an AI voice, what DubSee Pro adds, and what the dubbing does not do.',
            'h1': 'AI video dubbing for YouTube',
            'other': 'Bu sayfayı Türkçe oku',
        },
        'tr': {
            'slug': 'yapay-zeka-video-dublaji',
            'title': 'Yapay Zekâ ile Video Dublajı | DUBSEE',
            'description': 'DUBSEE, desteklenen YouTube konuşmasını yapay zekâ sesine nasıl çevirir? DubSee Pro ne ekler, dublaj ne vaat etmez?',
            'h1': 'Yapay zekâ ile video dublajı',
            'other': 'Read this page in English',
        },
    },
]

HOME_GUIDES = {
    'en': {
        'heading': 'Guides',
        'intro': 'Practical notes on translating supported YouTube videos and listening with AI dubbing.',
        'items': [
            ('youtube-video-translator/', 'YouTube video translator', 'What DUBSEE translates, which videos work, and which do not.'),
            ('how-to-translate-youtube-videos-on-iphone/', 'Translate YouTube on iPhone', 'The steps from a copied link to playback, plus what to try if dubbing does not start.'),
            ('ai-video-dubbing/', 'AI video dubbing', 'How the translated voice works, and what DubSee Pro changes.'),
        ],
    },
    'tr': {
        'heading': 'Rehberler',
        'intro': 'Desteklenen YouTube videolarını çevirip yapay zekâ dublajıyla dinlemek için ayrıntılar.',
        'items': [
            ('youtube-videolarini-turkce-dinleme/', 'YouTube videolarını Türkçe dinleme', 'Hangi videolar çevrilir, hangileri çevrilmez.'),
            ('iphone-youtube-video-cevirisi/', 'iPhone’da YouTube çevirisi', 'Bağlantıyı yapıştırmaktan dinlemeye kadar adımlar ve dublaj gelmezse ne yapılır.'),
            ('yapay-zeka-video-dublaji/', 'Yapay zekâ video dublajı', 'Çevrilmiş ses nasıl çalışır ve DubSee Pro ne ekler.'),
        ],
    },
}

BODIES = {
 'translator': {
  'en': '''
<p>DUBSEE is an iPhone app for people who have a YouTube link and want to follow the spoken part in another language. It is not a replacement YouTube player, a news app, or a remote for a television. You bring a link. DUBSEE translates the speech in that video and plays an AI voice while the video runs.</p>
<h2>What “supported” means</h2>
<p>Support is narrower than “any YouTube URL”. DUBSEE is built for regular YouTube videos that have captions available. Shorts are not supported. Live streams are not supported. A video can still fail when the captions, language, or region do not line up. If one link does not dub, another video is the right next test, not a second tap on the same link.</p>
<p>The App Store description calls the playback real-time dubbing and says the dubbed audio is meant to follow the video. That describes the product’s aim. It is not a promise that every sentence lands perfectly, and it is not an offline mode. DUBSEE needs the video you asked it to open.</p>
<h2>Languages you can listen in</h2>
<p>The dubbing languages are the same 31 languages published for the app and listed in the menu on this site: @@LANGS@@. Choosing Turkish on an English lecture, or English on a Turkish lecture, is the same action: paste the link, pick the language you want to hear, and play. The website’s language menu is the list of those dubbing languages. It does not mean every video exists in every language.</p>
<h2>Who it is for</h2>
<p>The useful cases are lectures, course videos, software tutorials, craft and repair explainers, podcasts posted on YouTube, and other videos where the information is in the speech. Students can stay with the diagram instead of pausing to read. Someone following a tutorial can keep their hands on the work. It is a poor fit if you want clips, live chat, or a general movie library.</p>
<h2>Free use and DubSee Pro</h2>
<p>The app is free to download. Free use includes 1 video a day, plus up to 2 more after rewarded ads, with about an 18-minute limit per free video. DubSee Pro unlocks unlimited videos, removes that duration limit and the ads, adds 10 voices, and enables background and lock-screen playback. A free trial appears only when the App Store says you are eligible. The price is shown in the app before purchase and can vary by region. DUBSEE is independent and is not affiliated with, endorsed by, or sponsored by YouTube or Google.</p>
<p>Related: <a href="@@HOWTO@@">how to translate a YouTube video on iPhone</a> and <a href="@@DUB@@">how the AI dubbing works</a>. Help is on the <a href="@@SUPPORT@@">support page</a>.</p>
''',
  'tr': '''
<p>DUBSEE, elinde bir YouTube bağlantısı olan ve videodaki konuşmayı başka bir dilde takip etmek isteyenler için bir iPhone uygulamasıdır. YouTube’un yerine geçen bir oynatıcı, haber uygulaması veya televizyon kumandası değildir. Bağlantıyı siz getirirsiniz. DUBSEE o videodaki konuşmayı çevirir ve video oynarken yapay zekâ sesiyle okur.</p>
<h2>Desteklenen video ne demek</h2>
<p>Destek, “her YouTube adresi” demek değildir. DUBSEE, altyazısı bulunan normal YouTube videoları içindir. Shorts desteklenmez. Canlı yayınlar desteklenmez. Altyazı, dil veya bölge uymadığında normal bir video da açılmayabilir. Bir bağlantı dublaj vermezse aynı bağlantıya tekrar basmak yerine başka bir video denemek gerekir.</p>
<p>App Store açıklaması bunu gerçek zamanlı dublaj olarak anlatır ve dublajın videoyla birlikte ilerlemesini amaçladığını söyler. Bu, ürünün hedefidir. Her cümlenin kusursuz oturacağı veya uygulamanın çevrimdışı çalışacağı anlamına gelmez.</p>
<h2>Dinleyebileceğiniz diller</h2>
<p>Dublaj dilleri, uygulamada yayımlanan ve bu sitedeki menüde duran 31 dildir: @@LANGS@@. İngilizce bir dersi Türkçe dinlemek ile Türkçe bir anlatımı İngilizce dinlemek aynı işlemdir: bağlantıyı yapıştırın, duymak istediğiniz dili seçin, oynatın. Sitedeki dil menüsü bu dublaj dillerinin listesidir. Her videonun her dilde bulunduğu anlamına gelmez.</p>
<h2>Kimler kullanır</h2>
<p>Ders kayıtları, kurs videoları, yazılım anlatımları, tamir ve el işi videoları, YouTube’da yayımlanan podcast’ler ve bilginin konuşmada olduğu diğer videolar buraya uyar. Öğrenci şekle bakmayı sürdürebilir. Anlatım videosu izleyen kişi ellerini işte tutabilir. Kısa klip, canlı sohbet veya film arşivi arıyorsanız bu uygulama o iş için değildir.</p>
<h2>Ücretsiz kullanım ve DubSee Pro</h2>
<p>İndirme ücretsizdir. Ücretsiz planda günde 1 video vardır; ödüllü reklamlarla en fazla 2 video daha açılır. Ücretsiz videolar yaklaşık 18 dakika ile sınırlıdır. DubSee Pro sınırsız video açar, süre sınırını ve reklamları kaldırır, 10 ses ile arka plan ve kilit ekranı dinlemeyi ekler. Ücretsiz deneme yalnızca App Store uygun bulursa görünür. Fiyat satın almadan önce uygulamada gösterilir ve bölgeye göre değişebilir. DUBSEE bağımsızdır; YouTube veya Google ile bağlantılı değildir, onlar tarafından desteklenmez ya da sponsor edilmez.</p>
<p>İlgili sayfalar: <a href="@@HOWTO@@">iPhone’da YouTube videosu çevirme</a> ve <a href="@@DUB@@">yapay zekâ dublajının nasıl çalıştığı</a>. Yardım için <a href="@@SUPPORT@@">destek sayfası</a>.</p>
''',
 },
 'howto': {
  'en': '''
<p>This is the path that actually exists in DUBSEE. There is no account step on the website, and there is no box on this page that dubs a video for you. The translation happens in the iPhone app after you paste a link.</p>
<h2>Before you paste</h2>
<p>Use a regular YouTube video, not a Short and not a live stream. Captions need to be available for that video. A link that only opens a channel page, a playlist with nothing selected, or a clip is not the input the app is built for. Copy the video link from YouTube’s share sheet.</p>
<h2>The three steps</h2>
<ol>
<li>Copy the supported YouTube link.</li>
<li>Open DUBSEE, paste the link, and choose the language you want to hear. The App Store build can also be reached from the iOS share sheet; if DUBSEE is missing there, install the App Store version and look again.</li>
<li>Press play and listen on the iPhone. You can switch between the original audio and the dubbing.</li>
</ol>
<h2>If you hear no dubbing</h2>
<p>The support notes for this case are specific. Try another video. Check the dubbing language in Settings. Language packs are included in the app, so the first launch does not wait on a voice download, and you can start without creating an account. Deleting the app removes the on-device library, cache, and settings; that is the local reset, not a cloud trash folder.</p>
<h2>What the free plan allows while you practice</h2>
<p>Free includes 1 video a day, plus up to 2 more after rewarded ads, with about an 18-minute limit per free video. A long lecture may stop at that limit until DubSee Pro removes it. Rewarded ads are part of the free allowance; the privacy policy says an ad plays when you choose to watch one. DubSee Pro also adds 10 voices and background playback with the screen locked. Prices and any trial are shown by the App Store, not guessed on this website.</p>
<p>If you are still deciding whether a video qualifies, read <a href="@@TRANSLATOR@@">which YouTube videos DUBSEE translates</a>. For what the voice is doing, read <a href="@@DUB@@">AI video dubbing</a>. Contact is on the <a href="@@SUPPORT@@">support page</a>.</p>
''',
  'tr': '''
<p>DUBSEE’de izlenen yol budur. Bu sitede hesap açma adımı yoktur ve bu sayfa videoyu sizin yerinize dublajlamaz. Çeviri, bağlantıyı yapıştırdıktan sonra iPhone uygulamasında olur.</p>
<h2>Yapıştırmadan önce</h2>
<p>Shorts veya canlı yayın değil, normal bir YouTube videosu kullanın. O videoda altyazı bulunmalıdır. Yalnızca kanal sayfası, içinden video seçilmemiş bir oynatma listesi veya klip, uygulamanın beklediği giriş değildir. Bağlantıyı YouTube’un paylaş menüsünden kopyalayın.</p>
<h2>Üç adım</h2>
<ol>
<li>Desteklenen YouTube bağlantısını kopyalayın.</li>
<li>DUBSEE’yi açın, bağlantıyı yapıştırın ve dinlemek istediğiniz dili seçin. App Store sürümü iOS paylaş menüsünden de açılabilir. DUBSEE orada yoksa App Store’dan kurulu sürümü kullanıp menüye yeniden bakın.</li>
<li>Oynatın ve iPhone’da dinleyin. Orijinal ses ile dublaj arasında geçiş yapılabilir.</li>
</ol>
<h2>Dublaj gelmezse</h2>
<p>Destek notları bu durum için kısadır. Başka bir video deneyin. Ayarlar’dan seslendirme dilini kontrol edin. Dil paketleri uygulamanın içindedir; ilk açılışta ses indirmesi beklenmez ve hesap açmadan kullanmaya başlanabilir. Uygulamayı silmek cihazdaki kütüphane, önbellek ve ayarları kaldırır; bu, bulutta bir çöp kutusu değil, cihaz içi sıfırlamadır.</p>
<h2>Denerken ücretsiz planın sınırı</h2>
<p>Ücretsiz planda günde 1 video vardır; ödüllü reklamlarla en fazla 2 video daha açılır. Ücretsiz videolar yaklaşık 18 dakika ile sınırlıdır. Uzun bir ders, DubSee Pro süre sınırını kaldırana kadar bu sınırda kesilebilir. Ödüllü reklam, ücretsiz kullanımın parçasıdır; gizlilik metni, reklamın siz izlemeyi seçtiğinizde oynadığını söyler. DubSee Pro ayrıca 10 ses ile kilit ekranında arka planda dinlemeyi açar. Fiyat ve varsa deneme, bu sitede tahmin edilmez; App Store gösterir.</p>
<p>Videonun uygun olup olmadığını ayırt etmek için <a href="@@TRANSLATOR@@">DUBSEE’nin hangi YouTube videolarını çevirdiğine</a> bakın. Sesin ne yaptığını okumak için <a href="@@DUB@@">yapay zekâ dublajı</a> sayfasına geçin. Yazışma adresi <a href="@@SUPPORT@@">destek sayfasında</a>.</p>
''',
 },
 'dubbing': {
  'en': '''
<p>AI video dubbing, in this app, means one job: take the spoken content of a supported YouTube video, translate it, and play that translation with a synthetic voice while you watch. It is not a studio recording, a human casting session, or a subtitle file you export. The thing you hear is speech, generated for the language you picked.</p>
<h2>What you hear</h2>
<p>You choose the target language. DUBSEE plays the dubbed voice with the video. The App Store listing also says you can switch back to the original audio, which matters when a term is clearer in the source language than in the translation. Language packs are included in the app, so dubbing does not wait on a first-launch download.</p>
<p>Ten advanced voices are part of DubSee Pro, not a claim that every free session offers a voice menu of ten. Background and lock-screen listening are also Pro features. Free playback stays inside the daily video count and the roughly 18-minute limit.</p>
<h2>Where dubbing helps</h2>
<p>A lecture, a conference talk, a cooking or woodworking tutorial, and a podcast episode uploaded to YouTube are the cases where a spoken translation is more useful than pausing to read. The picture stays in front of you. The voice carries the explanation. DUBSEE does not become a newsroom, a film catalog, or a remote control because the video happens to be about those subjects.</p>
<h2>Limits that stay true</h2>
<p>No Shorts. No live streams. No promise for videos without captions. No offline library of arbitrary YouTube downloads. No unlimited free use. DubSee Pro is the plan that removes the duration cap and the ads, unlocks unlimited videos, adds the 10 voices, and turns on background playback. If the App Store does not show a trial, there is no trial to describe here.</p>
<p>DUBSEE is an independent app. YouTube is a trademark of Google LLC. For the scope of which links work, see the <a href="@@TRANSLATOR@@">YouTube video translator</a> page. For the paste-and-play sequence, see <a href="@@HOWTO@@">how to translate YouTube videos on iPhone</a>.</p>
''',
  'tr': '''
<p>Bu uygulamada yapay zekâ video dublajı tek bir iştir: desteklenen bir YouTube videosunun konuşmasını çevirmek ve siz izlerken o çeviriyi sentetik bir sesle okumak. Stüdyo kaydı, oyuncu seçimi veya dışa aktardığınız bir altyazı dosyası değildir. Duyduğunuz şey, seçtiğiniz dil için üretilmiş konuşmadır.</p>
<h2>Ne duyarsınız</h2>
<p>Hedef dili siz seçersiniz. DUBSEE dublajı videoyla birlikte çalar. App Store açıklaması, özgün sese geri dönebildiğinizi de söyler. Bir terim kaynak dilde çeviriden daha açıksa bu geçiş işe yarar. Dil paketleri uygulamanın içindedir. Dublaj, ilk açılışta bir ses indirmesinin bitmesini beklemez.</p>
<p>On gelişmiş ses, her ücretsiz oturumda on seslik bir menü olduğu iddiası değil, DubSee Pro’nun parçasıdır. Arka planda ve kilit ekranında dinlemek de Pro özelliğidir. Ücretsiz oynatma, günlük video sayısı ve yaklaşık 18 dakikalık sınırın içinde kalır.</p>
<h2>Dublajın işe yaradığı yer</h2>
<p>Ders, konferans konuşması, yemek veya marangozluk anlatımı ve YouTube’a yüklenmiş bir podcast bölümü, konuşmanın çevirisinin altyazıda durup okumaktan daha kullanışlı olduğu yerlerdir. Görüntü önünüzde kalır. Açıklamayı ses taşır. Videonun konusu haber, film veya kumanda olsa da DUBSEE bir haber odası, film arşivi veya kumanda uygulaması olmaz.</p>
<h2>Değişmeyen sınırlar</h2>
<p>Shorts yok. Canlı yayın yok. Altyazısız her video için söz yok. İstediğiniz YouTube videosunu indirip çevrimdışı tutan bir arşiv yok. Sınırsız ücretsiz kullanım yok. Süre sınırını ve reklamları kaldıran, sınırsız video açan, 10 sesi ekleyen ve arka planda dinlemeyi açan plan DubSee Pro’dur. App Store deneme göstermiyorsa burada anlatılacak bir deneme yoktur.</p>
<p>DUBSEE bağımsız bir uygulamadır. YouTube, Google LLC’nin ticari markasıdır. Hangi bağlantıların çalıştığı için <a href="@@TRANSLATOR@@">YouTube video çevirisi</a> sayfasına, yapıştırıp oynatma sırası için <a href="@@HOWTO@@">iPhone’da YouTube çevirisi</a> sayfasına bakın.</p>
''',
 },
}

FAQS = {
 'translator': {
  'en': [
    {'q': 'Which YouTube videos can DUBSEE translate?', 'a': 'Regular YouTube videos with captions available. Shorts and live streams are not supported. A normal video can still be unavailable because of the captions, language, or region.'},
    {'q': 'Does the translator work for languages other than English?', 'a': 'Yes. DUBSEE dubs supported videos in 31 languages. You choose the language you want to hear after pasting the link.'},
  ],
  'tr': [
    {'q': 'DUBSEE hangi YouTube videolarını çevirir?', 'a': 'Altyazısı bulunan normal YouTube videolarını. Shorts ve canlı yayınlar desteklenmez. Normal bir video da altyazı, dil veya bölge yüzünden açılmayabilir.'},
    {'q': 'Çeviri yalnızca İngilizce için mi?', 'a': 'Hayır. DUBSEE desteklenen videoları 31 dilde seslendirir. Bağlantıyı yapıştırdıktan sonra duymak istediğiniz dili seçersiniz.'},
  ],
 },
 'howto': {
  'en': [
    {'q': 'Where do I paste the YouTube link?', 'a': 'In the DUBSEE app on your iPhone, not on this website. You can also look for DUBSEE in the iOS share sheet after the App Store version is installed.'},
    {'q': 'The video opens but there is no dubbing. What should I check?', 'a': 'Try another video and confirm the dubbing language in Settings. Language packs are included, and no account is required to start.'},
  ],
  'tr': [
    {'q': 'YouTube bağlantısını nereye yapıştırırım?', 'a': 'Bu siteye değil, iPhone’daki DUBSEE uygulamasına. App Store sürümü kuruluysa iOS paylaş menüsünde DUBSEE’ye de bakabilirsiniz.'},
    {'q': 'Video açılıyor ama dublaj yok. Neye bakmalıyım?', 'a': 'Başka bir video deneyin ve Ayarlar’dan seslendirme dilini kontrol edin. Dil paketleri uygulamanın içindedir; başlamak için hesap gerekmez.'},
  ],
 },
 'dubbing': {
  'en': [
    {'q': 'Is the dubbed voice a recording of a person?', 'a': 'No. DUBSEE plays an AI voice for the translation. It is not a cast dubbing session and it does not hand you a subtitle file.'},
    {'q': 'Can I listen with the screen locked?', 'a': 'Background and lock-screen playback are part of DubSee Pro. Free playback does not include that, and free videos are about 18 minutes.'},
  ],
  'tr': [
    {'q': 'Dublaj sesi bir kişinin kaydı mı?', 'a': 'Hayır. DUBSEE çeviriyi yapay zekâ sesiyle okur. Bu bir oyuncu kadrosu değildir ve size bir altyazı dosyası vermez.'},
    {'q': 'Ekran kilitliyken dinleyebilir miyim?', 'a': 'Arka planda ve kilit ekranında dinlemek DubSee Pro’nun parçasıdır. Ücretsiz oynatma bunu içermez; ücretsiz videolar yaklaşık 18 dakikadır.'},
  ],
 },
}


def home_guide_section(code):
    data = HOME_GUIDES.get(code)
    if not data:
        return ''
    items = ''.join(
        f'<a href="{href}"><strong>{escape(title)}</strong><span>{escape(text)}</span></a>'
        for href, title, text in data['items']
    )
    return (
        f'<section class="section wrap" id="guides"><p class="eyebrow">DUBSEE</p>'
        f'<h2 class="section-heading">{escape(data["heading"])}</h2>'
        f'<p class="section-sub">{escape(data["intro"])}</p>'
        f'<div class="guide-links">{items}</div></section>'
    )


def guide_urls(base):
    found = []
    for pair in PAIRS:
        en = f"{base}/{pair['en']['slug']}/"
        tr = f"{base}/tr/{pair['tr']['slug']}/"
        found.append((en, tr))
    return found


def _href(lang, target, pair):
    root = '../' if lang == 'en' else '../../'
    if target == lang:
        return './'
    if target == 'en':
        return root + pair['en']['slug'] + '/'
    if target == 'tr':
        return root + 'tr/' + pair['tr']['slug'] + '/'
    return root + target + '/'


def _fill(body, lang, lang_list):
    slugs = {item['key']: '../' + item[lang]['slug'] + '/' for item in PAIRS}
    return (body
        .replace('@@LANGS@@', escape(lang_list))
        .replace('@@SUPPORT@@', '../support.html')
        .replace('@@TRANSLATOR@@', slugs['translator'])
        .replace('@@HOWTO@@', slugs['howto'])
        .replace('@@DUB@@', slugs['dubbing']))


def _page(lang, pair, locales, base, store, email, icons, year, lang_list):
    meta = pair[lang]
    other = 'tr' if lang == 'en' else 'en'
    prefix = '../' if lang == 'en' else '../../'
    home = '../'
    canonical = f"{base}/{meta['slug']}/" if lang == 'en' else f"{base}/tr/{meta['slug']}/"
    en_url = f"{base}/{pair['en']['slug']}/"
    tr_url = f"{base}/tr/{pair['tr']['slug']}/"
    other_url = _href(lang, other, pair)
    title = meta['title']
    description = meta['description']
    faqs = FAQS[pair['key']][lang]
    faq_html = ''.join(
        f'<details class="faq-item"><summary>{escape(item["q"])}</summary><p>{escape(item["a"])}</p></details>'
        for item in faqs
    )
    options = ''.join(
        f'<a class="language-option" data-code="{code}" lang="{code}" hreflang="{code}" href="{_href(lang, code, pair)}"'
        f'{" aria-current=\"page\"" if code == lang else ""}>{escape(row["native"])}</a>'
        for code, row in locales.items()
    )
    crumbs_home = 'Home' if lang == 'en' else 'Ana sayfa'
    schema = {
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': crumbs_home, 'item': base + ('/' if lang == 'en' else '/tr/')},
                {'@type': 'ListItem', 'position': 2, 'name': meta['h1'], 'item': canonical},
            ]},
            {'@type': 'WebPage', '@id': canonical + '#webpage', 'url': canonical, 'name': title, 'description': description, 'inLanguage': lang, 'isPartOf': {'@id': base + '/#website'}},
            {'@type': 'FAQPage', 'inLanguage': lang, 'mainEntity': [
                {'@type': 'Question', 'name': item['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': item['a']}} for item in faqs
            ]},
            {'@type': 'SoftwareApplication', 'name': 'DUBSEE', 'operatingSystem': 'iOS', 'applicationCategory': 'MultimediaApplication', 'applicationSubCategory': 'Photo & Video', 'isAccessibleForFree': True, 'inLanguage': lang, 'downloadUrl': store, 'installUrl': store, 'url': canonical},
        ],
    }
    body = _fill(BODIES[pair['key']][lang], lang, lang_list)
    nav_how = escape('How it works' if lang == 'en' else 'Nasıl çalışır?')
    nav_features = escape('Features' if lang == 'en' else 'Özellikler')
    nav_faq = escape('Questions' if lang == 'en' else 'Sorular')
    privacy = escape('Privacy' if lang == 'en' else 'Gizlilik')
    terms = escape('Terms' if lang == 'en' else 'Kullanım şartları')
    support = escape('Support' if lang == 'en' else 'Destek')
    disclaimer = escape(locales[lang]['disclaimer'])
    schema_json = json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<!doctype html>
<html lang="{lang}" dir="ltr">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title><meta name="description" content="{escape(description, quote=True)}">
<meta name="theme-color" content="#ffffff"><meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="tr" href="{tr_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<link rel="icon" href="{prefix}assets/app-icon.png" type="image/png"><link rel="apple-touch-icon" href="{prefix}assets/app-icon.png">
<meta property="og:type" content="article"><meta property="og:site_name" content="DUBSEE"><meta property="og:locale" content="{'tr_TR' if lang == 'tr' else 'en_US'}"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{base}/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(title, quote=True)}"><meta name="twitter:description" content="{escape(description, quote=True)}"><meta name="twitter:image" content="{base}/assets/og.jpg">
<link rel="stylesheet" href="{prefix}assets/site.css"><link rel="stylesheet" href="{prefix}assets/mobile-refinement.css"><script src="{prefix}assets/site.js" defer></script>
<script type="application/ld+json">{schema_json}</script>
</head>
<body>
<a class="skip" href="#main">{nav_how}</a>
<div class="header-shell"><header class="site-header wrap"><a class="brand" href="{home}" aria-label="DUBSEE"><img src="{prefix}assets/app-icon.png" width="37" height="37" alt=""><span class="brand-copy"><strong>DUBSEE</strong><small>{escape(TAGLINES[lang])}</small></span></a>
<nav class="main-nav" id="main-nav" aria-label="DUBSEE"><a href="{home}#how">{nav_how}</a><a href="{home}#features">{nav_features}</a><a href="{home}#faq">{nav_faq}</a></nav>
<div class="header-actions"><a class="header-store" href="{escape(store)}" aria-label="App Store">{icons['apple']}</a>
<details class="language-picker"><summary aria-label="{escape(locales[lang]['languages'])}">{icons['globe']}<span>{lang.upper()}</span></summary><div class="language-panel"><input type="search" data-language-search placeholder="{escape(locales[lang]['languages'], quote=True)}" aria-label="{escape(locales[lang]['languages'], quote=True)}" autocomplete="off"><nav class="language-list" aria-label="{escape(locales[lang]['languages'], quote=True)}">{options}</nav></div></details>
<details class="mobile-menu"><summary aria-label="{nav_how}">{icons['menu']}</summary><nav aria-label="DUBSEE"><a href="{home}#how">{nav_how}</a><a href="{home}#features">{nav_features}</a><a href="{home}#faq">{nav_faq}</a><a href="../privacy.html">{privacy}</a><a href="../terms.html">{terms}</a><a href="../support.html">{support}</a></nav></details></div></header></div>
<main id="main" class="legal-page guide-page wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{home}">{crumbs_home}</a><span aria-hidden="true">/</span><span>{escape(meta['h1'])}</span></nav>
<p class="eyebrow">DUBSEE</p>
<h1 class="section-heading">{escape(meta['h1'])}</h1>
<p class="section-sub">{escape(description)}</p>
<p class="section-sub"><a href="{other_url}">{escape(meta['other'])}</a></p>
<article class="legal-copy">{body}<h2>{'Questions' if lang == 'en' else 'Sorular'}</h2><div class="faq-list">{faq_html}</div>
<p><a class="store-button" href="{escape(store)}" rel="external">{icons['apple']}<span>App Store</span></a></p>
<p><a href="mailto:{escape(email)}">{escape(email)}</a></p>
</article>
</main>
<footer class="site-footer"><div class="wrap"><div class="footer-top"><a class="brand" href="{home}" aria-label="DUBSEE"><img src="{prefix}assets/app-icon.png" width="37" height="37" alt=""><span class="brand-copy"><strong>DUBSEE</strong></span></a><nav class="footer-links" aria-label="{support}"><a href="../privacy.html">{privacy}</a><a href="../terms.html">{terms}</a><a href="../support.html">{support}</a></nav></div><div class="footer-bottom"><p>{disclaimer}</p><span class="copyright">© {year} DUBSEE</span></div></div></footer>
</body></html>'''


def write_guides(root, locales, base, store, email, icons, year):
    root = Path(root)
    lang_list = ', '.join(locales[code]['native'] for code in locales)
    for pair in PAIRS:
        for lang in ('en', 'tr'):
            folder = root / pair[lang]['slug'] if lang == 'en' else root / 'tr' / pair[lang]['slug']
            folder.mkdir(parents=True, exist_ok=True)
            html = _page(lang, pair, locales, base, store, email, icons, year, lang_list)
            (folder / 'index.html').write_text(html, encoding='utf-8')
    return guide_urls(base)
