import io
import os
import re
import zipfile
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template, request, send_file

app = Flask(__name__)

BASE = "https://contrataciondelestado.es"
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 PCSPAnalyzer/2.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.6",
})

EXT_RE = re.compile(r"\.(pdf|xml|html?|docx?|xlsx?|zip|rar|odt|ods|csv|txt)(?:[?#].*)?$", re.I)
DATE_RE = re.compile(r"\b\d{2}[/-]\d{2}[/-]\d{4}\b")


def clean(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


def safe_name(name):
    name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", name or "documento").strip()
    return (name[:120] or "documento")


def fetch(url, binary=False):
    if not url.lower().startswith(("http://", "https://")):
        raise ValueError("URL no válida")
    r = SESSION.get(url, timeout=35, allow_redirects=True)
    r.raise_for_status()
    return r.content if binary else r.text, r


def infer_ext(href, text="", content_type=""):
    for source in (href or "", text or ""):
        m = EXT_RE.search(source)
        if m:
            return m.group(1).lower().replace("htm", "html")
    ct = (content_type or "").split(";")[0].lower()
    return {
        "application/pdf": "pdf",
        "application/xml": "xml", "text/xml": "xml",
        "text/html": "html",
        "application/msword": "doc",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
        "application/vnd.ms-excel": "xls",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
        "application/zip": "zip", "text/csv": "csv", "text/plain": "txt",
    }.get(ct, "bin")


def is_document_link(href, text):
    h = (href or "").lower()
    t = (text or "").lower()
    return bool(
        EXT_RE.search(h) or EXT_RE.search(t) or
        any(x in h for x in ["documento", "fichero", "download", "descarga", "getfile", "getdoc", "document"]) or
        any(x in t for x in ["pliego", "anuncio", "documento", "deuc", "memoria", "informe", "acta", "resolución", "resolucion"])
    )


def extract_documents(html, source_url):
    soup = BeautifulSoup(html, "lxml")
    docs = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a.get("href") or ""
        text = clean(a.get_text(" "))
        if not href or href.startswith("#") or href.lower().startswith("javascript"):
            continue
        if not is_document_link(href, text):
            continue
        full = urljoin(source_url, href)
        if full in seen:
            continue
        seen.add(full)
        row = a.find_parent("tr") or a.find_parent("li") or a.parent
        row_text = clean(row.get_text(" ") if row else text)
        dm = DATE_RE.search(row_text)
        status = "Disponible"
        if re.search("anulad", row_text, re.I):
            status = "Anulado"
        elif re.search("publicad|vigente|activo", row_text, re.I):
            status = "Publicado"
        section = "Documentos"
        parent = a.parent
        for _ in range(8):
            if not parent:
                break
            header = parent.find(["h1", "h2", "h3", "h4", "caption", "th"])
            if header:
                sec = clean(header.get_text(" "))
                if sec:
                    section = sec[:60]
                    break
            parent = parent.parent
        name = text or os.path.basename(urlparse(full).path) or "Documento"
        docs.append({
            "id": f"d{len(docs)+1}",
            "name": name[:160],
            "ext": infer_ext(full, text),
            "date": dm.group(0) if dm else "",
            "status": status,
            "section": section,
            "url": full,
        })
    return docs


def extract_info(html, url, default_num=""):
    soup = BeautifulSoup(html, "lxml")
    text = clean(soup.get_text(" "))
    def first_text(selectors):
        for sel in selectors:
            el = soup.select_one(sel)
            if el:
                val = clean(el.get_text(" "))
                if val:
                    return val
        return ""
    numero = first_text(['[id*="numeroExpediente"]', '[id*="expediente"]', '[class*="expediente"]'])
    m = re.search(r"Expediente[:\s]+([A-Z0-9/_.\-]+)", text, re.I)
    if m and (not numero or len(numero) > 80):
        numero = m.group(1)
    titulo = first_text(["h1", "h2", '[class*="titulo"]', '[id*="titulo"]'])[:180]
    importe = ""
    m = re.search(r"\d[\d.,]+\s*€", text)
    if m:
        importe = m.group(0)
    fecha = ""
    m = DATE_RE.search(text)
    if m:
        fecha = m.group(0)
    tipo = "Contrato Menor" if re.search("menor", text, re.I) else ("Licitación" if re.search("licitac", text, re.I) else "Expediente")
    estado = "Disponible"
    if re.search("anulad", text, re.I): estado = "Anulado"
    elif re.search("adjudicad", text, re.I): estado = "Adjudicado"
    elif re.search("publicad|vigente|abierto", text, re.I): estado = "Publicado"
    return {"numero": clean(numero)[:80] or default_num, "titulo": titulo, "organo": "", "importe": importe, "fecha": fecha, "tipo": tipo, "estado": estado, "url": url}


def locate_detail(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    candidates = []
    for a in soup.find_all("a", href=True):
        href = a.get("href") or ""
        text = clean(a.get_text(" ")).lower()
        hlow = href.lower()
        if any(x in hlow for x in ["detalle", "deeplink:detalle", "idlicitacion", "idevl"]) or any(x in text for x in ["detalle", "expediente", "ver"]):
            candidates.append(urljoin(base_url, href))
    return candidates[0] if candidates else ""


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/url")
def api_url():
    url = request.args.get("url", "").strip()
    try:
        html, resp = fetch(url)
        final_url = resp.url or url
        # Para el botón Ver en plataforma conservamos la URL que pegó el usuario, no la portada tras redirección.
        info = extract_info(html, url)
        docs = extract_documents(html, final_url)
        return jsonify({"expediente": info, "documents": docs})
    except Exception as e:
        return jsonify(error=str(e)), 502


@app.get("/api/search")
def api_search():
    exp = request.args.get("exp", "").strip()
    if not exp:
        return jsonify(error="Falta número de expediente"), 400
    urls = [
        f"{BASE}/wps/portal/plataforma/buscar/resultado?numExpediente={requests.utils.quote(exp)}&tipoBusqueda=licitaciones",
        f"{BASE}/wps/portal/plataforma/buscar/resultado?numExpediente={requests.utils.quote(exp)}&tipoBusqueda=contratosmenores",
    ]
    last_err = None
    for u in urls:
        try:
            html, resp = fetch(u)
            detail = locate_detail(html, resp.url or u)
            if detail:
                html2, resp2 = fetch(detail)
                info = extract_info(html2, detail, exp)
                docs = extract_documents(html2, resp2.url or detail)
                return jsonify({"expediente": info, "documents": docs})
            docs = extract_documents(html, resp.url or u)
            if docs:
                info = extract_info(html, u, exp)
                return jsonify({"expediente": info, "documents": docs})
        except Exception as e:
            last_err = e
    return jsonify(error=f"No se encontró el expediente o no hay detalle accesible. {last_err or ''}"), 404


@app.get("/api/download")
def api_download():
    url = request.args.get("url", "").strip()
    filename = safe_name(request.args.get("filename", "documento"))
    try:
        content, resp = fetch(url, binary=True)
        cd = resp.headers.get("content-disposition", "")
        m = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)', cd, re.I)
        if m:
            filename = safe_name(requests.utils.unquote(m.group(1)))
        if "." not in os.path.basename(filename):
            filename += "." + infer_ext(url, content_type=resp.headers.get("content-type", ""))
        return send_file(io.BytesIO(content), as_attachment=True, download_name=filename, mimetype=resp.headers.get("content-type") or "application/octet-stream")
    except Exception as e:
        return jsonify(error=str(e)), 502


@app.post("/api/zip")
def api_zip():
    data = request.get_json(force=True, silent=True) or {}
    docs = data.get("documents") or []
    exp = (data.get("expediente") or {}).get("numero") or "expediente"
    mem = io.BytesIO()
    added = 0
    errors = []
    used = set()
    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as z:
        for doc in docs:
            url = (doc.get("url") or "").strip()
            if not url:
                continue
            try:
                content, resp = fetch(url, binary=True)
                name = safe_name(doc.get("name") or "documento")
                ext = (doc.get("ext") or infer_ext(url, content_type=resp.headers.get("content-type", ""))).lstrip(".")
                if not name.lower().endswith("." + ext.lower()):
                    name = f"{name}.{ext}"
                base, dot, suffix = name.partition(".")
                candidate = name
                i = 2
                while candidate in used:
                    candidate = f"{base}_{i}.{suffix}" if dot else f"{name}_{i}"
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
