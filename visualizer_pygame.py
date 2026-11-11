"""
Visualizador Interativo do K-Way Merge Sort em Pygame.
Apresenta em tempo real a divisão em K partições coloridas e a intercalação (merge).
"""

import sys
import os
import random
import pygame
from typing import List, Optional
from k_way_mergesort import k_way_mergesort_visual, AnimationStep

# Cores da interface (Paleta Moderna Dark)
BG_COLOR = (15, 23, 42)          # Slate escuro
CARD_BG = (30, 41, 59)           # Slate médio
CARD_BORDER = (51, 65, 85)       # Borda sutil
TEXT_PRIMARY = (248, 250, 252)   # Branco brilhante
TEXT_SECONDARY = (148, 163, 184) # Cinza claro
TEXT_MUTED = (100, 116, 139)     # Cinza escuro
ACCENT_BLUE = (59, 130, 246)     # Azul destaque
HIGHLIGHT_YELLOW = (250, 204, 21)# Amarelo destaque (comparação)
SORTED_GREEN = (34, 197, 94)     # Verde ordenado final
DEFAULT_BAR_COLOR = (71, 85, 105)# Barras inativas/neutras

# Paleta vibrante para até 8 partições distintas
PARTITION_COLORS = [
    (16, 185, 129),  # 1: Esmeralda
    (14, 165, 233),  # 2: Azul celeste
    (245, 158, 11),  # 3: Âmbar
    (168, 85, 247),  # 4: Roxo
    (244, 63, 94),   # 5: Rosa / Carmesim
    (6, 182, 212),   # 6: Ciano
    (132, 204, 22),  # 7: Lima
    (99, 102, 241),  # 8: Índigo
]


