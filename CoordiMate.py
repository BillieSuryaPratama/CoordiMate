import pygame
import cairo
import math

WIDTH, HEIGHT = 1200, 700

# Opsi warna
BACKGROUND = (36, 160, 237)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE_BUTTON = (0, 71, 171)
RED_BUTTON = (210, 43, 43)
GREEN_BUTTON = (31, 198, 0)

# Inisialisasi pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CoordiMate")

# Inisialisasi font
pygame.font.init()
font = pygame.font.Font(None, 50)
fontPersegi = pygame.font.Font(None, 25)

# Pengaturan page
ShowMenu = True
ShowPageMenggambar = False
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

def InputBox(screen, font, input_box, text, color_inactive, color_active, active):
    color = color_active if active else color_inactive
    txt_surface = font.render(text, True, color)
    max_width = input_box.width - 10  # Kurangi padding
    
    # Potong teks jika terlalu panjang
    while txt_surface.get_width() > max_width:
        text = text[1:]
        txt_surface = font.render(text, True, color)
    
    # Blit text dan kotak input
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)
    return text

def draw_text(screen, text, font, pos, color):
    txt_surface = font.render(text, True, color)
    screen.blit(txt_surface, pos)

def draw_persegi(x, y, Panjang, Tinggi, line_width=2):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, Panjang + line_width * 2, Tinggi + line_width * 2)
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(line_width)
    ctx.rectangle(line_width, line_width, Panjang, Tinggi)
    ctx.stroke()

    return pygame.image.frombuffer(surface.get_data(), (Panjang + line_width * 2, Tinggi + line_width * 2), "BGRA")

def draw_garis(x, y, endx, endy, line_width=2):
    width = abs(endx - x)
    height = abs(endy - y)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width + line_width * 2, height + line_width * 2)
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(line_width)

    start_x = line_width if x <= endx else width - line_width
    start_y = line_width if y <= endy else height - line_width
    end_x = width - line_width if x < endx else line_width
    end_y = height - line_width if y < endy else line_width

    ctx.move_to(start_x, start_y)
    ctx.line_to(end_x, end_y)
    ctx.stroke()

    return pygame.image.frombuffer(surface.get_data(), (width + line_width * 2, height + line_width * 2), "BGRA")

# Fungsi untuk memeriksa apakah tombol diklik
def isClicked(mouse_pos, button_pos, button_width, button_height):
    return (
        button_pos[0] <= mouse_pos[0] <= button_pos[0] + button_width and
        button_pos[1] <= mouse_pos[1] <= button_pos[1] + button_height
    )

# Button Main Menu
ButtonsMenu = [
    {'label': 'Mulai Menggambar', 'pos': (450, 300), 'ButtonColor': BLUE_BUTTON, 'TextColor': WHITE},
    {'label': 'Exit', 'pos': (450, 400), 'ButtonColor': RED_BUTTON, 'TextColor': WHITE}
]

# Button Mulai Menggambar
ButtonsMenggambar = [
    {'label': 'Persegi', 'pos': (25, 10), 'ButtonColor': BLUE_BUTTON, 'TextColor': WHITE},
    {'label': 'Lingkaran', 'pos': (25, 110), 'ButtonColor': BLUE_BUTTON, 'TextColor': WHITE},
    {'label': 'Garis', 'pos': (25, 210), 'ButtonColor': BLUE_BUTTON, 'TextColor': WHITE},
    {'label': 'Kurva', 'pos': (25, 310), 'ButtonColor': BLUE_BUTTON, 'TextColor': WHITE},
    {'label': 'Clear', 'pos': (25, 410), 'ButtonColor': GREEN_BUTTON, 'TextColor': WHITE},
    {'label': 'Undo', 'pos': (135, 410), 'ButtonColor': GREEN_BUTTON, 'TextColor': WHITE},
    {'label': 'Back', 'pos': (25, 610), 'ButtonColor': RED_BUTTON, 'TextColor': WHITE}
]

