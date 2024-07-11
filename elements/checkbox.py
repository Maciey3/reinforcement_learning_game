import pygame


class Checkbox:
    def __init__(self, surface, x, y, idnum, color=(255, 255, 255), caption="",
    outline_color=(0, 0, 0),
                 check_color=(0, 0, 0), font_size=24, font_color=(0, 0, 0),
    text_offset=(28, 1), font='Arial'):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.ft = font

        #identification for removal and reorginazation
        self.idnum = idnum

        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 20, 20)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = False

    def _draw_button_text(self):
        self.font = pygame.font.SysFont(self.ft, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + 16 / 2 - h / 2 +
        self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 10, self.y + 10), 7)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True
            print(str(self.caption)+' toggle '+str(self.checked))

    def update_checkbox(self):
        # if event_object.type == pygame.MOUSEBUTTONDOWN:
        #     self.click = True
        self._update()
        return self.checked