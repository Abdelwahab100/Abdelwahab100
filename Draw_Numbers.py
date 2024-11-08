import pygame
import numpy as np

class HandwritingRecognition:
    def __init__(self):
      
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.window_size = (28*10, 28*10)  
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('Draw numbers')

        self.drawing = False
        self.last_pos = None
        self.line_thickness = 2  
        self.pixel_size = 10  

        self.image_matrix = np.zeros((28, 28), dtype=np.uint8)

    def change_brightness(self, color, amount):
        return tuple(min(max(c - amount, 0), 255) for c in color)

    def draw_line_with_gradient(self, x1, y1, x2, y2, thickness, gradient_amount):
        dx, dy = x2 - x1, y2 - y1
        steps = max(abs(dx), abs(dy))
        for i in range(1, steps + 1):
            x = int(x1 + i * dx / steps)
            y = int(y1 + i * dy / steps)
            for j in range(-thickness // 2, (thickness + 1) // 2):
                for k in range(-thickness // 2, (thickness + 1) // 2):
                    px = x + j
                    py = y + k
                    if 0 <= px < 28 and 0 <= py < 28:
                        self.image_matrix[py][px] = 255 
                        self.screen.set_at((px * self.pixel_size, py * self.pixel_size),
                                          self.change_brightness(self.screen.get_at((px * self.pixel_size, py * self.pixel_size)),
                                                            gradient_amount))

    def draw(self):
        pygame.init()
        self.screen.fill(self.BLACK)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.drawing = True
                    self.last_pos = event.pos
                elif event.type == pygame.MOUSEMOTION and self.drawing:
                    current_pos = event.pos
                    brightness_amount = 25  
                    self.draw_line_with_gradient(self.last_pos[0] // self.pixel_size, self.last_pos[1] // self.pixel_size,
                                                current_pos[0] // self.pixel_size, current_pos[1] // self.pixel_size,
                                                self.line_thickness, brightness_amount)
                    self.last_pos = current_pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.drawing = False

            for y in range(28):
                for x in range(28):
                    color = (self.image_matrix[y][x], self.image_matrix[y][x], self.image_matrix[y][x])
                    pygame.draw.rect(self.screen, color, pygame.Rect(x * self.pixel_size, y * self.pixel_size, self.pixel_size, self.pixel_size))

            pygame.display.flip()

if __name__ == "__main__":
    handwriting_recognition = HandwritingRecognition()
    handwriting_recognition.draw()
    print(handwriting_recognition.image_matrix)
       