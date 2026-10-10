"""Hafta 2 · Ölçü ve Görünüş — Ders 2.1–2.4.
  python hafta2.py   → ekran/2.x/*.txt + *.png, cikti/*.dxf, OLCUMLER.json (d2_*)"""
from ortak import yeni, kaydet, dxf_ciz, oturum, olc
from arac import (baglanti, flans, tutucu_on, tutucu_ust, dikdortgen, yazi, olcu_yatay, olcu_dikey, olcu_cap, olcu_stil,
                  BAG, FLANS, TUTUCU)


def baglanti_uc_gorunus(msp, ara=25):
    """Birinci açı yerleşimi: ön görünüş solda üstte, üst görünüş ön görünüşün ALTINDA, soldan görünüş ön görünüşün SAĞINDA."""
    b = BAG; t = b["kalinlik"]
    baglanti(msp, 0, 0)
    # üst görünüş (yukarıdan bakış): 80 × kalınlık, delikler gizli çizgi
    y0 = -ara - t
    dikdortgen(msp, 0, y0, b["en"], t)
    cx = b["en"] / 2
    for dx, r in ((-b["delik_ara"] / 2, b["delik"] / 2), (0, b["orta"] / 2), (b["delik_ara"] / 2, b["delik"] / 2)):
        for s in (-r, r):
            msp.add_line((cx + dx + s, y0), (cx + dx + s, y0 + t), dxfattribs={"layer": "GIZLI"})
        msp.add_line((cx + dx, y0 - 3), (cx + dx, y0 + t + 3), dxfattribs={"layer": "EKSEN"})
    # soldan görünüş (ön görünüşün sağında): kalınlık × 40
    x0 = b["en"] + ara
    dikdortgen(msp, x0, 0, t, b["boy"])
    cy = b["boy"] / 2
    for r in (b["delik"] / 2, b["orta"] / 2):
        for s in (-r, r):
            msp.add_line((x0, cy + s), (x0 + t, cy + s), dxfattribs={"layer": "GIZLI"})
    msp.add_line((x0 - 3, cy), (x0 + t + 3, cy), dxfattribs={"layer": "EKSEN"})
    return y0, x0


def ders_2_1():
    ns = oturum("2.1", "olcu-ekle", """
from ortak import yeni
from arac import baglanti, olcu_stil, olcu_yatay, olcu_dikey, olcu_cap
doc = yeni()
olcu_stil(doc)
msp = doc.modelspace()
cx, cy = baglanti(msp)
olcu_yatay(msp, (0, 40), (80, 40), 50)
olcu_yatay(msp, (10, 20), (70, 20), -10)
olcu_dikey(msp, (80, 0), (80, 40), 92)
olcu_cap(msp, (cx, cy), 10, aci=60)
olcu_cap(msp, (10, 20), 4, aci=225)
olculer = msp.query("DIMENSION")
len(olculer)
[round(o.get_measurement(), 1) for o in olculer]
doc.saveas("cikti/baglanti_olculu.dxf")
""")
    dxf_ciz(ns["doc"], "2.1", "baglanti-olculu", "Ön kol bağlantı parçası, beş ölçüyle (ÖRNEK ölçüler, mm)", "baglanti_olculu.dxf")
    doc = yeni(); olcu_stil(doc); msp = doc.modelspace()
    flans(msp, 0, 0)
    f = FLANS
    olcu_cap(msp, (0, 0), f["dis"] / 2, aci=200)
    olcu_cap(msp, (0, 0), f["orta"] / 2, aci=-30)
    olcu_cap(msp, (0, 0), f["bolum"] / 2, aci=110)
    from arac import delik_merkezleri
    px, py = delik_merkezleri()[0]
    olcu_cap(msp, (px, py), f["delik"] / 2, aci=45)
    yazi(msp, "4 delik, eşit aralıklı", px + 8, py + 10, boy=3.5)
    kaydet(doc, "flans_olculu")
    dxf_ciz(doc, "2.1", "flans-olculu", "Motor flanşı: çap ölçüleri ve bölüm dairesi (ÖRNEK ölçüler, mm)", "flans_olculu.dxf")
    olc(d2_1_olcu=len(ns["olculer"]), d2_1_degerler=[round(o.get_measurement(), 1) for o in ns["olculer"]], d2_1_flans_olcu=4)


