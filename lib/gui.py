from lib.base import *

pygame.font.init()


class Textbox:
    def __init__(self, speaker, text, duration, font_size):
        self.speaker = speaker  # The character who is speaking
        self.text = text
        self.duration = duration  # The amount of time the textbox should remain fully visible
        self.font_size = font_size
        self.pos = [240, 720]
        self.time_visible = 0  # The time at which the textbox became fully visible
        self.fully_visible = False  # Flag to confirm when the textbox is fully visible
        self.sprite = pygame.image.load("assets/sprites/textbox.png")
        self.font = pygame.font.SysFont("courier", font_size)
        self.finished = False  # If the textbox is done displaying

        self.text = self.text.split(" ")  # This part of the constructor renders the text to the textbox with text wrapping
        self.text.append(" ")
        line_width = 0
        num_lines = 0
        if self.speaker is not None:
            self.font.set_bold(True)
            self.font.set_italic(True)
            self.sprite.blit(self.font.render(speaker, True, (0, 0, 0)), (15, 5))
            self.font.set_bold(False)
            self.font.set_italic(False)
            num_lines += 1
        for i, word in enumerate(self.text):
            word_image = self.font.render(word, True, (50, 50, 50))
            self.sprite.blit(word_image, (15 + line_width, (num_lines * self.font.get_linesize()) + 5))
            line_width += word_image.get_width() + self.font.size(" ")[0]
            if not word == self.text[-1]:
                if line_width + self.font.size(self.text[i + 1])[0] > 760:
                    line_width = 0
                    num_lines += 1

    def adjust_pos(self):  # Should be called every frame
        if not self.finished:
            if not self.fully_visible:
                if self.pos[1] > 420:
                    self.pos[1] -= 5
                else:
                    self.time_visible = pygame.time.get_ticks()
                    self.fully_visible = True
            if pygame.time.get_ticks() - self.time_visible > self.duration and self.fully_visible:
                if self.pos[1] < 720:
                    self.pos[1] += 5
                else:
                    self.finished = True


def render_health(health, display):
    healthbar_text.set_colorkey((255, 255, 255))  # Renders health GUI
    heart_empty.set_colorkey((255, 255, 255))
    heart_full.set_colorkey((255, 255, 255))
    display.blit(healthbar_text, (-5, 0))
    for i in range(3):
        display.blit(heart_empty, (i * 80 + 25, 50))
    for i in range(health):
        display.blit(heart_full, (i * 80 + 25, 50))
