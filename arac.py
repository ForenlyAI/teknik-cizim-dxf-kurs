"""Teknik Çizim ve DXF: Parçadan Paftaya — örnek parçaların ortak çizim işlevleri (Hafta 1–4).
Parça ölçüleri ÖRNEK'tir (insansı robotun kolundaki parçaya benzetilerek seçildi, gerçek parça ölçüsü değildir);
dirsek hareket aralığı benzetim parametre dosyasından (veri/sag_kol_parametre.csv) gelir.

  baglanti(msp, x, y)        : ön kol bağlantı parçası, ön görünüş (80 × 40, iki Ø8 delik, ortada Ø20)
  flans(msp, x, y)           : motor flanşı, ön görünüş (Ø90, ortada Ø30, Ø70 bölüm dairesinde dört Ø6,6 delik)
  tutucu_*(msp, x, y)        : bardak tutucu görünüşleri (dış Ø81, iç Ø75, yükseklik 60, taban 4)
"""
import math
import numpy as np

# ÖRNEK ölçüler (mm)
BAG = dict(en=80, boy=40, kalinlik=10, delik=8, delik_ara=60, orta=20)
FLANS = dict(dis=90, orta=30, bolum=70, delik=6.6, adet=4, kalinlik=8)
TUTUCU = dict(dis=81, ic=75, yukseklik=60, taban=4)


def dikdortgen(msp, x, y, w, h, katman="GORUNEN"):
    return msp.add_lwpolyline([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], close=True, dxfattribs={"layer": katman})


def eksen_cizgisi(msp, p1, p2):
    return msp.add_line(p1, p2, dxfattribs={"layer": "EKSEN"})


def arti(msp, x, y, r):
    """Deliğin iki eksen çizgisi: deliği her yönde 3 mm aşar (ÖRNEK taşma payı)."""
    eksen_cizgisi(msp, (x - r - 3, y), (x + r + 3, y))
    eksen_cizgisi(msp, (x, y - r - 3), (x, y + r + 3))


def baglanti(msp, x=0, y=0, eksen=True):
    b = BAG
    dikdortgen(msp, x, y, b["en"], b["boy"])
    cx, cy = x + b["en"] / 2, y + b["boy"] / 2
    msp.add_circle((cx, cy), b["orta"] / 2, dxfattribs={"layer": "GORUNEN"})
    for dx in (-b["delik_ara"] / 2, b["delik_ara"] / 2):
        msp.add_circle((cx + dx, cy), b["delik"] / 2, dxfattribs={"layer": "GORUNEN"})
        if eksen:
            arti(msp, cx + dx, cy, b["delik"] / 2)
    if eksen:
        arti(msp, cx, cy, b["orta"] / 2)
    return cx, cy


def delik_merkezleri(bolum=FLANS["bolum"], adet=FLANS["adet"], baslangic=45.0):
    return [(round(bolum / 2 * math.cos(math.radians(baslangic + i * 360 / adet)), 3),
             round(bolum / 2 * math.sin(math.radians(baslangic + i * 360 / adet)), 3)) for i in range(adet)]


def flans(msp, x=0, y=0, eksen=True):
    f = FLANS
    msp.add_circle((x, y), f["dis"] / 2, dxfattribs={"layer": "GORUNEN"})
    msp.add_circle((x, y), f["orta"] / 2, dxfattribs={"layer": "GORUNEN"})
    if eksen:
        msp.add_circle((x, y), f["bolum"] / 2, dxfattribs={"layer": "EKSEN"})
        eksen_cizgisi(msp, (x - f["dis"] / 2 - 5, y), (x + f["dis"] / 2 + 5, y))
        eksen_cizgisi(msp, (x, y - f["dis"] / 2 - 5), (x, y + f["dis"] / 2 + 5))
    for px, py in delik_merkezleri():
        msp.add_circle((x + px, y + py), f["delik"] / 2, dxfattribs={"layer": "GORUNEN"})
        if eksen:
            arti(msp, x + px, y + py, f["delik"] / 2)


