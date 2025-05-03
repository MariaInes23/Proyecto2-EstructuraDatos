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
        return
    
    def seleccionar_archivo(self):
        return

    def guardar_cancion(self):
        return

    def actualizar_lista_widget(self):
        return

    def reproducir(self):
        return

    def pausar(self):
        return
    
    def detener(self):
        return
    
    def siguiente(self):
        return

    def anterior(self):
        return

    def mover_slider(self, val):
        return

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
