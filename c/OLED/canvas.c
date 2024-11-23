#include "canvas.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define DISPLAY_WIDTH 128
#define DISPLAY_HEIGHT 32
#define SCALE_FACTOR 4


//style
// 0x30 = 00110000  │  ··██····
// 0x78 = 01111000  │  ·████···
// 0xCC = 11001100  │  ██··██··
// 0xCC = 11001100  │  ██··██··
// 0xFC = 11111100  │  ██████··
// 0xCC = 11001100  │  ██··██··
// 0xCC = 11001100  │  ██··██··
// 0x00 = 00000000  │  ········

static const uint8_t FONT_8X8[][8] = {
    //'0':
    {0x7C, 0xC6, 0xCE, 0xDE, 0xF6, 0xE6, 0x7C, 0x00},
    //'1':
    {0x30, 0x70, 0x30, 0x30, 0x30, 0x30, 0xFC, 0x00},
    //'2':
    {0x78, 0xCC, 0x0C, 0x38, 0x60, 0xCC, 0xFC, 0x00},
    //'3':
    {0x78, 0xCC, 0x0C, 0x38, 0x0C, 0xCC, 0x78, 0x00},
    //'4':
    {0x1C, 0x3C, 0x6C, 0xCC, 0xFE, 0x0C, 0x1E, 0x00},
    //'5':
    {0xFC, 0xC0, 0xF8, 0x0C, 0x0C, 0xCC, 0x78, 0x00},
    //'6':
    {0x38, 0x60, 0xC0, 0xF8, 0xCC, 0xCC, 0x78, 0x00},
    //'7':
    {0xFC, 0xCC, 0x0C, 0x18, 0x30, 0x30, 0x30, 0x00},
    //'8':
    {0x78, 0xCC, 0xCC, 0x78, 0xCC, 0xCC, 0x78, 0x00},
    //'9':
    {0x78, 0xCC, 0xCC, 0x7C, 0x0C, 0x18, 0x70, 0x00},
    //'A':
    {0x30, 0x78, 0xCC, 0xCC, 0xFC, 0xCC, 0xCC, 0x00},
    //'B':
    {0xFC, 0x66, 0x66, 0x7C, 0x66, 0x66, 0xFC, 0x00},
    //'C':
    {0x3C, 0x66, 0xC0, 0xC0, 0xC0, 0x66, 0x3C, 0x00},
    //'D':
    {0xF8, 0x6C, 0x66, 0x66, 0x66, 0x6C, 0xF8, 0x00},
    //'E':
    {0xFE, 0x62, 0x68, 0x78, 0x68, 0x62, 0xFE, 0x00},
    //'F':
    {0xFE, 0x62, 0x68, 0x78, 0x68, 0x60, 0xF0, 0x00},
    //'G':
    {0x3C, 0x66, 0xC0, 0xC0, 0xCE, 0x66, 0x3E, 0x00},
    //'H':
    {0xCC, 0xCC, 0xCC, 0xFC, 0xCC, 0xCC, 0xCC, 0x00},
    //'I':
    {0x78, 0x30, 0x30, 0x30, 0x30, 0x30, 0x78, 0x00},
    //'J':
    {0x1E, 0x0C, 0x0C, 0x0C, 0xCC, 0xCC, 0x78, 0x00},
    //'K':
    {0xE6, 0x66, 0x6C, 0x78, 0x6C, 0x66, 0xE6, 0x00},
    //'L':
    {0xF0, 0x60, 0x60, 0x60, 0x62, 0x66, 0xFE, 0x00},
    //'M':
    {0xC6, 0xEE, 0xFE, 0xD6, 0xC6, 0xC6, 0xC6, 0x00},
    //'N':
    {0xC6, 0xE6, 0xF6, 0xDE, 0xCE, 0xC6, 0xC6, 0x00},
    //'O':
    {0x38, 0x6C, 0xC6, 0xC6, 0xC6, 0x6C, 0x38, 0x00},
    //'P':
    {0xFC, 0x66, 0x66, 0x7C, 0x60, 0x60, 0xF0, 0x00},
    //'Q':
    {0x78, 0xCC, 0xCC, 0xCC, 0xDC, 0x78, 0x1C, 0x00},
    //'R':
    {0xFC, 0x66, 0x66, 0x7C, 0x6C, 0x66, 0xE6, 0x00},
    //'S':
    {0x78, 0xCC, 0x60, 0x30, 0x18, 0xCC, 0x78, 0x00},
    //'T':
    {0xFC, 0xB4, 0x30, 0x30, 0x30, 0x30, 0x78, 0x00},
    //'U':
    {0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0x78, 0x00},
    //'V':
    {0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0x78, 0x30, 0x00},
    //'W':
    {0xC6, 0xC6, 0xC6, 0xD6, 0xFE, 0xEE, 0xC6, 0x00},
    //'X':
    {0xC6, 0xC6, 0x6C, 0x38, 0x6C, 0xC6, 0xC6, 0x00},
    //'Y':
    {0xCC, 0xCC, 0xCC, 0x78, 0x30, 0x30, 0x78, 0x00},
    //'Z':
    {0xFC, 0xCC, 0x98, 0x30, 0x64, 0xCC, 0xFC, 0x00},
    //' ':
    {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00},
    //'.':
    {0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x30, 0x00},
    //',':
    {0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x30, 0x20},
    //'!':
    {0x30, 0x30, 0x30, 0x30, 0x30, 0x00, 0x30, 0x00},
    //'?':
    {0x78, 0xCC, 0x0C, 0x18, 0x30, 0x00, 0x30, 0x00},
    //':':
    {0x00, 0x30, 0x30, 0x00, 0x00, 0x30, 0x30, 0x00},
    //'-':
    {0x00, 0x00, 0x00, 0x7C, 0x00, 0x00, 0x00, 0x00},
};

