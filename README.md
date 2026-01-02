# Protocolo Saturno v2.0 - Guía de Funcionamiento

Este documento explica de forma sencilla qué es el Protocolo Saturno, para qué sirve y cómo protege tu trabajo.

## ¿Qué es el Protocolo Saturno?

Imagina que este protocolo es el **manual de seguridad y sentido común** de la Inteligencia Artificial.

Cuando hablas con una IA normal, esta intenta complacerte rápidamente, lo que a veces causa errores: inventa datos ("alucinaciones"), borra archivos sin querer o rompe código por no revisar antes.

El **Protocolo Saturno** es un conjunto de reglas estrictas que obligan a la IA a "pensar antes de actuar". Convierte a la IA en un **Auditor Técnico**: alguien que prefiere decir "no sé" a inventar una respuesta, y que prefiere pedir permiso antes que romper algo.

---

## ¿Cómo funciona? (El Flujo de Operación)

Cada vez que pides algo, la IA no ejecuta la orden inmediatamente. En su lugar, pasa tu petición por una serie de "filtros de seguridad", uno por uno, como si fuera una lista de chequeo de vuelo.

Aquí te explicamos el proceso paso a paso (que puedes ver resumido en la imagen de abajo):

### Paso 1: El Filtro de la Verdad (¿Es real?)
Lo primero que hace la IA es preguntarse: **"¿Tengo pruebas de lo que voy a decir?"**.
*   Si le pides un dato y no lo tiene en sus archivos -> **Se detiene.** Te dirá "No puedo confirmar esto" en lugar de inventar.
*   Si intenta adivinar -> **El protocolo lo prohíbe.**

### Paso 2: La Red de Seguridad (Si toca código)
Si tu petición implica cambiar código (ej: "Refactoriza este archivo"), la IA activa su **sistema de copias de seguridad**.
*   **Antes de tocar nada**, crea una copia exacta de tu archivo con un número de versión (ej: `archivo.js.v1.bak`).
*   Esto significa que si el cambio no te gusta, la IA puede "viajar en el tiempo" y dejarlo todo como estaba en un segundo.

### Paso 3: El Control de Peligro (Si toca infraestructura)
Si tu petición es arriesgada (ej: "Borra la base de datos" o "Sube esto a producción"), la IA se bloquea automáticamente.
*   **No actuará** hasta que tú le confirmes explícitamente que tienes una copia de seguridad externa (Snapshot) de todo el sistema.
*   Es como un botón rojo nuclear: se necesitan dos llaves (la tuya y la de la IA) para girarlo.

### Paso 4: Ejecución Segura
Solo si la petición pasa todos estos filtros (es verdad, hay backup local y tienes permiso), la IA ejecuta la acción.

---

## Visualización del Proceso

El siguiente diagrama representa este "cerebro" lógico. Sigue las flechas para ver cómo la IA decide qué hacer con tu petición:

```mermaid
graph TD
    A[Petición Usuario] --> B{¿Es Verdad?\n(R0-R7)}
    B -- No --> C[Detener / Abortar]
    B -- Sí --> D{¿Es Modificación\nde Código?}
    D -- Sí --> E[Backup Local\n(.vN.bak)]
    E --> F{¿Alto Riesgo?\n(R10)}
    D -- No --> F
    F -- Sí --> G[Solicitar Confirmación\n(Snapshot Ext)]
    F -- No --> H[Ejecución Segura]
    G --> H
    
    style C fill:#ff3333,stroke:#333,stroke-width:2px,color:white
    style H fill:#00cc66,stroke:#333,stroke-width:2px,color:black
    style E fill:#9933ff,stroke:#333,stroke-width:2px,color:white
    style G fill:#ff9900,stroke:#333,stroke-width:2px,color:black
```
---

## Estructura Técnica (Para Curiosos)

Para que esto funcione, el protocolo está escrito en dos "idiomas":
1.  **`Protocol.md` (Para Humanos):** El documento que lees con explicaciones y sentido.
2.  **`Protocol.json` (Para la Máquina):** Una versión comprimida y estricta que la IA lee para saber qué reglas aplicar matemáticamente.