# Button Menggambar Persegi
ButtonsPersegi = [
    {'label': 'Update', 'pos': (25, 410), 'ButtonColor': GREEN_BUTTON, 'TextColor': WHITE},
    {'label': 'Save', 'pos': (25, 510), 'ButtonColor': GREEN_BUTTON, 'TextColor': WHITE},
    {'label': 'Back', 'pos': (25, 610), 'ButtonColor': RED_BUTTON, 'TextColor': WHITE}
]

# Button Menggambar Lingkaran
ButtonsLingkaran = [
    {'label': 'Update', 'pos': (25, 410), 'ButtonColor': GREEN_BUTTON, 'TextColor': WHITE},
    {'label': 'Save', 'pos': (25, 510), 'ButtonColor': GREEN_BUTTON, 'TextColor': WHITE},
    {'label': 'Back', 'pos': (25, 610), 'ButtonColor': RED_BUTTON, 'TextColor': WHITE}
]

# Button Menggambar Garis
ButtonsGaris = [
    {'label': 'Update', 'pos': (25, 410), 'ButtonColor': GREEN_BUTTON, 'TextColor': WHITE},
    {'label': 'Save', 'pos': (25, 510), 'ButtonColor': GREEN_BUTTON, 'TextColor': WHITE},
    {'label': 'Back', 'pos': (25, 610), 'ButtonColor': RED_BUTTON, 'TextColor': WHITE}
]

# Button Menggambar Kurva
ButtonsKurva = [
    {'label': 'Update', 'pos': (25, 410), 'ButtonColor': GREEN_BUTTON, 'TextColor': WHITE},
    {'label': 'Save', 'pos': (25, 510), 'ButtonColor': GREEN_BUTTON, 'TextColor': WHITE},
    {'label': 'Back', 'pos': (25, 610), 'ButtonColor': RED_BUTTON, 'TextColor': WHITE}
]

# Shape yang telah digambar
Shape = []

# Variabel untuk Update
Update = 0

# Input box Persegi (PersegiStartX)
PersegiStartX_input_box = pygame.Rect(25, 60, 200, 40)
PersegiStartX_color_inactive = pygame.Color(BLUE_BUTTON)
PersegiStartX_color_active = pygame.Color(BLACK)
PersegiStartX_color = PersegiStartX_color_inactive
PersegiStartX_active = False
PersegiStartX_input_text = ''

# Input box Persegi (PersegiStartY)
PersegiStartY_input_box = pygame.Rect(25, 140, 200, 40)
PersegiStartY_color_inactive = pygame.Color(BLUE_BUTTON)
PersegiStartY_color_active = pygame.Color(BLACK)
PersegiStartY_color = PersegiStartY_color_inactive
PersegiStartY_active = False
PersegiStartY_input_text = ''

# Input box Persegi (PersegiPanjang)
PersegiPanjang_input_box = pygame.Rect(25, 220, 200, 40)
PersegiPanjang_color_inactive = pygame.Color(BLUE_BUTTON)
PersegiPanjang_color_active = pygame.Color(BLACK)
PersegiPanjang_color = PersegiPanjang_color_inactive
PersegiPanjang_active = False
PersegiPanjang_input_text = ''

# Input box Persegi (PersegiLebar)
PersegiLebar_input_box = pygame.Rect(25, 300, 200, 40)
PersegiLebar_color_inactive = pygame.Color(BLUE_BUTTON)
PersegiLebar_color_active = pygame.Color(BLACK)
PersegiLebar_color = PersegiLebar_color_inactive
PersegiLebar_active = False
PersegiLebar_input_text = ''

# Input box Garis (GarisStartX)
GarisStartX_input_box = pygame.Rect(25, 60, 200, 40)
GarisStartX_color_inactive = pygame.Color(BLUE_BUTTON)
GarisStartX_color_active = pygame.Color(BLACK)
GarisStartX_color = GarisStartX_color_inactive
GarisStartX_active = False
GarisStartX_input_text = ''

