import pygame
import os
from numpy import array
from time import perf_counter

from GRAFICA._modulo_elementi_grafici import Label_Text, Bottone_Push, Bottone_Toggle, RadioButton, Entrata, Scroll, ColorPicker, ContextMenu, BaseElement, Screen, Palette, Collapsable_Window
from GRAFICA._modulo_bottoni_callbacks import BottoniCallbacks

NON_ESEGUIRE = False
if NON_ESEGUIRE:
    from GRAFICA._modulo_UI import Logica



class Colors:
    def __init__(self):
        self.perano = [148, 177, 255]   #94b1ff 
        self.cremisi = [220, 20, 60]    #dc143c 



class Costruttore:
    def __init__(self, screen, width, height, font_size) -> None:

        self.screen: pygame.Surface = screen
        self.bg_def = (40, 40, 40)

        self.scene: dict[str, Scena] = {}
        
        self.pappardella_Costruttore = {
            "screen": self.screen,
            "bg_def": self.bg_def,
            "x_screen": width,
            "y_screen": height,
            "font_size": font_size
        }

        BaseElement._init_scene(self.pappardella_Costruttore)

        self.bott_calls = BottoniCallbacks()

        self.costruisci_main()
        self.costruisci_main_plot()


    def recalc(self, new_w, new_h):

        self.pappardella_Costruttore["x_screen"] = new_w
        self.pappardella_Costruttore["y_screen"] = new_h

        BaseElement._init_scene(self.pappardella_Costruttore)
        
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
        
        s.context_menu["main"].add_element("settings", ContextMenu(x="50%w", y="50%h", w="30%w", h="80%h", anchor="cc"))
        
        s.context_menu["main"].elements["settings"].add_window("scatter_info", Collapsable_Window(x="1%w", y="1%h", w="98%w", h="20%h", anchor="lu", bg=[27, 27, 27], text="scatter info"))
        s.context_menu["main"].elements["settings"].add_window("line_info", Collapsable_Window(w="98%w", h="20%h", anchor=("lu ld (0px) (1%h)", s.context_menu["main"].elements["settings"].windows["scatter_info"]), bg=[27, 27, 27], text="line info"))
        s.context_menu["main"].elements["settings"].add_window("gradient_info", Collapsable_Window(w="98%w", h="20%h", anchor=("lu ld (0px) (1%h)", s.context_menu["main"].elements["settings"].windows["line_info"]), bg=[27, 27, 27], text="gradient info"))
        s.context_menu["main"].elements["settings"].add_window("metadata_info", Collapsable_Window(w="98%w", h="20%h", anchor=("lu ld (0px) (1%h)", s.context_menu["main"].elements["settings"].windows["gradient_info"]), bg=[27, 27, 27], text="metadata info"))
        
        s.context_menu["main"].elements["settings"].add_element("bottone1", Bottone_Toggle(w="10%w", h="10%h", anchor="cc", x="50%w", y="35%h"), window="line_info")
        s.context_menu["main"].elements["settings"].add_element("bottone2", Bottone_Toggle(w="10%w", h="10%h", anchor="cc", x="50%w", y="55%h"), window="gradient_info")


    
    def costruisci_main_plot(self):
        
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

        s.context_menu["main"].add_element("elenco_plots1D", Scroll(x="73.5%w", y="5%h", anchor="lu", w="26%w", h="33%h", text="Grafici 1D caricati"))
        s.context_menu["main"].add_element("elenco_plots2D", Scroll(x="73.5%w", y="5%h", anchor="lu", w="26%w", h="33%h", text="Grafici 2D caricati"))
        s.context_menu["main"].add_element("elenco_metadata", Scroll(x="73.5%w", y="5%h", anchor="lu", w="26%w", h="33%h", text="Elenco metadata"))

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
        s.context_menu["item1"].add_window("wind1", Collapsable_Window(x="1%w", y="150px", w="98%w", h="310px", anchor="lu", bg=[20, 20, 20], text="Canvas proportions (size)", closed=1))
        s.context_menu["item1"].add_window("wind2", Collapsable_Window(w="98%w", h="270px", anchor=("lu ld (0px) (10px)", s.context_menu["item1"].windows["wind1"]), bg=[20, 20, 20], text="Canvas colors", closed=1))
        s.context_menu["item1"].add_window("wind3", Collapsable_Window(w="98%w", h="240px", anchor=("lu ld (0px) (10px)", s.context_menu["item1"].windows["wind2"]), bg=[20, 20, 20], text="Normalization and overlapping", closed=1))
        
        s.context_menu["item1"].add_element("plot_mode", RadioButton("50%w", "120px", "cd", "35%w", "50px", "x", cb_n=2, cb_s=[1, 0], cb_t=["1D", "2D"], w_button="17.5%w", h_button="50px", type_checkbox=False, always_one_active=True))
        
        s.context_menu["item1"].add_element("w_plot_area", Entrata("75%w", "220px", "lu", "20%w", "30px", text="0.8", title="larghezza plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999), window="wind1")
        s.context_menu["item1"].add_element("h_plot_area", Entrata("75%w", "255px", "lu", "20%w", "30px", text="0.8", title="altezza plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999), window="wind1")
        s.context_menu["item1"].add_element("size_plot_area", Entrata("75%w", "220px", "lu", "20%w", "30px", text="0.8", title="dimensione plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999), window="wind1")
        s.context_menu["item1"].add_element("x_plot_area", Entrata("75%w", "305px", "lu", "20%w", "30px", text="0.15", title="X plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999), window="wind1")
        s.context_menu["item1"].add_element("y_plot_area", Entrata("75%w", "340px", "lu", "20%w", "30px", text="0.1", title="Y plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999), window="wind1")
        
        s.context_menu["item1"].add_element("mantain_prop", Bottone_Toggle("25%w", "415px", "cc", "30px", "30px", False, True, "Mantain axis proportions"), window="wind1")
        
        s.context_menu["item1"].add_element("tema_chiaro", Bottone_Push("30%w", "580px", "cc", "33%w", "50px", self.bott_calls.change_state, "Tema chiaro"), window="wind2")
        s.context_menu["item1"].add_element("tema_scuro", Bottone_Push("70%w", "580px", "cc", "33%w", "50px", self.bott_calls.change_state, "Tema scuro"), window="wind2")
        s.context_menu["item1"].add_element("plot_area_bg", ColorPicker(s.palette_popup, "0", "30%w", "650px", "cc", "30%w", "40px", [50, 50, 50], bg=[50, 50, 50], text="Color plot area"), window="wind2")
        s.context_menu["item1"].add_element("canvas_area_bg", ColorPicker(s.palette_popup, "1", "30%w", "700px", "cc", "30%w", "40px", [40, 40, 40], bg=[50, 50, 50], text="Color background"), window="wind2")
        
        s.context_menu["item1"].add_element("norma_perc", RadioButton("50%w", "845px", "cc", "70%w", "50px", "x", cb_n=2, cb_s=[0, 0], cb_t=["[0..1]", "[%]"], type_checkbox=0, w_button="35%w", h_button="50px"), window="wind3")
        s.context_menu["item1"].add_element("overlap", Bottone_Toggle("50%w", "920px", "cc", "35%w", "50px", True, False, "Plots Overlap"), window="wind3")
        
        # # ITEM 1 GEOMETRY ------------------------------------------------
        
        
        # # ITEM 2 PLOTS ---------------------------------------------------
        s.context_menu["item2"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", w="-*w", h="-*h", text=r"\#88dd88{Impostazioni base Grafici 1D}"))
        s.context_menu["item2"].add_element("plot_name", Entrata("20%w", "90px", "lu", "75%w", "30px", text="", title="Name: "))
        
        s.context_menu["item2"].add_window("wind1", Collapsable_Window(x="1%w", y="150px", w="98%w", h="200px", anchor="lu", bg=[20, 20, 20], text="Scatter settings", closed=1))
        s.context_menu["item2"].add_window("wind2", Collapsable_Window(w="98%w", h="320px", anchor=("lu ld (0px) (10px)", s.context_menu["item2"].windows["wind1"]), bg=[20, 20, 20], text="Function settings", closed=1))
        s.context_menu["item2"].add_window("wind3", Collapsable_Window(w="98%w", h="200px", anchor=("lu ld (0px) (10px)", s.context_menu["item2"].windows["wind2"]), bg=[20, 20, 20], text="Gradient", closed=1))
        s.context_menu["item2"].add_window("wind4", Collapsable_Window(w="98%w", h="150px", anchor=("lu ld (0px) (10px)", s.context_menu["item2"].windows["wind3"]), bg=[20, 20, 20], text="Column selection", closed=1))
    

        s.context_menu["item2"].add_element("scatter_size", Entrata("55%w", "225px", "lu", "10%w", "30px", text="4", title="size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=1, num_valore_massimo=50), window="wind1")
        s.context_menu["item2"].add_element("scatter_border", Entrata("95%w", "225px", "ru", "10%w", "30px", text="0", title="width", lunghezza_max=2, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=9), window="wind1")
        s.context_menu["item2"].add_element("function_size", Entrata("75%w", "450px", "lu", "10%w", "30px", text="1", title="size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=1, num_valore_massimo=32), window="wind2")
        s.context_menu["item2"].add_element("dashed_density", Entrata("75%w", "550px", "lu", "10%w", "30px", text="21", title="N° traits", lunghezza_max=3, solo_numeri=True, num_valore_minimo=3, num_valore_massimo=101), window="wind2")

        s.context_menu["item2"].add_element("scatter_toggle", Bottone_Toggle("40%w", "225px", "ru", "30px", "30px", text="Toggle scatter", type_checkbox=True, text_on_right=False, state=True), window="wind1")
        s.context_menu["item2"].add_element("function_toggle", Bottone_Toggle("40%w", "450px", "ru", "30px", "30px", text="Toggle function", type_checkbox=True, text_on_right=False, state=True), window="wind2")
        s.context_menu["item2"].add_element("errorbar", Bottone_Toggle("40%w", "500px", "ru", "30px", "30px", text="Toggle errors", type_checkbox=True, text_on_right=False, state=True), window="wind2")
        s.context_menu["item2"].add_element("dashed", Bottone_Toggle("40%w", "550px", "ru", "30px", "30px", text="Dashed line", type_checkbox=True, text_on_right=False, state=True), window="wind2")
        
        s.context_menu["item2"].add_element("colore_function", ColorPicker(s.palette_popup, "2", "30%w", "630px", "cc", "30%w", "40px", [0, 0, 0], bg=[50, 50, 50], text="Colore function"), window="wind2")
        s.context_menu["item2"].add_element("colore_scatter", ColorPicker(s.palette_popup, "3", "30%w", "305px", "cc", "30%w", "40px", [0, 0, 0], bg=[50, 50, 50], text="Colore scatter"), window="wind1")
    
        s.context_menu["item2"].add_element("gradient", Bottone_Toggle("40%w", "770px", "ru", "30px", "30px", 0, text="Gradient", text_on_right=0), window="wind3")
        s.context_menu["item2"].add_element("grad_mode", RadioButton("90%w", "770px", "ru", "35%w", "80px", axis="y", cb_n=2, cb_s=[0, 1], cb_t=["Horizontal", "Vertical"], type_checkbox=False, w_button="35%w", h_button="40px"), window="wind3")
        
        s.context_menu["item2"].add_element("add_second_axis", Bottone_Toggle(w="30px", h="30px", anchor=("lu ld (10px) (30px)", s.context_menu["item2"].windows["wind4"]), state=0, text="Add to the second Y axis"))
        
        s.context_menu["item2"].add_element("column_x", Entrata("25%w", "970px", "cu", "5.5%w", "30px", text="0", title="X column", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=101), window="wind4")
        s.context_menu["item2"].add_element("column_y", Entrata("60%w", "970px", "cu", "5.5%w", "30px", text="0", title="Y column", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=101), window="wind4")
        s.context_menu["item2"].add_element("column_ey", Entrata("95%w", "970px", "cu", "5.5%w", "30px", text="0", title="Ey column", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=101), window="wind4")

        ################

        s.context_menu["item2"].add_element("_title_drop_menu_base2D", Label_Text("50%w", "10px", "cu", w="-*w", h="-*h", text=r"\#88dd88{Impostazioni base Grafici 2D}"))
        s.context_menu["item2"].add_element("plot_name2D", Entrata("20%w", "90px", "lu", "75%w", "30px", text="", title="Name: "))
        
        s.context_menu["item2"].add_window("wind2D_1", Collapsable_Window(x="1%w", y="150px", w="98%w", h="150px", anchor="lu", bg=[20, 20, 20], text="Spacing", closed=1, group=2))
        s.context_menu["item2"].add_window("wind2D_2", Collapsable_Window(w="98%w", h="200px", anchor=("lu ld (0px) (10px)", s.context_menu["item2"].windows["wind2D_1"]), bg=[20, 20, 20], text="Color map", closed=1, group=2))
        s.context_menu["item2"].add_window("wind2D_3", Collapsable_Window(w="98%w", h="150px", anchor=("lu ld (0px) (10px)", s.context_menu["item2"].windows["wind2D_2"]), bg=[20, 20, 20], text="Axes Flip", closed=1, group=2))
        
        s.context_menu["item2"].add_element("spacing_x", Entrata("95%w", "215px", "ru", "30%w", "30px", text="1", title="Spacing X", lunghezza_max=13, solo_numeri=True, num_valore_minimo=1e-10, num_valore_massimo=1e10), window="wind2D_1")
        s.context_menu["item2"].add_element("spacing_y", Entrata("95%w", "250px", "ru", "30%w", "30px", text="1", title="Spacing Y", lunghezza_max=13, solo_numeri=True, num_valore_minimo=1e-10, num_valore_massimo=1e10), window="wind2D_1")
        
        s.context_menu["item2"].add_element("colore_base1", ColorPicker(s.palette_popup, "2", "30%w", "400px", "cc", "30%w", "40px", [0, 0, 0], bg=[50, 50, 50], text="Colore estremo LOW"), window="wind2D_2")
        s.context_menu["item2"].add_element("colore_base2", ColorPicker(s.palette_popup, "3", "30%w", "455px", "cc", "30%w", "40px", [220, 20, 60], bg=[50, 50, 50], text="Colore estremo HIGH"), window="wind2D_2")
        
        s.context_menu["item2"].add_element("flip_y", Bottone_Toggle("80%w", "600px", "ru", "30px", "30px", 0, text="Flip Y axis", text_on_right=0), window="wind2D_3")
        s.context_menu["item2"].add_element("flip_x", Bottone_Toggle("40%w", "600px", "ru", "30px", "30px", 0, text="Flip X axis", text_on_right=0), window="wind2D_3")
        # # ITEM 2 PLOTS ---------------------------------------------------


        # # ITEM 3 AX LABELS -----------------------------------------------
        # s.context_menu["item3"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", w="-*w", h="-*h", text=r"\#88dd88{Impostazioni base Label}"))
        s.context_menu["item3"].add_window("wind1", Collapsable_Window(x="1%w", y="10px", w="98%w", h="270px", anchor="lu", bg=[20, 20, 20], text="Labels text", closed=1))
        s.context_menu["item3"].add_window("wind2", Collapsable_Window(w="98%w", h="250px", anchor=("lu ld (0px) (10px)", s.context_menu["item3"].windows["wind1"]), bg=[20, 20, 20], text="Font", closed=1))
        s.context_menu["item3"].add_window("wind3", Collapsable_Window(w="98%w", h="320px", anchor=("lu ld (0px) (10px)", s.context_menu["item3"].windows["wind2"]), bg=[20, 20, 20], text="Text colors", closed=1))
        s.context_menu["item3"].add_window("wind4", Collapsable_Window(w="98%w", h="180px", anchor=("lu ld (0px) (10px)", s.context_menu["item3"].windows["wind3"]), bg=[20, 20, 20], text="Projection labels", closed=1))
        
        s.context_menu["item3"].add_element("text_title", Entrata("50%w", "100px", "lu", "45%w", "30px", text="Title", title="Title text"), window="wind1")
        s.context_menu["item3"].add_element("text_label_x", Entrata("50%w", "150px", "lu", "45%w", "30px", text="X axis", title="Label text X"), window="wind1")
        s.context_menu["item3"].add_element("text_label_y", Entrata("50%w", "185px", "lu", "45%w", "30px", text="Y axis", title="Y"), window="wind1")
        s.context_menu["item3"].add_element("text_label_2y", Entrata("50%w", "220px", "lu", "45%w", "30px", text="2°Y axis", title="2°Y"), window="wind1")
        
        s.context_menu["item3"].add_element("font_size_title", Entrata("75%w", "355px", "lu", "20%w", "30px", text="48", title="Title font size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128), window="wind2")
        s.context_menu["item3"].add_element("font_size_label_x", Entrata("75%w", "405px", "lu", "20%w", "30px", text="48", title="Label font size X", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128), window="wind2")
        s.context_menu["item3"].add_element("font_size_label_y", Entrata("75%w", "440px", "lu", "20%w", "30px", text="48", title="Y", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128), window="wind2")
        s.context_menu["item3"].add_element("font_size_label_2y", Entrata("75%w", "475px", "lu", "20%w", "30px", text="48", title="2°Y", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128), window="wind2")
        
        s.context_menu["item3"].add_element("label_title_color", ColorPicker(s.palette_popup, "4", "50%w", "650px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore titolo"), window="wind3")
        s.context_menu["item3"].add_element("label_x_color", ColorPicker(s.palette_popup, "5", "50%w", "720px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore label X"), window="wind3")
        s.context_menu["item3"].add_element("label_y_color", ColorPicker(s.palette_popup, "6", "50%w", "770px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore label Y"), window="wind3")
        s.context_menu["item3"].add_element("label_2y_color", ColorPicker(s.palette_popup, "7", "50%w", "820px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore label 2Y"), window="wind3")
        
        s.context_menu["item3"].add_element("show_coords_projection", Bottone_Toggle("95%w", "950px", "ru", "30px", "30px", text="Mostra proiezione coords", state=True, type_checkbox=True, text_on_right=False), window="wind4")
        s.context_menu["item3"].add_element("show_coords_value", Bottone_Toggle("95%w", "990px", "ru", "30px", "30px", text="Mostra valore coords", state=True, type_checkbox=True, text_on_right=False), window="wind4")
        # # ITEM 3 AX LABELS -----------------------------------------------
        

        # # ITEM 4 AXES ----------------------------------------------------
        # s.context_menu["item4"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", w="-*w", h="-*h", text=r"\#88dd88{Impostazioni base Assi}"))
        s.context_menu["item4"].add_window("wind1", Collapsable_Window(x="1%w", y="10px", w="98%w", h="180px", anchor="lu", bg=[20, 20, 20], text="More settings", closed=1))
        s.context_menu["item4"].add_window("wind2", Collapsable_Window(w="98%w", h="180px", anchor=("lu ld (0px) (10px)", s.context_menu["item4"].windows["wind1"]), bg=[20, 20, 20], text="Round precision", closed=1))
        s.context_menu["item4"].add_window("wind3", Collapsable_Window(w="98%w", h="180px", anchor=("lu ld (0px) (10px)", s.context_menu["item4"].windows["wind2"]), bg=[20, 20, 20], text="Grid", closed=1))
        s.context_menu["item4"].add_window("wind4", Collapsable_Window(w="98%w", h="180px", anchor=("lu ld (0px) (10px)", s.context_menu["item4"].windows["wind3"]), bg=[20, 20, 20], text="Ax Formatting", closed=1))
        s.context_menu["item4"].add_window("wind5", Collapsable_Window(w="98%w", h="470px", anchor=("lu ld (0px) (10px)", s.context_menu["item4"].windows["wind4"]), bg=[20, 20, 20], text="Colori", closed=1))
        s.context_menu["item4"].add_window("wind6", Collapsable_Window(w="98%w", h="180px", anchor=("lu ld (0px) (10px)", s.context_menu["item4"].windows["wind5"]), bg=[20, 20, 20], text="Positioning", closed=1))
        s.context_menu["item4"].add_window("wind7", Collapsable_Window(w="98%w", h="130px", anchor=("lu ld (0px) (10px)", s.context_menu["item4"].windows["wind6"]), bg=[20, 20, 20], text="Font size", closed=1))
        
        s.context_menu["item4"].add_element("second_y_axis", Bottone_Toggle("70%w", "140px", "cd", "35%w", "50px", False, False, "Toggle 2° Y axis"), window="wind1")
        s.context_menu["item4"].add_element("invert_x_axis", Bottone_Toggle("30%w", "140px", "cd", "35%w", "50px", False, False, "Invert X axis"), window="wind1")

        s.context_menu["item4"].add_element("round_x", Entrata("75%w", "250px", "lu", "20%w", "30px", text="2", title="Round ticks X:", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=12), window="wind2")
        s.context_menu["item4"].add_element("round_y", Entrata("75%w", "285px", "lu", "20%w", "30px", text="2", title="Y:", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=12), window="wind2")
        s.context_menu["item4"].add_element("round_2y", Entrata("75%w", "320px", "lu", "20%w", "30px", text="2", title="2°Y:", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=12), window="wind2")
        
        s.context_menu["item4"].add_element("show_grid_x", Bottone_Toggle("95%w", "425px", "ru", "30px", "30px", text="Mostra griglia X", state=True, type_checkbox=True, text_on_right=False), window="wind3")
        s.context_menu["item4"].add_element("show_grid_y", Bottone_Toggle("95%w", "460px", "ru", "30px", "30px", text="Mostra griglia Y", state=True, type_checkbox=True, text_on_right=False), window="wind3")
        s.context_menu["item4"].add_element("show_grid_2y", Bottone_Toggle("95%w", "495px", "ru", "30px", "30px", text="Mostra griglia 2°Y", state=True, type_checkbox=True, text_on_right=False), window="wind3")
        
        s.context_menu["item4"].add_element("formatting_x", Bottone_Toggle("95%w", "625px", "ru", "30px", "30px", text="Not. Scien. asse X", type_checkbox=True, text_on_right=False), window="wind4")
        s.context_menu["item4"].add_element("formatting_y", Bottone_Toggle("95%w", "660px", "ru", "30px", "30px", text="Not. Scien. asse Y", type_checkbox=True, text_on_right=False), window="wind4")
        s.context_menu["item4"].add_element("formatting_2y", Bottone_Toggle("95%w", "695px", "ru", "30px", "30px", text="Not. Scien. asse 2°Y", type_checkbox=True, text_on_right=False), window="wind4")
        
        s.context_menu["item4"].add_element("ax_color_x", ColorPicker(s.palette_popup, "8", "30%w", "875px", "cc", "30%w", "40px", [70, 70, 70], bg=[50, 50, 50], text="Colore asse X"), window="wind5")
        s.context_menu["item4"].add_element("ax_color_y", ColorPicker(s.palette_popup, "9", "30%w", "925px", "cc", "30%w", "40px", [70, 70, 70], bg=[50, 50, 50], text="Colore asse Y"), window="wind5")
        s.context_menu["item4"].add_element("ax_color_2y", ColorPicker(s.palette_popup, "10", "30%w", "980px", "cc", "30%w", "40px", [70, 70, 70], bg=[50, 50, 50], text="Colore asse 2°Y"), window="wind5")
        s.context_menu["item4"].add_element("tick_color_x", ColorPicker(s.palette_popup, "11", "30%w", "1070px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore values X"), window="wind5")
        s.context_menu["item4"].add_element("tick_color_y", ColorPicker(s.palette_popup, "12", "30%w", "1120px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore values Y"), window="wind5")
        s.context_menu["item4"].add_element("tick_color_2y", ColorPicker(s.palette_popup, "13", "30%w", "1170px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore values 2°Y"), window="wind5")
        
        s.context_menu["item4"].add_element("offset_x_label_y", Entrata("75%w", "1330px", "lu", "20%w", "30px", text="45", title="Offset X of ticks Y axis:", lunghezza_max=4, solo_numeri=True), window="wind6")
        s.context_menu["item4"].add_element("offset_y_label_x", Entrata("75%w", "1365px", "lu", "20%w", "30px", text="-27", title="Offset Y of ticks X axis:", lunghezza_max=4, solo_numeri=True), window="wind6")
        
        s.context_menu["item4"].add_element("size_ticks", Entrata("75%w", "1520px", "lu", "20%w", "30px", text="1", title="Font size ticks Y axis:", lunghezza_max=4, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=3), window="wind7")
        # # ITEM 4 AXES ----------------------------------------------------


        # # ITEM 5 LEGEND --------------------------------------------------
        s.context_menu["item5"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", w="-*w", h="-*h", text=r"\#88dd88{Impostazioni base Legenda}"))
    
        s.context_menu["item5"].add_window("wind1", Collapsable_Window(x="1%w", y="170px", w="98%w", h="180px", anchor="lu", bg=[20, 20, 20], text="Position and size", closed=1))
        s.context_menu["item5"].add_window("wind2", Collapsable_Window(w="98%w", h="280px", anchor=("lu ld (0px) (10px)", s.context_menu["item5"].windows["wind1"]), bg=[20, 20, 20], text="Background", closed=1))
        s.context_menu["item5"].add_window("wind3", Collapsable_Window(w="98%w", h="220px", anchor=("lu ld (0px) (10px)", s.context_menu["item5"].windows["wind2"]), bg=[20, 20, 20], text="Text and icons", closed=1))
        s.context_menu["item5"].add_window("wind4", Collapsable_Window(w="98%w", h="170px", anchor=("lu ld (0px) (10px)", s.context_menu["item5"].windows["wind3"]), bg=[20, 20, 20], text="2D marker", closed=1))
        

        s.context_menu["item5"].add_element("show_legend", Bottone_Toggle("95%w", "80px", "ru", "30px", "30px", text="\\#dfffdf{\\b{Mostra legenda}}", state=False, type_checkbox=True, text_on_right=False))

        s.context_menu["item5"].add_element("x_legend", Entrata("75%w", "205px", "lu", "20%w", "30px", text="0.5", title="X legend", lunghezza_max=5, solo_numeri=True, num_valore_minimo=-0.5, num_valore_massimo=1.5), window="wind1")
        s.context_menu["item5"].add_element("y_legend", Entrata("75%w", "240px", "lu", "20%w", "30px", text="0.5", title="Y legend", lunghezza_max=5, solo_numeri=True, num_valore_minimo=-0.5, num_valore_massimo=1.5), window="wind1")
        
        s.context_menu["item5"].add_element("font_size_legend", Entrata("75%w", "305px", "lu", "20%w", "30px", text="48", title="Legend font size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128), window="wind1")
        
        s.context_menu["item5"].add_element("show_legend_background", Bottone_Toggle("95%w", "400px", "ru", "30px", "30px", text="\\#dfffdf{\\b{Disegna bg}}", state=False, type_checkbox=True, text_on_right=False), window="wind2")
        s.context_menu["item5"].add_element("legend_color_background", ColorPicker(s.palette_popup, "14", "30%w", "480px", "cc", "30%w", "40px", [250, 250, 250], bg=[50, 50, 50], text="Color legend bg"), window="wind2")
        s.context_menu["item5"].add_element("transparent_background", Bottone_Toggle("95%w", "540px", "ru", "30px", "30px", text="Trasparenza bg", state=True, type_checkbox=True, text_on_right=False), window="wind2")
        s.context_menu["item5"].add_element("blur_strenght", Entrata("75%w", "580px", "lu", "20%w", "30px", text="6", title="Forza di blur", lunghezza_max=2, solo_numeri=True, num_valore_minimo=1, num_valore_massimo=12), window="wind2")
        
        s.context_menu["item5"].add_element("show_icons", Bottone_Toggle("95%w", "710px", "ru", "30px", "30px", text="Mostra icone", state=True, type_checkbox=True, text_on_right=False), window="wind3")
        s.context_menu["item5"].add_element("match_color_text", Bottone_Toggle("95%w", "750px", "ru", "30px", "30px", text="Match text color", state=True, type_checkbox=True, text_on_right=False), window="wind3")
        s.context_menu["item5"].add_element("color_text", ColorPicker(s.palette_popup, "15", "30%w", "810px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Color legend text"), window="wind3")
        
        s.context_menu["item5"].add_element("text_2D_plot", Entrata("75%w", "950px", "lu", "20%w", "30px", text=r"1\mum", title="Testo marker scala"), window="wind4")
        s.context_menu["item5"].add_element("size_scale_marker2D", Entrata("75%w", "990px", "lu", "20%w", "30px", text="1000", title="Valore marker scala", solo_numeri=True), window="wind4")
        # # ITEM 5 LEGEND --------------------------------------------------


        # # ITEM 6 IMPORT --------------------------------------------------
        s.context_menu["item6"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Import}"))
        
        s.context_menu["item6"].add_element("import_single_plot1D", Bottone_Push("50%w", "80px", "cu", "70%w", "40px", function=self.bott_calls.load_file, text="Carica singolo file 1D"))
        s.context_menu["item6"].add_element("import_multip_plot1D", Bottone_Push("50%w", "130px", "cu", "70%w", "40px", function=self.bott_calls.load_files, text="Carica file multipli 1D"))
        s.context_menu["item6"].add_element("import_single_plot2D", Bottone_Push("50%w", "200px", "cu", "70%w", "40px", function=self.bott_calls.load_file, text="Carica singolo file 2D"))
        s.context_menu["item6"].add_element("import_multip_plot2D", Bottone_Push("50%w", "250px", "cu", "70%w", "40px", function=self.bott_calls.load_files, text="Carica file multipli 2D"))
    
        s.context_menu["item6"].add_element("remove_element_selected", Bottone_Push("50%w", "320px", "cu", "70%w", "40px", function=self.bott_calls.change_state, text=r"\#dc143c{Elimina elemento selezionato}"))
        
        # # ITEM 6 IMPORT --------------------------------------------------


        # # ITEM 7 EXPORT --------------------------------------------------
        s.context_menu["item7"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Export}"))
        s.context_menu["item7"].add_element("save_single_plot", Bottone_Push("50%w", "80px", "cu", "70%w", "40px", function=self.bott_calls.save_file, text="Salva grafico"))
        # # ITEM 7 EXPORT --------------------------------------------------


        # # ITEM 8 STATSISTIC ----------------------------------------------
        s.context_menu["item8"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Statistica}"))
        # # ITEM 8 STATSISTIC ----------------------------------------------


        # # ITEM 9 INTERPOLATION -------------------------------------------
        s.context_menu["item9"].add_window("wind1", Collapsable_Window(x="1%w", y="10px", w="98%w", h="380px", anchor="lu", bg=[20, 20, 20], text="Derivata", closed=1))
        s.context_menu["item9"].add_window("wind2", Collapsable_Window(w="98%w", h="580px", anchor=("lu ld (0px) (10px)", s.context_menu["item9"].windows["wind1"]), bg=[20, 20, 20], text="Interpolazione", closed=1))
        s.context_menu["item9"].add_window("wind3", Collapsable_Window(w="98%w", h="880px", anchor=("lu ld (0px) (10px)", s.context_menu["item9"].windows["wind2"]), bg=[20, 20, 20], text="Custom curve", closed=1))
        
        # s.context_menu["item9"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Interpolazioni}"))
        
        s.context_menu["item9"].add_element("compute_derivative", Bottone_Push("50%w", "100px", "cu", "50%w", "50px", text="Compute derivative", function=self.bott_calls.change_state), window="wind1")
        s.context_menu["item9"].add_element("output_derivative", Label_Text("5%w", "200px", "lu", "90%w", "-*h", text="Derivative results:\n---"), window="wind1")
        
        s.context_menu["item9"].add_element("min_x", Entrata("40%w", "500px", "cu", "30%w", "-*h", text="", title="Min. X", solo_numeri=True), window="wind2")
        s.context_menu["item9"].add_element("max_x", Entrata("40%w", "580px", "cd", "30%w", "-*h", text="", title="Max. X", solo_numeri=True), window="wind2")
        s.context_menu["item9"].add_element("intersection", Bottone_Toggle("10%w", "650px", "ld", "30px", "30px", text="Find intersection X"), window="wind2")
        s.context_menu["item9"].add_element("compute", Bottone_Push("90%w", "500px", "ru", "30%w", "80px", text="Compute", function=self.bott_calls.change_state), window="wind2")
        s.context_menu["item9"].add_element("output", Label_Text("5%w", "720px", "lu", "90%w", "-*h", text="Interpolation results:\n---"), window="wind2")
        
        s.context_menu["item9"].add_element("curve_function", Entrata("95%w", "1075px", "ru", "60%w", "-*h", text="p[0]+p[1]*np.exp(p[2]+(p[3]*x))", title="Custom function"), window="wind3")
        s.context_menu["item9"].add_element("param_0", Entrata("12.5%w", "1150px", "lu", "15.5%w", "-*h", text="", title="p[0]"), window="wind3")
        s.context_menu["item9"].add_element("param_1", Entrata("12.5%w", "1200px", "lu", "15.5%w", "-*h", text="", title="p[1]"), window="wind3")
        s.context_menu["item9"].add_element("param_2", Entrata("12.5%w", "1250px", "lu", "15.5%w", "-*h", text="", title="p[2]"), window="wind3")
        s.context_menu["item9"].add_element("param_3", Entrata("12.5%w", "1300px", "lu", "15.5%w", "-*h", text="", title="p[3]"), window="wind3")
        
        s.context_menu["item9"].add_element("l_param_0", Label_Text("30%w", "1150px", "lu", "15.5%w", "-*h", text="-> NULL"), window="wind3")
        s.context_menu["item9"].add_element("l_param_1", Label_Text("30%w", "1200px", "lu", "15.5%w", "-*h", text="-> NULL"), window="wind3")
        s.context_menu["item9"].add_element("l_param_2", Label_Text("30%w", "1250px", "lu", "15.5%w", "-*h", text="-> NULL"), window="wind3")
        s.context_menu["item9"].add_element("l_param_3", Label_Text("30%w", "1300px", "lu", "15.5%w", "-*h", text="-> NULL"), window="wind3")
        
        s.context_menu["item9"].add_element("compute_custom_curve", Bottone_Push("90%w", "1150px", "ru", "30%w", "80px", text="Compute", function=self.bott_calls.change_state), window="wind3")
        s.context_menu["item9"].add_element("show_guess", Bottone_Toggle("95%w", "1275px", "ru", "30px", "30px", text="Show guess function", text_on_right=False), window="wind3")
        
        s.context_menu["item9"].add_element("info1", Label_Text("5%w", "1400px", "lu", "90%w", "-*h", text="Use 'p[x]' instead of the parameter you\nwant to calculate."), window="wind3")
        s.context_menu["item9"].add_element("info2", Label_Text("5%w", "1500px", "lu", "90%w", "-*h", text="Example: p[0] * x ** 2 + p[1] * x + p[2]\nGives -> \\i{ax\\^{2} + bx + c}"), window="wind3")
        s.context_menu["item9"].add_element("info3", Label_Text("5%w", "1600px", "lu", "90%w", "-*h", text="Curve fit results:\n---"), window="wind3")
        # # ITEM 9 INTERPOLATION -------------------------------------------


        # # ITEM 10 MULTI-PLOTS --------------------------------------------
        s.context_menu["item10"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Multi-Plots}"))
        # # ITEM 10 MULTI-PLOTS --------------------------------------------


        # # ITEM 11 METADATA -----------------------------------------------
        s.context_menu["item11"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Metadata}"))
        s.context_menu["item11"].add_element("molecule_input", Entrata("30%w", "100px", "lu", "67.5%w", "40px", "", "SMILE code"))
        s.context_menu["item11"].add_element("molecule_preview", Screen("50%w", "280px", "cu", "90%w", "90%w"))
        s.context_menu["item11"].elements["molecule_preview"].tavolozza.fill([25, 25, 25])

        s.context_menu["item11"].add_element("add_molecola", Bottone_Push("72.5%w", "220px", "cu", "50%w", "40px", text="Add empty mol.", function=self.bott_calls.change_state))
        s.context_menu["item11"].add_element("pos_x_molecola", Entrata("30%w", "170px", "lu", "10%w", "40px", "50", "Pos. X [%]"))
        s.context_menu["item11"].add_element("pos_y_molecola", Entrata("30%w", "220px", "lu", "10%w", "40px", "50", "Pos. Y [%]"))
        s.context_menu["item11"].add_element("dimensione_molecola", Entrata("82.5%w", "170px", "lu", "15%w", "40px", "1000", "Dimensione"))
        # # ITEM 11 METADATA -----------------------------------------------

        starting = 5
        stato_iniziale_tab = [False for _ in range(11)]
        stato_iniziale_tab[starting] = True        
        s.context_menu["main"].add_element("modes", RadioButton(x="73.5%w", y="40%h", anchor="ru", w="2.4%w", h="55%h", bg=array([30, 30, 30]), axis="y", cb_n=11, cb_s=stato_iniziale_tab, cb_t=["" for _ in range(11)], type_checkbox=False, w_button="2.4%w", h_button="2.4%w"))
        [bottone.load_texture(f"item{index + 1}") for index, bottone in enumerate(s.context_menu["main"].elements["modes"].toggles)]
        
        s.context_menu["main"].add_element("tools", RadioButton(x="0px", y="5%h", anchor="lu", w="2.4%w", h=f"{2.5*3}%w", bg=array([30, 30, 30]), axis="y", cb_n=3, cb_s=[0, 0, 0], cb_t=["" for _ in range(3)], type_checkbox=False, w_button="2.4%w", h_button="2.4%w"))
        [bottone.load_texture(f"tool{index + 1}") for index, bottone in enumerate(s.context_menu["main"].elements["tools"].toggles)]

        s.context_menu["main"].add_element("reset_zoom", Bottone_Push(anchor=("cu cd (0px) (10px)", s.context_menu["main"].elements["tools"]), w="2.4%w", h="2.4%w", function=BottoniCallbacks.change_state))
        s.context_menu["main"].elements["reset_zoom"].load_texture(f"tool4")


        def hide_plot_attributes_based_on_plot_mode():
            state_1D = self.scene["main"].context_menu["item1"].elements["plot_mode"].cb_s[0]
            state_2D = self.scene["main"].context_menu["item1"].elements["plot_mode"].cb_s[1]

            self.scene["main"].context_menu["item2"].elements["_title_drop_menu_base"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["plot_name"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["scatter_size"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["scatter_border"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["function_size"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["dashed_density"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["scatter_toggle"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["function_toggle"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["errorbar"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["dashed"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["colore_function"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["colore_scatter"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["gradient"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["grad_mode"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["add_second_axis"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["column_x"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["column_y"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].elements["column_ey"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].windows["wind1"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].windows["wind2"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].windows["wind3"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item2"].windows["wind4"].hide_plus_children(state_2D)

            self.scene["main"].context_menu["item2"].elements["_title_drop_menu_base2D"].hide_plus_children(state_1D)
            self.scene["main"].context_menu["item2"].elements["plot_name2D"].hide_plus_children(state_1D)
            self.scene["main"].context_menu["item2"].elements["colore_base1"].hide_plus_children(state_1D)
            self.scene["main"].context_menu["item2"].elements["colore_base2"].hide_plus_children(state_1D)
            self.scene["main"].context_menu["item2"].elements["flip_y"].hide_plus_children(state_1D)
            self.scene["main"].context_menu["item2"].elements["flip_x"].hide_plus_children(state_1D)
            self.scene["main"].context_menu["item2"].elements["spacing_x"].hide_plus_children(state_1D)
            self.scene["main"].context_menu["item2"].elements["spacing_y"].hide_plus_children(state_1D)
            self.scene["main"].context_menu["item2"].windows["wind2D_1"].hide_plus_children(state_1D)
            self.scene["main"].context_menu["item2"].windows["wind2D_2"].hide_plus_children(state_1D)
            self.scene["main"].context_menu["item2"].windows["wind2D_3"].hide_plus_children(state_1D)

            self.scene["main"].context_menu["item1"].elements["mantain_prop"].hide_plus_children(state_1D)

            if state_1D:
                self.scene["main"].context_menu["item1"].elements["mantain_prop"].state_toggle = not state_1D
        

        def hide_metadata_based_on_metadata_lenght():
            hide = not len(self.scene["main"].context_menu["main"].elements["elenco_metadata"].elementi) > 0
            self.scene["main"].context_menu["item11"].elements["molecule_input"].hide_plus_children(hide)
            self.scene["main"].context_menu["item11"].elements["pos_x_molecola"].hide_plus_children(hide)
            self.scene["main"].context_menu["item11"].elements["pos_y_molecola"].hide_plus_children(hide)
            self.scene["main"].context_menu["item11"].elements["dimensione_molecola"].hide_plus_children(hide)

        
        def hide_legend_attributes_based_on_plot_mode():
            state_1D = self.scene["main"].context_menu["item1"].elements["plot_mode"].cb_s[0]
            state_2D = self.scene["main"].context_menu["item1"].elements["plot_mode"].cb_s[1]

            self.scene["main"].context_menu["item5"].elements["show_icons"].hide_plus_children(state_2D)
            self.scene["main"].context_menu["item5"].elements["match_color_text"].hide_plus_children(state_2D)

            self.scene["main"].context_menu["item5"].elements["text_2D_plot"].hide_plus_children(state_1D)
            self.scene["main"].context_menu["item5"].elements["size_scale_marker2D"].hide_plus_children(state_1D)

            # flag or not this toggle (in 2D always OFF)
            if state_2D:
                self.scene["main"].context_menu["item5"].elements["match_color_text"].state_toggle = False
            


        def hide_UI_plot_area_size_based_on_proportions():
            state = self.scene["main"].context_menu["item1"].elements["mantain_prop"].state_toggle
            self.scene["main"].context_menu["item1"].elements["w_plot_area"].hide_plus_children(state)
            self.scene["main"].context_menu["item1"].elements["h_plot_area"].hide_plus_children(state)
            self.scene["main"].context_menu["item1"].elements["size_plot_area"].hide_plus_children(not state)



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
                
                self.scene["main"].context_menu["item5"].elements["text_2D_plot"].hide_plus_children(stato)
                self.scene["main"].context_menu["item5"].elements["size_scale_marker2D"].hide_plus_children(stato)

                self.scene["main"].context_menu["item5"].elements["match_color_text"].hide_plus_children(stato)
                
                stato2 = self.scene["main"].context_menu["item5"].elements["match_color_text"].state_toggle

                self.scene["main"].context_menu["item5"].elements["color_text"].hide_plus_children(stato or stato2)



        def hide_UI_element_with_toggle_plot_section():

            if self.scene["main"].context_menu["main"].elements["modes"].cb_s[1] and self.scene["main"].context_menu["item1"].elements["plot_mode"].cb_s[0]:

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
                if self.scene["main"].context_menu["main"].elements["elenco_plots1D"].hide:
                    self.scene["main"].context_menu["main"].elements["elenco_plots2D"].remove_selected_item()
                if self.scene["main"].context_menu["main"].elements["elenco_plots2D"].hide:
                    self.scene["main"].context_menu["main"].elements["elenco_plots1D"].remove_selected_item()


        def hide_overlap_normalization():

            if not self.scene["main"].context_menu["item1"].elements["norma_perc"].cb_s[0]:
                self.scene["main"].context_menu["item1"].elements["overlap"].hide_plus_children(True)
                self.scene["main"].context_menu["item1"].elements["overlap"].state_toggle = True
            else:
                self.scene["main"].context_menu["item1"].elements["overlap"].hide_plus_children(False)
                


        s.functions.append(set_active_tab)
        s.functions.append(hide_plot_attributes_based_on_plot_mode)
        s.functions.append(hide_legend_attributes_based_on_plot_mode)
        s.functions.append(hide_UI_element_with_toggle_plot_section)
        s.functions.append(hide_UI_element_with_toggle_legend_section)
        s.functions.append(hide_overlap_normalization)
        s.functions.append(remove_selected_element)
        s.functions.append(hide_UI_plot_area_size_based_on_proportions)
        s.functions.append(hide_metadata_based_on_metadata_lenght)


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