# PDF Atölyesi: kaynak kod

Bu dal sitenin kaynağıdır. Yayındaki site `main` dalındadır; bu dal yayınlanmaz.

- `foy/index.html`: uygulamanın tamamı
- `build.py`: yayınlanacak dosyaları `site/` klasörüne üretir
- `og.py`, `assets/og.png`: bağlantı paylaşılınca görünen görsel
- `testler/duman.py`: hızlı kontrol

Derleme ve kontrol:

    mkdir -p site
    python3 build.py
    python3 testler/duman.py

Yayınlamak için `site/` içindeki dosyalar `main` dalının köküne kopyalanır.
Alan adı değişirse `build.py` içindeki `SITE` satırı güncellenir.

Bu depo herkese açıktır. Kitap sayfası, föy, soru, PDF, yedek dosyası (.json), şifre veya anahtar eklenmemelidir.
