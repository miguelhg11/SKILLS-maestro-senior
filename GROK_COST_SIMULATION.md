# Simulación de Costes: Proyecto Masivo con Grok API

## Escenario "Pesadilla" (Worst Case Scenario)
Imagina que estás desarrollando un "Super-Sistema" complejo durante **un mes entero**.

### Supuestos del Escenario
*   **Duración**: 1 mes de trabajo intensivo.
*   **Interacciones**: 1.000 consultas a Grok (aprox. 33 al día).
*   **Contexto**: En cada consulta le envías **100.000 tokens** de contexto (equivalente a enviarle 2 libros de Harry Potter enteros cada vez para que los lea antes de responder). Esto es una barbaridad de datos.
*   **Salida**: Grok responde con 2.000 tokens (código extenso o análisis detallado).

### Precios (Grok beta / Grok 3)
*   **Input (Leer)**: $5.00 por millón de tokens.
*   **Output (Escribir)**: $15.00 por millón de tokens.

### Cálculo
1.  **Coste de Lectura (Input)**:
    *   1.000 consultas * 100.000 tokens = 100 Millones de tokens procesados.
    *   100M tokens * ($5.00 / 1M) = **$500.00 USD**

2.  **Coste de Escritura (Output)**:
    *   1.000 consultas * 2.000 tokens = 2 Millones de tokens generados.
    *   2M tokens * ($15.00 / 1M) = **$30.00 USD**

### **TOTAL MENSUAL (Escenario Pesadilla): ~$530.00 USD**

---

## Escenario "Realista" (Desarrollo Normal)
Uso típico de un Agente como Maestro para programar y depurar.

### Supuestos
*   **Interacciones**: 500 consultas al mes.
*   **Contexto**: 10.000 tokens (promedio razonable: varios archivos de código + historia del chat).
*   **Salida**: 1.000 tokens (bloques de código, instrucciones).

### Cálculo
1.  **Input**: 500 * 10k = 5 Millones de tokens -> **$25.00**
2.  **Output**: 500 * 1k = 0.5 Millones de tokens -> **$7.50**

### **TOTAL MENSUAL (Uso Normal): ~$32.50 USD**

---

## Veredicto Económico
*   **¿Es viable?**: Sí, para desarrollo normal es muy asequible (~$30/mes), similar a pagar ChatGPT Plus ($20) pero pagando por uso.
*   **¿Riesgo?**: Si le envías contextos masivos (libros enteros) constantemente en un bucle automático ("Agente Autónomo Infinito"), puedes gastar cientos de dólares rápidamente.

### Recomendación de Protección
Implementaremos un **"Limitador de Presupuesto"** en `scripts/grok_integration.py` que te avise si una sola consulta va a costar más de $0.50 (aprox 100k tokens).
