import socket
from threading import Thread
import pygame
import sys
from threading import Thread
from tkinter import *

pygame.init()

client = None
NAME = None

def click():
    global client, e_ip, e_name, root, NAME
    SERVER = e_ip.get()
    NAME = e_name.get()
    try:
        PORT = 5050
        SERVER = socket.gethostbyname(socket.gethostname())
        ADDR = (SERVER, PORT)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        client.send(NAME.encode('utf-8'))
        root.destroy()
    except:
        root.destroy()
        sys.exit("Server Error!")


root = Tk()

Label(root, text="IP: ").grid(row=0, column=0)
e_ip = Entry(root, width=50)
e_ip.grid(row=0, column=1)
e_ip.insert(0, '192.168.1.8')

Label(root, text="Name: ").grid(row=1, column=0)
e_name = Entry(root, width=50)
e_name.grid(row=1, column=1)

Button(root, text="Submit", command=click).grid(row=2, column=0)


root.mainloop()



# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (207, 58, 159)

# Fonts
font = pygame.font.SysFont("comicsans", 20)


FPS = 60

WIDTH, HEIGHT = 600, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPS")

clock = pygame.time.Clock()
clock.tick(FPS)

events = None

msgs = list()
i = 0

player_choice = None
selected = False

opp_name = None

dic = {'r': "ROCK", 'p': "PAPER", 's': "SCISSORS"}

def text_objects(text, font, colour, pos):
    global WIN
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.center = pos
    WIN.blit(text_surface, text_rect)

def button(text, x, y, w, h, colour, active_colour, action=None):
    global events
    mouse = pygame.mouse.get_pos()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(WIN, active_colour, (x-4, y-4, w+10, h+10))
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and action is not None:
                action()
            elif event.type == pygame.MOUSEBUTTONUP:
                return True
        

    else:
        pygame.draw.rect(WIN, colour, (x, y, w, h))


    text_objects(text, font, BLACK, ((x + (w // 2)), (y + (h // 2))))
    return False


def quit_game():
    pygame.quit()
    sys.exit()

def recv_msg():
    global client, msgs
    while True:
        msg = client.recv(32).decode('utf-8')
        msgs.append(msg)

def select(s):
    global selected, player_choice
    player_choice = s
    client.send(s.encode('utf-8'))
    selected = True

def main():
    global events, WIN, RED, GREEN, WIDTH, HEIGHT, msgs, i, selected, player_choice, dic, opp_name, NAME
    running = True
    ready = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit_game()
                running = False

        WIN.fill(BLACK)
        if not selected and ready:
            button("Rock", 150, HEIGHT//2, 50, 50, RED, GREEN, lambda : select('r'))
            button("Paper", 300, HEIGHT//2, 50, 50, RED, GREEN, lambda : select('p'))
            button("Scissor", 450, HEIGHT//2, 50, 50, RED, GREEN, lambda : select('s'))
        elif selected and ready:
            text_objects(f"You chose {dic[player_choice]}.", font, GREEN, (150, 300))
            if len(msgs) > i:
                i += 1
                selected = False
                ready = False
            else:
                text_objects(f"Waiting for {opp_name}.", font, RED, (450, 300))
        elif not ready:
            opp = msgs[i-1]
            p = player_choice
            text_objects(f"You chose {dic[player_choice]}.", font, GREEN, (150, 300))
            text_objects(f"{opp_name} chose {dic[opp]}.", font, GREEN, (450, 300))
            if p == opp:
                text_objects("DRAW!", font, RED, (WIDTH//2, HEIGHT//2))
            elif (p == 'r' and opp == 's') or (p == 's' and opp == 'p') or (p == 'p' and opp == 'r'):
                text_objects("You won!", font, GREEN, (WIDTH//2, HEIGHT//2))
            elif (opp == 'r' and p == 's') or (opp == 's' and p == 'p') or (opp == 'p' and p == 'r'):
                text_objects("You lost!", font, RED, (WIDTH//2, HEIGHT//2))
            ready = button("Play again!", 500, 500, 75, 50, RED, GREEN)
            

        pygame.display.update()


def wait():
    global events, WIN, msgs, i, opp_name, NAME, thread
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit_game()
                running = False

        WIN.fill(BLACK)

        text_objects("Waiting for a opponent...", font, RED, (WIDTH//2, HEIGHT//2))

        if len(msgs) > i:
            i += 1
            opp_name = msgs[i-1]
            main()

        pygame.display.update()


thread = Thread(target=recv_msg)
thread.start()
wait()



