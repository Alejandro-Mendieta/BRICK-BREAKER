import pygame
import random
import math
import sys
import os
from enum import Enum

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()

# Configuración de pantalla
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌟Brick Breaker🌟")

# Colores cósmicos mejorados
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
NEGRO_COSMICO = (5, 5, 15)
AZUL_PROFUNDO = (10, 15, 40)
PURPURA_ESPACIAL = (25, 10, 35)
ROJO = (255, 0, 0)

# Paleta de colores cósmicos ultra vibrantes
COLORES_COSMICOS = [
    (0, 255, 255),      # CYAN NEBULOSA - Energía pura
    (150, 50, 255),     # PÚRPURA QUÁSAR - Materia oscura
    (255, 50, 150),     # ROSA SUPERNOVA - Explosión estelar
    (255, 255, 0),      # AMARILLO SOLAR - Estrella central
    (50, 255, 150),     # VERDE EXTRATERRESTRE - Vida alien
    (255, 150, 0),      # NARANJA ESTELAR - Gigante roja
    (255, 0, 255),      # MAGENTA CÓSMICO - Agujero de gusano
    (0, 200, 255),      # AZUL NEBULOSA
    (255, 100, 255),    # ROSA GALÁCTICO
    (100, 255, 200),    # VERDE ALIENÍGENA
    (255, 200, 50),     # ORO ESTELAR
    (180, 70, 250),     # PÚRPURA PROFUNDO
    (255, 100, 100),    # ROJO SUPERNOVA
    (70, 200, 255),     # AZUL ELECTRÓNICO
    (255, 255, 150)     # AMARILLO NEUTRÓN
]

# Estados del juego
class EstadoJuego(Enum):
    MENU = 0
    JUGANDO = 1
    PAUSA = 2
    GAME_OVER = 3
    VICTORIA = 4
    SELECCION_NIVEL = 5
    TRANSICION = 6

# Sistema de partículas ultra mejorado
particulas = []
estrellas_fondo = []
nebulosas = []

class Nebulosa:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(100, 300)
        self.color = random.choice(COLORES_COSMICOS)
        self.alpha = random.randint(10, 40)
        self.pulse_speed = random.uniform(0.001, 0.005)
        self.pulse_offset = random.uniform(0, math.pi * 2)
    
    def update(self):
        self.alpha = 20 + 15 * math.sin(pygame.time.get_ticks() * self.pulse_speed + self.pulse_offset)
    
    def draw(self, surface):
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        for i in range(3):
            radius = self.size - i * 20
            alpha = max(0, self.alpha - i * 10)
            if radius > 0:
                color_with_alpha = (*self.color, alpha)
                pygame.draw.circle(surf, color_with_alpha, (self.size, self.size), radius)
        surface.blit(surf, (self.x - self.size, self.y - self.size))

class Estrella:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.uniform(0.5, 3.0)
        self.speed = random.uniform(0.05, 0.2)
        self.brightness = random.uniform(0.3, 1.0)
        self.twinkle_speed = random.uniform(0.005, 0.02)
        self.twinkle_offset = random.uniform(0, math.pi * 2)
        self.color = random.choice([(255, 255, 255), (255, 255, 200), (200, 220, 255)])
    
    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
        
        self.brightness = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() * self.twinkle_speed + self.twinkle_offset)
    
    def draw(self, surface):
        color_value = int(255 * self.brightness)
        color = (
            min(255, self.color[0] * self.brightness),
            min(255, self.color[1] * self.brightness),
            min(255, self.color[2] * self.brightness)
        )
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

