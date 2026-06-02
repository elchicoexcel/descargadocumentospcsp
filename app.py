import io
import os
import re
import time
import zipfile
import mimetypes
from datetime import datetime
from urllib.parse import urljoin, urlparse, quote_plus

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template, request, send_file, Response

app = Flask(__name__)

BASE = "https://contrataciondelestado.es"
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
})
TIMEOUT = 30

BAD_URL_PARTS = [
    "contenthandler", "mashup/ra:collection", "deferred=true", "themeid=", "wp_", "st_skin",
    ".js", "javascript", ".css", "favicon", "analytics", "googletag", "cookie", "captcha"
]
DOC_WORDS = [
    "documento", "documentos", "doc", "fichero", "ficheros", "download", "descarga", "descargar", "getfile", "getdocument", "verdocumento",
    "anexo", "pliego", "prescripciones", "clausulas", "deuc", "memoria", "informe", "acta", "anuncio", "pcap", "ppt", "oferta"
]
EXTS = {"pdf", "xml", "doc", "docx", "xls", "xlsx", "odt", "ods", "csv", "zip", "rar", "7z", "txt", "html", "htm"}
CONTENT_EXT = {
    "application/pdf": "pdf",
    "application/xml": "xml",
    "text/xml": "xml",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/vnd.ms-excel": "xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "application/zip": "zip",
    "text/csv": "csv",
    "text/html": "html",
}


def clean_text(s):
    return re.sub(r"\s+", " ", s or "").strip()


def safe_filename(name, fallback="documento"):
    name = clean_text(name) or fallback
    name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", name)
    name = re.sub(r"\s+", " ", name).strip(" ._")
    return (name[:110] or fallback)


def absolute_url(href, base_url):
    if not href:
        return ""
    href = href.strip()
    if href.startswith("javascript:") or href.startswith("#") or href.lower().startswith("mailto:"):
        return ""
    return urljoin(base_url, href)


def url_ext(url):
    try:
        path = urlparse(url).path.lower()
        m = re.search(r"\.([a-z0-9]{2,5})$", path)
        if m and m.group(1) in EXTS:
            return m.group(1)
    except Exception:
        pass
    return ""


def is_bad_url(url):
    u = (url or "").lower()
    return any(p in u for p in BAD_URL_PARTS)


def looks_like_doc(url, text):
    u = (url or "").lower()
    t = (text or "").lower()
    if is_bad_url(u):
        return False
    if url_ext(u):
        return True
    if any(w in u for w in DOC_WORDS):
        return True
    if any(w in t for w in DOC_WORDS):
        return True
    return False


def fetch(url, stream=False):
    r = SESSION.get(url, timeout=TIMEOUT, allow_redirects=True, stream=stream)
    r.raise_for_status()
    return r


def detect_filename_and_ext(url, response=None, name_hint="Documento"):
    filename = ""
    ext = url_ext(url)
    ctype = ""
    if response is not None:
        cd = response.headers.get("Content-Disposition", "")
        m = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)', cd, re.I)
        if m:
            filename = requests.utils.unquote_header_value(m.group(1)).strip()
        ctype = (response.headers.get("Content-Type", "") or "").split(";")[0].strip().lower()
        if not ext and ctype in CONTENT_EXT:
            ext = CONTENT_EXT[ctype]
    if not filename:
        parsed = urlparse(url)
        base = os.path.basename(parsed.path)
        if base and "." in base and len(base) < 120:
            filename = base
    if not ext:
        ext = "bin"
    if not filename:
        filename = safe_filename(name_hint or "Documento") + "." + ext
    if "." not in os.path.basename(filename) and ext:
        filename += "." + ext
    base_name = safe_filename(os.path.splitext(filename)[0] or name_hint)
    return base_name, ext


