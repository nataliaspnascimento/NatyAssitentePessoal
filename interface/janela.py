import tkinter as tk
import math
import random
import time


class JanelaNaty:
    def __init__(self, root):
        self.root = root
        self.root.title("Naty")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        self.TRANSPARENTE = "#010101"
        self.root.attributes("-transparentcolor", self.TRANSPARENTE)
        self.root.config(bg=self.TRANSPARENTE)

        self.R  = 180 # Modal um pouco menor para facilitar mover
        self.W, self.H = self.R*2, self.R*2
        self.cx, self.cy = self.R, self.R

        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        self.root.geometry(f"{self.W}x{self.H}+{sw - self.W - 30}+{sh - self.H - 70}")

        self.canvas = tk.Canvas(self.root, width=self.W, height=self.H,
                                bg=self.TRANSPARENTE, highlightthickness=0)
        self.canvas.pack()

        # Configuração de arrastar
        self.canvas.bind("<Button-1>", self._iniciar_arrasto)
        self.canvas.bind("<B1-Motion>", self._arrastar)

        # ── Paleta Lilás e Rosa Vibrante ─────
        self.LILAS_FORTE   = "#9370DB"
        self.ROSA_VIBRANTE = "#FF1493"
        self.MAGENTA_NEON  = "#FF00FF"
        self.BRANCO_NEON   = "#FFFFFF"
        self.LAVANDA       = "#E6E6FA"
        self.LINHA_CONEXAO = "#4A2B3D"
        
        self.usuario_atual = "Natalia" # Estado global do usuário
        self.inicializado  = False     # Só libera o loop após a saudação
        self.falando = False
        self.pulso_tamanho = 32
        self.pulso_dir = 1
        self.ids_anim = []
        self.particulas = []
        
        self._gerar_obsidian_nodes()
        # Pequena pausa para garantir que os atributos foram registrados
        self.root.after(10, self._animar)

    def _iniciar_arrasto(self, event):
        self.x_off = event.x
        self.y_off = event.y

    def _arrastar(self, event):
        x = self.root.winfo_x() + (event.x - self.x_off)
        y = self.root.winfo_y() + (event.y - self.y_off)
        self.root.geometry(f"+{x}+{y}")
        # Atualiza base_x/y para a vibração não puxar de volta
        self.base_x, self.base_y = x, y

    def _gerar_obsidian_nodes(self):
        for _ in range(65):
            self.particulas.append({
                "x": random.uniform(50, 310),
                "y": random.uniform(50, 310),
                "vx": random.uniform(-0.5, 0.5),
                "vy": random.uniform(-0.5, 0.5),
                "r": random.uniform(1.5, 3.0),
                "cor": random.choice([self.LILAS_FORTE, self.ROSA_VIBRANTE, self.MAGENTA_NEON])
            })

    def _animar(self):
        cx, cy, R = self.cx, self.cy, self.R
        for idd in self.ids_anim:
            self.canvas.delete(idd)
        self.ids_anim.clear()

        # FUNDO DO MODAL (Estático)
        self.ids_anim.append(self.canvas.create_oval(cx-R, cy-R, cx+R, cy+R, 
                                                     fill="#120A10", outline=self.LILAS_FORTE, width=2))

        # Movimentação das Partículas (Sem vibração)
        for p in self.particulas:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            dx, dy = p["x"] - cx, p["y"] - cy
            d = math.sqrt(dx*dx + dy*dy)
            if d > R - 15:
                p["vx"] *= -1
                p["vy"] *= -1

        # DESENHAR REDE OBSIDIAN
        dist_limite = 65
        for i, p1 in enumerate(self.particulas):
            for p2 in self.particulas[i+1:]:
                dist = math.sqrt((p1["x"]-p2["x"])**2 + (p1["y"]-p2["y"])**2)
                if dist < dist_limite:
                    cor_linha = self.LINHA_CONEXAO
                    self.ids_anim.append(self.canvas.create_line(p1["x"], p1["y"], p2["x"], p2["y"], fill=cor_linha))

        for p in self.particulas:
            self.ids_anim.append(self.canvas.create_oval(p["x"]-p["r"], p["y"]-p["r"], p["x"]+p["r"], p["y"]+p["r"], fill=p["cor"], outline=""))

        # --- NOME NATY COM BATIMENTOS CARDÍACOS ---
        tx, ty = cx, cy
        if self.falando:
            # Batimento cardíaco duplo (lub-dub) mais realista
            t = time.time() * 1.5 # Velocidade dos batimentos
            # Combinação de duas ondas para o efeito de batimento duplo
            batida = math.pow(max(0, math.sin(t * math.pi * 2)), 12) + \
                     0.6 * math.pow(max(0, math.sin(t * math.pi * 2 - 0.5)), 12)
            
            self.pulso_tamanho = 32 + (batida * 16)
        else:
            self.pulso_tamanho = 32

        self.ids_anim.append(self.canvas.create_text(tx, ty, text="NATY", 
                                                     fill=self.BRANCO_NEON, font=("Segoe UI", int(self.pulso_tamanho), "bold")))
        
        status = self.status_atual if hasattr(self, 'status_atual') else "ONLINE"
        self.ids_anim.append(self.canvas.create_text(cx, cy+45, text=status, fill=self.LAVANDA, font=("Segoe UI", 7, "bold")))

        self.root.after(35, self._animar)

    def atualizar_status(self, status):
        self.falando = (status == "Respondendo...")
        self.status_atual = status.upper()

    def atualizar_comando(self, cmd):
        pass
