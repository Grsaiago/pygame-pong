#!/usr/bin/env python3

from enum import Enum
from typing import List
import pygame

class Colors(Enum):
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)


class PlayerOrientation(Enum):
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4


class Window:
    width = 1000
    height = 600
    def __init__(self, caption: str) -> None:
        self.instance = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(caption)


class Player:
    width = Window.width * 0.01
    height = Window.height * 0.1
    def __init__(self, player_x: float, player_y: float, name: str, orientation: PlayerOrientation) -> None:
        self.name = name
        self.orientation = orientation
        self.color = Colors.RED
        self.rect = pygame.Rect(player_x, player_y, self.width, self.height)
        self.speed = 0

    def set_speed(self, ammount: int) -> None:
        self.speed = ammount


class Ball:
    radius = 15
    INITIAL_X_SPEED = 0.1
    INITIAL_Y_SPEED = 0.1
    def __init__(self, x_pos: float, y_pos: float) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_speed = self.INITIAL_X_SPEED
        self.y_speed = self.INITIAL_Y_SPEED

class Game:
    def __init__(self, window: Window):
        self.should_run = True
        self.window = window
        self.players: List[Player] = []
        self.ball: Ball | None = None

    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def set_ball(self, ball: Ball) -> None:
        self.ball = ball

    def draw_players(self) -> None:
        for player in self.players:
            pygame.draw.rect(self.window.instance, player.color.value, player.rect)
        return 

    def draw_ball(self) -> None:
        assert self.ball is not None
        pygame.draw.circle(self.window.instance, Colors.BLUE.value, (self.ball.x_pos, self.ball.y_pos), radius=Ball.radius)
        return

    def draw_scene(self) -> None:
        self.window.instance.fill(Colors.BLACK.value)
        self.draw_players()
        self.draw_ball()
        pygame.display.update()
        return

    def calculate_players_position(self) -> None:
        for player in self.players:
            player.rect.y += player.speed
        return

    def calculate_ball_position(self) -> None:
        assert self.ball is not None
        # reverter se bater nas partes de cima ou de baixo
        if self.ball.y_pos <= 0 + self.ball.radius or self.ball.y_pos >= self.window.height - self.ball.radius:
            self.ball.y_speed *= -1
        # caso em que a bola bateu nas laterais (pontuou)
        elif self.ball.x_pos >= self.window.width - self.ball.radius \
            or self.ball.x_pos <= 0 + self.ball.radius:
            # resetar a bola pro meio
            self.ball.x_pos = self.window.width/2 - self.ball.radius
            self.ball.y_pos = self.window.height/2 - self.ball.radius
            # resetar a velocidade
            self.ball.x_speed = self.ball.INITIAL_X_SPEED
            self.ball.y_speed = self.ball.INITIAL_Y_SPEED
            # reverter a velocidade pra mudar o 'saque'
            self.ball.x_speed *= -1
            self.ball.y_speed *= -1

        # calcular colisão com os jogadores
        for player in self.players:
            match player.orientation.value:
                case PlayerOrientation.LEFT.value:
                # se a bola está entre o centro e a lateral em largura
                # e se a bola está entre o centro e as laterais em altura
                    if (player.rect.x <= self.ball.x_pos <= player.rect.x + player.rect.width) \
                        and (player.rect.y <= self.ball.y_pos <= player.rect.y + player.rect.height):
                        self.ball.x_pos = player.rect.x + player.width
                        self.ball.x_speed *= -1
                case PlayerOrientation.RIGHT.value:
                    if (player.rect.x <= self.ball.x_pos <= player.rect.x + player.rect.width) \
                        and (player.rect.y <= self.ball.y_pos <= player.rect.y + player.rect.height):
                        self.ball.x_pos = player.rect.x
                        self.ball.x_speed *= -1
                case PlayerOrientation.TOP.value:
                    pass
                case PlayerOrientation.BOTTOM.value:
                    pass

        # movimentação normal da bola
        self.ball.x_pos += self.ball.x_speed
        self.ball.y_pos += self.ball.y_speed

    def calculate_objects_position(self) -> None:
        self.calculate_ball_position()
        self.calculate_players_position()
        return

    def event_loop(self) -> None:
        if len(self.players) < 2:
            print(f"Error: only {len(self.players)} players connected, needs at least 2")
            return
        elif not self.ball:
            print("Error: There is no ball")
            return 
        while self.should_run:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self.should_run = False
                elif i.type == pygame.KEYDOWN:
                    match i.key:
                        case pygame.K_w:
                            self.players[0].set_speed(-1)
                        case pygame.K_s:
                            self.players[0].set_speed(1)
                        case pygame.K_UP:
                            self.players[1].set_speed(-1)
                        case pygame.K_DOWN:
                            self.players[1].set_speed(1)
                        case pygame.K_ESCAPE | pygame.K_q:
                            self.should_run = False

                elif i.type == pygame.KEYUP:
                    match i.key:
                        case pygame.K_w:
                            self.players[0].set_speed(0)
                        case pygame.K_s:
                            self.players[0].set_speed(0)
                        case pygame.K_UP:
                            self.players[1].set_speed(0)
                        case pygame.K_DOWN:
                            self.players[1].set_speed(0)
            self.calculate_objects_position()
            self.draw_scene()


def main():
    pygame.init()

    wn = Window("kinda transcending")
    app = Game(wn)
    app.add_player(Player(Window.width * 0.1, Window.height/2 - Player.height, "gabriel", PlayerOrientation.LEFT))
    app.add_player(Player(Window.width * 0.9, Window.height/2 - Player.height, "iza", PlayerOrientation.RIGHT))
    app.set_ball(Ball(Window.width/2 - Ball.radius, Window.height/2 - Ball.radius))
    
    app.event_loop()
    pygame.quit()

if __name__ == '__main__':
    main()