Canvas *canvas_init(void)
{
    Canvas *display = (Canvas *)malloc(sizeof(Canvas));
    if (!display)
        return NULL;

    if (SDL_Init(SDL_INIT_VIDEO) < 0)
    {
        free(display);
        return NULL;
    }

    display->window = SDL_CreateWindow("SSD1306 OLED Simulator Team06 SEA:ME",
                                       SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
                                       DISPLAY_WIDTH * SCALE_FACTOR, DISPLAY_HEIGHT * SCALE_FACTOR,
                                       SDL_WINDOW_SHOWN);

    if (!display->window)
    {
        free(display);
        SDL_Quit();
        return NULL;
    }

    display->renderer = SDL_CreateRenderer(display->window, -1,
                                           SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);

    if (!display->renderer)
    {
        SDL_DestroyWindow(display->window);
        free(display);
        SDL_Quit();
        return NULL;
    }

    SDL_SetRenderDrawColor(display->renderer, 0, 0, 0, 255);
    SDL_RenderClear(display->renderer);

    memset(display->buffer, 0, sizeof(display->buffer));
    display->running = true;

    return display;
}

void canvas_cleanup(Canvas *display)
{
    if (display)
    {
        if (display->renderer)
            SDL_DestroyRenderer(display->renderer);
        if (display->window)
            SDL_DestroyWindow(display->window);
        free(display);
    }
    SDL_Quit();
}

void canvas_clear(Canvas *display)
{
    memset(display->buffer, 0, sizeof(display->buffer));
}

void canvas_pixel(Canvas *display, int x, int y)
{
    if (x >= 0 && x < DISPLAY_WIDTH && y >= 0 && y < DISPLAY_HEIGHT)
    {
        display->buffer[y][x] = 1;
    }
}

void canvas_line(Canvas *display, int x0, int y0, int x1, int y1)
{
    int dx = abs(x1 - x0);
    int dy = abs(y1 - y0);
    int steep = dy > dx;

    if (steep)
    {
        int temp = x0;
        x0 = y0;
        y0 = temp;
        temp = x1;
        x1 = y1;
        y1 = temp;
    }

    if (x0 > x1)
    {
        int temp = x0;
        x0 = x1;
        x1 = temp;
        temp = y0;
        y0 = y1;
        y1 = temp;
    }

    dx = x1 - x0;
    dy = abs(y1 - y0);
    int error = dx / 2;
    int ystep = (y0 < y1) ? 1 : -1;
    int y = y0;

    for (int x = x0; x <= x1; x++)
    {
        if (steep)
        {
            canvas_pixel(display, y, x);
        }
        else
        {
            canvas_pixel(display, x, y);
        }

        error -= dy;
        if (error < 0)
        {
            y += ystep;
            error += dx;
        }
    }
}

