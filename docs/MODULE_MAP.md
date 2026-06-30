# MODULE MAP

Estado reconstruido desde el código fuente.

---

# Capas

```
Presentation
    │
    ▼
app.py
brain.py
    │
    ▼
Application
    │
    ├──────────────► Domain
    │
    └──────────────► Infrastructure
```

---

# Presentation

## app.py

Responsabilidades:

* Inicialización de la aplicación Streamlit.
* Punto de entrada.
* Cableado de Container → Brain.

## brain.py

Responsabilidades:

* Orquestación principal.
* Traducción entre interfaz y casos de uso.
* No contiene lógica de dominio.

# Application

Contiene exclusivamente casos de uso y el Composition Root.

## Casos de uso

* `analyze_aura.py`
* `send_message.py`
* `generate_missions.py`
* `complete_mission.py`
* `update_progress.py`
* `export_pdf.py`

Responsabilidades:

* Orquestar el flujo de ejecución.
* Coordinar Domain e Infrastructure.
* No implementar reglas de negocio.

## container.py

Composition Root.

Responsabilidades:

* Ensamblar dependencias.
* Resolver implementaciones.
* Construir casos de uso.
* Centralizar la configuración de infraestructura.

Toda dependencia concreta se resuelve aquí.

## contracts/

Contratos (ABCs) para servicios de infraestructura.

* `MessageGenerator`, `AuraAnalyzer`, `MissionGenerator`, `ProgressTracker`, `PdfExporter`.
* `AIProvider` (contrato del proveedor de IA).

## dto.py

Objetos de transferencia de datos.

* `ChatMessage` — DTO ligero para comunicación con IA.
* `AnalyzeAuraResponse`, `GenerateMissionsResponse`, `CompleteMissionResponse`.

---

# Domain

Contiene únicamente reglas de negocio.

## Entidades principales

* `User`, `Message`, `Aura`, `Mission`, `Progress`, `Conversation`.

## Value Objects

* `Text`, `Score`, `Identity`.

## Otros componentes

* Repositories (contratos), Rules, Policies, Specifications, Factories, Domain Services, Events, Aggregate Roots, Unit of Work.

---

# Infrastructure

Contiene implementaciones técnicas.

## infrastructure/ai/

* `factory.py` — Resolución del proveedor activo.
* `groq_provider.py` — `GroqProvider` (implementa `AIProvider`) + `GroqClient` (cliente HTTP concreto).

## infrastructure/services/

* `aura_service.py` — Implementa `MessageGenerator` + `AuraAnalyzer`.
* `mission_service.py` — Implementa `MissionGenerator`.
* `xp_service.py` — Implementa `ProgressTracker`.
* `pdf_service.py` — Implementa `PdfExporter`.

---

# UI

* `models.py` — View models (`BrainState`, `ProfileView`, `AuraView`, `ProgressView`, `RankView`, `ChatMessageView`).
* `session.py` — `SessionManager` (gestión de `st.session_state`).
* `chat.py`, `sidebar.py`, `profile.py`, `login.py`, `styles.py`.

---

# Configuración

`config.py` — Configuración global. No contiene reglas de negocio.

---

# Dependencias permitidas

```
Presentation (app, brain, ui)
        │
        ▼
Application (use cases, contracts, container)
      ↙     ↘
 Domain   Infrastructure
```

Reglas:

* Domain no depende de ninguna otra capa.
* Application depende de Domain e Infrastructure (solo en container.py).
* Infrastructure implementa contratos definidos por Application.
* Presentation nunca accede directamente a implementaciones concretas de Infrastructure.
* Todas las dependencias concretas se resuelven en `application/container.py`.