class PygameVisualizer:
    def __init__(self, width: int = 1050, height: int = 680, n: int = 48, k: int = 4):
        self.width = width
        self.height = height
        self.n = n
        self.k = k

        # Configurações de execução
        self.fps = 40
        self.paused = False
        self.step_mode = False
        self.done = False

        # Inicializa Pygame
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("K-Way Merge Sort Visualizer")
        self.clock = pygame.time.Clock()

        # Fontes
        self.font_title = pygame.font.SysFont("DejaVu Sans, Arial, Helvetica", 22, bold=True)
        self.font_hud = pygame.font.SysFont("DejaVu Sans, Arial, Helvetica", 14, bold=True)
        self.font_body = pygame.font.SysFont("DejaVu Sans, Arial, Helvetica", 13)
        self.font_small = pygame.font.SysFont("DejaVu Sans, Arial, Helvetica", 11)

        # Estado dos dados
        self.reset_array()

    def reset_array(self):
        """Gera um novo vetor aleatório e reinicia o gerador."""
        self.arr = [random.randint(10, 100) for _ in range(self.n)]
        self.generator = k_way_mergesort_visual(self.arr, self.k)
        self.current_step = AnimationStep(
            arr=list(self.arr),
            start=0,
            end=self.n,
            phase="READY",
            description="Pressione [ESPAÇO] para iniciar ou pausar a animação."
        )
        self.done = False

    def next_step(self):
        """Avança um passo no gerador."""
        if not self.done:
            try:
                self.current_step = next(self.generator)
                if self.current_step.phase == "DONE":
                    self.done = True
            except StopIteration:
                self.done = True

    def draw_hud(self):
        """Desenha a barra superior com métricas e status."""
        hud_rect = pygame.Rect(20, 15, self.width - 40, 95)
        pygame.draw.rect(self.screen, CARD_BG, hud_rect, border_radius=12)
        pygame.draw.rect(self.screen, CARD_BORDER, hud_rect, width=1, border_radius=12)

        # Título
        title_surf = self.font_title.render("K-WAY MERGE SORT VISUALIZER", True, TEXT_PRIMARY)
        self.screen.blit(title_surf, (35, 25))

        sub_surf = self.font_small.render("Divisão e Conquista com K Partições Simultâneas", True, ACCENT_BLUE)
        self.screen.blit(sub_surf, (35, 52))

        # Status textual do passo atual
        desc = self.current_step.description
        if self.paused and not self.done:
            desc = "[PAUSADO] " + desc
        desc_surf = self.font_body.render(desc, True, HIGHLIGHT_YELLOW if "Menor" in desc else TEXT_SECONDARY)
        self.screen.blit(desc_surf, (35, 75))

        # Badges de métricas à direita
        stats = self.current_step.stats
        badges = [
            ("N (Elementos)", str(self.n)),
            ("K (Partições)", str(self.k)),
            ("Comparações", str(stats.comparisons)),
            ("Movimentações", str(stats.moves)),
            ("Merges", str(stats.merges)),
            ("Velocidade", f"{self.fps} FPS"),
        ]

        badge_x = self.width - 45 - (len(badges) * 98)
        for label, val in badges:
            b_rect = pygame.Rect(badge_x, 28, 90, 68)
            pygame.draw.rect(self.screen, (20, 27, 45), b_rect, border_radius=8)
            pygame.draw.rect(self.screen, CARD_BORDER, b_rect, width=1, border_radius=8)

            lbl_surf = self.font_small.render(label, True, TEXT_MUTED)
            self.screen.blit(lbl_surf, (badge_x + 6, 35))

            val_surf = self.font_hud.render(val, True, TEXT_PRIMARY)
            self.screen.blit(val_surf, (badge_x + 6, 58))

            badge_x += 98

    def draw_bars(self):
        """Renderiza o gráfico de barras representando o vetor."""
        render_rect = pygame.Rect(20, 125, self.width - 40, self.height - 240)
        pygame.draw.rect(self.screen, CARD_BG, render_rect, border_radius=12)
        pygame.draw.rect(self.screen, CARD_BORDER, render_rect, width=1, border_radius=12)

        arr = self.current_step.arr
        n = len(arr)
        max_val = max(arr) if arr else 100

        area_x = render_rect.x + 20
        area_y = render_rect.y + 20
        area_w = render_rect.width - 40
        area_h = render_rect.height - 40

        bar_slot_w = area_w / n
        bar_w = max(2, bar_slot_w - (2 if bar_slot_w > 5 else 0))

        start = self.current_step.start
        end = self.current_step.end
        partitions = self.current_step.partitions
        selected_idx = self.current_step.selected_idx
        is_done = (self.current_step.phase == "DONE")

        for idx, val in enumerate(arr):
            bx = area_x + (idx * bar_slot_w)
            bh = int((val / max_val) * (area_h - 20))
            by = area_y + area_h - bh

            # Determina cor da barra
            if is_done:
                color = SORTED_GREEN
            elif idx == selected_idx:
                color = HIGHLIGHT_YELLOW
            elif start <= idx < end and partitions:
                # Determina a qual partição ativa o índice pertence
                part_idx = -1
                for p_i, (p_start, p_end) in enumerate(partitions):
                    if p_start <= idx < p_end:
                        part_idx = p_i
                        break
                
                if part_idx != -1:
                    color = PARTITION_COLORS[part_idx % len(PARTITION_COLORS)]
                else:
                    color = DEFAULT_BAR_COLOR
            elif start <= idx < end:
                color = ACCENT_BLUE
            else:
                color = DEFAULT_BAR_COLOR

            bar_rect = pygame.Rect(int(bx), int(by), int(bar_w), int(bh))
            pygame.draw.rect(self.screen, color, bar_rect, border_radius=3 if bar_w >= 6 else 0)

            # Rótulo de valor sobre a barra se houver espaço suficiente
            if bar_w >= 22:
                txt = self.font_small.render(str(val), True, TEXT_MUTED if color == DEFAULT_BAR_COLOR else TEXT_PRIMARY)
                self.screen.blit(txt, (int(bx + (bar_w - txt.get_width()) / 2), int(by - 16)))

    def draw_footer(self):
        """Desenha a legenda de partições e controles no rodapé."""
        footer_rect = pygame.Rect(20, self.height - 100, self.width - 40, 85)
        pygame.draw.rect(self.screen, CARD_BG, footer_rect, border_radius=12)
        pygame.draw.rect(self.screen, CARD_BORDER, footer_rect, width=1, border_radius=12)

        # Legenda das K Partições
        leg_title = self.font_hud.render("Partições Ativas:", True, TEXT_SECONDARY)
        self.screen.blit(leg_title, (35, self.height - 88))

        partitions = self.current_step.partitions
        active_k = len(partitions) if partitions else self.k

        leg_x = 160
        for p_i in range(min(active_k, len(PARTITION_COLORS))):
            color = PARTITION_COLORS[p_i % len(PARTITION_COLORS)]
            bullet_rect = pygame.Rect(leg_x, self.height - 85, 12, 12)
            pygame.draw.rect(self.screen, color, bullet_rect, border_radius=3)

            lbl = f"P{p_i + 1}"
            if partitions and p_i < len(partitions):
                lbl += f" [{partitions[p_i][0]}:{partitions[p_i][1]}]"

            lbl_surf = self.font_small.render(lbl, True, TEXT_PRIMARY)
            self.screen.blit(lbl_surf, (leg_x + 18, self.height - 87))
            leg_x += lbl_surf.get_width() + 32

        # Atalhos de Teclado
        keys = [
            "[ESPAÇO] Pausar/Play",
            "[→] Passo",
            "[R] Reset",
            "[K] Mudar K",
            "[N] Mudar N",
            "[↑/↓] Velocidade",
            "[S] Salvar Imagem"
        ]
        controls_text = "  |  ".join(keys)
        ctrl_surf = self.font_small.render(controls_text, True, TEXT_MUTED)
        self.screen.blit(ctrl_surf, (35, self.height - 45))

    def render(self):
        """Renderiza um quadro completo."""
        self.screen.fill(BG_COLOR)
        self.draw_hud()
        self.draw_bars()
        self.draw_footer()
        pygame.display.flip()

    def run(self):
        """Loop principal interativo."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_RIGHT:
                        self.paused = True
                        self.next_step()
                    elif event.key == pygame.K_r:
                        self.reset_array()
                    elif event.key == pygame.K_UP:
                        self.fps = min(120, self.fps + 10)
                    elif event.key == pygame.K_DOWN:
                        self.fps = max(5, self.fps - 10)
                    elif event.key == pygame.K_k:
                        # Cicla k entre [2, 3, 4, 5, 8]
                        options = [2, 3, 4, 5, 8]
                        idx = options.index(self.k) if self.k in options else 0
                        self.k = options[(idx + 1) % len(options)]
                        self.reset_array()
                    elif event.key == pygame.K_n:
                        # Cicla n entre [24, 48, 80, 120]
                        options = [24, 48, 80, 120]
                        idx = options.index(self.n) if self.n in options else 1
                        self.n = options[(idx + 1) % len(options)]
                        self.reset_array()
                    elif event.key == pygame.K_s:
                        filename = f"screenshot_k{self.k}_n{self.n}.png"
                        pygame.image.save(self.screen, filename)
                        print(f"Screenshot salvo em {filename}")

            if not self.paused and not self.done:
                self.next_step()

            self.render()
            self.clock.tick(self.fps)

        pygame.quit()


def generate_headless_screenshot(output_path: str, n: int = 40, k: int = 4, target_step_ratio: float = 0.5):
    """
    Gera um screenshot em modo headless (sem necessidade de servidor X/Wayland ativo)
    para ser utilizado no README.md.
    """
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    visualizer = PygameVisualizer(width=1050, height=650, n=n, k=k)

    # Executa até uma etapa interessante de merge
    total_steps = 0
    all_steps = []
    # Cria uma lista de passos
    temp_gen = k_way_mergesort_visual(list(visualizer.arr), k=k)
    for s in temp_gen:
        all_steps.append(s)

    target_idx = int(len(all_steps) * target_step_ratio)
    target_idx = min(len(all_steps) - 1, max(0, target_idx))
    visualizer.current_step = all_steps[target_idx]

    visualizer.render()
    pygame.image.save(visualizer.screen, output_path)
    print(f"Screenshot gerado com sucesso: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--screenshot":
        output = sys.argv[2] if len(sys.argv) > 2 else "assets/pygame_preview.png"
        generate_headless_screenshot(output, n=42, k=4, target_step_ratio=0.55)
    else:
        app = PygameVisualizer(width=1050, height=680, n=48, k=4)
        app.run()
