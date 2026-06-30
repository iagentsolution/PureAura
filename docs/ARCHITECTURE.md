# Arquitectura consolidada

PureAura se consolida en tres capas:

```
Domain
    ↑
Application
    ↑
Infrastructure
```

Las dependencias solo pueden apuntar hacia abajo en esta jerarquía lógica. Ninguna capa inferior conoce a una superior.

---

# Presentation

La capa de presentación consta de:

```
app.py          Punto de entrada Streamlit
brain.py        Coordinador entre UI y Application
ui/             Componentes visuales y view models
```

Presentation depende de Application (casos de uso) y de Domain (tipos compartidos como `MessageRole`).

---

# Proveedor IA

La infraestructura de IA reside en:

```
infrastructure/ai/
    factory.py           Resolución del proveedor activo
    groq_provider.py     Implementación concreta (GroqProvider + GroqClient)
```

El contrato `AIProvider` está definido en `application/contracts/ai.py`.

La capa Application consume únicamente las abstracciones expuestas mediante el Composition Root, evitando dependencias directas con implementaciones concretas.

---

# Composition Root

La composición del sistema se centraliza en:

```
application/container.py
```

Toda dependencia concreta se resuelve allí.

Los casos de uso no instancian servicios directamente.

---

# Estado actual

* Separación estricta entre Domain, Application e Infrastructure.
* Composition Root centralizado en `application/container.py`.
* Proveedor IA desacoplado de los consumidores.
* `core/` eliminado por completo.
* Sin adapters, shims ni código legacy.
* Arquitectura estable y consolidada.