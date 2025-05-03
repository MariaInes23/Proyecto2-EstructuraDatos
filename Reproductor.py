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


