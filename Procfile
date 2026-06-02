import io
import os
import re
import zipfile
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs, quote_plus

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template, request, send_file

app = Flask(__name__)

BASE = "https://contrataciondelestado.es"
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.6",
})

EXT_RE = re.compile(r"\.(pdf|xml|html?|docx?|xlsx?|zip|rar|odt|ods|csv|txt|rtf)(?:[?#].*)?$", re.I)
DATE_RE = re.compile(r"\b\d{2}[/-]\d{2}[/-]\d{4}\b")
BAD_URL_PARTS = [
    "/wps/contenthandler/", "/mashup/", "mime-type=text%2fjavascript", "mime-type=text/javascript",
    ".js", ".css", "javascript", "deferred=true", "themeid=", "config_js", "skin_", "wp_"
]
DOC_URL_PARTS = [
    "getdocumentbyidservlet", "getdocument", "getdocumento", "download", "descarga", "fichero",
    "documento", "docservlet", "export", "attachment"
]
CONTENT_TYPE_EXT = {
    "application/pdf": "pdf",
    "application/xml": "xml", "text/xml": "xml",
    "text/html": "html",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/vnd.ms-excel": "xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "application/zip": "zip",
    "application/x-zip-compressed": "zip",
    "text/csv": "csv",
    "text/plain": "txt",
    "application/rtf": "rtf",
}


