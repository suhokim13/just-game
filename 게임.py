import pygame
import random
import sys
import math
import colorsys

# 네온 별 초기화

from pygame import K_ESCAPE, K_SPACE

# 초기화
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 800,600

# 배경 음악 재생

pygame.mixer.music.load("../zero/zero.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(1)




screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
NEON_BLUE = (0, 255, 255)
GRAY = (100, 100, 100)

# 플레이어 설정
player_size = 30
player = pygame.Rect(WIDTH // 2, HEIGHT - player_size - 10, player_size, player_size)
player_speed = 5

# score
score = 0
stage = score//12
k_space = 0

# 점프 설정
is_jumping = False
jump_velocity = 0
GRAVITY = 0.4
JUMP_POWER = -15

# 플레이어 잔상 설정
trail = []
TRAIL_LENGTH = 15

# 발판 설정
platforms = [
    pygame.Rect(100, 500, 200, 10),
    pygame.Rect(400, 400, 150, 10),
    pygame.Rect(250, 300, 180, 10),
    pygame.Rect(600, 200, 120, 10)
]

# 적 설정
enemies = []
enemy_timer = 0
ENEMY_INTERVAL = 900  # 더 자주 등장하도록 간격을 줄임

# 룰 변경 시스템
rule_timer = 0
RULE_INTERVAL = 5000
reverse_controls = False

# 글꼴
font = pygame.font.SysFont(None, 50)
stars = [{'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT),
          'speed': random.uniform(0.5, 2)} for _ in range(120)]

# RGB 컬러 흐름
color_shift = 0.0

# 선 애니메이션 파라미터
lines = [{'x': i * 80, 'offset': random.uniform(0, math.pi)} for i in range(10)]
stars = []
for _ in range(150):
    stars.append({'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT), 'speed': random.uniform(1, 2)})

lines = [{'x': i * 80, 'offset': random.uniform(0, math.pi)} for i in range(10)]
color_shift = 0.0
stars = [{'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT), 'speed': random.uniform(1, 2)} for _ in range(150)]

# 네온 라인 설정
lines = [{'x': i * 80, 'offset': random.uniform(0, math.pi)} for i in range(10)]

# 색상 흐름 변수
blue_shift = 0.0




def show_start_screen():
    screen.fill(BLACK)
    title = font.render("just game", True, NEON_BLUE)
    instructions = font.render("Press any key to start", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 40))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False




show_start_screen()


def spawn_enemy():
    size = random.randint(20, 40)
    x = random.choice([0, WIDTH - size])
    y = random.randint(100, HEIGHT - size - 100)
    speed = random.randint(23, 26)
    direction = 1 if x == 0 else -1
    rect = pygame.Rect(x, y, size, size)
    offset = random.uniform(0, math.pi * 2)
    return {'rect': rect, 'speed': speed, 'dir': direction, 'base_y': y, 'offset': offset, 'trail': []}

def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def change_rule():
    global reverse_controls
    reverse_controls = not reverse_controls


# 게임 루프
running = True
while running:
    dt = clock.tick(60)
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()
    # 룰 변경
    rule_timer += dt
    if rule_timer >= RULE_INTERVAL:
        change_rule()
        rule_timer = 0
    if score > 20:
        speed = random.randint(24, 40)
    if score % 20 == 0:
        ENEMY_INTERVAL -= 1
    if score > 100:
        ENEMY_INTERVAL // 2
    if score > 10:
        GRAVITY = -GRAVITY
        if keys[pygame.K_SPACE] and is_jumping:
            is_jumping = True
            if score > 40:
                JUMP_POWER = +JUMP_POWER

    if score > 30:
        jump_velocity = -JUMP_POWER
    # 이벤트 처리
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 💠 컬러 흐름 배경
    color_shift += 0.001
    r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(color_shift % 1, 1, 0.1)]
    screen.fill((r, g, b))

    # 🌌 파란 계열 RGB 애니메이션 배경
    blue_shift += 0.002 + (score / 5000)
    hue = 0.55 + 0.1 * math.sin(blue_shift * 2)  # HSV에서 파란색 영역 유지
    r, g, b = [int(x * 255) for x in
               colorsys.hsv_to_rgb(hue % 1, 0.6 + min(score / 150, 0.4), 0.1 + min(score / 300, 0.7))]
    screen.fill((r, g, b))  # 화면 채우기

    # ✨ 별 갯수 및 속도 점수 기반 증가
    while len(stars) < 200 + score:
        stars.append({'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT), 'speed': random.uniform(1, 3)})

    for star in stars:
        star['y'] += star['speed'] + (score / 100)
        if star['y'] > HEIGHT:
            star['y'] = 0
            star['x'] = random.randint(0, WIDTH)
        pygame.draw.circle(screen, (0, 255, 255), (int(star['x']), int(star['y'])), 2)

    # ⚡ 점수에 따라 라인 진폭 + 속도 증가
    if score >= 30:
        for line in lines:
            amplitude = 50 + min(score, 100)
            freq = 0.005 + score / 5000
            y = int(HEIGHT // 2 + amplitude * math.sin(pygame.time.get_ticks() * freq + line['offset']))
            pygame.draw.line(screen, (0, 200, 255), (line['x'], 0), (line['x'], y), 2)
    # ⚡ 네온 선 애니메이션
    for line in lines:
        y = int(HEIGHT // 2 + 100 * math.sin(pygame.time.get_ticks() * 0.005 + line['offset']))
        pygame.draw.line(screen, (255, 0, 255), (line['x'], 0), (line['x'], y), 2)



    dx = 0
    if keys[pygame.K_LEFT]: dx -= 1
    if keys[pygame.K_RIGHT]: dx += 1
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        jump_velocity = JUMP_POWER

    if reverse_controls:
        dx = -dx

    player.x += dx * player_speed
    if is_jumping:
        jump_velocity += GRAVITY
        player.y += jump_velocity
    else:
        jump_velocity = 0

    # 충돌 판정: 바닥 또는 발판
    on_platform = False
    for plat in platforms:
        if player.colliderect(plat) and jump_velocity >= 0:
            player.bottom = plat.top
            is_jumping = False
            on_platform = True
            break

    if player.y >= HEIGHT - player_size - 10:
        player.y = HEIGHT - player_size - 10
        is_jumping = False
        on_platform = True

    if not on_platform:
        is_jumping = True

    player.clamp_ip(screen.get_rect())

    # 잔상 업데이트
    trail.append(player.copy())
    if len(trail) > TRAIL_LENGTH:
        trail.pop(0)


    # 적 생성
    enemy_timer += dt
    if enemy_timer >= ENEMY_INTERVAL:
        enemies.append(spawn_enemy())
        enemy_timer = 0
        score += 1


    # 적 이동 및 충돌
    for enemy in enemies:
        enemy['rect'].x += enemy['speed'] * enemy['dir']
        enemy['rect'].y = enemy['base_y'] + int(40 * math.sin(pygame.time.get_ticks() * 0.007 + enemy['offset']))
        pygame.draw.rect(screen, RED, enemy['rect'])
        if player.colliderect(enemy['rect']):
            draw_text("why did you die?", WIDTH // 2 - 90, HEIGHT // 2, RED)
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

        for i, pos in enumerate(enemy['trail']):
            alpha = int(255 * (i + 1) / TRAIL_LENGTH)
            s = pygame.Surface((enemy['rect'].width, enemy['rect'].height), pygame.SRCALPHA)
            s.fill((255, 0, 0, alpha))
            screen.blit(s, pos)

        if player.colliderect(enemy['rect']):
            draw_text("YOU DIED", WIDTH // 2 - 70, HEIGHT // 2, RED)
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()



    # 그리기 - 잔상
    for i, pos in enumerate(trail):
        alpha = int(255 * (i + 1) / TRAIL_LENGTH)
        s = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
        s.fill((0, 255, 255, alpha))
        screen.blit(s, pos)

    # 발판 그리기
    for plat in platforms:
        pygame.draw.rect(screen, WHITE, plat)

    # 플레이어 그리기
    pygame.draw.rect(screen, NEON_BLUE, player)

    font = pygame.font.SysFont(None, 30)
    draw_text("Reverse Controls: " + str(reverse_controls), 260, 20)
    draw_text("Score:" + str(score), 20, 20)
    draw_text("Stage: " + str(stage), 560, 20)



    pygame.display.flip()

pygame.quit()
