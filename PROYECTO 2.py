import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from collections import Counter

# ==========================================
# 1. LÓGICA DEL MODELO
# ==========================================
def simular_mercado(dias, estado_inicial):
    estados = ["Alza", "Baja", "Estancado"]
    matriz_transicion = np.array([
        [0.6, 0.2, 0.2],
        [0.2, 0.5, 0.3],
        [0.3, 0.3, 0.4]
    ])
    
    estado_actual = estado_inicial
    historial = [estado_actual]
    
    # CORRECCIÓN: Se resta 1 para que el total de días coincida con lo ingresado
    for _ in range(dias - 1):
        indice_actual = estados.index(estado_actual)
        estado_siguiente = np.random.choice(estados, p=matriz_transicion[indice_actual])
        historial.append(estado_siguiente)
        estado_actual = estado_siguiente
        
    return historial, estados, matriz_transicion

# ==========================================
# 2. FUNCIÓN DE DIBUJO MULTILÍNEA Y EJECUCIÓN
# ==========================================
def dibujar_linea_tiempo(canvas, historial):
    canvas.delete("all")
    colores = {"Alza": "#388e3c", "Baja": "#d32f2f", "Estancado": "#fbc02d"} 
    sombra_color = "#cbd5e1" 
    
    start_x = 55          
    start_y = 55          
    radio = 20            
    distancia_x = 80      
    distancia_y = 110     
    nodos_por_fila = 10   
    
    coordenadas = []
    
    for i, estado in enumerate(historial):
        columna = i % nodos_por_fila
        fila = i // nodos_por_fila
        
        x_actual = start_x + columna * distancia_x
        y_centro = start_y + fila * distancia_y
        coordenadas.append((x_actual, y_centro))
        
        if columna > 0 and i > 0:
            px, py = coordenadas[i-1]
            canvas.create_line(px + radio + 5, py, x_actual - radio - 5, y_centro, 
                               arrow=tk.LAST, fill="#94a3b8", width=2)
                
        canvas.create_oval(x_actual - radio + 2, y_centro - radio + 2, 
                           x_actual + radio + 2, y_centro + radio + 2, 
                           fill=sombra_color, outline="")

        canvas.create_oval(x_actual - radio, y_centro - radio, x_actual + radio, y_centro + radio, 
                           fill=colores[estado], outline=colores[estado])
        
        canvas.create_text(x_actual, y_centro, text=str(i+1), fill="white", font=("Segoe UI", 10, "bold"))
        
        canvas.create_text(x_actual, y_centro + radio + 22, text=f"Día {i+1}\n{estado}", 
                           fill="#475569", font=("Segoe UI", 8, "bold"), justify="center")
        
    bbox = canvas.bbox("all")
    if bbox:
        canvas.config(scrollregion=(0, 0, bbox[2] + 50, bbox[3] + 50))

def ejecutar_simulacion():
    try:
        dias = int(entry_dias.get().strip())
        if dias <= 0: return
        
        estado_inicio = combo_estado.get()
        historial, estados, matriz_transicion = simular_mercado(dias, estado_inicio)
        
        # --- A. Actualizar Línea de Tiempo ---
        dibujar_linea_tiempo(canvas_timeline, historial)
        
        conteos = Counter(historial)
        lbl_resumen.config(text=f"Días Alza: {conteos['Alza']}  |  Días Baja: {conteos['Baja']}  |  Días Estancado: {conteos['Estancado']}")
        
        # --- B. Calcular Estado Estacionario ---
        matriz_estacionaria = np.linalg.matrix_power(matriz_transicion, 50)
        prob_alza = matriz_estacionaria[0][0] * 100
        prob_baja = matriz_estacionaria[0][1] * 100
        prob_estancado = matriz_estacionaria[0][2] * 100
        
        # --- C. Actualizar Tablas Inferiores ---
        lbl_tbl1_alza.config(text=f"📈 Alza:\t\t{prob_alza:.1f}%")
        lbl_tbl1_baja.config(text=f"📉 Baja:\t\t{prob_baja:.1f}%")
        lbl_tbl1_est.config(text=f"➖ Estancado:\t{prob_estancado:.1f}%")
        
        lbl_tbl2_alza.config(text=f"{prob_alza:.1f}%")
        lbl_tbl2_baja.config(text=f"{prob_baja:.1f}%")
        lbl_tbl2_est.config(text=f"{prob_estancado:.1f}%")
            
    except ValueError:
        messagebox.showerror("Error", "Ingresa un número válido de días.")

