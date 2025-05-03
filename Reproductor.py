import tkinter as tk
from tkinter import ttk, filedialog
from pygame import mixer
import time
import threading
from mutagen.mp3 import MP3 

class NodoCancion:
    def __init__(self, nombre, artista, duracion, ruta):
        self.nombre = nombre
        self.artista = artista
        self.duracion = duracion
        self.ruta = ruta
        self.anterior = None
        self.siguiente = None

    def __str__(self):
        return f"{self.nombre} - {self.artista} ({self.duracion})"


class ListaReproduccion:
    def __init__(self):
        self.actual = None

    def agregar(self, nodo):
        if self.actual is None:
            self.actual = nodo
            nodo.anterior = nodo.siguiente = nodo
        else:
            ultimo = self.actual.anterior
            ultimo.siguiente = nodo
            nodo.anterior = ultimo
            nodo.siguiente = self.actual
            self.actual.anterior = nodo

    def obtener_actual(self):
        return self.actual

    def siguiente(self):
        if self.actual:
            self.actual = self.actual.siguiente
        return self.actual

    def anterior(self):
        if self.actual:
            self.actual = self.actual.anterior
        return self.actual

    def obtener_lista(self):
        canciones = []
        if not self.actual:
            return canciones
        nodo = self.actual
        while True:
            canciones.append(nodo)
            nodo = nodo.siguiente
            if nodo == self.actual:
                break
        return canciones