def flans_kesit(msp, x=0, y=0, tara=True):
    """Flanşın A–A kesiti (dikey düzlem, delik eksenlerinden geçmez → yalnız orta delik kesilir)."""
    f = FLANS
    R, r, t = f["dis"] / 2, f["orta"] / 2, f["kalinlik"]
    sol = [(x, y - R), (x + t, y - R), (x + t, y - r), (x, y - r)]
    sag = [(x, y + r), (x + t, y + r), (x + t, y + R), (x, y + R)]
    for p in (sol, sag):
        msp.add_lwpolyline(p, close=True, dxfattribs={"layer": "GORUNEN"})
        if tara:
            h = msp.add_hatch(dxfattribs={"layer": "TARAMA"})
            h.set_pattern_fill("ANSI31", scale=0.5)
            h.paths.add_polyline_path(p, is_closed=True)
    # delik kenarları (kesitin arkasında görünen çizgiler)
    msp.add_line((x, y - r), (x, y + r), dxfattribs={"layer": "GORUNEN"})
    msp.add_line((x + t, y - r), (x + t, y + r), dxfattribs={"layer": "GORUNEN"})
    eksen_cizgisi(msp, (x - 5, y), (x + t + 5, y))


def tutucu_on(msp, x=0, y=0, gizli=True):
    t = TUTUCU
    R, r = t["dis"] / 2, t["ic"] / 2
    dikdortgen(msp, x - R, y, t["dis"], t["yukseklik"])
    if gizli:
        msp.add_line((x - r, y + t["taban"]), (x - r, y + t["yukseklik"]), dxfattribs={"layer": "GIZLI"})
        msp.add_line((x + r, y + t["taban"]), (x + r, y + t["yukseklik"]), dxfattribs={"layer": "GIZLI"})
        msp.add_line((x - r, y + t["taban"]), (x + r, y + t["taban"]), dxfattribs={"layer": "GIZLI"})
    eksen_cizgisi(msp, (x, y - 5), (x, y + t["yukseklik"] + 5))


def tutucu_ust(msp, x=0, y=0):
    t = TUTUCU
    msp.add_circle((x, y), t["dis"] / 2, dxfattribs={"layer": "GORUNEN"})
    msp.add_circle((x, y), t["ic"] / 2, dxfattribs={"layer": "GORUNEN"})
    arti(msp, x, y, t["dis"] / 2)


def tutucu_yarim_kesit(msp, x=0, y=0):
    """Sol yarı görünüş, sağ yarı kesit (simetrik parça için yarım kesit)."""
    t = TUTUCU
    R, r, H, b = t["dis"] / 2, t["ic"] / 2, t["yukseklik"], t["taban"]
    msp.add_lwpolyline([(x, y), (x - R, y), (x - R, y + H), (x, y + H)], dxfattribs={"layer": "GORUNEN"})
    duvar = [(x + r, y + b), (x + R, y + b), (x + R, y + H), (x + r, y + H)]
    taban = [(x, y), (x + R, y), (x + R, y + b), (x, y + b)]
    for p in (duvar, taban):
        msp.add_lwpolyline(p, close=True, dxfattribs={"layer": "GORUNEN"})
        h = msp.add_hatch(dxfattribs={"layer": "TARAMA"})
        h.set_pattern_fill("ANSI31", scale=0.5)
        h.paths.add_polyline_path(p, is_closed=True)
    eksen_cizgisi(msp, (x, y - 5), (x, y + H + 5))   # yarım kesitte görünüş yarısına gizli çizgi konmaz


def yazi(msp, metin, x, y, boy=3.5, hiza="LEFT", katman="YAZI"):
    from ezdxf.enums import TextEntityAlignment
    h = {"LEFT": TextEntityAlignment.BOTTOM_LEFT, "CENTER": TextEntityAlignment.BOTTOM_CENTER,
         "MIDDLE": TextEntityAlignment.MIDDLE_CENTER, "RIGHT": TextEntityAlignment.BOTTOM_RIGHT}[hiza]
    return msp.add_text(metin, height=boy, dxfattribs={"layer": katman, "style": "OpenSans"}).set_placement((x, y), align=h)


