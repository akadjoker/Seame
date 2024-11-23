int main()
{
    Canvas *canvas = canvas_init();
    if (!canvas)
    {
        fprintf(stderr, "Failed to initialize display\n");
        return 1;
    }


    canvas_clear(canvas);
    canvas_text(canvas, 0, 0, "HELLO!", 2);
    canvas_text(canvas, 0, 20, "RPi Test", 1);
    canvas_update(canvas);


    sleep(5);

    canvas_cleanup(canvas);
    return 0;
}