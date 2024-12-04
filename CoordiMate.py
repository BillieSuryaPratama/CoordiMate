import pygame
import cairo
import math

WIDTH, HEIGHT = 1200, 700

# Opsi warna
BACKGROUND = (200, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE_BUTTON = (36, 160, 237)
RED_BUTTON = (210, 43, 43)
GREEN_BUTTON = (60, 179, 113)

# Inisialisasi pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CoordiMate")

# Inisialisasi font
pygame.font.init()
font = pygame.font.Font(None, 50)

# Pengaturan page
ShowMenu = True
ShowPageMenggambar = False
ShowPagePencerminan = False
ShowPagePersegi = False
ShowPageLingkaran = False
ShowPageGaris = False
ShowPageKurva = False

# Fungsi untuk Center align text
def center(context, x, y, text, font, size):
    context.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(size)
    extents = context.text_extents(text)
    context.move_to(x - extents.width / 2, y)
    context.set_source_rgb(0, 0, 0)
    context.show_text(text)

# Fungsi untuk menggambar tombol berisi teks
def Button(x, y, width, height, text, TextColor, ButtonColor, r, size):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(ButtonColor[0] / 255, ButtonColor[1] / 255, ButtonColor[2] / 255)
    ctx.arc(x+r, y+r, r, math.pi, 3*math.pi/2)
    ctx.arc(x+width-r, y+r, r, 3*math.pi/2, 0)
    ctx.arc(x+width-r, y+height-r, r, 0, math.pi/2)
    ctx.arc(x+r, y+height-r, r, math.pi/2, math.pi)
    ctx.fill()

    ctx.set_source_rgb(TextColor[0] / 255, TextColor[1] / 255, TextColor[2] / 255)
    ctx.select_font_face("Segoe UI", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    text_extents = ctx.text_extents(text)
    ctx.move_to((width - text_extents.width) / 2, (height + text_extents.height) / 2)
    ctx.show_text(text)

    return pygame.image.frombuffer(surface.get_data(), (width, height), "BGRA")

# Fungsi untuk memeriksa apakah tombol diklik
def isClicked(mouse_pos, button_pos, button_width, button_height):
    return (
        button_pos[0] <= mouse_pos[0] <= button_pos[0] + button_width and
        button_pos[1] <= mouse_pos[1] <= button_pos[1] + button_height
    )

# Button Main Menu
MenuButtons = [
    {'label': 'Menggambar Bebas', 'pos': (450, 300), 'ButtonColor': BLUE_BUTTON, 'TextColor': WHITE},
    {'label': 'Pencerminan', 'pos': (450, 400), 'ButtonColor': BLUE_BUTTON, 'TextColor': WHITE},
    {'label': 'Exit', 'pos': (450, 500), 'ButtonColor': RED_BUTTON, 'TextColor': WHITE}
]

# Button Menggambar Bebas
DrawingButtons = [
    {'label': 'Persegi', 'pos': (25, 10), 'ButtonColor': BLUE_BUTTON, 'TextColor': WHITE},
    {'label': 'Lingkaran', 'pos': (25, 110), 'ButtonColor': BLUE_BUTTON, 'TextColor': WHITE},
    {'label': 'Garis', 'pos': (25, 210), 'ButtonColor': BLUE_BUTTON, 'TextColor': WHITE},
    {'label': 'Kurva', 'pos': (25, 310), 'ButtonColor': BLUE_BUTTON, 'TextColor': WHITE},
    {'label': 'Clear', 'pos': (25, 410), 'ButtonColor': GREEN_BUTTON, 'TextColor': WHITE},
    {'label': 'Undo', 'pos': (25, 510), 'ButtonColor': GREEN_BUTTON, 'TextColor': WHITE},
    {'label': 'Back', 'pos': (25, 610), 'ButtonColor': RED_BUTTON, 'TextColor': WHITE}
]


# Loop Utama
running = True
while running:
    screen.fill(BACKGROUND)

    # Page Main Menu
    if ShowMenu:
        # Gambar teks judul "CoordiMate"
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        ctx = cairo.Context(surface)
        center(ctx, 600, 200, "CoordiMate", "Segoe UI", 60)
        title_surface = pygame.image.frombuffer(surface.get_data(), (WIDTH, HEIGHT), "BGRA")
        screen.blit(title_surface, (0, 0))

        # Gambar tombol pada menu
        for button in MenuButtons:
            btn_surf = Button(0, 0, 300, 80, button['label'], button['TextColor'], button['ButtonColor'], 25, 18)
            screen.blit(btn_surf, button['pos'])

        # Event handling menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in MenuButtons:
                    if button['label'] == 'Exit' and isClicked((mouse_x, mouse_y), button['pos'], 300, 80):
                        running = False
                    elif button['label'] == 'Menggambar Bebas' and isClicked((mouse_x, mouse_y), button['pos'], 300, 80):
                        ShowMenu = False
                        ShowPageMenggambar = True

    # Page Menggambar Bebas
    elif ShowPageMenggambar:
        # Canvas untuk menggambar
        pygame.draw.rect(screen, BLACK, (250, 10, 940, 680)) #1190x690
        pygame.draw.rect(screen, WHITE, (255, 15, 930, 670)) #1185x685

        # Gambar tombol
        for button in DrawingButtons:
            btn_surf = Button(0, 0, 200, 80, button['label'], button['TextColor'], button['ButtonColor'], 25, 18)
            screen.blit(btn_surf, button['pos'])

        # Event handling menggambar bebas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in DrawingButtons:
                    if button['label'] == 'Persegi' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        ShowPagePersegi = True
                        ShowPageMenggambar = False
                    elif button['label'] == 'Lingkaran' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        ShowPageLingkaran = True
                        ShowPageMenggambar = False
                    elif button['label'] == 'Garis' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        ShowPageGaris = True
                        ShowPageMenggambar = False
                    elif button['label'] == 'Kurva' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        ShowPageKurva = True
                        ShowPageMenggambar = False
                    elif button['label'] == 'Clear' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        pass
                    elif button['label'] == 'Undo' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        pass
                    elif button['label'] == 'Back' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        ShowMenu = True
                        ShowPageMenggambar = False

    # Page Menggambar Persegi
    elif ShowPagePersegi:
        # Canvas untuk menggambar
        pygame.draw.rect(screen, BLACK, (250, 10, 940, 680)) #1190x690
        pygame.draw.rect(screen, WHITE, (255, 15, 930, 670)) #1185x685

        # Event handling menggambar bebas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Page Menggambar Lingkaran
    elif ShowPageLingkaran:
        # Canvas untuk menggambar
        pygame.draw.rect(screen, BLACK, (250, 10, 940, 680)) #1190x690
        pygame.draw.rect(screen, WHITE, (255, 15, 930, 670)) #1185x685

        # Event handling menggambar bebas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Page Menggambar Garis
    elif ShowPageGaris:
        # Canvas untuk menggambar
        pygame.draw.rect(screen, BLACK, (250, 10, 940, 680)) #1190x690
        pygame.draw.rect(screen, WHITE, (255, 15, 930, 670)) #1185x685

        # Event handling menggambar bebas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Page Menggambar Kurva
    elif ShowPageKurva:
        # Canvas untuk menggambar
        pygame.draw.rect(screen, BLACK, (250, 10, 940, 680)) #1190x690
        pygame.draw.rect(screen, WHITE, (255, 15, 930, 670)) #1185x685

        # Event handling menggambar bebas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.display.flip()

pygame.quit()
