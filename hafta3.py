"""Hafta 3 · Kesit ve Plan — Ders 3.1–3.4.
  python hafta3.py   → ekran/3.x/*.txt + *.png, cikti/*.dxf, OLCUMLER.json (d3_*)
Kafe planının ölçüleri (oda, duvar, kapı, masa, tezgâh) ÖRNEK'tir; bardağın yolu benzetim kaydından gelir."""
import numpy as np
from ortak import yeni, kaydet, dxf_ciz, oturum, olc, kayit
from arac import flans, flans_kesit, tutucu_yarim_kesit, dikdortgen, yazi, olcu_yatay, olcu_dikey, olcu_stil, FLANS, TUTUCU

# ÖRNEK kafe ölçüleri (mm)
ODA = dict(en=8000, boy=6000, duvar=200, kapi=900)
MASA, SANDALYE = 800, 450
MASALAR = [(4300, 3500), (6300, 3500), (4300, 1500), (6300, 1500)]
KAYDIRMA = (1000.0, 11500.0)   # benzetim dünyası (m) → plan (mm): (x − 1,0 m, y − 11,5 m) × 1000


def ders_3_1():
    f = FLANS
    doc = yeni(); msp = doc.modelspace()
    flans(msp, 0, 0)
    R = f["dis"] / 2
    msp.add_line((0, -R - 10), (0, R + 10), dxfattribs={"layer": "KESIT"})
    for y in (-R - 10, R + 10):
        msp.add_line((0, y), (8, y), dxfattribs={"layer": "GORUNEN"})
        yazi(msp, "A", 10, y - 2, boy=5)
    flans_kesit(msp, R + 40, 0)
    yazi(msp, "A–A", R + 44, R + 8, boy=5, hiza="CENTER")
    kaydet(doc, "flans_kesit")
    dxf_ciz(doc, "3.1", "flans-kesit", "Motor flanşı: kesme düzlemi A–A ve kesit görünüşü", "flans_kesit.dxf")
    ns = oturum("3.1", "kesit-alani", """
import ezdxf
doc = ezdxf.readfile("cikti/flans_kesit.dxf")
taramalar = doc.modelspace().query("HATCH")
len(taramalar)
def alan(noktalar):
    x = [p[0] for p in noktalar]; y = [p[1] for p in noktalar]
    return abs(sum(x[i] * y[i - 1] - x[i - 1] * y[i] for i in range(len(x)))) / 2
alanlar = [alan([v[:2] for v in h.paths[0].vertices]) for h in taramalar]
alanlar
sum(alanlar)
(45 - 15) * 8 * 2
""")
    doc = yeni(); msp = doc.modelspace()
    flans_kesit(msp, 0, 0, tara=False)
    yazi(msp, "taramasız", 4, f["dis"] / 2 + 8, boy=5, hiza="CENTER")
    flans_kesit(msp, 90, 0)
    yazi(msp, "taralı", 94, f["dis"] / 2 + 8, boy=5, hiza="CENTER")
    kaydet(doc, "kesit_karsilastirma")
    dxf_ciz(doc, "3.1", "kesit-karsilastirma", "Aynı kesit: taramasız ve taralı", "kesit_karsilastirma.dxf")
    olc(d3_1_tarama=len(ns["taramalar"]), d3_1_alanlar=ns["alanlar"], d3_1_toplam_alan=sum(ns["alanlar"]),
        d3_1_kalinlik=f["kalinlik"])


def ders_3_2():
    desen = [("ANSI31", "metal, genel"), ("ANSI37", "metal dışı"), ("AR-CONC", "beton"), ("EARTH", "toprak"), ("AR-B816", "tuğla duvar")]
    ns = oturum("3.2", "desen-listesi", """
from ezdxf.tools import pattern
iso = pattern.load(measurement=1)
len(iso)
desen = ["ANSI31", "ANSI37", "AR-CONC", "EARTH", "AR-B816"]
[d in iso for d in desen]
for d in desen:
    print(f"{d:8s} {len(iso[d])} çizgi ailesi")
""")
    doc = yeni(); msp = doc.modelspace()
    olcek = {"ANSI31": 1, "ANSI37": 1, "AR-CONC": 0.05, "EARTH": 1, "AR-B816": 0.03}
    for i, (d, ad) in enumerate(desen):
        x = i * 70
        p = [(x, 0), (x + 55, 0), (x + 55, 55), (x, 55)]
        msp.add_lwpolyline(p, close=True, dxfattribs={"layer": "GORUNEN"})
        h = msp.add_hatch(dxfattribs={"layer": "TARAMA"})
        h.set_pattern_fill(d, scale=olcek[d])
        h.paths.add_polyline_path(p, is_closed=True)
        yazi(msp, d, x + 27.5, -10, boy=5, hiza="CENTER")
        yazi(msp, ad, x + 27.5, -20, boy=4.5, hiza="CENTER")
    kaydet(doc, "desenler")
    dxf_ciz(doc, "3.2", "desenler", "Beş tarama deseni (DXF desen adları; malzeme eşlemesi ÖRNEK)", "desenler.dxf")
    doc = yeni(); msp = doc.modelspace()
    tutucu_yarim_kesit(msp, 0, 0)
    yazi(msp, "görünüş", -TUTUCU["dis"] / 4, TUTUCU["yukseklik"] + 6, boy=4, hiza="CENTER")
    yazi(msp, "kesit", TUTUCU["dis"] / 4, TUTUCU["yukseklik"] + 6, boy=4, hiza="CENTER")
    kaydet(doc, "tutucu_yarim_kesit")
    dxf_ciz(doc, "3.2", "tutucu-yarim-kesit", "Bardak tutucu: yarım kesit, kesilen duvar ve taban taralı", "tutucu_yarim_kesit.dxf")
    olc(d3_2_desen_sayisi=len(ns["iso"]), d3_2_desen=[d for d, _ in desen], d3_2_tarama_yarim=2)