def ders_2_2():
    doc = yeni(); msp = doc.modelspace()
    y0, x0 = baglanti_uc_gorunus(msp)
    yazi(msp, "ön görünüş", 40, 46, boy=4, hiza="CENTER")
    yazi(msp, "üstten görünüş", 40, y0 - 10, boy=4, hiza="CENTER")
    yazi(msp, "soldan görünüş", x0 + 5, 46, boy=4, hiza="CENTER")
    kaydet(doc, "baglanti_uc_gorunus")
    dxf_ciz(doc, "2.2", "uc-gorunus", "Ön kol bağlantı parçası: üç görünüş, birinci açı yerleşimi", "baglanti_uc_gorunus.dxf")

    oturum("2.2", "gorunus-olculeri", """
from arac import BAG
en, boy, kalinlik = BAG["en"], BAG["boy"], BAG["kalinlik"]
gorunus = {
    "ön":     (en, boy),
    "üstten": (en, kalinlik),
    "soldan": (kalinlik, boy),
}
for ad, (g, y) in gorunus.items():
    print(f"{ad:7s} genişlik {g:3d} mm   yükseklik {y:3d} mm")
gorunus["ön"][0] == gorunus["üstten"][0]
gorunus["ön"][1] == gorunus["soldan"][1]
""")
    doc = yeni(); msp = doc.modelspace()
    # birinci açı yerleşim şeması: kutular ve oklar
    dikdortgen(msp, 0, 0, 60, 40); yazi(msp, "ÖN", 30, 20, boy=8, hiza="MIDDLE")
    dikdortgen(msp, 0, -70, 60, 40); yazi(msp, "ÜSTTEN", 30, -50, boy=8, hiza="MIDDLE")
    dikdortgen(msp, 90, 0, 50, 40); yazi(msp, "SOLDAN", 115, 20, boy=6, hiza="MIDDLE")
    dikdortgen(msp, -80, 0, 50, 40, katman="GIZLI"); yazi(msp, "SAĞDAN", -55, 20, boy=6, hiza="MIDDLE")
    yazi(msp, "Birinci açı: üstten bakış alta, soldan bakış sağa konur", -80, 60, boy=6)
    kaydet(doc, "birinci_aci")
    dxf_ciz(doc, "2.2", "birinci-aci", "Görünüşlerin yeri: birinci açı yöntemi (ISO 5456-2)", "birinci_aci.dxf")
    olc(d2_2_gorunus=3, d2_2_on=[BAG["en"], BAG["boy"]], d2_2_ust=[BAG["en"], BAG["kalinlik"]], d2_2_sol=[BAG["kalinlik"], BAG["boy"]],
        d2_2_ara_mm=25)


