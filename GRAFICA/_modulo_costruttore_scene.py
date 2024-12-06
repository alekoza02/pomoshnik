import pygame
import os
from numpy import array
from time import perf_counter

from GRAFICA._modulo_elementi_grafici import Label_Text, Bottone_Push, Bottone_Toggle, RadioButton, Entrata, Scroll, ColorPicker, ContextMenu, BaseElement, Screen, Palette
from GRAFICA._modulo_bottoni_callbacks import BottoniCallbacks

NON_ESEGUIRE = False
if NON_ESEGUIRE:
    from GRAFICA._modulo_UI import Logica

class Costruttore:
    def __init__(self, screen, width, height, font_size) -> None:

        self.screen: pygame.Surface = screen
        self.bg_def = (40, 40, 40)

        self.scene: dict[str, Scena] = {}
        
        self.pappardella = {
            "screen": self.screen,
            "bg_def": self.bg_def,
            "x_screen": width,
            "y_screen": height,
            "font_size": font_size
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
            for index, ele in scena.context_menu.items():
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
        
        s.palette_popup = Palette(x="50%w", y="50%h", anchor="cc", w="40%w", h="40%h")

        s.context_menu["main"] = ContextMenu(x="0px", y="0px", w="100%w", h="100%h", anchor="lu", bg=[30, 30, 30], scrollable=False)

        s.context_menu["main"].add_element("clock", Label_Text(x="100%w", y="100%h", w="-*w", h="-*h", anchor="rd", text="." * 22))
        s.context_menu["main"].add_element("memory", Label_Text(anchor=("rd ld (-0.7%w) (0px)", s.context_menu["main"].elements["clock"]), w="-*w", h="-*h", text="." * 22))
        s.context_menu["main"].add_element("battery", Label_Text(anchor=("rd ld (-0.7%w) (0px)", s.context_menu["main"].elements["memory"]), w="-*w", h="-*h", text="." * 8))
        s.context_menu["main"].add_element("fps", Label_Text(anchor=("rd ld (-0.7%w) (0px)", s.context_menu["main"].elements["battery"]), w="-*w", h="-*h", text="." * 13))
        s.context_menu["main"].add_element("cpu", Label_Text(anchor=("rd ld (-0.7%w) (0px)", s.context_menu["main"].elements["fps"]), w="-*w", h="-*h", text="." * 13))


        s.context_menu["main"].add_element("exit", Bottone_Push(x="100%w", y="0px", w="50px", h="50px", anchor="ru", text="X", function=self.bott_calls.exit))
        
        # # ----------------------------------------------------------------------------------------------------

        s.context_menu["main"].add_element("viewport", Screen(x="37.5%w", y="50%h", anchor="cc", w="65%w", h="90%h", latex_font=True))
        
        moltiplier = s.context_menu["main"].elements["viewport"].h / s.context_menu["main"].elements["viewport"].w

        s.context_menu["main"].add_element("renderer", Screen(f"{s.context_menu["main"].elements["viewport"].x}px", f"{s.context_menu["main"].elements["viewport"].y}px", anchor="lu", w="4000px", h=f"{4000 * moltiplier}px", latex_font=True, screenshot_type=True))

        s.context_menu["main"].add_element("elenco_plots", Scroll(x="73.5%w", y="5%h", anchor="lu", w="26%w", h="33%h", text="Grafici caricati"))

        s.context_menu["item1"] = ContextMenu(x="73.5%w", y="40%h", anchor="lu", w="26%w", h="55%h")
        s.context_menu["item2"] = ContextMenu(x="73.5%w", y="40%h", anchor="lu", w="26%w", h="55%h")
        s.context_menu["item3"] = ContextMenu(x="73.5%w", y="40%h", anchor="lu", w="26%w", h="55%h")
        s.context_menu["item4"] = ContextMenu(x="73.5%w", y="40%h", anchor="lu", w="26%w", h="55%h")
        s.context_menu["item5"] = ContextMenu(x="73.5%w", y="40%h", anchor="lu", w="26%w", h="55%h")
        s.context_menu["item6"] = ContextMenu(x="73.5%w", y="40%h", anchor="lu", w="26%w", h="55%h")
        s.context_menu["item7"] = ContextMenu(x="73.5%w", y="40%h", anchor="lu", w="26%w", h="55%h")
        s.context_menu["item8"] = ContextMenu(x="73.5%w", y="40%h", anchor="lu", w="26%w", h="55%h")
        s.context_menu["item9"] = ContextMenu(x="73.5%w", y="40%h", anchor="lu", w="26%w", h="55%h")
        s.context_menu["item10"] = ContextMenu(x="73.5%w", y="40%h", anchor="lu", w="26%w", h="55%h")
        s.context_menu["item11"] = ContextMenu(x="73.5%w", y="40%h", anchor="lu", w="26%w", h="55%h")

        # # ITEM 1 GEOMETRY ------------------------------------------------
        s.context_menu["item1"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", w="-*w", h="-*h", text=r"\#88dd88{Impostazioni base Geometria}"))
        s.context_menu["item1"].add_element("w_plot_area", Entrata("75%w", "120px", "lu", "20%w", "30px", text="0.8", title="larghezza plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999))
        s.context_menu["item1"].add_element("h_plot_area", Entrata("75%w", "155px", "lu", "20%w", "30px", text="0.8", title="altezza plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999))
        s.context_menu["item1"].add_element("x_plot_area", Entrata("75%w", "205px", "lu", "20%w", "30px", text="0.15", title="X plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999))
        s.context_menu["item1"].add_element("y_plot_area", Entrata("75%w", "240px", "lu", "20%w", "30px", text="0.1", title="Y plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999))
        s.context_menu["item1"].add_element("plot_area_bg", ColorPicker(s.palette_popup, "0", "30%w", "400px", "cc", "30%w", "40px", [50, 50, 50], bg=[50, 50, 50], text="Color plot area"))
        s.context_menu["item1"].add_element("canvas_area_bg", ColorPicker(s.palette_popup, "1", "30%w", "450px", "cc", "30%w", "40px", [40, 40, 40], bg=[50, 50, 50], text="Color background"))
        
        s.context_menu["item1"].add_element("norma_perc", RadioButton("50%w", "525px", "cc", "70%w", "50px", "x", cb_n=2, cb_s=[0, 0], cb_t=["[0..1]", "[%]"], type_checkbox=0, w_button="35%w", h_button="50px"))
        s.context_menu["item1"].add_element("overlap", Bottone_Toggle("50%w", "600px", "cc", "35%w", "50px", True, False, "Plots Overlap"))
        s.context_menu["item1"].add_element("second_y_axis", Bottone_Toggle("50%w", "700px", "cc", "35%w", "50px", False, False, "Toggle 2° Y axis"))
        # # ITEM 1 GEOMETRY ------------------------------------------------
        
        
        # # ITEM 2 PLOTS ---------------------------------------------------
        s.context_menu["item2"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", w="-*w", h="-*h", text=r"\#88dd88{Impostazioni base Grafici}"))
        
        s.context_menu["item2"].add_element("plot_name", Entrata("20%w", "90px", "lu", "75%w", "30px", text="", title="Name: "))
    
        s.context_menu["item2"].add_element("scatter_size", Entrata("55%w", "165px", "lu", "10%w", "30px", text="4", title="size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=1, num_valore_massimo=50))
        s.context_menu["item2"].add_element("scatter_border", Entrata("95%w", "165px", "ru", "10%w", "30px", text="0", title="width", lunghezza_max=2, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=9))
        s.context_menu["item2"].add_element("function_size", Entrata("55%w", "200px", "lu", "10%w", "30px", text="1", title="size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=1, num_valore_massimo=32))
        s.context_menu["item2"].add_element("dashed_density", Entrata("75%w", "495px", "lu", "10%w", "30px", text="21", title="N° traits", lunghezza_max=3, solo_numeri=True, num_valore_minimo=3, num_valore_massimo=101))

        s.context_menu["item2"].add_element("scatter_toggle", Bottone_Toggle("40%w", "165px", "ru", "30px", "30px", text="Toggle scatter", type_checkbox=True, text_on_right=False, state=True))
        s.context_menu["item2"].add_element("function_toggle", Bottone_Toggle("40%w", "200px", "ru", "30px", "30px", text="Toggle function", type_checkbox=True, text_on_right=False, state=True))
        s.context_menu["item2"].add_element("errorbar", Bottone_Toggle("40%w", "235px", "ru", "30px", "30px", text="Toggle errors", type_checkbox=True, text_on_right=False, state=True))
        s.context_menu["item2"].add_element("dashed", Bottone_Toggle("40%w", "495px", "ru", "30px", "30px", text="Dashed line", type_checkbox=True, text_on_right=False, state=True))
        
        s.context_menu["item2"].add_element("colore_function", ColorPicker(s.palette_popup, "2", "30%w", "350px", "cc", "30%w", "40px", [0, 0, 0], bg=[50, 50, 50], text="Colore function"))
        s.context_menu["item2"].add_element("colore_scatter", ColorPicker(s.palette_popup, "3", "30%w", "405px", "cc", "30%w", "40px", [0, 0, 0], bg=[50, 50, 50], text="Colore scatter"))
    
        s.context_menu["item2"].add_element("gradient", Bottone_Toggle("40%w", "600px", "ru", "30px", "30px", 0, text="Gradient", text_on_right=0))
        s.context_menu["item2"].add_element("grad_mode", RadioButton("90%w", "600px", "ru", "35%w", "80px", axis="y", cb_n=2, cb_s=[0, 1], cb_t=["Horizontal", "Vertical"], type_checkbox=False, w_button="35%w", h_button="40px"))
        
        s.context_menu["item2"].add_element("add_second_axis", Bottone_Toggle("40%w", "750px", "ru", "30px", "30px", 0, text="Add to the second Y axis"))
        # # ITEM 2 PLOTS ---------------------------------------------------


        # # ITEM 3 AX LABELS -----------------------------------------------
        s.context_menu["item3"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", w="-*w", h="-*h", text=r"\#88dd88{Impostazioni base Label}"))
        
        s.context_menu["item3"].add_element("text_title", Entrata("50%w", "120px", "lu", "45%w", "30px", text="Title", title="Title text"))
        s.context_menu["item3"].add_element("text_label_x", Entrata("50%w", "170px", "lu", "45%w", "30px", text="X axis", title="Label text X"))
        s.context_menu["item3"].add_element("text_label_y", Entrata("50%w", "205px", "lu", "45%w", "30px", text="Y axis", title="Y"))
        s.context_menu["item3"].add_element("text_label_2y", Entrata("50%w", "240px", "lu", "45%w", "30px", text="2°Y axis", title="2°Y"))
        
        s.context_menu["item3"].add_element("font_size_title", Entrata("75%w", "305px", "lu", "20%w", "30px", text="48", title="Title font size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128))
        s.context_menu["item3"].add_element("font_size_label_x", Entrata("75%w", "355px", "lu", "20%w", "30px", text="48", title="Label font size X", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128))
        s.context_menu["item3"].add_element("font_size_label_y", Entrata("75%w", "390px", "lu", "20%w", "30px", text="48", title="Y", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128))
        s.context_menu["item3"].add_element("font_size_label_2y", Entrata("75%w", "425px", "lu", "20%w", "30px", text="48", title="2°Y", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128))
        s.context_menu["item3"].add_element("label_title_color", ColorPicker(s.palette_popup, "4", "30%w", "500px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore titolo"))
        s.context_menu["item3"].add_element("label_x_color", ColorPicker(s.palette_popup, "5", "30%w", "570px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore label X"))
        s.context_menu["item3"].add_element("label_y_color", ColorPicker(s.palette_popup, "6", "30%w", "620px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore label Y"))
        s.context_menu["item3"].add_element("label_2y_color", ColorPicker(s.palette_popup, "7", "30%w", "670px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore label 2Y"))
        
        s.context_menu["item3"].add_element("show_coords_projection", Bottone_Toggle("95%w", "750px", "ru", "30px", "30px", text="Mostra proiezione coords", type_checkbox=True, text_on_right=False))
        # # ITEM 3 AX LABELS -----------------------------------------------
        

        # # ITEM 4 AXES ----------------------------------------------------
        s.context_menu["item4"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", w="-*w", h="-*h", text=r"\#88dd88{Impostazioni base Assi}"))
        
        s.context_menu["item4"].add_element("round_x", Entrata("75%w", "120px", "lu", "20%w", "30px", text="2", title="Round ticks X:", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=12))
        s.context_menu["item4"].add_element("round_y", Entrata("75%w", "155px", "lu", "20%w", "30px", text="2", title="Y:", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=12))
        s.context_menu["item4"].add_element("round_2y", Entrata("75%w", "190px", "lu", "20%w", "30px", text="2", title="2°Y:", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=12))
        
        s.context_menu["item4"].add_element("show_grid_x", Bottone_Toggle("95%w", "255px", "ru", "30px", "30px", text="Mostra griglia X", state=True, type_checkbox=True, text_on_right=False))
        s.context_menu["item4"].add_element("show_grid_y", Bottone_Toggle("95%w", "290px", "ru", "30px", "30px", text="Mostra griglia Y", state=True, type_checkbox=True, text_on_right=False))
        s.context_menu["item4"].add_element("show_grid_2y", Bottone_Toggle("95%w", "325px", "ru", "30px", "30px", text="Mostra griglia 2°Y", state=True, type_checkbox=True, text_on_right=False))
        
        s.context_menu["item4"].add_element("formatting_x", Bottone_Toggle("95%w", "385px", "ru", "30px", "30px", text="Usa notazione scientifica asse X", type_checkbox=True, text_on_right=False))
        s.context_menu["item4"].add_element("formatting_y", Bottone_Toggle("95%w", "420px", "ru", "30px", "30px", text="Usa notazione scientifica asse Y", type_checkbox=True, text_on_right=False))
        s.context_menu["item4"].add_element("formatting_2y", Bottone_Toggle("95%w", "455px", "ru", "30px", "30px", text="Usa notazione scientifica asse 2°Y", type_checkbox=True, text_on_right=False))
        
        s.context_menu["item4"].add_element("ax_color_x", ColorPicker(s.palette_popup, "8", "30%w", "565px", "cc", "30%w", "40px", [70, 70, 70], bg=[50, 50, 50], text="Colore asse X"))
        s.context_menu["item4"].add_element("ax_color_y", ColorPicker(s.palette_popup, "9", "30%w", "615px", "cc", "30%w", "40px", [70, 70, 70], bg=[50, 50, 50], text="Colore asse Y"))
        s.context_menu["item4"].add_element("ax_color_2y", ColorPicker(s.palette_popup, "10", "30%w", "670px", "cc", "30%w", "40px", [70, 70, 70], bg=[50, 50, 50], text="Colore asse 2°Y"))
        s.context_menu["item4"].add_element("tick_color_x", ColorPicker(s.palette_popup, "11", "30%w", "760px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore values X"))
        s.context_menu["item4"].add_element("tick_color_y", ColorPicker(s.palette_popup, "12", "30%w", "810px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore values Y"))
        s.context_menu["item4"].add_element("tick_color_2y", ColorPicker(s.palette_popup, "13", "30%w", "860px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore values 2°Y"))
        # # ITEM 4 AXES ----------------------------------------------------


        # # ITEM 5 LEGEND --------------------------------------------------
        s.context_menu["item5"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", w="-*w", h="-*h", text=r"\#88dd88{Impostazioni base Legenda}"))
    
        s.context_menu["item5"].add_element("show_legend", Bottone_Toggle("95%w", "80px", "ru", "30px", "30px", text="\\#dfffdf{\\b{Mostra legenda}}", state=False, type_checkbox=True, text_on_right=False))

        s.context_menu["item5"].add_element("x_legend", Entrata("75%w", "155px", "lu", "20%w", "30px", text="0.5", title="X legend", lunghezza_max=5, solo_numeri=True, num_valore_minimo=-0.5, num_valore_massimo=1.5))
        s.context_menu["item5"].add_element("y_legend", Entrata("75%w", "190px", "lu", "20%w", "30px", text="0.5", title="Y legend", lunghezza_max=5, solo_numeri=True, num_valore_minimo=-0.5, num_valore_massimo=1.5))
        
        s.context_menu["item5"].add_element("font_size_legend", Entrata("75%w", "255px", "lu", "20%w", "30px", text="48", title="Legend font size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128))
        
        s.context_menu["item5"].add_element("show_legend_background", Bottone_Toggle("95%w", "350px", "ru", "30px", "30px", text="\\#dfffdf{\\b{Disegna bg}}", state=False, type_checkbox=True, text_on_right=False))
        s.context_menu["item5"].add_element("legend_color_background", ColorPicker(s.palette_popup, "14", "30%w", "430px", "cc", "30%w", "40px", [250, 250, 250], bg=[50, 50, 50], text="Color legend bg"))
        s.context_menu["item5"].add_element("transparent_background", Bottone_Toggle("95%w", "490px", "ru", "30px", "30px", text="Trasparenza bg", state=True, type_checkbox=True, text_on_right=False))
        s.context_menu["item5"].add_element("blur_strenght", Entrata("75%w", "530px", "lu", "20%w", "30px", text="6", title="Forza di blur", lunghezza_max=2, solo_numeri=True, num_valore_minimo=1, num_valore_massimo=12))
        
        s.context_menu["item5"].add_element("show_icons", Bottone_Toggle("95%w", "620px", "ru", "30px", "30px", text="Mostra icone", state=True, type_checkbox=True, text_on_right=False))
        s.context_menu["item5"].add_element("match_color_text", Bottone_Toggle("95%w", "660px", "ru", "30px", "30px", text="Match text color", state=True, type_checkbox=True, text_on_right=False))
        s.context_menu["item5"].add_element("color_text", ColorPicker(s.palette_popup, "15", "30%w", "720px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Color legend text"))
        # # ITEM 5 LEGEND --------------------------------------------------


        # # ITEM 6 IMPORT --------------------------------------------------
        s.context_menu["item6"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Import}"))
        
        s.context_menu["item6"].add_element("import_single_plot", Bottone_Push("50%w", "80px", "cu", "70%w", "40px", function=self.bott_calls.load_file, text="Carica singolo file"))
        s.context_menu["item6"].add_element("import_multip_plot", Bottone_Push("50%w", "130px", "cu", "70%w", "40px", function=self.bott_calls.load_files, text="Carica file multipli"))
    
        s.context_menu["item6"].add_element("remove_element_selected", Bottone_Push("50%w", "200px", "cu", "70%w", "40px", function=self.bott_calls.change_state, text=r"\#dc143c{Elimina elemento selezionato}"))
        
        # # ITEM 6 IMPORT --------------------------------------------------


        # # ITEM 7 EXPORT --------------------------------------------------
        s.context_menu["item7"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Export}"))
        s.context_menu["item7"].add_element("save_single_plot", Bottone_Push("50%w", "80px", "cu", "70%w", "40px", function=self.bott_calls.save_file, text="Salva grafico"))
        # # ITEM 7 EXPORT --------------------------------------------------


        # # ITEM 8 STATSISTIC ----------------------------------------------
        s.context_menu["item8"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Statistica}"))
        # # ITEM 8 STATSISTIC ----------------------------------------------


        # # ITEM 9 INTERPOLATION -------------------------------------------
        s.context_menu["item9"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Interpolazioni}"))
        
        s.context_menu["item9"].add_element("min_x", Entrata("40%w", "100px", "cu", "30%w", "-*h", text="", title="Min. X", solo_numeri=True))
        s.context_menu["item9"].add_element("max_x", Entrata("40%w", "180px", "cd", "30%w", "-*h", text="", title="Max. X", solo_numeri=True))
        s.context_menu["item9"].add_element("intersection", Bottone_Toggle("10%w", "250px", "ld", "30px", "30px", text="Find intersection X"))
        s.context_menu["item9"].add_element("compute", Bottone_Push("90%w", "100px", "ru", "30%w", "80px", text="Compute", function=self.bott_calls.change_state))
        s.context_menu["item9"].add_element("output", Label_Text("5%w", "320px", "lu", "90%w", "-*h", text="Interpolation results:\n---"))
        # # ITEM 9 INTERPOLATION -------------------------------------------


        # # ITEM 10 MULTI-PLOTS --------------------------------------------
        s.context_menu["item10"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Multi-Plots}"))
        # # ITEM 10 MULTI-PLOTS --------------------------------------------


        # # ITEM 11 METADATA -----------------------------------------------
        s.context_menu["item11"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Metadata}"))
        s.context_menu["item11"].add_element("molecule_input", Entrata("30%w", "100px", "lu", "67.5%w", "40px", "", "SMILE code"))
        s.context_menu["item11"].add_element("molecule_preview", Screen("50%w", "180px", "cu", "95%w", "95%w"))
        # # ITEM 11 METADATA -----------------------------------------------

        starting = 1
        stato_iniziale_tab = [False for _ in range(11)]
        stato_iniziale_tab[starting] = True        
        s.context_menu["main"].add_element("modes", RadioButton(x="73.5%w", y="40%h", anchor="ru", w="2.4%w", h="55%h", bg=array([30, 30, 30]), axis="y", cb_n=11, cb_s=stato_iniziale_tab, cb_t=["" for _ in range(11)], type_checkbox=False, w_button="2.4%w", h_button="2.4%w"))
        [bottone.load_texture(f"item{index + 1}") for index, bottone in enumerate(s.context_menu["main"].elements["modes"].toggles)]
        
        s.context_menu["main"].add_element("tools", RadioButton(x="0px", y="5%h", anchor="lu", w="2.4%w", h=f"{2.5*3}%w", bg=array([30, 30, 30]), axis="y", cb_n=3, cb_s=[0, 0, 0], cb_t=["" for _ in range(3)], type_checkbox=False, w_button="2.4%w", h_button="2.4%w"))
        [bottone.load_texture(f"tool{index + 1}") for index, bottone in enumerate(s.context_menu["main"].elements["tools"].toggles)]

        s.context_menu["main"].add_element("reset_zoom", Bottone_Push(anchor=("cu cd (0px) (10px)", s.context_menu["main"].elements["tools"]), w="2.4%w", h="2.4%w", function=BottoniCallbacks.change_state))
        s.context_menu["main"].elements["reset_zoom"].load_texture(f"tool4")


        def set_active_tab():
            for index, state in enumerate(self.scene["main"].context_menu["main"].elements["modes"].cb_s):
                self.scene["main"].context_menu[f"item{index + 1}"].hide_plus_children(not state)
                self.scene["main"].context_menu[f"item{index + 1}"].hide_elements()

                if not self.scene["main"].context_menu[f"item{index + 1}"].hide and not self.scene["main"].context_menu[f"item{index + 1}"].inizializzato:
                    self.scene["main"].context_menu[f"item{index + 1}"].inizializzato = True
                    self.scene["main"].context_menu[f"item{index + 1}"].update_window_change()


        def hide_UI_element_with_toggle_legend_section():
            
            if self.scene["main"].context_menu["main"].elements["modes"].cb_s[4]:
                stato = not self.scene["main"].context_menu["item5"].elements["show_legend"].state_toggle
                stato2 = not self.scene["main"].context_menu["item5"].elements["show_legend_background"].state_toggle


                self.scene["main"].context_menu["item5"].elements["legend_color_background"].hide_plus_children(stato or stato2)
                self.scene["main"].context_menu["item5"].elements["transparent_background"].hide_plus_children(stato or stato2)
                self.scene["main"].context_menu["item5"].elements["blur_strenght"].hide_plus_children(stato or stato2)
                
                self.scene["main"].context_menu["item5"].elements["x_legend"].hide_plus_children(stato)
                self.scene["main"].context_menu["item5"].elements["y_legend"].hide_plus_children(stato)
                self.scene["main"].context_menu["item5"].elements["font_size_legend"].hide_plus_children(stato)
                self.scene["main"].context_menu["item5"].elements["show_legend_background"].hide_plus_children(stato)
                self.scene["main"].context_menu["item5"].elements["show_icons"].hide_plus_children(stato)

                self.scene["main"].context_menu["item5"].elements["match_color_text"].hide_plus_children(stato)
                
                stato2 = self.scene["main"].context_menu["item5"].elements["match_color_text"].state_toggle

                self.scene["main"].context_menu["item5"].elements["color_text"].hide_plus_children(stato or stato2)



        def hide_UI_element_with_toggle_plot_section():

            if self.scene["main"].context_menu["main"].elements["modes"].cb_s[1]:

                if not self.scene["main"].context_menu["item2"].elements["scatter_toggle"].state_toggle:
                    self.scene["main"].context_menu["item2"].elements["scatter_size"].hide_plus_children(True)
                    self.scene["main"].context_menu["item2"].elements["colore_scatter"].hide_plus_children(True)
                else:
                    self.scene["main"].context_menu["item2"].elements["scatter_size"].hide_plus_children(False)
                    self.scene["main"].context_menu["item2"].elements["colore_scatter"].hide_plus_children(False)

                if not self.scene["main"].context_menu["item2"].elements["function_toggle"].state_toggle:
                    self.scene["main"].context_menu["item2"].elements["function_size"].hide_plus_children(True)
                    self.scene["main"].context_menu["item2"].elements["colore_function"].hide_plus_children(True)
                    self.scene["main"].context_menu["item2"].elements["dashed"].hide_plus_children(True)
                else:
                    self.scene["main"].context_menu["item2"].elements["function_size"].hide_plus_children(False)
                    self.scene["main"].context_menu["item2"].elements["colore_function"].hide_plus_children(False)
                    self.scene["main"].context_menu["item2"].elements["dashed"].hide_plus_children(False)


        def remove_selected_element():

            if self.scene["main"].context_menu["item6"].elements["remove_element_selected"].flag_foo:
                self.scene["main"].context_menu["item6"].elements["remove_element_selected"].flag_foo = False
                self.scene["main"].context_menu["main"].elements["elenco_plots"].remove_selected_item()


        def hide_overlap_normalization():

            if not self.scene["main"].context_menu["item1"].elements["norma_perc"].cb_s[0]:
                self.scene["main"].context_menu["item1"].elements["overlap"].hide_plus_children(True)
                self.scene["main"].context_menu["item1"].elements["overlap"].state_toggle = True
            else:
                self.scene["main"].context_menu["item1"].elements["overlap"].hide_plus_children(False)
                


        s.functions.append(set_active_tab)
        s.functions.append(hide_UI_element_with_toggle_plot_section)
        s.functions.append(hide_UI_element_with_toggle_legend_section)
        s.functions.append(hide_overlap_normalization)
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
        self.context_menu: dict[str, ContextMenu] = {}
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
        [dropmenu.disegnami(logica) for indice, dropmenu in self.context_menu.items()]
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


            for indice, dropmenu in self.context_menu.items():
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