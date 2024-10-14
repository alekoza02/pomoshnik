import pygame
import os

from GRAFICA._modulo_elementi_grafici import Label_Text, Bottone_Push, Bottone_Toggle, RadioButton, Entrata, Scroll, ColorPicker
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

        self.scene: dict[str, Scena] = {}
        
        self.pappardella = {
            "screen": self.screen,
            "bg_def": self.bg_def,
            "moltiplicatore_x": self.moltiplicatore_x,
            "ori_y": self.ori_y,
            "offset": self.offset,
            "rapporto_y": rapporto_y,
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
        
        # self.scene["main"].scrolls["debug_visualizer"] = Scroll(10, 20, 37, 30, "Prova testo", 1.3, self.pappardella)
        # self.scene["main"].label["vis"] = Label_Text(80, 50, "", 1, self.pappardella)
        # self.scene["main"].bottoni_t["bottone"] = Bottone_Toggle(50, 50, False, "Prova testo", 1.3, self.pappardella)
        # self.scene["main"].entrate["entrata"] = Entrata(80, 30, 10, 2, "ciao", 1, self.pappardella)
        # self.scene["main"].color_pickers["debug"] = ColorPicker(30, 30, [180, 0, 0], "Pick a color!", 1, self.pappardella)
        self.scene["main"].bottoni_r["debug"] = RadioButton(30, 30, 5, [0, 0, 0, 0, 0], [f"{i}" for i in range(5)], "Hellou", False, 1, self.pappardella)


class Scena:
    def __init__(self) -> None:
        self.label: dict[str, Label_Text] = {}
        self.bottoni_p: dict[str, Bottone_Push] = {}
        self.bottoni_t: dict[str, Bottone_Toggle] = {}
        self.bottoni_r: dict[str, RadioButton] = {}
        self.entrate: dict[str, Entrata] = {}
        self.scrolls: dict[str, Scroll] = {}
        self.color_pickers: dict[str, ColorPicker] = {}


    def disegna_scena(self, logica: 'Logica'):
        [label.disegnami() for indice, label in self.label.items()]
        [bottone.disegnami(logica) for indice, bottone in self.bottoni_p.items()]
        [bottone.disegnami() for indice, bottone in self.bottoni_t.items()]
        [bottone.disegnami() for indice, bottone in self.bottoni_r.items()]
        [entrate.disegnami(logica) for indice, entrate in self.entrate.items()]
        [scroll.disegnami(logica) for indice, scroll in self.scrolls.items()]
        [color_picker.disegnami(logica) for indice, color_picker in self.color_pickers.items()]

    
    def gestisci_eventi(self, eventi: list[pygame.event.Event], logica: 'Logica'):
        [bottone.eventami(eventi, logica) for indice, bottone in self.bottoni_p.items()]
        [bottone.eventami(eventi, logica) for indice, bottone in self.bottoni_t.items()]
        [bottone.eventami(eventi, logica) for indice, bottone in self.bottoni_r.items()]
        [entrata.eventami(eventi, logica) for indice, entrata in self.entrate.items()]
        [scroll.eventami(eventi, logica) for indice, scroll in self.scrolls.items()]
        [color_picker.eventami(eventi, logica) for indice, color_picker in self.color_pickers.items()]


