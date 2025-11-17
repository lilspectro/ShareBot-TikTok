"""Gravity-driven stair descent animation using pygame.

This module renders an infinite staircase that slopes downward.
A ball experiences gravity, bounces lightly on each stair, and keeps
rolling forward along the infinite steps.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass

import pygame

# Screen configuration
WIDTH, HEIGHT = 960, 640
BACKGROUND_COLOR = (15, 18, 32)
STAIR_COLOR = (65, 86, 121)
BALL_COLOR = (231, 111, 81)
ACCENT_COLOR = (129, 178, 154)

# Stair configuration
STEP_WIDTH = 160
STEP_HEIGHT = 28
STEP_HORIZONTAL_SPACING = 140
STEP_VERTICAL_DROP = 40

# Physics parameters
GRAVITY = 900.0  # pixels per second^2
BALL_RADIUS = 24
BALL_SPEED_X = 160.0
BOUNCE_DAMPING = 0.35
MIN_BOUNCE_SPEED = 45.0

# Visual tweaks
GRID_SPACING = 80
FPS = 60


@dataclass
class Step:
    """A single rectangular stair step."""

    index: int

    @property
    def x(self) -> float:
        return self.index * STEP_HORIZONTAL_SPACING

    @property
    def y(self) -> float:
        # The staircase endlessly descends by shifting each step down.
        return HEIGHT * 0.35 + self.index * STEP_VERTICAL_DROP

    def rect(self, camera_x: float, camera_y: float) -> pygame.Rect:
        return pygame.Rect(
            int(self.x - camera_x),
            int(self.y - camera_y),
            STEP_WIDTH,
            STEP_HEIGHT,
        )

    def contains_x(self, x: float) -> bool:
        return self.x <= x <= self.x + STEP_WIDTH


class Ball:
    """A simple physics body representing the falling sphere."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.vx = BALL_SPEED_X
        self.vy = 0.0

    def update(self, dt: float, steps: list[Step]) -> None:
        previous_y = self.y

        # Integrate velocity and position.
        self.vy += GRAVITY * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Resolve collisions against any step the ball is crossing.
        if self.vy >= 0:
            for step in steps:
                if not step.contains_x(self.x):
                    continue

                top = step.y
                was_above = previous_y + BALL_RADIUS <= top
                is_overlapping = self.y + BALL_RADIUS >= top

                if was_above and is_overlapping:
                    self.y = top - BALL_RADIUS
                    if self.vy > 0:
                        self.vy = -self.vy * BOUNCE_DAMPING
                        if abs(self.vy) < MIN_BOUNCE_SPEED:
                            self.vy = 0.0
                    break

    def draw(self, surface: pygame.Surface, camera_x: float, camera_y: float) -> None:
        screen_pos = (int(self.x - camera_x), int(self.y - camera_y))
        pygame.draw.circle(surface, BALL_COLOR, screen_pos, BALL_RADIUS)
        # Draw a simple highlight to emphasize the sphere.
        highlight_offset = (-BALL_RADIUS // 2, -BALL_RADIUS // 2)
        highlight_pos = (
            screen_pos[0] + highlight_offset[0],
            screen_pos[1] + highlight_offset[1],
        )
        pygame.draw.circle(surface, ACCENT_COLOR, highlight_pos, BALL_RADIUS // 3)


class StaircaseAnimation:
    """Encapsulates the pygame event loop and rendering logic."""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Gravity Staircase")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # Pre-generate a band of steps around the starting point.
        self.min_index = -12
        self.max_index = 64
        self.steps: list[Step] = []
        for i in range(self.min_index, self.max_index + 1):
            step = Step(i)
            self.steps.append(step)
            if i == 0:
                self.start_step = step

        self.ball = Ball(
            x=self.start_step.x + STEP_WIDTH / 2,
            y=self.start_step.y - BALL_RADIUS,
        )

        # Camera offset follows the ball.
        self.camera_x = 0.0
        self.camera_y = 0.0

    def run(self) -> None:
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self._update(dt)
            self._draw()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def _update(self, dt: float) -> None:
        self.ball.update(dt, self.steps)
        self._update_camera()
        self._update_steps()

    def _update_camera(self) -> None:
        target_x = self.ball.x - WIDTH * 0.3
        target_y = self.ball.y - HEIGHT * 0.45
        smoothing = 0.15

        self.camera_x += (target_x - self.camera_x) * smoothing
        self.camera_y += (target_y - self.camera_y) * smoothing

    def _update_steps(self) -> None:
        # Remove steps that are far behind the camera to keep the list short.
        while self.steps and self.steps[0].x + STEP_WIDTH < self.camera_x - WIDTH:
            removed = self.steps.pop(0)
            self.min_index = removed.index + 1

        # Add new steps ahead of the camera to maintain the endless staircase.
        while self.steps and self.steps[-1].x < self.camera_x + WIDTH * 2:
            self.max_index += 1
            self.steps.append(Step(self.max_index))

    def _draw_grid(self, surface: pygame.Surface) -> None:
        # Background grid for depth perception.
        start_x = int(self.camera_x // GRID_SPACING * GRID_SPACING - GRID_SPACING * 2)
        end_x = int(self.camera_x + WIDTH + GRID_SPACING * 2)
        start_y = int(self.camera_y // GRID_SPACING * GRID_SPACING - GRID_SPACING * 2)
        end_y = int(self.camera_y + HEIGHT + GRID_SPACING * 2)

        for x in range(start_x, end_x, GRID_SPACING):
            screen_x = int(x - self.camera_x)
            pygame.draw.line(
                surface,
                (24, 32, 48),
                (screen_x, 0),
                (screen_x, HEIGHT),
                1,
            )

        for y in range(start_y, end_y, GRID_SPACING):
            screen_y = int(y - self.camera_y)
            pygame.draw.line(
                surface,
                (24, 32, 48),
                (0, screen_y),
                (WIDTH, screen_y),
                1,
            )

    def _draw(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        self._draw_grid(self.screen)

        # Draw stairs
        for step in self.steps:
            rect = step.rect(self.camera_x, self.camera_y)
            pygame.draw.rect(self.screen, STAIR_COLOR, rect)
            pygame.draw.rect(self.screen, (48, 63, 93), rect, 2)

        self.ball.draw(self.screen, self.camera_x, self.camera_y)
        self._draw_hud()
        pygame.display.flip()

    def _draw_hud(self) -> None:
        font = pygame.font.SysFont("arial", 18)
        text = font.render(
            "Appuyez sur la croix pour quitter", True, (180, 200, 220)
        )
        self.screen.blit(text, (20, 20))


def main() -> None:
    animation = StaircaseAnimation()
    animation.run()


if __name__ == "__main__":
    main()
