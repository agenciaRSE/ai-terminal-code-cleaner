# AI Terminal Code Cleaner

Utilidad local de escritorio (Python + Tkinter) que limpia los artefactos que las IAs introducen en los snippets de código (comillas tipográficas, em-dash, zero-width, BOM, fences de markdown, prefijos de prompt, CRLF, espacios al final de línea), para que se peguen en la terminal sin errores.

## Garantías

- **Sin red**: no usa `socket`, `urllib`, `requests`, `subprocess`, `os.system`, `eval`, `exec`.
- **Sin disco**: no escribe ni lee archivos. No hay logs, caché, ni configuración persistida.
- **Sin telemetría**.
- **Sin dependencias externas**: solo librería estándar (`tkinter`, `re`).
- El portapapeles del SO se usa solo cuando pulsas Pegar/Copiar.

## Cómo usar

Doble clic en `Lanzar.bat` (Windows) o ejecuta:

```
python clean_terminal.py
```

Atajos:

- `Ctrl+Shift+V` — pegar desde el portapapeles, limpiar y volver a copiar el resultado en un solo paso.
- `Ctrl+L` — limpiar lo que ya esté en el área de entrada.
- `Ctrl+Shift+C` — copiar el resultado limpio al portapapeles.

## Reglas de limpieza (todas conservadoras)

- Caracteres invisibles (zero-width, BOM, mongolian vowel separator) → eliminados.
- `nbsp` → espacio normal.
- Comillas tipográficas `“ ” „ ‟` → `"`, `‘ ’ ‚ ‛` → `'`.
- Em-dash `—` → `--` (recupera flags como `--save-dev`), en-dash `–` → `-`, `…` → `...`.
- `\r\n` y `\r` sueltos → `\n`.
- Espacios y tabs al final de cada línea → eliminados.
- Líneas que son solo <code>```</code> o <code>```lang</code> → eliminadas.
- Prefijos de prompt al inicio de línea (`$ `, `> `, `PS …> `, `C:\…>`) → eliminados.
- Líneas en blanco al inicio y al final del bloque → recortadas (las internas se conservan).

**No se hace** colapsar espacios múltiples, tocar tabs, unir líneas con `\`, convertir a one-liner, ni alterar contenido entre comillas.

## Requisitos

- Python 3.8+ con Tkinter (incluido en la instalación estándar de Python en Windows).

## Licencia

MIT — ver [LICENSE](LICENSE).
