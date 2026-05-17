
# 📊 Simulador Didáctico de Modelos Ocultos de Markov (HMM) - Mercado Bursátil

Este repositorio contiene una aplicación interactiva desarrollada en Python orientada a la simulación y análisis de ciclos económicos y bursátiles mediante un **Modelo Oculto de Markov (HMM - Hidden Markov Model)**.

🎯 Descripción del Proyecto
En los mercados financieros del mundo real, la salud macroeconómica exacta (Expansión o Contracción) no es directamente observable en tiempo real; es un **estado oculto**. Lo que los inversores sí pueden observar diariamente es el comportamiento del mercado de valores (Alza, Baja o Estancado); estas son las **observaciones**. 

Este simulador permite inferir la relación estocástica entre la economía oculta y el mercado visible, calculando trayectorias a corto plazo y el estado estacionario a largo plazo.

✨ Características Principales
Interfaz Gráfica (GUI):** Desarrollada con `tkinter` para una experiencia de usuario amigable y moderna.
Simulación de Línea de Tiempo: Generación visual paso a paso de los saltos del mercado según los días estipulados por el usuario.
Cálculo de Estado Estacionario: Demostración matemática del equilibrio a largo plazo del sistema.
Manejo de Errores: Validación de entradas de usuario integradas.

🧠 Estructura Matemática del Modelo (HMM)
El programa basa su lógica en tres matrices probabilísticas fundamentales:
1. Probabilidades Iniciales :Define la probabilidad de iniciar la simulación en una economía en Expansión (70%) o Contracción (30%).
2. Matriz de Transición :** Rige la inercia del estado oculto (Economía). Asume altas probabilidades de mantenerse en el estado actual (85% para expansión, 80% para contracción) evitando cambios abruptos irreales.
3. Matriz de Emisión : Conecta el estado oculto con la observación visible. Define la probabilidad de ver un mercado al Alza, a la Baja o Estancado dependiendo de si la economía real subyacente está en bonanza o en crisis (incluyendo el "ruido" del mercado).

🛠️ Requisitos e Instalación

Para ejecutar este proyecto, necesitas tener instalado **Python 3.x** en tu sistema.

La interfaz gráfica utiliza `tkinter` (incluido por defecto en Python) y `collections`. La única librería externa requerida para los cálculos matriciales es `numpy`.

1. Clonar el repositorio:**
```bash
git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
cd TU_REPOSITORIO