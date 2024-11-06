import pygame
import os
from numpy import array

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

        self.bott_calls = BottoniCallbacks()

        self.costruisci_main()


    def recalc(self, new_w, new_h):

        self.pappardella["x_screen"] = new_w
        self.pappardella["y_screen"] = new_h

        BaseElement._init_scene(self.pappardella)

        for nome_scena, scena in self.scene.items():
            for index, ele in scena.screens.items():
                ele.update_window_change()
            for index, ele in scena.drop_menu.items():
                ele.update_window_change()
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


    def costruisci_main(self):
        
        self.scene["main"] = Scena()

        s = self.scene["main"]

        s.label["clock"] = Label_Text(x=100, y=100, anchor="rd", text="." * 22)
        s.label["memory"] = Label_Text(anchor=("rc", "lc", s.label["clock"], -20, 0), text="." * 22)
        s.label["battery"] = Label_Text(anchor=("rc", "lc", s.label["memory"], -20, 0), text="." * 8)
        s.label["fps"] = Label_Text(anchor=("rc", "lc", s.label["battery"], -20, 0), text="." * 13)
        s.label["cpu"] = Label_Text(anchor=("rc", "lc", s.label["fps"], -20, 0), text="." * 13)
        
        s.bottoni_p["exit"] = Bottone_Push(x=100, y=0, w="50", h="50", anchor="ru", text="X", function=self.bott_calls.exit)
        
        # ----------------------------------------------------------------------------------------------------

        s.screens["viewport"] = Screen(37.5, 50, "cc", 70, 90, mantain_aspect_ratio=False)

        s.drop_menu["item1"] = DropMenu(76.5, 5, "lu", 22, 90, "item1", hide=True)
        s.drop_menu["item2"] = DropMenu(76.5, 40, "lu", 22, 55, "item2", hide=True)
        s.drop_menu["item3"] = DropMenu(76.5, 5, "lu", 22, 90, "item3", hide=True)
        s.drop_menu["item4"] = DropMenu(76.5, 5, "lu", 22, 90, "item4", hide=True)
        s.drop_menu["item5"] = DropMenu(76.5, 5, "lu", 22, 90, "item5", hide=True)
        s.drop_menu["item6"] = DropMenu(76.5, 5, "lu", 22, 90, "item6", hide=True)
        s.drop_menu["item7"] = DropMenu(76.5, 5, "lu", 22, 90, "item7", hide=True)
        s.drop_menu["item8"] = DropMenu(76.5, 5, "lu", 22, 90, "item8", hide=True)
        s.drop_menu["item9"] = DropMenu(76.5, 5, "lu", 22, 90, "item9", hide=True)
        s.drop_menu["item10"] = DropMenu(76.5, 5, "lu", 22, 90, "item10", hide=True)
        s.drop_menu["item11"] = DropMenu(76.5, 5, "lu", 22, 90, "item11", hide=True)

        # ITEM 1 GEOMETRY ------------------------------------------------
        s.drop_menu["item1"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\green{Impostazioni base Geometria}", font_size=28))
        # ITEM 1 GEOMETRY ------------------------------------------------
        
        
        # ITEM 2 PLOTS ---------------------------------------------------
        s.scrolls["item2"] = Scroll(76.5, 5, "lu", 22, 35, "Grafici caricati", mantain_aspect_ratio=False)
        s.drop_menu["item2"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\green{Impostazioni base Grafici}", font_size=28))
        # ITEM 2 PLOTS ---------------------------------------------------


        # ITEM 3 AX LABELS -----------------------------------------------
        s.drop_menu["item3"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\green{Impostazioni base Label}", font_size=28))
        
        s.drop_menu["item3"].add_element("text_title", Entrata(50, "120", "lu", 45, "30", text="Title", title="Title text"))
        s.drop_menu["item3"].add_element("text_label_x", Entrata(50, "170", "lu", 45, "30", text="X axis", title="Label text X"))
        s.drop_menu["item3"].add_element("text_label_y", Entrata(50, "205", "lu", 45, "30", text="Y axis", title="Y"))
        
        s.drop_menu["item3"].add_element("font_size_title", Entrata(75, "305", "lu", 20, "30", text="24", title="Title font size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128))
        s.drop_menu["item3"].add_element("font_size_label_x", Entrata(75, "355", "lu", 20, "30", text="24", title="Label font size X", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128))
        s.drop_menu["item3"].add_element("font_size_label_y", Entrata(75, "390", "lu", 20, "30", text="24", title="Y", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128))
        
        s.drop_menu["item3"].add_element("_title_drop_menu_avanz", Label_Text(50, "480", "cu", text=r"\yellow{Impostazioni avanzate Label}", font_size=28))
        
        s.drop_menu["item3"].add_element("_title_drop_menu_debug", Label_Text(50, "900", "cu", text=r"\red{Debugging Label}", font_size=28))
        # ITEM 3 AX LABELS -----------------------------------------------

        # ITEM 4 AXES ----------------------------------------------------
        s.drop_menu["item4"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\green{Impostazioni base Assi}", font_size=28))
        
        s.drop_menu["item4"].add_element("round_x", Entrata(75, "120", "lu", 20, "30", text="2", title="Round ticks X:", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=12))
        s.drop_menu["item4"].add_element("round_y", Entrata(75, "155", "lu", 20, "30", text="2", title="Y:", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=12))
        
        s.drop_menu["item4"].add_element("formatting_x", Bottone_Toggle(95, "255", "ru", "30", "30", text="Usa notazione scientifica asse X", type_checkbox=True, mantain_aspect_ratio=False, text_on_right=False))
        s.drop_menu["item4"].add_element("formatting_y", Bottone_Toggle(95, "290", "ru", "30", "30", text="Usa notazione scientifica asse Y", type_checkbox=True, mantain_aspect_ratio=False, text_on_right=False))
        # ITEM 4 AXES ----------------------------------------------------


        # ITEM 5 PLOTS ---------------------------------------------------
        s.drop_menu["item5"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\green{Impostazioni base Legenda}", font_size=28))
        # ITEM 5 PLOTS ---------------------------------------------------


        # ITEM 6 PLOTS ---------------------------------------------------
        s.drop_menu["item6"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\green{Impostazioni base Import}", font_size=28))
        # ITEM 6 PLOTS ---------------------------------------------------


        # ITEM 7 PLOTS ---------------------------------------------------
        s.drop_menu["item7"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\green{Impostazioni base Export}", font_size=28))
        # ITEM 7 PLOTS ---------------------------------------------------


        # ITEM 8 PLOTS ---------------------------------------------------
        s.drop_menu["item8"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\green{Impostazioni base Statistica}", font_size=28))
        # ITEM 8 PLOTS ---------------------------------------------------


        # ITEM 9 PLOTS ---------------------------------------------------
        s.drop_menu["item9"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\green{Impostazioni base Interpolazioni}", font_size=28))
        # ITEM 9 PLOTS ---------------------------------------------------


        # ITEM 10 PLOTS ---------------------------------------------------
        s.drop_menu["item10"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\green{Impostazioni base Multi-Plots}", font_size=28))
        # ITEM 10 PLOTS ---------------------------------------------------


        # ITEM 11 PLOTS ---------------------------------------------------
        s.drop_menu["item11"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\green{Impostazioni base Metadata}", font_size=28))
        # ITEM 11 PLOTS ---------------------------------------------------



        s.bottoni_r["modes"] = RadioButton(anchor=("rc", "lc", s.drop_menu["item3"], 0, 0), w="70", h="900", bg=array([35, 35, 35]), axis="y", cb_n=11, cb_s=[False for _ in range(11)], cb_t=["" for _ in range(11)], type_checkbox=False, w_button="70", h_button="70")
        [bottone.load_texture(f"item{index + 1}") for index, bottone in enumerate(s.bottoni_r["modes"].toggles)]
        
        s.label["label_x"] = Label_Text(latex_font=True)
        s.label["label_y"] = Label_Text(latex_font=True)
        s.label["title"] = Label_Text(latex_font=True)

        def set_active_tab():
            for index, state in enumerate(self.scene["main"].bottoni_r["modes"].cb_s):
                self.scene["main"].drop_menu[f"item{index + 1}"].hide = not state

                if index == 1:
                    self.scene["main"].scrolls[f"item{index + 1}"].hide = not state


        s.functions.append(set_active_tab)



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

        self.functions: list[function] = []


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

        for foo in self.functions:
            foo()
