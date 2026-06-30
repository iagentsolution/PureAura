# FUNCTION INDEX

Índice funcional reconstruido a partir de la arquitectura consolidada.

---

# Presentation

## app.py

* Inicialización de la aplicación Streamlit.
* Bootstrap del sistema.
* Cableado Container → Brain.

---

## brain.py

* Coordinación del flujo principal.
* Ejecución de casos de uso.
* Comunicación con la capa Application.

---

# Application

## send_message.py

* Envío de mensajes.
* Coordinación con proveedor IA, análisis de aura, generación de misiones y progreso.

## analyze_aura.py

* Análisis del aura.
* Orquestación del caso de uso.

## generate_missions.py

* Generación de misiones.
* Coordinación entre Domain e Infrastructure.

## complete_mission.py

* Finalización de misiones.
* Actualización del estado y progreso correspondiente.

## update_progress.py

* Actualización de progreso.

## export_pdf.py

* Exportación a PDF.

## container.py

Composition Root.

* Construcción del grafo de dependencias.
* Resolución de implementaciones concretas.
* Ensamblado de casos de uso.

## dto.py

* `ChatMessage` — DTO para comunicación con IA.
* `AnalyzeAuraResponse`, `GenerateMissionsResponse`, `CompleteMissionResponse`.

## contracts/

* `AIProvider` — Contrato del proveedor de IA.
* `MessageGenerator`, `AuraAnalyzer`, `MissionGenerator`, `ProgressTracker`, `PdfExporter`.

---

# Domain

## entities.py

* `Entity` — Clase base genérica para entidades de dominio.

## message.py

* `Message` — Aggregate Root de mensajes.
* `MessageRole` — Enum de roles (SYSTEM, USER, ASSISTANT).

## user.py

* `User` — Aggregate Root de usuario.

## aura.py

* `Aura` — Aggregate Root del aura del usuario.

## mission.py

* `Mission` — Aggregate Root de misiones con ciclo de vida controlado.
* `MissionStatus` — Enum de estados de misión.

## progress.py

* `Progress` — Aggregate Root de seguimiento de progreso.

## conversation.py

* `Conversation` — Aggregate Root de conversaciones.

## value_objects.py

* `ValueObject` — Clase base para objetos de valor.

## score.py

* `Score` — Objeto de valor para puntuaciones.

## text.py

* `Text` — Objeto de valor para texto normalizado.

## identity.py

* `Identity` — Objeto de valor para identificadores de dominio.

## result.py

* `Result` — Tipo unión para resultados con manejo de errores.

## services.py

* `DomainService`, `AuraAnalysisService`, `MissionGenerationService`, `ProgressCalculationService`.

---

# Infrastructure

## infrastructure/ai/factory.py

* `AIProviderFactory` — Selección y resolución del proveedor activo.

## infrastructure/ai/groq_provider.py

* `GroqProvider` — Implementación concreta de `AIProvider`.
* `GroqClient` — Cliente HTTP del API de Groq.

## infrastructure/services/

* `AuraService` — Implementa `MessageGenerator` + `AuraAnalyzer`.
* `MissionService` — Implementa `MissionGenerator`.
* `XpService` — Implementa `ProgressTracker`.
* `PdfService` — Implementa `PdfExporter`.

---

Este documento debe mantenerse sincronizado con la estructura real del proyecto.