def ders_2_3():
    t = TUTUCU
    doc = yeni(); msp = doc.modelspace()
    tutucu_on(msp, 0, 0)
    tutucu_ust(msp, 0, -30 - t["dis"] / 2)
    tutucu_on(msp, t["dis"] + 30, 0)
    yazi(msp, "ön görünüş", 0, t["yukseklik"] + 8, boy=4, hiza="CENTER")
    yazi(msp, "soldan görünüş", t["dis"] + 30, t["yukseklik"] + 8, boy=4, hiza="CENTER")
    yazi(msp, "üstten görünüş", 0, -30 - t["dis"] - 10, boy=4, hiza="CENTER")
    kaydet(doc, "tutucu_uc_gorunus")
    dxf_ciz(doc, "2.3", "tutucu-gorunus", "Bardak tutucu: gizli çizgiler içteki boşluğu gösterir (ÖRNEK ölçüler)", "tutucu_uc_gorunus.dxf")

    ns = oturum("2.3", "hizalama-denetimi", """
import ezdxf
doc = ezdxf.readfile("cikti/tutucu_uc_gorunus.dxf")
msp = doc.modelspace()
on = msp.query("LWPOLYLINE")[0]
xs = [p[0] for p in on.get_points()]
ust = [c for c in msp.query("CIRCLE")]
ust_cap = max(c.dxf.radius for c in ust) * 2
on_genislik = float(max(xs) - min(xs))
on_genislik, ust_cap
bool(on_genislik == ust_cap)
gizli = msp.query('LINE[layer=="GIZLI"]')
len(gizli)
sorted({l.dxf.start.x for l in gizli if abs(l.dxf.start.x) < 50 and l.dxf.start.x == l.dxf.end.x})
""")
    doc = yeni(); msp = doc.modelspace()
    tutucu_on(msp, 0, 0)
    tutucu_ust(msp, 0, -30 - t["dis"] / 2)
    for x in (-t["dis"] / 2, -t["ic"] / 2, t["ic"] / 2, t["dis"] / 2):
        msp.add_line((x, t["yukseklik"]), (x, -30 - t["dis"] / 2), dxfattribs={"layer": "OLCU", "color": 6})
    kaydet(doc, "tutucu_hizalama")
    dxf_ciz(doc, "2.3", "tutucu-hizalama", "Ön ve üstten görünüş aynı genişlikte: izdüşüm çizgileri", "tutucu_hizalama.dxf")
    olc(d2_3_on_genislik=ns["on_genislik"], d2_3_ust_cap=ns["ust_cap"], d2_3_gizli=len(ns["gizli"]),
        d2_3_dis=t["dis"], d2_3_ic=t["ic"], d2_3_yukseklik=t["yukseklik"], d2_3_taban=t["taban"])


def ders_2_4():
    t = TUTUCU
    doc = yeni(); olcu_stil(doc); msp = doc.modelspace()
    tutucu_on(msp, 0, 0)
    R = t["dis"] / 2
    olcu_yatay(msp, (-R, t["yukseklik"]), (R, t["yukseklik"]), t["yukseklik"] + 12)
    olcu_yatay(msp, (-R, 0), (R, 0), -12)                     # TEKRAR: aynı genişlik ikinci kez
    olcu_dikey(msp, (R, 0), (R, t["yukseklik"]), R + 12)
    kaydet(doc, "tutucu_tekrarli")
    ns = oturum("2.4", "tekrar-denetimi", """
import ezdxf
from collections import Counter
doc = ezdxf.readfile("cikti/tutucu_tekrarli.dxf")
olculer = [round(o.get_measurement(), 1) for o in doc.modelspace().query("DIMENSION")]
olculer
tekrar = [d for d, n in Counter(olculer).items() if n > 1]
tekrar
gereken = {"dış çap": 81, "iç çap": 75, "yükseklik": 60, "taban": 4}
eksik = [ad for ad, d in gereken.items() if d not in olculer]
eksik
""")
    dxf_ciz(doc, "2.4", "tutucu-tekrarli", "Önce: aynı ölçü iki kez, iki ölçü eksik", "tutucu_tekrarli.dxf")
    doc = yeni(); olcu_stil(doc); msp = doc.modelspace()
    tutucu_on(msp, 0, 0)
    r = t["ic"] / 2
    olcu_yatay(msp, (-R, t["yukseklik"]), (R, t["yukseklik"]), t["yukseklik"] + 20, metin="Ø<>")
    olcu_yatay(msp, (-r, t["yukseklik"]), (r, t["yukseklik"]), t["yukseklik"] + 10, metin="Ø<>")
    olcu_dikey(msp, (R, 0), (R, t["yukseklik"]), R + 12)
    olcu_dikey(msp, (-r, 0), (-r, t["taban"]), -R - 12)
    kaydet(doc, "tutucu_olculu")
    import ezdxf
    son = [round(o.get_measurement(), 1) for o in ezdxf.readfile("cikti/tutucu_olculu.dxf").modelspace().query("DIMENSION")]
    dxf_ciz(doc, "2.4", "tutucu-olculu", "Sonra: dört ölçü, her biri bir kez", "tutucu_olculu.dxf")
    olc(d2_4_once=ns["olculer"], d2_4_tekrar=ns["tekrar"], d2_4_eksik=ns["eksik"], d2_4_sonra=son)


if __name__ == "__main__":
    for f in (ders_2_1, ders_2_2, ders_2_3, ders_2_4):
        f(); print(f.__name__, "tamam")
