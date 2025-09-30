import pygame
import math
import time

# Configurações básicas
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GRAY = (200, 200, 200)

# Comprimento dos segmentos do braço
L1 = 150
L2 = 100

# Inicializa o Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Braço Robótico 2D")
font = pygame.font.Font(None, 24)

# Sliders e valores iniciais
angle1 = 90
angle2 = 180
entry_x = 0
entry_y = 0
slider_values = [entry_x, entry_y]
slider_labels = [ "Entry X:", "Entry Y:"]
slider_ranges = [700, 700]  # Define o intervalo máximo dos sliders
slider_rects = [pygame.Rect(10, HEIGHT - 160 + i * 40, 200, 20) for i in range(len(slider_labels))]
slider_knobs = [pygame.Rect(10 + int((slider_values[i] / slider_ranges[i]) * 200), HEIGHT - 160 + i * 40, 10, 20) for i in range(len(slider_labels))]
selected_slider = None

running = True
while running:
    screen.fill(WHITE)
    
    # Posição do primeiro segmento
    base_x, base_y = WIDTH // 2, HEIGHT // 2

    # Desenha o plano cartesiano
    pygame.draw.circle(screen,RED,(base_x,base_y),L1+L2,1)
    pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 1)
    pygame.draw.line(screen, BLACK, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1)
    
    
    
    desired_x = slider_values[slider_labels.index("Entry X:")] -200
    desired_y = slider_values[slider_labels.index("Entry Y:")] -200

    # mouse_x, mouse_y = pygame.mouse.get_pos()
    # desired_x = mouse_x - WIDTH // 2
    # desired_y = HEIGHT // 2 - mouse_y

    if math.hypot(desired_x,desired_y) < L1 + L2:

        beta = math.atan2(desired_y,desired_x+1e-10)
        phi = math.acos( (math.sqrt( math.pow(desired_x,2) + math.pow(desired_y,2) )/2)/L1 )
        alpha = phi + beta

        theta =  2*phi + math.radians(180)



        angle1 = alpha
        angle2 = theta

        angle1 = -angle1 
        angle2 = angle2 - math.radians(180) 
        
        
        joint1_x = base_x + L1 * math.cos(angle1)
        joint1_y = base_y + L1 * math.sin(angle1)
        joint2_x = joint1_x + L2 * math.cos(angle1 + angle2)
        joint2_y = joint1_y + L2 * math.sin(angle1 + angle2)
        
        # Desenha o braço
        pygame.draw.line(screen, BLACK, (base_x, base_y), (joint1_x, joint1_y), 5)
        pygame.draw.line(screen, RED, (joint1_x, joint1_y), (joint2_x, joint2_y), 5)
        pygame.draw.circle(screen, BLUE, (int(joint1_x), int(joint1_y)), 6)
        pygame.draw.circle(screen, BLUE, (int(joint2_x), int(joint2_y)), 6)
        
        # Exibe coordenadas
        coord_text = font.render(f"End Effector: ({int(joint2_x - WIDTH // 2)}, {int(HEIGHT // 2 - joint2_y)})", True, BLACK)
        # screen.blit(coord_text, (10, 10))
        pygame.draw.line(screen, BLACK, (round(int(joint2_x)),0), (round(int(joint2_x)),HEIGHT), 1)
        pygame.draw.line(screen, BLACK, (0,round(int(joint2_y))), (WIDTH,round(int(joint2_y))), 1)
        
        desired_text = font.render(f"Desired: ({desired_x +200};{desired_y + 200})", True, BLACK)
        screen.blit(desired_text, (10, 30))

        J1angle_text = font.render(f"J1angle: ({math.degrees(angle1)})", True, BLACK)
        screen.blit(J1angle_text, (10, 50))
        J2angle_text = font.render(f"J2angle: ({math.degrees(angle2)})", True, BLACK)
        screen.blit(J2angle_text, (10, 70))
    else:

        error_text = font.render(f"Out of envelope", True, RED)
        if math.hypot(desired_x,desired_y)>L1+L2:
            screen.blit(error_text, (10, 100))
    
    # Processa eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, knob in enumerate(slider_knobs):
                if knob.collidepoint(event.pos):
                    selected_slider = i
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_slider = None
        elif event.type == pygame.MOUSEMOTION and selected_slider is not None:
            x = max(slider_rects[selected_slider].x, min(event.pos[0], slider_rects[selected_slider].x + 200))
            slider_knobs[selected_slider].x = x
            slider_values[selected_slider] = ((x - slider_rects[selected_slider].x) / 200) * slider_ranges[selected_slider]
            # slider_values[2] -= 350
    
    # Desenha sliders
    for i in range(len(slider_labels)):
        pygame.draw.rect(screen, GRAY, slider_rects[i])
        pygame.draw.rect(screen, RED, slider_knobs[i])
        txt_surface = font.render(f"{slider_labels[i]} {int(slider_values[i])}", True, BLACK)
        screen.blit(txt_surface, (slider_rects[i].x + 220, slider_rects[i].y))
    
    
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()