void canvas_rect(Canvas *display, int x, int y, int width, int height, bool fill)
{
    if (width < 0)
    {
        x += width;
        width = -width;
    }
    if (height < 0)
    {
        y += height;
        height = -height;
    }

    if (fill)
    {
        for (int i = x; i < x + width; i++)
        {
            for (int j = y; j < y + height; j++)
            {
                canvas_pixel(display, i, j);
            }
        }
    }
    else
    {

        for (int i = x; i < x + width; i++)
        {
            canvas_pixel(display, i, y);
            canvas_pixel(display, i, y + height - 1);
        }

        for (int i = y; i < y + height; i++)
        {
            canvas_pixel(display, x, i);
            canvas_pixel(display, x + width - 1, i);
        }
    }
}

void canvas_circle(Canvas *display, int x_center, int y_center, int radius, bool fill)
{
    int x = radius;
    int y = 0;
    int error = -radius;

    while (x >= y)
    {
        if (fill)
        {
            for (int i = -x; i <= x; i++)
            {
                canvas_pixel(display, x_center + i, y_center + y);
                canvas_pixel(display, x_center + i, y_center - y);
            }
            for (int i = -y; i <= y; i++)
            {
                canvas_pixel(display, x_center + i, y_center + x);
                canvas_pixel(display, x_center + i, y_center - x);
            }
        }
        else
        {
            canvas_pixel(display, x_center + x, y_center + y);
            canvas_pixel(display, x_center + y, y_center + x);
            canvas_pixel(display, x_center - y, y_center + x);
            canvas_pixel(display, x_center - x, y_center + y);
            canvas_pixel(display, x_center - x, y_center - y);
            canvas_pixel(display, x_center - y, y_center - x);
            canvas_pixel(display, x_center + y, y_center - x);
            canvas_pixel(display, x_center + x, y_center - y);
        }

        error += 2 * y + 1;
        y++;
        if (error >= 0)
        {
            error += 2 * (1 - x);
            x--;
        }
    }
} 

void canvas_char(Canvas *canvas, int x, int y, char c, int scale)
{
  
    c = toupper(c);


    int char_index = 0;

   
    if (c >= '0' && c <= '9')
    {
        char_index = c - '0';
    }

    else if (c >= 'A' && c <= 'Z')
    {
        char_index = 10 + (c - 'A'); // 10 é o offset após os números
    }
    // char especiais
    else if (c == ' ')
        char_index = 36;
    else if (c == '.')
        char_index = 37;
    else if (c == ',')
        char_index = 38;
    else if (c == '!')
        char_index = 39;
    else if (c == '?')
        char_index = 40;
    else if (c == ':')
        char_index = 41;
    else if (c == '-')
        char_index = 42;
    else
        return; // char não suportado


    for (int row = 0; row < 8; row++)
    {
        uint8_t line = FONT_8X8[char_index][row];
        for (int col = 0; col < 8; col++)
        {
            if (line & (1 << (7 - col)))
            {
                for (int sy = 0; sy < scale; sy++)
                {
                    for (int sx = 0; sx < scale; sx++)
                    {
                        canvas_pixel(canvas,
                                     x + col * scale + sx,
                                     y + row * scale + sy);
                    }
                }
            }
        }
    }
}

void canvas_text(Canvas *canvas, int x, int y, const char *text, int scale)
{
    int cursor_x = x;
    int cursor_y = y;
    int char_spacing = 8 * scale; 

    while (*text)
    {
        if (cursor_x + 8 * scale > CANVAS_WIDTH)
        {
            cursor_x = x;
            cursor_y += 8 * scale;
        }
        if (cursor_y + 8 * scale > CANVAS_HEIGHT)
            break;

        canvas_char(canvas, cursor_x, cursor_y, *text, scale);
        cursor_x += char_spacing;
        text++;
    }
}

void canvas_update(Canvas *display)
{
    SDL_SetRenderDrawColor(display->renderer, 0, 0, 0, 255);
    SDL_RenderClear(display->renderer);

    SDL_SetRenderDrawColor(display->renderer, 255, 255, 255, 255);

    for (int y = 0; y < DISPLAY_HEIGHT; y++)
    {
        for (int x = 0; x < DISPLAY_WIDTH; x++)
        {
            if (display->buffer[y][x])
            {
                SDL_Rect rect = {
                    x * SCALE_FACTOR,
                    y * SCALE_FACTOR,
                    SCALE_FACTOR,
                    SCALE_FACTOR};
                SDL_RenderFillRect(display->renderer, &rect);
            }
        }
    }

    SDL_RenderPresent(display->renderer);
}

bool canvas_is_running(Canvas *display)
{
    SDL_Event event;
    while (SDL_PollEvent(&event))
    {
        if (event.type == SDL_QUIT)
        {
            display->running = false;
        }
    }
    return display->running;
}