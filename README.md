# Teknik Çizim ve DXF: Parçadan Paftaya — kurs dosyaları

Forenly AI Academy'deki **Teknik Çizim ve DXF: Parçadan Paftaya** kursunun çizim dosyaları. Derslerde ekranda gördüğünüz her Python oturumu ve her çizim bu betiklerle üretildi; çizimler DXF dosyası olarak yazılır ve aynı dosyadan PNG / PDF'e çevrilir.

DXF açık bir çizim dosyası biçimidir; buradaki dosyalar AutoCAD'de ve öteki çizim programlarında (ör. ücretsiz DXF görüntüleyiciler) açılabilir. Kurs bir programın menüsünü değil, teknik resmin kurallarını öğretir.

## Gerekenler

- **Python 3.10 veya üstü**, `ezdxf` (1.4 ya da üstü), `matplotlib`, `numpy` ve `pillow`. Hepsi ücretsizdir.
- Kurulum: `python -m pip install -r requirements.txt`
- Bilgisayarınıza kurmak istemezseniz tarayıcıda çalışan bir not defterine (ör. Google Colab) bu klasörü yükleyip aynı betikleri çalıştırabilirsiniz.

## Nasıl çalıştırılır

1. Bu depoyu indirin (Code → Download ZIP) ve klasörde bir terminal açın.
2. Haftaları sırayla çalıştırın: `python hafta1.py`, `python hafta2.py`, `python hafta3.py`, `python hafta4.py`. Dördüncü hafta üçüncü haftanın kat planı işlevlerini kullanır.
3. Betikler çalışınca `cikti/` klasöründe DXF, PDF ve PNG dosyaları, `ekran/<ders>/` klasöründe derslerdeki çizimler (`.png`) ve Python oturum kayıtları (`.txt`), kökte de ölçülen sayılar (`OLCUMLER.json`) oluşur.
4. İsteğe bağlı: `python komut_ciz.py` oturum kayıtlarını derslerdeki gibi resme çizer (Linux'taki DejaVu yazı tipini kullanır).

## Sonucunuzu karşılaştırın

`beklenen/OLCUMLER.json` ekibimizin 2026-10-08 koşumunda ölçtüğü sayılardır; `beklenen/ekran/` aynı koşumun çizimleri ve oturum kayıtları, `beklenen/cikti/` ise DXF, PDF ve PNG dosyalarıdır. Dosya boyutları (Ders 4.3, `d4_3_dosya_kb`) bilgisayara göre birkaç kB farklı çıkabilir; öteki sayılar aynı çıkmalıdır.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ortak.py` | Milimetre birimli yeni çizim ve katman düzeni (`yeni`), DXF'ten PNG çizimi, oturum kaydı, ölçüm yazma |
| `arac.py` | Örnek parçalar (bağlantı parçası, motor flanşı, bardak tutucu), ölçü, pafta ve antet yardımcıları |
| `kaynaklar.py` | Kursta anılan standartların künyeleri ve müfredat eşlemesinde kullanılan ders izlenceleri |
| `hafta1.py` | Çizginin dili: ilk DXF, çizgi türleri ve katmanlar, delik dizisi ve yay, ölçek ve yazı |
| `hafta2.py` | Ölçü ve görünüş: ölçülendirme, üç görünüş, gizli çizgi ve hizalama, tekrar ve eksik ölçü denetimi |
| `hafta3.py` | Kesit ve plan: kesit ve tarama, yarım kesit, bloklar, 1:50 kafe kat planı |
| `hafta4.py` | Pafta ve çıktı: A serisi ve çerçeve, antet, PDF ve PNG çıktısı, teslim öncesi denetim |
| `komut_ciz.py` | Oturum kayıtlarını resme çizer (isteğe bağlı) |
| `veri/cay_servisi_kaydi.csv` | Kafede çay servisi benzetim kaydı: zaman, kol eklem açıları, bardağın konumu (saniyede 50 örnek) |
| `veri/sag_kol_parametre.csv` | Sağ kol benzetim parametreleri: eklem sınırları (dirseğin hareket aralığı buradan) |

## Veri ve ölçüler hakkında

Robot verisi **benzetim kaydıdır**, gerçek robot ölçümü değildir. Dirseğin hareket aralığı ve kat planındaki bardağın yolu bu kayıttan gelir.

Parça ölçüleri (bağlantı parçası, motor flanşı, bardak tutucu), oda ve mobilya ölçüleri, pafta kenar payları, yazı yükseklikleri ve antet ölçüleri **ÖRNEKTİR**; gerçek bir parçanın ya da mekânın ölçüsü değildir. `kaynaklar.py` içindeki standartlar gerçek yayınlardır; kursta yalnız konuları anılır, metinlerinden sayı alınmamıştır.
