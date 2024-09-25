import pygame
import os

from GRAFICA._modulo_elementi_grafici import Label_Text, Bottone_Push, Bottone_Toggle, Entrata
from GRAFICA._modulo_bottoni_callbacks import BottoniCallbacks

NON_ESEGUIRE = False
if NON_ESEGUIRE:
    from GRAFICA._modulo_UI import Logica

class Costruttore:
    def __init__(self, screen, offset, moltiplicatore_x, rapporto_x, rapporto_y) -> None:

        self.screen: pygame.Surface = screen
        self.offset: int = offset
        self.moltiplicatore_x: int = moltiplicatore_x
        self.ori_y: int =  self.screen.get_height()
        self.bg_def = (40, 40, 40)

        self.font = Font(24 * rapporto_y)

        self.scene: dict[str, Scena] = {}
        
        self.pappardella = {
            "font": self.font,
            "screen": self.screen,
            "bg_def": self.bg_def,
            "moltiplicatore_x": self.moltiplicatore_x,
            "ori_y": self.ori_y,
            "offset": self.offset
        }

        bott_calls = BottoniCallbacks()

        self.costruisci_main()



    def costruisci_main(self):
        
        self.scene["main"] = Scena()

        self.scene["main"].label["cpu"] = Label_Text(58.5, 98.5, "cpu", 1, self.pappardella)
        self.scene["main"].label["fps"] = Label_Text(65.5, 98.5, "fps", 1, self.pappardella)
        self.scene["main"].label["battery"] = Label_Text(72.5, 98.5, "battery", 1, self.pappardella)
        self.scene["main"].label["memory"] = Label_Text(78.1, 98.5, "memory", 1, self.pappardella)
        self.scene["main"].label["clock"] = Label_Text(89.5, 98.5, "clock", 1, self.pappardella)
        
        self.scene["main"].label["debug_visualizer"] = Label_Text(40, 50, "Ciao?", 1, self.pappardella)
        
        self.scene["main"].entrate["debug_visualizer1"] = Entrata(10, 50, 20, 2, "Prova testo", 1, self.pappardella)


class Scena:
    def __init__(self) -> None:
        self.label: dict[str, Label_Text] = {}
        self.bottoni_p: dict[str, Bottone_Push] = {}
        self.bottoni_t: dict[str, Bottone_Toggle] = {}
        self.entrate: dict[str, Entrata] = {}


    def disegna_scena(self, logica: 'Logica'):
        [label.disegnami() for indice, label in self.label.items()]
        [bottone.disegnami(logica) for indice, bottone in self.bottoni_p.items()]
        [bottone.disegnami() for indice, bottone in self.bottoni_t.items()]
        [entrate.disegnami(logica) for indice, entrate in self.entrate.items()]

    
    def gestisci_eventi(self, eventi: list[pygame.event.Event], logica: 'Logica'):
        [bottone.eventami(eventi, logica) for indice, bottone in self.bottoni_p.items()]
        [bottone.eventami(eventi, logica) for indice, bottone in self.bottoni_t.items()]
        [entrata.eventami(eventi, logica) for indice, entrata in self.entrate.items()]



class Font:
    def __init__(self, dim) -> None:
        
        self.original = int(dim)

        self.dim_font = self.original 
        path_r = os.path.join('TEXTURES', 'font_r.ttf')
        path_b = os.path.join('TEXTURES', 'font_b.ttf')
        path_i = os.path.join('TEXTURES', 'font_i.ttf')
        self.font_pyg_r = pygame.font.Font(path_r, self.dim_font)
        self.font_pyg_i = pygame.font.Font(path_i, self.dim_font)
        self.font_pyg_b = pygame.font.Font(path_b, self.dim_font)
        self.font_pixel_dim = self.font_pyg_r.size("a")


    def scala_font(self, moltiplicatore):

        if moltiplicatore == -1:
            if self.dim_font != self.original:
                self.dim_font = self.original
        else:
            self.dim_font *= moltiplicatore 
    
        path_r = os.path.join('TEXTURES', 'font_r.ttf')
        path_b = os.path.join('TEXTURES', 'font_b.ttf')
        path_i = os.path.join('TEXTURES', 'font_i.ttf')
        self.font_pyg_r = pygame.font.Font(path_r, round(self.dim_font))
        self.font_pyg_i = pygame.font.Font(path_i, round(self.dim_font))
        self.font_pyg_b = pygame.font.Font(path_b, round(self.dim_font))
        self.font_pixel_dim = self.font_pyg_r.size("a")

