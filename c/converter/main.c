#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32
#define SCREEN_BUFFER_SIZE (SCREEN_WIDTH * SCREEN_HEIGHT / 8)


void create_valid_variable_name(const char *input, char *output)
{
    // Remove a extensão e caracteres inválidos
    int i = 0, j = 0;
    while (input[i] != '\0' && input[i] != '.')
    {
        if (isalnum(input[i]) || input[i] == '_')
        {
            output[j++] = tolower(input[i]);
        }
        else
        {
            output[j++] = '_';
        }
        i++;
    }
    output[j] = '\0';
}


void generate_header_file(const char *filename, uint8_t *buffer, int width, int height)
{
    char var_name[256];
    char header_name[256];

    create_valid_variable_name(filename, var_name);


    snprintf(header_name, sizeof(header_name), "%s_H", var_name);
    for (int i = 0; header_name[i]; i++)
    {
        header_name[i] = toupper(header_name[i]);
    }

    // Calcula tamanho do buffer em bytes
    int buffer_size = (width * height + 7) / 8;


    char header_filename[256];
    snprintf(header_filename, sizeof(header_filename), "%s.h", var_name);
    FILE *file = fopen(header_filename, "w");
    if (!file)
    {
        printf("Erro ao criar arquivo header!\n");
        return;
    }


    fprintf(file, "#ifndef %s\n", header_name);
    fprintf(file, "#define %s\n\n", header_name);
    fprintf(file, "#include <stdint.h>\n\n");
    fprintf(file, "// Imagem: %s\n", filename);
    fprintf(file, "// Dimensões: %dx%d pixels\n", width, height);
    fprintf(file, "// Tamanho do buffer: %d bytes\n\n", buffer_size);

  
    fprintf(file, "#define %s_WIDTH %d\n", var_name, width);
    fprintf(file, "#define %s_HEIGHT %d\n\n", var_name, height);

    fprintf(file, "const uint8_t %s_data[%d] = {\n    ", var_name, buffer_size);

    for (int i = 0; i < buffer_size; i++)
    {
        fprintf(file, "0x%02X", buffer[i]);
        if (i < buffer_size - 1)
        {
            fprintf(file, ", ");
            if ((i + 1) % 12 == 0)
            { // Break line em 12 numer ?? por testar
                fprintf(file, "\n    ");
            }
        }
    }

    fprintf(file, "\n};\n\n#endif // %s\n", header_name);
    fclose(file);

    printf("Arquivo header gerado: %s\n", header_filename);
}


void print_buffer(uint8_t *buffer, int width, int height)
{
    printf("Buffer visual (%dx%d):\n", width, height);


    printf("   ");
    for (int x = 0; x < width; x += 10)
    {
        printf("%-10d", x);
    }
    printf("\n   ");
    for (int x = 0; x < width; x++)
    {
        printf("%d", x % 10);
    }
    printf("\n");


    for (int y = 0; y < height; y++)
    {
        printf("%2d ", y); 
        for (int x = 0; x < width; x++)
        {
            int byte_idx = (y * width + x) / 8;
            int bit_idx = 7 - ((y * width + x) % 8);
            int pixel = (buffer[byte_idx] >> bit_idx) & 0x01;
            printf("%c", pixel ? '#' : '.');
        }
        printf("\n");
    }
}

uint8_t *load_bmp_to_buffer(const char *filename, int *width, int *height)
{
    if (SDL_Init(SDL_INIT_VIDEO) < 0)
    {
        printf("SDL não pode inicializar! SDL_Error: %s\n", SDL_GetError());
        return NULL;
    }

    SDL_Surface *surface = SDL_LoadBMP(filename);
    if (surface == NULL)
    {
        printf("Não foi possível carregar a imagem %s! SDL_Error: %s\n", filename, SDL_GetError());
        SDL_Quit();
        return NULL;
    }

    *width = surface->w;
    *height = surface->h;

    uint8_t *buffer = (uint8_t *)malloc((*width * *height + 7) / 8);
    if (buffer == NULL)
    {
        SDL_FreeSurface(surface);
        SDL_Quit();
        return NULL;
    }
    memset(buffer, 0, (*width * *height + 7) / 8);

    SDL_LockSurface(surface);
    uint8_t *pixels = (uint8_t *)surface->pixels;
    int pitch = surface->pitch;

    for (int y = 0; y < *height; y++)
    {
        for (int x = 0; x < *width; x++)
        {
            uint8_t r = pixels[y * pitch + x * surface->format->BytesPerPixel];
            uint8_t g = pixels[y * pitch + x * surface->format->BytesPerPixel + 1];
            uint8_t b = pixels[y * pitch + x * surface->format->BytesPerPixel + 2];

            uint8_t gray = (r + g + b) / 3;

            int byte_idx = (y * *width + x) / 8;
            int bit_idx = 7 - ((y * *width + x) % 8);

            if (gray > 127)
            {
                buffer[byte_idx] |= (1 << bit_idx);
            }
        }
    }

    SDL_UnlockSurface(surface);
    SDL_FreeSurface(surface);
    SDL_Quit();

    return buffer;
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Uso: %s <arquivo.bmp>\n", argv[0]);
        return 1;
    }

    int width, height;
    uint8_t *image_buffer = load_bmp_to_buffer(argv[1], &width, &height);

    if (image_buffer == NULL)
    {
        printf("Erro ao carregar a imagem!\n");
        return 1;
    }


    print_buffer(image_buffer, width, height);

    generate_header_file(argv[1], image_buffer, width, height);

    free(image_buffer);
    return 0;
}