# Brick Breaker 🎮

![Brick Breaker](https://img.shields.io/badge/Game-Brick%20Breaker-blue)
![Version](https://img.shields.io/badge/Version-1.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Descripción 📝

**Brick Breaker** es un juego clásico de arcade donde el objetivo es destruir todos los ladrillos en pantalla utilizando una pelota que rebota. Controlas una plataforma en la parte inferior de la pantalla para evitar que la pelota caiga, mientras intentas romper todos los ladrillos dispuestos en formaciones superiores.

## Características 🚀

- **Gameplay clásico y adictivo**
- **Múltiples niveles** con diferentes patrones de ladrillos
- **Sistema de vidas** y puntuación
- **Power-ups** especiales (plataforma más grande, pelotas extra, etc.)
- **Física realista** de rebotes
- **Efectos de sonido** y música de fondo
- **Interfaz intuitiva** y controles sencillos

## Controles 🎯

- **Flecha izquierda (←)** o **Tecla A**: Mover plataforma a la izquierda
- **Flecha derecha (→)** o **Tecla D**: Mover plataforma a la derecha
- **Espacio**: Pausar/reanudar el juego
- **Enter**: Iniciar juego o lanzar pelota

## Instalación ⚙️

### Requisitos del Sistema
- Python 3.8 o superior
- Pygame library

### Pasos de instalación

1. **Clona el repositorio**:
```bash
git clone https://github.com/tuusuario/brick-breaker.git
cd brick-breaker
```

2. **Instala las dependencias**:
```bash
pip install pygame
```

3. **Ejecuta el juego**:
```bash
python main.py
```

## Estructura del Proyecto 📁

```
brick-breaker/
│
├── main.py              # Archivo principal del juego
├── game/
│   ├── __init__.py
│   ├── game.py          # Lógica principal del juego
│   ├── paddle.py        # Clase de la plataforma
│   ├── ball.py          # Clase de la pelota
│   ├── brick.py         # Clase de los ladrillos
│   └── powerup.py       # Clase de los power-ups
├── assets/
│   ├── images/          # Sprites y gráficos
│   ├── sounds/          # Efectos de sonido
│   └── fonts/           # Fuentes del juego
├── config/
│   └── settings.py      # Configuraciones del juego
└── README.md
```

## Cómo Jugar 🎮

1. **Inicia el juego** y selecciona el nivel
2. **Controla la plataforma** con las teclas de flecha
3. **Destruye los ladrillos** haciendo rebotar la pelota
4. **Atrapa los power-ups** que caen de los ladrillos destruidos
5. **Evita que la pelota caiga** - pierdes una vida si esto ocurre
6. **Completa todos los niveles** para ganar el juego

## Power-ups Disponibles 🔮

- **🔴 Bola Extra**: Añade una pelota adicional
- **🔵 Plataforma Grande**: Temporalmente agranda tu plataforma
- **🟢 Bola Lenta**: Reduce la velocidad de la pelota
- **🟡 Puntuación Doble**: Duplica los puntos por un tiempo limitado

## Desarrolladores 👨‍💻

- ALEJANDRO MENDIETA - Desarrollador Principal

## Contribuciones 🤝

¡Las contribuciones son bienvenidas! Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia 📄

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.


## Roadmap 🗺️

- [ ] Modo multijugador
- [ ] Editor de niveles
- [ ] Logros y tablas de clasificación
- [ ] Más tipos de ladrillos y power-ups
- [ ] Soporte para temas personalizados

---

**¡Diviértete jugando!** 🎉

Si encuentras algún error o tienes sugerencias, por favor abre un issue en el repositorio.