"""Hafta 4 · Pafta ve Çıktı — Ders 4.1–4.4.
  python hafta4.py   → ekran/4.x/*.txt + *.png, cikti/*.dxf, *.pdf, *.png, OLCUMLER.json (d4_*)
Pafta kenar payları ve antet ölçüleri ÖRNEK'tir; A serisi kâğıt boyları ISO 216'dan, alan adları ISO 7200'den esinlenir."""
import matplotlib.pyplot as plt
from ezdxf.math import Matrix44
from ortak import yeni, kaydet, dxf_ciz, oturum, olc, ciz_ax, LAB, CIKTI
from arac import (flans, flans_kesit, pafta, antet, yazi, olcu_cap, olcu_dikey, olcu_stil, ANTET_ALAN, FLANS)
from hafta3 import kafe_plani


def kafe_paftasi():
    doc = kafe_plani()
    msp = doc.modelspace()
    m = Matrix44.scale(1 / 50) @ Matrix44.translate(60, 100, 0)
    for e in list(msp):
        e.transform(m)
    for h in msp.query("HATCH"):
        h.set_pattern_scale(0.025)   # çizgi aralığı ≈ 1,6 mm (taşınan desen ölçeklenmez)
    pafta(msp, 420, 297)
    alan = dict(ANTET_ALAN)
    alan.update({"Belge türü": "Kat planı", "Başlık": "Kafe yerleşimi", "Belge no": "TCD-KP-01", "Ölçek": "1:50",
                 "Sayfa": "1/1", "İzdüşüm": "plan"})
    antet(msp, 410, 10, list(alan.items()))
    return doc


def flans_paftasi(antetli=True):
    doc = yeni(); olcu_stil(doc); msp = doc.modelspace()
    pafta(msp, 297, 210)
    f = FLANS
    cx, cy = 95, 128
    flans(msp, cx, cy)
    olcu_cap(msp, (cx, cy), f["dis"] / 2, aci=200)
    olcu_cap(msp, (cx, cy), f["orta"] / 2, aci=-30)
    olcu_cap(msp, (cx, cy), f["bolum"] / 2, aci=110)
    R = f["dis"] / 2
    msp.add_line((cx, cy - R - 8), (cx, cy + R + 8), dxfattribs={"layer": "KESIT"})
    for y in (cy - R - 8, cy + R + 8):
        yazi(msp, "A", cx + 3, y - 1.5, boy=3.5)
    sx = 200
    flans_kesit(msp, sx, cy)
    olcu_dikey(msp, (sx, cy - R), (sx, cy + R), sx - 12)
    msp.add_linear_dim(base=(sx + 4, cy + R + 8), p1=(sx, cy + R), p2=(sx + f["kalinlik"], cy + R), angle=0,
                       dimstyle="EZDXF", dxfattribs={"layer": "OLCU"}).render()
    yazi(msp, "A–A", sx + 4, cy + R + 15, boy=3.5, hiza="CENTER")
    yazi(msp, "4 delik, çapı 6,6 mm, eşit aralıklı", 30, 66, boy=3)
    if antetli:
        alan = dict(ANTET_ALAN)
        alan.update({"Başlık": "Motor flanşı", "Belge no": "TCD-MF-01", "Ölçek": "1:1"})
        antet(msp, 287, 10, list(alan.items()))
    return doc


def ders_4_1():
    ns = oturum("4.1", "a-serisi", """
boylar = {}
en, boy = 841, 1189
for n in range(5):
    boylar[f"A{n}"] = (en, boy)
    en, boy = boy // 2, en
for ad, (e, b) in boylar.items():
    print(f"{ad}  {e:4d} × {b:4d} mm   oran {b / e:.3f}")
def kullanilir(e, b, sol=20, diger=10):
    return b - sol - diger, e - 2 * diger
kullanilir(*boylar["A3"])
plan = (8400 / 50, 6400 / 50)
plan
""")
    doc = yeni(); msp = doc.modelspace()
    pafta(msp, 420, 297)
    yazi(msp, "kâğıt kenarı 420 × 297 mm", 30, 265, boy=12)
    yazi(msp, "çizim çerçevesi: sol 20 mm, öteki kenarlar 10 mm (ÖRNEK)", 30, 245, boy=9)
    kaydet(doc, "a3_cerceve")
    dxf_ciz(doc, "4.1", "a3-cerceve", "A3 pafta: kâğıt kenarı ve çizim çerçevesi", "a3_cerceve.dxf")
    doc = kafe_paftasi()
    kaydet(doc, "kafe_paftasi")
    dxf_ciz(doc, "4.1", "kafe-paftasi", "Kafe kat planı A3 paftada, ölçek 1:50", "kafe_paftasi.dxf")
    olc(d4_1_boylar={k: list(v) for k, v in ns["boylar"].items()}, d4_1_a3_kullanilir=list(ns["kullanilir"](*ns["boylar"]["A3"])),
        d4_1_plan_kagit=list(ns["plan"]), d4_1_sol_pay=20, d4_1_diger_pay=10)


def ders_4_2():
    ns = oturum("4.2", "antet-alanlari", """
from arac import ANTET_ALAN
alan = dict(ANTET_ALAN)
alan.update({"Başlık": "Motor flanşı", "Belge no": "TCD-MF-01", "Ölçek": "1:1"})
for ad, deger in alan.items():
    print(f"{ad:11s} {deger}")
len(alan)
bos = [ad for ad, deger in alan.items() if not deger]
bos
""")
    doc = flans_paftasi()
    kaydet(doc, "flans_paftasi")
    # antetin yakın görünüşü: yalnız antet çizilir
    yakin = yeni(); antet(yakin.modelspace(), 287, 10, list(ns["alan"].items()))
    dxf_ciz(yakin, "4.2", "antet-yakin", "Antet: on alan, iki sütun (alan seçimi ISO 7200'e dayanır, ölçüler ÖRNEK)", "flans_paftasi.dxf")
    dxf_ciz(doc, "4.2", "flans-paftasi", "Motor flanşı paftası: A4 yatay, ölçek 1:1", "flans_paftasi.dxf")
    olc(d4_2_alan=len(ns["alan"]), d4_2_bos=ns["bos"], d4_2_antet_en=180, d4_2_antet_satir=10)