class Reproductor(tk.Tk):
    def __init__(self):
        # DISEÑO
        super().__init__()
        self.title("🎵 Reproductor de Música")
        self.geometry("700x600")
        self.configure(bg="#1e1e2e") #AZUL OSCURO

        mixer.init()
        self.lista = ListaReproduccion()
        self.en_pausa = False
        self.en_reproduccion = False
        self.actualizando_slider = False
        
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Segoe UI", 10), padding=5, background="#FFEB3B", foreground="black")
        self.style.configure("TLabel", background="#1e1e2e", foreground="white", font=("Britannic Bold", 30))
        self.style.configure("TLabelframe", background="#1e1e2e", foreground="white", font=("Britannic Bold", 10))

        self.init_ui()

    def init_ui(self):
        self.label = ttk.Label(self, text="🎶 Canción actual: Ninguna")
        self.label.pack(pady=10)

        self.lista_widget = tk.Listbox(self, bg="#FF9800", fg="white", selectbackground="#89b4fa", font=("Britannic Bold", 20))
        self.lista_widget.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        #BOTONES DE LA PANTALLA PRINCIPAL
        frame_botones = ttk.Frame(self)
        frame_botones.pack(pady=10)

        self.btn_cargar = ttk.Button(frame_botones, text="📂 Cargar Canción", command=self.cargar_cancion)
        self.btn_cargar.grid(row=0, column=0, padx=5)

        self.btn_play = ttk.Button(frame_botones, text="    ▶️", command=self.reproducir)
        self.btn_play.grid(row=0, column=1, padx=5)

        self.btn_pause = ttk.Button(frame_botones, text="⏸️", command=self.pausar)
        self.btn_pause.grid(row=0, column=2, padx=5)

        self.btn_stop = ttk.Button(frame_botones, text="⏹️", command=self.detener)
        self.btn_stop.grid(row=0, column=3, padx=5)

        self.btn_prev = ttk.Button(frame_botones, text="⏮️", command=self.anterior)
        self.btn_prev.grid(row=0, column=4, padx=5)

        self.btn_next = ttk.Button(frame_botones, text="⏭️", command=self.siguiente)
        self.btn_next.grid(row=0, column=5, padx=5)

        self.slider = ttk.Scale(self, from_=0, to=100, orient="horizontal", command=self.mover_slider)
        self.slider.pack(fill=tk.X, padx=20, pady=10)

        self.label_tiempo = ttk.Label(self, text="00:00 / 00:00")
        self.label_tiempo.pack()

    def cargar_cancion(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos MP3", "*.mp3")])
        if not ruta:
            return  

        duracion = self.obtener_duracion(ruta)
        self.ruta_seleccionada = ruta

        # PESTAÑA PARA AGREGAR
        self.cargar_ventana = tk.Toplevel(self)
        self.cargar_ventana.title("Ingresar Datos de la Canción")
        self.cargar_ventana.geometry("600x400")
        self.cargar_ventana.configure(bg="#1e1e2e")

        ttk.Label(self.cargar_ventana, text="Nombre de Canción:").pack(pady=5)
        self.entry_nombre = ttk.Entry(self.cargar_ventana)
        self.entry_nombre.pack(pady=5, fill=tk.X, padx=20)

        ttk.Label(self.cargar_ventana, text="Artista:").pack(pady=5)
        self.entry_artista = ttk.Entry(self.cargar_ventana)
        self.entry_artista.pack(pady=5, fill=tk.X, padx=20)

        ttk.Label(self.cargar_ventana, text="Duración (automatico):").pack(pady=5)
        self.entry_duracion = ttk.Entry(self.cargar_ventana, state="readonly")
        self.entry_duracion.pack(pady=5, fill=tk.X, padx=20)
        self.entry_duracion.config(state="normal")
        self.entry_duracion.insert(0, duracion)
        self.entry_duracion.config(state="readonly")

        #BOTONES DE LA PESTAÑA PARA AGRGAR --> ACEPTAR Y CANCELAR
        frame_botones = ttk.Frame(self.cargar_ventana)
        frame_botones.pack(pady=15)

        btn_aceptar = ttk.Button(frame_botones, text="Aceptar", command=self.guardar_cancion)
        btn_aceptar.grid(row=0, column=0, padx=10)

        btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=self.cargar_ventana.destroy)
        btn_cancelar.grid(row=0, column=1, padx=10)
        
    
    def seleccionar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos MP3", "*.mp3")])
        if ruta:
            # Obtener duración automáticamente
            duracion = self.obtener_duracion(ruta)
            self.entry_duracion.config(state="normal")
            self.entry_duracion.delete(0, tk.END)
            self.entry_duracion.insert(0, duracion)
            self.entry_duracion.config(state="readonly")
            self.ruta_seleccionada = ruta

    def guardar_cancion(self):
        nombre = self.entry_nombre.get()
        artista = self.entry_artista.get()
        duracion = self.entry_duracion.get()

        if nombre and artista and duracion and hasattr(self, 'ruta_seleccionada'):
            nodo = NodoCancion(nombre, artista, duracion, self.ruta_seleccionada)
            self.lista.agregar(nodo)
            self.actualizar_lista_widget()
            self.cargar_ventana.destroy()  # Cerrar la ventana de carga

    def actualizar_lista_widget(self):
        self.lista_widget.delete(0, tk.END)
        for nodo in self.lista.obtener_lista():
            self.lista_widget.insert(tk.END, str(nodo))

    def reproducir(self):
        nodo = self.lista.obtener_actual()
        if nodo:
            if self.en_pausa:
                mixer.music.unpause()
                self.en_pausa = False
            else:
                mixer.music.load(nodo.ruta)
                mixer.music.play()
                self.en_reproduccion = True
                self.label.config(text=f"🎶 {nodo.nombre} - {nodo.artista}")
                self.slider.config(to=self.obtener_duracion_estimada(nodo.duracion))
                threading.Thread(target=self.actualizar_slider, daemon=True).start()

    def pausar(self):
        if mixer.music.get_busy():
            mixer.music.pause()
            self.en_pausa = True

    def detener(self):
        mixer.music.stop()
        self.en_reproduccion = False
        self.label.config(text="🎶 Canción actual: Ninguna")
        self.slider.set(0)
        self.label_tiempo.config(text="00:00 / 00:00")

    def siguiente(self):
        self.lista.siguiente()
        self.en_pausa = False
        self.reproducir()

    def anterior(self):
        self.lista.anterior()
        self.en_pausa = False
        self.reproducir()

    def mover_slider(self, val):
        if self.en_reproduccion:
            if not self.actualizando_slider:
                mixer.music.play(start=float(val))
                self.en_pausa = False

    def obtener_duracion(self, ruta):
        return

    def obtener_duracion_estimada(self, duracion_str):
        return

    def actualizar_slider(self):
        return

    def formato_tiempo(self, segundos):
        return


reproductor = Reproductor()
reproductor.mainloop()
