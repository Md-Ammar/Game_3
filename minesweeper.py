import pygame
import random
from datetime import datetime
import accessories as acc
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE
import os
import sys

pygame.init()
w, h = 750, 550
win = pygame.display.set_mode((w, h), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption("MINESWEEPER-a game by ammar")
# pygame.mouse.set_cursor(*pygame.cursors.broken_x)

clock = pygame.time.Clock()

fnt = pygame.font.SysFont("jetbrains mono", 30)
fnt2 = pygame.font.SysFont("jetbrains mono", 20)

run = True
ramrun = False

# DEFAULTS
rows = 10
cols = 15
bmcount = int(0.2 * (rows * cols))
name = ''

txtbx = pygame.Rect(70, h - 30, 100, 20)
keycount = 0  # flag time delay counter

fps = 25

first = 0



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# img = pygame.transform.scale(pygame.image.load(resource_path("background.jpg")), (w, h))


def resizing():
    global w, h, size, rows, cols, bmcount, num_font, block

    nr = (h - 50) // rows
    nc = w // cols
    size = nc if nc < nr else nr
    block = []
    for i in range(0, cols * size, size):
        for j in range(0, rows * size, size):
            block.append((i, j))

    num_font = pygame.font.SysFont("Jetbrains mono", size-5)


def init():
    global block, bcolor, bombs, bnos, flag, Hint
    Hint = {'status': False, 'number': 2}
    block = []
    bcolor = []
    bombs = []
    bnos = []
    flag = []
    dif = int((bmcount * 100) / (rows * cols))
    no_of_hints = {(0, 20): 1,
                  (20, 40): 2,
                  (40, 50): 3,
                  (50, 60): 4,
                  (60, 70): 5,
                  (70, 100): 6}
    for ranges in no_of_hints.keys():
        if dif in range(ranges[0], ranges[1]):
            Hint = {'status': False, 'number': no_of_hints[ranges]}
    resizing()


def grid():
    global rows, cols, block
    block = []
    for i in range(0, cols * size, size):
        for j in range(0, rows * size, size):
            block.append((i, j))
            bcolor.append((0, 0, 0))
            bnos.append(0)


def Bombs():
    global rows, cols, bombs, bmcount
    count = 0

    while count < bmcount:
        x = random.randrange(0, cols * size, size)
        y = random.randrange(0, rows * size, size)
        if bombs.count((x, y)) == 0:
            bombs.append((x, y))
            count += 1

    for b in bombs:
        ind = block.index(b)
        bcolor[ind] = (200, 0, 0)


def get_surr(b):
    up = (b[0], b[1] - size)
    down = (b[0], b[1] + size)
    left = (b[0] - size, b[1])
    right = (b[0] + size, b[1])

    d1 = (b[0] - size, b[1] - size)
    d2 = (b[0] + size, b[1] - size)
    d3 = (b[0] - size, b[1] + size)
    d4 = (b[0] + size, b[1] + size)

    return [up, left, right, down, d1, d2, d3, d4]


def get_first(lim):
    global first
    first = []

    for b in block:
        if bcolor[block.index(b)] != (200, 0, 0) and bnos[block.index(b)] == 0:
            c = 0
            surr = get_surr(b)

            for s in surr:
                if s in block and bnos[block.index(s)] == 0:
                    c += 1

            if c == lim:
                first = b
                break

    if not first:
        get_first(lim - 1)


def wipe_adj(b):
    surr = get_surr(b)

    for s in surr:
        if block.count(s) > 0:
            # if not bcolor[block.index(s)] == (0, 200, 0) and not bcolor[block.index(s)] == (200, 0, 0):
            bcolor[block.index(s)] = (0, 200, 0)


def count_adj(b):
    global ramrun
    h = 0

    surr = get_surr(b)

    for s in surr:
        if block.count(s) > 0:
            if bcolor[block.index(s)] == (200, 0, 0):
                h += 1
    if h > 0:
        bnos[block.index(b)] = h
        ramrun = False
    # if h==0 and bcolor[block.index(b)]==(0,200,0):wipe_adj(b)


def restart():
    global Sec, Min, start, name
    start = datetime.now().time()
    # Sec=Min=0
    init()
    grid()
    Bombs()
    name = ""
    for b in block:
        count_adj(b)
    co = 0
    for b in bombs:
        if block.count(b) == 0:
            co += 1
        else:
            ind = block.index(b)
            bcolor[ind] = (200, 0, 0)

    if bmcount == int(0.2 * (rows * cols)):
        lim = 8
    else:
        lim = int((1 - (bmcount / (rows * cols))) * 8)
    get_first(lim)
    # acc.start_anim2(block, size)


# restart()

def gameover():
    global w, h
    n = True
    t = fnt.render("GAMEOVER!", 1, (0, 200, 0))
    txt = fnt.render("BETTER LUCK NEXT TIME !", 1, (0, 200, 0))
    wid = txt.get_width()
    ht = txt.get_height()

    for bl in block:
        i = block.index(bl)
        pygame.draw.rect(win, (0, 0, 0), (bl, (size, size)), 1)
        if bcolor[block.index(bl)] == (200, 0, 0):
            acc.drawbombs(bl, size)
        if bnos[i] > 0 and bcolor[i] != (200, 0, 0):
            win.blit(num_font.render(str(bnos[i]), 1, acc.ncolor[bnos[i]]), (block[i][0] + 4, block[i][1] + 4))
    pygame.display.update()

    while n:
        statusbar("_", "_")
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
        for bl in range(len(block)):
            if bcolor[bl] == (200, 0, 0):
                acc.drawbombs(block[bl], size)
        pygame.display.update()
        clock.tick(5)


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
        if bnos[i] > 0 and bcolor[i] != (200, 0, 0):
            win.blit(num_font.render(str(bnos[i]), 1, acc.ncolor[bnos[i]]), (block[i][0] + 4, block[i][1] + 4))

    while n:
        statusbar("_", "_")
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
    txt = ['CONTROLS', ' ', 'RT. CLICK  - OPEN TILE', 'LT. CLICK - FLAG/UNFLAG TILE', 'H - HINT',
           'Z - REMOVE LAST FLAG', 'R - RESTART', 'TAB - MENU', 'ESC - EXIT', ' ', 'PRESS ANY KEY TO CONTINUE']

    while n:
        win.fill((0, 0, 0))
        for i in range(0, len(txt)):
            color = (0, 200, 0)
            if i == 0: color = (200, 200, 200)
            if i == 8: color = (200, 0, 0)
            if i == 10: color = (200, 200, 0)
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


def get_difficulty(d):
    difficulty = {(0, 20): "SUPER EASY",
                  (20, 40): "EASY",
                  (40, 50): "MEDIUM",
                  (50, 60): "HARD",
                  (60, 70): "SUPER HARD",
                  (70, 100): "INSANE"}
    for item in list(difficulty.keys()):
        if d in range(item[0], item[1]):
            return difficulty[item]


def menu():
    global w, h, bmcount, run, name, rows, cols, event
    name = ''
    n = True
    c = (255, 255, 255)
    inv = False
    txtr = (w // 2, h // 2 - 40)
    txtc = (w // 2, h // 2)
    txtbx = (w // 2, h // 2 + 40)
    while n:
        win.fill((0, 0, 0))
        acc.background()
        acc.heading(w, h)
        pygame.draw.rect(win, (200, 100, 200), (10, 10, w - 20, h - 20), 3)
        pygame.draw.rect(win, (0, 200, 200), (w // 2 - 100, h // 3 - 10, 250, 220))
        pygame.draw.rect(win, (255, 255, 255), (w // 2 - 100 + 10, h // 3 - 10 + 10, 250 - 20, 220 - 20), 5)

        win.blit(fnt.render("SETTINGS", 1, (0, 0, 0)), (w // 2 - 10, h // 3))
        win.blit(fnt.render("ROWS", 1, (0, 0, 100)), (w // 2 - 80, h // 2 - 40))
        win.blit(fnt.render("COLS", 1, (0, 100, 0)), (w // 2 - 80, h // 2))
        win.blit(fnt.render("MINES", 1, (200, 0, 0)), (w // 2 - 80, h // 2 + 40))

        dif = int((bmcount * 100) / (rows * cols))
        win.blit(fnt.render(f"DIFFICULTY {get_difficulty(dif)}({dif}%)", 1, (0, 0, 0)), (w // 2 - 80, h // 2 + 80))

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
                txtr = (w // 2, h // 2 - 40)
                txtc = (w // 2, h // 2)
                txtbx = (w // 2, h // 2 + 40)
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

                if pygame.Rect(w // 2 - 50, 3 * h // 4, 100, 30).collidepoint(x, y):  # start
                    n = False
                    pygame.draw.rect(win, (200, 200, 200), (w // 2 - 50 + 2, 3 * h // 4 + 2, 100 - 4, 30 - 4), 3)
                    pygame.display.update()
                    restart()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    n = False
                    restart()
                if event.key == pygame.K_ESCAPE:
                    n = False
                    run = False

            if bmcount > rows * cols:
                bmcount = int(rows * cols * 0.2)

            if inv:
                win.blit(fnt.render('INVALID INPUT!', 1, (200, 0, 0)), (w // 2 - 50, 3 * h // 4 - 20))
                pygame.display.update()
                pygame.time.delay(1000)
                inv = False
        pygame.display.update()
        clock.tick(10)


menu()


def statusbar(c, q):
    global bcolor, prog
    pygame.draw.rect(win, (0, 0, 0), (0, h - 50, w, 50))

    if name == '':
        win.blit(fnt2.render("PLAYER:", 1, (0, 200, 0)), (0, h - 30))
        pygame.draw.rect(win, (255, 255, 255), txtbx)
        win.blit(fnt2.render("<NAME>", 1, (100, 100, 100)), txtbx[0:2])
    else:
        win.blit(fnt2.render("PLAYER: " + name, 1, (0, 200, 0)), (0, h - 30))

    cfps = int(clock.get_fps())
    eff = int((cfps / fps) * 100)
    if eff > 100:
        eff = 100
    pygame.draw.rect(win, (eff // 100 * 250, 250 - (eff // 100 * 250), 0), (int(0.25 * w), h - 40, cfps * 6, 15))
    pygame.draw.rect(win, (200, 200, 200), (int(0.25 * w), h - 40, fps * 6, 15), 2)
    win.blit(fnt2.render("FPS : " + str(cfps) + "/" + str(fps) + "(" + str(eff) + "%" + ")", 1, (200, 0, 0)),
             (int(0.25 * w), h - 40))
    # win.blit(fnt2.render("FPS:" + str(cfp) + "/" + str(fps), 1, (200, 0, 0)), (200, h - 20))

    win.blit(fnt2.render("TIME:" + timetaken, 1, (0, 200, 0)), (int(0.45 * w), h - 40))
    win.blit(fnt2.render("POS: " + str(q) + "," + str(c), 1, (0, 200, 0)), (int(0.45 * w), h - 20))

    # win.blit(fnt2.render("BOMBS LEFT:" + str(bmcount - lef), 1, (0, 200, 0)), (w // 2 + 100, h - 40))
    prog = bcolor.count((0, 200, 0)) / (len(bcolor) - bcolor.count((200, 0, 0)))
    pygame.draw.rect(win, (0, 200, 200), (int(0.6 * w), h - 40, prog * 100, 15))
    pygame.draw.rect(win, (200, 200, 200), (int(0.6 * w), h - 40, 100, 15), 2)
    win.blit(fnt2.render("PROGRESS", 1, (200, 0, 0)), (int(0.6 * w) + 2, h - 40))
    win.blit(fnt2.render(str(int(prog * 100)) + "%", 1, (200, 0, 0)), (int(0.6 * w) + 100 + 2, h - 40))
    win.blit(fnt2.render("FLAGS/MINES:" + str(len(flag)) + "/" + str(bmcount), 1, (0, 200, 0)), (int(0.6 * w), h - 20))

    if Hint['status']:
        win.blit(fnt2.render("HINT ACTIVE", 1, acc.random_colors()), (int(0.8 * w), h - 40))
    else:
        win.blit(fnt2.render("HINTS(H) - " + str(Hint['number']), 1, (0, 200, 0)), (int(0.8 * w), h - 40))
    win.blit(fnt2.render("F1 - CONTROLS", 1, (0, 200, 0)), (int(0.8 * w), h - 20))


def redrawgamewindow():
    c = q = "_"
    global w, h, size, timetaken, fps, name, ramrun, keycount, first, Hint
    win.fill((100, 100, 100))
    # win.blit(img, (0, 0))

    for ind in range(0, len(block)):
        b = block[ind]

        # pygame.draw.rect(win, (100, 100, 100), (b, (size, size)))  # outline
        if bcolor[ind] == (0, 200, 0):
            pygame.draw.rect(win, (255, 255, 255), (b, (size, size)))
        pygame.draw.rect(win, (0, 0, 0), (b, (size, size)), 1)  # grid
        pygame.draw.rect(win, (200, 200, 200), (b[0] + 1, b[1] + 1, size - 2, size - 2), 1)

        if first != 0 and block.count(first) != 0 and bcolor[block.index(first)] != (0, 200, 0):
            pygame.draw.rect(win, acc.random_colors(), (first, (size, size)), 2)

        if name == 'AMMAR' and bcolor[ind] == (200, 0, 0):
            acc.drawbombs(b, size)

        if bcolor[ind] == (0, 200, 0) and bnos[ind] == 0:
            wipe_adj(b)

        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            if pygame.Rect(b, (size, size)).collidepoint(x, y):
                pygame.draw.rect(win, (255, 255, 255), (b, (size, size)), 2)
                c = int(ind / rows)
                q = ind - int(c * rows)

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            ramrun = True

            if Hint['status'] is True and pygame.Rect(b, (size, size)).collidepoint(x, y) and event.button == 1:
                ind = block.index(b)
                if bcolor[ind] == (200, 0, 0):
                    flag.append(b)
                Hint['number'] -= 1
                Hint['status'] = False


            elif pygame.Rect(b, (size, size)).collidepoint(x, y) and flag.count(b) == 0 and event.button == 1:
                ind = block.index(b)
                if bcolor[ind] == (200, 0, 0):
                    gameover()
                else:
                    bcolor[ind] = (0, 200, 0)
            if pygame.Rect(b, (size, size)).collidepoint(x, y) and event.button == 3:
                keycount += 1
                if flag.count(b) == 0 and not bcolor[block.index(b)] == (0, 200, 0) and keycount == 3:
                    flag.append(b)
                    keycount = 0
                elif flag.count(b) > 0 and keycount == 3:
                    flag.remove(b)
                    keycount = 0
        # else:
        #     keycount = 0

    for i in range(0, len(flag)):
        coord = flag[i]
        acc.drawflag(coord, size)
        if block.count(coord) != 0 and bcolor[block.index(coord)] == (0, 200, 0):
            flag.pop(i)
            break

    timetaken = str(
        datetime.combine(datetime.today(), datetime.now().time()) - datetime.combine(datetime.today(), start))[0:7]
    if bcolor.count((0, 200, 0)) == (rows * cols) - bmcount:
        complete()

    for i in range(0, len(bnos)):
        if bnos[i] > 0 and bcolor[i] == (0, 200, 0):
            win.blit(num_font.render(str(bnos[i]), 1, acc.ncolor[bnos[i]]), (block[i][0] + 4, block[i][1] + 4))

    statusbar(c, q)

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if txtbx.collidepoint(x, y) and name == '':
            name = acc.textbox(txtbx[0:2], txtbx[2])

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_z and len(flag) > 0 and keycount == 0:
            flag.pop(len(flag) - 1)
            pygame.time.wait(50)
    pygame.display.update()


while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
            w = screen.get_width()
            h = screen.get_height()
            txtbx = pygame.Rect(70, h - 40, 100, 30)
            win.fill((200, 200, 200))
            resizing()
            # acc.start_anim(block, size)
            # restart()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False

    if keys[pygame.K_TAB]:
        menu()

    if keys[pygame.K_r]:
        restart()

    if keys[pygame.K_F1]:
        Help()

    if keys[pygame.K_h] and Hint['number'] > 0:
        if Hint['status'] is False:
            Hint['status'] = True
        else:
            Hint['status'] = False

    redrawgamewindow()
pygame.quit()
