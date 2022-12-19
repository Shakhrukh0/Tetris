import pygame
from copy import deepcopy
from random import choice, randrange

'''Воспроизведение музыки для игры'''
pygame.mixer.init()
pygame.mixer.music.load('tetris.mp3')
pygame.mixer.music.play(-1)
'''Создание игрового поля с заданным разрешением'''
w, h = 10, 20
tile = 34
game_res = w * tile, h * tile
res = 690, 740
fps = 60

pygame.init()
sc = pygame.display.set_mode(res)
game_sc = pygame.Surface(game_res)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * tile, y * tile, tile, tile) for x in range (w) for y in range (h)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + w // 2, y + 1, 1,1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, tile - 2, tile - 2)
field = [[0 for i in range(w)]for j in range(h)]

anim_count, anim_speed, anim_limit = 0, 60, 2000
'''Загрузка необходимых картинок на задний и передний фон'''
bg = pygame.image.load('ctf2.jpg').convert()
game_bg = pygame.image.load('ctf1.jpg').convert()

main_font = pygame.font.Font('font.ttf', 45)
font = pygame.font.Font('font.ttf', 25)

title_tetris = main_font.render('Тетрис', True, pygame.Color('yellow'))
title_score = font.render('Очки:', True, pygame.Color('blue'))
title_record = font.render('Рекорд:', True, pygame.Color('green'))

get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

'''Функция которая проверяет границы, что бы фигурки не вышли за пределы границы'''
def check_borders():
    if figure[i].x < 0 or figure[i].x > w - 1:
        return False
    elif figure[i].y > h - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


'''Функция для получения рекорда'''
def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')

'''Функция для установления рекорда'''
def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))

while True:
    record = get_record()
    dx, rotate = 0, False
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.blit(game_bg, (0, 0))
    # удаление заполненных линий
    for i in range(lines):
        pygame.time.wait(200)
    # управление клавиатурой
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 150
            elif event.key == pygame.K_UP:
                rotate = True
        # управление мышкой
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dx -= 1
            elif event.button == 3:
                dx += 1
            elif event.button == 2:
                anim_limit = 150
            elif event.button == 4:
                rotate = True

    # движение фигур вправо и влево
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
    # движение фигур вниз
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                break
    # блок кода для вращения
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break
    # проверка линий
    line, lines = h - 1, 0
    for row in range(h - 1, -1, -1):
        count = 0
        for i in range(w):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < w:
            line -= 1
        else:
            anim_speed += 3
            lines += 1
    # вычисление очков
    score += scores[lines]
    # рисование клеток
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
    # рисование фигур
    for i in range(4):
        figure_rect.x = figure[i].x * tile
        figure_rect.y = figure[i].y * tile
        pygame.draw.rect(game_sc, color, figure_rect)
    # поле для рисования
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * tile, y * tile
                pygame.draw.rect(game_sc, col, figure_rect)
    # рисование следующих фигур
    for i in range(4):
        figure_rect.x = next_figure[i].x * tile + 285
        figure_rect.y = next_figure[i].y * tile + 150
        pygame.draw.rect(sc, next_color, figure_rect)
    # рисование надписей и их координаты
    sc.blit(title_tetris, (385, 15))
    sc.blit(title_score, (400, 420))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (415, 460))
    sc.blit(title_record, (400, 315))
    sc.blit(font.render(record, True, pygame.Color('orange')), (415, 355))
    '''Игра заканчивается когда поле заполняется'''
    for i in range(w):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(w)] for i in range(h)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(fps)