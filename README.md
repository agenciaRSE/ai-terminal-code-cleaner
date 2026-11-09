> [!IMPORTANT]
> **Proyecto archivado.** Lo sustituye [Auto Clipboard](https://github.com/agenciaRSE/auto-clipboard), una skill para Claude Code y Claude Desktop que copia en el portapapeles el texto exacto que Claude te da para pegar, así que ya no hace falta limpiarlo después.
>
> **Archived.** Replaced by [Auto Clipboard](https://github.com/agenciaRSE/auto-clipboard), a Claude Code and Claude Desktop skill that copies the exact text Claude gives you to paste, so there is nothing left to clean.

<div align="center">

# 🧹 AI Terminal Code Cleaner

**Pega en la terminal lo que te da la IA… sin que explote.**
Una pequeña app de escritorio que limpia los snippets de ChatGPT, Claude o Gemini (comillas tipográficas, rayas largas, caracteres invisibles, fences de Markdown, prompts `$ `) antes de pegarlos.

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](clean_terminal.py)
[![Sin dependencias](https://img.shields.io/badge/dependencias-0-22c55e?style=for-the-badge)](#-garantías)
[![Sin red](https://img.shields.io/badge/red-ninguna-0a0a0a?style=for-the-badge)](#-garantías)
[![Licencia MIT](https://img.shields.io/badge/licencia-MIT-a855f7?style=for-the-badge)](LICENSE)

[English](#-in-english) · [Contribuir](#-contribuir)

</div>

---

## 😤 El problema

Copias un comando de la IA, lo pegas y la terminal responde con un error absurdo. El culpable no se ve: una comilla `“` en vez de `"`, una raya `—` donde iba `--`, un espacio de ancho cero o la línea <code>```bash</code> que se coló al copiar.

## ✅ Antes y después

````text
ANTES (copiado del chat)
```bash
$ npm install —save-dev vite
$ git commit -m “fix”
```

DESPUÉS (listo para la terminal)
npm install --save-dev vite
git commit -m "fix"
````

## ⚡ Cómo se usa

Doble clic en **`Lanzar.bat`** (Windows) o:

```bash
python clean_terminal.py
```

| Atajo | Qué hace |
|---|---|
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd> | Pega del portapapeles, limpia y vuelve a copiar el resultado, todo en un paso |
| <kbd>Ctrl</kbd>+<kbd>L</kbd> | Limpia lo que ya está en el área de entrada |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd> | Copia el resultado limpio |

## 🧽 Qué limpia (siempre de forma conservadora)

| Artefacto | Se convierte en |
|---|---|
| Caracteres invisibles (zero-width, BOM, separador mongol) | se eliminan |
| Espacio duro `nbsp` | espacio normal |
| Comillas tipográficas `“ ” „ ‟` / `‘ ’ ‚ ‛` | `"` / `'` |
| Raya `—` / semirraya `–` / `…` | `--` (recupera flags como `--save-dev`) / `-` / `...` |
| Saltos `\r\n` y `\r` | `\n` |
| Espacios y tabs al final de línea | se eliminan |
| Líneas <code>```</code> o <code>```lang</code> | se eliminan |
| Prompts al inicio de línea (`$ `, `> `, `PS …> `, `C:\…>`) | se eliminan |
| Líneas en blanco al principio y al final | se recortan (las de dentro se conservan) |

**Lo que no toca:** no junta espacios múltiples, no cambia tabs, no une líneas con `\`, no lo convierte en una sola línea y no altera nada entre comillas.

## 🔒 Garantías

- **Sin red:** no usa `socket`, `urllib`, `requests`, `subprocess`, `os.system`, `eval` ni `exec`.
- **Sin disco:** no lee ni escribe archivos. Sin logs, sin caché, sin configuración guardada.
- **Sin telemetría** y **sin dependencias**: solo la librería estándar (`tkinter`, `re`).
- El portapapeles solo se usa cuando pulsas pegar o copiar.

Es un solo archivo de Python: puedes leerlo entero antes de ejecutarlo.

## 📋 Requisitos

Python 3.8 o superior con Tkinter (viene incluido en la instalación estándar de Python para Windows; en Linux puede hacer falta el paquete `python3-tk`).

## 🤝 Contribuir

¿Te has encontrado otro carácter raro que rompe la terminal? **Esa es la mejor contribución posible.**

- 🧪 **Nuevos artefactos:** abre un issue con el texto que falló (sin datos sensibles) y qué esperabas.
- 🐧 **macOS y Linux:** prueba los atajos y el lanzador en tu sistema y cuéntanos cómo va.
- 🛡️ **Regla de oro:** cada limpieza nueva debe ser conservadora. Si una regla puede cambiar el significado de un comando, no entra.

Pull requests bienvenidos. Mantén las garantías: nada de red, nada de disco, nada de dependencias.

## 🇬🇧 In English

A tiny desktop app (Python + Tkinter, standard library only) that cleans AI-generated code snippets so they paste cleanly into a terminal: smart quotes, em dashes (`—` → `--`), invisible characters, non-breaking spaces, Markdown fences, `$ ` / `PS>` prompts, CRLF and trailing spaces. No network, no disk I/O, no telemetry. Run `python clean_terminal.py` and press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd>. Issues and pull requests are welcome.

## 📄 Licencia

[MIT](LICENSE) © Diego Meijide · Hecho por [AGENCIA RSE](https://agenciarse.com/estudio/), estudio de A Coruña.
