import pygame
import os

from GRAFICA._modulo_elementi_grafici import Label_Text, Bottone_Push, Bottone_Toggle, RadioButton, Entrata, Scroll, ColorPicker, DropMenu, BaseElement
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

        BaseElement._init_scene(self.pappardella)

        bott_calls = BottoniCallbacks()

        self.costruisci_main()


    def costruisci_main(self):
        
        self.scene["main"] = Scena()

        self.scene["main"].label["cpu"] = Label_Text(x=58.5, y=98.5, text="cpu")
        self.scene["main"].label["fps"] = Label_Text(x=65.5, y=98.5, text="fps")
        self.scene["main"].label["battery"] = Label_Text(x=72.5, y=98.5, text="battery")
        self.scene["main"].label["memory"] = Label_Text(x=78.1, y=98.5, text="memory")
        self.scene["main"].label["clock"] = Label_Text(x=89.5, y=98.5, text="clock")
        
        self.scene["main"].label["debug"] = Label_Text(x=5, y=20, text="\\red{Hello world!}")
        self.scene["main"].scrolls["debug"] = Scroll(x=5, y=30, w=20, h=30, text="Scroll console")
        self.scene["main"].entrate["entrata"] = Entrata(x=5, y=70, w=10, h=2, text="ciao")
        self.scene["main"].color_pickers["debug"] = ColorPicker(x=35, y=20, w=5, h=3, initial_color=[220, 20, 60], text="Pick a color!")
        self.scene["main"].bottoni_t["debug1"] = Bottone_Toggle(x=35, y=50, w=10, h=3, state=False, text="Prova testo1", type_checkbox=False)
        self.scene["main"].bottoni_t["debug2"] = Bottone_Toggle(x=35, y=55, w=1, h=1, state=False, text="Prova testo2", type_checkbox=True)
        self.scene["main"].bottoni_p["debug"] = Bottone_Push(x=35, y=60, w=10, h=3, function=None, text="Prova testo")
        self.scene["main"].bottoni_r["debug"] = RadioButton(x=55, y=20, w=5, h=30, axis="y", cb_n=5, cb_s=[0, 0, 0, 0, 0], cb_t=[f"{i}" for i in range(5)], title="Hellou", multiple_choice=False, type_checkbox=True)
        self.scene["main"].drop_menu["debug"] = DropMenu(x=65, y=10, w=25, h=80)

        def hello(): print("hello")
        self.scene["main"].drop_menu["debug"].add_element(Bottone_Push(x=45, y=45, w=30, h=10, function=hello, text="Prova"), mantain_prop=True)
        self.scene["main"].drop_menu["debug"].add_element(Bottone_Push(x=35, y=35, w=30, h=10, function=hello, text="Prova"), mantain_prop=True)
        self.scene["main"].drop_menu["debug"].add_element(Bottone_Push(x=55, y=55, w=30, h=10, function=hello, text="Prova"), mantain_prop=True)
        self.scene["main"].drop_menu["debug"].add_element(ColorPicker(x=10, y=85, w=80, h=20, initial_color=[255, 0, 0], text="Pick a color"), mantain_prop=True)


class Scena:
    def __init__(self) -> None:
        self.label: dict[str, Label_Text] = {}
        self.bottoni_p: dict[str, Bottone_Push] = {}
        self.bottoni_t: dict[str, Bottone_Toggle] = {}
        self.bottoni_r: dict[str, RadioButton] = {}
        self.entrate: dict[str, Entrata] = {}
        self.scrolls: dict[str, Scroll] = {}
        self.color_pickers: dict[str, ColorPicker] = {}
        self.drop_menu: dict[str, DropMenu] = {}


    def disegna_scena(self, logica: 'Logica'):
        [label.disegnami(logica) for indice, label in self.label.items()]
        [bottone.disegnami(logica) for indice, bottone in self.bottoni_p.items()]
        [bottone.disegnami(logica) for indice, bottone in self.bottoni_t.items()]
        [bottone.disegnami(logica) for indice, bottone in self.bottoni_r.items()]
        [entrate.disegnami(logica) for indice, entrate in self.entrate.items()]
        [scroll.disegnami(logica) for indice, scroll in self.scrolls.items()]
        [color_picker.disegnami(logica) for indice, color_picker in self.color_pickers.items()]
        [dropmenu.disegnami(logica) for indice, dropmenu in self.drop_menu.items()]

    
    def gestisci_eventi(self, eventi: list[pygame.event.Event], logica: 'Logica'):
        [bottone.eventami(eventi, logica) for indice, bottone in self.bottoni_p.items()]
        [bottone.eventami(eventi, logica) for indice, bottone in self.bottoni_t.items()]
        [bottone.eventami(eventi, logica) for indice, bottone in self.bottoni_r.items()]
        [entrata.eventami(eventi, logica) for indice, entrata in self.entrate.items()]
        [scroll.eventami(eventi, logica) for indice, scroll in self.scrolls.items()]
        [color_picker.eventami(eventi, logica) for indice, color_picker in self.color_pickers.items()]
        [dropmenu.eventami(eventi, logica) for indice, dropmenu in self.drop_menu.items()]


