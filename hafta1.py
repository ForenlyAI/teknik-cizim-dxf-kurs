"""Hafta 1 · Çizginin Dili — Ders 1.1–1.4.
  python hafta1.py   → ekran/1.x/*.txt + *.png, cikti/*.dxf, OLCUMLER.json (d1_*)"""
import math, os
import numpy as np
from ortak import yeni, kaydet, dxf_ciz, oturum, olc, parametre, LAB, CIKTI
from arac import baglanti, flans, arti, yazi, dikdortgen, delik_merkezleri, BAG, FLANS


def ders_1_1():
    ns = oturum("1.1", "ilk-cizim", """
import ezdxf
doc = ezdxf.new("R2018", units=4)
msp = doc.modelspace()
kose = [(0, 0), (80, 0), (80, 40), (0, 40)]
for i in range(4):
    msp.add_line(kose[i], kose[(i + 1) % 4])
for merkez, r in [((40, 20), 10), ((10, 20), 4), ((70, 20), 4)]:
    msp.add_circle(merkez, radius=r)
len(msp)
[e.dxftype() for e in msp]
doc.saveas("cikti/ilk_cizim.dxf")
""")
    dxf_ciz(ns["doc"], "1.1", "ilk-cizim-dxf", "İlk çizim: dört çizgi ve üç daire (80 × 40 mm, ÖRNEK)", "ilk_cizim.dxf")
    metin = (CIKTI / "ilk_cizim.dxf").read_text(encoding="utf-8", errors="replace").splitlines()
    oturum("1.1", "dxf-metin", """
satirlar = open("cikti/ilk_cizim.dxf", encoding="utf-8").read().splitlines()
len(satirlar)
satirlar[:6]
i = satirlar.index("CIRCLE")
satirlar[i:i + 2]
bolumler = [satirlar[k + 2] for k, s in enumerate(satirlar[:-2]) if s.strip() == "SECTION"]
bolumler
""")
    bolum = [metin[k + 2].strip() for k, s in enumerate(metin[:-2]) if s.strip() == "SECTION"]
    olc(d1_1_varlik=len(ns["msp"]), d1_1_cizgi=4, d1_1_daire=3, d1_1_satir=len(metin), d1_1_bolum=len(bolum),
        d1_1_bolumler=bolum, d1_1_en_mm=80, d1_1_boy_mm=40)


def ders_1_2():
    ns = oturum("1.2", "katmanlar", """
from ortak import yeni, KATMAN
doc = yeni()
for ad in KATMAN:
    k = doc.layers.get(ad)
    print(f"{ad:8s} renk {k.dxf.color}  çizgi {k.dxf.linetype:10s} kalınlık {k.dxf.lineweight / 100:.2f} mm")
len(KATMAN)
""")
    doc = yeni(); msp = doc.modelspace()
    ornek = [("GORUNEN", "görünen kenar · sürekli kalın"), ("GIZLI", "görünmeyen kenar · kesik ince"),
             ("EKSEN", "eksen · noktalı ince"), ("KESIT", "kesme düzlemi · noktalı kalın uçlu"),
             ("OLCU", "ölçü ve yardımcı çizgi · sürekli ince")]
    for i, (k, ad) in enumerate(ornek):
        y = 100 - i * 22
        msp.add_line((0, y), (120, y), dxfattribs={"layer": k})
        yazi(msp, f"{k} — {ad}", 130, y - 2.5, boy=6)
    dxf_ciz(doc, "1.2", "cizgi-turleri", "Beş katman, beş çizgi türü", "cizgi_turleri.dxf")
    kaydet(doc, "cizgi_turleri")

    doc = yeni(); msp = doc.modelspace()
    baglanti(msp, 0, 0)
    msp.add_line((0, -25), (80, -25), dxfattribs={"layer": "GORUNEN"})
    dikdortgen(msp, 0, -35, 80, 10)
    for x in (10, 30, 50, 70):
        msp.add_line((x, -35), (x, -25), dxfattribs={"layer": "GIZLI"})
    msp.add_line((40, -38), (40, -22), dxfattribs={"layer": "EKSEN"})
    kaydet(doc, "baglanti_katmanli")
    dxf_ciz(doc, "1.2", "baglanti-katmanli", "Ön kol bağlantı parçası: görünen, gizli ve eksen katmanları", "baglanti_katmanli.dxf")
    sayim = {}
    for e in msp:
        sayim[e.dxf.layer] = sayim.get(e.dxf.layer, 0) + 1
    oturum("1.2", "katman-sayimi", """
import ezdxf
doc = ezdxf.readfile("cikti/baglanti_katmanli.dxf")
sayim = {}
for e in doc.modelspace():
    sayim[e.dxf.layer] = sayim.get(e.dxf.layer, 0) + 1
sayim
sayim.get("0", 0)
""")
    olc(d1_2_katman=len(ns["KATMAN"]), d1_2_sayim=sayim, d1_2_katman0=sayim.get("0", 0))


