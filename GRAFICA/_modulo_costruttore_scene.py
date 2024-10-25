import pygame
import os

from GRAFICA._modulo_elementi_grafici import Label_Text, Bottone_Push, Bottone_Toggle, RadioButton, Entrata, Scroll, ColorPicker, DropMenu, BaseElement
from GRAFICA._modulo_bottoni_callbacks import BottoniCallbacks

NON_ESEGUIRE = False
if NON_ESEGUIRE:
    from GRAFICA._modulo_UI import Logica

class Costruttore:
    def __init__(self, screen, width, height) -> None:

        self.screen: pygame.Surface = screen
        self.bg_def = (40, 40, 40)

        self.scene: dict[str, Scena] = {}
        
        self.pappardella = {
            "screen": self.screen,
            "bg_def": self.bg_def,
            "x_screen": width,
            "y_screen": height,
        }

        BaseElement._init_scene(self.pappardella)

        bott_calls = BottoniCallbacks()

        self.costruisci_main()


    def recalc(self, new_w, new_h):

        self.pappardella["x_screen"] = new_w
        self.pappardella["y_screen"] = new_h

        BaseElement._init_scene(self.pappardella)

        for nome_scena, scena in self.scene.items():
            for index, ele in scena.label.items():
                ele.update_window_change()
            for index, ele in scena.bottoni_p.items():
                ele.update_window_change()
            for index, ele in scena.bottoni_r.items():
                ele.update_window_change()
            for index, ele in scena.bottoni_t.items():
                ele.update_window_change()
            for index, ele in scena.entrate.items():
                ele.update_window_change()
            for index, ele in scena.scrolls.items():
                ele.update_window_change()
            for index, ele in scena.color_pickers.items():
                ele.update_window_change()
            for index, ele in scena.drop_menu.items():
                ele.update_window_change()


    def costruisci_main(self):
        
        self.scene["main"] = Scena()

        s = self.scene["main"]

        s.label["clock"] = Label_Text(x=100, y=100, anchor="rd", text="." * 22)
        s.label["memory"] = Label_Text(anchor=("rc", "lc", s.label["clock"], -20, 0), text="." * 22)
        s.label["battery"] = Label_Text(anchor=("rc", "lc", s.label["memory"], -20, 0), text="." * 10)
        s.label["fps"] = Label_Text(anchor=("rc", "lc", s.label["battery"], -20, 0), text="." * 13)
        s.label["cpu"] = Label_Text(anchor=("rc", "lc", s.label["fps"], -20, 0), text="." * 13)

        s.drop_menu["debug"] = DropMenu(99, 5, "ru", 30, 90, "DEBUG DROP MENU", mantain_aspect_ratio=False)
        
        s.drop_menu["debug"].add_element("bottone1", Bottone_Toggle(x=50, y="0", anchor="cu", w=98, h="55", text=r"Tester1", type_checkbox=False))
        s.drop_menu["debug"].add_element("bottone2", Bottone_Toggle(x=50, y="55", anchor="cu", w=98, h="55", text=r"Tester2", type_checkbox=False))
        s.drop_menu["debug"].add_element("bottone3", Bottone_Toggle(x=50, y="110", anchor="cu", w=98, h="55", text=r"Tester3", type_checkbox=False))
        s.drop_menu["debug"].add_element("bottone4", Bottone_Toggle(x=50, y="165", anchor="cu", w=98, h="55", text=r"Tester4", type_checkbox=False))
        s.drop_menu["debug"].add_element("bottone5", Bottone_Toggle(x=50, y="220", anchor="cu", w=98, h="55", text=r"Tester5", type_checkbox=False))
        s.drop_menu["debug"].add_element("bottone6", Bottone_Toggle(x=50, y="275", anchor="cu", w=98, h="55", text=r"Tester6", type_checkbox=False))
        s.drop_menu["debug"].add_element("bottone7", Bottone_Toggle(x=50, y="330", anchor="cu", w=98, h="55", text=r"Tester7", type_checkbox=False))
        

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


