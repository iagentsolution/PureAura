# Estructura del Proyecto

```
app.py

brain.py

config.py

prompts.py

application/

domain/

infrastructure/

ui/

docs/
```

---

## application

Casos de uso.

DTOs.

Container (Composition Root).

Contratos (ABCs).

---

## domain

Modelo del negocio.

Entidades.

Objetos de valor.

Eventos.

Servicios de dominio.

Repositorios (contratos).

Policies.

Specifications.

Factories.

Aggregate Roots.

---

## infrastructure

Implementaciones concretas.

* `ai/` — Proveedor Groq.
* `services/` — Servicios técnicos (Aura, Mission, XP, PDF).
* `events/`, `files/`, `persistence/` — Reservados para extensiones futuras.

---

## ui

Interfaz de usuario Streamlit.

Componentes visuales.

View models.

Gestión de sesión.

---

## Configuración

`config.py` — Configuración global centralizada.