class Particula:
    def __init__(self, x, y, tipo="estrella", color=None, size_multiplier=1.0):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.life = random.uniform(40, 120)
        self.max_life = self.life
        self.size = random.uniform(1, 4) * size_multiplier
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.color = color or random.choice(COLORES_COSMICOS)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-8, 8)
        self.glow_size = self.size * 2
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.08
        self.rotation += self.rotation_speed
        self.life -= 1
        
        # Efecto de desvanecimiento
        life_ratio = self.life / self.max_life
        self.glow_size = self.size * 2 * life_ratio
        
        return self.life > 0
    
    def draw(self, surface):
        alpha = min(255, int(self.life * 2))
        current_size = self.size * (self.life / self.max_life)
        
        if self.tipo == "estrella":
            # Dibujar halo de luz
            surf_glow = pygame.Surface((self.glow_size * 2, self.glow_size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha // 2)
            pygame.draw.circle(surf_glow, color_with_alpha, 
                             (self.glow_size, self.glow_size), self.glow_size)
            surface.blit(surf_glow, (self.x - self.glow_size, self.y - self.glow_size))
            
            # Dibujar estrella giratoria
            points = []
            for i in range(5):
                angle = self.rotation + i * 72
                rad = math.radians(angle)
                x = self.x + math.cos(rad) * current_size
                y = self.y + math.sin(rad) * current_size
                points.append((x, y))
                
            surf_star = pygame.Surface((current_size * 4, current_size * 4), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            pygame.draw.polygon(surf_star, color_with_alpha, points)
            surface.blit(surf_star, (self.x - current_size * 2, self.y - current_size * 2))
            
        elif self.tipo == "energia":
            # Partícula de energía con efecto de pulso
            pulse = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.1)
            size_pulse = current_size * pulse
            
            surf_energy = pygame.Surface((size_pulse * 2, size_pulse * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            pygame.draw.circle(surf_energy, color_with_alpha, 
                             (size_pulse, size_pulse), size_pulse)
            surface.blit(surf_energy, (self.x - size_pulse, self.y - size_pulse))
            
        else:
            # Partícula normal con glow
            surf_glow = pygame.Surface((self.glow_size * 2, self.glow_size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha // 2)
            pygame.draw.circle(surf_glow, color_with_alpha, 
                             (self.glow_size, self.glow_size), self.glow_size)
            surface.blit(surf_glow, (self.x - self.glow_size, self.y - self.glow_size))
            
            surf_particle = pygame.Surface((current_size * 2, current_size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            pygame.draw.circle(surf_particle, color_with_alpha, 
                             (current_size, current_size), current_size)
            surface.blit(surf_particle, (self.x - current_size, self.y - current_size))

def crear_particulas(x, y, cantidad=20, tipo="estrella", color=None, size_multiplier=1.0):
    for _ in range(cantidad):
        particulas.append(Particula(x, y, tipo, color, size_multiplier))

def crear_explosion_cosmica(x, y, color, cantidad=30):
    for _ in range(cantidad):
        particulas.append(Particula(x, y, "estrella", color, 1.5))
        particulas.append(Particula(x, y, "energia", color, 1.2))

def crear_lluvia_estelar(x, y, color):
    for _ in range(15):
        particulas.append(Particula(x, y, "estrella", color, 2.0))

# Inicializar fondo espacial
for _ in range(5):
    nebulosas.append(Nebulosa())

for _ in range(300):
    estrellas_fondo.append(Estrella())

# Sistema de niveles ultra mejorado
class Nivel:
    def __init__(self, numero, nombre, descripcion, patron_ladrillos, velocidad_pelota=5, 
                 velocidad_raqueta=8, vidas=3, tiempo_limite=None, tema_especial=None):
        self.numero = numero
        self.nombre = nombre
        self.descripcion = descripcion
        self.patron_ladrillos = patron_ladrillos
        self.velocidad_pelota = velocidad_pelota
        self.velocidad_raqueta = velocidad_raqueta
        self.vidas_iniciales = vidas
        self.tiempo_limite = tiempo_limite
        self.tema_especial = tema_especial
        self.desbloqueado = numero == 1
        self.estrellas = 0
        self.mejor_puntuacion = 0
        self.completado = False
        self.fondo_color = (
            random.randint(10, 30),
            random.randint(10, 20),
            random.randint(30, 50)
        )
    
    def calcular_estrellas(self, puntuacion, vidas_restantes, tiempo_restante):
        estrellas = 1  # Estrella base por completar
        
        if puntuacion >= 1500 + (self.numero * 200):
            estrellas += 1
                
        if vidas_restantes >= self.vidas_iniciales - 1:
            estrellas += 1
                
        self.estrellas = max(self.estrellas, estrellas)
        return estrellas

# Generar patrones de niveles más interesantes
def generar_patron_espiral(filas, columnas):
    patron = [[0 for _ in range(columnas)] for _ in range(filas)]
    direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir_idx = 0
    i, j = 0, 0
    resistencia = 1
    
    for _ in range(filas * columnas):
        if 0 <= i < filas and 0 <= j < columnas:
            patron[i][j] = resistencia
            resistencia = (resistencia % 3) + 1
        
        next_i = i + direcciones[dir_idx][0]
        next_j = j + direcciones[dir_idx][1]
        
        if (next_i < 0 or next_i >= filas or next_j < 0 or next_j >= columnas or 
            patron[next_i][next_j] != 0):
            dir_idx = (dir_idx + 1) % 4
            next_i = i + direcciones[dir_idx][0]
            next_j = j + direcciones[dir_idx][1]
        
        i, j = next_i, next_j
    
    return patron

def generar_patron_galaxia(filas, columnas):
    patron = [[0 for _ in range(columnas)] for _ in range(filas)]
    centro_x, centro_y = columnas // 2, filas // 2
    
    for i in range(filas):
        for j in range(columnas):
            dist = math.sqrt((i - centro_y)**2 + (j - centro_x)**2)
            if dist < min(centro_x, centro_y):
                # Resistencia basada en la distancia al centro
                resistencia = max(1, min(3, int(4 - dist / (min(centro_x, centro_y) / 3))))
                patron[i][j] = resistencia if random.random() < 0.8 else 0
    
    return patron

def generar_patron_aleatorio(filas, columnas, densidad=0.7):
    """Genera un patrón aleatorio de ladrillos"""
    patron = [[0 for _ in range(columnas)] for _ in range(filas)]
    for i in range(filas):
        for j in range(columnas):
            if random.random() < densidad:
                patron[i][j] = random.randint(1, 3)
    return patron

def generar_patron_lineas(filas, columnas):
    """Genera un patrón de líneas alternadas"""
    patron = [[0 for _ in range(columnas)] for _ in range(filas)]
    for i in range(filas):
        if i % 2 == 0:
            for j in range(columnas):
                patron[i][j] = (j % 3) + 1
    return patron

def generar_patron_marco(filas, columnas):
    """Genera un patrón de marco"""
    patron = [[0 for _ in range(columnas)] for _ in range(filas)]
    for i in range(filas):
        for j in range(columnas):
            if i == 0 or i == filas-1 or j == 0 or j == columnas-1:
                patron[i][j] = random.randint(2, 3)
    return patron

def generar_patron_diamante(filas, columnas):
    """Genera un patrón en forma de diamante"""
    patron = [[0 for _ in range(columnas)] for _ in range(filas)]
    centro_x, centro_y = columnas // 2, filas // 2
    
    for i in range(filas):
        for j in range(columnas):
            dist_x = abs(j - centro_x)
            dist_y = abs(i - centro_y)
            if dist_x + dist_y <= min(centro_x, centro_y):
                resistencia = max(1, 3 - (dist_x + dist_y) // 2)
                patron[i][j] = resistencia
    return patron

def generar_patron_cruz(filas, columnas):
    """Genera un patrón en forma de cruz"""
    patron = [[0 for _ in range(columnas)] for _ in range(filas)]
    centro_x, centro_y = columnas // 2, filas // 2
    
    for i in range(filas):
        for j in range(columnas):
            if i == centro_y or j == centro_x:
                distancia = max(abs(i - centro_y), abs(j - centro_x))
                resistencia = max(1, 3 - distancia // 2)
                patron[i][j] = resistencia
    return patron

# Generar 100 niveles épicos
niveles = []
temas_especiales = [
    "Nebulosa del Cangrejo", "Galaxia Andrómeda", "Cúmulo de Virgo",
    "Supernova Cassiopeia", "Agujero Negro Sagitario", "Quásar 3C273",
    "Púlsar del Cangrejo", "Nube de Magallanes", "Cinturón de Orión",
    "Vía Láctea Central", "Nebulosa del Águila", "Galaxia del Sombrero",
    "Cúmulo Estelar Pléyades", "Nebulosa de la Hélice", "Galaxia del Molinete",
    "Nebulosa de Orión", "Galaxia del Triángulo", "Cúmulo de Hércules",
    "Nebulosa de la Laguna", "Galaxia del Remolino", "Nebulosa de la Tarántula",
    "Galaxia de Bode", "Nebulosa del Anillo", "Galaxia de la Rueda de Carro",
    "Nebulosa de la Hormiga", "Galaxia del Ojo Negro", "Nebulosa del Corazón",
    "Galaxia del Girasol", "Nebulosa del Casco de Thor", "Galaxia de Centauro A",
    "Nebulosa de la Roseta", "Galaxia de la Ballena", "Nebulosa del Velo",
    "Galaxia de la Aguja", "Nebulosa de la Flama", "Galaxia de Sculptor",
    "Nebulosa de la Medusa", "Galaxia de Leo", "Nebulosa del Cangrejo Austral",
    "Galaxia de Draco", "Nebulosa de la Mariposa", "Galaxia de Ursa Major",
    "Nebulosa de la Hélice Sur", "Galaxia de Pegaso", "Nebulosa de la Burbuja",
    "Galaxia de Andrómeda II", "Nebulosa de Omega", "Galaxia de Virgo A",
    "Nebulosa de la Gaviota", "Galaxia del Molinete Sur"
]

# Generar 100 niveles
for i in range(1, 101):
    # Configuración progresiva de dificultad
    if i <= 20:
        # Niveles 1-20: Básicos
        filas = 4 + (i // 4)
        columnas = 6 + (i // 2)
        if i % 5 == 0:
            patron = generar_patron_espiral(filas, columnas)
            tema = "Espiral Cósmica"
        elif i % 5 == 1:
            patron = generar_patron_lineas(filas, columnas)
            tema = "Líneas Estelares"
        elif i % 5 == 2:
            patron = generar_patron_marco(filas, columnas)
            tema = "Marco Galáctico"
        else:
            patron = generar_patron_aleatorio(filas, columnas, 0.6 + (i * 0.01))
            tema = "Campo Estelar"
            
    elif i <= 40:
        # Niveles 21-40: Intermedios
        filas = 6 + ((i - 20) // 5)
        columnas = 10 + ((i - 20) // 3)
        if i % 6 == 0:
            patron = generar_patron_galaxia(filas, columnas)
            tema = "Galaxia Espiral"
        elif i % 6 == 1:
            patron = generar_patron_diamante(filas, columnas)
            tema = "Diamante Cósmico"
        elif i % 6 == 2:
            patron = generar_patron_cruz(filas, columnas)
            tema = "Cruz Estelar"
        else:
            patron = generar_patron_aleatorio(filas, columnas, 0.7 + ((i - 20) * 0.008))
            tema = "Cúmulo Estelar"
            
    elif i <= 60:
        # Niveles 41-60: Avanzados
        filas = 8 + ((i - 40) // 4)
        columnas = 12 + ((i - 40) // 2)
        if i % 4 == 0:
            patron = generar_patron_espiral(filas, columnas)
            tema = "Espiral Profunda"
        elif i % 4 == 1:
            patron = generar_patron_galaxia(filas, columnas)
            tema = "Galaxia Activa"
        else:
            patron = generar_patron_aleatorio(filas, columnas, 0.75 + ((i - 40) * 0.006))
            tema = "Nebulosa Densa"
            
    elif i <= 80:
        # Niveles 61-80: Expertos
        filas = 10 + ((i - 60) // 3)
        columnas = 14 + ((i - 60) // 2)
        if i % 3 == 0:
            patron = generar_patron_diamante(filas, columnas)
            tema = "Diamante Quántico"
        elif i % 3 == 1:
            patron = generar_patron_cruz(filas, columnas)
            tema = "Cruz Cósmica"
        else:
            patron = generar_patron_aleatorio(filas, columnas, 0.8 + ((i - 60) * 0.005))
            tema = "Agujero Negro"
            
    else:
        # Niveles 81-100: Maestros
        filas = 12 + ((i - 80) // 2)
        columnas = 16 + ((i - 80) // 2)
        if i % 2 == 0:
            patron = generar_patron_espiral(filas, columnas)
            tema = "Espiral Maestra"
        else:
            patron = generar_patron_aleatorio(filas, columnas, 0.85 + ((i - 80) * 0.004))
            tema = temas_especiales[(i - 81) % len(temas_especiales)]
    
    # Configuración de dificultad progresiva
    velocidad_pelota = 4 + (i // 10)
    velocidad_raqueta = 7 + (i // 15)
    vidas = max(1, 1 - (i // 20))
    
    # Tiempo límite para niveles más altos
    if i >= 30:
        tiempo_limite = max(30, 120 - i)
    else:
        tiempo_limite = None
    
    nombre = f"{tema} {i}"
    descripcion = f"Desafío nivel {i} - {tema}"
    
    niveles.append(Nivel(i, nombre, descripcion, patron, velocidad_pelota, 
                      velocidad_raqueta, vidas, tiempo_limite, tema))

# Fuentes mejoradas
try:
    fuente_pequena = pygame.font.SysFont("arial", 16)
    fuente_media = pygame.font.SysFont("arial", 20)
    fuente_grande = pygame.font.SysFont("arial", 28)
    fuente_titulo = pygame.font.SysFont("arial", 48, bold=True)
    fuente_enorme = pygame.font.SysFont("arial", 72, bold=True)
    fuente_cosmica = pygame.font.SysFont("arial", 36)
except:
    fuente_pequena = pygame.font.Font(None, 16)
    fuente_media = pygame.font.Font(None, 20)
    fuente_grande = pygame.font.Font(None, 28)
    fuente_titulo = pygame.font.Font(None, 48)
    fuente_enorme = pygame.font.Font(None, 72)
    fuente_cosmica = pygame.font.Font(None, 36)

# Clase Raqueta con efectos mejorados
class Raqueta:
    def __init__(self, velocidad=8):
        self.ancho_base = 120
        self.ancho = self.ancho_base
        self.alto = 20
        self.x = WIDTH // 2 - self.ancho // 2
        self.y = HEIGHT - 80
        self.velocidad = velocidad
        self.color = COLORES_COSMICOS[0]  # Cyan Nebulosa
        self.efecto_luz = 0
        self.energia = 0
        self.ultimo_movimiento = 0
        
    def dibujar(self, surface):
        # Efecto de estela al moverse
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_movimiento < 100:
            for i in range(3):
                alpha = 100 - i * 30
                ancho_estela = self.ancho - i * 10
                x_estela = self.x + i * 3
                surf_estela = pygame.Surface((ancho_estela, self.alto), pygame.SRCALPHA)
                color_with_alpha = (*self.color, alpha)
                pygame.draw.rect(surf_estela, color_with_alpha, 
                               (0, 0, ancho_estela, self.alto), border_radius=8)
                surface.blit(surf_estela, (x_estela, self.y))
        
        # Efecto de luz de energía
        if self.efecto_luz > 0:
            surf_luz = pygame.Surface((self.ancho + 40, self.alto + 40), pygame.SRCALPHA)
            for i in range(4):
                alpha = 80 - i * 20
                size_reduction = i * 6
                color_with_alpha = (*self.color, alpha)
                pygame.draw.rect(surf_luz, color_with_alpha, 
                               (size_reduction, size_reduction, 
                                self.ancho + 40 - size_reduction * 2, 
                                self.alto + 40 - size_reduction * 2), 
                               border_radius=12)
            surface.blit(surf_luz, (self.x - 20, self.y - 20))
            self.efecto_luz -= 3
        
        # Raqueta principal con gradiente
        surf_raqueta = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        for i in range(self.ancho):
            progress = i / self.ancho
            r = int(self.color[0] * (1 - progress) + 255 * progress)
            g = int(self.color[1] * (1 - progress) + 255 * progress)
            b = int(self.color[2] * (1 - progress) + 255 * progress)
            pygame.draw.rect(surf_raqueta, (r, g, b), (i, 0, 1, self.alto))
        
        pygame.draw.rect(surf_raqueta, BLANCO, (0, 0, self.ancho, self.alto), 2, border_radius=8)
        surface.blit(surf_raqueta, (self.x, self.y))
        
        # Núcleo de energía central
        if self.energia > 0:
            surf_nucleo = pygame.Surface((20, 20), pygame.SRCALPHA)
            color_with_alpha = (255, 255, 200, self.energia)
            pygame.draw.circle(surf_nucleo, color_with_alpha, (10, 10), 8)
            surface.blit(surf_nucleo, (self.x + self.ancho//2 - 10, self.y - 5))
            self.energia -= 2
    
    def mover(self, direccion):
        self.ultimo_movimiento = pygame.time.get_ticks()
        
        if direccion == "izquierda" and self.x > 0:
            self.x -= self.velocidad
            crear_particulas(self.x + self.ancho, self.y + self.alto//2, 2, "energia", self.color)
        if direccion == "derecha" and self.x < WIDTH - self.ancho:
            self.x += self.velocidad
            crear_particulas(self.x, self.y + self.alto//2, 2, "energia", self.color)
    
    def activar_efecto(self):
        self.efecto_luz = 120
        self.energia = 200
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

# Clase Pelota con efectos mejorados
class Pelota:
    def __init__(self, velocidad=5):
        self.radio_base = 12
        self.radio = self.radio_base
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.velocidad_x = velocidad * random.choice([-1, 1])
        self.velocidad_y = -velocidad
        self.color = COLORES_COSMICOS[3]  # Amarillo Solar
        self.activa = True
        self.trail = []
        self.energia = 0
        self.pulse = 0
        
    def dibujar(self, surface):
        # Dibujar trail de energía
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = 150 - i * 25
            size = self.radio * (alpha / 150)
            if alpha > 0:
                surf_trail = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                color_with_alpha = (*self.color, alpha)
                pygame.draw.circle(surf_trail, color_with_alpha, (size, size), size)
                surface.blit(surf_trail, (trail_x - size, trail_y - size))
        
        # Efecto de pulso de energía
        pulse_factor = 1.0 + 0.2 * math.sin(self.pulse)
        current_radius = self.radio * pulse_factor
        
        # Halo de energía
        if self.energia > 0:
            surf_halo = pygame.Surface((current_radius * 4, current_radius * 4), pygame.SRCALPHA)
            color_with_alpha = (*self.color, self.energia // 2)
            pygame.draw.circle(surf_halo, color_with_alpha, 
                             (current_radius * 2, current_radius * 2), current_radius * 2)
            surface.blit(surf_halo, (self.x - current_radius * 2, self.y - current_radius * 2))
        
        # Pelota principal
        surf_pelota = pygame.Surface((current_radius * 2, current_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf_pelota, self.color, (current_radius, current_radius), current_radius)
        
        # Núcleo brillante
        nucleo_size = current_radius * 0.6
        pygame.draw.circle(surf_pelota, (255, 255, 200), 
                         (current_radius, current_radius), nucleo_size)
        
        # Efecto de energía interna
        if self.energia > 0:
            energy_size = current_radius * 0.3
            color_with_alpha = (255, 255, 255, self.energia)
            pygame.draw.circle(surf_pelota, color_with_alpha, 
                             (current_radius, current_radius), energy_size)
        
        surface.blit(surf_pelota, (self.x - current_radius, self.y - current_radius))
        
        # Actualizar trail y efectos
        self.trail.insert(0, (self.x, self.y))
        if len(self.trail) > 8:
            self.trail.pop()
        
        self.pulse += 0.3
        self.energia = max(0, self.energia - 3)
    
    def mover(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y
    
    def rebotar_paredes(self):
        if self.x <= self.radio or self.x >= WIDTH - self.radio:
            self.velocidad_x *= -1
            self.energia = 150
            crear_lluvia_estelar(self.x, self.y, self.color)
        
        if self.y <= self.radio:
            self.velocidad_y *= -1
            self.energia = 150
            crear_lluvia_estelar(self.x, self.y, self.color)
    
    def rebotar_raqueta(self, raqueta):
        raqueta_rect = raqueta.get_rect()
        if (self.y + self.radio >= raqueta_rect.top and 
            self.y - self.radio <= raqueta_rect.bottom and
            self.x >= raqueta_rect.left and self.x <= raqueta_rect.right):
            
            # Ángulo de rebote más preciso
            rel_x = (self.x - raqueta_rect.centerx) / (raqueta_rect.width / 2)
            angulo = rel_x * math.pi / 3
            
            # Aumentar velocidad gradualmente
            velocidad_actual = math.sqrt(self.velocidad_x**2 + self.velocidad_y**2)
            nueva_velocidad = min(velocidad_actual * 1.02, 15)  # Límite de velocidad
            
            self.velocidad_x = nueva_velocidad * math.sin(angulo)
            self.velocidad_y = -nueva_velocidad * math.cos(angulo)
            
            raqueta.activar_efecto()
            self.energia = 200
            crear_explosion_cosmica(self.x, self.y, self.color, 40)
            return True
        return False
    
    def caer(self):
        return self.y >= HEIGHT
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radio, self.y - self.radio, 
                          self.radio * 2, self.radio * 2)

# Clase Ladrillo con efectos mejorados
class Ladrillo:
    def __init__(self, x, y, ancho, alto, resistencia=1):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.resistencia = resistencia
        self.resistencia_original = resistencia
        self.visible = True
        self.color_base = random.choice(COLORES_COSMICOS)
        self.efecto_dano = 0
        self.pulse = random.uniform(0, math.pi * 2)
        self.pulse_speed = random.uniform(0.02, 0.05)
        
        if resistencia == 1:
            self.puntos = 100
            self.tipo = "básico"
        elif resistencia == 2:
            self.puntos = 250
            self.tipo = "reforzado"
        else:
            self.puntos = 500
            self.tipo = "cristal"
    
    def dibujar(self, surface):
        if not self.visible:
            return
        
        self.pulse += self.pulse_speed
        pulse_factor = 0.9 + 0.1 * math.sin(self.pulse)
        
        color = self.color_base
        
        # Efecto de daño (parpadeo)
        if self.efecto_dano > 0:
            surf_efecto = pygame.Surface((self.ancho + 10, self.alto + 10), pygame.SRCALPHA)
            flash_alpha = min(255, self.efecto_dano * 2)
            color_with_alpha = (255, 255, 255, flash_alpha)
            pygame.draw.rect(surf_efecto, color_with_alpha, 
                           (0, 0, self.ancho + 10, self.alto + 10), border_radius=6)
            surface.blit(surf_efecto, (self.x - 5, self.y - 5))
            self.efecto_dano -= 8
        
        # Ladrillo principal con efecto de pulso
        current_width = self.ancho * pulse_factor
        current_height = self.alto * pulse_factor
        current_x = self.x + (self.ancho - current_width) / 2
        current_y = self.y + (self.alto - current_height) / 2
        
        # Sombra interna
        surf_sombra = pygame.Surface((current_width, current_height), pygame.SRCALPHA)
        color_with_alpha = (*color, 200)
        pygame.draw.rect(surf_sombra, color_with_alpha, 
                       (0, 0, current_width, current_height), border_radius=6)
        
        # Efecto de brillo en los bordes
        edge_color = (min(255, color[0] + 60), min(255, color[1] + 60), min(255, color[2] + 60), 180)
        pygame.draw.rect(surf_sombra, edge_color, 
                       (0, 0, current_width, 4), border_radius=3)
        
        pygame.draw.rect(surf_sombra, BLANCO, (0, 0, current_width, current_height), 
                        2, border_radius=6)
        
        surface.blit(surf_sombra, (current_x, current_y))
        
        # Mostrar resistencia con efecto
        if self.resistencia > 1:
            texto = fuente_pequena.render(str(self.resistencia), True, BLANCO)
            text_shadow = fuente_pequena.render(str(self.resistencia), True, (0, 0, 0))
            
            # Sombra del texto
            surface.blit(text_shadow, (self.x + self.ancho//2 - texto.get_width()//2 + 1, 
                                    self.y + self.alto//2 - texto.get_height()//2 + 1))
            # Texto principal
            surface.blit(texto, (self.x + self.ancho//2 - texto.get_width()//2, 
                              self.y + self.alto//2 - texto.get_height()//2))
    
    def golpear(self):
        self.resistencia -= 1
        self.efecto_dano = 150
        
        if self.resistencia <= 0:
            self.visible = False
            crear_explosion_cosmica(self.x + self.ancho//2, self.y + self.alto//2, self.color_base, 50)
            return True, self.puntos
        return False, self.puntos // 2
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

# Clase PowerUp con efectos mejorados
class PowerUp:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.velocidad = 3
        self.ancho = 36
        self.alto = 36
        self.activo = True
        self.rotation = 0
        self.rotation_speed = 4
        self.pulse = 0
        self.glow_size = 0
        
        self.colores = {
            'raqueta_grande': (0, 255, 150),    # Verde futurista
            'raqueta_pequena': (255, 100, 100), # Rojo energético
            'multi_pelota': (255, 255, 0),      # Amarillo plasma
            'vida_extra': (0, 150, 255),        # Azul cuántico
            'lento': (200, 100, 255),           # Púrpura temporal
            'imán': (150, 200, 255)            # Azul magnético
        }
        
        self.simbolos = {
            'raqueta_grande': "⬆",
            'raqueta_pequena': "⬇", 
            'multi_pelota': "⚡",
            'vida_extra': "❤",
            'lento': "⏳",
            'imán': "🧲"
        }
    
    def dibujar(self, surface):
        if not self.activo:
            return
            
        self.rotation += self.rotation_speed
        self.pulse += 0.1
        self.glow_size = 10 + 5 * math.sin(self.pulse)
        
        # Efecto de glow
        surf_glow = pygame.Surface((self.ancho + self.glow_size * 2, 
                                  self.alto + self.glow_size * 2), pygame.SRCALPHA)
        color = self.colores.get(self.tipo, BLANCO)
        color_with_alpha = (*color, 80)
        pygame.draw.rect(surf_glow, color_with_alpha, 
                       (0, 0, self.ancho + self.glow_size * 2, self.alto + self.glow_size * 2), 
                       border_radius=10)
        surface.blit(surf_glow, (self.x - self.glow_size, self.y - self.glow_size))
        
        # Power-up principal
        surf_main = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        
        # Fondo con gradiente
        for i in range(self.ancho):
            progress = i / self.ancho
            r = int(color[0] * (1 - progress) + 255 * progress)
            g = int(color[1] * (1 - progress) + 255 * progress)
            b = int(color[2] * (1 - progress) + 255 * progress)
            pygame.draw.rect(surf_main, (r, g, b), (i, 0, 1, self.alto))
        
        pygame.draw.rect(surf_main, BLANCO, (0, 0, self.ancho, self.alto), 2, border_radius=8)
        
        # Símbolo
        texto = fuente_media.render(self.simbolos[self.tipo], True, BLANCO)
        surf_main.blit(texto, (self.ancho//2 - texto.get_width()//2, 
                             self.alto//2 - texto.get_height()//2))
        
        # Rotar y dibujar
        rotated_surf = pygame.transform.rotate(surf_main, self.rotation)
        rect = rotated_surf.get_rect(center=(self.x + self.ancho//2, self.y + self.alto//2))
        surface.blit(rotated_surf, rect)
        
        # Partículas de energía ocasionales
        if random.random() < 0.4:
            crear_particulas(self.x + self.ancho//2, self.y + self.alto//2, 
                           1, "energia", color, 0.8)
    
    def mover(self):
        self.y += self.velocidad
        if self.y > HEIGHT:
            self.activo = False
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

# Clase Juego principal mejorada
class Juego:
    def __init__(self):
        self.raqueta = None
        self.pelotas = []
        self.ladrillos = []
        self.powerups = []
        self.vidas = 3
        self.puntuacion = 0
        self.nivel_actual = None
        self.estado = EstadoJuego.MENU
        self.tiempo_inicio_nivel = 0
        self.tiempo_restante = 0
        self.combo = 0
        self.ultimo_combo_tiempo = 0
        self.pagina_actual = 0
        self.niveles_por_pagina = 12  # Mostrar 12 niveles por página para 100 niveles
        self.efectos_activos = {}
        self.transicion_tiempo = 0
        self.mensaje_especial = ""
        self.mensaje_tiempo = 0
    
    def iniciar_nivel(self, nivel):
        self.nivel_actual = nivel
        self.raqueta = Raqueta(nivel.velocidad_raqueta)
        self.pelotas = [Pelota(nivel.velocidad_pelota)]
        self.ladrillos = []
        self.powerups = []
        self.vidas = nivel.vidas_iniciales
        self.puntuacion = 0
        self.combo = 0
        self.tiempo_inicio_nivel = pygame.time.get_ticks()
        self.tiempo_restante = nivel.tiempo_limite
        self.efectos_activos = {}
        self.mostrar_mensaje(f"Nivel {nivel.numero}: {nivel.nombre}")
        
        # Crear ladrillos según el patrón del nivel
        if nivel.patron_ladrillos and len(nivel.patron_ladrillos) > 0:
            ancho_ladrillo = (WIDTH - 60) // len(nivel.patron_ladrillos[0])
            alto_ladrillo = 35
            
            for fila_idx, fila in enumerate(nivel.patron_ladrillos):
                for col_idx, resistencia in enumerate(fila):
                    if resistencia > 0:
                        x = 30 + col_idx * ancho_ladrillo
                        y = 100 + fila_idx * alto_ladrillo
                        self.ladrillos.append(Ladrillo(x, y, ancho_ladrillo - 6, alto_ladrillo - 6, resistencia))

    def mostrar_mensaje(self, mensaje):
        self.mensaje_especial = mensaje
        self.mensaje_tiempo = pygame.time.get_ticks()

    def actualizar(self):
        if self.estado != EstadoJuego.JUGANDO or not self.nivel_actual:
            return
        
        # Actualizar tiempo restante
        if self.nivel_actual.tiempo_limite:
            tiempo_transcurrido = (pygame.time.get_ticks() - self.tiempo_inicio_nivel) // 1000
            self.tiempo_restante = max(0, self.nivel_actual.tiempo_limite - tiempo_transcurrido)
            
            if self.tiempo_restante <= 0:
                self.estado = EstadoJuego.GAME_OVER
                return
        
        # Actualizar combo
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_combo_tiempo > 2000:
            if self.combo > 0:
                self.mostrar_mensaje(f"Combo perdido! x{self.combo + 1}")
            self.combo = 0
        
        # Actualizar mensajes especiales
        if tiempo_actual - self.mensaje_tiempo > 2000:
            self.mensaje_especial = ""
        
        # Actualizar powerups
        for powerup in self.powerups[:]:
            powerup.mover()
            if not powerup.activo:
                self.powerups.remove(powerup)
            elif powerup.get_rect().colliderect(self.raqueta.get_rect()):
                self.aplicar_powerup(powerup)
                self.powerups.remove(powerup)
        
        # Actualizar efectos activos
        for efecto in list(self.efectos_activos.keys()):
            if self.efectos_activos[efecto] > 0:
                self.efectos_activos[efecto] -= 1
                if self.efectos_activos[efecto] <= 0:
                    self.revertir_efecto(efecto)
        
        # Actualizar pelotas
        for pelota in self.pelotas[:]:
            if not pelota.activa:
                continue
                
            pelota.mover()
            pelota.rebotar_paredes()
            
            # Rebotar con la raqueta
            if pelota.rebotar_raqueta(self.raqueta):
                self.puntuacion += 10 * (self.combo + 1)
                self.combo += 1
                self.ultimo_combo_tiempo = tiempo_actual
                if self.combo >= 3:
                    self.mostrar_mensaje(f"COMBO x{self.combo + 1}! +{10 * (self.combo + 1)} puntos")
            
            # Verificar si la pelota cae
            if pelota.caer():
                pelota.activa = False
                self.pelotas.remove(pelota)
                crear_explosion_cosmica(pelota.x, pelota.y, ROJO, 40)
                
                # Si no quedan pelotas, perder vida
                if not any(p.activa for p in self.pelotas):
                    self.vidas -= 1
                    if self.combo > 0:
                        self.mostrar_mensaje(f"Combo perdido! -1 vida")
                    self.combo = 0
                    if self.vidas > 0:
                        # Nueva pelota desde la raqueta
                        nueva_pelota = Pelota(self.nivel_actual.velocidad_pelota)
                        nueva_pelota.x = self.raqueta.x + self.raqueta.ancho // 2
                        nueva_pelota.y = self.raqueta.y - 30
                        self.pelotas.append(nueva_pelota)
                        self.mostrar_mensaje(f"Vidas restantes: {self.vidas}")
                    else:
                        self.estado = EstadoJuego.GAME_OVER
                        crear_explosion_cosmica(WIDTH//2, HEIGHT//2, ROJO, 100)
            
            # Colisiones con ladrillos
            for ladrillo in self.ladrillos[:]:
                if ladrillo.visible and pelota.get_rect().colliderect(ladrillo.get_rect()):
                    # Determinar dirección del rebote
                    dx = pelota.x - (ladrillo.x + ladrillo.ancho/2)
                    dy = pelota.y - (ladrillo.y + ladrillo.alto/2)
                    
                    if abs(dx) > abs(dy):
                        pelota.velocidad_x *= -1
                    else:
                        pelota.velocidad_y *= -1
                    
                    # Golpear ladrillo
                    destruido, puntos = ladrillo.golpear()
                    puntos_con_combo = puntos * (self.combo + 1)
                    self.puntuacion += puntos_con_combo
                    
                    if destruido:
                        self.ladrillos.remove(ladrillo)
                        self.combo += 1
                        self.ultimo_combo_tiempo = tiempo_actual
                        
                        # Mensaje especial para cristales
                        if ladrillo.tipo == "cristal":
                            self.mostrar_mensaje("¡CRISTAL DESTRUIDO! +500 puntos")
                        
                        # Posibilidad de soltar powerup (mayor probabilidad en combos altos)
                        prob_powerup = 0.15 + (min(self.combo, 10) * 0.02)
                        if random.random() < prob_powerup:
                            tipos = ['raqueta_grande', 'raqueta_pequena', 'multi_pelota', 'vida_extra', 'lento', 'imán']
                            pesos = [0.2, 0.1, 0.25, 0.15, 0.1, 0.2]  # multi_pelota más común
                            tipo = random.choices(tipos, weights=pesos)[0]
                            self.powerups.append(PowerUp(ladrillo.x + ladrillo.ancho//2, 
                                                       ladrillo.y + ladrillo.alto//2, tipo))
                    
                    crear_particulas(ladrillo.x + ladrillo.ancho//2, 
                                   ladrillo.y + ladrillo.alto//2, 
                                   15, "estrella", ladrillo.color_base)
                    break
        
        # Verificar si se completó el nivel
        if not any(ladrillo.visible for ladrillo in self.ladrillos):
            estrellas = self.nivel_actual.calcular_estrellas(
                self.puntuacion, self.vidas, self.tiempo_restante
            )
            self.nivel_actual.mejor_puntuacion = max(self.nivel_actual.mejor_puntuacion, self.puntuacion)
            self.nivel_actual.completado = True
            
            # Desbloquear siguiente nivel si existe
            nivel_actual_idx = niveles.index(self.nivel_actual)
            if nivel_actual_idx + 1 < len(niveles):
                niveles[nivel_actual_idx + 1].desbloqueado = True
            
            # Efecto de victoria
            for _ in range(5):
                crear_explosion_cosmica(random.randint(100, WIDTH-100), 
                                      random.randint(100, HEIGHT-100), 
                                      random.choice(COLORES_COSMICOS), 30)
            
            self.estado = EstadoJuego.VICTORIA
    
    def aplicar_powerup(self, powerup):
        tipo = powerup.tipo
        color = powerup.colores[tipo]
        
        if tipo == 'raqueta_grande':
            self.raqueta.ancho = min(200, self.raqueta.ancho + 40)
            self.efectos_activos['raqueta_grande'] = 600  # 10 segundos
            self.mostrar_mensaje("¡RAQUETA GRANDE! +40px")
        elif tipo == 'raqueta_pequena':
            self.raqueta.ancho = max(60, self.raqueta.ancho - 30)
            self.efectos_activos['raqueta_pequena'] = 600
            self.mostrar_mensaje("¡RAQUETA PEQUEÑA! -30px")
        elif tipo == 'multi_pelota':
            for _ in range(2):
                if len(self.pelotas) < 5:
                    nueva_pelota = Pelota(self.nivel_actual.velocidad_pelota)
                    nueva_pelota.x = self.raqueta.x + self.raqueta.ancho // 2
                    nueva_pelota.y = self.raqueta.y - 30
                    nueva_pelota.velocidad_x = random.uniform(-4, 4)
                    nueva_pelota.velocidad_y = -self.nivel_actual.velocidad_pelota
                    nueva_pelota.color = random.choice(COLORES_COSMICOS)
                    self.pelotas.append(nueva_pelota)
            self.mostrar_mensaje("¡MÚLTIPLES PELOTAS!")
        elif tipo == 'vida_extra':
            self.vidas += 1
            self.mostrar_mensaje("¡VIDA EXTRA! +1")
        elif tipo == 'lento':
            for pelota in self.pelotas:
                pelota.velocidad_x *= 0.6
                pelota.velocidad_y *= 0.6
            self.efectos_activos['lento'] = 300  # 5 segundos
            self.mostrar_mensaje("¡CÁMARA LENTA! Velocidad -40%")
        elif tipo == 'imán':
            self.efectos_activos['imán'] = 450  # 7.5 segundos
            self.mostrar_mensaje("¡CAMPO MAGNÉTICO! Atrae power-ups")
        
        crear_explosion_cosmica(self.raqueta.x + self.raqueta.ancho//2, 
                              self.raqueta.y, color, 50)
    
    def revertir_efecto(self, efecto):
        if efecto == 'raqueta_grande':
            self.raqueta.ancho = self.raqueta.ancho_base
        elif efecto == 'raqueta_pequena':
            self.raqueta.ancho = self.raqueta.ancho_base
        elif efecto == 'lento':
            for pelota in self.pelotas:
                pelota.velocidad_x /= 0.6
                pelota.velocidad_y /= 0.6

# Funciones de dibujo para cada estado del juego
def dibujar_menu(juego):
    # Título principal con efecto brillante
    tiempo = pygame.time.get_ticks() * 0.002
    brillo = 0.5 + 0.5 * math.sin(tiempo)
    color_titulo = (
        int(100 + 155 * brillo),
        int(150 + 105 * brillo),
        int(255 + 0 * brillo)
    )
    
    titulo_texto = fuente_enorme.render("BRICK BREAKER", True, color_titulo)
    titulo_rect = titulo_texto.get_rect(center=(WIDTH//2, HEIGHT//4))
    
    # Sombra del título
    sombra_texto = fuente_enorme.render("BRICK BREAKER", True, (0, 0, 0))
    screen.blit(sombra_texto, (titulo_rect.x + 4, titulo_rect.y + 4))
    screen.blit(titulo_texto, titulo_rect)
    
    # Subtítulo
    subtitulo = fuente_cosmica.render("", True, COLORES_COSMICOS[0])
    screen.blit(subtitulo, (WIDTH//2 - subtitulo.get_width()//2, HEIGHT//4 + 80))
    
    # Botones del menú
    opciones = ["INICIAR", "SELECCIONAR", "SALIR"]
    y_pos = HEIGHT // 2
    
    for i, opcion in enumerate(opciones):
        color = COLORES_COSMICOS[i % len(COLORES_COSMICOS)]
        texto = fuente_grande.render(opcion, True, color)
        rect = texto.get_rect(center=(WIDTH//2, y_pos + i * 70))
        
        # Efecto hover
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            surf_hover = pygame.Surface((rect.width + 20, rect.height + 10), pygame.SRCALPHA)
            pygame.draw.rect(surf_hover, (*color, 30), (0, 0, rect.width + 20, rect.height + 10), border_radius=10)
            screen.blit(surf_hover, (rect.x - 10, rect.y - 5))
            crear_particulas(mouse_pos[0], mouse_pos[1], 2, "energia", color)
        
        screen.blit(texto, rect)

def dibujar_seleccion_nivel(juego):
    # Título
    titulo = fuente_titulo.render("SELECCIÓN DE NIVEL - 100 NIVELES", True, BLANCO)
    screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 50))
    
    # Información de páginas
    total_paginas = (len(niveles) + juego.niveles_por_pagina - 1) // juego.niveles_por_pagina
    pagina_info = fuente_media.render(f"Página {juego.pagina_actual + 1}/{total_paginas}", True, BLANCO)
    screen.blit(pagina_info, (WIDTH//2 - pagina_info.get_width()//2, 120))
    
    # Cuadrícula de niveles - 4 filas x 3 columnas para 12 niveles por página
    niveles_por_fila = 3
    nivel_size = 120
    margen = 40
    inicio_x = (WIDTH - (niveles_por_fila * nivel_size + (niveles_por_fila - 1) * margen)) // 2
    inicio_y = 180
    
    for i in range(juego.niveles_por_pagina):
        nivel_idx = juego.pagina_actual * juego.niveles_por_pagina + i
        if nivel_idx >= len(niveles):
            break
            
        nivel = niveles[nivel_idx]
        fila = i // niveles_por_fila
        columna = i % niveles_por_fila
        
        x = inicio_x + columna * (nivel_size + margen)
        y = inicio_y + fila * (nivel_size + margen)
        
        # Dibujar tarjeta de nivel
        color_fondo = AZUL_PROFUNDO if nivel.desbloqueado else NEGRO
        surf_nivel = pygame.Surface((nivel_size, nivel_size), pygame.SRCALPHA)
        pygame.draw.rect(surf_nivel, color_fondo, (0, 0, nivel_size, nivel_size), border_radius=15)
        
        if nivel.desbloqueado:
            pygame.draw.rect(surf_nivel, COLORES_COSMICOS[nivel_idx % len(COLORES_COSMICOS)], 
                           (0, 0, nivel_size, nivel_size), 3, border_radius=15)
        
        # Número del nivel
        numero_color = BLANCO if nivel.desbloqueado else (100, 100, 100)
        numero = fuente_grande.render(str(nivel.numero), True, numero_color)
        surf_nivel.blit(numero, (nivel_size//2 - numero.get_width()//2, nivel_size//2 - numero.get_height()//2))
        
        # Estrellas si está completado
        if nivel.completado:
            estrellas_texto = "★" * nivel.estrellas
            estrellas_surf = fuente_pequena.render(estrellas_texto, True, (255, 255, 0))
            surf_nivel.blit(estrellas_surf, (nivel_size//2 - estrellas_surf.get_width()//2, nivel_size - 20))
        
        screen.blit(surf_nivel, (x, y))
        
        # Efecto hover
        mouse_pos = pygame.mouse.get_pos()
        nivel_rect = pygame.Rect(x, y, nivel_size, nivel_size)
        if nivel_rect.collidepoint(mouse_pos) and nivel.desbloqueado:
            surf_hover = pygame.Surface((nivel_size, nivel_size), pygame.SRCALPHA)
            pygame.draw.rect(surf_hover, (255, 255, 255, 30), (0, 0, nivel_size, nivel_size), border_radius=15)
            screen.blit(surf_hover, (x, y))
    
    # Botones de navegación
    if juego.pagina_actual > 0:
        boton_anterior = fuente_media.render("◀ ANTERIOR", True, BLANCO)
        screen.blit(boton_anterior, (50, HEIGHT - 50))
    
    if (juego.pagina_actual + 1) * juego.niveles_por_pagina < len(niveles):
        boton_siguiente = fuente_media.render("SIGUIENTE ▶", True, BLANCO)
        screen.blit(boton_siguiente, (WIDTH - boton_siguiente.get_width() - 50, HEIGHT - 50))
    
    # Botón volver
    boton_volver = fuente_media.render("← VOLVER", True, COLORES_COSMICOS[0])
    screen.blit(boton_volver, (50, 50))

def dibujar_jugando(juego):
    # Dibujar elementos del juego
    for ladrillo in juego.ladrillos:
        ladrillo.dibujar(screen)
    
    for powerup in juego.powerups:
        powerup.dibujar(screen)
    
    juego.raqueta.dibujar(screen)
    
    for pelota in juego.pelotas:
        if pelota.activa:
            pelota.dibujar(screen)
    
    # UI durante el juego
    # Puntuación
    puntuacion_texto = fuente_media.render(f"Puntos: {juego.puntuacion}", True, BLANCO)
    screen.blit(puntuacion_texto, (20, 20))
    
    # Vidas
    vidas_texto = fuente_media.render(f"Vidas: {juego.vidas}", True, BLANCO)
    screen.blit(vidas_texto, (WIDTH - vidas_texto.get_width() - 20, 20))
    
    # Nivel actual
    if juego.nivel_actual:
        nivel_texto = fuente_media.render(f"Nivel: {juego.nivel_actual.numero} - {juego.nivel_actual.nombre}", True, BLANCO)
        screen.blit(nivel_texto, (WIDTH//2 - nivel_texto.get_width()//2, 20))
    
    # Tiempo restante si aplica
    if juego.nivel_actual and juego.nivel_actual.tiempo_limite:
        tiempo_texto = fuente_media.render(f"Tiempo: {juego.tiempo_restante}s", True, BLANCO)
        screen.blit(tiempo_texto, (WIDTH//2 - tiempo_texto.get_width()//2, 50))
    
    # Combo
    if juego.combo > 0:
        combo_texto = fuente_grande.render(f"COMBO x{juego.combo + 1}!", True, COLORES_COSMICOS[3])
        screen.blit(combo_texto, (WIDTH//2 - combo_texto.get_width()//2, HEIGHT - 100))
    
    # Mensaje especial
    if juego.mensaje_especial:
        mensaje_texto = fuente_cosmica.render(juego.mensaje_especial, True, COLORES_COSMICOS[1])
        screen.blit(mensaje_texto, (WIDTH//2 - mensaje_texto.get_width()//2, HEIGHT//2 - 50))
    
    # Botón pausa
    pausa_texto = fuente_pequena.render("PAUSA (P)", True, BLANCO)
    screen.blit(pausa_texto, (WIDTH - pausa_texto.get_width() - 20, HEIGHT - 30))

def dibujar_pausa():
    # Fondo semitransparente
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Texto de pausa
    pausa_texto = fuente_titulo.render("JUEGO EN PAUSA", True, BLANCO)
    screen.blit(pausa_texto, (WIDTH//2 - pausa_texto.get_width()//2, HEIGHT//2 - 50))
    
    instrucciones = fuente_media.render("Presiona P para continuar", True, COLORES_COSMICOS[0])
    screen.blit(instrucciones, (WIDTH//2 - instrucciones.get_width()//2, HEIGHT//2 + 20))

def dibujar_game_over(juego):
    # Fondo semitransparente
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Texto de game over
    game_over_texto = fuente_titulo.render("GAME OVER", True, (255, 50, 50))
    screen.blit(game_over_texto, (WIDTH//2 - game_over_texto.get_width()//2, HEIGHT//2 - 100))
    
    # Puntuación final
    puntuacion_texto = fuente_cosmica.render(f"Puntuación: {juego.puntuacion}", True, BLANCO)
    screen.blit(puntuacion_texto, (WIDTH//2 - puntuacion_texto.get_width()//2, HEIGHT//2))
    
    # Opciones
    opciones = ["REINTENTAR", "MENÚ PRINCIPAL", "SALIR"]
    y_pos = HEIGHT//2 + 80
    
    for i, opcion in enumerate(opciones):
        color = COLORES_COSMICOS[i % len(COLORES_COSMICOS)]
        texto = fuente_media.render(opcion, True, color)
        rect = texto.get_rect(center=(WIDTH//2, y_pos + i * 60))
        
        # Efecto hover
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            surf_hover = pygame.Surface((rect.width + 20, rect.height + 10), pygame.SRCALPHA)
            pygame.draw.rect(surf_hover, (*color, 30), (0, 0, rect.width + 20, rect.height + 10), border_radius=10)
            screen.blit(surf_hover, (rect.x - 10, rect.y - 5))
        
        screen.blit(texto, rect)

def dibujar_victoria(juego):
    # Fondo semitransparente
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Texto de victoria
    victoria_texto = fuente_titulo.render("¡NIVEL COMPLETADO!", True, (50, 255, 150))
    screen.blit(victoria_texto, (WIDTH//2 - victoria_texto.get_width()//2, HEIGHT//2 - 100))
    
    # Estadísticas
    if juego.nivel_actual:
        estrellas = juego.nivel_actual.calcular_estrellas(
            juego.puntuacion, juego.vidas, juego.tiempo_restante
        )
        estrellas_texto = "★" * estrellas
        
        puntuacion_texto = fuente_cosmica.render(f"Puntuación: {juego.puntuacion}", True, BLANCO)
        screen.blit(puntuacion_texto, (WIDTH//2 - puntuacion_texto.get_width()//2, HEIGHT//2 - 30))
        
        estrellas_surf = fuente_cosmica.render(f"Estrellas: {estrellas_texto}", True, (255, 255, 0))
        screen.blit(estrellas_surf, (WIDTH//2 - estrellas_surf.get_width()//2, HEIGHT//2 + 10))
    
    # Opciones
    opciones = ["SIGUIENTE NIVEL", "REPETIR NIVEL", "MENÚ PRINCIPAL"]
    y_pos = HEIGHT//2 + 80
    
    for i, opcion in enumerate(opciones):
        color = COLORES_COSMICOS[i % len(COLORES_COSMICOS)]
        texto = fuente_media.render(opcion, True, color)
        rect = texto.get_rect(center=(WIDTH//2, y_pos + i * 60))
        
        # Efecto hover
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            surf_hover = pygame.Surface((rect.width + 20, rect.height + 10), pygame.SRCALPHA)
            pygame.draw.rect(surf_hover, (*color, 30), (0, 0, rect.width + 20, rect.height + 10), border_radius=10)
            screen.blit(surf_hover, (rect.x - 10, rect.y - 5))
        
        screen.blit(texto, rect)

# Función principal COMPLETA
def main():
    clock = pygame.time.Clock()
    juego = Juego()
    
    # Inicializar algunos niveles de ejemplo como desbloqueados para prueba
    for i in range(min(5, len(niveles))):
        niveles[i].desbloqueado = True
    
    running = True
    while running:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if juego.estado == EstadoJuego.JUGANDO:
                        juego.estado = EstadoJuego.PAUSA
                    elif juego.estado == EstadoJuego.PAUSA:
                        juego.estado = EstadoJuego.JUGANDO
                    else:
                        juego.estado = EstadoJuego.MENU
                
                elif event.key == pygame.K_p and juego.estado == EstadoJuego.JUGANDO:
                    juego.estado = EstadoJuego.PAUSA
                elif event.key == pygame.K_p and juego.estado == EstadoJuego.PAUSA:
                    juego.estado = EstadoJuego.JUGANDO
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if juego.estado == EstadoJuego.MENU:
                    # Detectar clic en opciones del menú
                    opciones = ["🎮 INICIAR AVENTURA", "🌌 SELECCIONAR NIVEL", "🚪 SALIR"]
                    y_pos = HEIGHT // 2
                    
                    for i, opcion in enumerate(opciones):
                        texto = fuente_grande.render(opcion, True, COLORES_COSMICOS[i])
                        rect = texto.get_rect(center=(WIDTH//2, y_pos + i * 70))
                        
                        if rect.collidepoint(mouse_pos):
                            if i == 0:  # Iniciar aventura
                                juego.iniciar_nivel(niveles[0])
                                juego.estado = EstadoJuego.JUGANDO
                            elif i == 1:  # Seleccionar nivel
                                juego.estado = EstadoJuego.SELECCION_NIVEL
                                juego.pagina_actual = 0
                            elif i == 2:  # Salir
                                running = False
                
                elif juego.estado == EstadoJuego.SELECCION_NIVEL:
                    # Detectar clic en niveles
                    niveles_por_fila = 3
                    nivel_size = 120
                    margen = 40
                    inicio_x = (WIDTH - (niveles_por_fila * nivel_size + (niveles_por_fila - 1) * margen)) // 2
                    inicio_y = 180
                    
                    for i in range(juego.niveles_por_pagina):
                        nivel_idx = juego.pagina_actual * juego.niveles_por_pagina + i
                        if nivel_idx >= len(niveles):
                            break
                            
                        nivel = niveles[nivel_idx]
                        fila = i // niveles_por_fila
                        columna = i % niveles_por_fila
                        
                        x = inicio_x + columna * (nivel_size + margen)
                        y = inicio_y + fila * (nivel_size + margen)
                        
                        nivel_rect = pygame.Rect(x, y, nivel_size, nivel_size)
                        if nivel_rect.collidepoint(mouse_pos) and nivel.desbloqueado:
                            juego.iniciar_nivel(nivel)
                            juego.estado = EstadoJuego.JUGANDO
                            break
                    
                    # Botones de navegación
                    if juego.pagina_actual > 0:
                        boton_anterior = fuente_media.render("◀ ANTERIOR", True, BLANCO)
                        anterior_rect = boton_anterior.get_rect(topleft=(50, HEIGHT - 50))
                        if anterior_rect.collidepoint(mouse_pos):
                            juego.pagina_actual -= 1
                    
                    if (juego.pagina_actual + 1) * juego.niveles_por_pagina < len(niveles):
                        boton_siguiente = fuente_media.render("SIGUIENTE ▶", True, BLANCO)
                        siguiente_rect = boton_siguiente.get_rect(topleft=(WIDTH - boton_siguiente.get_width() - 50, HEIGHT - 50))
                        if siguiente_rect.collidepoint(mouse_pos):
                            juego.pagina_actual += 1
                    
                    # Botón volver
                    boton_volver = fuente_media.render("← VOLVER", True, COLORES_COSMICOS[0])
                    volver_rect = boton_volver.get_rect(topleft=(50, 50))
                    if volver_rect.collidepoint(mouse_pos):
                        juego.estado = EstadoJuego.MENU
                
                elif juego.estado == EstadoJuego.GAME_OVER:
                    opciones = ["🔄 REINTENTAR NIVEL", "🌌 MENÚ PRINCIPAL", "🚪 SALIR"]
                    y_pos = HEIGHT//2 + 80
                    
                    for i, opcion in enumerate(opciones):
                        texto = fuente_media.render(opcion, True, COLORES_COSMICOS[i])
                        rect = texto.get_rect(center=(WIDTH//2, y_pos + i * 60))
                        
                        if rect.collidepoint(mouse_pos):
                            if i == 0:  # Reintentar
                                if juego.nivel_actual:
                                    juego.iniciar_nivel(juego.nivel_actual)
                                    juego.estado = EstadoJuego.JUGANDO
                            elif i == 1:  # Menú principal
                                juego.estado = EstadoJuego.MENU
                            elif i == 2:  # Salir
                                running = False
                
                elif juego.estado == EstadoJuego.VICTORIA:
                    opciones = ["🎮 SIGUIENTE NIVEL", "🔄 REPETIR NIVEL", "🌌 MENÚ PRINCIPAL"]
                    y_pos = HEIGHT//2 + 80
                    
                    for i, opcion in enumerate(opciones):
                        texto = fuente_media.render(opcion, True, COLORES_COSMICOS[i])
                        rect = texto.get_rect(center=(WIDTH//2, y_pos + i * 60))
                        
                        if rect.collidepoint(mouse_pos):
                            if i == 0:  # Siguiente nivel
                                if juego.nivel_actual:
                                    nivel_actual_idx = niveles.index(juego.nivel_actual)
                                    if nivel_actual_idx + 1 < len(niveles):
                                        juego.iniciar_nivel(niveles[nivel_actual_idx + 1])
                                        juego.estado = EstadoJuego.JUGANDO
                            elif i == 1:  # Repetir
                                if juego.nivel_actual:
                                    juego.iniciar_nivel(juego.nivel_actual)
                                    juego.estado = EstadoJuego.JUGANDO
                            elif i == 2:  # Menú principal
                                juego.estado = EstadoJuego.MENU
        
        # Actualizar juego según estado
        if juego.estado == EstadoJuego.JUGANDO:
            # Controles de la raqueta
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                juego.raqueta.mover("izquierda")
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                juego.raqueta.mover("derecha")
            
            juego.actualizar()
        
        # Actualizar partículas
        global particulas
        particulas = [p for p in particulas if p.update()]
        
        # Dibujar
        # Fondo espacial
        screen.fill(NEGRO_COSMICO)
        
        # Nebulosas
        for nebulosa in nebulosas:
            nebulosa.update()
            nebulosa.draw(screen)
        
        # Estrellas de fondo
        for estrella in estrellas_fondo:
            estrella.update()
            estrella.draw(screen)
        
        # Partículas
        for particula in particulas:
            particula.draw(screen)
        
        # Dibujar según estado del juego
        if juego.estado == EstadoJuego.MENU:
            dibujar_menu(juego)
        elif juego.estado == EstadoJuego.SELECCION_NIVEL:
            dibujar_seleccion_nivel(juego)
        elif juego.estado == EstadoJuego.JUGANDO:
            dibujar_jugando(juego)
        elif juego.estado == EstadoJuego.PAUSA:
            dibujar_jugando(juego)
            dibujar_pausa()
        elif juego.estado == EstadoJuego.GAME_OVER:
            dibujar_jugando(juego)
            dibujar_game_over(juego)
        elif juego.estado == EstadoJuego.VICTORIA:
            dibujar_jugando(juego)
            dibujar_victoria(juego)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()