import pygame
import math

# Konstanten
FPS = 60
ENEMY_SPEED = 2  # Geschwindigkeit der Gegner
GRASS_COLOR = (34, 139, 34)  # Farbe für Gras (optional, falls kein Gras-Tile existiert)

# Pygame initialisieren
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Vollbildmodus aktivieren
clock = pygame.time.Clock()

# Gegnerklasse
class Enemy:
    def __init__(self, path):
        self.path = path  # Liste von Wegpunkten (Koordinaten)
        self.current_wp = 0  # Aktueller Wegpunkt
        self.x, self.y = path[0]  # Startposition des Gegners
        self.speed = ENEMY_SPEED

    def move(self):
        if self.current_wp < len(self.path) - 1:
            target_x, target_y = self.path[self.current_wp + 1]
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance > 0:
                # Normiere den Vektor und bewege den Gegner mit der vorgegebenen Geschwindigkeit
                dx = dx / distance
                dy = dy / distance
                self.x += dx * self.speed
                self.y += dy * self.speed

            # Wenn der Gegner nahe genug am nächsten Wegpunkt ist, wechsle zum nächsten
            if distance < self.speed:
                self.current_wp += 1

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 10)  # Zeichne den Gegner als roten Kreis


# Beispiel-Pfad (Wegpunkte) auf dem Weg
path = [(815, 900), (815, 700), (990, 700), (990, 480), (655, 480), (655, 300), (655, 0)]

# Gegnerliste
enemies = [Enemy(path)]

# Map und Tileset-Bilder laden
tileset_image = pygame.image.load('TDK_Map/simplified/Level_0/Tiles.png')
grass_tile_image = pygame.image.load('TDK_Map/simplified/Level_0/grass-tile.png')  # Lade das Gras-Tile

# Map-Größe (256x256 in deinem Fall)
map_width = tileset_image.get_width()  # Breite der Karte (z.B. 256 px)
map_height = tileset_image.get_height()  # Höhe der Karte (z.B. 256 px)

# Funktion zum Zeichnen des Hintergrunds (Gras)
def draw_grass(screen, grass_tile_image, screen_width, screen_height):
    grass_tile_size = grass_tile_image.get_width()  # Breite und Höhe des Gras-Tiles
    for y in range(0, screen_height, grass_tile_size):
        for x in range(0, screen_width, grass_tile_size):
            screen.blit(grass_tile_image, (x, y))

# Funktion zum Zeichnen der Karte
def draw_map(screen, tileset_image, screen_width, screen_height):
    # Berechne das Seitenverhältnis der Karte
    aspect_ratio = map_width / map_height
    scaled_width = screen_width
    scaled_height = int(screen_width / aspect_ratio)

    # Wenn die Höhe zu groß ist, passe die Breite an
    if scaled_height > screen_height:
        scaled_height = screen_height
        scaled_width = int(screen_height * aspect_ratio)

    # Berechne die Position, um die Karte in der Mitte des Bildschirms zu platzieren
    offset_x = (screen_width - scaled_width) // 2
    offset_y = (screen_height - scaled_height) // 2

    # Zeichne das Gras zuerst (damit die Ränder ausgefüllt werden)
    draw_grass(screen, grass_tile_image, screen_width, screen_height)

    # Skaliere die Karte und zeichne sie in der Mitte
    scaled_map = pygame.transform.scale(tileset_image, (scaled_width, scaled_height))
    screen.blit(scaled_map, (offset_x, offset_y))

# Hauptspiel-Schleife
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC-Taste, um das Spiel zu beenden
                running = False

    # Hintergrundfarbe setzen (optional)
    screen.fill((0, 0, 0))

    # Aktuelle Bildschirmgröße
    window_width, window_height = screen.get_size()

    # Zeichne die Karte und fülle die Ränder mit Gras
    draw_map(screen, tileset_image, window_width, window_height)

    # Gegner bewegen und zeichnen
    for enemy in enemies:
        enemy.move()
        enemy.draw(screen)

    # Bildschirm aktualisieren
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
