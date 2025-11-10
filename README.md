# 🌌Brick Breaker🚀

<img width="901" height="636" alt="image" src="https://github.com/Alejandro-Mendieta/BRICK-BREAKER/blob/main/assets/FOTOS/FOTO1.png?raw=true" />

![Brick Breaker](https://img.shields.io/badge/Game-%20Brick%20Breaker-purple)
![Version](https://img.shields.io/badge/Version-2.0-cyan)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.5.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Levels](https://img.shields.io/badge/Levels-100%20Epic%20Levels-orange)

## ✨ Descripción

**Cosmic Brick Breaker - Viaje Interestelar** es una experiencia de juego revolucionaria que lleva el clásico Brick Breaker a nuevas dimensiones cósmicas. Sumérgete en un viaje interestelar lleno de efectos visuales espectaculares, mecánicas de juego innovadoras y 100 niveles épicos que desafiarán tus habilidades.

## 🎮 Características Principales

### 🌟 **Características Únicas**
- **🎇 100 Niveles Épicos** con progresión de dificultad perfectamente balanceada
- **✨ Sistema de Partículas Avanzado** con efectos cósmicos y explosiones estelares
- **🌠 Fondos Dinámicos** con nebulosas animadas y estrellas centelleantes
- **⚡ Efectos Visuales Ultra Vibrantes** con iluminación realista y gradientes cósmicos

### 🎯 **Mecánicas de Juego Mejoradas**
- **🔮 Sistema de Combos** - Multiplicadores de puntuación por golpes consecutivos
- **⭐ Sistema de Estrellas** - 3 estrellas por nivel basadas en tu desempeño
- **💫 Power-ups Cósmicos** - 6 tipos diferentes con efectos únicos
- **🚀 Física Mejorada** - Rebotes realistas y ángulos dinámicos

### 🎨 **Experiencia Visual**
- **Paleta de Colores Cósmicos** - 15 colores ultra vibrantes inspirados en el espacio
- **Animaciones Suaves** - Transiciones fluidas entre todos los estados del juego
- **Interfaz Espacial** - Diseño moderno con temática interestelar
- **Efectos de Partículas** - Explosiones, estelas y lluvias estelares

## 🎪 Power-ups Cósmicos Disponibles

| Power-up | Símbolo | Efecto | Duración |
|----------|----------|---------|-----------|
| **Raqueta Grande** | ⬆ | Aumenta tamaño +40px | 10 segundos |
| **Raqueta Pequeña** | ⬇ | Reduce tamaño -30px | 10 segundos |
| **Múltiples Pelotas** | ⚡ | Añade 2 pelotas extra | Instantáneo |
| **Vida Extra** | ❤ | +1 vida adicional | Instantáneo |
| **Cámara Lenta** | ⏳ | Reduce velocidad 40% | 5 segundos |
| **Campo Magnético** | 🧲 | Atrae power-ups | 7.5 segundos |

## 🕹️ Controles

### 🎯 **Controles Principales**
- **🠔 Flecha Izquierda** o **Tecla A**: Mover plataforma a la izquierda
- **🠖 Flecha Derecha** o **Tecla D**: Mover plataforma a la derecha
- **P**: Pausar/Reanudar el juego
- **ESC**: Navegar entre menús

### 🎮 **Controles de Navegación**
- **Clic Izquierdo**: Seleccionar opciones en menús
- **Rueda del Ratón**: Navegar entre páginas de niveles

## 🚀 Instalación Rápida

### 📋 Requisitos del Sistema
- **Python 3.8** o superior
- **Pygame 2.5.2** o superior
- **Sistema operativo**: Windows, macOS o Linux

### ⚡ Instalación en 3 Pasos

1. **Descarga el juego**:
```bash
git clone https://github.com/alejandro-mendieta/brick-breaker.git
cd brick-breaker
```

2. **Instala Pygame**:
```bash
pip install pygame
```

3. **¡Lanza al espacio!**:
```bash
python cosmic_brick_breaker.py
```

### 🐧 Instalación Avanzada (Linux)
```bash
# Para mejor rendimiento con soporte AVX2:
PYGAME_DETECT_AVX2=1 pip install pygame --no-binary=pygame
```

## 🏗️ Arquitectura del Proyecto

```
cosmic-brick-breaker/
│
├── 🌟 cosmic_brick_breaker.py    # Archivo principal del juego
├── 🎮 game/
│   ├── __init__.py
│   ├── core/
│   │   ├── game_engine.py       # Motor principal del juego
│   │   ├── particle_system.py   # Sistema de partículas avanzado
│   │   └── level_generator.py   # Generador procedural de niveles
│   ├── entities/
│   │   ├── paddle.py           # Plataforma con efectos cósmicos
│   │   ├── ball.py             # Pelota con trail de energía
│   │   ├── brick.py            # Ladrillos con resistencia y efectos
│   │   └── powerup.py          # Power-ups con rotación y glow
│   └── ui/
│       ├── menu_system.py      # Sistema de menús interactivos
│       ├── level_selector.py   # Selector de niveles con páginas
│       └── hud.py              # Interfaz de usuario en juego
├── 🎨 assets/
│   ├── cosmic_palettes/        # Paletas de colores cósmicos
│   └── effects/               # Configuraciones de efectos
├── 📊 config/
│   ├── game_settings.py       # Configuraciones del juego
│   ├── level_design.py        # Diseño de niveles progresivos
│   └── visual_effects.py      # Configuración de efectos visuales
└── 📚 docs/
    ├── API_REFERENCE.md       # Referencia de la API
    └── LEVEL_DESIGN_GUIDE.md  # Guía de diseño de niveles
```

## 🎯 Guía de Juego

### 🚀 **Cómo Dominar el Juego**

1. **🏁 Inicio Rápido**
   - Selecciona "Iniciar Aventura" para comenzar desde el nivel 1
   - Usa "Seleccionar Nivel" para acceder a niveles desbloqueados

2. **⭐ Sistema de Estrellas**
   - **★**: Completar el nivel
   - **★★**: Superar 1500 + (nivel × 200) puntos
   - **★★★**: Terminar con todas las vidas menos una

3. **💥 Combos y Estrategias**
   - **Combo x2+**: Puntuación doble por golpes consecutivos
   - **Rompe cristales**: +500 puntos y mensaje especial
   - **Power-ups estratégicos**: Usa Campo Magnético en niveles densos

### 🌌 **Progresión de Dificultad**

| Grupo | Niveles | Características |
|-------|---------|-----------------|
| **🌠 Aprendiz** | 1-20 | Patrones básicos, velocidad normal |
| **🚀 Intermedio** | 21-40 | Formaciones complejas, mayor velocidad |
| **💫 Avanzado** | 41-60 | Patrones avanzados, menos vidas |
| **⭐ Experto** | 61-80 | Alta densidad, tiempo límite |
| **👑 Maestro** | 81-100 | Patrones maestros, máxima dificultad |

## 🎨 Personalización

### 🔧 **Configuración de Dificultad**
El juego incluye 5 niveles de dificultad preconfigurados que se adaptan automáticamente según tu progreso.

### 🎪 **Efectos Visuales**
Todos los efectos pueden ajustarse desde el código:
- Intensidad de partículas
- Velocidad de animaciones
- Brillo de efectos luminosos

## 👨‍💻 Desarrolladores

### **Equipo Principal**
- **ALEJANDRO MENDIETA** - Arquitecto Principal & Desarrollador
  - *Sistemas de Partículas*
  - *Generación Procedural de Niveles*
  - *Motor Gráfico Avanzado*

### **Colaboradores**
¡Buscamos colaboradores apasionados por los juegos retro y los efectos visuales!

## 🤝 Contribuciones

¡Amamos las contribuciones! Aquí cómo puedes ayudar:

### 💡 **Nuevas Características**
1. **Discute** tu idea en los Discussions
2. **Fork** el repositorio
3. **Desarrolla** en una rama feature: `git checkout -b feature/nueva-caracteristica`
4. **Testea** exhaustivamente
5. **PR** con descripción detallada

### 🎯 **Áreas de Mejora Prioritaria**
- [ ] 🌍 Internacionalización (múltiples idiomas)
- [ ] 🎵 Sistema de audio espacial
- [ ] 🔧 Editor de niveles integrado
- [ ] 🌐 Modo multijugador online
- [ ] 📱 Versión móvil
- [ ] 🏆 Logros y tablas de clasificación globales

## 📜 Licencia

Este proyecto está bajo la **Licencia MIT** - ver el archivo [LICENSE](LICENSE) para detalles completos.

### 🎵 Atribuciones
- Efectos de partículas inspirados en fenómenos cósmicos reales
- Paleta de colores basada en nebulosas y eventos estelares
- Mecánicas de juego probadas y optimizadas para máxima diversión

## 🗺️ Roadmap 2024

### 🎯 **Próximas Versiones**
- **v2.1** - Sistema de logros y estadísticas detalladas
- **v2.2** - Editor de niveles con interfaz visual
- **v2.3** - Modos de juego alternativos (Supervivencia, Contrareloj)
- **v2.4** - Integración con plataformas de streaming

### 🌟 **Características Futuras**
- [ ] 🎵 Banda sonora original orquestal
- [ ] 🎨 Temas visuales intercambiables
- [ ] 🔧 Modo desarrollador con consola integrada
- [ ] 📊 Análisis de rendimiento en tiempo real
- [ ] 🌐 API para mods y extensiones


### 🏆 **Reconocimientos**
Un agradecimiento especial a la comunidad de Pygame y a todos los beta testers que han ayudado a pulir esta experiencia cósmica.

---

<div align="center">

## 🚀 **¡Prepárate para el Viaje Interestelar Definitivo!**

**¿Tienes lo que se necesita para conquistar los 100 niveles cósmicos?**

[![Jugar Ahora](https://img.shields.io/badge/🚀_Jugar_Brick_Breaker-Play_Now-purple?style=for-the-badge&logo=game)](https://github.com/alejandro-mendietacosmic-brick-breaker)

*¡Que la fuerza cósmica te acompañe!* 🌌

</div>

---

**⭐ ¿Te gusta el proyecto?** No olvides darle una estrella al repositorio para apoyar el desarrollo continuo!