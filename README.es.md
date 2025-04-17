# DBNoteRescueAI

**DBNoteRescueAI** es una herramienta de migración inteligente que convierte notas almacenadas en bases de datos SQLite (comúnmente usadas por aplicaciones móviles de toma de notas) en archivos Markdown independientes, aprovechando la inteligencia artificial para mejorar los títulos y organizar el contenido de manera eficiente.

![Licencia: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)  
![Python 3.7+](https://img.shields.io/badge/Python-3.7+-blue)

## 🚀 Características

- **Migración integral de notas**: Extrae notas de bases de datos SQLite y las convierte en archivos Markdown individuales, preservando los metadatos.  
- **Mejora de títulos con IA**: Utiliza la API de Google Gemini para generar títulos descriptivos y concisos basados en el contenido de las notas.  
- **Soporte multilingüe**: Soporta tanto inglés como español para los prompts de generación de títulos con IA.  
- **Formateo Markdown enriquecido**: Exporta las notas con formato Markdown mejorado, conservando fechas de creación, marcas de tiempo de modificación y metadatos originales.  
- **Alta personalización**: Configurable para distintas estructuras de bases de datos mediante parámetros de línea de comandos.  
- **Modo sin IA**: Opción para migrar notas sin usar IA, manteniendo los títulos originales si se prefiere.  
- **Gestión de límites de API**: Sistema de demoras integrado para respetar las cuotas de la API y asegurar un funcionamiento fluido.

## 📋 Requisitos previos

- Python 3.7 o superior  
- Conexión a Internet (para funcionalidad de IA)  
- Clave de API de Google Gemini (opcional, solo si deseas usar la mejora de títulos con IA)  
- Acceso al archivo de base de datos SQLite que contiene tus notas

## 📦 Instalación

1. Clona este repositorio:  
   ```bash
   git clone https://github.com/Gabriel-Adaro/DBNoteRescueAI.git
   cd DBNoteRescueAI
   ```

2. Instala las dependencias requeridas:  
   ```bash
   pip install -r requirements.txt
   ```

3. (Opcional) Si planeas usar la funcionalidad de IA, [obtén una clave de API de Google Gemini gratis](https://ai.google.dev/gemini-api/docs/api-key?hl=es-419).

## 🔍 Guía de uso detallada

### Estructura básica del comando

```bash
python dbnoterescueai.py --db /ruta/a/tu/database.db [opciones]
```

### Parámetros esenciales

| Parámetro        | Abreviatura | Descripción                                         | Por defecto             |
|------------------|-------------|-----------------------------------------------------|-------------------------|
| `--db`           | `-d`        | Ruta al archivo de base de datos SQLite             | `blocdenotas.db`        |
| `--output`       | `-o`        | Directorio de salida para los archivos Markdown     | `migrated_notes_md`     |
| `--api-key`      | `-k`        | Clave de API de Google Gemini                       | Variable `GEMINI_API_KEY` |
| `--no-ai`        |             | Deshabilita la generación de títulos con IA         | False (IA habilitada)   |
| `--language`     | `-l`        | Idioma para los prompts de IA (`en` o `es`)         | `en` (inglés)           |

### Parámetros de estructura de la base de datos

| Parámetro          | Descripción                            | Por defecto     |
|--------------------|----------------------------------------|-----------------|
| `--table`          | Nombre de la tabla en la base de datos | `notes`         |
| `--id-column`      | Nombre de la columna de ID de nota     | `_id`           |
| `--title-column`   | Nombre de la columna de título         | `title`         |
| `--body-column`    | Nombre de la columna de contenido      | `body`          |
| `--date-column`    | Nombre de la columna de fecha de creación | `date`       |
| `--updated-column` | Nombre de la columna de última modificación | `updated_at` |

### Parámetros de comportamiento de la API

| Parámetro          | Descripción                                           | Por defecto |
|--------------------|-------------------------------------------------------|-------------|
| `--content-limit`  | Máximo de caracteres a enviar a la API                | `2000`      |
| `--delay`          | Retraso entre llamadas a la API en segundos           | `4`         |

## 🚀 Ejemplos de uso

### Migración básica con mejora de título por IA

```bash
python dbnoterescueai.py --db my_notes.db --api-key TU_API_KEY
```

### Migración de notas en español

```bash
python dbnoterescueai.py --db my_notes.db --api-key TU_API_KEY --language es
```

### Migración sin IA (mantener títulos originales)

```bash
python dbnoterescueai.py --db my_notes.db --no-ai
```

### Uso de variable de entorno para la clave de API

```bash
export GEMINI_API_KEY=tu_api_key_aquí
python dbnoterescueai.py --db my_notes.db
```

### Estructura de base de datos personalizada

```bash
python dbnoterescueai.py --db my_notes.db --api-key TU_API_KEY \
  --table my_notes_table \
  --title-column note_title \
  --body-column note_content \
  --date-column created_at \
  --updated-column modified_at
```

### Ajuste de límites de tasa de la API

```bash
python dbnoterescueai.py --db my_notes.db --api-key TU_API_KEY --delay 2
```

## 🔑 ¿Por qué usar la integración con Google Gemini API?

DBNoteRescueAI utiliza la API de Google Gemini por varias razones:

1. **Disponibilidad de capa gratuita**: Gemini ofrece una capa gratuita que permite hasta 30 solicitudes por minuto (RPM) para el modelo `gemini-2.0-flash-lite`, lo que la hace accesible para uso personal.  
2. **Rendimiento**: El modelo `gemini-2.0-flash-lite` ofrece un excelente equilibrio entre velocidad y calidad para esta tarea.  
3. **Soporte multilingüe**: Soporta de forma nativa múltiples idiomas, incluidos inglés y español.

### Gestión de límites de tasa

El script incluye protección incorporada contra límites de tasa de la API:

- Por defecto, introduce un retraso de 4 segundos entre llamadas (`--delay 4`).  
- Este ajuste mantiene tu uso muy por debajo del límite de 30 RPM de la capa gratuita de Gemini.  
- Puedes ajustar este retraso según tu cuota específica:
  - Usuarios de capa gratuita: 3–4 segundos recomendados.  
  - Usuarios de capa de pago: se puede reducir a 0.5–1 segundos si es necesario.

Si procesas muchas notas y quieres optimizar la velocidad sin exceder los límites, ajusta el parámetro `--delay`:

```bash
# Ejemplo: Procesamiento más rápido (2 segundos de retraso)
python dbnoterescueai.py --db my_notes.db --api-key TU_API_KEY --delay 2

# Ejemplo: Enfoque muy conservador (6 segundos de retraso)
python dbnoterescueai.py --db my_notes.db --api-key TU_API_KEY --delay 6
```

## 🌐 Soporte de idiomas

DBNoteRescueAI admite la generación de títulos con IA en varios idiomas:

- **Inglés** (`--language en`): Opción predeterminada con prompts optimizados para inglés.  
- **Español** (`--language es`): Prompts especializados para generación de títulos en español.

El parámetro de idioma afecta:  
1. Los prompts enviados a la API de Gemini.  
2. El estilo y la estructura de los títulos generados.

Ejemplo para notas en español:

```bash
python dbnoterescueai.py --db mis_notas.db --api-key TU_API_KEY --language es
```

## 🔎 Compatibilidad de bases de datos

### Estructura de base de datos esperada

Por defecto, DBNoteRescueAI espera una base de datos SQLite con la siguiente estructura:

```sql
CREATE TABLE notes (
    _id INTEGER PRIMARY KEY,
    title TEXT,
    body TEXT,
    date TEXT,
    updated_at INTEGER
);
```

### Aplicaciones de notas compatibles

DBNoteRescueAI funciona bien con bases de datos de varias aplicaciones de toma de notas, incluyendo:

- Aplicaciones simples que usan SQLite para almacenamiento.  
- Muchas apps de notas en Android (yo personalmente utilizaba [Bloc de Notas](https://play.google.com/store/apps/details?id=jikansoftware.com.blocdenotas) y este script fue hecho específicamente para esa app, así que si tenes tus notas en esa aplicación, podés usar este script en su versión predeterminada sin problemas).
- Bases de datos exportadas de ciertos sistemas de gestión de notas.

Si tu base de datos tiene una estructura distinta, utiliza los parámetros de tabla y columna para personalizar el proceso.

## 📝 Formato de salida

La herramienta genera archivos Markdown con la siguiente estructura:

```markdown
# Título generado por IA (o Título original)

*(Título original: El título original si es diferente)*  
*(ID de nota: 123)*  
*(Fecha de creación: 2023-04-15)*  
*(Última actualización: 2023-05-20 14:30:45)*  
---

Contenido de la nota preservado en su forma original...
```

## 🛠️ Opciones de configuración adicionales

### Configuración de variables de entorno

Para mayor comodidad, puedes establecer la clave de API como variable de entorno:

**Linux/macOS**:  
```bash
export GEMINI_API_KEY=tu_api_key_aquí
```

**Windows (CMD)**:  
```cmd
set GEMINI_API_KEY=tu_api_key_aquí
```

**Windows (PowerShell)**:  
```powershell
$env:GEMINI_API_KEY="tu_api_key_aquí"
```

### Límite de contenido para la API

Para optimizar el uso de tokens y el coste de la API, DBNoteRescueAI limita el contenido enviado:

```bash
# Enviar solo los primeros 1000 caracteres para generación de títulos
python dbnoterescueai.py --db my_notes.db --api-key TU_API_KEY --content-limit 1000
```

## 🔍 Obtención de una clave de API de Google Gemini

Google Gemini ofrece una capa gratuita con límites de uso generosos, suficiente para procesar cientos de notas:

1. Visita [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key?hl=es-419)  
2. Inicia sesión con tu cuenta de Google  
3. Haz clic en "Create API Key"  
4. Copia la clave generada

**Notas importantes sobre la capa gratuita**:  
- Ofrece hasta 30 solicitudes por minuto (RPM) para el modelo `gemini-2.0-flash-lite`.  
- El retraso predeterminado de 4 segundos entre solicitudes garantiza que te mantengas por debajo del límite.  
- No se requiere tarjeta de crédito para la capa gratuita.

## 🔧 Guía de resolución de problemas

### Problemas de conexión a la base de datos

Si encuentras problemas de conexión:

- Verifica que la ruta de la base de datos sea correcta.  
- Asegúrate de tener permisos de lectura sobre el archivo.  
- Confirma que sea una base de datos SQLite válida.  
- Prueba usar una ruta absoluta en lugar de relativa:

  ```bash
  # Uso de ruta absoluta
  python dbnoterescueai.py --db /ruta/absoluta/a/tu/notes.db
  ```

### Errores de API

Para problemas con la API de Gemini:

- Verifica que tu clave de API sea correcta.  
- Comprueba tu conexión a Internet.  
- Confirma que no hayas superado tu cuota de API.  
- Prueba aumentando el retraso entre solicitudes:

  ```bash
  python dbnoterescueai.py --db my_notes.db --api-key TU_API_KEY --delay 6
  ```

### Problemas de codificación de caracteres

Si ves caracteres extraños en los archivos generados:

- Asegúrate de que tu base de datos use codificación UTF-8.  
- Revisa posibles incompatibilidades entre sistemas de origen y destino.  
- En Windows, considera ajustar la consola a UTF-8:

  ```cmd
  chcp 65001
  ```

### Salida faltante o vacía

Si no se generan archivos:

- Verifica que el directorio de salida exista y sea escribible.  
- Confirma que las notas en la base de datos tengan contenido.  
- Usa el modo verbose para ver información detallada:

  ```bash
  python dbnoterescueai.py --db my_notes.db --verbose
  ```

## 📊 Consideraciones de rendimiento

- **Velocidad de procesamiento**: Con la configuración predeterminada (4 segundos de retraso), se procesan aproximadamente 15 notas por minuto.  
- **Uso de memoria**: Requisitos mínimos de memoria, capaz de manejar bases de datos con miles de notas.  
- **Espacio en disco**: Los archivos de salida suelen ser más pequeños que la base de datos original.  
- **Costes de API**: La capa gratuita es suficiente para la mayoría de usos personales.

## 📄 Licencia

Este proyecto está licenciado bajo la [Licencia Pública General GNU v3.0](LICENSE).

## 🤝 Contribuciones

¡Pueden contribuir libremente, encontrando errores o haciendo sugerencias! Para eso, pueden:

1. Abrir un issue describiendo el problema o la mejora.  
2. Hacer un fork del repositorio y crear una nueva rama para tu función.  
3. Enviar un pull request con una descripción clara de los cambios.

Para cambios importantes, abrí primero un issue para discutir qué te gustaría cambiar.

## 🙏 Agradecimientos

- Google por proporcionar capacidades de IA accesibles.
