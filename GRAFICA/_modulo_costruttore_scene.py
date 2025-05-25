import pygame
import os
from numpy import array
from time import perf_counter

from GRAFICA._modulo_elementi_grafici import Label_Text, Bottone_Push, Bottone_Toggle, RadioButton, Entrata, Scroll, ColorPicker, ContextMenu, BaseElement, Screen, PopUp_color_palette_hard, PopUp_color_palette_easy, Collapsable_Window, Slider
from GRAFICA._modulo_bottoni_callbacks import BottoniCallbacks

NON_ESEGUIRE = False
if NON_ESEGUIRE:
    from GRAFICA._modulo_UI import Logica
    "\\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 9} | Std: 0}\n\\#777777{}"


class Colors:
    def __init__(self):
        self.perano = [148, 177, 255]   #94b1ff 
        self.cremisi = [220, 20, 60]    #dc143c 



class Costruttore:
    def __init__(self, screen, width, height, font_size) -> None:

        # init_sound = pygame.mixer.Sound("./TEXTURES/AUDIO_SC2/Battlecruiser_Pissed04.ogg")
        # init_sound.play()
        
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
            
            scena.pop_up_palette.update_window_change()
            scena.pop_up_palette_hard.update_window_change()


    def costruisci_main(self):
        self.scene["main"] = Scena()

        s = self.scene["main"]
        
        s.context_menu["main"] = ContextMenu(x="0px", y="0px", w="100%w", h="100%h", anchor="lu", bg=[30, 30, 30], scrollable=False)

        s.context_menu["main"].add_element("clock", Label_Text(x="100%w", y="100%h", w="-*w", h="-*h", anchor="rd", text="." * 22))
        s.context_menu["main"].add_element("memory", Label_Text(anchor=("rd ld (-0.7%w) (0px)", s.context_menu["main"].elements["clock"]), w="-*w", h="-*h", text="." * 22))
        s.context_menu["main"].add_element("battery", Label_Text(anchor=("rd ld (-0.7%w) (0px)", s.context_menu["main"].elements["memory"]), w="-*w", h="-*h", text="." * 8))
        s.context_menu["main"].add_element("fps", Label_Text(anchor=("rd ld (-0.7%w) (0px)", s.context_menu["main"].elements["battery"]), w="-*w", h="-*h", text="." * 13))
        s.context_menu["main"].add_element("cpu", Label_Text(anchor=("rd ld (-0.7%w) (0px)", s.context_menu["main"].elements["fps"]), w="-*w", h="-*h", text="." * 13))

        s.context_menu["main"].add_element("exit", Bottone_Push(x="100%w", y="0px", w="50px", h="50px", anchor="ru", text="X", function=self.bott_calls.exit))


    
    def costruisci_main_plot(self):
        
        self.scene["main"] = Scena()

        s = self.scene["main"]

        s.context_menu["main"] = ContextMenu(x="0px", y="0px", w="100%w", h="100%h", anchor="lu", bg=[30, 30, 30], scrollable=False, root=True)

        s.context_menu["main"].add_element("clock", Label_Text(x="100%w", y="100%h", w="-*w", h="-*h", anchor="rd", text="." * 22))
        s.context_menu["main"].add_element("memory", Label_Text(anchor=("rd ld (-0.7%w) (0px)", s.context_menu["main"].elements["clock"]), w="-*w", h="-*h", text="." * 22))
        s.context_menu["main"].add_element("battery", Label_Text(anchor=("rd ld (-0.7%w) (0px)", s.context_menu["main"].elements["memory"]), w="-*w", h="-*h", text="." * 8))
        s.context_menu["main"].add_element("fps", Label_Text(anchor=("rd ld (-0.7%w) (0px)", s.context_menu["main"].elements["battery"]), w="-*w", h="-*h", text="." * 13))
        s.context_menu["main"].add_element("cpu", Label_Text(anchor=("rd ld (-0.7%w) (0px)", s.context_menu["main"].elements["fps"]), w="-*w", h="-*h", text="." * 13))


        s.context_menu["main"].add_element("exit", Bottone_Push(x="100%w", y="2px", w="40px", h="40px", anchor="ru", text="X", function=self.bott_calls.exit, tooltip="Esci dal programma. \\#aaffaa{Shortcut: ESC + SPACE}"))
        s.context_menu["main"].add_element("open", Bottone_Push(x="0px", y="2px", w="3%w", h="40px", anchor="lu", text="Open", function=self.bott_calls.change_state, tooltip="Apre un file *.json \\#aaffaa{Shortcut: CTRL + O}"))
        s.context_menu["main"].add_element("save", Bottone_Push(x="3%w 5px", y="2px", w="3%w", h="40px", anchor="lu", text="Save", function=self.bott_calls.change_state, tooltip="Salva il tutto in un file *.json \\#aaffaa{Shortcut: CTRL + S}"))
        s.context_menu["main"].add_element("saveas", Bottone_Push(x="6%w 5px", y="2px", w="5%w", h="40px", anchor="lu", text="Save as", function=self.bott_calls.change_state, tooltip="Salva con nome tutto in un file *.json"))
        s.context_menu["main"].add_element("default", Bottone_Push(x="11%w 5px", y="2px", w="5%w", h="40px", anchor="lu", text="Default", function=self.bott_calls.change_state, tooltip="Salva la configurazione attuale come startup default file *.json\n\\#777777{Nel caso di errore o overwright accidentale, esiste un backup sotto /SETTINGS/default_backup.json}"))
        s.context_menu["main"].add_element("save_status", Label_Text(anchor=("lc rc (0.7%w) (0px)", s.context_menu["main"].elements["default"]), w="-*w", h="-*h", text=" " * 7))

        # # ----------------------------------------------------------------------------------------------------

        s.context_menu["main"].add_element("viewport", Screen(x="37.5%w", y="50%h", anchor="cc", w="65%w", h="90%h", latex_font=True, tooltip="Viewport del grafico. Quando viene salvata, l'immagine avrà sempre una larghezza di 4000px"))
        
        moltiplier = s.context_menu["main"].elements["viewport"].h / s.context_menu["main"].elements["viewport"].w

        s.context_menu["main"].add_element("renderer", Screen(f"{s.context_menu["main"].elements["viewport"].x}px", f"{s.context_menu["main"].elements["viewport"].y}px", anchor="lu", w="4000px", h=f"{4000 * moltiplier}px", latex_font=True, screenshot_type=True, show_tooltip=False))

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
        
        s.context_menu["item1"].add_element("plot_mode", RadioButton("50%w", "120px", "cd", "35%w", "50px", "x", cb_n=2, cb_s=[1, 0], cb_t=["1D", "2D"], cb_tooltips=["Modifica la modalità di visualizzazione in 1D: \\i{y = f(x)}", "Modifica la modalità di visualizzazione in 2D: \\i{immagine}"], w_button="17.5%w", h_button="50px", type_checkbox=False, always_one_active=True))
        
        s.context_menu["item1"].add_element("w_plot_area", Entrata("75%w", "220px", "lu", "20%w", "30px", text="0.975", title="larghezza plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999, tooltip="Indica la larghezza massima occupata dal grafico. \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 1} | Std: 0.8}\n\\#777777{La larghezza massima è riferita alla dimensione del lato del quadrato massimo inscritto dentro alla zona di disegno.}"), window="wind1")
        s.context_menu["item1"].add_element("h_plot_area", Entrata("75%w", "255px", "lu", "20%w", "30px", text="0.8", title="altezza plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999, tooltip="Indica l'altezza massima occupata dal grafico. \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 1} | Std: 0.8}\n\\#777777{L'altezza massima è riferita alla dimensione del lato del quadrato massimo inscritto dentro alla zona di disegno.}"), window="wind1")
        s.context_menu["item1"].add_element("size_plot_area", Entrata("75%w", "220px", "lu", "20%w", "30px", text="0.8", title="dimensione plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999, tooltip="Indica la dimensione massima occupata dal grafico (proporzioni fissate). \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 1} | Std: 0.8}\n\\#777777{Il valore massimo è riferito alla dimensione del lato del quadrato massimo inscritto dentro alla zona di disegno.}"), window="wind1")
        s.context_menu["item1"].add_element("x_plot_area", Entrata("75%w", "305px", "lu", "20%w", "30px", text="0.05", title="X plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999, tooltip="Indica la posizione X del lato superiore dal grafico. \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 1} | Std: 0.1}\n\\#777777{La posizione X massima è riferita alla dimensione del lato del quadrato massimo inscritto dentro alla zona di disegno.}"), window="wind1")
        s.context_menu["item1"].add_element("y_plot_area", Entrata("75%w", "340px", "lu", "20%w", "30px", text="0.1", title="Y plot area", lunghezza_max=5, solo_numeri=True, num_valore_minimo=0.001, num_valore_massimo=0.999, tooltip="Indica la posizione Y del lato sinistro dal grafico. \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 1} | Std: 0.15}\n\\#777777{La posizione Y massima è riferita alla dimensione del lato del quadrato massimo inscritto dentro alla zona di disegno.}"), window="wind1")
        
        s.context_menu["item1"].add_element("mantain_prop", Bottone_Toggle("25%w", "415px", "cc", "30px", "30px", False, True, "Mantain axis proportions", tooltip="Forza il mantenimento della scala 1:1 tra gli assi X e Y. \\i{Std: 0.15}\n\\#777777{Potrebbe essere necessario modificare lo spacing degli assi per vedere l'effetto.}"), window="wind1")
        
        s.context_menu["item1"].add_element("tema_chiaro", Bottone_Push("30%w", "580px", "cc", "33%w", "50px", self.bott_calls.change_state, "Tema chiaro", tooltip="Imposta tema chiaro del plot.\n\\#777777{Cambi applicati a: Sfondo Canvas, Sfondo Plot, Colore assi, Colore titolo, Colore Label, Colore griglia.}"), window="wind2")
        s.context_menu["item1"].add_element("tema_scuro", Bottone_Push("70%w", "580px", "cc", "33%w", "50px", self.bott_calls.change_state, "Tema scuro", tooltip="Imposta tema scuro del plot.\n\\#777777{Cambi applicati a: Sfondo Canvas, Sfondo Plot, Colore assi, Colore titolo, Colore Label, Colore griglia.}"), window="wind2")
        s.context_menu["item1"].add_element("plot_area_bg", ColorPicker("30%w", "650px", "cc", "30%w", "40px", [30, 30, 30], bg=[50, 50, 50], text="Color plot area", tooltip="Modifica il colore dello sfondo dell'area grafici.\n\\#777777{Consigliabile usare lo stesso colore qui e in 'Color background'}"), window="wind2")
        s.context_menu["item1"].add_element("canvas_area_bg", ColorPicker("30%w", "700px", "cc", "30%w", "40px", [30, 30, 30], bg=[50, 50, 50], text="Color background", tooltip="Modifica il colore di tutta la tavolozza.\n\\#777777{Consigliabile usare lo stesso colore qui e in 'Color plot area'}"), window="wind2") 
        
        s.context_menu["item1"].add_element("norma_perc", RadioButton("50%w", "845px", "cc", "70%w", "50px", "x", cb_n=2, cb_s=[0, 0], cb_t=["[0..1]", "[%]"], cb_tooltips=["Scala tutti i plot, forzando la scala da 0 a 1\n\\#ffaa00{NOTA: Necessario abilitare questa funzione per usare 'Plots Overlap'}", "Scala tutti i plot, forzando la scala da 0 a 100\n\\#ffaa00{NOTA: Questa funzione \\#dc143c{NON} abilita 'Plots Overlap'}"], type_checkbox=0, w_button="35%w", h_button="50px"), window="wind3")
        s.context_menu["item1"].add_element("overlap", Bottone_Toggle("50%w", "920px", "cc", "35%w", "50px", True, False, "Plots Overlap", tooltip="Permette la sovrapposizione dei grafici o stratificazione.\n\\#777777{BUG Conosciuti: 1) Altezza di un singolo grafico ~1 | 2) Crash improvvisi usando colonne di lettura diverse da: X0, Y1, EY2}"), window="wind3")
        
        # # ITEM 1 GEOMETRY ------------------------------------------------
        
        
        # # ITEM 2 PLOTS ---------------------------------------------------
        s.context_menu["item2"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", w="-*w", h="-*h", text=r"\#88dd88{Impostazioni base Grafici 1D}"))
        s.context_menu["item2"].add_element("plot_name", Entrata("20%w", "90px", "lu", "75%w", "30px", text="", title="Name: ", tooltip="Cambia il nome del grafico. La modifica sarà visibile nei plot selection e nella legenda.\n\\#dc143c{NOTA:} per modificare il valore della legenda, è necessario modificare il nome QUI."))
        
        s.context_menu["item2"].add_window("wind1", Collapsable_Window(x="1%w", y="150px", w="98%w", h="200px", anchor="lu", bg=[20, 20, 20], text="Scatter settings", closed=1))
        s.context_menu["item2"].add_window("wind2", Collapsable_Window(w="98%w", h="320px", anchor=("lu ld (0px) (10px)", s.context_menu["item2"].windows["wind1"]), bg=[20, 20, 20], text="Function settings", closed=1))
        s.context_menu["item2"].add_window("wind3", Collapsable_Window(w="98%w", h="200px", anchor=("lu ld (0px) (10px)", s.context_menu["item2"].windows["wind2"]), bg=[20, 20, 20], text="Gradient", closed=1))
        s.context_menu["item2"].add_window("wind4", Collapsable_Window(w="98%w", h="150px", anchor=("lu ld (0px) (10px)", s.context_menu["item2"].windows["wind3"]), bg=[20, 20, 20], text="Column selection", closed=1))
        s.context_menu["item2"].add_window("wind5", Collapsable_Window(w="98%w", h="180px", anchor=("lu ld (0px) (10px)", s.context_menu["item2"].windows["wind4"]), bg=[20, 20, 20], text="Scale / convert", closed=1))
    

        s.context_menu["item2"].add_element("scatter_size", Entrata("55%w", "225px", "lu", "10%w", "30px", text="4", title="size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=1, num_valore_massimo=50, tooltip="Imposta la dimensione dei pallini. \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 50} | Std: 4}"), window="wind1")
        s.context_menu["item2"].add_element("scatter_border", Entrata("95%w", "225px", "ru", "10%w", "30px", text="0", title="width", lunghezza_max=2, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=9, tooltip="Imposta lo spessore dei pallini. Questo genererà pallini sempre più sottili con numeri più piccoli. \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 9} | Std: 0}\n\\#777777{Valore pari a 0 verrà interpretato come pallino pieno}"), window="wind1")
        s.context_menu["item2"].add_element("function_size", Entrata("75%w", "450px", "lu", "10%w", "30px", text="2", title="size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=1, num_valore_massimo=32, tooltip="Imposta la dimensione del tratto. \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 32} | Std: 1}"), window="wind2")
        s.context_menu["item2"].add_element("dashed_density", Entrata("75%w", "550px", "lu", "10%w", "30px", text="21", title="N° traits", lunghezza_max=3, solo_numeri=True, num_valore_minimo=3, num_valore_massimo=101, tooltip="Imposta il numero di alternanze di tratteggio. \\i{\\#aaffaa{Min: 3} | \\#ffaaaa{Max: 101} | Std: 99}\n\\#777777{Consigliabile usare numeri dispari, numeri pari possono portare a comportamenti imprevedibili.}"), window="wind2")

        s.context_menu["item2"].add_element("scatter_toggle", Bottone_Toggle("40%w", "225px", "ru", "30px", "30px", text="Toggle scatter", type_checkbox=True, text_on_right=False, state=False, tooltip="Abilita la visualizzazione dei pallini nel plot attivo."), window="wind1")
        s.context_menu["item2"].add_element("function_toggle", Bottone_Toggle("40%w", "450px", "ru", "30px", "30px", text="Toggle function", type_checkbox=True, text_on_right=False, state=True, tooltip="Abilita la visualizzazione del tratto unico nel plot attivo."), window="wind2")
        s.context_menu["item2"].add_element("errorbar", Bottone_Toggle("40%w", "500px", "ru", "30px", "30px", text="Toggle errors", type_checkbox=True, text_on_right=False, state=True, tooltip="Se il plot importato possiede \\b{ALMENO} 3 colonne di dati, abilita la visualizzazione delle barre di errori.\n\\#777777{Il bottone avrà un leggero colore rosso o verde. Questo indicherà se è presente la 3° colonna di dati o meno.}"), window="wind2")
        s.context_menu["item2"].add_element("dashed", Bottone_Toggle("40%w", "550px", "ru", "30px", "30px", text="Dashed line", type_checkbox=True, text_on_right=False, state=True, tooltip="Abilita la visualizzazione di una linea tratteggiata al posto del tratto continuo.\n\\#777777{Richiede 'Toggle function' abilitato per funzionare.}"), window="wind2")
        
        s.context_menu["item2"].add_element("colore_function", ColorPicker("30%w", "630px", "cc", "30%w", "40px", [0, 0, 0], bg=[50, 50, 50], text="Colore function", tooltip="Imposta il colore del tratto continuo / tratteggiato.\n\\#777777{Il colore è randomico ad ogni caricamento di un nuovo plot, ma sarà sempre una tonalità più scura del colore dello scatter.}"), window="wind2")
        s.context_menu["item2"].add_element("colore_scatter", ColorPicker("30%w", "305px", "cc", "30%w", "40px", [0, 0, 0], bg=[50, 50, 50], text="Colore scatter", tooltip="Imposta il colore dello scatter.\n\\#777777{Il colore è randomico ad ogni caricamento di un nuovo plot, ma sarà sempre una tonalità più chiara del colore del tratto.}"), window="wind1")
    
        s.context_menu["item2"].add_element("gradient", Bottone_Toggle("40%w", "770px", "ru", "30px", "30px", 0, text="Gradient", text_on_right=0, tooltip="Abilita la visualizzazione del gradiente dell'area sottostante. \n\\#dc143c{Quest'opzione è molto pesante!} \\#777777{Considera di accenderla solo prima di renderizzare l'immagine}"), window="wind3")
        s.context_menu["item2"].add_element("grad_mode", RadioButton("90%w", "770px", "ru", "35%w", "80px", axis="y", cb_n=2, cb_s=[0, 1], cb_t=["Horizontal", "Vertical"], cb_tooltips=["Imposta il tipo di gradiente in: ORIZZONTALE. Più il valore Y si avvicina a 0, più il colore tende al trasparente.\n\\#777777{Nel caso di più plot con gradiente ORIZZONTALE attivo, solo il gradiente dell'ultimo grafico sarà renderizzato.}", "Imposta il tipo di gradiente in: VERTICALE. Più il \\DeltaY si avvicina a 0, più il colore tende al trasparente.\n\\#777777{Nel caso di più plot con gradiente VERTICALE attivo, è possibile sovrapporre aree più piccole su quelle più grandi.}"], type_checkbox=False, w_button="35%w", h_button="40px"), window="wind3")
        
        s.context_menu["item2"].add_element("column_x", Entrata("25%w", "970px", "cu", "5.5%w", "30px", text="0", title="X column", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=101, tooltip="Imposta la colonna selezionata di dati come valori X da riportare nel grafico. \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 101} | Std: 0}\n\\#777777{Valore massimo riportabile è il numero di colonne nel file.} \\#dc143c{TUTTI e 3 valori DEVONO essere diversi.}"), window="wind4")
        s.context_menu["item2"].add_element("column_y", Entrata("60%w", "970px", "cu", "5.5%w", "30px", text="0", title="Y column", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=101, tooltip="Imposta la colonna selezionata di dati come valori Y da riportare nel grafico. \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 101} | Std: 1}\n\\#777777{Valore massimo riportabile è il numero di colonne nel file.} \\#dc143c{TUTTI e 3 valori DEVONO essere diversi.}"), window="wind4")
        s.context_menu["item2"].add_element("column_ey", Entrata("95%w", "970px", "cu", "5.5%w", "30px", text="0", title="Ey column", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=101, tooltip="Imposta la colonna selezionata di dati come errori di Y da riportare nel grafico. \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 101} | Std: 2}\n\\#777777{Valore massimo riportabile è il numero di colonne nel file.} \\#dc143c{TUTTI e 3 valori DEVONO essere diversi.}"), window="wind4")

        s.context_menu["item2"].add_element("conversion_column", Entrata("75%w", "1130px", "lu", "20%w", "30px", text="0", title="Column to convert", num_valore_minimo=0, num_valore_massimo=999, lunghezza_max=4, solo_numeri=True, tooltip="Selezione la colonna interessata ad esser scalata / modificata. \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 9999} | Std: 0}"), window="wind5")
        s.context_menu["item2"].add_element("conversion_expression", Entrata("27%w", "1165px", "lu", "68%w", "30px", text="x = x", title="Expression:", tooltip="Imposta l'espressione di conversione. Utilizza la 'x' come variabile.\n\\#777777{Esempio 'x = x' non modifica nulla, 'x = x * 2' raddoppia tutti i valori.}"), window="wind5")
        
        s.context_menu["item2"].add_element("add_second_axis", Bottone_Toggle(w="30px", h="30px", anchor=("lu ld (10px) (30px)", s.context_menu["item2"].windows["wind5"]), state=0, text="Add to the second Y axis", tooltip="Aggiunge il plot al buffer di plot da renderizzare usando la scala del secondo asse Y.\n\\#ffaa00{NOTA: Necessario abilitare 'Toggle 2° Y axis' per vedere l'effetto.}"))

        ################

        s.context_menu["item2"].add_element("_title_drop_menu_base2D", Label_Text("50%w", "10px", "cu", w="-*w", h="-*h", text=r"\#88dd88{Impostazioni base Grafici 2D}"))
        s.context_menu["item2"].add_element("plot_name2D", Entrata("20%w", "90px", "lu", "75%w", "30px", text="", title="Name: ", tooltip="Cambia il nome del grafico. La modifica sarà visibile nei plot selection e nella legenda."))
        
        s.context_menu["item2"].add_window("wind2D_1", Collapsable_Window(x="1%w", y="150px", w="98%w", h="150px", anchor="lu", bg=[20, 20, 20], text="Spacing", closed=1, group=2))
        s.context_menu["item2"].add_window("wind2D_2", Collapsable_Window(w="98%w", h="200px", anchor=("lu ld (0px) (10px)", s.context_menu["item2"].windows["wind2D_1"]), bg=[20, 20, 20], text="Color map", closed=1, group=2))
        s.context_menu["item2"].add_window("wind2D_3", Collapsable_Window(w="98%w", h="150px", anchor=("lu ld (0px) (10px)", s.context_menu["item2"].windows["wind2D_2"]), bg=[20, 20, 20], text="Axes Flip", closed=1, group=2))
        
        s.context_menu["item2"].add_element("spacing_x", Entrata("95%w", "215px", "ru", "30%w", "30px", text="1", title="Spacing X", lunghezza_max=13, solo_numeri=True, num_valore_minimo=1e-10, num_valore_massimo=1e10, tooltip="Imposta il valore di spacing tra un pixel e l'altro (ASSE X) (solitamente != 1) \\i{\\#aaffaa{Min: 1e-10} | \\#ffaaaa{Max: 1e10} | Std: 1}\n\\#777777{Durante l'import è possibile vedere nel CMD questo valore. Per alcuni formati, il processo è automatizzato.}"), window="wind2D_1")
        s.context_menu["item2"].add_element("spacing_y", Entrata("95%w", "250px", "ru", "30%w", "30px", text="1", title="Spacing Y", lunghezza_max=13, solo_numeri=True, num_valore_minimo=1e-10, num_valore_massimo=1e10, tooltip="Imposta il valore di spacing tra un pixel e l'altro (ASSE Y) (solitamente != 1) \\i{\\#aaffaa{Min: 1e-10} | \\#ffaaaa{Max: 1e10} | Std: 1}\n\\#777777{Durante l'import è possibile vedere nel CMD questo valore. Per alcuni formati, il processo è automatizzato.}"), window="wind2D_1")
        
        s.context_menu["item2"].add_element("colore_base1", ColorPicker("30%w", "400px", "cc", "30%w", "40px", [0, 0, 0], bg=[50, 50, 50], text="Colore estremo LOW", tooltip="Imposta uno degli estremi di colore per la visualizzazione di un range di valori.\n\\#777777{Per visualizzare la visualizzazione della rampa di colore, abilitare la visualizzazione del secondo asse.}"), window="wind2D_2")
        s.context_menu["item2"].add_element("colore_base2", ColorPicker("30%w", "455px", "cc", "30%w", "40px", [220, 20, 60], bg=[50, 50, 50], text="Colore estremo HIGH", tooltip="Imposta uno degli estremi di colore per la visualizzazione di un range di valori.\n\\#777777{Per visualizzare la visualizzazione della rampa di colore, abilitare la visualizzazione del secondo asse.}"), window="wind2D_2")
        
        s.context_menu["item2"].add_element("flip_y", Bottone_Toggle("80%w", "600px", "ru", "30px", "30px", 0, text="Flip Y axis", text_on_right=0, tooltip="Inverte la visualizzazione dell'asse Y.\n\\#ffaa00{NOTA: Il valore dei tick NON cambierà.}"), window="wind2D_3")
        s.context_menu["item2"].add_element("flip_x", Bottone_Toggle("40%w", "600px", "ru", "30px", "30px", 0, text="Flip X axis", text_on_right=0, tooltip="Inverte la visualizzazione dell'asse X.\n\\#ffaa00{NOTA: Il valore dei tick NON cambierà.}"), window="wind2D_3")
        # # ITEM 2 PLOTS ---------------------------------------------------


        # # ITEM 3 AX LABELS -----------------------------------------------
        # s.context_menu["item3"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", w="-*w", h="-*h", text=r"\#88dd88{Impostazioni base Label}"))
        s.context_menu["item3"].add_window("wind1", Collapsable_Window(x="1%w", y="10px", w="98%w", h="270px", anchor="lu", bg=[20, 20, 20], text="Labels text", closed=1))
        s.context_menu["item3"].add_window("wind2", Collapsable_Window(w="98%w", h="250px", anchor=("lu ld (0px) (10px)", s.context_menu["item3"].windows["wind1"]), bg=[20, 20, 20], text="Font", closed=1))
        s.context_menu["item3"].add_window("wind3", Collapsable_Window(w="98%w", h="320px", anchor=("lu ld (0px) (10px)", s.context_menu["item3"].windows["wind2"]), bg=[20, 20, 20], text="Text colors", closed=1))
        s.context_menu["item3"].add_window("wind4", Collapsable_Window(w="98%w", h="280px", anchor=("lu ld (0px) (10px)", s.context_menu["item3"].windows["wind3"]), bg=[20, 20, 20], text="Projection labels", closed=1))
        
        s.context_menu["item3"].add_element("text_title", Entrata("20%w", "100px", "lu", "75%w", "30px", text="Title", title="Title", tooltip="Imposta il titolo del grafico.\n\\#777777{Il testo sarà sempre centrato, per ulteriori impostazioni cercare più in basso.}"), window="wind1")
        s.context_menu["item3"].add_element("text_label_x", Entrata("20%w", "150px", "lu", "75%w", "30px", text="X axis", title="Label X", tooltip="Imposta il label dell'asse X.\n\\#777777{Il testo sarà sempre centrato, per ulteriori impostazioni cercare più in basso.}"), window="wind1")
        s.context_menu["item3"].add_element("text_label_y", Entrata("20%w", "185px", "lu", "75%w", "30px", text="Y axis", title="Y", tooltip="Imposta il label dell'asse Y.\n\\#777777{Il testo sarà sempre centrato, per ulteriori impostazioni cercare più in basso.}"), window="wind1")
        s.context_menu["item3"].add_element("text_label_2y", Entrata("20%w", "220px", "lu", "75%w", "30px", text="2Y axis", title="2°Y", tooltip="Imposta il label del secondo asse Y.\n\\#777777{Il testo sarà sempre centrato, per ulteriori impostazioni cercare più in basso.}"), window="wind1")
        
        s.context_menu["item3"].add_element("font_size_title", Entrata("75%w", "355px", "lu", "20%w", "30px", text="64", title="Title font size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128, tooltip="Imposta la dimensione del carattere del label. \\i{\\#aaffaa{Min: 8} | \\#ffaaaa{Max: 128} | Std: 48}"), window="wind2")
        s.context_menu["item3"].add_element("font_size_label_x", Entrata("75%w", "405px", "lu", "20%w", "30px", text="48", title="Label font size X", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128, tooltip="Imposta la dimensione del carattere del label. \\i{\\#aaffaa{Min: 8} | \\#ffaaaa{Max: 128} | Std: 48}"), window="wind2")
        s.context_menu["item3"].add_element("font_size_label_y", Entrata("75%w", "440px", "lu", "20%w", "30px", text="48", title="Y", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128, tooltip="Imposta la dimensione del carattere del label. \\i{\\#aaffaa{Min: 8} | \\#ffaaaa{Max: 128} | Std: 48}"), window="wind2")
        s.context_menu["item3"].add_element("font_size_label_2y", Entrata("75%w", "475px", "lu", "20%w", "30px", text="48", title="2°Y", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128, tooltip="Imposta la dimensione del carattere del label. \\i{\\#aaffaa{Min: 8} | \\#ffaaaa{Max: 128} | Std: 48}"), window="wind2")
        
        s.context_menu["item3"].add_element("label_title_color", ColorPicker("50%w", "650px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore titolo", tooltip="Seleziona il colore della scritta del titolo."), window="wind3")
        s.context_menu["item3"].add_element("label_x_color", ColorPicker("50%w", "720px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore label X", tooltip="Seleziona il colore della scritta del label X."), window="wind3")
        s.context_menu["item3"].add_element("label_y_color", ColorPicker("50%w", "770px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore label Y", tooltip="Seleziona il colore della scritta del label Y."), window="wind3")
        s.context_menu["item3"].add_element("label_2y_color", ColorPicker("50%w", "820px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore label 2Y", tooltip="Seleziona il colore della scritta del label 2Y."), window="wind3")
        
        s.context_menu["item3"].add_element("show_coords_projection", Bottone_Toggle("95%w", "950px", "ru", "30px", "30px", text="Mostra proiezione coords", state=True, type_checkbox=True, text_on_right=False, tooltip="Mostra la proiezione del punto selezionato sull'asse X con un linea verticale."), window="wind4")
        s.context_menu["item3"].add_element("show_coords_value", Bottone_Toggle("95%w", "990px", "ru", "30px", "30px", text="Mostra valore coords", state=True, type_checkbox=True, text_on_right=False, tooltip="Mostra il valore della coordinata del punto selezionato.\n\\#777777{Attenzione: per modificare l'arrotondamento di uno dei valori, modifica l'approssimazione di quel determinato asse.}"), window="wind4")
        s.context_menu["item3"].add_element("toggle_coordinate_x", Bottone_Toggle("95%w", "1050px", "ru", "30px", "30px", text="Mostra coord. X", state=True, type_checkbox=True, text_on_right=False, tooltip="Mostra la coordinata X del punto selezionato.\n\\#777777{Attenzione: per modificare l'arrotondamento di uno dei valori, modifica l'approssimazione di quel determinato asse.}"), window="wind4")
        s.context_menu["item3"].add_element("toggle_coordinate_y", Bottone_Toggle("95%w", "1090px", "ru", "30px", "30px", text="Mostra coord. Y", state=True, type_checkbox=True, text_on_right=False, tooltip="Mostra la coordinata Y del punto selezionato.\n\\#777777{Attenzione: per modificare l'arrotondamento di uno dei valori, modifica l'approssimazione di quel determinato asse.}"), window="wind4")
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
        
        s.context_menu["item4"].add_element("first_y_axis", Bottone_Toggle("20%w", "140px", "cd", "25%w", "50px", True, False, "1° Y axis", tooltip="Abilita la visualizzazione del secondo asse Y. Per i plot 2D abilita la barra di colore con i valori in Z.\n\\#777777{Per visualizzare un plot sul secondo asse, aggiungerlo nella sezione 'Impostazioni plot'}"), window="wind1")
        s.context_menu["item4"].add_element("second_y_axis", Bottone_Toggle("50%w", "140px", "cd", "25%w", "50px", False, False, "2° Y axis", tooltip="Abilita la visualizzazione del secondo asse Y. Per i plot 2D abilita la barra di colore con i valori in Z.\n\\#777777{Per visualizzare un plot sul secondo asse, aggiungerlo nella sezione 'Impostazioni plot'}"), window="wind1")
        s.context_menu["item4"].add_element("invert_x_axis", Bottone_Toggle("80%w", "140px", "cd", "25%w", "50px", False, False, "Invert X", tooltip="Inverte la visualizzazione dell'asse X. Inverte sia la visualizzazione dei punti che il loro valore riportato."), window="wind1")

        s.context_menu["item4"].add_element("round_x", Entrata("75%w", "250px", "lu", "20%w", "30px", text="0", title="Round ticks X:", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=12, tooltip="Imposta l'approssimazione dopo la virgola dei valori relativi all'asse X. \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 12} | Std: 2}"), window="wind2")
        s.context_menu["item4"].add_element("round_y", Entrata("75%w", "285px", "lu", "20%w", "30px", text="0", title="Y:", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=12, tooltip="Imposta l'approssimazione dopo la virgola dei valori relativi all'asse Y. \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 12} | Std: 2}"), window="wind2")
        s.context_menu["item4"].add_element("round_2y", Entrata("75%w", "320px", "lu", "20%w", "30px", text="0", title="2°Y:", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=12, tooltip="Imposta l'approssimazione dopo la virgola dei valori relativi al secondo asse Y. \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 12} | Std: 2}"), window="wind2")
        
        s.context_menu["item4"].add_element("show_grid_x", Bottone_Toggle("95%w", "425px", "ru", "30px", "30px", text="Mostra griglia X", state=True, type_checkbox=True, text_on_right=False, tooltip="Abilita la visualizzazione della griglia X: si intendono i prolungamenti dei tick dei valori da ogni asse."), window="wind3")
        s.context_menu["item4"].add_element("show_grid_y", Bottone_Toggle("95%w", "460px", "ru", "30px", "30px", text="Mostra griglia Y", state=True, type_checkbox=True, text_on_right=False, tooltip="Abilita la visualizzazione della griglia Y: si intendono i prolungamenti dei tick dei valori da ogni asse."), window="wind3")
        s.context_menu["item4"].add_element("show_grid_2y", Bottone_Toggle("95%w", "495px", "ru", "30px", "30px", text="Mostra griglia 2°Y", state=True, type_checkbox=True, text_on_right=False, tooltip="Abilita la visualizzazione della griglia 2°Y: si intendono i prolungamenti dei tick dei valori da ogni asse."), window="wind3")
        s.context_menu["item4"].add_element("show_bounding_box", Bottone_Toggle("35%w", "495px", "ru", "30px", "30px", text="Mostra BB", state=True, type_checkbox=True, text_on_right=False, tooltip="Abilita la visualizzazione dell'asse verticale destro e l'asse orizzontale in alto. Racchiude il plot in un rettangolo."), window="wind3")
        
        s.context_menu["item4"].add_element("formatting_x", Bottone_Toggle("95%w", "625px", "ru", "30px", "30px", text="Not. Scien. asse X", type_checkbox=True, text_on_right=False, tooltip="Decide il formattatore da usare per i valori dell'asse X.\n\\#777777{Passa da una visualizzazione del tipo '1000.0' a '1.0e3'}"), window="wind4")
        s.context_menu["item4"].add_element("formatting_y", Bottone_Toggle("95%w", "660px", "ru", "30px", "30px", text="Not. Scien. asse Y", type_checkbox=True, text_on_right=False, tooltip="Decide il formattatore da usare per i valori dell'asse Y.\n\\#777777{Passa da una visualizzazione del tipo '1000.0' a '1.0e3'}"), window="wind4")
        s.context_menu["item4"].add_element("formatting_2y", Bottone_Toggle("95%w", "695px", "ru", "30px", "30px", text="Not. Scien. asse 2°Y", type_checkbox=True, text_on_right=False, tooltip="Decide il formattatore da usare per i valori dell'asse 2°Y.\n\\#777777{Passa da una visualizzazione del tipo '1000.0' a '1.0e3'}"), window="wind4")
        
        s.context_menu["item4"].add_element("ax_color_x", ColorPicker("30%w", "875px", "cc", "30%w", "40px", [70, 70, 70], bg=[50, 50, 50], text="Colore asse X", tooltip="Controlla il colore dell'asse X e delle sue proiezioni."), window="wind5")
        s.context_menu["item4"].add_element("ax_color_y", ColorPicker("30%w", "925px", "cc", "30%w", "40px", [70, 70, 70], bg=[50, 50, 50], text="Colore asse Y", tooltip="Controlla il colore dell'asse Y e delle sue proiezioni."), window="wind5")
        s.context_menu["item4"].add_element("ax_color_2y", ColorPicker("30%w", "980px", "cc", "30%w", "40px", [70, 70, 70], bg=[50, 50, 50], text="Colore asse 2°Y", tooltip="Controlla il colore dell'asse 2°Y e delle sue proiezioni."), window="wind5")
        s.context_menu["item4"].add_element("tick_color_x", ColorPicker("30%w", "1070px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore values X", tooltip="Controlla il colore dei tick label dell'asse X."), window="wind5")
        s.context_menu["item4"].add_element("tick_color_y", ColorPicker("30%w", "1120px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore values Y", tooltip="Controlla il colore dei tick label dell'asse Y."), window="wind5")
        s.context_menu["item4"].add_element("tick_color_2y", ColorPicker("30%w", "1170px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Colore values 2°Y", tooltip="Controlla il colore dei tick label dell'asse 2°Y."), window="wind5")
        
        s.context_menu["item4"].add_element("offset_x_label_y", Entrata("75%w", "1330px", "lu", "20%w", "30px", text="45", title="Offset Y of ticks X axis:", lunghezza_max=4, solo_numeri=True, tooltip="Imposta un offset in pixel della posizione dei tick label dell'asse X in verticale. \\i{\\#aaffaa{Min: -999} | \\#ffaaaa{Max: 9999} | Std: 45}"), window="wind6")
        s.context_menu["item4"].add_element("offset_y_label_x", Entrata("75%w", "1365px", "lu", "20%w", "30px", text="-27", title="Offset X of ticks Y axis:", lunghezza_max=4, solo_numeri=True, tooltip="Imposta un offset in pixel della posizione dei tick label dell'asse Y in orizzontale. \\i{\\#aaffaa{Min: -999} | \\#ffaaaa{Max: 9999} | Std: -27}"), window="wind6")

        s.context_menu["item4"].add_element("size_ticks", Entrata("75%w", "1520px", "lu", "20%w", "30px", text="1.5", title="Font size ticks Y axis:", lunghezza_max=4, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=3, tooltip="Imposta la dimensione del font dei tick label. Viene usata una scala custom. \\i{\\#aaffaa{Min: 0} | \\#ffaaaa{Max: 3} | Std: 1.5}"), window="wind7")
        # # ITEM 4 AXES ----------------------------------------------------


        # # ITEM 5 LEGEND --------------------------------------------------
        s.context_menu["item5"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", w="-*w", h="-*h", text=r"\#88dd88{Impostazioni base Legenda}"))
    
        s.context_menu["item5"].add_window("wind1", Collapsable_Window(x="1%w", y="170px", w="98%w", h="180px", anchor="lu", bg=[20, 20, 20], text="Position and size", closed=1))
        s.context_menu["item5"].add_window("wind2", Collapsable_Window(w="98%w", h="280px", anchor=("lu ld (0px) (10px)", s.context_menu["item5"].windows["wind1"]), bg=[20, 20, 20], text="Background", closed=1))
        s.context_menu["item5"].add_window("wind3", Collapsable_Window(w="98%w", h="220px", anchor=("lu ld (0px) (10px)", s.context_menu["item5"].windows["wind2"]), bg=[20, 20, 20], text="Text and icons", closed=1))
        s.context_menu["item5"].add_window("wind4", Collapsable_Window(w="98%w", h="170px", anchor=("lu ld (0px) (10px)", s.context_menu["item5"].windows["wind3"]), bg=[20, 20, 20], text="2D marker", closed=1))
        

        s.context_menu["item5"].add_element("show_legend", Bottone_Toggle("95%w", "80px", "ru", "30px", "30px", text="\\#dfffdf{\\b{Mostra legenda}}", state=False, type_checkbox=True, text_on_right=False, tooltip="Abilita la renderizzazione della legenda.\n\\#dc143c{Attenzione: è necessario abilitare la legenda per modificare le impostazioni.}"))

        s.context_menu["item5"].add_element("x_legend", Slider("25%w", "260px", "lu", "40%w", "30px", title="X legend", initial_value=0.75, min_value=-0.5, max_value=1.5, tooltip="Imposta la posizione X del centro della legenda. \\i{\\#aaffaa{Min: -0.5} | \\#ffaaaa{Max: 1.5} | Std: 0.5}\n\\#777777{Valori tra 0 e 1 posizionano la legenda dentro al grafico, ma è possibile uscire da questi limiti.}"), window="wind1")
        s.context_menu["item5"].add_element("y_legend", Slider("25%w", "295px", "lu", "40%w", "30px", title="Y legend", initial_value=0., min_value=-0.5, max_value=1.5, tooltip="Imposta la posizione Y del centro della legenda. \\i{\\#aaffaa{Min: -0.5} | \\#ffaaaa{Max: 1.5} | Std: 0.5}\n\\#777777{Valori tra 0 e 1 posizionano la legenda dentro al grafico, ma è possibile uscire da questi limiti.}"), window="wind1")

        s.context_menu["item5"].add_element("font_size_legend", Entrata("85%w", "195px", "lu", "10%w", "30px", text="48", title="Legend font size", lunghezza_max=3, solo_numeri=True, num_valore_minimo=8, num_valore_massimo=128, tooltip="Imposta la dimensione del font della legenda. \\i{\\#aaffaa{Min: 8} | \\#ffaaaa{Max: 128} | Std: 48}\n\\#777777{Nota: Cambia solo la dimensione del testo, non del simbolo.}"), window="wind1")
        
        s.context_menu["item5"].add_element("show_legend_background", Bottone_Toggle("95%w", "400px", "ru", "30px", "30px", text="\\#dfffdf{\\b{Disegna bg}}", state=False, type_checkbox=True, text_on_right=False, tooltip="Decide se disegnare lo sfondo della legenda. Altre impostazioni seguono."), window="wind2")
        s.context_menu["item5"].add_element("legend_color_background", ColorPicker("30%w", "480px", "cc", "30%w", "40px", [250, 250, 250], bg=[50, 50, 50], text="Color legend bg", tooltip="Imposta il colore dello sfondo della legenda.\n\\#777777{Quando lo sfondo è trasparente, questo colore fungerà da attenuatore dei colori sottostanti.}"), window="wind2")
        s.context_menu["item5"].add_element("transparent_background", Bottone_Toggle("95%w", "540px", "ru", "30px", "30px", text="Trasparenza bg", state=True, type_checkbox=True, text_on_right=False, tooltip="Cambia lo sfondo in trasparente, dando la possibilità di sfumare i colori sottostanti.\n\\#dc143c{Quest'opzione è molto pesante!} \\#777777{Considera di accenderla solo prima di renderizzare l'immagine}"), window="wind2")
        s.context_menu["item5"].add_element("blur_strenght", Entrata("75%w", "580px", "lu", "20%w", "30px", text="6", title="Forza di blur", lunghezza_max=2, solo_numeri=True, num_valore_minimo=1, num_valore_massimo=12, tooltip="Aumenta l'effetto di sfumatura. \\i{\\#aaffaa{Min: 1} | \\#ffaaaa{Max: 12} | Std: 6}"), window="wind2")
        
        s.context_menu["item5"].add_element("show_icons", Bottone_Toggle("95%w", "710px", "ru", "30px", "30px", text="Mostra icone", state=True, type_checkbox=True, text_on_right=False, tooltip="Mostra il corrispondente simbolo usato nel grafico (combinazione di scatter e function)."), window="wind3")
        s.context_menu["item5"].add_element("match_color_text", Bottone_Toggle("95%w", "750px", "ru", "30px", "30px", text="Match text color", state=True, type_checkbox=True, text_on_right=False, tooltip="Decide se mostrare il titolo del singolo plot come colore unico o matchare il colore del plot."), window="wind3")
        s.context_menu["item5"].add_element("color_text", ColorPicker("30%w", "810px", "cc", "30%w", "40px", [255, 255, 255], bg=[50, 50, 50], text="Color legend text", tooltip="Imposta il colore unificato del testo."), window="wind3")
        
        s.context_menu["item5"].add_element("text_2D_plot", Entrata("75%w", "950px", "lu", "20%w", "30px", text=r"1\mum", title="Testo marker scala", tooltip="Imposta cosa visualizzare nel marker dimensionale nei plot 2D.\n\\#777777{Se per esempio l'asse X va da 0 a 1 \\mum, imposta 0.2 \\mum oppure 200 nm.}"), window="wind4")
        s.context_menu["item5"].add_element("size_scale_marker2D", Entrata("75%w", "990px", "lu", "20%w", "30px", text="1000", title="Valore marker scala", solo_numeri=True, tooltip="Imposta la dimensione del marker da mostrare. Indica la dimensione in unità dell'asse X.\n\\#777777{Se per esempio l'asse X va da 0 a 1 \\mum, imposta questo valore a 0.2 per visualizzare 0.2 \\mum.}"), window="wind4")
        # # ITEM 5 LEGEND --------------------------------------------------


        # # ITEM 6 IMPORT --------------------------------------------------
        s.context_menu["item6"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Import}"))
        
        s.context_menu["item6"].add_element("import_single_plot1D", Bottone_Push("50%w", "80px", "cu", "70%w", "40px", function=self.bott_calls.load_file, text="Carica singolo file 1D", tooltip="Importa un singolo file che verrà trattato come \\i{f(x)}, quindi un insieme di coordinate X-Y. Supporta l'import di file a più colonne.\n\\#777777{Formati supportati: \\#aaff00{.txt, .csv, .CSV, .dpt, .ASCII, .dat} | Codifiche: \\#ffaa00{utf8, utf-16-le}}"))
        s.context_menu["item6"].add_element("import_multip_plot1D", Bottone_Push("50%w", "130px", "cu", "70%w", "40px", function=self.bott_calls.load_files, text="Carica file multipli 1D", tooltip="Versione multipla di 'Carica singolo file 1D', è possibile trascinare i file direttamente sull'app per caricarli.\n\\#777777{\\#dc143c{Attenzione:} Se si usa la modalità trascinamento, assicurarsi di aver scelto la modalità di plot corretta in 'Modalità di visualizzazione'.}"))
        s.context_menu["item6"].add_element("import_single_plot2D", Bottone_Push("50%w", "200px", "cu", "70%w", "40px", function=self.bott_calls.load_file, text="Carica singolo file 2D", tooltip="Importa un singolo file che verrà trattato come immagine, quindi un insieme di valori Z alla posizione X-Y. Supporta l'import di file a 3 colonne.\n\\#777777{Formati supportati: \\#aaff00{.txt, .tiff, .TIFF}. Estrazione metadata automatica da file generati da AFM e SEM. Leggere l'output nel CMD per più informazioni.}"))
        s.context_menu["item6"].add_element("import_multip_plot2D", Bottone_Push("50%w", "250px", "cu", "70%w", "40px", function=self.bott_calls.load_files, text="Carica file multipli 2D", tooltip="Versione multipla di 'Carica singolo file 2D', è possibile trascinare i file direttamente sull'app per caricarli.\n\\#777777{\\#dc143c{Attenzione:} Se si usa la modalità trascinamento, assicurarsi di aver scelto la modalità di plot corretta in 'Modalità di visualizzazione'.}"))
    
        s.context_menu["item6"].add_element("remove_element_selected", Bottone_Push("50%w", "320px", "cu", "70%w", "40px", function=self.bott_calls.change_state, text=r"\#dc143c{Elimina elemento selezionato}", tooltip="Elimina dall'elenco dei file caricato il file selezionato."))
        
        # # ITEM 6 IMPORT --------------------------------------------------


        # # ITEM 7 EXPORT --------------------------------------------------
        s.context_menu["item7"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Export}"))
        s.context_menu["item7"].add_element("save_single_plot", Bottone_Push("50%w", "80px", "cu", "70%w", "40px", function=self.bott_calls.save_image, text="Salva grafico", tooltip="Salva il grafico in formato .png\n\\#777777{La dimensione X viene fissata a 4000px, mentre la dimensione Y viene aggiustata per mantenere la scala.}"))
        # # ITEM 7 EXPORT --------------------------------------------------


        # # ITEM 8 STATSISTIC ----------------------------------------------
        s.context_menu["item8"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Statistica}"))
        # # ITEM 8 STATSISTIC ----------------------------------------------


        # # ITEM 9 INTERPOLATION -------------------------------------------
        s.context_menu["item9"].add_window("wind1", Collapsable_Window(x="1%w", y="10px", w="98%w", h="380px", anchor="lu", bg=[20, 20, 20], text="Derivata", closed=1))
        s.context_menu["item9"].add_window("wind2", Collapsable_Window(w="98%w", h="580px", anchor=("lu ld (0px) (10px)", s.context_menu["item9"].windows["wind1"]), bg=[20, 20, 20], text="Interpolazione", closed=1))
        s.context_menu["item9"].add_window("wind3", Collapsable_Window(w="98%w", h="880px", anchor=("lu ld (0px) (10px)", s.context_menu["item9"].windows["wind2"]), bg=[20, 20, 20], text="Custom curve", closed=1))
        
        # s.context_menu["item9"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Interpolazioni}"))
        
        s.context_menu["item9"].add_element("compute_derivative", Bottone_Push("50%w", "100px", "cu", "50%w", "50px", text="Compute derivative", function=self.bott_calls.change_state, tooltip="Calcola la derivata del grafico attivo e la aggiunge alla lista dei grafici."), window="wind1")
        s.context_menu["item9"].add_element("output_derivative", Label_Text("5%w", "200px", "lu", "90%w", "-*h", text="Derivative results:\n---"), window="wind1")
        
        s.context_menu["item9"].add_element("min_x", Entrata("40%w", "500px", "cu", "30%w", "-*h", text="", title="Min. X", solo_numeri=True, tooltip="Imposta il valore minimo di X dell'intervallo che verrà considerato quando verrà calcolata l'interpolazione.\n\\#777777{Dati al di fuori di questo range verranno ignorati.}"), window="wind2")
        s.context_menu["item9"].add_element("max_x", Entrata("40%w", "580px", "cd", "30%w", "-*h", text="", title="Max. X", solo_numeri=True, tooltip="Imposta il valore massimo di X dell'intervallo che verrà considerato quando verrà calcolata l'interpolazione.\n\\#777777{Dati al di fuori di questo range verranno ignorati.}"), window="wind2")
        s.context_menu["item9"].add_element("intersection", Bottone_Toggle("10%w", "650px", "ld", "30px", "30px", text="Find intersection X", tooltip="Forza il calcolo dell'intersezione con l'asse X del grafico, utile per trovare lo zero dell'interpolazione."), window="wind2")
        s.context_menu["item9"].add_element("compute", Bottone_Push("90%w", "500px", "ru", "30%w", "80px", text="Compute", function=self.bott_calls.change_state, tooltip="Calcola l'interpolazione lineare."), window="wind2")
        s.context_menu["item9"].add_element("output", Label_Text("5%w", "720px", "lu", "90%w", "-*h", text="Interpolation results:\n---"), window="wind2")
        
        s.context_menu["item9"].add_element("curve_function", Entrata("95%w", "1075px", "ru", "60%w", "-*h", text="", title="Custom function", tooltip="Inserisci la funzione custom da interpolare scritta con la sintassi NumPy.\n\\#777777{Usa 'x' come incognita e p[*] come parametri da calcolare.} \\#aaff00{Carica un preset (\\i{ex: GAUSSIANA}) per vedere un esempio di sintassi.}"), window="wind3")
        s.context_menu["item9"].add_element("param_0", Entrata("12.5%w", "1150px", "lu", "15.5%w", "-*h", text="", title="p[0]", tooltip="Inserisci il parametro 0 guess.\n\\#777777{\\#dc143c{Attenzione:} solo i parametri usati nella funzione verranno considerati.}"), window="wind3")
        s.context_menu["item9"].add_element("param_1", Entrata("12.5%w", "1200px", "lu", "15.5%w", "-*h", text="", title="p[1]", tooltip="Inserisci il parametro 1 guess.\n\\#777777{\\#dc143c{Attenzione:} solo i parametri usati nella funzione verranno considerati.}"), window="wind3")
        s.context_menu["item9"].add_element("param_2", Entrata("12.5%w", "1250px", "lu", "15.5%w", "-*h", text="", title="p[2]", tooltip="Inserisci il parametro 2 guess.\n\\#777777{\\#dc143c{Attenzione:} solo i parametri usati nella funzione verranno considerati.}"), window="wind3")
        s.context_menu["item9"].add_element("param_3", Entrata("12.5%w", "1300px", "lu", "15.5%w", "-*h", text="", title="p[3]", tooltip="Inserisci il parametro 3 guess.\n\\#777777{\\#dc143c{Attenzione:} solo i parametri usati nella funzione verranno considerati.}"), window="wind3")
        
        s.context_menu["item9"].add_element("l_param_0", Label_Text("30%w", "1150px", "lu", "15.5%w", "-*h", text="-> NULL"), window="wind3")
        s.context_menu["item9"].add_element("l_param_1", Label_Text("30%w", "1200px", "lu", "15.5%w", "-*h", text="-> NULL"), window="wind3")
        s.context_menu["item9"].add_element("l_param_2", Label_Text("30%w", "1250px", "lu", "15.5%w", "-*h", text="-> NULL"), window="wind3")
        s.context_menu["item9"].add_element("l_param_3", Label_Text("30%w", "1300px", "lu", "15.5%w", "-*h", text="-> NULL"), window="wind3")
        
        s.context_menu["item9"].add_element("compute_custom_curve", Bottone_Push("90%w", "1150px", "ru", "30%w", "80px", text="Compute", function=self.bott_calls.change_state, tooltip="Calcola l'interpolazione custom"), window="wind3")
        s.context_menu["item9"].add_element("show_guess", Bottone_Toggle("95%w", "1275px", "ru", "30px", "30px", text="Show guess function", text_on_right=False, tooltip="Crea la funzione generata dai parametri guess usati.\n\\#777777{Usa il \\i{'Compute'} di nuovo per aggiornare la scelta.}"), window="wind3")
        
        s.context_menu["item9"].add_element("presets1", Bottone_Push("5%w", "1375px", "lu", "30%w", "50px", text="Esponenziale", function=self.bott_calls.change_state, tooltip="Usa il seguente preset per impostare il calcolo di interpolazione con una \\#aaff00{ESPONENZIALE} a + b * exp[c + x * d]"), window="wind3")
        s.context_menu["item9"].add_element("presets2", Bottone_Push("35%w", "1375px", "lu", "30%w", "50px", text="Gaussiana", function=self.bott_calls.change_state, tooltip="Usa il seguente preset per impostare il calcolo di interpolazione con una \\#aaff00{GAUSSIANA} a * exp[- ((x - b) / c)\\^{2} / 2]"), window="wind3")
        s.context_menu["item9"].add_element("presets3", Bottone_Push("65%w", "1375px", "lu", "30%w", "50px", text="Sigmoide", function=self.bott_calls.change_state, tooltip="Usa il seguente preset per impostare il calcolo di interpolazione con una \\#aaff00{SIGMOIDE} a + b / (1 + exp[(-x + c) / d])"), window="wind3")
        
        s.context_menu["item9"].add_element("info1", Label_Text("5%w", "1450px", "lu", "90%w", "-*h", text="Use 'p[x]' instead of the parameter you\nwant to calculate."), window="wind3")
        s.context_menu["item9"].add_element("info2", Label_Text("5%w", "1550px", "lu", "90%w", "-*h", text="Example: p[0] * x ** 2 + p[1] * x + p[2]\nGives -> \\i{ax\\^{2} + bx + c}"), window="wind3")
        s.context_menu["item9"].add_element("info3", Label_Text("5%w", "1650px", "lu", "90%w", "-*h", text="Curve fit results:\n---"), window="wind3")
        # # ITEM 9 INTERPOLATION -------------------------------------------


        # # ITEM 10 MULTI-PLOTS --------------------------------------------
        s.context_menu["item10"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Multi-Plots}"))
        # # ITEM 10 MULTI-PLOTS --------------------------------------------


        # # ITEM 11 METADATA -----------------------------------------------
        s.context_menu["item11"].add_element("_title_drop_menu_base", Label_Text("50%w", "10px", "cu", "-*w", "-*h", text=r"\#88dd88{Impostazioni base Metadata}"))
        s.context_menu["item11"].add_element("molecule_input", Entrata("30%w", "100px", "lu", "67.5%w", "40px", "", "SMILE code", tooltip="Inserisci il codice SMILE della molecola. Segui le istruzioni in '\\i{molecules_doc.md}'"))
        s.context_menu["item11"].add_element("molecule_preview", Screen("50%w", "280px", "cu", "90%w", "90%w"))
        s.context_menu["item11"].elements["molecule_preview"].tavolozza.fill([25, 25, 25])

        s.context_menu["item11"].add_element("add_molecola", Bottone_Push("72.5%w", "220px", "cu", "50%w", "40px", text="Add empty mol.", function=self.bott_calls.change_state, tooltip="Aggiunge una nuova molecola vuota da modificare."))
        s.context_menu["item11"].add_element("pos_x_molecola", Entrata("30%w", "170px", "lu", "10%w", "40px", "50", "Pos. X [%]", tooltip="Imposta la posizione X percentuale della molecola. \\i{\\#aaffaa{Min: /} | \\#ffaaaa{Max: /} | Std: 50}"))
        s.context_menu["item11"].add_element("pos_y_molecola", Entrata("30%w", "220px", "lu", "10%w", "40px", "50", "Pos. Y [%]", tooltip="Imposta la posizione Y percentuale della molecola. \\i{\\#aaffaa{Min: /} | \\#ffaaaa{Max: /} | Std: 50}"))
        s.context_menu["item11"].add_element("dimensione_molecola", Entrata("82.5%w", "170px", "lu", "15%w", "40px", "1000", "Dimensione", tooltip="Imposta la dimensione della molecola in pixel. \\i{\\#aaffaa{Min: /} | \\#ffaaaa{Max: /} | Std: 1000}"))
        # # ITEM 11 METADATA -----------------------------------------------

        stato_iniziale_tab = [False for _ in range(11)]
        tooltips_modes = [
            "GEOMETRIA\n\\#777777{Impostazioni di dimensioni e proporzionalità. Scelta di tipologia di grafici.}",
            "GRAFICI\n\\#777777{Impostazioni del grafico attivo.}",
            "LABELS\n\\#777777{Impostazioni di testo e forma delle scritte presenti nel disegno.}",
            "ASSI\n\\#777777{Impostazioni di testo e forma degli assi, scala, valori numerici.}",
            "LEGENDA\n\\#777777{Impostazioni legenda e marker.}",
            "IMPORT\n\\#777777{Impostazioni di import di file e dati.}",
            "EXPORT\n\\#777777{Impostazioni di rendering del disegno.}",
            "STATISTICA\n\\#ffaa00{In sviluppo...}",
            "DATA EXTRACTION\n\\#777777{Estrazione di Derivata, Interpolazione lineare, Interpolazione custom.}",
            "MULTI-PLOT\n\\#ffaa00{In sviluppo}",
            "EXTRA-DOODLES\n\\#777777{Aggiunta di altri elementi: \\#aaff00{Molecole,} \\#dc143c{Testo, Frecce, Riquadri, Cerchi.}}",
        ]

        s.context_menu["main"].add_element("modes", RadioButton(x="73.5%w", y="40%h", anchor="ru", w="2.4%w", h="55%h", bg=array([30, 30, 30]), axis="y", cb_n=11, cb_s=stato_iniziale_tab, cb_t=tooltips_modes, cb_tooltips=["" for _ in range(11)], type_checkbox=False, w_button="2.4%w", h_button="2.4%w"))
        [bottone.load_texture(f"item{index + 1}") for index, bottone in enumerate(s.context_menu["main"].elements["modes"].toggles)]
        
        s.context_menu["main"].add_element("tools", RadioButton(x="0px", y="10%h", anchor="lu", w="2.4%w", h=f"{2.5*3}%w", bg=array([30, 30, 30]), axis="y", cb_n=3, cb_s=[0, 0, 0], cb_t=["" for _ in range(3)], cb_tooltips=["ZOOM della regione interessata. Proporzioni NON mantenute", "PAN della zona, nel caso 2D non esce dai margini dell'immagine", "Inserimento coordinate, consultare \\i{'LABELS > Projection labels'} per più informazioni."], type_checkbox=False, w_button="2.4%w", h_button="2.4%w"))
        [bottone.load_texture(f"tool{index + 1}") for index, bottone in enumerate(s.context_menu["main"].elements["tools"].toggles)]

        s.context_menu["main"].add_element("reset_zoom", Bottone_Push(anchor=("cu cd (0px) (10px)", s.context_menu["main"].elements["tools"]), w="2.4%w", h="2.4%w", function=BottoniCallbacks.change_state, tooltip="Resetta lo zoom e pan del grafico."))
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
                

        def open_project(user_call=False):
            if user_call:
                s.context_menu["main"].elements["open"].flag_foo = True


        def save_project(user_call=False):
            if user_call:
                s.context_menu["main"].elements["save"].flag_foo = True


        s.functions.append(set_active_tab)
        s.functions.append(hide_plot_attributes_based_on_plot_mode)
        s.functions.append(hide_legend_attributes_based_on_plot_mode)
        s.functions.append(hide_UI_element_with_toggle_plot_section)
        s.functions.append(hide_UI_element_with_toggle_legend_section)
        s.functions.append(hide_overlap_normalization)
        s.functions.append(remove_selected_element)
        s.functions.append(hide_UI_plot_area_size_based_on_proportions)
        s.functions.append(hide_metadata_based_on_metadata_lenght)
        s.functions.append(save_project)
        s.functions.append(open_project)


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


        self.pop_up_palette_hard: PopUp_color_palette_hard = PopUp_color_palette_hard(x="50%w", y="50%h", anchor="cc", w="40%w", h="40%h")
        self.pop_up_palette: PopUp_color_palette_easy = PopUp_color_palette_easy(x="50%w", y="50%h", anchor="cc", w="40%w", h="40%h")

        self.pop_up_palette_open_next = False

        self.pop_up_palette_receiver: ColorPicker = None

        self.pop_up_palette_aperto: bool = False
        self.pop_up_palette_hard_aperto: bool = False

        self.user_wants_tooltips = True

        self.functions: list[function] = []


    def disegna_scena(self, logica: 'Logica'):
        [context.disegnami(logica) for indice, context in self.context_menu.items()]
        
        self.pop_up_palette.disegnami(logica)
        self.pop_up_palette_hard.disegnami(logica)

        if self.user_wants_tooltips:
            # gestione tooltip
            def flatten(lst):
                result = []
                for item in lst:
                    if isinstance(item, list):
                        result.extend(item)
                    else:
                        result.append(item)
                return result
            
            possibili_tooltip = [ele.search_for_tooltip(logica) for index, ele in self.context_menu.items()]
            
            run = 1
            max_iteration = 0
            messaggio = possibili_tooltip
            while run and max_iteration < 10:
                max_iteration += 1
                messaggio = flatten(messaggio)
                if len([1 for is_list in messaggio if type(is_list) == list]) == 0:
                    run = 0

            messaggio = [ele for ele in messaggio if not ele is None]
            if len(messaggio) == 1:
                [ele.change_tooltip(messaggio[0]) for index, ele in self.context_menu.items() if ele.root]
            elif len(messaggio) > 1:
                print(messaggio)
                [ele.change_tooltip(" | ".join(messaggio)) for index, ele in self.context_menu.items() if ele.root]
            else:
                [ele.change_tooltip("Premere \\#aaffaa{CTRL + T} per disabilitare e/o riabilitare i tooltip") for index, ele in self.context_menu.items() if ele.root]
    
    
    def gestisci_eventi(self, eventi: list[pygame.event.Event], logica: 'Logica'):
        
        if not self.pop_up_palette_aperto:

            [context.eventami(eventi, logica) for indice, context in self.context_menu.items()]

            # POSSIBILI GENERATORI DI POP-UP -> COLORE
            # controllo degli elementi figli dei dropmenu
            for indice, context in self.context_menu.items():
                for indice_ele, elemento in context.elements.items():
                    if type(elemento) == ColorPicker:
                        pop_up_colore_domanda = elemento.check_open_popup_call()

                        if pop_up_colore_domanda:
                            self.pop_up_palette_receiver = elemento
                            self.pop_up_palette_aperto = True
                            self.pop_up_palette.active = True
                            self.pop_up_palette.start_connection(self.pop_up_palette_receiver.send_popup_request())

            
            for foo in self.functions:
                foo()


        elif self.pop_up_palette.conferma_uscita:

            if not self.pop_up_palette.open_next:
                self.pop_up_palette_aperto = False
                
                self.pop_up_palette_receiver.open_call = False
                self.pop_up_palette_receiver.receive_popup_answer(self.pop_up_palette.end_connection())
                self.pop_up_palette_receiver = None

            if self.pop_up_palette.open_next:
                self.pop_up_palette_aperto = True

                self.pop_up_palette_hard.active = True
                self.pop_up_palette_hard.start_connection(self.pop_up_palette_receiver.send_popup_request())

            self.pop_up_palette.conferma_uscita = False
            self.pop_up_palette.packet_out = None


        elif self.pop_up_palette.open_next and self.pop_up_palette_hard.conferma_uscita:
            self.pop_up_palette.open_next = False
            self.pop_up_palette_aperto = False
            
            self.pop_up_palette_receiver.open_call = False
            self.pop_up_palette_receiver.receive_popup_answer(self.pop_up_palette_hard.end_connection())
            self.pop_up_palette_receiver = None

            self.pop_up_palette_hard.conferma_uscita = False
            self.pop_up_palette_hard.packet_out = None
        

        if self.pop_up_palette.active:
            self.pop_up_palette.eventami(eventi, logica)
        if self.pop_up_palette_hard.active:
            self.pop_up_palette_hard.eventami(eventi, logica)

        for event in eventi:
            # Check if a key was pressed
            if event.type == pygame.KEYDOWN:
                # Check if 'T' was pressed AND Ctrl is held
                if event.key == pygame.K_t and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.user_wants_tooltips = not self.user_wants_tooltips 

                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    foo = self.functions[9]
                    foo(True)

                if event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    foo = self.functions[10]
                    foo(True)