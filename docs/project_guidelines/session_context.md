# Session Context — Log Analysis Pipeline

## Estado actual del proyecto

Estamos en **Mes 1, Semana 1 — Sprint completado**.
El pipeline base está funcionando de punta a punta.

---

## Lo que está completo

### `scripts/log_generator.py` ✅
Generador sintético de logs con soporte para argparse.

Decisiones de diseño importantes:
- CPU influye en `response_time` — correlación realista para ML
- `determine_level()` usa thresholds + probabilidades con `random.choices()`
- Todas las constantes viven en `config/config.yaml` — cargadas con `yaml.safe_load()`
- `load_config()` valida que las claves existan y no estén vacías — fail fast
- Dos funciones de timestamp separadas: `generate_log_timestamp()` para el contenido del log, `generate_runtimestamp()` para el nombre del archivo
- Número de logs configurable desde CLI con `-c` / `--count`

### `src/ingestion/log_reader.py` ✅
Lee el primer archivo de logs disponible para un servicio dado.

Decisiones de diseño importantes:
- Recibe el nombre del servicio como string
- Retorna una lista de strings — una por línea de log
- Maneja dos errores con mensajes descriptivos:
  - `ValueError` si el directorio del servicio no existe
  - `FileNotFoundError` si el directorio está vacío

### `src/processing/log_parser.py` ✅
Transforma lista de strings en lista de diccionarios.

Decisiones de diseño importantes:
- `partition(" msg=")` aísla el campo msg antes de hacer split
- Type conversion con try/except — sin hardcodear nombres de campos
- `strip('"\n')` limpia el mensaje de comillas y newlines
- Líneas malformadas skipeadas con `logger.warning()` — no crashea
- `_parse_line()` como función privada — separación de responsabilidades
- `None` como sentinel value para líneas malformadas

### `pipelines/run_pipeline.py` ✅
Orquestador del pipeline.

Decisiones de diseño importantes:
- Solo orquesta — no contiene lógica de negocio
- Llama a reader → parser y retorna solo el resultado final
- `pipelines/` es plural por diseño — preparado para escalar

### `main.py` ✅
Entry point de la aplicación.

Decisiones de diseño importantes:
- `logging.basicConfig()` se configura primero — antes de argparse y de cualquier función que loggee
- Servicio configurable desde CLI con `-s` / `--service`
- `main()` es thin — solo llama a `run_pipeline()` y retorna resultado

---

## Log format actual

```
timestamp=2026-03-09T22:15:52Z service=booking user=15 cpu=35 mem=43 response_time=413 level=INFO msg="Booking failed"
```

Todos los campos son `key=value` — formato consistente y parseable.

---

## Estructura del proyecto

```
log-analysis-pipeline/
│
├── config/
│   └── config.yaml
├── data/
│   └── raw/
│       ├── shopping/
│       ├── pricing/
│       └── booking/
├── src/
│   ├── __init__.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── log_reader.py
│   ├── processing/
│   │   ├── __init__.py
│   │   └── log_parser.py
│   └── utils/
│       └── features.py
├── pipelines/
│   ├── __init__.py
│   └── run_pipeline.py
├── scripts/
│   └── log_generator.py
├── tests/
├── docs/
├── output/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Documentación generada

- `docs/log_generator_design.md` — v2, incluye argparse
- `docs/log_reader_design.md` — v1
- `docs/log_parser_design.md` — v1, incluye manejo implícito de msg malformado
- `docs/run_pipeline_design.md` — v1
- `docs/main_design.md` — v1

---

## Lo que viene — Semana 2

- Convertir la lista de dicts en un DataFrame de pandas
- Operaciones básicas de análisis: conteos, agrupaciones, filtros
- Primera visualización con matplotlib — bar plot de log levels
- Introducción a tipos de datos en pandas

---

## Perfil del estudiante

- Trabaja como Critical Incident Manager
- Aprende con WSL + Vim
- Objetivo: Data/ML Engineering a largo plazo
- Filosofía: profundidad sobre velocidad

---

## Reglas para el asistente (Scrum Master)

- Guiar con preguntas, no dar soluciones directamente
- Dar código solo cuando el estudiante está genuinamente atascado
- Conectar cada tarea al proyecto principal
- Preferir soluciones simples
- Recordar commits y documentación cada sesión
- No recomendar soluciones que vayan en contra de buenas prácticas de Python aunque sean más fáciles
