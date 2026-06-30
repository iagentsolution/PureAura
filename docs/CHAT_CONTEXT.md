# Contexto para futuras conversaciones

Antes de modificar el proyecto debe leerse, en este orden:

1. AI_CONTEXT.md
2. ARCHITECTURE.md
3. MODULE_MAP.md
4. FUNCTION_INDEX.md
5. ROADMAP.md

Reglas:

* No asumir comportamiento inexistente.
* Basar cualquier cambio en el estado actual del código.
* Mantener consistencia arquitectónica.
* Evitar duplicación de responsabilidades.
* Priorizar reutilización de casos de uso existentes.
* Actualizar esta documentación cuando cambie la arquitectura.
* No importar implementaciones concretas fuera del Composition Root (`application/container.py`).
* Domain nunca debe depender de capas superiores.
* Toda nueva infraestructura debe implementar un contrato existente en `application/contracts/`.