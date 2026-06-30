# PureAura Documentation

> Documentación arquitectónica generada a partir del código fuente del proyecto.

---

## Objetivo

La carpeta `docs/` constituye la fuente oficial de documentación técnica de PureAura.

Su finalidad es permitir comprender el proyecto sin necesidad de recorrer manualmente el código.

Toda la documentación se reconstruye desde la implementación existente.

No documenta arquitectura hipotética.

No documenta funcionalidades planificadas que aún no existan.

---

## Contenido

```
docs/
│
├── README.md
├── AI_CONTEXT.md
├── ARCHITECTURE.md
├── PROYECT_STRUCTURE.md
├── MODULE_MAP.md
├── FUNCTION_INDEX.md
├── ROADMAP.md
├── CHANGELOG.md
├── CHAT_CONTEXT.md
└── decisions/
    ├── 0001-project-vision.md
    ├── 0002-clean-architecture.md
    ├── 0003-groq-core.md
    ├── 0004-state-of-aura.md
    ├── 0005-xp-system.md
    ├── 0006-pdf-architecture.md
    ├── 0007-ui-guidelines.md
    └── 0008-development-workflow.md
```

---

## Principios

* La documentación refleja el código existente.
* No se inventan módulos.
* No se inventan responsabilidades.
* Se documentan migraciones arquitectónicas cuando existen.
* La documentación evoluciona junto al proyecto.

---

## Orden recomendado de lectura

1. AI_CONTEXT.md
2. ARCHITECTURE.md
3. PROYECT_STRUCTURE.md
4. MODULE_MAP.md
5. FUNCTION_INDEX.md
6. ROADMAP.md
7. CHANGELOG.md
8. CHAT_CONTEXT.md
9. decisions/

---

## Estado del proyecto

El roadmap arquitectónico está **completado** (Fase 12 — Freeze).

La arquitectura se encuentra consolidada con separación estricta entre Domain, Application e Infrastructure.