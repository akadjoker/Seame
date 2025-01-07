class ClusterTheme:
    def __init__(self,
                 # Caminhos de imagens
                 background_path: str,
                 
                 # Posições dos elementos principais (x, y)
                 speed_center: tuple,
                 rpm_center: tuple,
                 battery_position: tuple,
                 temp_position: tuple,
                 
                 # Dimensões e ângulos dos mostradores
                 speed_radius: int,
                 rpm_radius: int,
                 speed_angle_range: tuple,  # (min_angle, max_angle)
                 rpm_angle_range: tuple,    # (min_angle, max_angle)
                 
                 # Cores principais
                 primary_color: str,
                 warning_color: str,
                 danger_color: str,
                 text_color: str,
                 
                 # Fontes e tamanhos
                 primary_font: str,
                 primary_font_size: int,
                 secondary_font_size: int,
                 
                 # Limites e ranges
                 speed_range: tuple = (0, 220),  # (min, max)
                 rpm_range: tuple = (0, 8000),
                 temp_range: tuple = (50, 130),
                 
                 # Opcional - elementos extras
                 extra_elements: dict = None):
        
        # Atributos obrigatórios
        self.background_path = background_path
        self.speed_center = speed_center
        self.rpm_center = rpm_center
        self.battery_position = battery_position
        self.temp_position = temp_position
        
        self.speed_radius = speed_radius
        self.rpm_radius = rpm_radius
        self.speed_angle_range = speed_angle_range
        self.rpm_angle_range = rpm_angle_range
        
        self.primary_color = primary_color
        self.warning_color = warning_color
        self.danger_color = danger_color
        self.text_color = text_color
        
        self.primary_font = primary_font
        self.primary_font_size = primary_font_size
        self.secondary_font_size = secondary_font_size
        
        self.speed_range = speed_range
        self.rpm_range = rpm_range
        self.temp_range = temp_range
        
        # Elementos extras opcionais (posições de indicadores adicionais, etc)
        self.extra_elements = extra_elements or {}

# Exemplo de uso:
modern_theme = ClusterTheme(
    background_path="themes/modern/bg.png",
    speed_center=(300, 240),
    rpm_center=(700, 240),
    battery_position=(100, 400),
    temp_position=(900, 400),
    speed_radius=150,
    rpm_radius=150,
    speed_angle_range=(-140, 140),
    rpm_angle_range=(-140, 140),
    primary_color="#00FF00",
    warning_color="#FFFF00",
    danger_color="#FF0000",
    text_color="#FFFFFF",
    primary_font="Arial",
    primary_font_size=24,
    secondary_font_size=18,
    extra_elements={
        "gear_position": (500, 300),
        "fuel_gauge": (150, 350)
    }
)