def masa_bloklari(doc):
    m = doc.blocks.new("MASA")
    m.add_lwpolyline([(-MASA / 2, -MASA / 2), (MASA / 2, -MASA / 2), (MASA / 2, MASA / 2), (-MASA / 2, MASA / 2)], close=True,
                     dxfattribs={"layer": "0"})
    s = doc.blocks.new("SANDALYE")
    s.add_lwpolyline([(-SANDALYE / 2, -SANDALYE / 2), (SANDALYE / 2, -SANDALYE / 2), (SANDALYE / 2, SANDALYE / 2),
                      (-SANDALYE / 2, SANDALYE / 2)], close=True, dxfattribs={"layer": "0"})
    s.add_line((-SANDALYE / 2, SANDALYE / 2 - 80), (SANDALYE / 2, SANDALYE / 2 - 80), dxfattribs={"layer": "0"})


def masa_takimi(msp, x, y):
    msp.add_blockref("MASA", (x, y), dxfattribs={"layer": "MOBILYA"})
    for aci, (dx, dy) in ((0, (0, -650)), (180, (0, 650)), (270, (-650, 0)), (90, (650, 0))):
        msp.add_blockref("SANDALYE", (x + dx, y + dy), dxfattribs={"layer": "MOBILYA", "rotation": aci})


def ders_3_3():
    ns = oturum("3.3", "blok-tanimla", """
from ortak import yeni
from hafta3 import masa_bloklari, masa_takimi, MASALAR
doc = yeni()
katman = doc.layers.add("MOBILYA", color=30)
masa_bloklari(doc)
msp = doc.modelspace()
for x, y in MASALAR:
    masa_takimi(msp, x, y)
len(msp.query('INSERT[name=="MASA"]'))
len(msp.query('INSERT[name=="SANDALYE"]'))
len(doc.blocks.get("SANDALYE"))
doc.saveas("cikti/masalar.dxf")
""")
    dxf_ciz(ns["doc"], "3.3", "masalar", "Dört masa takımı: iki blok, yirmi yerleştirme (ÖRNEK ölçüler)", "masalar.dxf")
    ns2 = oturum("3.3", "blok-degistir", """
import ezdxf
doc = ezdxf.readfile("cikti/masalar.dxf")
masa = doc.blocks.get("MASA")
for e in list(masa):
    masa.delete_entity(e)
daire = masa.add_circle((0, 0), 400)
len(doc.modelspace().query('INSERT[name=="MASA"]'))
doc.saveas("cikti/masalar_yuvarlak.dxf")
""")
    dxf_ciz(ns2["doc"], "3.3", "masalar-yuvarlak", "Blok tanımı bir kez değişti, dört masa birden yuvarlak oldu", "masalar_yuvarlak.dxf")
    olc(d3_3_masa=len(ns["msp"].query('INSERT[name=="MASA"]')), d3_3_sandalye=len(ns["msp"].query('INSERT[name=="SANDALYE"]')),
        d3_3_masa_mm=MASA, d3_3_sandalye_mm=SANDALYE, d3_3_yuvarlak_cap=800)


def bardak_yolu(adim=25):
    k = kayit()
    x = (k["bardak_x_m"] - KAYDIRMA[0] / 1000) * 1000
    y = (k["bardak_y_m"] - KAYDIRMA[1] / 1000) * 1000
    return np.column_stack([x, y])[::adim], np.column_stack([x, y])


