#!/usr/bin/python

import pygame

class Background:
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]

    def generate(self, color):
        surface = pygame.Surface((self.width, self.height))
        surface.fill(color)
        return surface
