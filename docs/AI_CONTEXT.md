# AI_CONTEXT

> Memoria arquitectónica permanente de PureAura.

Este documento debe leerse antes de realizar cualquier modificación sobre el proyecto.

---

# Estado actual

El proyecto se encuentra consolidado bajo Clean Architecture con tres capas estrictas:

```
Domain ← Application ← Infrastructure
```

Presentation (`app.py`, `brain.py`, `ui/`) consume Application y Domain.

La capa `core/` fue eliminada completamente.

---

# Objetivo del proyecto

PureAura implementa una plataforma centrada en el análisis del usuario ("Aura"), conversación asistida mediante IA, generación de misiones, progreso, experiencia (XP) y exportación de información.

---

# Capas identificadas

## Presentation

* `app.py` — Punto de entrada Streamlit.
* `brain.py` — Coordinador entre UI y casos de uso.
* `ui/` — Componentes visuales, view models y sesión.

## Application

Casos de uso (`send_message`, `analyze_aura`, `generate_missions`, `complete_mission`, `update_progress`, `export_pdf`).

DTOs (`ChatMessage`, `AnalyzeAuraResponse`, `GenerateMissionsResponse`, `CompleteMissionResponse`).

Container (Composition Root en `container.py`).

Contratos (`contracts/` — ABCs para services y AI provider).

Event bus (`event_bus.py`).

## Domain

Modelo de dominio puro.

Entidades: `User`, `Message`, `Aura`, `Mission`, `Progress`, `Conversation`.

Value Objects: `Text`, `Score`, `Identity`.

Eventos de dominio, servicios de dominio, repositorios, reglas, policies, specifications, factories, aggregate roots, unit of work.

## Infrastructure

Implementaciones concretas.

* `infrastructure/ai/` — Proveedor Groq (factory + provider + client).
* `infrastructure/services/` — AuraService, MissionService, XpService, PdfService.
* `infrastructure/events/`, `files/`, `persistence/` — Reservados para extensiones futuras.

---

# Configuración

`config.py` — Centraliza toda la configuración global (Groq, app settings).

---

# Flujo general

```
Usuario → UI → brain.py → Application (Use Cases) → Domain + Infrastructure
```

---

# Arquitectura

Separación estricta entre:

* dominio (reglas de negocio puras)
* casos de uso (coordinación)
* infraestructura (implementaciones técnicas)
* interfaz (Streamlit)

---

# Principios

* Separación de responsabilidades.
* Inversión de dependencias.
* DTOs entre capas.
* Servicios desacoplados via contratos.
* Proveedor IA intercambiable.
* Dominio aislado (sin dependencias externas).
* Composition Root único.

---

# Restricciones

* La documentación siempre debe surgir del código existente.
* No asumir módulos inexistentes.
* No asumir funcionalidades futuras.
* Registrar explícitamente módulos incompletos.
* No importar implementaciones concretas fuera del Composition Root.

---

# Objetivo de la documentación

Convertir `docs/` en la fuente oficial de conocimiento del proyecto para desarrolladores y futuras IA.