def extract_exp_info(soup, source_url, exp_hint=""):
    text = clean_text(soup.get_text(" "))
    title = ""
    for sel in ["h1", "h2", ".titulo", "[class*=titulo]", "title"]:
        el = soup.select_one(sel)
        if el:
            title = clean_text(el.get_text(" "))[:250]
            if title:
                break
    numero = exp_hint
    patterns = [
        r"(?:N[úu]mero\s+de\s+expediente|Expediente)\s*[:：]?\s*([A-Z0-9][A-Z0-9/_.\- ]{2,60})",
        r"(?:Expte\.?|Nº\s*Expediente)\s*[:：]?\s*([A-Z0-9][A-Z0-9/_.\- ]{2,60})",
    ]
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            numero = clean_text(m.group(1)).split(" Órgano")[0].strip()
            break
    importe = ""
    m = re.search(r"\d[\d\.]*,\d{2}\s*€", text)
    if m:
        importe = m.group(0)
    fecha = ""
    m = re.search(r"\d{2}[/-]\d{2}[/-]\d{4}", text)
    if m:
        fecha = m.group(0)
    organo = ""
    m = re.search(r"Órgano\s+de\s+Contratación\s*[:：]?\s*(.{3,120}?)(?:Objeto|Estado|Importe|Fecha|Expediente|$)", text, re.I)
    if m:
        organo = clean_text(m.group(1))
    tipo = "Contrato menor" if re.search(r"contrato\s+menor", text, re.I) else "Licitación"
    estado = "Disponible"
    for k in ["Anulado", "Adjudicado", "Publicado", "Resuelto", "En plazo", "Cerrado"]:
        if re.search(k, text, re.I):
            estado = k
            break
    return {"numero": numero or "Expediente", "titulo": title or "Título no disponible", "organo": organo, "importe": importe, "fecha": fecha, "tipo": tipo, "estado": estado, "url": source_url}


def section_for_anchor(a):
    for parent in list(a.parents)[:8]:
        header = parent.find(["h1", "h2", "h3", "h4", "caption", "th"])
        if header:
            txt = clean_text(header.get_text(" "))
            if txt and len(txt) < 90:
                return txt
    return "Documentos"


def extract_documents(html, source_url):
    soup = BeautifulSoup(html, "html.parser")
    docs = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a.get("href")
        full = absolute_url(href, source_url)
        text = clean_text(a.get_text(" "))
        if not full or not looks_like_doc(full, text):
            continue
        key = full.split("#")[0]
        if key in seen:
            continue
        seen.add(key)
        row = a.find_parent("tr") or a.find_parent("li") or a.parent
        row_text = clean_text(row.get_text(" ")) if row else text
        date = ""
        m = re.search(r"\d{2}[/-]\d{2}[/-]\d{4}", row_text)
        if m:
            date = m.group(0)
        status = "Disponible"
        if re.search(r"anulad", row_text, re.I):
            status = "Anulado"
        elif re.search(r"publicad|vigente|activo|disponible", row_text, re.I):
            status = "Publicado"
        ext = url_ext(full) or "bin"
        name = text or os.path.basename(urlparse(full).path) or "Documento"
        # Improve names for common tiny labels
        if len(name) < 4 or name.lower() in {"ver", "pdf", "xml", "doc", "descargar", "download"}:
            name = row_text[:120] or name
        docs.append({
            "id": f"d{len(docs)+1}", "name": safe_filename(name, "Documento"), "ext": ext,
            "date": date, "status": status, "section": section_for_anchor(a), "url": full
        })
    return docs


def enrich_docs(docs, max_head=30):
    enriched = []
    for d in docs:
        nd = dict(d)
        if nd.get("ext") == "bin" or not nd.get("name") or nd["name"].lower().startswith("documento"):
            try:
                r = SESSION.head(nd["url"], timeout=12, allow_redirects=True)
                if r.status_code >= 400 or not r.headers:
                    r = SESSION.get(nd["url"], timeout=12, allow_redirects=True, stream=True)
                base, ext = detect_filename_and_ext(nd["url"], r, nd.get("name", "Documento"))
                if ext != "html" or "document" in nd["url"].lower() or "fichero" in nd["url"].lower():
                    nd["ext"] = ext
                if base and not base.lower().startswith("contenthandler"):
                    nd["name"] = base
            except Exception:
                pass
        enriched.append(nd)
        if len(enriched) >= max_head:
            # still include rest without HEAD
            enriched.extend(docs[len(enriched):])
            break
    return enriched


def find_detail_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        text = clean_text(a.get_text(" ")).lower()
        full = absolute_url(a.get("href"), base_url)
        low = full.lower()
        if not full or is_bad_url(low):
            continue
        if any(x in low for x in ["detalle", "resultado/detalle", "licitacion", "expediente"]) or any(x in text for x in ["detalle", "ver", "expediente"]):
            links.append(full)
    # unique, prioritize detalle
    out = []
    for l in sorted(set(links), key=lambda u: ("detalle" not in u.lower(), len(u))):
        if l not in out:
            out.append(l)
    return out[:10]


