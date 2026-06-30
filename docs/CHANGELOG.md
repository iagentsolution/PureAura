# Changelog de la Documentación

## Versión 1.0

Se incorpora el sistema oficial de documentación del proyecto.

### Objetivos

* Reconstrucción arquitectónica.
* Documentación técnica.
* Índice completo del código.
* Mapa de módulos.
* Convenciones.
* Decisiones arquitectónicas.
* Contexto permanente para futuras sesiones.

---

## Versión 2.0 — Consolidación arquitectónica completa

Se ejecutaron las fases 3 a 12 del Roadmap.

### Fase 3 — Consumers

* `ChatMessage` y `MessageRole` migrados de `core/` a `application/dto.py` y `domain/message.py`.
* View models migrados de `core/models.py` a `ui/models.py`.
* `SessionManager` migrado de `core/session.py` a `ui/session.py`.
* Todos los consumidores actualizados para usar contratos en vez de implementaciones.
* `app.py` cablea `Brain` al `Container`.

### Fase 5 — Legacy Services

* Carpeta `core/` eliminada completamente (`constants.py`, `models.py`, `session.py`, `bootstrap.py`, `dependencies.py`).

### Fase 6 — Adapters

* Eliminados `application/base_service.py`, `handlers.py`, `command.py`, `query.py` (shims legacy sin consumidores).

### Fase 9 — Infrastructure Review

* Eliminado `infrastructure/ai/groq_service.py` (métodos vacíos, reemplazado por `GroqClient`).
* Eliminado contrato huérfano `ProgressUpdater`.

### Fase 10 — Cleanup

* Eliminados `domain/interfaces.py` y `domain/errors.py` (duplicados).
* Eliminada export huérfana `AuraState`.

### Fase 11 — Validation

* Verificación completa: sin ciclos, sin imports prohibidos, sin módulos huérfanos.

### Fase 12 — Freeze

* Todas las fases del Roadmap completadas.
* Arquitectura estable.

---

Esta documentación se genera directamente desde el código del proyecto y deberá mantenerse sincronizada con la implementación.