import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("География Алтайского края")

background = pygame.image.load('../img/alt ktay.png').convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

# Шрифты
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Словарь городов с их координатами-прямоугольниками (x1, y1, x2, y2)
# и позициями для названий на карте
cities = {
    "Барнаул": {
        "rect": (300, 200, 400, 250),  # x1, y1, x2, y2
        "label_pos": (350, 180)
    },
    "Бийск": {
        "rect": (500, 300, 580, 340),
        "label_pos": (540, 280)
    },
    "Рубцовск": {
        "rect": (200, 400, 280, 440),
        "label_pos": (240, 380)
    },
    "Заринск": {
        "rect": (450, 150, 520, 190),
        "label_pos": (485, 130)
    },
    "Славгород": {
        "rect": (100, 300, 180, 340),
        "label_pos": (140, 280)
    }
}


class Game:
    def __init__(self):
        self.score = 0
        self.round_num = 0
        self.current_city = None
        self.rounds = list(cities.keys())
        random.shuffle(self.rounds)
        self.message = ""
        self.message_timer = 0
        self.next_round()

    def next_round(self):
        """Переход к следующему раунду"""
        if self.round_num < 5:
            self.current_city = self.rounds[self.round_num]
            self.round_num += 1
            self.message = f"Найди: {self.current_city}"
            self.message_timer = 180  # Показывать сообщение 3 секунды (60 FPS * 3)
        else:
            self.current_city = None
            self.message = f"Игра окончена! Счет: {self.score}/5"

    def check_click(self, pos):
        """Проверка клика мыши"""
        if self.current_city is None:
            return

        x, y = pos
        city_data = cities[self.current_city]
        x1, y1, x2, y2 = city_data["rect"]

        # Проверяем, попадает ли клик в прямоугольник города
        if x1 <= x <= x2 and y1 <= y <= y2:
            self.score += 1
            self.message = "Правильно! +1 очко"
            self.next_round()
        else:
            self.message = "Неправильно. Попробуй еще раз"
            self.message_timer = 120

    def draw_map(self):
        """Рисование схематической карты"""
        # Фон
        screen.blit(background, (0, 0))

        # Рисуем границы "Алтайского края" (большой прямоугольник)
        pygame.draw.rect(screen, BLACK, (10, 10, 1580, 880), 3)

        # Рисуем реку Обь (синяя линия)
        pygame.draw.line(screen, BLUE, (250, 80), (600, 450), 5)

        # Рисуем города (прямоугольники)
        for city_name, city_data in cities.items():
            x1, y1, x2, y2 = city_data["rect"]
            # Рисуем прямоугольник города
            rect_width = x2 - x1
            rect_height = y2 - y1
            rect = pygame.Rect(x1, y1, rect_width, rect_height)

            # Если это текущий город для поиска, выделяем его
            if city_name == self.current_city:
                pygame.draw.rect(screen, YELLOW, rect)
                pygame.draw.rect(screen, RED, rect, 3)
            else:
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)

            # Рисуем название города
            text = font_small.render(city_name, True, BLACK)
            screen.blit(text, city_data["label_pos"])

        # Рисуем счет
        score_text = font_medium.render(f"Счет: {self.score}/5", True, BLUE)
        screen.blit(score_text, (10, 10))

        # Рисуем номер раунда
        if self.round_num <= 5:
            round_text = font_medium.render(f"Раунд: {self.round_num}/5", True, BLUE)
            screen.blit(round_text, (10, 50))

        # Рисуем сообщение
        if self.message_timer > 0:
            # Затемняем фон под сообщением
            s = pygame.Surface((400, 60))
            s.set_alpha(200)
            s.fill(WHITE)
            screen.blit(s, (200, 100))

            msg_text = font_large.render(self.message, True, RED)
            text_rect = msg_text.get_rect(center=(SCREEN_WIDTH // 2, 130))
            screen.blit(msg_text, text_rect)
            self.message_timer -= 1


def main():
    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    game.check_click(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.round_num > 5:  # Нажми R для рестарта
                    game = Game()

        # Отрисовка
        game.draw_map()
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()