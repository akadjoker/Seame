// canvas.c
#include "canvas.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wiringPiI2C.h>
#include <wiringPi.h>
#include <unistd.h>


//style
// 0x30 = 00110000  │  ··██····
// 0x78 = 01111000  │  ·████···
// 0xCC = 11001100  │  ██··██··
// 0xCC = 11001100  │  ██··██··
// 0xFC = 11111100  │  ██████··
// 0xCC = 11001100  │  ██··██··
// 0xCC = 11001100  │  ██··██··
// 0x00 = 00000000  │  ········

static const uint8_t FONT_8X8[][8] = 
{
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

// Comandos do SSD1306
#define SSD1306_COMMAND 0x00
#define SSD1306_DATA 0x40

static void write_command(Canvas *canvas, uint8_t command)
{
    wiringPiI2CWriteReg8(canvas->i2c_fd, SSD1306_COMMAND, command);
}

static void write_data(Canvas *canvas, uint8_t data)
{
    wiringPiI2CWriteReg8(canvas->i2c_fd, SSD1306_DATA, data);
}

Canvas *canvas_init(void)
{
    Canvas *canvas = (Canvas *)malloc(sizeof(Canvas));
    if (!canvas)
        return NULL;

    // Inicializa I2C
    canvas->i2c_fd = wiringPiI2CSetup(I2C_ADDRESS);
    if (canvas->i2c_fd < 0)
    {
        free(canvas);
        return NULL;
    }

    uint8_t init_sequence[] = {
        0xAE,       // display off
        0xD5, 0x80, // set display clock
        0xA8, 0x1F, // set multiplex (HEIGHT-1)
        0xD3, 0x00, // set display offset
        0x40,       // set start line
        0x8D, 0x14, // enable charge pump
        0x20, 0x00, // memory mode horizontal
        0xA1,       // segment remap
        0xC8,       // COM scan direction
        0xDA, 0x02, // COM pins
        0x81, 0x8F, // contrast
        0xD9, 0xF1, // pre-charge period
        0xDB, 0x40, // vcomh deselect level
        0xA4,       // output follows RAM
        0xA6,       // normal display
        0xAF        // display on
    };

    for (size_t i = 0; i < sizeof(init_sequence); i++)
    {
        write_command(canvas, init_sequence[i]);
        usleep(1000); // Pequeno delay entre comandos
    }

    // Limpa o buffer
    memset(canvas->buffer, 0, sizeof(canvas->buffer));

    return canvas;
}

void canvas_cleanup(Canvas *canvas)
{
    if (canvas)
    {
        // Desliga o display
        write_command(canvas, 0xAE);
        free(canvas);
    }
}

void canvas_clear(Canvas *canvas)
{
    memset(canvas->buffer, 0, sizeof(canvas->buffer));
}

void canvas_pixel(Canvas *canvas, int x, int y)
{
    if (x >= 0 && x < CANVAS_WIDTH && y >= 0 && y < CANVAS_HEIGHT)
    {
        uint8_t page = y / 8;
        uint8_t bit = y % 8;
        canvas->buffer[page][x] |= (1 << bit);
    }
}

void canvas_char(Canvas *canvas, int x, int y, char c, int scale)
{

    c = toupper(c);

    int char_index = 0;

    // Números
    if (c >= '0' && c <= '9')
    {
        char_index = c - '0';
    }
    // Letras
    else if (c >= 'A' && c <= 'Z')
    {
        char_index = 10 + (c - 'A');
    }
    // Caracteres especiais
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
        return;

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
                                     y + row * scale + sy, 1);
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
    int char_spacing = 6 * scale;

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

void canvas_update(Canvas *canvas)
{
    // Define a area de atualizacao
    write_command(canvas, 0x20); // endereçamento horizontal
    write_command(canvas, 0x00);

    write_command(canvas, 0x21); //  coluna
    write_command(canvas, 0);
    write_command(canvas, CANVAS_WIDTH - 1);

    write_command(canvas, 0x22); //  pagina
    write_command(canvas, 0);
    write_command(canvas, CANVAS_HEIGHT / 8 - 1);

    for (int page = 0; page < CANVAS_HEIGHT / 8; page++)
    {
        for (int col = 0; col < CANVAS_WIDTH; col++)
        {
            write_data(canvas, canvas->buffer[page][col]);
        }
    }
}

void canvas_line(Canvas *canvas, int x0, int y0, int x1, int y1)
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
            canvas_pixel(canvas, y, x);
        }
        else
        {
            canvas_pixel(canvas, x, y);
        }

        error -= dy;
        if (error < 0)
        {
            y += ystep;
            error += dx;
        }
    }
}

void canvas_rect(Canvas *canvas, int x, int y, int width, int height, bool fill)
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


    if (x < 0)
    {
        width += x;
        x = 0;
    }
    if (y < 0)
    {
        height += y;
        y = 0;
    }
    if (x + width > CANVAS_WIDTH)
    {
        width = CANVAS_WIDTH - x;
    }
    if (y + height > CANVAS_HEIGHT)
    {
        height = CANVAS_HEIGHT - y;
    }


    if (width <= 0 || height <= 0)
        return;

    if (fill)
    {
       
        int start_page = y / 8;
        int end_page = (y + height - 1) / 8;

        for (int page = start_page; page <= end_page; page++)
        {
            uint8_t mask = 0xFF;

   
            if (page == start_page)
            {
                mask &= 0xFF << (y % 8);
            }

   
            if (page == end_page)
            {
                mask &= 0xFF >> (7 - ((y + height - 1) % 8));
            }

            for (int col = x; col < x + width; col++)
            {
                canvas->buffer[page][col] |= mask;
            }
        }
    }
    else
    {

        for (int i = x; i < x + width; i++)
        {
            canvas_pixel(canvas, i, y);
            canvas_pixel(canvas, i, y + height - 1);
        }

        for (int i = y; i < y + height; i++)
        {
            canvas_pixel(canvas, x, i);
            canvas_pixel(canvas, x + width - 1, i);
        }
    }
}

void canvas_circle(Canvas *canvas, int x_center, int y_center, int radius, bool fill)
{
    int x = radius;
    int y = 0;
    int err = 0;

    while (x >= y)
    {
        if (fill)
        {
 
            for (int i = -x; i <= x; i++)
            {
                canvas_pixel(canvas, x_center + i, y_center + y);
                canvas_pixel(canvas, x_center + i, y_center - y);
            }
            for (int i = -y; i <= y; i++)
            {
                canvas_pixel(canvas, x_center + i, y_center + x);
                canvas_pixel(canvas, x_center + i, y_center - x);
            }
        }
        else
        {

            canvas_pixel(canvas, x_center + x, y_center + y);
            canvas_pixel(canvas, x_center + y, y_center + x);
            canvas_pixel(canvas, x_center - y, y_center + x);
            canvas_pixel(canvas, x_center - x, y_center + y);
            canvas_pixel(canvas, x_center - x, y_center - y);
            canvas_pixel(canvas, x_center - y, y_center - x);
            canvas_pixel(canvas, x_center + y, y_center - x);
            canvas_pixel(canvas, x_center + x, y_center - y);
        }

        y++;
        err += 1 + 2 * y;
        if (2 * (err - x) + 1 > 0)
        {
            x--;
            err += 1 - 2 * x;
        }
    }
}