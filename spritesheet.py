import pygame


def extract_images(filename, pos_offsets):
    sheet = pygame.image.load('images/' + filename)
    result = []
    for rect in pos_offsets:
        select = pygame.Rect(rect)
        image = pygame.Surface(select.size).convert(pygame.display.get_surface())
        image.blit(sheet, (0, 0), select)
        result.append(image)
    return result