def kafe_plani(olculu=False):
    o = ODA
    doc = yeni(); doc.layers.add("MOBILYA", color=30); doc.layers.add("DUVAR", color=7, lineweight=70)
    doc.layers.add("YOL", color=6, lineweight=35)
    olcu_stil(doc, boy=150)
    for ad in ("EZDXF",):
        s = doc.dimstyles.get(ad); s.dxf.dimasz = 150; s.dxf.dimexe = 100; s.dxf.dimexo = 50; s.dxf.dimgap = 50
    masa_bloklari(doc)
    msp = doc.modelspace()
    d = o["duvar"]
    dis = [(-d, -d), (o["en"] + d, -d), (o["en"] + d, o["boy"] + d), (-d, o["boy"] + d)]
    ic = [(0, 0), (o["en"], 0), (o["en"], o["boy"]), (0, o["boy"])]
    msp.add_lwpolyline(dis, close=True, dxfattribs={"layer": "DUVAR"})
    msp.add_lwpolyline(ic, close=True, dxfattribs={"layer": "DUVAR"})
    h = msp.add_hatch(dxfattribs={"layer": "TARAMA"})
    h.set_pattern_fill("ANSI31", scale=20)
    h.paths.add_polyline_path(dis, is_closed=True, flags=1)
    h.paths.add_polyline_path(ic, is_closed=True, flags=16)
    # kapı: alt duvarda boşluk (taramada ada) ve kanat yayı
    kx = 2000
    h.paths.add_polyline_path([(kx, -d), (kx + o["kapi"], -d), (kx + o["kapi"], 0), (kx, 0)], is_closed=True, flags=16)
    msp.add_lwpolyline([(kx, -d), (kx + o["kapi"], -d), (kx + o["kapi"], 0), (kx, 0)], close=True,
                       dxfattribs={"layer": "GORUNEN", "color": 7})
    msp.add_arc((kx, 0), o["kapi"], 0, 90, dxfattribs={"layer": "GORUNEN"})
    msp.add_line((kx, 0), (kx, o["kapi"]), dxfattribs={"layer": "GORUNEN"})
    # tezgâh
    dikdortgen(msp, 0, 600, 600, 2000)
    yazi(msp, "TEZGÂH", 0, 2700, boy=150)
    for x, y in MASALAR:
        masa_takimi(msp, x, y)
    seyrek, _ = bardak_yolu()
    msp.add_lwpolyline(seyrek.tolist(), dxfattribs={"layer": "YOL"})
    msp.add_circle(seyrek[0].tolist(), 60, dxfattribs={"layer": "YOL"})
    msp.add_circle(seyrek[-1].tolist(), 60, dxfattribs={"layer": "YOL"})
    yazi(msp, "bardağın yolu (benzetim kaydı)", seyrek[-1][0] - 1800, seyrek[-1][1] + 900, boy=150)
    if olculu:
        olcu_yatay(msp, (-d, o["boy"] + d), (o["en"] + d, o["boy"] + d), o["boy"] + d + 600)
        olcu_dikey(msp, (o["en"] + d, -d), (o["en"] + d, o["boy"] + d), o["en"] + d + 600)
        olcu_yatay(msp, (kx, -d), (kx + o["kapi"], -d), -d - 500)
        olcu_yatay(msp, (0, o["boy"]), (o["en"], o["boy"]), o["boy"] - 400)
        yazi(msp, "KAT PLANI  ÖLÇEK 1:50", 0, -d - 1300, boy=250)
    return doc


def ders_3_4():
    doc = kafe_plani()
    kaydet(doc, "kafe_plani")
    dxf_ciz(doc, "3.4", "kafe-plani", "Kafe kat planı: duvarlar, kapı, tezgâh, masalar ve bardağın yolu", "kafe_plani.dxf")
    ns = oturum("3.4", "yol-ve-olcek", """
import numpy as np
from hafta3 import bardak_yolu, ODA
_, yol = bardak_yolu()
uzunluk_m = float(np.linalg.norm(np.diff(yol, axis=0), axis=1).sum()) / 1000
round(uzunluk_m, 2)
dogrusal_m = float(np.linalg.norm(yol[-1] - yol[0])) / 1000
round(dogrusal_m, 2)
kagitta = lambda mm, payda: mm / payda
kagitta(ODA["en"], 50), kagitta(ODA["boy"], 50)
kagitta(ODA["en"], 100), kagitta(ODA["boy"], 100)
round(kagitta(uzunluk_m * 1000, 50), 1)
""")
    doc = kafe_plani(olculu=True)
    kaydet(doc, "kafe_plani_olculu")
    dxf_ciz(doc, "3.4", "kafe-plani-olculu", "Kat planı ölçüleriyle: oda 8,0 × 6,0 m, kapı 0,9 m (ÖRNEK ölçüler)", "kafe_plani_olculu.dxf")
    uz = float(np.linalg.norm(np.diff(ns["yol"], axis=0), axis=1).sum() / 1000)
    dg = float(np.linalg.norm(ns["yol"][-1] - ns["yol"][0]) / 1000)
    olc(d3_4_yol_m=round(uz, 2), d3_4_dogrusal_m=round(dg, 2), d3_4_oran=round(uz / dg, 2),
        d3_4_oda_m=[ODA["en"] / 1000, ODA["boy"] / 1000], d3_4_duvar_mm=ODA["duvar"], d3_4_kapi_mm=ODA["kapi"],
        d3_4_kagit_1_50=[ODA["en"] / 50, ODA["boy"] / 50], d3_4_kagit_1_100=[ODA["en"] / 100, ODA["boy"] / 100],
        d3_4_yol_kagit_1_50_mm=round(uz * 1000 / 50, 1), d3_4_masa=len(MASALAR))


if __name__ == "__main__":
    for f in (ders_3_1, ders_3_2, ders_3_3, ders_3_4):
        f(); print(f.__name__, "tamam")