def disari_ver(doc, ad, en, boy, dpi=150):
    """Paftayı kâğıt boyunda çizer: 1 çizim birimi = 1 mm, PDF gerçek boyutta, PNG dpi çözünürlükte."""
    fig = plt.figure(figsize=(en / 25.4, boy / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ciz_ax(doc, ax)
    ax.set_xlim(0, en); ax.set_ylim(0, boy); ax.set_aspect("equal")
    fig.savefig(CIKTI / f"{ad}.pdf")
    fig.savefig(CIKTI / f"{ad}.png", dpi=dpi, facecolor="white")
    plt.close(fig)


def ders_4_3():
    doc = flans_paftasi()
    disari_ver(doc, "flans_paftasi", 297, 210)
    ns = oturum("4.3", "disari-ver", """
import re, pathlib
from PIL import Image
from hafta4 import flans_paftasi, disari_ver
disari_ver(flans_paftasi(), "flans_paftasi", 297, 210)
pdf = pathlib.Path("cikti/flans_paftasi.pdf").read_bytes()
kutu = [float(x) for x in re.search(rb"/MediaBox \\[ *([\\d. ]+)\\]", pdf).group(1).split()]
kutu
[round(kutu[2] / 72 * 25.4), round(kutu[3] / 72 * 25.4)]
boyut = Image.open("cikti/flans_paftasi.png").size
boyut
round(boyut[0] / (297 / 25.4))
""")
    from PIL import Image
    im = Image.open(CIKTI / "flans_paftasi.png")
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.text(0.016, 0.962, "PDF'le aynı sayfanın PNG çıktısı (150 nokta / inç)", fontsize=26, va="center", color="white")
    fig.text(0.984, 0.962, "Gerçek koşum çıktısı · flans_paftasi.png", fontsize=19, va="center", ha="right", color="#c7d7ea")
    fig.patches.append(plt.Rectangle((0, 0.925), 1, 0.075, transform=fig.transFigure, fc="#1f2a37", zorder=0))
    ax = fig.add_axes([0.03, 0.02, 0.94, 0.88]); ax.imshow(im); ax.axis("off")
    (LAB / "ekran/4.3").mkdir(parents=True, exist_ok=True)
    fig.savefig(LAB / "ekran/4.3/png-cikti.png", dpi=100); plt.close(fig)
    disari_ver(kafe_paftasi(), "kafe_paftasi", 420, 297)
    ns3 = oturum("4.3", "dosyalar", """
import pathlib
for yol in sorted(pathlib.Path("cikti").glob("*_paftasi.*")):
    print(f"{yol.name:20s} {yol.stat().st_size / 1024:7.0f} kB")
""")
    boyut = {p.name: round(p.stat().st_size / 1024) for p in sorted(CIKTI.glob("*_paftasi.*"))}
    olc(d4_3_dosya_kb=boyut)
    olc(d4_3_pdf_mm=[round(ns["kutu"][2] / 72 * 25.4), round(ns["kutu"][3] / 72 * 25.4)], d4_3_png_px=list(im.size), d4_3_dpi=150)


def ders_4_4():
    kaydet(flans_paftasi(), "flans_paftasi")
    ns = oturum("4.4", "denetim", """
import ezdxf
doc = ezdxf.readfile("cikti/flans_paftasi.dxf")
rapor = doc.audit()
len(rapor.errors), len(rapor.fixes)
from collections import Counter
katman = Counter(e.dxf.layer for e in doc.modelspace())
dict(katman)
katman["0"]
yazilar = [t.dxf.text for t in doc.modelspace().query("TEXT")]
"1:1" in yazilar, "Motor flanşı" in yazilar
len(doc.modelspace().query("DIMENSION"))
""")
    eksik = yeni(); olcu_stil(eksik); m = eksik.modelspace()
    flans(m, 0, 0); m.add_circle((0, 0), 20)   # katmansız (0 katmanında) fazladan bir daire
    kaydet(eksik, "flans_hatali")
    ns2 = oturum("4.4", "hatali-dosya", """
import ezdxf
from collections import Counter
doc = ezdxf.readfile("cikti/flans_hatali.dxf")
katman = Counter(e.dxf.layer for e in doc.modelspace())
katman["0"]
len(doc.modelspace().query("DIMENSION")), len(doc.modelspace().query("TEXT"))
""")
    dxf_ciz(flans_paftasi(), "4.4", "son-pafta", "Teslime hazır pafta: çerçeve, iki görünüş, ölçüler, antet", "flans_paftasi.dxf")
    olc(d4_4_hata=len(ns["rapor"].errors), d4_4_duzeltme=len(ns["rapor"].fixes), d4_4_katman=dict(ns["katman"]),
        d4_4_katman0=ns["katman"]["0"], d4_4_olcu=len(ns["doc"].modelspace().query("DIMENSION")),
        d4_4_hatali_katman0=ns2["katman"]["0"])


if __name__ == "__main__":
    for f in (ders_4_1, ders_4_2, ders_4_3, ders_4_4):
        f(); print(f.__name__, "tamam")
