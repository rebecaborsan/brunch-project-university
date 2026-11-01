from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.shortcuts import render
from django.http import Http404
from django.utils.html import format_html


DESCRIERE = (
    "Brunch & Bloom este un site comercial dedicat unui local de brunch, care va "
    "oferi spre vânzare preparate pentru late breakfast, precum ouă Benedict, "
    "toasturi cu avocado, clătite și boluri cu iaurt și fructe, alături de cafea, "
    "ceai și sucuri naturale. Platforma va permite consultarea meniului și "
    "filtrarea produselor după categorie, preț și opțiuni vegetariene. Fiecare "
    "preparat va avea o descriere, ingrediente, alergeni, gramaj și preț. "
    "Utilizatorii își vor putea crea un cont, adăuga produse în coș, plasa "
    "comenzi pentru ridicare din local și adăuga recenzii produselor cumpărate. "
    "Administratorul va putea gestiona produsele, categoriile, prețurile, "
    "disponibilitatea preparatelor și comenzile."
)
ZILE = ("Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică")
LUNI = (
    "Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie",
    "Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie",
)
FORMAT_DATA = "%A, %-d %B %Y"


def formateaza_data(data, format=FORMAT_DATA):
    """Scrie data in romana, indiferent de limba calculatorului."""
    valori = {
        "A": ZILE[data.weekday()], "a": ZILE[data.weekday()][:3],
        "B": LUNI[data.month - 1], "b": LUNI[data.month - 1][:3],
    }
    rezultat = []
    i = 0
    while i < len(format):
        if format[i] != "%" or i + 1 == len(format):
            rezultat.append(format[i])
            i += 1
            continue
        if format[i:i + 3] == "%-d":
            rezultat.append(str(data.day))
            i += 3
            continue
        cod = format[i + 1]
        rezultat.append(valori[cod] if cod in valori else data.strftime("%" + cod))
        i += 2
    return "".join(rezultat)


class Accesare:
    ultimul_id = 0

    def __init__(self, ip_client, url, parametri=None):
        Accesare.ultimul_id += 1
        self.id = Accesare.ultimul_id
        self.ip_client = ip_client
        self.url = url
        # Fiecare accesare are propriul dictionar de parametri.
        self.parametri = dict(parametri) if parametri is not None else {}
        self.data = datetime.now(ZoneInfo(settings.TIME_ZONE))

    def lista_parametri(self):
        return [(nume, valoare if valoare != "" else None)
                for nume, valoare in self.parametri.items()]

    def string_url(self):
        return self.url

    def pagina(self):
        from urllib.parse import urlsplit
        return urlsplit(self.url).path or "/"

    def calculeaza_data(self, format=FORMAT_DATA, data=""):
        if data == "zi":
            text = formateaza_data(self.data, "%-d %B %Y")
        elif data == "timp":
            text = formateaza_data(self.data, "%H:%M:%S")
        else:
            text = formateaza_data(self.data, format)
            if format == FORMAT_DATA:
                text += " - " + formateaza_data(self.data, "%H:%M:%S")
        return format_html('<section><h2>Data și ora</h2><p>{}</p></section>', text)

    def __str__(self):
        return (
            f"id: {self.id}\nip_client: {self.ip_client}\n"
            f"string_url: {self.string_url()}\npagina: {self.pagina()}\n"
            f"calculeaza_data: {self.calculeaza_data()}\n"
            f"lista_parametri: {self.lista_parametri()}"
        )


ACCESARI = []


def inregistreaza_accesare(request):
    parametri = {}
    for nume in request.GET:
        valori = request.GET.getlist(nume)
        parametri[nume] = valori if len(valori) > 1 else valori[0]
    accesare = Accesare(request.ip_client, request.build_absolute_uri(), parametri)
    ACCESARI.append(accesare)
    print(str(accesare))
    return accesare


def index(request):
    inregistreaza_accesare(request)
    return render(request, "brunch/index.html", {"descriere": DESCRIERE})


def info(request):
    accesare = inregistreaza_accesare(request)
    mod = request.GET.get("data", "")
    return render(request, "brunch/info.html", {
        "sectiune_data": accesare.calculeaza_data(data=mod),
        "mod": mod,
    })


