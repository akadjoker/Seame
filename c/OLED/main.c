#include "canvas.h"
#include <stdio.h>

int main()
{
    Canvas *canvas = canvas_init();
    if (!canvas)
    {
        fprintf(stderr, "Failed to initialize canvas\n");
        return 1;
    }


    canvas_clear(canvas);


    // canvas_rect(canvas, 10, 5, 20, 15, true); 
    // canvas_circle(canvas, 60, 16, 10, false); 
    // canvas_line(canvas, 80, 5, 120, 25);     

    canvas_text(canvas, 10, 0, "Team06!", 2);  // Texto grande
    canvas_text(canvas, 5, 20, "SEA:ME Portugal", 1);  // Texto normal


    // Loop principal
    while (canvas_is_running(canvas))
    {
        canvas_update(canvas);
        SDL_Delay(16); // ~60 FPS
    }

    canvas_cleanup(canvas);
    return 0;
}