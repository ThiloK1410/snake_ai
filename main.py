import pygame
from numpy import array
from snake import Snake


class App:
    # main function from where everything is called
    def __init__(self):
        # initiating a clock and setting timer of the application
        self.clock = pygame.time.Clock()
        self.fps = 5
        self.time_per_frame = 1000 / self.fps

        self._running = True
        self.display = None

        size = array([500, 500])

        self.grid_dim = array([10, 10])
        self.cell_size = min((size - (size % self.grid_dim)) / self.grid_dim)
        self.size = self.grid_dim * self.cell_size
        self.grid_size = (int(self.size[0] / self.grid_dim[0]), int(self.size[1] / self.grid_dim[1]))

        self.snakes = []

    # called once to start program
    def on_init(self):
        pygame.init()
        self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        self.snakes.append(Snake(self.grid_dim, self.grid_dim / 2, 1))

        self.on_execute()

    # handles player inputs
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if len(self.snakes) >= 1:
                if event.key == pygame.K_SPACE:
                    self.snakes[0].grow()
                if event.key == pygame.K_RIGHT:
                    self.snakes[0].change_dir(1)
                if event.key == pygame.K_DOWN:
                    self.snakes[0].change_dir(2)
                if event.key == pygame.K_LEFT:
                    self.snakes[0].change_dir(3)
                if event.key == pygame.K_UP:
                    self.snakes[0].change_dir(0)

    # loop which will be executed at fixed rate (for physics, animations and such)
    def on_loop(self):
        for snake in self.snakes:
            snake.move()

    # loop which will only be called when enough cpu time is available
    def on_render(self):
        self.display.fill((0, 0, 0))

        for snake in self.snakes:
            self.draw_snake_foods(snake)
            self.draw_snake(snake)

        self.draw_grid()

        pygame.display.update()

    @staticmethod
    def on_cleanup():
        pygame.quit()

    def on_execute(self):
        previous = pygame.time.get_ticks()
        lag = 0.0

        # advanced game loop to call on_loop() at fixed rate and on_render() as fast as possible
        # (kinda overkill right now) (also not relevant)
        while self._running:
            current = pygame.time.get_ticks()
            elapsed = current - previous
            lag += elapsed
            previous = current

            for event in pygame.event.get():
                self.on_event(event)

            while lag > self.time_per_frame:
                self.on_loop()
                lag -= self.time_per_frame
            self.on_render()
        self.on_cleanup()

    def draw_grid(self):
        for i in range(self.grid_dim[0]):
            pygame.draw.line(self.display, (255, 255, 255), (i * self.cell_size, 0), (i * self.cell_size, self.size[1]))
        for i in range(self.grid_dim[1]):
            pygame.draw.line(self.display, (255, 255, 255), (0, i * self.cell_size), (self.size[0], i * self.cell_size))

    def draw_snake(self, snake):
        positions = snake.get_segment_positions()
        color = (34, 139, 34)
        if snake.dead:
            color = (255, 0, 0)
        for pos in positions:
            rect = pygame.Rect(pos * self.cell_size, array([self.cell_size, self.cell_size]))
            pygame.draw.rect(self.display, color, rect)

    def draw_snake_foods(self, snake):
        positions = snake.get_food_positions()
        color = (255, 255, 0)
        for pos in positions:
            rect = pygame.Rect(pos * self.cell_size, array([self.cell_size, self.cell_size]))
            pygame.draw.rect(self.display, color, rect)


if __name__ == "__main__":
    app = App()
    app.on_init()
