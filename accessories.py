import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE
import random
pygame.init()
w, h = 750, 550
win = pygame.display.set_mode((w, h), HWSURFACE | DOUBLEBUF | RESIZABLE)

clock = pygame.time.Clock()

wc = []
for i in 'MINESWEEPER':
    wc.append((random.randrange(0, 255),
               random.randrange(0, 255),
               random.randrange(0, 255)))

r = 0

font2 = pygame.font.SysFont('Chiller', 25, True)
fnt3 = pygame.font.SysFont("jetbrains mono", 20)
font4 = pygame.font.SysFont("jetbrains mono", 10)

ncolor = {1: (100, 0, 100),
          2: (0, 100, 200),
          3: (100, 100, 0),
          4: (200, 100, 0),
          5: (0, 200, 100),
          6: (0, 100, 100),
          7: (100, 200, 0),
          8: (0, 100, 200)}

def random_colors():
    return (random.randrange(0, 255),
            random.randrange(0, 255),
            random.randrange(0, 255))


def drawbombs(b, size):
    # pygame.draw.rect(win ,bcolor[block.index(b)],(b,(size,size)))
    pygame.draw.circle(win, (0, 0, 0), (b[0] + size // 2, b[1] + size // 2), size // 4)
    pygame.draw.circle(win, random_colors(), (b[0] + size // 2, b[1] + size // 2), size // 4, 1)
    pygame.draw.line(win, (200, 0, 0), (b[0] + size//3, b[1] + size//3), (b[0] + size - size//3, b[1] + size - size//3), 3)
    pygame.draw.line(win, (200, 0, 0), (b[0] + size - size//3, b[1] + size//3), (b[0] + size//3, b[1] + size - size//3), 3)

bg_rects = []
for i in range(w//50):
    bg_rects.append([random.randrange(0, w), random.randrange(0, h), random.randrange(0, 100), random_colors(), random.randrange(0, 9)])


def background():
    for i in bg_rects:
        i[1] += 10
        if i[1] >= h:
            bg_rects.pop(bg_rects.index(i))
            bg_rects.append([random.randrange(0, w), 0, random.randrange(10, 50), random_colors(), random.randrange(0, 9)])
        else:
            # pygame.draw.circle(win, random_colors(), (i[0], i[1]), i[2], 1)

            if i[4] != 0:
                pygame.draw.rect(win, (255, 255, 255), (i[0], i[1], 25, 25))
                win.blit(font2.render(str(i[4]), 1, ncolor[i[4]]), i[0:2])
            else:
                drawbombs(i[0:2], 40)


def start_anim(block, size):
    global w, h
    win.fill((255, 255, 255))
    b = []
    n = True
    font2 = pygame.font.SysFont('system', 20, True)
    for i in range(0, len(block)):
        b.append([block[i][0], block[i][1], 0])
    load_x, load_y, load = w//2 -100, h - 100, 0
    while n:
        load = (b[0][2]/size) * 100
        for _ in range(len(b)):
            i = b[_]
            pygame.draw.rect(win, (100, 100, 100), (i[0] + size//2 - i[2]//2, i[1] + size//2 - i[2]//2, i[2], i[2]))
            pygame.draw.rect(win, (0, 0, 0), (i[0] + size//2 - i[2]//2, i[1] + size//2 - i[2]//2, i[2], i[2]), 1)

            if i[2] + 5 <= size:
                i[2] += 5
            else:
                n = False

            pygame.draw.rect(win, (0, 0, 0), (load_x - 2, load_y - 2, 200 + 4, 40 + 4))
            pygame.draw.rect(win, (0, 200, 0), (load_x, load_y, load * 2, 20))
            win.blit(font2.render(f"Rendering...{int(load)}%", 1, (0, 200, 0)), (load_x, load_y + 20))
            pygame.display.update()
        clock.tick(8)

def start_anim2(block, size):
    win.fill((0, 0, 0))
    b = []
    n = True
    s = size
    i = 0
    random.shuffle(block)
    while n:
        # s = int((len(b)/len(block)) * size)
        # new = block[i]
        # if b.count(new) == 0:
        #     b.append(new)
        #     i += 1
        b.append(block[i])
        i += 1
        for _ in b:
            # pygame.draw.rect(win, (100, 100, 100), (_[0]+size//2 - s//2, _[1]+size//2 - s//2, s, s))
            # pygame.draw.rect(win, (0, 0, 0), (_[0]+size//2 - s//2, _[1]+size//2 - s//2, s, s), 1)

            pygame.draw.rect(win, (100, 100, 100), (_[0], _[1], size, size))
            pygame.draw.rect(win, (0, 0, 0), (_[0], _[1], size, size), 1)

        if len(b) == len(block):
            break

        pygame.display.update()
        clock.tick(30)

def heading(w, h):
    global r
    st = 'MINESWEEPER'
    pygame.draw.rect(win, (255, 255, 255), (w // 2 - 100, h // 4 - 55, 275, 35))
    pygame.draw.rect(win, (200, 0, 0), (w // 2 - 100, h // 4 - 55, 275, 35), 1)
    for i in range(0, len(st)):
        s = st[i]
        if r <= 360:
            if i % 2 == 0:
                ang = 360 - r  # color = (0, 255, 0)
            else:
                ang = r
            win.blit(pygame.transform.rotate(fnt3.render(s, 1, wc[i]),
                                             ang), (w // 2 - 100 + (i * 25), h // 4 - 50))
        else:
            r = 0
        r += 1

    wc.pop(len(wc) - 1)
    wc.insert(0, random_colors())

def textbox(c, wid):
    global w, h
    s = ""
    n = True
    while n:
        pygame.draw.rect(win, (255, 255, 255), (c[0], c[1], wid, 30))
        pygame.draw.rect(win, (0, 200, 0), (c[0], c[1], wid, 30), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                w = screen.get_width()
                h = screen.get_height()
            if event.type == pygame.MOUSEBUTTONDOWN and len(s) > 0: return s
            if event.type == pygame.KEYDOWN:
                l = str(pygame.key.name(event.key))
                if l == "backspace":  s = s[0:len(s) - 1]
                if l == "space":      s += " "
                if l == "return" and len(s) > 0: return s
                if len(l) == 1 and len(s) <= 15:
                    s += l
                    s = s.upper()
                else:
                    pygame.draw.rect(win, (200, 0, 0), (c[0], c[1], wid, 30), 3)
        txt = font2.render(s, 1, (0, 0, 0))
        win.blit(txt, c)

        if wid < txt.get_width():
            wid = txt.get_width()
        pygame.display.update()
        clock.tick(20)
    restart()

def drawflag(c, size):
    # pygame.draw.rect(win,(0,0,200),(flag[i],(size,size)))
    pygame.draw.polygon(win, (200, 0, 0), ((c[0] + int(0.32 * size), c[1] + int(0.28 * size)),
                                           (c[0] + int(0.32 * size), c[1] + int(0.52 * size)),
                                           (c[0] + int(0.64 * size), c[1] + int(0.4 * size))))
    pygame.draw.polygon(win, (0, 0, 0), ((c[0] + int(0.32 * size), c[1] + int(0.28 * size)),
                                         (c[0] + int(0.32 * size), c[1] + int(0.52 * size)),
                                         (c[0] + int(0.64 * size), c[1] + int(0.4 * size))), 1)
    pygame.draw.line(win, (0, 0, 0), (c[0] + int(0.32 * size), c[1] + int(0.28 * size)),
                     (c[0] + int(0.32 * size), c[1] + int(0.8 * size)), 2)
    pygame.draw.line(win, (0, 0, 0), (c[0] + int(0.2 * size), c[1] + int(0.8 * size)),
                     (c[0] + int(0.5 * size), c[1] + int(0.8 * size)), 2)

