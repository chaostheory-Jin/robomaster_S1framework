import cv2 as cv
import pygame

__all__ = ['window','init']


def init():
    pygame.init()
    screen = pygame.display.set_mode((720, 420), 0, 32)
    pygame.display.set_caption('try')
    pygame.mouse.set_visible(True)

    return screen


def transform(image, angle, center=None, scale=0.56):
    (h, w) = image.shape[:2]
    if center is None:
        center = (w // 2, h // 2)

    M = cv.getRotationMatrix2D(center, angle, scale)

    rotated = cv.warpAffine(image, M, (w, h))
    rotated = cv.flip(rotated,0)
    rotated = rotated[:,430:850]
    rotated = cv.cvtColor(rotated,cv.COLOR_BGR2RGB)
    return rotated


def window(img,s1,screen):
    img[50:120,50:240,:] = img[50:120,50:240,:]/6
    font = cv.FONT_HERSHEY_COMPLEX
    cv.putText(img,f"{s1.name} HP:{s1.hp}",(60,80),font,1,(0,255,0),3)
    cv.putText(img,f"{s1.name} CAL:{s1.heat}",(60,120),font,1,(0,255,0),3)
    if not s1.debug:
        cv.putText(img,f"BATTERY POWER:{s1.battery}",(400,80),font,1,(0,255,0),3)
    img_show = transform(img, 90)
    pygame.surfarray.blit_array(screen, img_show)
    if s1.debug:
        s1.pos_x += s1.speed_x
        s1.pos_y += s1.speed_y
        s1.screen.blit(s1.pic, (s1.pos_x, s1.pos_y))
