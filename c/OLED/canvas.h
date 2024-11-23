
#pragma once

#include <SDL2/SDL.h>
#include <stdint.h>
#include <stdbool.h>

#define CANVAS_WIDTH 128
#define CANVAS_HEIGHT 32
#define CANVAS_SCALE 4

typedef struct
{
    SDL_Window *window;
    SDL_Renderer *renderer;
    uint8_t buffer[CANVAS_HEIGHT][CANVAS_WIDTH];
    bool running;
} Canvas;


Canvas *canvas_init(void);
void canvas_clear(Canvas *canvas);
void canvas_update(Canvas *canvas);
bool canvas_is_running(Canvas *canvas);
void canvas_cleanup(Canvas *canvas);


void canvas_pixel(Canvas *canvas, int x, int y);
void canvas_line(Canvas *canvas, int x1, int y1, int x2, int y2);
void canvas_rect(Canvas *canvas, int x, int y, int w, int h, bool fill);
void canvas_circle(Canvas *canvas, int x, int y, int r, bool fill);


void canvas_char(Canvas *canvas, int x, int y, char c, int scale);
void canvas_text(Canvas *canvas, int x, int y, const char *text, int scale);
