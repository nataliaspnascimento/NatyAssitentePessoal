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

        self.R  = 210
        self.W  = self.R * 2
        self.H  = self.R * 2
        self.cx = self.R
        self.cy = self.R

        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        self.root.geometry(f"{self.W}x{self.H}+{sw - self.W - 30}+{sh - self.H - 60}")

        self.canvas = tk.Canvas(self.root, width=self.W, height=self.H,
                                bg=self.TRANSPARENTE, highlightthickness=0)
        self.canvas.pack()

        # ── Paleta Rose Gold Premium ─────────────────────────────
        self.ROSA_PEROLADO = "#FFE4EE"   # Rosa pérola (brilho central)
        self.ROSA_MEDIO    = "#FF8FAB"   # Rosa médio
        self.ROSA_FORTE    = "#FF3D70"   # Rosa vibrante
        self.MAGENTA       = "#D63384"   # Magenta profundo
        self.PURPURA       = "#7B2D8B"   # Púrpura (borda)
        self.DOURADO       = "#FFD700"   # Dourado puro
        self.CREME         = "#FFF5E6"   # Creme quente
        self.BORDA_ESC     = "#2D0B3E"   # Borda muito escura

        self.falando   = False
        self.pulso     = 0.0
        self.pulso_dir = 1
        self.ids_anim  = []
        self._drag_x   = 0
        self._drag_y   = 0

        self._gerar_particulas()
        self._desenhar_base()
        self._criar_textos()
        self._animar()

        self.canvas.bind("<Button-1>",  self._drag_start)
        self.canvas.bind("<B1-Motion>", self._drag_move)

    # ─────────────────────────────────────────────────────────────
    # BASE GRADIENTE (desenhado UMA VEZ — permanente)
    # ─────────────────────────────────────────────────────────────

    def _desenhar_base(self):
        cx, cy, R = self.cx, self.cy, self.R

        # Gradiente radial: escuro nas bordas → rose gold luminoso no centro
        camadas = [
            (R,        "#0f0118"),   # Borda ultra-escura
            (R - 12,   "#1e0230"),   # Roxo profundo
            (R - 28,   "#3d0857"),   # Roxo médio
            (R - 46,   "#6b1577"),   # Púrpura
            (R - 66,   "#9d1f8b"),   # Magenta escuro
            (R - 88,   "#cc2f8e"),   # Magenta
            (R - 108,  "#e8507a"),   # Rosa forte
            (R - 128,  "#f07090"),   # Rosa médio
            (R - 148,  "#f8a0b8"),   # Rosa claro
            (R - 166,  "#fcd0e0"),   # Rosa pérola
            (R - 180,  "#fff0f5"),   # Quase branco rosado
            (R - 190,  "#ffffff"),   # Branco puro no núcleo
        ]
        for r, cor in camadas:
            if r > 0:
                self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                        fill=cor, outline="")

        # Anel decorativo interno (linha sutil)
        self.canvas.create_oval(cx - (R-5), cy - (R-5),
                                cx + (R-5), cy + (R-5),
                                outline="#3d0857", width=2)

        # Marcações douradas (tipo mostrador de relógio)
        for i in range(60):
            ang = math.radians(i * 6)
            r_ext = R - 8
            r_int = R - 16 if i % 5 == 0 else R - 13
            cor   = self.DOURADO if i % 5 == 0 else "#cc2f8e"
            lw    = 2 if i % 5 == 0 else 1
            x1 = cx + r_int * math.sin(ang)
            y1 = cy - r_int * math.cos(ang)
            x2 = cx + r_ext * math.sin(ang)
            y2 = cy - r_ext * math.cos(ang)
            self.canvas.create_line(x1, y1, x2, y2, fill=cor, width=lw)

    def _criar_textos(self):
        cx, cy = self.cx, self.cy

        # Sombra suave do nome (logo abaixo do centro)
        self.canvas.create_text(cx + 1, cy - 12 + 2, text="Naty",
                                fill="#8B0044",
                                font=("Segoe UI Semibold", 30, "bold"))

        # Nome principal — branco sobre o gradiente, bem visível
        self.nome_text = self.canvas.create_text(
            cx, cy - 12, text="Naty",
            fill="#FFFFFF",
            font=("Segoe UI Semibold", 30, "bold"))

        # Linha separadora decorativa
        self.canvas.create_line(cx - 55, cy + 20, cx + 55, cy + 20,
                                fill=self.DOURADO, width=1)

        # Status
        self.status_text = self.canvas.create_text(
            cx, cy + 36, text="AGUARDANDO",
            fill=self.CREME,
            font=("Segoe UI", 8, "bold"))

        # Comando capturado
        self.cmd_text = self.canvas.create_text(
            cx, cy + 54, text="",
            fill="#f8a0b8",
            font=("Segoe UI Light", 7), width=310)

    # ─────────────────────────────────────────────────────────────
    # PARTÍCULAS
    # ─────────────────────────────────────────────────────────────

    def _gerar_particulas(self):
        cx, cy, R = self.cx, self.cy, self.R
        self.particulas = []
        cores = [
            self.ROSA_FORTE, self.ROSA_MEDIO, self.MAGENTA,
            self.DOURADO, self.CREME, "#FF6EAA", "#FFB3CC"
        ]
        for _ in range(85):
            ang = random.uniform(0, 2 * math.pi)
            r   = random.uniform(10, R - 25)
            x   = cx + r * math.cos(ang)
            y   = cy + r * math.sin(ang)
            # Cada partícula tem um ângulo de movimento que deriva suavemente
            ang_mov = random.uniform(0, 2 * math.pi)
            spd     = random.uniform(0.4, 1.2)  # Velocidade base sempre positiva
            self.particulas.append({
                "x":   x,   "y":   y,
                "ox":  x,   "oy":  y,
                "ang": ang_mov,        # Ângulo atual de movimento
                "spd": spd,            # Velocidade base
                "d_ang": random.uniform(-0.03, 0.03),  # Deriva do ângulo (wander)
                "r":   random.uniform(1.5, 4.5),
                "cor": random.choice(cores)
            })

    # ─────────────────────────────────────────────────────────────
    # ANIMAÇÃO
    # ─────────────────────────────────────────────────────────────

    def _animar(self):
        cx, cy, R = self.cx, self.cy, self.R

        for idd in self.ids_anim:
            self.canvas.delete(idd)
        self.ids_anim.clear()

        # Velocidade e dist de conexão variam com o estado mas sempre animado
        multiplicador = 2.2 if self.falando else 1.0
        dist_conn     = 90  if self.falando else 65

        # Move partículas com wandering (deriva orgânica contínua)
        for p in self.particulas:
            # Deriva o ângulo suavemente a cada frame
            p["ang"] += p["d_ang"]
            # Pequena perturbação aleatória (torna o movimento imprevisível e vivo)
            p["d_ang"] += random.uniform(-0.005, 0.005)
            p["d_ang"]  = max(-0.06, min(0.06, p["d_ang"]))  # Limita a deriva

            # Velocidade real = base * multiplicador
            vel = p["spd"] * multiplicador
            p["x"] += math.cos(p["ang"]) * vel
            p["y"] += math.sin(p["ang"]) * vel

            # Elasticidade MUITO suave (apenas para não sair da esfera)
            dx = p["x"] - cx
            dy = p["y"] - cy
            d  = math.sqrt(dx*dx + dy*dy)
            limite = R - 22

            if d > limite:
                # Ao bater na borda, inverte suavemente a direção de volta ao centro
                p["ang"] = math.atan2(-dy, -dx) + random.uniform(-0.5, 0.5)
                f = limite / d
                p["x"] = cx + dx * f
                p["y"] = cy + dy * f

        # Conexões
        for i, a in enumerate(self.particulas):
            for b in self.particulas[i + 1:]:
                dx = a["x"] - b["x"]
                dy = a["y"] - b["y"]
                d  = math.sqrt(dx*dx + dy*dy)
                if d < dist_conn:
                    ratio = 1 - d / dist_conn
                    if self.falando:
                        cor = self.ROSA_FORTE if ratio > 0.5 else self.MAGENTA
                    else:
                        cor = "#7B2D8B" if ratio > 0.6 else "#3d0857"
                    idd = self.canvas.create_line(
                        a["x"], a["y"], b["x"], b["y"],
                        fill=cor, width=1)
                    self.ids_anim.append(idd)

        # Nós das partículas
        for p in self.particulas:
            r = p["r"] * (random.uniform(0.85, 1.35) if self.falando else 1.0)
            idd = self.canvas.create_oval(
                p["x"] - r, p["y"] - r,
                p["x"] + r, p["y"] + r,
                fill=p["cor"], outline="")
            self.ids_anim.append(idd)

        # Anel pulsante ao falar
        self.pulso += 0.06 * self.pulso_dir * (2.5 if self.falando else 0.4)
        if self.pulso >= 1.0: self.pulso_dir = -1
        if self.pulso <= 0.0: self.pulso_dir =  1

        if self.falando:
            for extra, cor_anel, lw in [(int(self.pulso * 16), self.ROSA_FORTE, 2),
                                         (int(self.pulso * 8),  self.DOURADO, 1)]:
                rp = R - 6 + extra
                idd = self.canvas.create_oval(
                    cx - rp, cy - rp, cx + rp, cy + rp,
                    outline=cor_anel, width=lw)
                self.ids_anim.append(idd)

        # Mantém textos no topo
        for item in (self.nome_text, self.status_text, self.cmd_text):
            self.canvas.lift(item)

        # Nome pisca entre branco e dourado ao falar
        if self.falando:
            cor_nome = self.DOURADO if int(time.time() * 3) % 2 == 0 else self.CREME
        else:
            cor_nome = "#FFFFFF"
        self.canvas.itemconfig(self.nome_text, fill=cor_nome)

        self.root.after(40, self._animar)

    # ─────────────────────────────────────────────────────────────
    # INTERFACE PÚBLICA
    # ─────────────────────────────────────────────────────────────

    def atualizar_status(self, status):
        cores = {
            "Aguardando...":  self.CREME,
            "Ouvindo...":     "#FFFFFF",
            "Processando...": self.DOURADO,
            "Respondendo...": self.ROSA_PEROLADO,
        }
        self.falando = (status == "Respondendo...")
        self.canvas.itemconfig(self.status_text,
                               text=status.upper(),
                               fill=cores.get(status, self.CREME))

    def atualizar_comando(self, cmd):
        txt = cmd[:65] + "..." if len(cmd) > 65 else cmd
        self.canvas.itemconfig(self.cmd_text, text=txt)

    def _drag_start(self, e):
        self._drag_x, self._drag_y = e.x, e.y

    def _drag_move(self, e):
        dx, dy = e.x - self._drag_x, e.y - self._drag_y
        self.root.geometry(
            f"+{self.root.winfo_x()+dx}+{self.root.winfo_y()+dy}")