# ==========================================
# 3. CONSTRUCCIÓN DE LA INTERFAZ
# ==========================================
ventana = tk.Tk()
ventana.title("Simulador Didáctico de Markov")
ventana.geometry("1150x750")
ventana.configure(bg="#eef2f5") 

# Título Principal
tk.Label(ventana, text="📊 Simulador Didáctico de Markov", font=("Segoe UI", 18, "bold"), bg="#eef2f5", fg="#1e293b").pack(pady=15)

frame_principal = tk.Frame(ventana, bg="#eef2f5")
frame_principal.pack(fill="both", expand=True, padx=20, pady=5)

# --- COLUMNA IZQUIERDA ---
col_izq = tk.Frame(frame_principal, bg="#eef2f5", width=280)
col_izq.pack(side="left", fill="y", padx=(0, 15))

# Panel Configuración
frame_config = tk.Frame(col_izq, bg="white", bd=1, relief="ridge", padx=15, pady=15)
frame_config.pack(fill="x", pady=(0, 15))
tk.Label(frame_config, text="⚙️ Panel de Guía y Configuración", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").pack(anchor="w", pady=(0,15))

tk.Label(frame_config, text="Estado inicial del mercado:", font=("Segoe UI", 9), bg="white").pack(anchor="w")
combo_estado = ttk.Combobox(frame_config, values=["Alza", "Baja", "Estancado"], state="readonly")
combo_estado.current(0) 
combo_estado.pack(fill="x", pady=(0, 10))

tk.Label(frame_config, text="Días a simular:", font=("Segoe UI", 9), bg="white").pack(anchor="w")
entry_dias = ttk.Entry(frame_config)
entry_dias.insert(0, "30")
entry_dias.pack(fill="x", pady=(0, 15))

tk.Button(frame_config, text="▶ Ejecutar Simulación", bg="#4a6b8c", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=ejecutar_simulacion, pady=5).pack(fill="x")

# Panel Didáctica
frame_info = tk.Frame(col_izq, bg="white", bd=1, relief="ridge", padx=15, pady=15)
frame_info.pack(fill="both", expand=True)
tk.Label(frame_info, text="💡 Didáctica de Markov", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").pack(anchor="w", pady=(0,10))

textos = [
    ("⏱️ Dependencia Exclusiva:", "El modelo asume que el estado de mañana depende ÚNICAMENTE del estado de hoy."),
    ("🎲 Simulación de Saltos:", "Simulación paso a paso basándose en las probabilidades de la matriz."),
    ("🔄 Estabilidad a Largo Plazo:", "Tras estabilizarse, muestra el % de tiempo total en cada estado (ver tablas inferiores).")
]
for titulo, desc in textos:
    tk.Label(frame_info, text=titulo, font=("Segoe UI", 9, "bold"), bg="white", fg="#333", justify="left").pack(anchor="w", pady=(10,0))
    tk.Label(frame_info, text=desc, font=("Segoe UI", 9), bg="white", fg="#666", justify="left", wraplength=220).pack(anchor="w")


# --- COLUMNA DERECHA ---
col_der = tk.Frame(frame_principal, bg="#eef2f5")
col_der.pack(side="right", fill="both", expand=True)

# Panel Superior: Línea de Tiempo
frame_recorrido = tk.Frame(col_der, bg="white", bd=1, relief="ridge", padx=10, pady=10)
frame_recorrido.pack(fill="both", expand=True, pady=(0, 15))

frame_titulos_rec = tk.Frame(frame_recorrido, bg="white")
frame_titulos_rec.pack(fill="x", pady=(0,5))
tk.Label(frame_titulos_rec, text="📈 Recorrido de la Simulación Visualizado", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").pack(side="left")
lbl_resumen = tk.Label(frame_titulos_rec, text="Días Alza: 0  |  Días Baja: 0  |  Días Estancado: 0", font=("Segoe UI", 9, "bold"), bg="#f0f4f8", fg="#333", padx=10, pady=3)
lbl_resumen.pack(side="right")

frame_canvas_scroll = tk.Frame(frame_recorrido, bg="white", bd=0)
frame_canvas_scroll.pack(fill="both", expand=True)

scroll_y = tk.Scrollbar(frame_canvas_scroll, orient="vertical")
scroll_y.pack(side="right", fill="y")

canvas_timeline = tk.Canvas(frame_canvas_scroll, bg="white", height=200, highlightthickness=0, yscrollcommand=scroll_y.set)
canvas_timeline.pack(side="left", fill="both", expand=True)
scroll_y.config(command=canvas_timeline.yview)

# Panel Inferior: Tablas Organizadas
frame_analisis = tk.Frame(col_der, bg="white", bd=1, relief="ridge", padx=10, pady=10)
frame_analisis.pack(fill="both", expand=False)
tk.Label(frame_analisis, text="📉 Análisis de Estado Estacionario a Largo Plazo", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").pack(anchor="w", pady=(0, 15))

# Contenedor central para las tablas
frame_tablas_centro = tk.Frame(frame_analisis, bg="white")
frame_tablas_centro.pack(expand=True, pady=10)

# Tabla 1
tbl1 = tk.Frame(frame_tablas_centro, bg="white", bd=1, relief="solid", padx=20, pady=15)
tbl1.pack(side="left", padx=20)
lbl_tbl1_alza = tk.Label(tbl1, text="📈 Alza:\t\t--%", font=("Segoe UI", 10, "bold"), bg="white", fg="#388e3c")
lbl_tbl1_alza.pack(anchor="w")
lbl_tbl1_baja = tk.Label(tbl1, text="📉 Baja:\t\t--%", font=("Segoe UI", 10, "bold"), bg="white", fg="#d32f2f")
lbl_tbl1_baja.pack(anchor="w", pady=10)
lbl_tbl1_est = tk.Label(tbl1, text="➖ Estancado:\t--%", font=("Segoe UI", 10, "bold"), bg="white", fg="#fbc02d")
lbl_tbl1_est.pack(anchor="w")

# Tabla 2
tbl2 = tk.Frame(frame_tablas_centro, bg="#f8f9fa", bd=1, relief="solid", padx=20, pady=15)
tbl2.pack(side="left", padx=20)
tk.Label(tbl2, text="State\tIcon\tLong-Term %", font=("Segoe UI", 9, "bold"), bg="#f8f9fa").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,10))

tk.Label(tbl2, text="Alza", font=("Segoe UI", 9), bg="#f8f9fa").grid(row=1, column=0, sticky="w", padx=(0,20))
tk.Label(tbl2, text="📈", bg="#f8f9fa").grid(row=1, column=1)
lbl_tbl2_alza = tk.Label(tbl2, text="--%", font=("Segoe UI", 9), bg="#f8f9fa")
lbl_tbl2_alza.grid(row=1, column=2, sticky="e", padx=(20,0))

tk.Label(tbl2, text="Baja", font=("Segoe UI", 9), bg="#f8f9fa").grid(row=2, column=0, sticky="w", pady=5)
tk.Label(tbl2, text="📉", bg="#f8f9fa").grid(row=2, column=1, pady=5)
lbl_tbl2_baja = tk.Label(tbl2, text="--%", font=("Segoe UI", 9), bg="#f8f9fa")
lbl_tbl2_baja.grid(row=2, column=2, sticky="e", pady=5)

tk.Label(tbl2, text="Estancado", font=("Segoe UI", 9), bg="#f8f9fa").grid(row=3, column=0, sticky="w")
tk.Label(tbl2, text="➖", bg="#f8f9fa").grid(row=3, column=1)
lbl_tbl2_est = tk.Label(tbl2, text="--%", font=("Segoe UI", 9), bg="#f8f9fa")
lbl_tbl2_est.grid(row=3, column=2, sticky="e")

ejecutar_simulacion()

ventana.mainloop()