def clean(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


def safe_name(name):
    name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", name or "documento").strip(" ._")
    return (name[:140] or "documento")


def fetch(url, binary=False):
    if not url.lower().startswith(("http://", "https://")):
        raise ValueError("URL no válida")
    r = SESSION.get(url, timeout=45, allow_redirects=True)
    r.raise_for_status()
    return r.content if binary else r.text, r


def filename_from_content_disposition(cd):
    if not cd:
        return ""
    m = re.search(r"filename\*=UTF-8''([^;]+)", cd, re.I)
    if m:
        return safe_name(requests.utils.unquote(m.group(1).strip().strip('"')))
    m = re.search(r'filename="?([^";]+)"?', cd, re.I)
    if m:
        return safe_name(requests.utils.unquote(m.group(1).strip()))
    return ""


def infer_ext(href="", text="", content_type="", filename=""):
    for source in (filename or "", href or "", text or ""):
        m = EXT_RE.search(source)
        if m:
            ext = m.group(1).lower()
            return "html" if ext == "htm" else ext
    ct = (content_type or "").split(";")[0].lower().strip()
    return CONTENT_TYPE_EXT.get(ct, "bin")


def is_bad_resource(url):
    u = (url or "").lower()
    return any(x in u for x in BAD_URL_PARTS)


def looks_like_document_url(url):
    u = (url or "").lower()
    if is_bad_resource(u):
        return False
    return bool(EXT_RE.search(u) or any(x in u for x in DOC_URL_PARTS))


def looks_like_document_text(text):
    t = (text or "").lower()
    return any(x in t for x in ["pliego", "anuncio", "deuc", "memoria", "informe", "acta", "resolución", "resolucion", "adjudicación", "adjudicacion", "formalización", "formalizacion", "csv"])


def nearby_label(a, full_url):
    candidates = []
    for attr in ["title", "aria-label", "download"]:
        v = clean(a.get(attr))
        if v:
            candidates.append(v)
    txt = clean(a.get_text(" "))
    if txt:
        candidates.append(txt)
    row = a.find_parent("tr")
    if row:
        cells = [clean(c.get_text(" ")) for c in row.find_all(["td", "th"])]
        for c in cells:
            if c and len(c) > 3:
                candidates.append(c)
    parent = a.parent
    for _ in range(4):
        if not parent:
            break
        ptxt = clean(parent.get_text(" "))
        if ptxt and len(ptxt) > 3:
            candidates.append(ptxt)
        parent = parent.parent
    # Limpieza: descartamos URLs, nombres técnicos y textos enormes de JS
    cleaned = []
    for c in candidates:
        c = re.sub(r"https?://\S+", " ", c)
        c = re.sub(r"GetDocumentByIdServlet\S*", " ", c, flags=re.I)
        c = re.sub(r"[?&][A-Za-z0-9_=-]{10,}", " ", c)
        c = clean(c)
        if not c:
            continue
        if len(c) > 180:
            c = c[:180]
        low = c.lower()
        if low in ["descargar", "download", "ver", "documento", "getdocumentbyidservlet"]:
            continue
        if "deferred modules" in low or "contenthandler" in low or "javascript" in low:
            continue
        cleaned.append(c)
    if cleaned:
        # preferimos etiquetas con palabras de documento; si no, la primera útil
        for c in cleaned:
            if looks_like_document_text(c):
                return c
        return cleaned[0]
    base = os.path.basename(urlparse(full_url).path)
    return base if base and base.lower() != "getdocumentbyidservlet" else "Documento"


def section_for_anchor(a):
    parent = a.parent
    for _ in range(10):
        if not parent:
            break
        # encabezados anteriores o dentro del contenedor
        header = parent.find(["h1", "h2", "h3", "h4", "caption", "legend"])
        if header:
            sec = clean(header.get_text(" "))
            if sec:
                return sec[:70]
        prev = parent.find_previous(["h1", "h2", "h3", "h4", "caption", "legend"])
        if prev:
            sec = clean(prev.get_text(" "))
            if sec and len(sec) < 100:
                return sec[:70]
        parent = parent.parent
    return "Documentos"


def enrich_doc_metadata(doc):
    """Intenta conocer nombre/tipo real sin descargar el cuerpo completo."""
    try:
        r = SESSION.head(doc["url"], timeout=12, allow_redirects=True)
        # Algunos servidores no aceptan HEAD
        if r.status_code >= 400 or not r.headers:
            r = SESSION.get(doc["url"], timeout=16, allow_redirects=True, stream=True)
        cd_name = filename_from_content_disposition(r.headers.get("content-disposition", ""))
        ct = r.headers.get("content-type", "")
        if cd_name:
            doc["name"] = cd_name.rsplit(".", 1)[0] if "." in cd_name else cd_name
        ext = infer_ext(doc["url"], doc.get("name", ""), ct, cd_name)
        if ext != "bin":
            doc["ext"] = ext
    except Exception:
        pass
    return doc


def extract_documents(html, source_url, enrich=True):
    soup = BeautifulSoup(html, "lxml")
    docs, seen = [], set()
    for a in soup.find_all("a", href=True):
        href = a.get("href") or ""
        if not href or href.startswith("#") or href.lower().startswith("javascript"):
            continue
        full = urljoin(source_url, href)
        if full in seen or is_bad_resource(full):
            continue
        text = clean(a.get_text(" ") or a.get("title") or a.get("aria-label") or "")
        if not (looks_like_document_url(full) or looks_like_document_text(text)):
            continue
        seen.add(full)
        row = a.find_parent("tr") or a.find_parent("li") or a.parent
        row_text = clean(row.get_text(" ") if row else text)
        dm = DATE_RE.search(row_text)
        status = "Disponible"
        if re.search("anulad", row_text, re.I):
            status = "Anulado"
        elif re.search("publicad|vigente|activo|disponible", row_text, re.I):
            status = "Publicado" if re.search("publicad", row_text, re.I) else "Disponible"
        name = nearby_label(a, full)
        ext = infer_ext(full, name)
        doc = {
            "id": f"d{len(docs)+1}",
            "name": safe_name(name),
            "ext": ext,
            "date": dm.group(0) if dm else "",
            "status": status,
            "section": section_for_anchor(a),
            "url": full,
        }
        if enrich:
            doc = enrich_doc_metadata(doc)
        docs.append(doc)
    # Dejar fuera cualquier recurso técnico que se haya colado
    docs = [d for d in docs if not is_bad_resource(d["url"])]
    return docs


def extract_info(html, url, default_num=""):
    soup = BeautifulSoup(html, "lxml")
    text = clean(soup.get_text(" "))
    def first_text(selectors):
        for sel in selectors:
            el = soup.select_one(sel)
            if el:
                val = clean(el.get_text(" "))
                if val and len(val) < 200:
                    return val
        return ""
    numero = ""
    for pat in [r"Expediente[:\s]+([A-Z0-9/_.\-]+)", r"N[úu]mero de expediente[:\s]+([A-Z0-9/_.\-]+)"]:
        m = re.search(pat, text, re.I)
        if m:
            numero = m.group(1); break
    numero = numero or default_num
    titulo = first_text(["h1", "h2", '[class*="titulo"]', '[id*="titulo"]'])[:180]
    importe = (re.search(r"\d[\d.,]+\s*€", text) or [""])[0] if re.search(r"\d[\d.,]+\s*€", text) else ""
    fecha = (DATE_RE.search(text).group(0) if DATE_RE.search(text) else "")
    tipo = "Contrato Menor" if re.search("menor", text, re.I) else ("Licitación" if re.search("licitac", text, re.I) else "Expediente")
    estado = "Disponible"
    if re.search("anulad", text, re.I): estado = "Anulado"
    elif re.search("adjudicad", text, re.I): estado = "Adjudicado"
    elif re.search("publicad|vigente|abierto", text, re.I): estado = "Publicado"
    return {"numero": clean(numero)[:80] or default_num, "titulo": titulo or "Información del expediente", "organo": "", "importe": importe, "fecha": fecha, "tipo": tipo, "estado": estado, "url": url}


def locate_detail(html, base_url, exp=""):
    soup = BeautifulSoup(html, "lxml")
    candidates = []
    exp_low = exp.lower().strip()
    for a in soup.find_all("a", href=True):
        href = a.get("href") or ""
        full = urljoin(base_url, href)
        if is_bad_resource(full):
            continue
        text = clean(a.get_text(" ")).lower()
        row_text = clean((a.find_parent("tr") or a.parent).get_text(" ")).lower() if (a.find_parent("tr") or a.parent) else text
        hlow = full.lower()
        score = 0
        if "deeplink:detalle" in hlow or "detalle_licitacion" in hlow or "detalle" in hlow: score += 5
        if "idevl" in hlow or "idlicitacion" in hlow: score += 4
        if "detalle" in text or "ver" in text or "expediente" in text: score += 2
        if exp_low and exp_low in row_text: score += 5
        if score:
            candidates.append((score, full))
    candidates.sort(reverse=True, key=lambda x: x[0])
    return candidates[0][1] if candidates else ""


def search_urls_for_exp(exp):
    q = quote_plus(exp)
    return [
        f"{BASE}/wps/portal/plataforma/buscar/resultado?numExpediente={q}&tipoBusqueda=licitaciones",
        f"{BASE}/wps/portal/plataforma/buscar/resultado?numExpediente={q}&tipoBusqueda=contratosmenores",
        f"{BASE}/wps/portal/plataforma/buscar/resultado?textoBusqueda={q}",
        f"{BASE}/wps/portal/plataforma/buscar?numExpediente={q}",
    ]

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/url")
def api_url():
    url = request.args.get("url", "").strip()
    try:
        html, resp = fetch(url)
        final_url = resp.url or url
        info = extract_info(html, url)
        docs = extract_documents(html, final_url, enrich=True)
        return jsonify({"expediente": info, "documents": docs})
    except Exception as e:
        return jsonify(error=str(e)), 502

@app.get("/api/search")
def api_search():
    exp = request.args.get("exp", "").strip()
    if not exp:
        return jsonify(error="Falta número de expediente"), 400
    last_err = None
    for u in search_urls_for_exp(exp):
        try:
            html, resp = fetch(u)
            base_url = resp.url or u
            detail = locate_detail(html, base_url, exp)
            if detail:
                html2, resp2 = fetch(detail)
                docs = extract_documents(html2, resp2.url or detail, enrich=True)
                if docs:
                    return jsonify({"expediente": extract_info(html2, detail, exp), "documents": docs})
            # Solo usamos documentos de la página de resultados si son documentos reales, no recursos técnicos
            docs = extract_documents(html, base_url, enrich=True)
            if docs:
                return jsonify({"expediente": extract_info(html, u, exp), "documents": docs})
        except Exception as e:
            last_err = e
    return jsonify(error=f"No se encontró el expediente o no hay documentos accesibles. {last_err or ''}"), 404

@app.get("/api/download")
def api_download():
    url = request.args.get("url", "").strip()
    filename = safe_name(request.args.get("filename", "documento"))
    try:
        content, resp = fetch(url, binary=True)
        cd_name = filename_from_content_disposition(resp.headers.get("content-disposition", ""))
        if cd_name:
            filename = cd_name
        if "." not in os.path.basename(filename):
            filename += "." + infer_ext(url, content_type=resp.headers.get("content-type", ""), filename=filename)
        return send_file(io.BytesIO(content), as_attachment=True, download_name=filename, mimetype=resp.headers.get("content-type") or "application/octet-stream")
    except Exception as e:
        return jsonify(error=str(e)), 502

@app.post("/api/zip")
def api_zip():
    data = request.get_json(force=True, silent=True) or {}
    docs = data.get("documents") or []
    exp = (data.get("expediente") or {}).get("numero") or "expediente"
    mem = io.BytesIO(); added = 0; errors = []; used = set()
    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as z:
        for doc in docs:
            url = (doc.get("url") or "").strip()
            if not url:
                continue
            try:
                content, resp = fetch(url, binary=True)
                cd_name = filename_from_content_disposition(resp.headers.get("content-disposition", ""))
                name = cd_name or safe_name(doc.get("name") or "documento")
                ext = infer_ext(url, doc.get("name", ""), resp.headers.get("content-type", ""), name)
                if "." not in os.path.basename(name):
                    name = f"{name}.{ext}"
                candidate = safe_name(name)
                stem, extdot = os.path.splitext(candidate)
                i = 2
                while candidate in used:
                    candidate = f"{stem}_{i}{extdot}"
                    i += 1
                used.add(candidate)
                z.writestr(candidate, content)
                added += 1
            except Exception as e:
                errors.append(f"{doc.get('name','documento')}: {e}")
        if errors:
            z.writestr("ERRORES_DESCARGA.txt", "No se pudieron descargar estos documentos:\n" + "\n".join(errors))
    if added == 0:
        return jsonify(error="No se pudo descargar ningún documento real."), 502
    mem.seek(0)
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{safe_name(exp)}_{stamp}.zip"
    return send_file(mem, as_attachment=True, download_name=filename, mimetype="application/zip")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
