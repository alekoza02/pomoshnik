import pygame
import os

from GRAFICA._modulo_elementi_grafici import Label_Text, Bottone_Push, Bottone_Toggle, RadioButton, Entrata, Scroll, ColorPicker, DropMenu, BaseElement, Screen
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
            for index, ele in scena.screens.items():
                ele.update_window_change()


    def costruisci_main(self):
        
        self.scene["main"] = Scena()

        s = self.scene["main"]

        s.label["clock"] = Label_Text(x=100, y=100, anchor="rd", text="." * 22)
        s.label["memory"] = Label_Text(anchor=("rc", "lc", s.label["clock"], -20, 0), text="." * 22)
        s.label["battery"] = Label_Text(anchor=("rc", "lc", s.label["memory"], -20, 0), text="." * 8)
        s.label["fps"] = Label_Text(anchor=("rc", "lc", s.label["battery"], -20, 0), text="." * 13)
        s.label["cpu"] = Label_Text(anchor=("rc", "lc", s.label["fps"], -20, 0), text="." * 13)

        s.screens["viewport"] = Screen(40, 50, "cc", 70, 90, mantain_aspect_ratio=False)

        s.drop_menu["main"] = DropMenu(77.5, 5, "lu", 20, 90, "Main")

        s.drop_menu["main"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text="Impostazioni base Label", font_size=28))
        
        s.drop_menu["main"].add_element("text_title", Entrata(50, "120", "lu", 45, "30", text="Title", title="Title text"))
        s.drop_menu["main"].add_element("text_label_x", Entrata(50, "170", "lu", 45, "30", text="X axis", title="Label text X"))
        s.drop_menu["main"].add_element("text_label_y", Entrata(50, "205", "lu", 45, "30", text="Y axis", title="Y"))
        
        s.drop_menu["main"].add_element("font_size_title", Entrata(75, "305", "lu", 20, "30", text="24", title="Title font size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128))
        s.drop_menu["main"].add_element("font_size_label_x", Entrata(75, "355", "lu", 20, "30", text="24", title="Label font size X", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128))
        s.drop_menu["main"].add_element("font_size_label_y", Entrata(75, "390", "lu", 20, "30", text="24", title="Y", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128))
        
        s.drop_menu["main"].add_element("_title_drop_menu_avanz", Label_Text(50, "480", "cu", text="Impostazioni avanzate Label", font_size=28))


        s.label["label_x"] = Label_Text()
        s.label["label_y"] = Label_Text()
        s.label["title"] = Label_Text()



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
        self.screens: dict[str, Screen] = {}


    def disegna_scena(self, logica: 'Logica'):
        [label.disegnami(logica) for indice, label in self.label.items()]
        [bottone.disegnami(logica) for indice, bottone in self.bottoni_p.items()]
        [bottone.disegnami(logica) for indice, bottone in self.bottoni_t.items()]
        [bottone.disegnami(logica) for indice, bottone in self.bottoni_r.items()]
        [entrate.disegnami(logica) for indice, entrate in self.entrate.items()]
        [scroll.disegnami(logica) for indice, scroll in self.scrolls.items()]
        [color_picker.disegnami(logica) for indice, color_picker in self.color_pickers.items()]
        [dropmenu.disegnami(logica) for indice, dropmenu in self.drop_menu.items()]
        [screen.disegnami(logica) for indice, screen in self.screens.items()]

    
    def gestisci_eventi(self, eventi: list[pygame.event.Event], logica: 'Logica'):
        [bottone.eventami(eventi, logica) for indice, bottone in self.bottoni_p.items()]
        [bottone.eventami(eventi, logica) for indice, bottone in self.bottoni_t.items()]
        [bottone.eventami(eventi, logica) for indice, bottone in self.bottoni_r.items()]
        [entrata.eventami(eventi, logica) for indice, entrata in self.entrate.items()]
        [scroll.eventami(eventi, logica) for indice, scroll in self.scrolls.items()]
        [color_picker.eventami(eventi, logica) for indice, color_picker in self.color_pickers.items()]
        [dropmenu.eventami(eventi, logica) for indice, dropmenu in self.drop_menu.items()]
        [screen.eventami(eventi, logica) for indice, screen in self.screens.items()]