# Input box Garis (GarisStartY)
GarisStartY_input_box = pygame.Rect(25, 140, 200, 40)
GarisStartY_color_inactive = pygame.Color(BLUE_BUTTON)
GarisStartY_color_active = pygame.Color(BLACK)
GarisStartY_color = GarisStartY_color_inactive
GarisStartY_active = False
GarisStartY_input_text = ''

# Input box Garis (GarisEndX)
GarisEndX_input_box = pygame.Rect(25, 220, 200, 40)
GarisEndX_color_inactive = pygame.Color(BLUE_BUTTON)
GarisEndX_color_active = pygame.Color(BLACK)
GarisEndX_color = GarisEndX_color_inactive
GarisEndX_active = False
GarisEndX_input_text = ''

# Input box Garis (GarisEndY)
GarisEndY_input_box = pygame.Rect(25, 300, 200, 40)
GarisEndY_color_inactive = pygame.Color(BLUE_BUTTON)
GarisEndY_color_active = pygame.Color(BLACK)
GarisEndY_color = GarisEndY_color_inactive
GarisEndY_active = False
GarisEndY_input_text = ''

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

        # Gambar tombol
        for button in ButtonsMenu:
            btn_surf = Button(0, 0, 300, 80, button['label'], button['TextColor'], button['ButtonColor'], 25, 18)
            screen.blit(btn_surf, button['pos'])

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in ButtonsMenu:
                    if button['label'] == 'Exit' and isClicked((mouse_x, mouse_y), button['pos'], 300, 80):
                        running = False
                    elif button['label'] == 'Mulai Menggambar' and isClicked((mouse_x, mouse_y), button['pos'], 300, 80):
                        ShowMenu = False
                        ShowPageMenggambar = True

    # Page Mulai Menggambar
    elif ShowPageMenggambar:
        # Canvas untuk menggambar
        pygame.draw.rect(screen, BLACK, (250, 10, 940, 680)) #1190x690
        pygame.draw.rect(screen, WHITE, (255, 15, 930, 670)) #1185x685

        for bentuk in Shape:
            if bentuk[0] == 'persegi':
                x, y, width, height = bentuk[1:]
                persegi_surf = draw_persegi(x, y, width, height)
                screen.blit(persegi_surf, (x + 255, y + 15))
            elif bentuk[0] == 'garis':
                garis_surf = draw_garis(bentuk[1], bentuk[2], bentuk[3], bentuk[4])
                screen.blit(garis_surf, (min(bentuk[1], bentuk[3]) + 255, min(bentuk[2], bentuk[4]) + 15))
        
        # Gambar tombol
        for button in ButtonsMenggambar:
            if button['label'] == "Clear" or button['label'] == "Undo":
                btn_surf = Button(0, 0, 90, 180, button['label'], button['TextColor'], button['ButtonColor'], 25, 18)
            else:
                btn_surf = Button(0, 0, 200, 80, button['label'], button['TextColor'], button['ButtonColor'], 25, 18)
            screen.blit(btn_surf, button['pos'])

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in ButtonsMenggambar:
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
                    elif button['label'] == 'Clear' and isClicked((mouse_x, mouse_y), button['pos'], 90, 180):
                        Shape.clear()
                    elif button['label'] == 'Undo' and isClicked((mouse_x, mouse_y), button['pos'], 90, 180):
                        if len(Shape) == 0:
                            pass
                        else:
                            Shape.pop()
                        print(Shape)
                    elif button['label'] == 'Back' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        ShowMenu = True
                        ShowPageMenggambar = False
                        Shape.clear()

    # Page Menggambar Persegi
    elif ShowPagePersegi:
        # Canvas untuk menggambar
        pygame.draw.rect(screen, BLACK, (250, 10, 940, 680)) #1190x690
        pygame.draw.rect(screen, WHITE, (255, 15, 930, 670)) #1185x685

        for bentuk in Shape:
            if bentuk[0] == 'persegi':
                x, y, width, height = bentuk[1:]
                persegi_surf = draw_persegi(x, y, width, height)
                screen.blit(persegi_surf, (x + 255, y + 15))
            elif bentuk[0] == 'garis':
                garis_surf = draw_garis(bentuk[1], bentuk[2], bentuk[3], bentuk[4])
                screen.blit(garis_surf, (min(bentuk[1], bentuk[3]) + 255, min(bentuk[2], bentuk[4]) + 15))
        
        for button in ButtonsPersegi:
            btn_surf = Button(0, 0, 200, 80, button['label'], button['TextColor'], button['ButtonColor'], 25, 18)
            screen.blit(btn_surf, button['pos'])

        PersegiStartX = InputBox(screen,
                                 font,
                                 PersegiStartX_input_box,
                                 PersegiStartX_input_text,
                                 PersegiStartX_color_inactive,
                                 PersegiStartX_color_active,
                                 PersegiStartX_active)
        
        PersegiStartY = InputBox(screen,
                                 font,
                                 PersegiStartY_input_box,
                                 PersegiStartY_input_text,
                                 PersegiStartY_color_inactive,
                                 PersegiStartY_color_active,
                                 PersegiStartY_active)
        
        PersegiPanjang = InputBox(screen,
                                 font,
                                 PersegiPanjang_input_box,
                                 PersegiPanjang_input_text,
                                 PersegiPanjang_color_inactive,
                                 PersegiPanjang_color_active,
                                 PersegiPanjang_active)
        
        PersegiLebar = InputBox(screen,
                                 font,
                                 PersegiLebar_input_box,
                                 PersegiLebar_input_text,
                                 PersegiLebar_color_inactive,
                                 PersegiLebar_color_active,
                                 PersegiLebar_active)
        
        draw_text(screen, "Titik Mulai Sumbu X", fontPersegi, (25, 40), pygame.Color('black'))
        draw_text(screen, "Titik Mulai Sumbu Y", fontPersegi, (25, 120), pygame.Color('black'))
        draw_text(screen, "Panjang", fontPersegi, (25, 200), pygame.Color('black'))
        draw_text(screen, "Lebar", fontPersegi, (25, 280), pygame.Color('black'))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in ButtonsPersegi:
                    if button['label'] == 'Update' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        if Update == 0:
                            x = int(PersegiStartX_input_text)
                            y = int(PersegiStartY_input_text)
                            Panjang = int(PersegiPanjang_input_text)
                            Lebar = int(PersegiLebar_input_text)
                            Shape.append(('persegi', x, y, Panjang, Lebar))
                            Update += 1
                        if Update > 0:
                            x = int(PersegiStartX_input_text)
                            y = int(PersegiStartY_input_text)
                            Panjang = int(PersegiPanjang_input_text)
                            Lebar = int(PersegiLebar_input_text)
                            Shape.pop()
                            Shape.append(('persegi', x, y, Panjang, Lebar))
                    elif button['label'] == 'Save' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        try:
                            x = int(PersegiStartX_input_text)
                            y = int(PersegiStartY_input_text)
                            Panjang = int(PersegiPanjang_input_text)
                            Lebar = int(PersegiLebar_input_text)
                            Shape.append(('persegi', x, y, Panjang, Lebar))
                            PersegiStartX_input_text = ''
                            PersegiStartY_input_text = ''
                            PersegiPanjang_input_text = ''
                            PersegiLebar_input_text = ''
                            x = 0
                            y = 0
                            panjang = 0
                            lebar = 0
                            Update = 0
                        except ValueError:
                            continue
                        ShowPagePersegi = False
                        ShowPageMenggambar = True
                    elif button['label'] == 'Back' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        ShowPageMenggambar = True
                        ShowPagePersegi = False
                        PersegiStartX_input_text = ''
                        PersegiStartY_input_text = ''
                        PersegiPanjang_input_text = ''
                        PersegiLebar_input_text = ''
                        x = 0
                        y = 0
                        panjang = 0
                        lebar = 0
                        Update = 0

                if PersegiStartX_input_box.collidepoint(event.pos):
                    PersegiStartX_active = not PersegiStartX_active
                    PersegiStartY_active = False
                    PersegiPanjang_active = False
                    PersegiLebar_active = False
                elif PersegiStartY_input_box.collidepoint(event.pos):
                    PersegiStartY_active = not PersegiStartY_active
                    PersegiStartX_active = False
                    PersegiPanjang_active = False
                    PersegiLebar_active = False
                elif PersegiPanjang_input_box.collidepoint(event.pos):
                    PersegiPanjang_active = not PersegiPanjang_active
                    PersegiStartX_active = False
                    PersegiStartY_active = False
                    PersegiLebar_active = False
                elif PersegiLebar_input_box.collidepoint(event.pos):
                    PersegiLebar_active = not PersegiLebar_active
                    PersegiStartX_active = False
                    PersegiStartY_active = False
                    PersegiPanjang_active = False
                else:
                    PersegiStartX_active = False
                    PersegiStartY_active = False
                    PersegiPanjang_active = False
                    PersegiLebar_active = False

            elif event.type == pygame.KEYDOWN and PersegiStartX_active:
                if event.key == pygame.K_RETURN:
                    PersegiStartX_input_text = int(PersegiStartX_input_text)
                elif event.key == pygame.K_BACKSPACE:
                    PersegiStartX_input_text = PersegiStartX_input_text[:-1]
                else:
                    PersegiStartX_input_text += event.unicode
                    x = PersegiStartX_input_text

            elif event.type == pygame.KEYDOWN and PersegiStartY_active:
                if event.key == pygame.K_RETURN:
                    PersegiStartY_input_text = int(PersegiStartY_input_text)
                elif event.key == pygame.K_BACKSPACE:
                    PersegiStartY_input_text = PersegiStartY_input_text[:-1]
                else:
                    PersegiStartY_input_text += event.unicode
                    y = PersegiStartY_input_text

            elif event.type == pygame.KEYDOWN and PersegiPanjang_active:
                if event.key == pygame.K_RETURN:
                    PersegiPanjang_input_text = int(PersegiPanjang_input_text)
                elif event.key == pygame.K_BACKSPACE:
                    PersegiPanjang_input_text = PersegiPanjang_input_text[:-1]
                else:
                    PersegiPanjang_input_text += event.unicode
                    Panjang = PersegiPanjang_input_text

            elif event.type == pygame.KEYDOWN and PersegiLebar_active:
                if event.key == pygame.K_RETURN:
                    PersegiLebar_input_text = int(PersegiLebar_input_text)
                elif event.key == pygame.K_BACKSPACE:
                    PersegiLebar_input_text = PersegiLebar_input_text[:-1]
                else:
                    PersegiLebar_input_text += event.unicode
                    Lebar = PersegiLebar_input_text

    # Page Menggambar Lingkaran
    elif ShowPageLingkaran:
        # Canvas untuk menggambar
        pygame.draw.rect(screen, BLACK, (250, 10, 940, 680)) #1190x690
        pygame.draw.rect(screen, WHITE, (255, 15, 930, 670)) #1185x685
        
        for button in ButtonsLingkaran:
            btn_surf = Button(0, 0, 200, 80, button['label'], button['TextColor'], button['ButtonColor'], 25, 18)
            screen.blit(btn_surf, button['pos'])

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in ButtonsLingkaran:
                    if button['label'] == 'Update' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        pass
                    elif button['label'] == 'Save' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        pass
                    elif button['label'] == 'Back' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        ShowPageMenggambar = True
                        ShowPageLingkaran = False

    # Page Menggambar Garis
    elif ShowPageGaris:
        # Canvas untuk menggambar
        pygame.draw.rect(screen, BLACK, (250, 10, 940, 680)) #1190x690
        pygame.draw.rect(screen, WHITE, (255, 15, 930, 670)) #1185x685

        for bentuk in Shape:
            if bentuk[0] == 'persegi':
                x, y, width, height = bentuk[1:]
                persegi_surf = draw_persegi(x, y, width, height)
                screen.blit(persegi_surf, (x + 255, y + 15))
            elif bentuk[0] == 'garis':
                garis_surf = draw_garis(bentuk[1], bentuk[2], bentuk[3], bentuk[4])
                screen.blit(garis_surf, (min(bentuk[1], bentuk[3]) + 255, min(bentuk[2], bentuk[4]) + 15))
        
        for button in ButtonsGaris:
            btn_surf = Button(0, 0, 200, 80, button['label'], button['TextColor'], button['ButtonColor'], 25, 18)
            screen.blit(btn_surf, button['pos'])

        GarisStartX = InputBox(screen,
                                 font,
                                 GarisStartX_input_box,
                                 GarisStartX_input_text,
                                 GarisStartX_color_inactive,
                                 GarisStartX_color_active,
                                 GarisStartX_active)
        
        GarisStartY = InputBox(screen,
                                 font,
                                 GarisStartY_input_box,
                                 GarisStartY_input_text,
                                 GarisStartY_color_inactive,
                                 GarisStartY_color_active,
                                 GarisStartY_active)
        
        GarisEndX = InputBox(screen,
                                 font,
                                 GarisEndX_input_box,
                                 GarisEndX_input_text,
                                 GarisEndX_color_inactive,
                                 GarisEndX_color_active,
                                 GarisEndX_active)
        
        GarisEndY = InputBox(screen,
                                 font,
                                 GarisEndY_input_box,
                                 GarisEndY_input_text,
                                 GarisEndY_color_inactive,
                                 GarisEndY_color_active,
                                 GarisEndY_active)
        
        draw_text(screen, "Titik Mulai Sumbu X", fontPersegi, (25, 40), pygame.Color('black'))
        draw_text(screen, "Titik Mulai Sumbu Y", fontPersegi, (25, 120), pygame.Color('black'))
        draw_text(screen, "Titik Akhir Sumbu X", fontPersegi, (25, 200), pygame.Color('black'))
        draw_text(screen, "Titik Akhir Sumbu Y", fontPersegi, (25, 280), pygame.Color('black'))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in ButtonsGaris:
                    if button['label'] == 'Update' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        if Update == 0:
                            x = int(GarisStartX_input_text)
                            y = int(GarisStartY_input_text)
                            endx = int(GarisEndX_input_text)
                            endy = int(GarisEndY_input_text)
                            Shape.append(('garis', x, y, endx, endy))
                            Update += 1
                        if Update > 0:
                            x = int(GarisStartX_input_text)
                            y = int(GarisStartY_input_text)
                            endx = int(GarisEndX_input_text)
                            endy = int(GarisEndY_input_text)
                            Shape.pop()
                            Shape.append(('garis', x, y, endx, endy))
                    elif button['label'] == 'Save' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        try:
                            x = int(GarisStartX_input_text)
                            y = int(GarisStartY_input_text)
                            endx = int(GarisEndX_input_text)
                            endy = int(GarisEndY_input_text)
                            Shape.append(('garis', x, y, endx, endy))
                            GarisStartX_input_text = ''
                            GarisStartY_input_text = ''
                            GarisEndX_input_text = ''
                            GarisEndY_input_text = ''
                            x = 0
                            y = 0
                            endx = 0
                            endy = 0
                            Update = 0
                        except ValueError:
                            continue
                        ShowPagePersegi = False
                        ShowPageMenggambar = True
                    elif button['label'] == 'Back' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        ShowPageMenggambar = True
                        ShowPageGaris = False
                        GarisStartX_input_text = ''
                        GarisStartY_input_text = ''
                        GarisEndX_input_text = ''
                        GarisEndY_input_text = ''
                        x = 0
                        y = 0
                        endx = 0
                        endy = 0
                        Update = 0

                if GarisStartX_input_box.collidepoint(event.pos):
                    GarisStartX_active = not GarisStartX_active
                    GarisStartY_active = False
                    GarisEndX_active = False
                    GarisEndY_active = False
                elif GarisStartY_input_box.collidepoint(event.pos):
                    GarisStartY_active = not GarisStartY_active
                    GarisStartX_active = False
                    GarisEndX_active = False
                    GarisEndY_active = False
                elif GarisEndX_input_box.collidepoint(event.pos):
                    GarisEndX_active = not GarisEndX_active
                    GarisStartX_active = False
                    GarisStartY_active = False
                    GarisEndY_active = False
                elif GarisEndY_input_box.collidepoint(event.pos):
                    GarisEndY_active = not GarisEndY_active
                    GarisStartX_active = False
                    GarisStartY_active = False
                    GarisEndX_active = False
                else:
                    GarisStartX_active = False
                    GarisStartY_active = False
                    PersegiPanjang_active = False
                    PersegiLebar_active = False

            elif event.type == pygame.KEYDOWN and GarisStartX_active:
                if event.key == pygame.K_RETURN:
                    GarisStartX_input_text = int(GarisStartX_input_text)
                elif event.key == pygame.K_BACKSPACE:
                    GarisStartX_input_text = GarisStartX_input_text[:-1]
                else:
                    GarisStartX_input_text += event.unicode
                    x = GarisStartX_input_text

            elif event.type == pygame.KEYDOWN and GarisStartY_active:
                if event.key == pygame.K_RETURN:
                    GarisStartY_input_text = int(GarisStartY_input_text)
                elif event.key == pygame.K_BACKSPACE:
                    GarisStartY_input_text = GarisStartY_input_text[:-1]
                else:
                    GarisStartY_input_text += event.unicode
                    y = GarisStartY_input_text

            elif event.type == pygame.KEYDOWN and GarisEndX_active:
                if event.key == pygame.K_RETURN:
                    GarisEndX_input_text = int(GarisEndX_input_text)
                elif event.key == pygame.K_BACKSPACE:
                    GarisEndX_input_text = GarisEndX_input_text[:-1]
                else:
                    GarisEndX_input_text += event.unicode
                    endx = GarisEndX_input_text

            elif event.type == pygame.KEYDOWN and GarisEndY_active:
                if event.key == pygame.K_RETURN:
                    GarisEndY_input_text = int(GarisEndY_input_text)
                elif event.key == pygame.K_BACKSPACE:
                    GarisEndY_input_text = GarisEndY_input_text[:-1]
                else:
                    GarisEndY_input_text += event.unicode
                    endy = GarisEndY_input_text

    # Page Menggambar Kurva
    elif ShowPageKurva:
        # Canvas untuk menggambar
        pygame.draw.rect(screen, BLACK, (250, 10, 940, 680)) #1190x690
        pygame.draw.rect(screen, WHITE, (255, 15, 930, 670)) #1185x685

        for button in ButtonsKurva:
            btn_surf = Button(0, 0, 200, 80, button['label'], button['TextColor'], button['ButtonColor'], 25, 18)
            screen.blit(btn_surf, button['pos'])

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in ButtonsGaris:
                    if button['label'] == 'Update' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        pass
                    elif button['label'] == 'Save' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        pass
                    elif button['label'] == 'Back' and isClicked((mouse_x, mouse_y), button['pos'], 200, 80):
                        ShowPageMenggambar = True
                        ShowPageKurva = False

    pygame.display.flip()

pygame.quit()
