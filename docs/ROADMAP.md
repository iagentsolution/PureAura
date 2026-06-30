# ROADMAP.md

# PureAura — Roadmap de Ejecución y Seguimiento Arquitectónico

**Versión:** 2.0
**Estado:** Consolidado
**Objetivo:** Consolidar la arquitectura del proyecto hasta obtener una separación estricta entre Domain, Application e Infrastructure sin pérdida de funcionalidad.

---

# 1. Principios Invariantes

Estos principios nunca deben romperse durante la refactorización.

## Arquitectura

```
Domain
    ↑
Application
    ↑
Infrastructure
```

## Reglas

* Domain nunca depende de Application.
* Domain nunca depende de Infrastructure.
* Domain nunca depende de UI.
* Domain nunca depende de Services.
* Application nunca contiene implementaciones concretas.
* Infrastructure implementa únicamente contratos de Application.
* Toda dependencia concreta se resuelve desde el Composition Root.
* Nunca duplicar implementaciones.
* Nunca mantener dos fuentes de verdad.
* Nunca eliminar código con consumidores activos.
* Cada iteración debe dejar el proyecto compilable y consistente.

---

# 2. Estado Global

| Fase                  | Estado |
| --------------------- | ------ |
| Baseline              | ☑      |
| Contracts             | ☑      |
| Infrastructure        | ☑      |
| Consumers             | ☑      |
| Composition Root      | ☑      |
| Legacy Services       | ☑      |
| Adapters              | ☑      |
| Domain                | ☑      |
| Application           | ☑      |
| Infrastructure Review | ☑      |
| Cleanup               | ☑      |
| Validation            | ☑      |
| Freeze                | ☑      |

---

# 3. Fases de Ejecución

## Fase 0 — Baseline

### Objetivo

Congelar el estado actual del proyecto.

### Actividades

* Inventario completo de módulos.
* Grafo de imports.
* Mapa de dependencias.
* Mapa de consumidores.
* Inventario de implementaciones.

### Criterio de salida

Existe una fotografía completa del estado inicial.

### Resultado

☑ Completada.

---

## Fase 1 — Contracts

### Objetivo

Centralizar todos los contratos en Application.

### Verificación

☑ Todos los contratos están en Application.

---

## Fase 2 — Infrastructure

### Objetivo

Mover todas las implementaciones concretas.

### Verificación

☑ Toda implementación concreta reside en Infrastructure.

---

## Fase 3 — Consumers

### Objetivo

Actualizar consumidores para usar exclusivamente contratos.

### Cambios realizados

* `ChatMessage` y `MessageRole` migrados de `core/` a `application/dto.py` y `domain/message.py`.
* `application/contracts/ai.py` actualizado para importar desde `application.dto`.
* `infrastructure/ai/groq_provider.py` actualizado para importar desde `application.dto` y `domain.message`.
* View models (`BrainState`, `ProfileView`, `AuraView`, `ProgressView`, `RankView`) migrados de `core/models.py` a `ui/models.py`.
* `SessionManager` migrado de `core/session.py` a `ui/session.py`.
* `ui/chat.py`, `ui/sidebar.py`, `ui/profile.py` actualizados para importar desde `ui.*`.
* `app.py` actualizado: importa desde `ui.session` y cablea `Brain` al `Container`.

### Verificación

☑ No existen imports directos a implementaciones salvo desde el Composition Root.

---

## Fase 4 — Composition Root

### Objetivo

Centralizar la construcción de dependencias.

### Verificación

☑ Ningún módulo instancia infraestructura manualmente. `application/container.py` es el único punto de resolución.

---

## Fase 5 — Legacy Services

### Objetivo

Eliminar la capa `core/` completa.

### Cambios realizados

* Eliminado `core/constants.py` (duplicaba `config.py` y definía `Role` que migró a `domain/message.py`).
* Eliminado `core/models.py` (todos los modelos migraron a `domain/` y `ui/models.py`).
* Eliminado `core/session.py` (migrado a `ui/session.py`).
* Eliminado `core/bootstrap.py` (wrapper legacy, Container se usa directamente).
* Eliminado `core/dependencies.py` (adaptador legacy sin consumidores).

### Verificación

☑ `core/` puede eliminarse completamente.

---

## Fase 6 — Adapters

### Objetivo

Eliminar código temporal: wrappers, bridges, adapters, compatibility shims.

### Cambios realizados

* Eliminado `application/base_service.py` (alias vacío de compatibilidad).
* Eliminado `application/handlers.py` (protocolos legacy sin consumidores).
* Eliminado `application/command.py` (especialización semántica legacy de UseCase).
* Eliminado `application/query.py` (especialización semántica legacy de UseCase).

### Verificación

☑ No existen adapters temporales.

---

## Fase 7 — Domain

### Objetivo

