"""Teknik Çizim ve DXF: Parçadan Paftaya — lab ortak araçları.
Çizimler ezdxf ile DXF dosyası olarak yazılır (AutoCAD'de ve öteki CAD programlarında açılabilen açık biçim),
ardından ezdxf'in çizim eklentisi ve Matplotlib ile PNG / PDF'e çevrilir.
Veri: veri/cay_servisi_kaydi.csv (insansı robotun kafede çay servisi BENZETİM KAYDI, saniyede 50 örnek) ve
veri/sag_kol_parametre.csv (sağ kol eklem sınırları, benzetim parametre dosyası). Bunlardan ya da kaynaklar.py'deki
standartlardan gelmeyen her ölçü ÖRNEK'tir.

  oturum(ders, ad, kod)        : kodu Python etkileşimli oturumu gibi çalıştırır → ekran/<ders>/<ad>.txt
  dxf_ciz(doc, ders, ad, ...)  : DXF'i PNG'ye çizer → ekran/<ders>/<ad>.png ("Gerçek koşum çıktısı" etiketiyle)
  olc(anahtar=değer)           : ölçümü OLCUMLER.json'a yazar (derslerdeki bütün sayılar buradan gelir)
"""
import ast, contextlib, io, json, os, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, LineweightPolicy

LAB = pathlib.Path(__file__).resolve().parent
OLC = LAB / "OLCUMLER.json"
CIKTI = LAB / "cikti"
CIKTI.mkdir(exist_ok=True)
os.chdir(LAB)   # oturumlardaki göreli yollar (cikti/…) lab klasörüne göredir
np.set_printoptions(precision=2, suppress=True, linewidth=88)
plt.rcParams.update({"font.size": 22, "font.family": "DejaVu Sans"})

# Katman düzeni (adlar Türkçe; çizgi türü adları DXF'in standart adları)
KATMAN = {
    "GORUNEN": dict(color=7, linetype="CONTINUOUS", lineweight=50),
    "EKSEN":   dict(color=1, linetype="CENTER",     lineweight=25),
    "GIZLI":   dict(color=5, linetype="DASHED",     lineweight=25),
    "OLCU":    dict(color=94, linetype="CONTINUOUS", lineweight=18),
    "TARAMA":  dict(color=8, linetype="CONTINUOUS", lineweight=18),
    "YAZI":    dict(color=7, linetype="CONTINUOUS", lineweight=25),
    "KESIT":   dict(color=1, linetype="DASHDOT",    lineweight=35),
    "CERCEVE": dict(color=7, linetype="CONTINUOUS", lineweight=70),
}


def yeni(katmanlar=True):
    """Milimetre birimli yeni DXF belgesi; standart çizgi türleri ve kurs katmanları hazır."""
    doc = ezdxf.new("R2018", setup=True, units=4)   # units=4: milimetre
    doc.header["$LTSCALE"] = 1.0
    doc.header["$LWDISPLAY"] = 1
    if katmanlar:
        for ad, ozellik in KATMAN.items():
            doc.layers.add(ad, **ozellik)
    return doc


def kaydet(doc, ad):
    yol = CIKTI / f"{ad}.dxf"
    doc.saveas(yol)
    return yol


def parametre():
    """Sağ kol eklem parametreleri (benzetim parametre dosyası): ad → sözlük."""
    d = np.genfromtxt(LAB / "veri/sag_kol_parametre.csv", delimiter=",", names=True, dtype=None, encoding="utf-8")
    return {str(r["ad"]): {k: r[k] for k in d.dtype.names} for r in d}


def kayit():
    d = np.genfromtxt(LAB / "veri/cay_servisi_kaydi.csv", delimiter=",", names=True)
    return {k: d[k] for k in d.dtype.names}


def _j(v):
    if isinstance(v, np.ndarray):
        return [_j(x) for x in v.tolist()]
    if isinstance(v, (list, tuple)):
        return [_j(x) for x in v]
    if isinstance(v, dict):
        return {k: _j(x) for k, x in v.items()}
    if isinstance(v, (float, np.floating)):
        return round(float(v), 4)
    if isinstance(v, (np.integer,)):
        return int(v)
    return v


def olc(**kw):
    d = json.loads(OLC.read_text()) if OLC.exists() else {}
    d.update({k: _j(v) for k, v in kw.items()})
    OLC.write_text(json.dumps(d, ensure_ascii=False, indent=1))


def oturum(ders, ad, kod, ns=None):
    """Kodu etkileşimli Python oturumu gibi çalıştırır: ifadenin değeri yazdırılır, atama sessizdir."""
    ns = {} if ns is None else ns
    ns.setdefault("__name__", "__oturum__")
    kod = kod.strip("\n")
    agac = ast.parse(kod)
    satirlar = kod.splitlines()
    out = []
    for st in agac.body:
        parca = satirlar[st.lineno - 1: st.end_lineno]
        out.append(">>> " + parca[0])
        out += ["... " + l for l in parca[1:]]
        if len(parca) > 1:
            out.append("...")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            if isinstance(st, ast.Expr):
                v = eval(compile(ast.Expression(st.value), "<oturum>", "eval"), ns)
                if v is not None:
                    print(repr(v))
            else:
                exec(compile(ast.Module([st], []), "<oturum>", "exec"), ns)
        out += buf.getvalue().rstrip("\n").splitlines() if buf.getvalue() else []
    yol = LAB / "ekran" / ders / f"{ad}.txt"
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text("\n".join(out) + "\n", encoding="utf-8")
    return ns


def ciz_ax(doc, ax, layout=None):
    """DXF'i Matplotlib eksenine çizer (beyaz zemin, çizgi kalınlıkları gerçek)."""
    cfg = Configuration(background_policy=BackgroundPolicy.WHITE, lineweight_policy=LineweightPolicy.ABSOLUTE,
                        lineweight_scaling=1.6)
    ctx = RenderContext(doc)
    Frontend(ctx, MatplotlibBackend(ax, adjust_figure=False), config=cfg).draw_layout(layout or doc.modelspace(), finalize=False)
    ax.set_aspect("equal", adjustable="datalim")
    ax.autoscale()
    ax.margins(0.04)
    ax.axis("off")


def dxf_ciz(doc, ders, ad, baslik, dosya=None):
    """DXF'i 1920 × 1080 PNG'ye çizer; üst şeritte 'Gerçek koşum çıktısı' ve dosya adı yazar."""
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0.03, 0.03, 0.94, 0.80])
    ciz_ax(doc, ax)
    ax.set_facecolor("white")
    fig.patches.append(matplotlib.patches.Rectangle((0, 0.925), 1, 0.075, transform=fig.transFigure, fc="#1f2a37", zorder=0))
    fig.text(0.016, 0.962, baslik, color="white", fontsize=26, va="center", ha="left")
    fig.text(0.984, 0.962, f"Gerçek koşum çıktısı · {dosya or ad + '.dxf'}", color="#c7d7ea", fontsize=19, va="center", ha="right")
    fig.text(0.016, 0.885, "ezdxf → Matplotlib · ders " + ders, color="#6B7280", fontsize=17, va="center", ha="left")
    yol = LAB / "ekran" / ders / f"{ad}.png"
    yol.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(yol, dpi=100, facecolor="white")
    plt.close(fig)
    return yol


def tr(x, basamak=1):
    return f"{x:.{basamak}f}".replace(".", ",")