def olcu_yatay(msp, p1, p2, y_taban, dimstyle="EZDXF", metin="<>"):
    msp.add_linear_dim(base=((p1[0] + p2[0]) / 2, y_taban), p1=p1, p2=p2, angle=0, dimstyle=dimstyle, text=metin,
                              dxfattribs={"layer": "OLCU"}).render()


def olcu_dikey(msp, p1, p2, x_taban, dimstyle="EZDXF"):
    msp.add_linear_dim(base=(x_taban, (p1[1] + p2[1]) / 2), p1=p1, p2=p2, angle=90, dimstyle=dimstyle,
                              dxfattribs={"layer": "OLCU"}).render()


def olcu_cap(msp, merkez, r, aci=45, dimstyle="EZ_RADIUS"):
    msp.add_diameter_dim(center=merkez, radius=r, angle=aci, dimstyle=dimstyle,
                                dxfattribs={"layer": "OLCU"}).render()


def olcu_stil(doc, boy=3.5):
    """Kursun ölçü stili: yazı 3,5 mm, ok 3 mm (ÖRNEK), milimetre, ondalık ayıracı virgül."""
    for ad in ("EZDXF", "EZ_RADIUS"):
        s = doc.dimstyles.get(ad)
        s.dxf.dimtxt = boy
        s.dxf.dimlfac = 1
        s.dxf.dimtsz = 0
        s.dxf.dimblk = ""
        s.dxf.dimscale = 1
        s.dxf.dimasz = 3
        s.dxf.dimexe = 2
        s.dxf.dimexo = 1
        s.dxf.dimgap = 1
        s.dxf.dimdsep = ord(",")
        s.dxf.dimdec = 1 if ad == "EZ_RADIUS" else 0
        s.dxf.dimtzin = 8
        s.dxf.dimclrd = 94
        s.dxf.dimclre = 94
        s.dxf.dimclrt = 7


def pafta(msp, en, boy, sol=20, diger=10):
    """Kâğıt kenarı (ince) ve çizim çerçevesi (kalın). Kenar payları ÖRNEK (sol 20 mm dosyalama payı, öteki kenarlar 10 mm)."""
    dikdortgen(msp, 0, 0, en, boy, katman="OLCU")
    dikdortgen(msp, sol, diger, en - sol - diger, boy - 2 * diger, katman="CERCEVE")
    return (sol, diger, en - diger, boy - diger)


ANTET_ALAN = [("Kurum", "Forenly AI Academy"), ("Belge türü", "Parça resmi"), ("Başlık", ""),
              ("Belge no", ""), ("Düzenleyen", "Kurs örneği"), ("Onaylayan", "ÖRNEK"),
              ("Tarih", "2026-10-08"), ("Ölçek", ""), ("Sayfa", "1/1"), ("İzdüşüm", "birinci açı")]


def antet(msp, x2, y1, alanlar, en=180, satir=10):
    """Sağ alt köşeye antet: iki sütun, her hücrede alan adı (küçük) ve değeri. Alan seçimi ISO 7200'deki alanlara dayanır."""
    n = (len(alanlar) + 1) // 2
    x1 = x2 - en
    dikdortgen(msp, x1, y1, en, n * satir, katman="CERCEVE")
    msp.add_line((x1 + en / 2, y1), (x1 + en / 2, y1 + n * satir), dxfattribs={"layer": "GORUNEN"})
    for i in range(1, n):
        msp.add_line((x1, y1 + i * satir), (x2, y1 + i * satir), dxfattribs={"layer": "GORUNEN"})
    for i, (ad, deger) in enumerate(alanlar):
        sx = x1 + (i % 2) * en / 2
        sy = y1 + (n - 1 - i // 2) * satir
        yazi(msp, ad, sx + 1.5, sy + satir - 2.8, boy=1.8)
        yazi(msp, deger, sx + 1.5, sy + 1.5, boy=3.0)
    return x1, y1, n * satir