PAGINI = {
    "/": "Pagina principală", "/info": "Informații despre server",
    "/log": "Jurnalul accesărilor", "/despre": "Despre noi", "/istoric": "Istoric",
    "/produse": "Produse", "/contact": "Contact", "/cos_virtual": "Coș virtual",
    "/meniu_sezon": "Meniu de sezon", "/evenimente": "Evenimente",
}
CAMPURI = ["id", "ip_client", "url", "parametri", "data"]


def log(request):
    inregistreaza_accesare(request)
    selectate = list(ACCESARI)
    erori = []

    if "iduri" in request.GET:
        selectate = []
        iduri_afisate = set()
        dupa_id = {accesare.id: accesare for accesare in ACCESARI}
        for grup in request.GET.getlist("iduri"):
            for valoare in grup.split(","):
                try:
                    id_accesare = int(valoare.strip())
                except ValueError:
                    erori.append("ID invalid: " + valoare)
                    continue
                if id_accesare not in dupa_id:
                    erori.append(f"Nu există accesarea cu ID-ul {id_accesare}.")
                elif request.GET.get("dubluri", "false") == "true" or id_accesare not in iduri_afisate:
                    selectate.append(dupa_id[id_accesare])
                    iduri_afisate.add(id_accesare)

    if "ultimele" in request.GET:
        try:
            n = int(request.GET["ultimele"])
            if n < 0:
                raise ValueError
        except ValueError:
            erori.append("Parametrul ultimele trebuie să fie un număr întreg nenegativ.")
            selectate = []
        else:
            k = len(ACCESARI)
            if n > k:
                erori.append(f"Exista doar {k} accesari fata de {n} accesari cerute")
            # Pastram ordinea ceruta de iduri, daca sunt folositi ambii parametri.
            ultimele_iduri = {a.id for a in ACCESARI[-n:]} if n else set()
            selectate = [a for a in selectate if a.id in ultimele_iduri]

    coloane = []
    if "tabel" in request.GET:
        valoare = request.GET["tabel"]
        cerute = CAMPURI if valoare == "tot" else valoare.split(",")
        for nume in cerute:
            nume = nume.strip()
            if nume not in CAMPURI:
                erori.append("Proprietate necunoscută: " + nume)
            elif nume not in coloane:
                coloane.append(nume)

    randuri = []
    for accesare in selectate:
        valori = []
        for camp in coloane:
            valoare = getattr(accesare, camp)
            if camp == "data":
                valoare = formateaza_data(valoare, "%A, %-d %B %Y %H:%M:%S")
            valori.append(valoare)
        randuri.append({"id": accesare.id, "valori": valori})

    # Numaram toate paginile, inclusiv cele care nu au fost accesate inca.
    numarari = {cale: 0 for cale in PAGINI}
    for accesare in ACCESARI:
        cale = accesare.pagina()
        numarari[cale] = numarari.get(cale, 0) + 1
    minim, maxim = min(numarari.values()), max(numarari.values())
    putine = [PAGINI.get(cale, cale) for cale, nr in numarari.items() if nr == minim]
    multe = [PAGINI.get(cale, cale) for cale, nr in numarari.items() if nr == maxim]
    detalii = [{"id": a.id, "moment": formateaza_data(a.data, "%A, %-d %B %Y %H:%M:%S")}
               for a in selectate]
    return render(request, "brunch/log.html", {
        "accesari": selectate, "erori": erori, "coloane": coloane, "randuri": randuri,
        "mod": request.GET.get("accesari", ""), "detalii": detalii,
        "total": len(ACCESARI), "parametri": list(request.GET),
        "nr_parametri": sum(len(request.GET.getlist(nume)) for nume in request.GET),
        "putine": putine, "multe": multe, "minim": minim, "maxim": maxim,
    })


def detaliu_accesare(request, id):
    inregistreaza_accesare(request)
    for accesare in ACCESARI:
        if accesare.id == int(id):
            return render(request, "brunch/accesare.html", {"accesare": accesare})
    raise Http404("Accesarea cerută nu există în sesiunea curentă.")


def despre(request):
    inregistreaza_accesare(request)
    return render(request, "brunch/despre.html")


def istoric(request):
    inregistreaza_accesare(request)
    return render(request, "brunch/istoric.html")


def in_lucru(request):
    inregistreaza_accesare(request)
    return render(request, "brunch/in_lucru.html")