Aislar completamente el dominio.

### Verificación

☑ Domain no depende de ninguna capa superior. Todos los imports son internos o stdlib.

---

## Fase 8 — Application

### Objetivo

Mantener únicamente coordinación.

### Verificación

☑ Application contiene únicamente coordinación y contratos. Sin Streamlit, sin SDKs, sin implementaciones.

---

## Fase 9 — Infrastructure Review

### Objetivo

Revisar todas las implementaciones. Eliminar duplicados y código obsoleto.

### Cambios realizados

* Eliminado `infrastructure/ai/groq_service.py` (todos los métodos lanzaban RuntimeError, reemplazado por `GroqClient` interno en `groq_provider.py`).
* Eliminado contrato huérfano `ProgressUpdater` de `application/contracts/__init__.py` (sin implementación ni consumidores).
* Corregido `infrastructure/ai/__init__.py` (eliminada referencia al archivo borrado).

### Verificación

☑ Existe una única implementación por contrato.

---

## Fase 10 — Cleanup

### Objetivo

Eliminar código muerto, imports huérfanos, módulos duplicados.

### Cambios realizados

* Eliminado `domain/interfaces.py` (Protocol duplicados de `services.py`, `repositories.py`, `uow.py`).
* Eliminado `domain/errors.py` (duplicado de `domain/exceptions.py`).
* Eliminada export huérfana `AuraState` de `domain/__init__.py`.
* Eliminados DTOs genéricos no utilizados (`Request`, `Response`) de `application/dto.py`.

### Verificación

☑ No queda deuda técnica identificada.

---

## Fase 11 — Validation

### Resultado

☑ Sin ciclos.

☑ Sin imports prohibidos.

☑ Sin dependencias hacia `core/` o `services/`.

☑ Domain aislado (solo imports internos + stdlib).

☑ Application desacoplada (sin Streamlit, sin SDKs, sin implementaciones).

☑ Infrastructure concreta (sin contratos propios, solo implementaciones de Application contracts).

☑ Todos los contratos tienen implementación.

☑ No existen módulos huérfanos.

---

## Fase 12 — Freeze

### Propiedades finales

☑ Sin `core/`.

☑ Sin adapters.

☑ Sin compatibility shims.

☑ Sin código legacy.

☑ Sin dependencias circulares.

☑ Composition Root único (`application/container.py`).

☑ Arquitectura estable para futuras extensiones.

### Estructura final

```
app.py                  # Punto de entrada (Presentation)
brain.py                # Coordinador Presentation → Application
config.py               # Configuración global
prompts.py              # Prompts del sistema

domain/                 # Modelo de dominio puro
    entities.py
    value_objects.py
    aggregate.py
    events.py
    message.py
    aura.py
    mission.py
    progress.py
    user.py
    conversation.py
    ...                 # (rules, policies, specifications, etc.)

application/            # Coordinación + contratos
    use_case.py
    container.py        # Composition Root
    contracts/          # Contratos (ABCs)
    dto.py              # DTOs de transferencia
    send_message.py     # Casos de uso
    analyze_aura.py
    generate_missions.py
    complete_mission.py
    update_progress.py
    export_pdf.py
    event_bus.py

infrastructure/         # Implementaciones concretas
    ai/
        factory.py
        groq_provider.py
    services/
        aura_service.py
        mission_service.py
        xp_service.py
        pdf_service.py
    events/             # (reservado)
    files/              # (reservado)
    persistence/        # (reservado)

ui/                     # Capa de presentación
    models.py           # View models
    session.py          # Gestión de sesión Streamlit
    chat.py
    sidebar.py
    profile.py
    login.py
    styles.py
```

---

# 4. Protocolo de Trabajo

Cada iteración seguirá estrictamente este ciclo:

1. Analizar el proyecto completo.
2. Determinar la primera tarea pendiente de la fase activa.
3. Aplicar únicamente esa tarea.
4. Actualizar imports y consumidores afectados.
5. Eliminar código obsoleto únicamente si quedó sin consumidores.
6. Verificar que la fase continúa consistente.
7. Esperar un nuevo ZIP.

Nunca avanzar dos fases simultáneamente.

---

# 5. Criterios de Finalización del Proyecto

El proyecto se considerará consolidado cuando se cumplan simultáneamente todas las condiciones siguientes:

* Todas las fases marcadas como completadas.
* Domain completamente aislado.
* Application desacoplada.
* Infrastructure como única capa de implementaciones.
* Composition Root único.
* Carpeta `core/` eliminada.
* Sin adapters temporales.
* Sin compatibility shims.
* Sin código legacy.
* Sin módulos duplicados.
* Sin módulos huérfanos.
* Sin dependencias circulares.
* Sin imports prohibidos.
* Arquitectura estable para futuras extensiones.
