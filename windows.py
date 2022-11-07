import pygame, random
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE
import accessories as acc
pygame.init()
w, h = 750, 550
win = pygame.display.set_mode((w, h), HWSURFACE | DOUBLEBUF | RESIZABLE)

fnt = pygame.font.SysFont("comicsans", 30)
fnt2 = pygame.font.SysFont("comicsans", 20)
fnt3 = pygame.font.SysFont("comicsans", 30)

r = 0

wv = 0
wc = []
for i in 'MINESWEEPER':
    wc.append((random.randrange(0, 255),
               random.randrange(0, 255),
               random.randrange(0, 255)))

clock = pygame.time.Clock()

Restart = False


def heading():
    global r, wv, wc
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
            # win.blit(pygame.transform.rotate(fnt3.render(s, 1, (random.randrange(0, 255),
            #                                                     random.randrange(0, 255),
            #                                                     random.randrange(0, 255))),
            #                                  ang), (w // 2 - 100 + (i * 25), h // 4 - 50))
            win.blit(pygame.transform.rotate(fnt3.render(s, 1, wc[i]),
                                             ang), (w // 2 - 100 + (i * 25), h // 4 - 50))
        else:
            r = 0
        r += 1

    wc.pop(len(wc) - 1)
    wc.insert(0, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))


def menu(bmcount, rows, cols):
    global w, h
    name = ''
    n = True
    c = (255, 255, 255)
    inv = False
    txtbx = (w // 2, h // 2)
    txtr = (w // 2, h // 2 + 40)
    txtc = (w // 2, h // 2 + 80)
    while n:
        win.fill((0, 0, 0))
        heading()
        pygame.draw.rect(win, (200, 100, 200), (10, 10, w - 20, h - 20), 3)
        pygame.draw.rect(win, (0, 200, 200), (w // 2 - 100, h // 3 - 10, 250, 220))
        pygame.draw.rect(win, (255, 255, 255), (w // 2 - 100 + 10, h // 3 - 10 + 10, 250 - 20, 220 - 20), 5)
        win.blit(fnt.render("SETTINGS", 1, (0, 0, 0)), (w // 2 - 10, h // 3))
        win.blit(fnt.render("MINES", 1, (200, 0, 0)), (w // 2 - 80, h // 2))
        win.blit(fnt.render("ROWS", 1, (0, 0, 100)), (w // 2 - 80, h // 2 + 40))
        win.blit(fnt.render("COLS", 1, (0, 100, 0)), (w // 2 - 80, h // 2 + 80))
        pygame.draw.rect(win, (0, 200, 0), (w // 2 - 50, 3 * h // 4, 100, 30))
        pygame.draw.rect(win, (0, 0, 0), (w // 2 - 50 + 2, 3 * h // 4 + 2, 100 - 4, 30 - 4), 1)
        win.blit(fnt.render("START", 1, (0, 0, 200)), (w // 2 - 40 + 5, 3 * h // 4 + 7))
        # win.blit(fnt.render("DEVELOPED BY AMMAR", 1, c), (w - 240, h - 40))

        pygame.draw.rect(win, c, (txtbx, (50, 30)))
        win.blit(fnt.render(str(bmcount), 1, (200, 100, 100)), txtbx[0:2])
        pygame.draw.rect(win, c, (txtr, (50, 30)))
        win.blit(fnt.render(str(rows), 1, (100, 100, 200)), txtr[0:2])
        pygame.draw.rect(win, c, (txtc, (50, 30)))
        win.blit(fnt.render(str(cols), 1, (100, 200, 100)), txtc[0:2])

        if int(rows * cols * 0.2) != bmcount:
            win.blit(fnt.render("RECOMMENDED " + str(int(rows * cols * 0.2)), 1, (200, 0, 0)),
                     (txtbx[0] + 50, txtbx[1]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                n = False
                run = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                w = screen.get_width()
                h = screen.get_height()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if pygame.Rect(txtbx, (50, 30)).collidepoint(x, y):
                    win.blit(fnt.render("RECOMMENDED " + str(int(rows * cols * 0.2)), 1, (100, 100, 100)),
                             (txtbx[0] + 50, txtbx[1]))
                    val = acc.textbox(txtbx, 50)
                    if val.isnumeric() and int(val) < rows * cols:
                        bmcount = int(val)
                    else:
                        inv = True
                if pygame.Rect(txtr, (50, 30)).collidepoint(x, y):
                    win.blit(fnt.render("<0-50>", 1, (100, 100, 100)), (txtr[0] + 50, txtr[1]))
                    val = acc.textbox(txtr, 50)
                    if val.isnumeric() and int(val) in range(0, 51):
                        rows = int(val)
                    else:
                        inv = True
                    pygame.display.update()
                if pygame.Rect(txtc, (50, 30)).collidepoint(x, y):
                    win.blit(fnt.render("<0-50>", 1, (100, 100, 100)), (txtc[0] + 50, txtc[1]))
                    val = acc.textbox(txtc, 50)
                    if val.isnumeric() and int(val) in range(0, 51):
                        cols = int(val)
                    else:
                        inv = True
                if bmcount > rows * cols:
                    bmcount = int(rows * cols * 0.2)
                # pygame.display.update()
                if inv:
                    win.blit(fnt.render('INVALID INPUT!', 1, (200, 0, 0)), (w // 2 - 50, 3 * h // 4 - 20))
                    pygame.display.update()
                    pygame.time.delay(1000)
                    inv = False

                if pygame.Rect(w // 2 - 50, 3 * h // 4, 100, 30).collidepoint(x, y):
                    n = False
                    pygame.draw.rect(win, (200, 200, 200), (w // 2 - 50 + 2, 3 * h // 4 + 2, 100 - 4, 30 - 4), 3)
                    pygame.display.update()
                    Restart = True
                    # transition()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: n = False; Restart = True
                if event.key == pygame.K_ESCAPE: n = False; run = False
        pygame.display.update()
        clock.tick(10)


def transition():
    n = True
    i = 0
    open = True
    vel = 10
    while n:
        win.fill((0, 0, 0))
        if open:
            if i <= h // 2:
                i += vel
            if i > h // 2:
                open = False
        if not open:
            if i >= 0:
                i -= vel
            if i < 0:
                n = False
        pygame.draw.rect(win, (100, 100, 100), (0, -h // 2 + i, w, h // 2))
        pygame.draw.rect(win, (100, 100, 100), (0, h - i, w, h // 2))
        pygame.display.update()
        clock.tick(20)


def complete():
    global w, h, timetaken
    n = True
    t = fnt.render("CONGRATULATIONS!", 1, (0, 200, 0))
    txt = fnt.render("COMPLETED IN " + str(timetaken), 1, (0, 200, 0))
    wid = txt.get_width()
    ht = txt.get_height()

    for bl in block:
        i = block.index(bl)
        pygame.draw.rect(win, (0, 0, 0), (bl, (size, size)), 1)
        if bcolor[block.index(bl)] == (200, 0, 0):
            drawbombs(bl)
        if bnos[i] > 0 and bcolor[i] != (200, 0, 0):
            win.blit(num_font.render(str(bnos[i]), 1, ncolor[bnos[i]]), (block[i][0] + 4, block[i][1] + 4))

    while n:
        gamestatus("_", "_")
        pygame.draw.rect(win, (0, 0, 0), (w // 2 - wid // 2 - 5, h // 2 - ht // 2 - 30, wid + 10, ht + 40))
        pygame.draw.rect(win, (0, 200, 0), (w // 2 - wid // 2 - 5, h // 2 - ht // 2 - 30, wid + 10, ht + 40), 1)
        win.blit(txt, (w // 2 - wid // 2, h // 2 - ht // 2 + 5))
        win.blit(t, (w // 2 - t.get_width() // 2, h // 2 - t.get_height() // 2 - 25))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                restart()
                n = False
        pygame.display.update()
        clock.tick(5)


def Help():
    global event, w, h, run
    n = True
    txt = ['HELP', ' ', 'RT. CLICK  - OPEN TILE', 'LT. CLICK - FLAG TILE',
           'Z - REMOVE LAST FLAG', 'R - RESTART', 'TAB - MENU', 'ESC - EXIT', ' ', 'PRESS ANY KEY TO CONTINUE']

    while n:
        win.fill((0, 0, 0))
        for i in range(0, len(txt)):
            color = (0, 200, 0)
            if i == 0: color = (200, 200, 200)
            if i == 7: color = (200, 0, 0)
            if i == 9: color = (200, 200, 0)
            t = fnt2.render(txt[i], 1, color)
            win.blit(t, (w // 2 - t.get_width() // 2, h // 2 - ((len(txt) // 2) * 30) + i * 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                w = screen.get_width()
                h = screen.get_height()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                n = False
        pygame.display.update()
        clock.tick(5)

t = []
for i in range(0, w, 25):
    for j in range(0, h, 25):
        t.append(pygame.Rect(i, j, 25, 25))

def trans(T):
    global t

    for b in t:
        pygame.draw.rect(win, (0, 0, 0), b)

    if len(t) > 0:
        temp = random.randrange(0, len(t))
    if len(t) > 0:
        t.remove(t[temp])
    else:
        return False

    pygame.display.update()
    return True