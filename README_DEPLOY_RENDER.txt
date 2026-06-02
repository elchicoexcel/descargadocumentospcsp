PCSP Analyzer - despliegue en Render
====================================

Esta versión funciona con:
- búsqueda por número de expediente
- búsqueda por URL directa del expediente
- visualización de documentos encontrados
- descarga individual real
- ZIP real con nombre expediente_fecha.zip

Pasos en Render:

1) Crea un repositorio en GitHub.
2) Sube TODO el contenido de esta carpeta al repositorio:
   app.py
   requirements.txt
   Procfile
   render.yaml
   templates/index.html

3) En Render:
   New + -> Web Service
   Conecta tu GitHub y elige el repositorio.

4) Configuración:
   Runtime: Python
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app

5) Pulsa Deploy.

Cuando termine, Render te dará una URL pública. Esa URL la podrá usar cualquier persona.

Notas:
- No hace falta instalar nada en los PCs de los usuarios.
- Si la Plataforma de Contratación cambia su HTML, puede requerir ajustes en los selectores de app.py.
- Si un expediente no aparece por número, prueba pegando la URL exacta del detalle del expediente.
