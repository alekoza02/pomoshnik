import pygame
import os
from numpy import array
from time import perf_counter

from GRAFICA._modulo_elementi_grafici import Label_Text, Bottone_Push, Bottone_Toggle, RadioButton, Entrata, Scroll, ColorPicker, DropMenu, BaseElement, Screen, Palette
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
        
        s.palette_popup = Palette()

        s.label["clock"] = Label_Text(x=100, y=100, anchor="rd", text="." * 22)
        s.label["memory"] = Label_Text(anchor=("rc", "lc", s.label["clock"], -20, 0), text="." * 22)
        s.label["battery"] = Label_Text(anchor=("rc", "lc", s.label["memory"], -20, 0), text="." * 8)
        s.label["fps"] = Label_Text(anchor=("rc", "lc", s.label["battery"], -20, 0), text="." * 13)
        s.label["cpu"] = Label_Text(anchor=("rc", "lc", s.label["fps"], -20, 0), text="." * 13)
        
        s.bottoni_p["exit"] = Bottone_Push(x=100, y=0, w="50", h="50", anchor="ru", text="X", function=self.bott_calls.exit)
        
        # ----------------------------------------------------------------------------------------------------

        s.screens["viewport"] = Screen(37.5, 50, "cc", 65, 90, mantain_aspect_ratio=False, latex_font=True)
        
        moltiplier = s.screens["viewport"].h / s.screens["viewport"].w

        s.screens["renderer"] = Screen(f"{s.screens["viewport"].x}", f"{s.screens["viewport"].y}", "lu", "4000", f"{4000 * moltiplier}", mantain_aspect_ratio=False, latex_font=True, hide=True)

        s.scrolls["elenco_plots"] = Scroll(76.5, 5, "lu", 22, 33, "Grafici caricati", mantain_aspect_ratio=False)

        s.drop_menu["item1"] = DropMenu(76.5, 40, "lu", 22, 55, "item1", hide=True)
        s.drop_menu["item2"] = DropMenu(76.5, 40, "lu", 22, 55, "item2", hide=True)
        s.drop_menu["item3"] = DropMenu(76.5, 40, "lu", 22, 55, "item3", hide=True)
        s.drop_menu["item4"] = DropMenu(76.5, 40, "lu", 22, 55, "item4", hide=True)
        s.drop_menu["item5"] = DropMenu(76.5, 40, "lu", 22, 55, "item5", hide=True)
        s.drop_menu["item6"] = DropMenu(76.5, 40, "lu", 22, 55, "item6", hide=True)
        s.drop_menu["item7"] = DropMenu(76.5, 40, "lu", 22, 55, "item7", hide=True)
        s.drop_menu["item8"] = DropMenu(76.5, 40, "lu", 22, 55, "item8", hide=True)
        s.drop_menu["item9"] = DropMenu(76.5, 40, "lu", 22, 55, "item9", hide=True)
        s.drop_menu["item10"] = DropMenu(76.5, 40, "lu", 22, 55, "item10", hide=True)
        s.drop_menu["item11"] = DropMenu(76.5, 40, "lu", 22, 55, "item11", hide=True)

        # ITEM 1 GEOMETRY ------------------------------------------------
        s.drop_menu["item1"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\#88dd88{Impostazioni base Geometria}", font_size=28))
        s.drop_menu["item1"].add_element("w_plot_area", Entrata(75, "120", "lu", 20, "30", text="0.8", title="larghezza plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999))
        s.drop_menu["item1"].add_element("h_plot_area", Entrata(75, "155", "lu", 20, "30", text="0.8", title="altezza plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999))
        s.drop_menu["item1"].add_element("x_plot_area", Entrata(75, "205", "lu", 20, "30", text="0.15", title="X plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999))
        s.drop_menu["item1"].add_element("y_plot_area", Entrata(75, "240", "lu", 20, "30", text="0.1", title="Y plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999))
        s.drop_menu["item1"].add_element("plot_area_bg", ColorPicker(s.palette_popup, "0", 30, "400", "cc", 10, "40", [50, 50, 50], bg=[50, 50, 50], text="Color plot area"))
        s.drop_menu["item1"].add_element("canvas_area_bg", ColorPicker(s.palette_popup, "1", 30, "450", "cc", 10, "40", [40, 40, 40], bg=[50, 50, 50], text="Color background"))
        
        s.drop_menu["item1"].add_element("normalizza", Bottone_Toggle(10, "525", "lc", 35, "50", False, False, "[0..1]"))
        s.drop_menu["item1"].add_element("percentualizza", Bottone_Toggle(90, "525", "rc", 35, "50", False, False, "[%]"))
        s.drop_menu["item1"].add_element("overlap", Bottone_Toggle(50, "600", "cc", 35, "50", True, False, "Plots Overlap"))
        # ITEM 1 GEOMETRY ------------------------------------------------
        
        
        # ITEM 2 PLOTS ---------------------------------------------------
        s.drop_menu["item2"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\#88dd88{Impostazioni base Grafici}", font_size=28))
        
        s.drop_menu["item2"].add_element("plot_name", Entrata(50, "90", "lu", 45, "30", text="", title="Plot name"))
        
        s.drop_menu["item2"].add_element("scatter_size", Entrata(75, "155", "lu", 20, "30", text="4", title="size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=1, num_valore_massimo=50))
        s.drop_menu["item2"].add_element("function_size", Entrata(75, "190", "lu", 20, "30", text="1", title="size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=1, num_valore_massimo=32))
        s.drop_menu["item2"].add_element("dashed_density", Entrata(75, "485", "lu", 20, "30", text="21", title="N° traits", lunghezza_max=3, solo_numeri=True, num_valore_minimo=3, num_valore_massimo=101))

        s.drop_menu["item2"].add_element("scatter_toggle", Bottone_Toggle(50, "155", "ru", "30", "30", text="Toggle scatter", type_checkbox=True, mantain_aspect_ratio=False, text_on_right=False, state=True))
        s.drop_menu["item2"].add_element("function_toggle", Bottone_Toggle(50, "190", "ru", "30", "30", text="Toggle function", type_checkbox=True, mantain_aspect_ratio=False, text_on_right=False, state=True))
        s.drop_menu["item2"].add_element("errorbar", Bottone_Toggle(50, "225", "ru", "30", "30", text="Toggle errors", type_checkbox=True, mantain_aspect_ratio=False, text_on_right=False, state=True))
        s.drop_menu["item2"].add_element("dashed", Bottone_Toggle(50, "485", "ru", "30", "30", text="Dashed line", type_checkbox=True, mantain_aspect_ratio=False, text_on_right=False, state=True))
        
        s.drop_menu["item2"].add_element("colore_function", ColorPicker(s.palette_popup, "2", 30, "340", "cc", 10, "40", [0, 0, 0], bg=[50, 50, 50], text="Colore function"))
        s.drop_menu["item2"].add_element("colore_scatter", ColorPicker(s.palette_popup, "3", 30, "395", "cc", 10, "40", [0, 0, 0], bg=[50, 50, 50], text="Colore scatter"))
        # ITEM 2 PLOTS ---------------------------------------------------


        # ITEM 3 AX LABELS -----------------------------------------------
        s.drop_menu["item3"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\#88dd88{Impostazioni base Label}", font_size=28))
        s.drop_menu["item3"].add_element("_title_drop_menu_avanz", Label_Text(50, "680", "cu", text=r"\#ddaa88{Impostazioni avanzate Label}", font_size=28))
        
        s.drop_menu["item3"].add_element("text_title", Entrata(50, "120", "lu", 45, "30", text="Title", title="Title text"))
        s.drop_menu["item3"].add_element("text_label_x", Entrata(50, "170", "lu", 45, "30", text="X axis", title="Label text X"))
        s.drop_menu["item3"].add_element("text_label_y", Entrata(50, "205", "lu", 45, "30", text="Y axis", title="Y"))
        
        s.drop_menu["item3"].add_element("font_size_title", Entrata(75, "305", "lu", 20, "30", text="48", title="Title font size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128))
        s.drop_menu["item3"].add_element("font_size_label_x", Entrata(75, "355", "lu", 20, "30", text="48", title="Label font size X", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128))
        s.drop_menu["item3"].add_element("font_size_label_y", Entrata(75, "390", "lu", 20, "30", text="48", title="Y", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128))
        s.drop_menu["item3"].add_element("label_title_color", ColorPicker(s.palette_popup, "4", 30, "495", "cc", 10, "40", [255, 255, 255], bg=[50, 50, 50], text="Colore titolo"))
        s.drop_menu["item3"].add_element("label_x_color", ColorPicker(s.palette_popup, "5", 30, "555", "cc", 10, "40", [255, 255, 255], bg=[50, 50, 50], text="Colore label X"))
        s.drop_menu["item3"].add_element("label_y_color", ColorPicker(s.palette_popup, "6", 30, "605", "cc", 10, "40", [255, 255, 255], bg=[50, 50, 50], text="Colore label Y"))
        
        # ITEM 3 AX LABELS -----------------------------------------------

        # ITEM 4 AXES ----------------------------------------------------
        s.drop_menu["item4"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\#88dd88{Impostazioni base Assi}", font_size=28))
        
        s.drop_menu["item4"].add_element("round_x", Entrata(75, "120", "lu", 20, "30", text="2", title="Round ticks X:", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=12))
        s.drop_menu["item4"].add_element("round_y", Entrata(75, "155", "lu", 20, "30", text="2", title="Y:", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=12))
        
        s.drop_menu["item4"].add_element("show_grid_x", Bottone_Toggle(95, "255", "ru", "30", "30", text="Mostra griglia X", state=True, type_checkbox=True, mantain_aspect_ratio=False, text_on_right=False))
        s.drop_menu["item4"].add_element("show_grid_y", Bottone_Toggle(95, "290", "ru", "30", "30", text="Mostra griglia Y", state=True, type_checkbox=True, mantain_aspect_ratio=False, text_on_right=False))
        
        s.drop_menu["item4"].add_element("formatting_x", Bottone_Toggle(95, "350", "ru", "30", "30", text="Usa notazione scientifica asse X", type_checkbox=True, mantain_aspect_ratio=False, text_on_right=False))
        s.drop_menu["item4"].add_element("formatting_y", Bottone_Toggle(95, "390", "ru", "30", "30", text="Usa notazione scientifica asse Y", type_checkbox=True, mantain_aspect_ratio=False, text_on_right=False))
        
        s.drop_menu["item4"].add_element("ax_color_x", ColorPicker(s.palette_popup, "7", 30, "505", "cc", 10, "40", [70, 70, 70], bg=[50, 50, 50], text="Colore asse X"))
        s.drop_menu["item4"].add_element("ax_color_y", ColorPicker(s.palette_popup, "8", 30, "555", "cc", 10, "40", [70, 70, 70], bg=[50, 50, 50], text="Colore asse Y"))
        s.drop_menu["item4"].add_element("tick_color_x", ColorPicker(s.palette_popup, "9", 30, "620", "cc", 10, "40", [255, 255, 255], bg=[50, 50, 50], text="Colore values X"))
        s.drop_menu["item4"].add_element("tick_color_y", ColorPicker(s.palette_popup, "10", 30, "670", "cc", 10, "40", [255, 255, 255], bg=[50, 50, 50], text="Colore values Y"))
        # ITEM 4 AXES ----------------------------------------------------


        # ITEM 5 LEGEND --------------------------------------------------
        s.drop_menu["item5"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\#88dd88{Impostazioni base Legenda}", font_size=28))
    
        s.drop_menu["item5"].add_element("show_legend", Bottone_Toggle(95, "80", "ru", "30", "30", text="\\#dfffdf{\\b{Mostra legenda}}", state=False, type_checkbox=True, mantain_aspect_ratio=False, text_on_right=False))

        s.drop_menu["item5"].add_element("x_legend", Entrata(75, "155", "lu", 20, "30", text="0.5", title="X legend", lunghezza_max=5, solo_numeri=True, num_valore_minimo=-0.5, num_valore_massimo=1.5))
        s.drop_menu["item5"].add_element("y_legend", Entrata(75, "190", "lu", 20, "30", text="0.5", title="Y legend", lunghezza_max=5, solo_numeri=True, num_valore_minimo=-0.5, num_valore_massimo=1.5))
        
        s.drop_menu["item5"].add_element("font_size_legend", Entrata(75, "255", "lu", 20, "30", text="48", title="Legend font size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128))
        
        s.drop_menu["item5"].add_element("show_legend_background", Bottone_Toggle(95, "350", "ru", "30", "30", text="\\#dfffdf{\\b{Disegna bg}}", state=False, type_checkbox=True, mantain_aspect_ratio=False, text_on_right=False))
        s.drop_menu["item5"].add_element("legend_color_background", ColorPicker(s.palette_popup, "11", 30, "430", "cc", 10, "40", [250, 250, 250], bg=[50, 50, 50], text="Color legend bg"))
        s.drop_menu["item5"].add_element("transparent_background", Bottone_Toggle(95, "490", "ru", "30", "30", text="Trasparenza bg", state=True, type_checkbox=True, mantain_aspect_ratio=False, text_on_right=False))
        s.drop_menu["item5"].add_element("blur_strenght", Entrata(75, "530", "lu", 20, "30", text="6", title="Forza di blur", lunghezza_max=2, solo_numeri=True, num_valore_minimo=1, num_valore_massimo=12))
        
        s.drop_menu["item5"].add_element("show_icons", Bottone_Toggle(95, "620", "ru", "30", "30", text="Mostra icone", state=True, type_checkbox=True, mantain_aspect_ratio=False, text_on_right=False))
        s.drop_menu["item5"].add_element("match_color_text", Bottone_Toggle(95, "660", "ru", "30", "30", text="Match text color", state=True, type_checkbox=True, mantain_aspect_ratio=False, text_on_right=False))
        s.drop_menu["item5"].add_element("color_text", ColorPicker(s.palette_popup, "12", 30, "720", "cc", 10, "40", [255, 255, 255], bg=[50, 50, 50], text="Color legend text"))
        # ITEM 5 LEGEND --------------------------------------------------


        # ITEM 6 IMPORT --------------------------------------------------
        s.drop_menu["item6"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\#88dd88{Impostazioni base Import}", font_size=28))
        
        s.drop_menu["item6"].add_element("import_single_plot", Bottone_Push(50, "80", "cu", 70, "40", function=self.bott_calls.load_file, text="Carica singolo file"))
        s.drop_menu["item6"].add_element("import_multip_plot", Bottone_Push(50, "130", "cu", 70, "40", function=self.bott_calls.load_files, text="Carica file multipli"))
    
        s.drop_menu["item6"].add_element("remove_element_selected", Bottone_Push(50, "200", "cu", 70, "40", function=self.bott_calls.change_state, text=r"\#dc143c{Elimina elemento selezionato}"))
        
        # ITEM 6 IMPORT --------------------------------------------------


        # ITEM 7 EXPORT --------------------------------------------------
        s.drop_menu["item7"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\#88dd88{Impostazioni base Export}", font_size=28))
        s.drop_menu["item7"].add_element("save_single_plot", Bottone_Push(50, "80", "cu", 70, "40", function=self.bott_calls.save_file, text="Salva grafico"))
        # ITEM 7 EXPORT --------------------------------------------------


        # ITEM 8 STATSISTIC ----------------------------------------------
        s.drop_menu["item8"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\#88dd88{Impostazioni base Statistica}", font_size=28))
        # ITEM 8 STATSISTIC ----------------------------------------------


        # ITEM 9 INTERPOLATION -------------------------------------------
        s.drop_menu["item9"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\#88dd88{Impostazioni base Interpolazioni}", font_size=28))
        # ITEM 9 INTERPOLATION -------------------------------------------


        # ITEM 10 MULTI-PLOTS --------------------------------------------
        s.drop_menu["item10"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\#88dd88{Impostazioni base Multi-Plots}", font_size=28))
        # ITEM 10 MULTI-PLOTS --------------------------------------------


        # ITEM 11 METADATA -----------------------------------------------
        s.drop_menu["item11"].add_element("_title_drop_menu_base", Label_Text(50, "10", "cu", text=r"\#88dd88{Impostazioni base Metadata}", font_size=28))
        # ITEM 11 METADATA -----------------------------------------------

        starting = 1
        stato_iniziale_tab = [False for _ in range(11)]
        stato_iniziale_tab[starting] = True        
        s.bottoni_r["modes"] = RadioButton(anchor=("rc", "lc", s.drop_menu["item3"], 0, 0), w="70", h="900", bg=array([30, 30, 30]), axis="y", cb_n=11, cb_s=stato_iniziale_tab, cb_t=["" for _ in range(11)], type_checkbox=False, w_button="70", h_button="70")
        [bottone.load_texture(f"item{index + 1}") for index, bottone in enumerate(s.bottoni_r["modes"].toggles)]
        
        s.bottoni_r["tools"] = RadioButton(x=0, y=5, anchor="lu", w="70", h="150", bg=array([30, 30, 30]), axis="y", cb_n=2, cb_s=[0, 0], cb_t=["" for _ in range(2)], type_checkbox=False, w_button="70", h_button="70")
        [bottone.load_texture(f"tool{index + 1}") for index, bottone in enumerate(s.bottoni_r["tools"].toggles)]

        s.bottoni_p["reset_zoom"] = Bottone_Push(anchor=("cu", "cd", s.bottoni_r["tools"], 0, 10), w="70", h="70", function=BottoniCallbacks.change_state)
        s.bottoni_p["reset_zoom"].load_texture(f"tool3")

        s.label["label_x"] = Label_Text(latex_font=True)
        s.label["label_y"] = Label_Text(latex_font=True)
        s.label["title"] = Label_Text(latex_font=True)
        s.label["legend"] = Label_Text(latex_font=True)

        def set_active_tab():
            for index, state in enumerate(self.scene["main"].bottoni_r["modes"].cb_s):
                self.scene["main"].drop_menu[f"item{index + 1}"].hide_plus_children(not state)
                
                if not self.scene["main"].drop_menu[f"item{index + 1}"].hide and not self.scene["main"].drop_menu[f"item{index + 1}"].inizializzato:
                    self.scene["main"].drop_menu[f"item{index + 1}"].inizializzato = True
                    self.scene["main"].drop_menu[f"item{index + 1}"].update_window_change()


        def hide_UI_element_with_toggle_legend_section():
            
            if self.scene["main"].bottoni_r["modes"].cb_s[4]:
                stato = not self.scene["main"].drop_menu["item5"].elements["show_legend"].state_toggle
                stato2 = not self.scene["main"].drop_menu["item5"].elements["show_legend_background"].state_toggle


                self.scene["main"].drop_menu["item5"].elements["legend_color_background"].hide_plus_children(stato or stato2)
                self.scene["main"].drop_menu["item5"].elements["transparent_background"].hide_plus_children(stato or stato2)
                self.scene["main"].drop_menu["item5"].elements["blur_strenght"].hide_plus_children(stato or stato2)
                
                self.scene["main"].drop_menu["item5"].elements["x_legend"].hide_plus_children(stato)
                self.scene["main"].drop_menu["item5"].elements["y_legend"].hide_plus_children(stato)
                self.scene["main"].drop_menu["item5"].elements["font_size_legend"].hide_plus_children(stato)
                self.scene["main"].drop_menu["item5"].elements["show_legend_background"].hide_plus_children(stato)
                self.scene["main"].drop_menu["item5"].elements["show_icons"].hide_plus_children(stato)

                self.scene["main"].drop_menu["item5"].elements["match_color_text"].hide_plus_children(stato)
                
                stato2 = self.scene["main"].drop_menu["item5"].elements["match_color_text"].state_toggle

                self.scene["main"].drop_menu["item5"].elements["color_text"].hide_plus_children(stato or stato2)



        def hide_UI_element_with_toggle_plot_section():

            if self.scene["main"].bottoni_r["modes"].cb_s[1]:

                if not self.scene["main"].drop_menu["item2"].elements["scatter_toggle"].state_toggle:
                    self.scene["main"].drop_menu["item2"].elements["scatter_size"].hide_plus_children(True)
                    self.scene["main"].drop_menu["item2"].elements["colore_scatter"].hide_plus_children(True)
                else:
                    self.scene["main"].drop_menu["item2"].elements["scatter_size"].hide_plus_children(False)
                    self.scene["main"].drop_menu["item2"].elements["colore_scatter"].hide_plus_children(False)

                if not self.scene["main"].drop_menu["item2"].elements["function_toggle"].state_toggle:
                    self.scene["main"].drop_menu["item2"].elements["function_size"].hide_plus_children(True)
                    self.scene["main"].drop_menu["item2"].elements["colore_function"].hide_plus_children(True)
                    self.scene["main"].drop_menu["item2"].elements["dashed"].hide_plus_children(True)
                else:
                    self.scene["main"].drop_menu["item2"].elements["function_size"].hide_plus_children(False)
                    self.scene["main"].drop_menu["item2"].elements["colore_function"].hide_plus_children(False)
                    self.scene["main"].drop_menu["item2"].elements["dashed"].hide_plus_children(False)


        def remove_selected_element():

            if self.scene["main"].drop_menu["item6"].elements["remove_element_selected"].flag_foo:
                self.scene["main"].drop_menu["item6"].elements["remove_element_selected"].flag_foo = False
                self.scene["main"].scrolls["elenco_plots"].remove_selected_item()


        s.functions.append(set_active_tab)
        s.functions.append(hide_UI_element_with_toggle_plot_section)
        s.functions.append(hide_UI_element_with_toggle_legend_section)
        s.functions.append(remove_selected_element)


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
        self.palette_popup: Palette = None

        self.pop_up_aperto: bool = False
        self.pop_up: list[ColorPicker] = []

        self.functions: list[function] = []


    def disegna_scena_inizio_ciclo(self, logica: 'Logica'):
        [label.disegnami(logica) for indice, label in self.label.items()]
        [bottone.disegnami(logica) for indice, bottone in self.bottoni_p.items()]
        [bottone.disegnami(logica) for indice, bottone in self.bottoni_t.items()]
        [bottone.disegnami(logica) for indice, bottone in self.bottoni_r.items()]
        [entrate.disegnami(logica) for indice, entrate in self.entrate.items()]
        [scroll.disegnami(logica) for indice, scroll in self.scrolls.items()]
        [screen.disegnami(logica) for indice, screen in self.screens.items()]
        [dropmenu.disegnami(logica) for indice, dropmenu in self.drop_menu.items()]
        [color_picker.disegnami(logica) for indice, color_picker in self.color_pickers.items()]
    
    
    def disegna_scena_fine_ciclo(self, logica: 'Logica'):
        self.palette_popup.disegnami(logica)

    
    def gestisci_eventi(self, eventi: list[pygame.event.Event], logica: 'Logica'):
        
        if not self.pop_up_aperto:

            [bottone.eventami(eventi, logica) for indice, bottone in self.bottoni_p.items()]
            [bottone.eventami(eventi, logica) for indice, bottone in self.bottoni_t.items()]
            [bottone.eventami(eventi, logica) for indice, bottone in self.bottoni_r.items()]
            [entrata.eventami(eventi, logica) for indice, entrata in self.entrate.items()]
            [scroll.eventami(eventi, logica) for indice, scroll in self.scrolls.items()]
            [screen.eventami(eventi, logica) for indice, screen in self.screens.items()]

            # POSSIBILI GENERATORI DI POP-UP

            for indice, color_picker in self.color_pickers.items():
                pop_up_domanda_color = color_picker.eventami(eventi, logica)
                
                if pop_up_domanda_color:
                    self.pop_up.append(color_picker)
                    self.pop_up_aperto = True


            for indice, dropmenu in self.drop_menu.items():
                pop_up_domanda_drop_menu = dropmenu.eventami(eventi, logica)

                if pop_up_domanda_drop_menu:
                    self.pop_up.append(pop_up_domanda_drop_menu)
                    self.pop_up_aperto = True

            
            for foo in self.functions:
                foo()

        else:
            
            for elemento in self.pop_up:
                if type(elemento) == ColorPicker:
                    pop_running = elemento.eventami(eventi, logica)
                    
                    if not pop_running:
                        self.pop_up.pop()

            if len(self.pop_up) == 0:
                self.pop_up_aperto = False

        
        self.palette_popup.eventami(logica, eventi)