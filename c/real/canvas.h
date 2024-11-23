#pragama once
#include <stdint.h>
#include <stdbool.h>

#define CANVAS_WIDTH 128
#define CANVAS_HEIGHT 32
#define I2C_ADDRESS 0x3C

typedef struct 
{
    uint8_t buffer[CANVAS_HEIGHT/8][CANVAS_WIDTH];
    int i2c_fd;
} Canvas;

Canvas* canvas_init(void);
void canvas_cleanup(Canvas* canvas);
void canvas_clear(Canvas* canvas);
void canvas_update(Canvas* canvas);

void canvas_pixel(Canvas* canvas, int x, int y);
void canvas_char(Canvas* canvas, int x, int y, char c, int scale);
void canvas_text(Canvas* canvas, int x, int y, const char* text, int scale);

void canvas_line(Canvas* canvas, int x0, int y0, int x1, int y1);
void canvas_rect(Canvas* canvas, int x, int y, int width, int height, bool fill);
void canvas_circle(Canvas* canvas, int x_center, int y_center, int radius, bool fill);