def candidate_search_urls(exp):
    q = quote_plus(exp)
    return [
        f"{BASE}/wps/portal/plataforma/buscar/resultado?numExpediente={q}",
        f"{BASE}/wps/portal/plataforma/buscar/resultado?numExpediente={q}&tipoBusqueda=licitaciones",
        f"{BASE}/wps/portal/plataforma/buscar/resultado?numExpediente={q}&tipoBusqueda=contratosmenores",
        f"{BASE}/wps/portal/plataforma/buscar?numeroExpediente={q}",
    ]


def analyze_url(url, exp_hint=""):
    r = fetch(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    docs = extract_documents(html, r.url)
    if len(docs) <= 1:
        for detail in find_detail_links(html, r.url):
            try:
                rr = fetch(detail)
                dd = extract_documents(rr.text, rr.url)
                if len(dd) > len(docs):
                    html = rr.text
                    soup = BeautifulSoup(html, "html.parser")
                    docs = dd
                    url = rr.url
                    break
            except Exception:
                continue
    docs = [d for d in docs if not is_bad_url(d.get("url", ""))]
    docs = enrich_docs(docs)
    info = extract_exp_info(soup, url, exp_hint)
    return info, docs


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/url")
def api_url():
    url = request.args.get("url", "").strip()
    if not url.startswith("http"):
        return jsonify(error="URL no válida"), 400
    try:
        info, docs = analyze_url(url)
        return jsonify(expediente=info, documents=docs)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/api/search")
def api_search():
    exp = request.args.get("exp", "").strip()
    if not exp:
        return jsonify(error="Falta número de expediente"), 400
    last_error = None
    best_info, best_docs = None, []
    for url in candidate_search_urls(exp):
        try:
            info, docs = analyze_url(url, exp)
            if len(docs) > len(best_docs):
                best_info, best_docs = info, docs
            if docs:
                return jsonify(expediente=info, documents=docs)
        except Exception as e:
            last_error = e
    if best_info:
        return jsonify(expediente=best_info, documents=best_docs)
    return jsonify(error=f"No se encontraron documentos para el expediente. {last_error or ''}"), 404


def download_bytes(url):
    r = fetch(url, stream=True)
    data = r.content
    base, ext = detect_filename_and_ext(r.url, r, "Documento")
    ctype = r.headers.get("Content-Type", mimetypes.guess_type("x." + ext)[0] or "application/octet-stream")
    return data, base, ext, ctype


@app.route("/api/download")
def api_download():
    url = request.args.get("url", "").strip()
    filename = request.args.get("filename", "").strip()
    if not url.startswith("http"):
        return jsonify(error="URL de documento no válida"), 400
    try:
        data, base, ext, ctype = download_bytes(url)
        if filename:
            out = safe_filename(os.path.splitext(filename)[0])
            ext2 = url_ext(filename) or ext
        else:
            out, ext2 = base, ext
        final = out if out.lower().endswith("." + ext2.lower()) else f"{out}.{ext2}"
        return send_file(io.BytesIO(data), mimetype=ctype, as_attachment=True, download_name=final)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/api/zip", methods=["POST"])
def api_zip():
    payload = request.get_json(force=True, silent=True) or {}
    exp = payload.get("expediente") or {}
    docs = payload.get("documents") or []
    if not docs:
        return jsonify(error="No hay documentos seleccionados"), 400
    zbuf = io.BytesIO()
    used = {}
    errors = []
    with zipfile.ZipFile(zbuf, "w", zipfile.ZIP_DEFLATED) as z:
        for d in docs:
            url = d.get("url", "")
            if not url.startswith("http"):
                continue
            try:
                data, base, ext, ctype = download_bytes(url)
                name_hint = d.get("name") or base or "Documento"
                fname_base = safe_filename(os.path.splitext(name_hint)[0] or base)
                fname = fname_base if fname_base.lower().endswith("." + ext) else f"{fname_base}.{ext}"
                if fname in used:
                    used[fname] += 1
                    stem, ex = os.path.splitext(fname)
                    fname = f"{stem}_{used[fname]}{ex}"
                else:
                    used[fname] = 1
                z.writestr(fname, data)
            except Exception as e:
                errors.append(f"{d.get('name','Documento')}: {e}")
        if errors:
            z.writestr("_errores_descarga.txt", "\n".join(errors))
    zbuf.seek(0)
    expnum = safe_filename(exp.get("numero") or "expediente", "expediente")
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    return send_file(zbuf, mimetype="application/zip", as_attachment=True, download_name=f"{expnum}_{stamp}.zip")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