def ders_1_3():
    p = parametre()["dirsek"]
    alt, ust = math.degrees(p["alt_rad"]), math.degrees(p["ust_rad"])
    ns = oturum("1.3", "delik-merkezleri", """
import math
from arac import delik_merkezleri, FLANS
FLANS
merkez = delik_merkezleri()
for x, y in merkez:
    print(f"x {x:7.2f}   y {y:7.2f}   uzaklık {math.hypot(x, y):.1f}")
aci = [round(math.degrees(math.atan2(y, x))) % 360 for x, y in merkez]
aci
""")
    doc = yeni(); msp = doc.modelspace()
    flans(msp, 0, 0)
    kaydet(doc, "flans")
    dxf_ciz(doc, "1.3", "flans", "Motor flanşı: dört delik bölüm dairesi üzerinde, 90° arayla (ÖRNEK ölçüler)", "flans.dxf")

    doc = yeni(); msp = doc.modelspace()
    L = 100  # ön kol çizgisi uzunluğu ÖRNEK
    msp.add_circle((0, 0), 6, dxfattribs={"layer": "GORUNEN"})
    arti(msp, 0, 0, 6)
    msp.add_line((-L * 0.9, 0), (0, 0), dxfattribs={"layer": "GORUNEN"})
    yazi(msp, "üst kol", -L * 0.9, 4, boy=6)
    msp.add_arc((0, 0), L * 0.8, alt, ust, dxfattribs={"layer": "OLCU"})
    for a, ad in ((alt, "alt sınır"), (ust, "üst sınır")):
        x, y = L * math.cos(math.radians(a)), L * math.sin(math.radians(a))
        msp.add_line((0, 0), (x, y), dxfattribs={"layer": "EKSEN"})
        yazi(msp, f"{ad} {a:.0f}°", x + 3, y, boy=6)
    yazi(msp, f"dirsek hareket aralığı {ust - alt:.0f}° (benzetim parametre dosyası)", -L * 0.9, -L * 1.08, boy=6)
    kaydet(doc, "dirsek_yayi")
    dxf_ciz(doc, "1.3", "dirsek-yayi", "Dirseğin hareket aralığı: yay ve iki sınır çizgisi", "dirsek_yayi.dxf")
    olc(d1_3_delik=FLANS["adet"], d1_3_bolum_cap=FLANS["bolum"], d1_3_delik_cap=FLANS["delik"], d1_3_dis_cap=FLANS["dis"],
        d1_3_orta_cap=FLANS["orta"], d1_3_merkez=delik_merkezleri(), d1_3_aci=ns["aci"],
        d1_3_dirsek_alt_der=round(alt, 1), d1_3_dirsek_ust_der=round(ust, 1), d1_3_dirsek_aralik_der=round(ust - alt, 1))


def ders_1_4():
    ns = oturum("1.4", "olcek", """
buyutme = [50, 20, 10, 5, 2]
kucultme = [2, 5, 10, 20, 50, 100, 200, 500, 1000]
def kagitta(gercek_mm, olcek):
    pay, payda = olcek
    return gercek_mm * pay / payda
kagitta(90, (1, 1))
kagitta(90, (2, 1))
kagitta(8000, (1, 50))
kagitta(8000, (1, 100))
def sigdir(gercek_mm, alan_mm):
    for p in buyutme + [1]:
        if gercek_mm * p <= alan_mm:
            return (p, 1)
    for q in kucultme:
        if gercek_mm / q <= alan_mm:
            return (1, q)
sigdir(90, 180)
sigdir(8000, 250)
""")
    doc = yeni(); msp = doc.modelspace()
    for i, h in enumerate([2.5, 3.5, 5, 7, 10]):
        yazi(msp, f"Yazı yüksekliği {str(h).replace('.', ',')} mm — ÖN KOL BAĞLANTI PARÇASI", 0, 120 - i * 26 - h, boy=h)
    kaydet(doc, "yazi_boylari")
    dxf_ciz(doc, "1.4", "yazi-boylari", "Aynı yazı, beş yükseklik (ÖRNEK yükseklikler)", "yazi_boylari.dxf")

    doc = yeni(); msp = doc.modelspace()
    flans(msp, 60, 60)
    dikdortgen(msp, 0, 0, 120, 120, katman="OLCU")
    yazi(msp, "1:1", 60, -12, boy=8, hiza="CENTER")
    from ezdxf.math import Matrix44
    tmp = yeni(); flans(tmp.modelspace(), 0, 0)
    for e in tmp.modelspace():
        k = e.copy(); k.transform(Matrix44.scale(2) @ Matrix44.translate(250, 90, 0)); msp.add_entity(k)
    dikdortgen(msp, 150, -10, 200, 200, katman="OLCU")
    yazi(msp, "2:1", 250, -22, boy=8, hiza="CENTER")
    kaydet(doc, "flans_olcek")
    dxf_ciz(doc, "1.4", "flans-olcek", "Aynı flanş iki ölçekte: 1:1 ve 2:1", "flans_olcek.dxf")
    olc(d1_4_flans_1_1=ns["kagitta"](90, (1, 1)), d1_4_flans_2_1=ns["kagitta"](90, (2, 1)),
        d1_4_plan_1_50=ns["kagitta"](8000, (1, 50)), d1_4_plan_1_100=ns["kagitta"](8000, (1, 100)),
        d1_4_sigdir_flans=list(ns["sigdir"](90, 180)), d1_4_sigdir_plan=list(ns["sigdir"](8000, 250)))


if __name__ == "__main__":
    for f in (ders_1_1, ders_1_2, ders_1_3, ders_1_4):
        f(); print(f.__name__, "tamam")
