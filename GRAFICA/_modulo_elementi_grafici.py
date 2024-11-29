import pygame
from numpy import array
from MATEMATICA._modulo_mate_utils import MateUtils
import pyperclip
import os
from PIL import Image
from math import ceil

NON_ESEGUIRE = False

if NON_ESEGUIRE:    
    from pygame.event import Event
    from _modulo_UI import Logica

    # formula per ricavare l'altezza del Font: floor(font_size * 0.16209 + 1)

from GRAFICA._modulo_database import Dizionario; diction = Dizionario()



class BaseElement:

    '''
    Creazione standard:
    
    coordinata, qualunque essa sia, sarà composta da diverse parti:

    x: float | str = se float rappresenta una posizione percentuale, se str rappresenta una posizione in pixel
    anchor_x: tuple[float | None] = 3 valori, il primo indica l'ancoraggio dell'elemento, il secondo l'ancoraggio al quale si punta, il terzo è l'effettiva quantità
    tipi di ancoraggio: 

    lu  cu  ru
    lc  cc  rc
    ld  cd  rd

    '''

    pappardella = None

    def __init__(self, x="", y="", anchor="lu", w="", h="", text="", hide=False, color_text=[200, 200, 200], latex_font=False, bg=None) -> None:
        
        self.latex_font = latex_font

        self.schermo = BaseElement.pappardella["screen"]

        self.color_text = color_text

        if bg is None:
            self.bg = array(BaseElement.pappardella["bg_def"])
        else:
            self.bg = bg

        self.hide: bool = hide

        self.testo: str = text
        self.testo_diplayed = (f"{self.testo}", 1)
        
        self.font_size_update = 24
        self.font: Font = Font(24, self.latex_font)

        self.ori_coords = (x, y, w, h, anchor)

        self.need_update = False

        self.x_Context = 0
        self.y_Context = 0
        self.w_Context = self.pappardella["x_screen"]
        self.h_Context = self.pappardella["y_screen"]

        self.recalc_geometry(x, y, w, h, anchor)



    @classmethod
    def _init_scene(cls, pappardella) -> None:
        cls.pappardella = pappardella 


    def disegnami(self, logica):
        ...

    
    def eventami(self, events, logica):
        ...

    
    def change_text(self, text):
        self.testo = text


    def change_font_size(self, new_size):
        self.font_size_update = new_size
        self.font: Font = Font(new_size, self.latex_font)


    def update_window_change(self):
        self.recalc_geometry(*self.ori_coords)

    
    def update_context_menu(self, *args):
        self.x_Context = args[0]
        self.y_Context = args[1]
        self.w_Context = args[2]
        self.h_Context = args[3]


    def recalc_geometry(self, new_x="", new_y="", new_w="", new_h="", anchor_point=""):
        
        '''
        Come fornire le coordinate:
        ---
        - X%w               -> valore percentuale in larghezza
        - X%h               -> valore percenutale in altezza
        - Xpx               -> valore in pixel
        - -*w               -> automatico (si adatta alla larghezza del testo)
        - -*h               -> automatico (si adatta all'altezza del testo)

        Ancoraggio:
        ---
        - Type 1:
            - lu                        -> simple anchor point of the child element
        - Type 2:
            - lu                        -> anchor point of the child
            - rd                        -> anchor point of the parent
            - (X)                       -> offset X same as coords
            - (Y)                       -> offset Y same as coords
            - element.coords | None     -> coords of the parent element, or relative to the container

        Example:
        --- 
        - 50%w 10px is my new X position
        - 30%h 50px is my new Y position
        - 200px is my new width
        - --- is my new height

        - ("lu rd (-10%w -30px) (0)", label_time.coords) 

        Example combined:
        ---
        - Bottone(x="50%w 10px", y="30%h 50px", w="200px", h="-*h", anchor=("lu rd (-10%w -30px) (0)", label_time.coords))

        '''

        self.need_update = False

        self.one_percent_x = self.w_Context / 100
        self.one_percent_y = self.h_Context / 100
        
        def analyze_string_coordinate(string: str):

            # divido le varie componenti della coordinata (percentuali, valori puri, ecc...)
            sub_coords = string.split()

            # inizializzo la posizione finale, a cui aggiungo i vari valori ottenuti dalle coordinate
            posizione_finale = 0

            for sub_coord in sub_coords:
                if "px" in sub_coord:
                    posizione_finale += float(sub_coord[:-2])
                elif "%w" in sub_coord:
                    posizione_finale += float(sub_coord[:-2]) * self.one_percent_x
                elif "%h" in sub_coord:
                    posizione_finale += float(sub_coord[:-2]) * self.one_percent_y
                elif "-*w" in sub_coord:
                    posizione_finale += self.font.font_pyg_r.size(self.testo_diplayed[0])[0]
                elif "-*h" in sub_coord:
                    posizione_finale += self.font.font_pyg_r.size(self.testo_diplayed[0])[1] * self.testo_diplayed[1] # prendo l'altezza del carattere e la moltiplico per il numero di righe


            return posizione_finale


        def analyze_anchor_coordinate(string: str, coords_child, coords_parent):

            if len(string) == 2:
                # caso semplice di ancoraggio

                match string:
                    case "lu":
                        return (coords_child[0] - 0,                    coords_child[1] - 0)    
                    case "cu":
                        return (coords_child[0] - coords_child[2] / 2,  coords_child[1] - 0)    
                    case "ru":
                        return (coords_child[0] - coords_child[2],      coords_child[1] - 0)    
                    case "lc":
                        return (coords_child[0] - 0,                    coords_child[1] - coords_child[3] / 2)    
                    case "cc":
                        return (coords_child[0] - coords_child[2] / 2,  coords_child[1] - coords_child[3] / 2)    
                    case "rc":
                        return (coords_child[0] - coords_child[2],      coords_child[1] - coords_child[3] / 2)    
                    case "ld":
                        return (coords_child[0] - 0,                    coords_child[1] - coords_child[3])    
                    case "cd":
                        return (coords_child[0] - coords_child[2] / 2,  coords_child[1] - coords_child[3])    
                    case "rd":
                        return (coords_child[0] - coords_child[2],      coords_child[1] - coords_child[3])    

            else:
                # divido le varie componenti dell'istruzione
                sub_instructions = string.split()

                anchor_child = sub_instructions[0]
                anchor_parent = sub_instructions[1]
        
                coords_raw = string.split("(")                                  # -> (ciao) (pippo) = ["ciao) ", "pippo)"]
                coords_ref = [string.split(")")[0] for string in coords_raw]    # -> ["ciao) ", "pippo)"] = ["ciao", "pippo"]

                x_offset = analyze_string_coordinate(coords_ref[1]) # il numero 0 sono le anchor, 1 è X e 2 è Y
                y_offset = analyze_string_coordinate(coords_ref[2]) 

                match anchor_parent:
                    case "lu":
                        anchor_parent_coords = (coords_parent[0] + 0,                    coords_parent[1] + 0)    
                    case "cu":
                        anchor_parent_coords = (coords_parent[0] + coords_parent[2] / 2,  coords_parent[1] + 0)    
                    case "ru":
                        anchor_parent_coords = (coords_parent[0] + coords_parent[2],      coords_parent[1] + 0)    
                    case "lc":
                        anchor_parent_coords = (coords_parent[0] + 0,                    coords_parent[1] + coords_parent[3] / 2)    
                    case "cc":
                        anchor_parent_coords = (coords_parent[0] + coords_parent[2] / 2,  coords_parent[1] + coords_parent[3] / 2)    
                    case "rc":
                        anchor_parent_coords = (coords_parent[0] + coords_parent[2],      coords_parent[1] + coords_parent[3] / 2)    
                    case "ld":
                        anchor_parent_coords = (coords_parent[0] + 0,                    coords_parent[1] + coords_parent[3])    
                    case "cd":
                        anchor_parent_coords = (coords_parent[0] + coords_parent[2] / 2,  coords_parent[1] + coords_parent[3])    
                    case "rd":
                        anchor_parent_coords = (coords_parent[0] + coords_parent[2],      coords_parent[1] + coords_parent[3]) 

                self.coords[0] = anchor_parent_coords[0] + x_offset
                self.coords[1] = anchor_parent_coords[1] + y_offset

                return analyze_anchor_coordinate(anchor_child, self.coords, None)



        # estraggo informazioni su x, y, w, h
        self.x = analyze_string_coordinate(new_x)
        self.y = analyze_string_coordinate(new_y)
        self.w = analyze_string_coordinate(new_w)
        self.h = analyze_string_coordinate(new_h)

        self.coords = [self.x, self.y, self.w, self.h]
        self.ori_coords = (new_x, new_y, new_w, new_h, anchor_point)
        
        # aggiusto la posizione in base all'ancoraggio se diverso dal default
        if anchor_point != "lu":
            if type(anchor_point) == str:
                self.x, self.y = analyze_anchor_coordinate(anchor_point, self.coords, None)
            elif type(anchor_point) == tuple:
                self.x, self.y = analyze_anchor_coordinate(anchor_point[0], self.coords, anchor_point[1].coords)

            self.coords[0] = self.x
            self.coords[1] = self.y


        # aggiusto per posizione del context menù
        self.x += self.x_Context
        self.y += self.y_Context

        self.bounding_box = pygame.Rect(self.x, self.y, self.w, self.h)


    def hide_plus_children(self, booleano):
        self.hide = booleano



class Label_Text(BaseElement):

    def __init__(self, x="", y="", anchor="lu", w="", h="", text="", hide=False, color_text=[200, 200, 200], latex_font=False) -> None:
        super().__init__(x, y, anchor, w, h, text, hide, color_text, latex_font=latex_font)
        self.debug = False


    def disegnami(self, logica, rotation=0, DANG_surface=None, DANG_offset_x=0, DANG_offset_y=0):

        surface_to_use = self.schermo if DANG_surface is None else DANG_surface

        if self.need_update:
            self.recalc_geometry(*self.ori_coords)

        if not self.hide:

            # sostituzione caratteri speciali
            testo_analisi = SubStringa.analisi_caratteri_speciali(self.testo)

            self.testo_diplayed = ["", 0]
            
            for index, frase in enumerate(testo_analisi.split("\n")):

                self.testo_diplayed[1] += 1                

                # offset multi-riga
                offset_frase = index * self.font.font_pixel_dim[1]
        
                # analisi dei tag composti da "\tag{...}"
                elenco_substringhe: list[SubStringa] = SubStringa.start_analize(frase)
                
                original_spacing_x = self.font.font_pixel_dim[0]
                original_spacing_y = self.font.font_pixel_dim[1]

                offset_orizzontale = 0
                offset_orizzontale_apice = 0
                offset_orizzontale_pedice = 0

                iteration_lenght = 0

                testo_diplayed_iteration = ""
                for substringa_analizzata in elenco_substringhe:

                    if substringa_analizzata.pedice or substringa_analizzata.apice:
                        testo_diplayed_iteration += substringa_analizzata.testo[:int(len(substringa_analizzata.testo) / 2)]
                    else:
                        testo_diplayed_iteration += substringa_analizzata.testo

                    if substringa_analizzata.pedice or substringa_analizzata.apice:
                        self.font.scala_font(0.5)

                    if substringa_analizzata.apice:
                        offset_highlight = - 1 / 2
                        offset_usato = offset_orizzontale_apice  

                    elif substringa_analizzata.pedice:
                        offset_highlight = - 1 / 2                            
                        offset_usato = offset_orizzontale_pedice 

                    else:
                        offset_highlight = - 1

                        offset_usato = offset_orizzontale
                        offset_orizzontale_apice = offset_orizzontale
                        offset_orizzontale_pedice = offset_orizzontale

                    if substringa_analizzata.colore is None: substringa_analizzata.colore = self.color_text

                    offset_pedice_apice = original_spacing_y * 0.5 if substringa_analizzata.pedice else - original_spacing_y * 0.1 if substringa_analizzata.apice else 0

                    if substringa_analizzata.highlight and not self.latex_font:
                        pre_rotation = self.font.font_pyg_r.render("" + "█" * (len(substringa_analizzata.testo)) + "", True, [100, 100, 100])
                        if rotation != 0:
                            pre_rotation = pygame.transform.rotate(pre_rotation, rotation)
                        surface_to_use.blit(pre_rotation, (self.x + original_spacing_x * offset_highlight + offset_usato + DANG_offset_x, self.y + offset_frase + offset_pedice_apice + DANG_offset_y))

                    if substringa_analizzata.bold:
                        pre_rotation = self.font.font_pyg_b.render(substringa_analizzata.testo, True, substringa_analizzata.colore)
                        if rotation != 0:
                            pre_rotation = pygame.transform.rotate(pre_rotation, rotation)
                        surface_to_use.blit(pre_rotation, (self.x + offset_usato + DANG_offset_x, self.y + offset_frase + offset_pedice_apice + DANG_offset_y))
                    elif substringa_analizzata.italic:
                        pre_rotation = self.font.font_pyg_i.render(substringa_analizzata.testo, True, substringa_analizzata.colore)
                        if rotation != 0:
                            pre_rotation = pygame.transform.rotate(pre_rotation, rotation)
                        surface_to_use.blit(pre_rotation, (self.x + offset_usato + DANG_offset_x, self.y + offset_frase + offset_pedice_apice + DANG_offset_y))
                    else:
                        pre_rotation = self.font.font_pyg_r.render(substringa_analizzata.testo, True, substringa_analizzata.colore)
                        if rotation != 0:
                            pre_rotation = pygame.transform.rotate(pre_rotation, rotation)
                        surface_to_use.blit(pre_rotation, (self.x + offset_usato + DANG_offset_x, self.y + offset_frase + offset_pedice_apice + DANG_offset_y))
                    

                    font_usato = self.font.font_pyg_i if substringa_analizzata.italic else (self.font.font_pyg_b if substringa_analizzata.bold else self.font.font_pyg_r)
                    
                    if substringa_analizzata.apice: offset_orizzontale_apice += substringa_analizzata.end(font_usato)
                    elif substringa_analizzata.pedice: offset_orizzontale_pedice += substringa_analizzata.end(font_usato)
                    else:
                        offset_orizzontale_apice += substringa_analizzata.end(font_usato)
                        offset_orizzontale_pedice += substringa_analizzata.end(font_usato)

                    if substringa_analizzata.pedice or substringa_analizzata.apice:
                        self.font.scala_font(2)

                    offset_orizzontale = max(offset_orizzontale_apice, offset_orizzontale_pedice)

                    iteration_lenght += substringa_analizzata.end(font_usato)

                    if max(len(self.testo_diplayed[0]), len(testo_diplayed_iteration)) == len(testo_diplayed_iteration):
                        self.testo_diplayed[0] = testo_diplayed_iteration


    def change_text(self, text):
        if self.latex_font:
            old_text = self.testo
            self.testo = text
            if old_text != self.testo:
                self.need_update = True
        else:
            if len(text) != len(self.testo):
                self.need_update = True
            self.testo = text



class Bottone_Push(BaseElement):

    def __init__(self, x="", y="", anchor="lu", w="", h="", function=None, text="", hide=False, disable=False) -> None:
        super().__init__(x, y, anchor, w, h, text, hide)

        self.contorno = 2

        self.callback = function
        self.flag_foo = False

        if self.callback is None:
            def Fuffa(self): ...
            self.callback = Fuffa

        # SUPPORTO PATHS
        self.paths: list[str] = []

        self.animazione = Animazione(100, "once")
        self.hover = False

        self.disable: bool = disable
        self.suppress_animation: bool = False

        self.label_title = Label_Text(anchor=("cc cc (0px) (0px)", self), w="-*w", h="-*h", text=text, hide=hide)

        self.smussatura = 20
        self.debug = False

        self.texture = None
        self.texture_name = None

    
    def load_texture(self, name: str = None):

        if self.texture_name is None and not name is None:
            self.texture_name = name
    
        if name is None:
            path = os.path.join(f"TEXTURES", f'{self.texture_name}.png')
        else:
            path = os.path.join(f"TEXTURES", f'{name}.png')
        
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.w, self.h))


    def disegnami(self, logica: 'Logica'):


        if not self.hide:

            colore = self.bg.copy()
            
            if not self.disable:
                colore = self.animazione_press(logica.dt, colore)
                colore = self.animazione_hover(colore)

            colore = [s_colore if s_colore <= 255 else 255 for s_colore in colore]

            pygame.draw.rect(self.schermo, colore, [self.x, self.y, self.w, self.h], self.contorno, self.smussatura)

            if self.texture is None:
                self.label_title.disegnami(logica)
            else:
                self.schermo.blit(self.texture, (self.x, self.y))


        if self.debug:
            pygame.draw.circle(self.schermo, [255, 0, 0], self.lu, 5)
            pygame.draw.circle(self.schermo, [255, 0, 0], self.lc, 5)
            pygame.draw.circle(self.schermo, [255, 0, 0], self.ld, 5)
            pygame.draw.circle(self.schermo, [255, 0, 0], self.cu, 5)
            pygame.draw.circle(self.schermo, [255, 0, 0], self.cc, 5)
            pygame.draw.circle(self.schermo, [255, 0, 0], self.cd, 5)
            pygame.draw.circle(self.schermo, [255, 0, 0], self.ru, 5)
            pygame.draw.circle(self.schermo, [255, 0, 0], self.rc, 5)
            pygame.draw.circle(self.schermo, [255, 0, 0], self.rd, 5)
    

    def eventami(self, events: list['Event'], logica: 'Logica'):

        if self.hide == False or self.disable == False:

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.bounding_box.collidepoint(event.pos):
                        self.callback(self)
                        self.animazione.riavvia()

            self.hover = True if self.bounding_box.collidepoint(logica.mouse_pos) else False
                    

    def animazione_press(self, dt: int, colore):
        
        if self.animazione.update(dt):

            if not self.suppress_animation:
                colore += 20
                self.contorno = 0

        else: 
            if not self.suppress_animation:
                self.contorno = 2
        
        return colore


    def animazione_hover(self, colore):
        if self.hover:
            if not self.suppress_animation:
                colore += 10
                self.contorno = 0
        else:
            if not self.suppress_animation:
                self.contorno = 2

        return colore


    def change_text(self, text):
        super().change_text(text)

    
    def update_context_menu(self, *args):
        super().update_context_menu(*args)
        self.label_title.update_context_menu(*args)


    def update_window_change(self):
        super().update_window_change()
        try:
            self.load_texture()
        except FileNotFoundError:
            ...
        self.label_title.update_window_change()


    def hide_plus_children(self, booleano):
        super().hide_plus_children(booleano)
        self.disable = booleano


        
class Bottone_Toggle(BaseElement):
    def __init__(self, x="", y="", anchor="lu", w="", h="", state=False, type_checkbox=True, text="", hide=False, disable=False, text_on_right=True) -> None:
        super().__init__(x, y, anchor, w, h, text, hide)
        
        self.contorno = 2

        if type_checkbox:
            if text_on_right:
                self.label_title = Label_Text(anchor=("lc rc (10px) (0px)", self), w="-*w", h="-*h", text=text)
            else:
                self.label_title = Label_Text(anchor=("rc lc (-10px) (0px)", self), w="-*w", h="-*h", text=text)
        else:
            self.label_title = Label_Text(anchor=("cc cc (0px) (0px)", self), w="-*w", h="-*h", text=text)


        self.checkbox = type_checkbox

        self.state_toggle = state

        self.animazione = Animazione(-1, "once")
        self.hover = False

        self.disable: bool = False

        self.smussatura = 5

        self.texture = None
        self.texture_name = None

    
    def load_texture(self, name: str = None):

        if self.texture_name is None and not name is None:
            self.texture_name = name
    
        if name is None:
            path = os.path.join(f"TEXTURES", f'{self.texture_name}.png')
        else:
            path = os.path.join(f"TEXTURES", f'{name}.png')
        
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.w, self.h))


    def disegnami(self, logica):

        if not self.hide:

            colore = self.bg.copy()

            colore = self.animazione_press(colore)
            colore = self.animazione_hover(colore)

            if self.checkbox:

                pygame.draw.rect(self.schermo, colore, [self.x, self.y, self.w, self.h], self.contorno, self.smussatura)

                if self.state_toggle:
                    pygame.draw.rect(self.schermo, [255, 255, 255], [self.x + 4, self.y + 4, self.w - 8, self.h - 8], self.contorno, self.smussatura)


                self.label_title.disegnami(logica)
            
            else:

                pygame.draw.rect(self.schermo, colore, [self.x, self.y, self.w, self.h], self.contorno, self.smussatura)
                
                if self.texture is None:
                    self.label_title.disegnami(logica)
                else:
                    self.schermo.blit(self.texture, (self.x, self.y))


    def eventami(self, events: list['Event'], logica: 'Logica'):

        if not self.hide:

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.bounding_box.collidepoint(event.pos):
                        
                        if self.state_toggle:
                            self.state_toggle = False
                        else:
                            self.state_toggle = True

            self.hover = True if self.bounding_box.collidepoint(logica.mouse_pos) else False


    def animazione_press(self, colore):
        if self.state_toggle:
            
            self.contorno = 0
            colore += 20

        else: 
            self.contorno = 2
        
        return colore


    def animazione_hover(self, colore):
        if self.hover:
            self.contorno = 0
            colore += 10
        elif not self.state_toggle:
            self.contorno = 2
        return colore


    def update_context_menu(self, *args):
        super().update_context_menu(*args)
        self.label_title.update_context_menu(*args)


    def update_window_change(self):
        super().update_window_change()
        try:
            self.load_texture()
        except FileNotFoundError:
            ...
        self.label_title.update_window_change()



class RadioButton(BaseElement):
    def __init__(self, x="", y="", anchor="lu", w="", h="", axis="x", bg=None, cb_n=1, cb_s=[False], cb_t=["Default item"], title="", multiple_choice=False, hide=False, type_checkbox=True, w_button="30px", h_button="30px") -> None:
        super().__init__(x, y, anchor, w, h, title, hide)

        if not bg is None:
            self.bg = bg

        self.main_ax = axis
        
        self.title = title
        self.multiple_choice = multiple_choice

        self.hide = hide

        self.type_checkbox = type_checkbox

        self.cb_n, self.cb_s, self.cb_t = cb_n, cb_s, cb_t

        self.w_button, self.h_button = w_button, h_button
        
        self.toggles: list[Bottone_Toggle] = []

        self.w_button_calcoli, self.h_button_calcoli = self.w_button, self.h_button

        if self.w_button[-2:] == "%w":
            self.w_button_calcoli = f"{float(self.w_button[:-2]) * self.one_percent_x}px"
        if self.w_button[-2:] == "%h":
            self.w_button_calcoli = f"{float(self.w_button[:-2]) * self.one_percent_y}px"
        if self.h_button[-2:] == "%w":
            self.h_button_calcoli = f"{float(self.h_button[:-2]) * self.one_percent_x}px"
        if self.h_button[-2:] == "%h":
            self.h_button_calcoli = f"{float(self.h_button[:-2]) * self.one_percent_y}px"
        
        for index, state, text  in zip(range(cb_n), cb_s, cb_t):
            
            match self.main_ax:
                case "x": 
                        spacing = (self.w - float(self.w_button_calcoli[:-2]) * cb_n) / (cb_n - 1)
                        self.toggles.append(Bottone_Toggle(f"{self.x}px {index * (float(self.w_button_calcoli[:-2]) + spacing)}px", f"{self.y}px", "lu", w_button, h_button, state, type_checkbox, text=text, hide=hide))
                case "y":
                        spacing = (self.h - float(self.h_button_calcoli[:-2]) * cb_n) / (cb_n - 1)
                        self.toggles.append(Bottone_Toggle(f"{self.x}px", f"{self.y}px {index * (float(self.h_button_calcoli[:-2]) + spacing)}px", "lu", w_button, h_button, state, type_checkbox, text=text, hide=hide))
                    
                case _: raise TypeError(f"Invalid mode {self.main_ax}, accepted types: 'x', 'y'.")
        
        for bottone in self.toggles:
            if bottone.state_toggle:
                bottone.bg = array([50, 100, 50])
            else:
                bottone.bg = self.bg + 10 



    def disegnami(self, logica):
        pygame.draw.rect(self.schermo, self.bg, [self.x, self.y, self.w, self.h], 0, 5)

        for bottone in self.toggles:
            if bottone.state_toggle:
                bottone.bg = array([50, 100, 50])
            else:
                bottone.bg = self.bg + 10

        [bottone.disegnami(logica) for bottone in self.toggles]


    def eventami(self, events, logica):

        old_state = self.buttons_state

        [bottone.eventami(events, logica) for bottone in self.toggles]
        
        new_state = self.buttons_state

        if not self.multiple_choice:
            ele_vecchio, ele_nuovo = self.check_for_diff(old_state, new_state)

            if not ele_nuovo is None and not ele_vecchio is None:
                self.toggles[ele_vecchio].state_toggle = False

        self.cb_s = [b.state_toggle for b in self.toggles]


    @property
    def buttons_state(self):
        return [bottone.state_toggle for bottone in self.toggles]


    def set_state(self, states):
        
        for bottone, stato in zip(self.toggles, states):
            bottone.state_toggle = stato


    def check_for_diff(self, list1, list2):

        elemento_vecchio = None
        elemento_nuovo = None

        for index, state1, state2 in zip(range(len(list1)), list1, list2):
            if state1 != state2:
                elemento_nuovo = index

            if state1 == state2 and state1 == 1:
                elemento_vecchio = index

        return elemento_vecchio, elemento_nuovo


    def update_window_change(self):
        super().update_window_change()

        textures_info = [bottone.texture_name for bottone in self.toggles]

        self.cb_n = len(self.toggles)
        self.cb_s = [bottone.state_toggle for bottone in self.toggles]
        self.cb_t = [bottone.testo for bottone in self.toggles]

        self.toggles = []

        if self.w_button[-2:] == "%w":
            self.w_button_calcoli = f"{float(self.w_button[:-2]) * self.one_percent_x}px"
        if self.w_button[-2:] == "%h":
            self.w_button_calcoli = f"{float(self.w_button[:-2]) * self.one_percent_y}px"
        if self.h_button[-2:] == "%w":
            self.h_button_calcoli = f"{float(self.h_button[:-2]) * self.one_percent_x}px"
        if self.h_button[-2:] == "%h":
            self.h_button_calcoli = f"{float(self.h_button[:-2]) * self.one_percent_y}px"
        
        for index, state, text  in zip(range(self.cb_n), self.cb_s, self.cb_t):
            
            match self.main_ax:
                case "x": 
                        spacing = (self.w - float(self.w_button_calcoli[:-2]) * self.cb_n) / (self.cb_n - 1)
                        self.toggles.append(Bottone_Toggle(f"{self.x}px {index * (float(self.w_button_calcoli[:-2]) + spacing)}px", f"{self.y}px", "lu", self.w_button_calcoli, self.h_button_calcoli, state, self.type_checkbox, text=text, hide=self.hide))
                case "y":
                        spacing = (self.h - float(self.h_button_calcoli[:-2]) * self.cb_n) / (self.cb_n - 1)
                        self.toggles.append(Bottone_Toggle(f"{self.x}px", f"{self.y}px {index * (float(self.h_button_calcoli[:-2]) + spacing)}px", "lu", self.w_button_calcoli, self.h_button_calcoli, state, self.type_checkbox, text=text, hide=self.hide))
                    
                case _: raise TypeError(f"Invalid mode {self.main_ax}, accepted types: 'x', 'y'.")
        
            self.toggles[-1].x_Context = self.x_Context
            self.toggles[-1].y_Context = self.y_Context
            self.toggles[-1].w_Context = self.w_Context
            self.toggles[-1].h_Context = self.h_Context

            if not textures_info[index] is None:
                self.toggles[-1].load_texture(textures_info[index])

        for bottone in self.toggles:
            if bottone.state_toggle:
                bottone.bg = array([50, 100, 50])
            else:
                bottone.bg = self.bg + 10 



class Entrata(BaseElement):
    def __init__(self, x="", y="", anchor="lu", w="", h="", text="", title="Entrata", hide=False, lunghezza_max=None, solo_numeri=False, num_valore_minimo=None, num_valore_massimo=None, is_hex=False) -> None:       
        super().__init__(x, y, anchor, w, h, text, hide)

        self.contorno = 0

        self.label_title = Label_Text(anchor=("rc lc (-10px) (0)", self), w="-*w", h="-*h", color_text=[i / 2 for i in self.color_text], text=title)

        self.offset_grafico_testo = 5
        self.puntatore_pos = 0
        self.highlight_region: list[int] = [0, 0]

        self.selezionato = False
        self.hover = False

        self.previous_text: str = ""

        self.lunghezza_max = lunghezza_max
        self.solo_numeri = solo_numeri
        self.num_valore_minimo = num_valore_minimo
        self.num_valore_massimo = num_valore_massimo
        self.is_hex = is_hex
        self.input_error = False
        self.return_previous_text = False

        self.animazione_puntatore = Animazione(1000, "loop")
        self.animazione_puntatore.attiva = True



    def disegnami(self, logica: 'Logica'):

        if not self.hide:

            colore = self.bg.copy()

            colore = self.animazione_press(colore)
            colore = self.animazione_hover(colore)

            self.label_title.disegnami(logica)

            pygame.draw.rect(self.schermo, colore, [self.x, self.y, self.w, self.h], self.contorno, 5)

            if self.selezionato:
                pygame.draw.rect(self.schermo, [90, 90, 90], [self.x + self.font.font_pixel_dim[0] * self.highlight_region[0] + self.offset_grafico_testo, self.y, self.font.font_pixel_dim[0] * (self.highlight_region[1] - self.highlight_region[0]), self.h], 0, 5)

            # testo
            self.schermo.blit(self.font.font_pyg_r.render(self.testo, True, self.color_text), (self.x + self.offset_grafico_testo, self.y + self.h / 2 - self.font.font_pixel_dim[1] / 2))

            # puntatore flickerio
            self.animazione_puntatore.update(logica.dt)
            if self.selezionato and self.animazione_puntatore.dt < 500:
                offset_puntatore_pos = self.font.font_pixel_dim[0] * self.puntatore_pos
                pygame.draw.rect(self.schermo, self.color_text, [self.x + self.offset_grafico_testo + offset_puntatore_pos, self.y, 2, self.h], 0)


    def eventami(self, events: list['Event'], logica: 'Logica'):
        
        if not self.hide:

            if self.selezionato:
                self.return_previous_text = True
                self.eventami_scrittura(events, logica)

                if self.solo_numeri:
                    numero_equivalente = MateUtils.inp2flo(self.testo, None)

                    if numero_equivalente is None:
                        self.color_text = array([255, 0, 0])
                    else:
                        self.color_text = array([200, 200, 200])


            else:
                self.return_previous_text = False
                self.previous_text = self.testo

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.bounding_box.collidepoint(event.pos):
                            
                            if self.selezionato:
                                self.highlight_region = [0, 0]
                                self.update_puntatore_pos(event.pos)
                            else:    
                                self.selezionato = True
                                self.highlight_region = [len(self.testo), 0]
                                self.puntatore_pos = len(self.testo)

                            self.animazione_puntatore.riavvia()

                        else:
                            self.selezionato = False
                            self.highlight_region = [0, 0]
                            

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.bounding_box.collidepoint(event.pos):
                            if self.selezionato:
                                self.animazione_puntatore.riavvia()
                            

                # selected
                if logica.dragging and self.selezionato:

                    self.highlight_region[0] = self.get_puntatore_pos(logica.mouse_pos[0])
                    self.highlight_region[1] = self.get_puntatore_pos(logica.original_start_pos[0])
                    self.update_puntatore_pos(logica.mouse_pos)
                    self.animazione_puntatore.riavvia()

            self.hover = True if self.bounding_box.collidepoint(logica.mouse_pos) else False


    def eventami_scrittura(self, events: list['Event'], logica: 'Logica'):
        
        if not self.hide:

            def move_selected(dir: bool, amount: int = 1):
                if dir:
                    if self.highlight_region == [0, 0]:
                        self.highlight_region = [self.puntatore_pos, self.puntatore_pos]

                    if self.highlight_region[0] < len(self.testo):
                        self.highlight_region[0] += amount
                
                else:
                    if self.highlight_region == [0, 0]:
                        self.highlight_region = [self.puntatore_pos, self.puntatore_pos]

                    if self.highlight_region[0] > 0:
                        self.highlight_region[0] -= amount


            def find_ricercatore(self: Entrata, dir: bool):

                elenco_ricercatori = [" ", "\\", "/", ",", ".", "-", "{", "}", "[", "]", "(", ")"]

                if dir:
                    # movimento verso destra
                    dst = len(self.testo)
                    for ricercatore in elenco_ricercatori:
                        candidato = self.testo.find(ricercatore, self.puntatore_pos + 1)
                        if candidato >= 0:
                            dst = min(candidato, dst)

                else:
                    # movimento verso sinistra
                    dst = 0
                    for ricercatore in elenco_ricercatori:
                        candidato = self.testo[:self.puntatore_pos].rfind(ricercatore)
                        if candidato >= 0:
                            dst = max(candidato, dst)

                return dst


            reset_animation = False


            # SINGOLI TASTI
            # --------------------------------------------------------------------------------------------------------------------------
            lunghezza_testo_execute = False

            if self.lunghezza_max is None:
                lunghezza_testo_execute = True
            
            elif len(self.testo) < self.lunghezza_max:
                lunghezza_testo_execute = True

            for event in events:
                
                if event.type == pygame.TEXTINPUT:

                    if lunghezza_testo_execute:
                        apertura = ""
                        chiusura = ""

                        if event.text == '{' or event.text == "[" or event.text == "(" or event.text == '"':
                            apertura = event.text
                            match event.text:
                                case "{": chiusura = "}"
                                case "[": chiusura = "]"
                                case "(": chiusura = ")"
                                case '"': chiusura = '"'



                        if self.highlight_region != [0, 0]:

                            min_s = min(self.highlight_region[0], self.highlight_region[1])
                            max_s = max(self.highlight_region[0], self.highlight_region[1])
                            
                            if apertura != "":
                                self.testo = self.testo[:min_s] + apertura + self.testo[min_s : max_s] + chiusura + self.testo[max_s:]
                                self.highlight_region[0] += 1
                                self.highlight_region[1] += 1
                                self.puntatore_pos += 1

                            else:
            
                                self.testo = self.testo[:min_s] + event.text + self.testo[max_s:]
                                self.puntatore_pos = len(self.testo[:min_s]) + len(event.text)
                                self.highlight_region = [0, 0]

                        else:
                            if apertura != "":
                                self.testo = self.testo[:self.puntatore_pos] + apertura + chiusura + self.testo[self.puntatore_pos:]
                            else:
                                self.testo = self.testo[:self.puntatore_pos] + event.text + self.testo[self.puntatore_pos:]
            
                            self.puntatore_pos += len(event.text)

                        
                        reset_animation = True
                
                if event.type == pygame.KEYDOWN:

                    # copia, incolla e taglia       
                    if logica.ctrl and event.key == pygame.K_c:
                        
                        min_s = min(self.highlight_region[0], self.highlight_region[1])
                        max_s = max(self.highlight_region[0], self.highlight_region[1])

                        pyperclip.copy(self.testo[min_s : max_s])
                    
                        self.highlight_region = [0, 0]

                    if lunghezza_testo_execute:
                        if logica.ctrl and event.key == pygame.K_v:
                        
                            incolla = pyperclip.paste()
                            self.testo = f"{self.testo[:self.puntatore_pos]}{incolla}{self.testo[self.puntatore_pos:]}"
                            self.puntatore_pos = len(self.testo[:self.puntatore_pos]) + len(incolla)

                            self.highlight_region = [0, 0]
                    
                    if logica.ctrl and event.key == pygame.K_x:
                        
                        if self.highlight_region != [0, 0]:
                            min_s = min(self.highlight_region[0], self.highlight_region[1])
                            max_s = max(self.highlight_region[0], self.highlight_region[1])

                            pyperclip.copy(self.testo[min_s : max_s])
                        
                            self.highlight_region = [0, 0]
                            
                            self.testo = self.testo[:min_s] + self.testo[max_s:]
                            self.puntatore_pos = len(self.testo[:min_s])
    

                    # HOME and END
                    if event.key == pygame.K_HOME:
                        if logica.shift:
                            self.highlight_region = [self.puntatore_pos, 0]
                        else:
                            self.highlight_region = [0, 0]
                        self.puntatore_pos = 0
                        reset_animation = True

                    

                    if event.key == pygame.K_END:
                        if logica.shift:
                            self.highlight_region = [self.puntatore_pos, len(self.testo)]
                        else:
                            self.highlight_region = [0, 0]
                        self.puntatore_pos = len(self.testo)
                        reset_animation = True

                    
                    # ESC
                    if event.key == pygame.K_ESCAPE:
                        self.highlight_region = [0, 0]


                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        reset_animation = True

                        if self.highlight_region[1] - self.highlight_region[0] != 0:

                            min_s = min(self.highlight_region[0], self.highlight_region[1])
                            max_s = max(self.highlight_region[0], self.highlight_region[1])

                            self.testo = self.testo[:min_s] + self.testo[max_s:]

                            self.puntatore_pos = min_s
                            self.highlight_region = [0, 0]

                        
                        elif event.key == pygame.K_DELETE:
                            if self.puntatore_pos < len(self.testo):
                                self.testo = self.testo[:self.puntatore_pos] + self.testo[self.puntatore_pos + 1:]

                        elif event.key == pygame.K_BACKSPACE:

                            if logica.ctrl:

                                nuovo_puntatore = find_ricercatore(self, 0)

                                text2eli = self.testo[nuovo_puntatore : self.puntatore_pos]
                                self.puntatore_pos = nuovo_puntatore
                                self.testo = self.testo[:nuovo_puntatore] + self.testo[nuovo_puntatore:].replace(text2eli, "", 1)
                                
                            else:
                                if self.puntatore_pos != 0:
                                    self.testo = self.testo[:self.puntatore_pos-1] + self.testo[self.puntatore_pos:]
                                if self.puntatore_pos > 0:
                                    self.puntatore_pos -= 1
                            

                    if event.key == pygame.K_LEFT:

                        if self.puntatore_pos > 0:
                            
                            if logica.ctrl:
                                
                                puntatore_left = find_ricercatore(self, 0)
                                
                                if logica.shift:

                                    move_selected(0, self.puntatore_pos - puntatore_left)
                
                                else:
                                    reset_animation = True
                                    self.highlight_region = [0, 0]

                                self.puntatore_pos = puntatore_left

                            else: 

                                if logica.shift:

                                    move_selected(0)
                
                                else:
                                    reset_animation = True
                                    self.highlight_region = [0, 0]

                                self.puntatore_pos -= 1


                    if event.key == pygame.K_RIGHT:

                        if self.puntatore_pos < len(self.testo):
                            
                            if logica.ctrl:
                                
                                puntatore_right = find_ricercatore(self, 1)
                                
                                if logica.shift:

                                    move_selected(1, puntatore_right - self.puntatore_pos)
                
                                else:
                                    reset_animation = True
                                    self.highlight_region = [0, 0]

                                self.puntatore_pos = puntatore_right

                            else: 

                                if logica.shift:

                                    move_selected(1)
                
                                else:
                                    reset_animation = True
                                    self.highlight_region = [0, 0]

                                self.puntatore_pos += 1

                        else:
                            reset_animation = True
                            self.highlight_region = [0, 0]


            if logica.backspace:
                logica.acc_backspace += logica.dt
                if logica.acc_backspace > 500:
                    if self.puntatore_pos != 0:
                        self.testo = self.testo[:self.puntatore_pos-1] + self.testo[self.puntatore_pos:]
                    if self.puntatore_pos > 0:
                        self.puntatore_pos -= 1
                        reset_animation = True
                    logica.acc_backspace -= 50
            else: 
                logica.acc_backspace = 0

            if logica.left:
                logica.acc_left += logica.dt
                if logica.acc_left > 500:
                    reset_animation = True 
                    if self.puntatore_pos > 0:
                        self.puntatore_pos -= 1
                        if logica.shift:
                            move_selected(0)
                    logica.acc_left -= 50
            else: 
                logica.acc_left = 0
            
            if logica.right:
                logica.acc_right += logica.dt
                if logica.acc_right > 500:
                    reset_animation = True
                    if self.puntatore_pos < len(self.testo):
                        self.puntatore_pos += 1
                        if logica.shift:
                            move_selected(1)
                    logica.acc_right -= 50
            else: 
                logica.acc_right = 0

            if reset_animation:
                self.animazione_puntatore.riavvia()


    def update_puntatore_pos(self, pos: tuple[int]):
        x, y = pos
        
        self.puntatore_pos = self.get_puntatore_pos(x)


    def get_puntatore_pos(self, x: int):
        ris = round((x - self.x - self.offset_grafico_testo) / (self.font.font_pixel_dim[0]))
    
        if ris > len(self.testo):
            ris = len(self.testo)
        elif ris < 0:
            ris = 0

        return ris


    def animazione_press(self, colore):
        if self.selezionato:
            
            self.contorno = 0
            colore += 20

        else: 
            self.contorno = 0
        
        return colore


    def animazione_hover(self, colore):
        if self.hover:
            self.contorno = 0
            colore += 10
        elif not self.selezionato:
            self.contorno = 0
        return colore
    

    def change_text(self, text):
        self.testo = text


    def get_text(self) -> str:
        if self.return_previous_text:
            restituisco = f"{self.previous_text}"
        else:
            restituisco = f"{self.testo}"
        
        if self.solo_numeri:
            numero_equivalente = MateUtils.inp2flo(restituisco, None)

            if numero_equivalente is None:
                self.color_text = array([255, 0, 0])
                return self.num_valore_minimo

            else:
                self.color_text = array((200, 200, 200))

                if numero_equivalente > self.num_valore_massimo:
                    self.change_text(f"{self.num_valore_massimo}")
                    return self.get_text()
                elif numero_equivalente < self.num_valore_minimo:
                    self.change_text(f"{self.num_valore_minimo}")
                    return self.get_text()
                else:
                    return restituisco


        elif self.is_hex:
            if MateUtils.hex2rgb(restituisco, std_return=None) is None:
                self.color_text = array([255, 0, 0])
                return "aaaaaa"
            else:
                self.color_text = array([200, 200, 200])
                return restituisco

        else:
            return restituisco


    def update_context_menu(self, *args):
        super().update_context_menu(*args)
        self.label_title.update_context_menu(*args)


    def update_window_change(self):
        super().update_window_change()
        self.label_title.update_window_change()



class Scroll(BaseElement):
    def __init__(self, x="", y="", anchor="lu", w="", h="", text="Scroll console...", hide=False) -> None:
        super().__init__(x, y, anchor, w, h, text, hide)

        self.label_title = Label_Text(anchor=("lu lu (10px) (10px)", self), w=w, h="40px", text=text, hide=hide)
        self.color_text_selected = (40, 100, 40)

        self.bg_selected = (60, 70, 70)
        
        self.contorno = 2

        self.no_dragging_animation = False

        # self.elementi = [f"{i}" for i in range(100)]
        self.elementi = []
        self.ele_mask = [False for _ in range(len(self.elementi))]
        self.ele_selected_index = 0
        self.ele_first = 0
        
        self.ele_max = int((self.h - self.label_title.font.font_pixel_dim[1] * 2) // self.label_title.font.font_pixel_dim[1])

        # creazione toggles
        self.ele_toggle = [Bottone_Toggle(anchor=(f"lu lu ({self.w * 0.01}px) ({self.label_title.font.font_pixel_dim[1] * (i + 2)}px)", self), w=f"{self.label_title.font.font_pixel_dim[1]}px", h=f"{self.label_title.font.font_pixel_dim[1]}px", state=False, text="") for i in range(self.ele_max)]

        for ele in self.ele_toggle:
            ele.bg += array([10, 10, 10])

        self.offset_grafico_testo = self.w * 0.02 + self.ele_toggle[0].w

        self.selezionato = False
        self.hover = False

        self.animazione_puntatore = Animazione(1000, "loop")
        self.animazione_puntatore.attiva = True

        # self.bounding_box = pygame.Rect(self.x + self.offset_grafico_testo, self.y, self.w - self.offset_grafico_testo, self.h)
        self.bounding_box = pygame.Rect(self.x, self.y, self.w, self.h)
        

    def add_element_scroll(self, element: str, stato: bool):
        self.elementi.append(element)
        self.ele_mask.append(stato)


    def remove_selected_item(self):
        if len(self.elementi) > 0:
            self.elementi.pop(self.ele_selected_index)
            self.ele_mask.pop(self.ele_selected_index)
            if self.ele_selected_index == len(self.elementi) and self.ele_selected_index > 0:
                self.ele_selected_index -= 1

                if self.elemento_attivo < 0:
                    self.ele_first -= 1


    @property
    def elemento_attivo(self):
        elemento = self.ele_selected_index - self.ele_first
        return elemento


    def disegnami(self, logica: 'Logica'):

        if not self.hide:

            pygame.draw.rect(self.schermo, self.bg, [self.x, self.y, self.w, self.h], 0, 5)
            
            self.label_title.disegnami(logica)

            # creazione elementi (righe)
            alt_font = self.label_title.font.font_pixel_dim[1]

            for chunck in range(int((self.h - alt_font * 2) // alt_font)):
                
                if self.ele_selected_index == chunck + self.ele_first:
                    colore = self.bg_selected
                else:
                    colore_bg = self.bg.copy()
                    colore_var1 = colore_bg + 10
                    colore_var2 = colore_bg + 20
                    colore = colore_var1 if chunck % 2 == 0 else colore_var2

                if self.ele_first + chunck < len(self.elementi):
                    pygame.draw.rect(self.schermo, colore, [self.x + self.offset_grafico_testo, (self.y + alt_font * 2) + alt_font * chunck, self.w - self.offset_grafico_testo, alt_font], 0, 5)
                
        

            # creazione elementi (testo)
            self.ele_max = int((self.h - alt_font * 2) // alt_font)
            for ele_iterator in range(self.ele_max):
                
                if self.ele_first + ele_iterator >= len(self.elementi):
                    break

                testo = f"{self.elementi[self.ele_first + ele_iterator]}"

                if self.ele_selected_index == ele_iterator + self.ele_first:
                    colore = self.color_text_selected
                else:
                    colore = self.color_text
                    

                self.schermo.blit(self.label_title.font.font_pyg_r.render(testo, True, colore), (self.x + self.offset_grafico_testo + 5, self.y + (alt_font * (2 + ele_iterator))))
            

            # creazione toggles
            [bottone.disegnami(logica) for bottone in self.ele_toggle]

            # disegno elementi grafici di drag
            if logica.dragging and not self.no_dragging_animation:

                if self.bounding_box.collidepoint(logica.mouse_pos):

                    pygame.draw.rect(self.schermo, self.bg_selected, [logica.mouse_pos[0], logica.mouse_pos[1], self.w - self.offset_grafico_testo, self.label_title.font.font_pixel_dim[1]], 0, 5)
                    self.schermo.blit(self.label_title.font.font_pyg_r.render(f"{self.elementi[self.ele_selected_index]}", True, self.color_text_selected), (logica.mouse_pos[0] + 5, logica.mouse_pos[1]))

                    # mostro dove finisce l'elemento
                    elemento_finale = round((logica.mouse_pos[1] - self.y - self.label_title.font.font_pixel_dim[1] // 2) // self.label_title.font.font_pixel_dim[1]) - 2 + 1 # il +1 è per risolvere un problema grafico in cui il calcolo non tiene conto che l'operazione non è ancora stata eseguita
                    pygame.draw.rect(self.schermo, [255, 200, 0], [self.x + self.offset_grafico_testo, (self.y + alt_font * 2) + alt_font * elemento_finale, self.w - self.offset_grafico_testo, 1], 0, 5)



    def eventami(self, events: list['Event'], logica: 'Logica'):
        
        if not self.hide:

            # aggiorna tutto quello che succede alle toggle box
            [bottone.eventami(events, logica) for bottone in self.ele_toggle]

            # nascondo le toggle box che non corrispondono a nessun elemento (fine corsa)
            for i in range(self.ele_max):
                if self.ele_first + i < len(self.elementi):
                    self.ele_toggle[i].hide = False
                    self.ele_mask[self.ele_first + i] = self.ele_toggle[i].state_toggle
                elif self.ele_first + i >= len(self.elementi):
                    self.ele_toggle[i].hide = True
            

            if self.bounding_box.collidepoint(logica.mouse_pos):

                for event in events:

                    if event.type == pygame.MOUSEBUTTONDOWN:
                    
                        if event.button == 1:
                            # selezione elemento
                            self.ele_selected_index = self.ele_first + round((logica.mouse_pos[1] - self.y) // self.label_title.font.font_pixel_dim[1]) - 2
                            self.no_dragging_animation = False

                            # abilita / disabilita visualizzazione dragging element nel caso di swap posizioni
                            if self.ele_selected_index > len(self.elementi) - 1:
                                self.no_dragging_animation = True

                            # impedisce la selezione di elementi oltre al range consentito
                            if self.ele_selected_index >= len(self.elementi) - 1:
                                self.ele_selected_index = len(self.elementi) - 1


                        if event.button == 4:
                            # scroll down
                            if self.ele_first > 0:
                                self.ele_first -= 1

                                for bottone, status in zip(self.ele_toggle, self.ele_mask[self.ele_first : self.ele_first + self.ele_max]):
                                    bottone.state_toggle = status

                        if event.button == 5:
                            # scroll up
                            if self.ele_first < len(self.elementi) - 1:
                                self.ele_first += 1

                                for bottone, status in zip(self.ele_toggle, self.ele_mask[self.ele_first : self.ele_first + self.ele_max]):
                                    bottone.state_toggle = status


                    if event.type == pygame.MOUSEBUTTONUP:

                        if event.button == 1:

                            # calcola l'indice dove verrà inserito un valore (offset di mezzo elemento)
                            rilascio = self.ele_first + round((logica.mouse_pos[1] - self.y - self.label_title.font.font_pixel_dim[1] // 2) // self.label_title.font.font_pixel_dim[1]) - 2
                            
                            if rilascio < len(self.elementi) - 1: # se il rilascio avviene entro il range di elementi

                                if self.ele_selected_index != rilascio: # se l'elemento spostato e la destinazione sono diversi

                                    offset = True if rilascio < self.ele_selected_index else False # offset nel caso di percorrenza opposta (index slide reverse list)
                                    
                                    # aggiusto i dati di elementi e le relative maschere
                                    self.elementi.insert(rilascio + 1, self.elementi[self.ele_selected_index])
                                    self.ele_mask.insert(rilascio + 1, self.ele_mask[self.ele_selected_index])

                                    self.elementi.pop(self.ele_selected_index + offset)
                                    self.ele_mask.pop(self.ele_selected_index + offset)

                                    self.ele_selected_index = rilascio + offset

                                    if self.ele_selected_index > len(self.elementi):
                                        self.ele_selected_index = len(self.elementi) - 1

                                    # aggiorno i bottoni dopo lo swap di posizioni
                                    for bottone, status in zip(self.ele_toggle, self.ele_mask[self.ele_first : self.ele_first + self.ele_max]):
                                        bottone.state_toggle = status

                            elif rilascio == len(self.elementi) - 1: # caso particolare in cui il rilascio avviene all'ultimo valore

                                if self.ele_selected_index != rilascio:

                                    offset = True if rilascio < self.ele_selected_index else False
                                    
                                    self.elementi.append(self.elementi[self.ele_selected_index])
                                    self.ele_mask.append(self.ele_mask[self.ele_selected_index])

                                    self.elementi.pop(self.ele_selected_index + offset)
                                    self.ele_mask.pop(self.ele_selected_index + offset)

                                    self.ele_selected_index = len(self.elementi) - 1

                                    for bottone, status in zip(self.ele_toggle, self.ele_mask[self.ele_first : self.ele_first + self.ele_max]):
                                        bottone.state_toggle = status


    def update_context_menu(self, *args):
        super().update_context_menu(*args)
        self.label_title.update_context_menu(*args)


    def update_window_change(self):
        super().update_window_change()
        self.label_title.update_window_change()

        self.ele_max = int((self.h - self.label_title.font.font_pixel_dim[1] * 2) // self.label_title.font.font_pixel_dim[1])

        status_toggle = self.ele_mask + [False for _ in range(self.ele_max - len(self.ele_mask))]

        self.ele_toggle = [Bottone_Toggle(anchor=(f"lu lu ({self.w * 0.01}px) ({self.label_title.font.font_pixel_dim[1] * (i + 2)}px)", self), w=f"{self.label_title.font.font_pixel_dim[1]}px", h=f"{self.label_title.font.font_pixel_dim[1]}px", state=stato, text="") for i, stato in zip(range(self.ele_max), status_toggle)]
        [ele.update_context_menu(self.x_Context, self.y_Context, self.w_Context, self.h_Context) for ele in self.ele_toggle]
        [ele.update_window_change() for ele in self.ele_toggle]

        for ele in self.ele_toggle:
            ele.bg += array([10, 10, 10])



class ColorPicker(BaseElement):
    def __init__(self, palette, id, x="", y="", anchor="lu", w="", h="", initial_color=[200, 200, 200], text="", hide=False, bg=None) -> None:
        
        super().__init__(x, y, anchor, w, h, text, hide)

        self.label_title = Label_Text(anchor=(f"lc rc (10px) (0px)", self), w="-*w", h="-*h", text=text, hide=hide)

        self.opener = Bottone_Push(anchor=("cc cc (0px) (0px)", self), w=w, h=h, function=self.apri_picker, hide=hide)
        self.opener.suppress_animation = True
        self.opener.contorno = 0
        self.opener.bg = initial_color

        self.update_mouse_position = False

        self.id = id

        self.title = text
        
        self.palette: Palette = palette
        self.picked_color = initial_color

    
    def set_color(self, color):
        self.picked_color = color
        self.opener.bg = color


    def disegnami(self, logica):
        self.label_title.disegnami(logica)
        self.opener.disegnami(logica)


    def eventami(self, events, logica: 'Logica'):

        if not self.hide:

            self.opener.eventami(events, logica)

            if self.palette.aggiorna_colore and self.id == self.palette.chosen_id:
                self.opener.bg = array(self.palette.colore_scelto) * self.palette.intensity
                self.set_color(array(self.palette.colore_scelto) * self.palette.intensity)

            if self.update_mouse_position:
                logica.mouse_pos = (self.palette.x + self.palette.w / 2, self.palette.y + self.palette.h / 2)
                self.update_mouse_position = False

            return self.palette.toggle


    def apri_picker(self, __useless):
        # pygame.mouse.set_pos(self.palette.x + self.palette.w / 2, self.palette.y + self.palette.h / 2)
        # self.update_mouse_position = True
        
        self.palette.mouse_inside_BB = False

        self.palette.colore_scelto = self.picked_color
        self.palette.intensity = 1
        self.palette.toggle = False if self.palette.toggle else True
        self.palette.chosen_id = self.id


    def hide_plus_children(self, booleano):
        super().hide_plus_children(booleano)
        self.label_title.hide_plus_children(booleano)
        self.opener.hide_plus_children(booleano)
        self.palette.hide_plus_children(booleano)

    
    def get_color(self):
        return self.picked_color


    def update_context_menu(self, *args):
        super().update_context_menu(*args)
        self.label_title.update_context_menu(*args)
        self.opener.update_context_menu(*args)
        

    def update_window_change(self):
        super().update_window_change()
        self.label_title.update_window_change()
        self.opener.update_window_change()
        self.palette.update_window_change()



class Palette(BaseElement):
    def __init__(self, x="", y="", anchor="cc", w="", h="", initial_color=[200, 200, 200], bg=None) -> None:

        super().__init__(x, y, anchor, w, h, "", False, bg=bg)

        self.colore_scelto = initial_color
        self.aggiorna_colore = False
        self.intensity = 1
        self.update_color_value = False

        self.chosen_id = ""
        self.toggle = False
        self.mouse_inside_BB = False

        ###### generazione colori ###### 
        def generate_color_function(color):
            def return_selected_color(__useless):
                self.colore_scelto = array(color)
                self.update_color_value = True
            return return_selected_color
        
        colori = [
            [255, 0, 0], [255, 125, 0], [255, 255, 0], [125, 255, 0], [0, 255, 0], [0, 255, 125], [0, 255, 255], [0, 125, 255], [0, 0, 255], [125, 0, 255], [255, 0, 255],
            [255 + 32, 0 + 32, 0 + 32], [255 + 32, 125 + 32, 0 + 32], [255 + 32, 255 + 32, 0 + 32], [125 + 32, 255 + 32, 0 + 32], [0 + 32, 255 + 32, 0 + 32], [0 + 32, 255 + 32, 125 + 32], [0 + 32, 255 + 32, 255 + 32], [0 + 32, 125 + 32, 255 + 32], [0 + 32, 0 + 32, 255 + 32], [125 + 32, 0 + 32, 255 + 32], [255 + 32, 0 + 32, 255 + 32],
            [255 + 64, 0 + 64, 0 + 64], [255 + 64, 125 + 64, 0 + 64], [255 + 64, 255 + 64, 0 + 64], [125 + 64, 255 + 64, 0 + 64], [0 + 64, 255 + 64, 0 + 64], [0 + 64, 255 + 64, 125 + 64], [0 + 64, 255 + 64, 255 + 64], [0 + 64, 125 + 64, 255 + 64], [0 + 64, 0 + 64, 255 + 64], [125 + 64, 0 + 64, 255 + 64], [255 + 64, 0 + 64, 255 + 64],
            [255 + 96, 0 + 96, 0 + 96], [255 + 96, 125 + 96, 0 + 96], [255 + 96, 255 + 96, 0 + 96], [125 + 96, 255 + 96, 0 + 96], [0 + 96, 255 + 96, 0 + 96], [0 + 96, 255 + 96, 125 + 96], [0 + 96, 255 + 96, 255 + 96], [0 + 96, 125 + 96, 255 + 96], [0 + 96, 0 + 96, 255 + 96], [125 + 96, 0 + 96, 255 + 96], [255 + 96, 0 + 96, 255 + 96],
            [255 + 128, 0 + 128, 0 + 128], [255 + 128, 125 + 128, 0 + 128], [255 + 128, 255 + 128, 0 + 128], [125 + 128, 255 + 128, 0 + 128], [0 + 128, 255 + 128, 0 + 128], [0 + 128, 255 + 128, 125 + 128], [0 + 128, 255 + 128, 255 + 128], [0 + 128, 125 + 128, 255 + 128], [0 + 128, 0 + 128, 255 + 128], [125 + 128, 0 + 128, 255 + 128], [255 + 128, 0 + 128, 255 + 128],
            [255 + 160, 0 + 160, 0 + 160], [255 + 160, 125 + 160, 0 + 160], [255 + 160, 255 + 160, 0 + 160], [125 + 160, 255 + 160, 0 + 160], [0 + 160, 255 + 160, 0 + 160], [0 + 160, 255 + 160, 125 + 160], [0 + 160, 255 + 160, 255 + 160], [0 + 160, 125 + 160, 255 + 160], [0 + 160, 0 + 160, 255 + 160], [125 + 160, 0 + 160, 255 + 160], [255 + 160, 0 + 160, 255 + 160],
            [255 + 192, 0 + 192, 0 + 192], [255 + 192, 125 + 192, 0 + 192], [255 + 192, 255 + 192, 0 + 192], [125 + 192, 255 + 192, 0 + 192], [0 + 192, 255 + 192, 0 + 192], [0 + 192, 255 + 192, 125 + 192], [0 + 192, 255 + 192, 255 + 192], [0 + 192, 125 + 192, 255 + 192], [0 + 192, 0 + 192, 255 + 192], [125 + 192, 0 + 192, 255 + 192], [255 + 192, 0 + 192, 255 + 192],
            [255 + 224, 0 + 224, 0 + 224], [255 + 224, 125 + 224, 0 + 224], [255 + 224, 255 + 224, 0 + 224], [125 + 224, 255 + 224, 0 + 224], [0 + 224, 255 + 224, 0 + 224], [0 + 224, 255 + 224, 125 + 224], [0 + 224, 255 + 224, 255 + 224], [0 + 224, 125 + 224, 255 + 224], [0 + 224, 0 + 224, 255 + 224], [125 + 224, 0 + 224, 255 + 224], [255 + 224, 0 + 224, 255 + 224],
            [255 + 255, 0 + 255, 0 + 255], [255 + 255, 125 + 255, 0 + 255], [255 + 255, 255 + 255, 0 + 255], [125 + 255, 255 + 255, 0 + 255], [0 + 255, 255 + 255, 0 + 255], [0 + 255, 255 + 255, 125 + 255], [0 + 255, 255 + 255, 255 + 255], [0 + 255, 125 + 255, 255 + 255], [0 + 255, 0 + 255, 255 + 255], [125 + 255, 0 + 255, 255 + 255], [255 + 255, 0 + 255, 255 + 255],
        ]

        for index_a, colore in enumerate(colori):
            for index_b, componente in enumerate(colore):
                if componente > 255:
                    colori[index_a][index_b] = 255

        color_functions = [generate_color_function(color) for color in colori]


        self.colori_bottoni: list[Bottone_Push] = []

        for y in range(9):
            for x in range(11):    
                
                if x == 0:
                    if y == 0:
                        anchor = ("lu lu (0px) (0px)", self)
                    else:
                        anchor = ("lu ld (0px) (-1px)", self.colori_bottoni[(y - 1) * 11 + x])
                else:
                    anchor = ("lu ru (-1px) (0px)", self.colori_bottoni[-1])

                ele_iter = Bottone_Push(anchor=anchor, w="2.4%w", h="2%w", function=color_functions[y * 11 + x])
                self.colori_bottoni.append(ele_iter)
            
        for bottone, colore in zip(self.colori_bottoni, colori):
            bottone.original_color = array(colore)
            bottone.suppress_animation = True
            bottone.contorno = 0
            bottone.smussatura = 0

        ###### generazione intensità ###### 
        def generate_intens_function(intensity):
            def return_selected_intensity(__useless):
                self.intensity = intensity
                self.update_color_value = True
            return return_selected_intensity
        
        intensities = [0.0, 0.12, 0.24, 0.36, 0.48, 0.6, 0.76, 0.88, 1.0]
        intensities = intensities[::-1]

        intensities_functions = [generate_intens_function(intens) for intens in intensities]
        
        self.intens_bottoni: list[Bottone_Push] = []
        for y in range(9):
    
            anchor = (f"lu ru ({self.w / 12}px) (0px)", self.colori_bottoni[y * 11 + 10])

            ele_iter = Bottone_Push(anchor=anchor, w="2.4%w", h="2%w", function=intensities_functions[y])
            self.intens_bottoni.append(ele_iter)
    

        for bottone, colore in zip(self.intens_bottoni, intensities):
            bottone.bg = array([colore, colore , colore]) * 255
            bottone.suppress_animation = True
            bottone.contorno = 0
            bottone.smussatura = 0

        ###### generazione preview ###### 
        self.preview_button = Bottone_Push(anchor=("ru ru (0px) (0px)", self), w="5%w", h=f"{9 * 1.9}%w", disable=True)
        self.preview_button.contorno = 0
        
        ###### generazione entrate ###### 
        self.RGB_inputs: list[Entrata] = []
        for y in range(3):
    
            if y == 0:
                anchor = (f"ld ld (5%w) ({-self.h / 12}px)", self)
            else:
                anchor = (f"lu ru (5%w) (0px)", self.RGB_inputs[-1])

            ele_iter = Entrata(anchor=anchor, w=f"{20/6}%w", h="-*h", text=f"{self.colore_scelto[y]}", lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=255, title="")
            self.RGB_inputs.append(ele_iter)
        
        for index, entrata in enumerate(self.RGB_inputs):
            entrata.bg = array([90, 90, 90])
            entrata.bg[index] = 180

        self.HEX_input: Entrata = Entrata(anchor=(f"lu ru (5%w) (0px)", self.RGB_inputs[-1]), w=f"{20/3}%w", h="-*h",
                                 text=f"{MateUtils.rgb2hex(self.colore_scelto)}", title="", 
                                 lunghezza_max=6, is_hex=True)
        self.HEX_input.bg = array([60, 60, 60])

        
    def disegnami(self, logica):

        if self.toggle:
            pygame.draw.rect(self.schermo, [200, 200, 200], [self.x - 2, self.y - 2, self.w + 4, self.h + 4], 0, 5)
            pygame.draw.rect(self.schermo, self.bg, [self.x, self.y, self.w, self.h], 0, 5)

            for bottone in self.colori_bottoni:
                bottone.bg = bottone.original_color * self.intensity
            
            [bottone.disegnami(logica) for bottone in self.colori_bottoni]
            [bottone.disegnami(logica) for bottone in self.intens_bottoni]
            self.preview_button.bg = array(self.colore_scelto) * self.intensity
            
            self.preview_button.disegnami(logica)

            [entrata.disegnami(logica) for entrata in self.RGB_inputs]
            self.HEX_input.disegnami(logica)


    def eventami(self, logica: 'Logica', events):
    
        stato_prima = self.toggle

        BB_collision = self.bounding_box.collidepoint(logica.mouse_pos)
        if not BB_collision and self.mouse_inside_BB: 
            self.toggle = False
            self.mouse_inside_BB = False
        elif BB_collision:
            self.mouse_inside_BB = True

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
                self.toggle = False
                        
        if self.toggle:
            if self.update_color_value:
                colore_nuovo = array(self.colore_scelto) * self.intensity
                self.RGB_inputs[0].change_text(f"{int(colore_nuovo[0])}" )
                self.RGB_inputs[1].change_text(f"{int(colore_nuovo[1])}" )
                self.RGB_inputs[2].change_text(f"{int(colore_nuovo[2])}" )
                self.HEX_input.change_text(f"{MateUtils.rgb2hex(colore_nuovo)}")
                self.update_color_value = False

            [bottone.eventami(events, logica) for bottone in self.colori_bottoni]
            [bottone.eventami(events, logica) for bottone in self.intens_bottoni]

            [entrata.eventami(events, logica) for entrata in self.RGB_inputs]
            for index, entrata in enumerate(self.RGB_inputs):
                if entrata.selezionato:
                    self.colore_scelto[index] = MateUtils.inp2int(entrata.testo)
                    self.intensity = 1
                    self.HEX_input.change_text(MateUtils.rgb2hex([self.RGB_inputs[0].testo, self.RGB_inputs[1].testo, self.RGB_inputs[2].testo]))


            self.HEX_input.eventami(events, logica)
            if self.HEX_input.selezionato:
                self.colore_scelto = array(MateUtils.hex2rgb(self.HEX_input.testo))
                self.intensity = 1
                
                for colore, entrata in zip(self.colore_scelto, self.RGB_inputs):
                    entrata.change_text(f"{colore}")

        if self.toggle != stato_prima:
            self.aggiorna_colore = True
        else:
            self.aggiorna_colore = False

    
    def update_window_change(self):
        super().update_window_change()
        [ele.update_window_change() for ele in self.colori_bottoni]
        [ele.update_window_change() for ele in self.intens_bottoni]
        [ele.update_window_change() for ele in self.RGB_inputs]
        self.HEX_input.update_window_change()
        self.preview_button.update_window_change()


class SubStringa:
    def __init__(self, colore, bold, italic, apice, pedice, highlight, testo) -> None:
        
        self.colore: tuple[int] = colore
        
        self.bold: bool = bold
        self.italic: bool = italic
        self.apice: bool = apice
        self.pedice: bool = pedice
        self.highlight: bool = highlight
        
        self.testo: str = testo


    def end(self, font:pygame.font.Font):
        lung = font.size(self.testo)
        return lung[0] 


    @staticmethod
    def analisi_caratteri_speciali(frase):

        risultato = frase

        for indice, segno in diction.simboli.items():
            if indice in risultato: risultato = risultato.replace(indice, segno)

        return risultato


    @staticmethod
    def start_analize(frase: str):
        
        def flatten(lst):

            flattened_list = []
            for item in lst:
                if isinstance(item, list):
                    flattened_list.extend(flatten(item))  # Recursively flatten nested lists
                else:
                    flattened_list.append(item)
            return flattened_list

        start = SubStringa(None, False, False, False, False, False, frase)

        substringhe = start.analisi()

        sub_flatten = flatten(substringhe)

        risultato = [elemento for elemento in sub_flatten if elemento.testo != ""]

        return risultato


    def analisi(self):
        
        substringhe_create = []

        formattatori=(r"\h{", r"\^{", r"\_{", r"\b{", r"\i{", r"\#")
        lookup_lenghts = {
            r"\h{": 3,
            r"\^{": 3,
            r"\_{": 3,
            r"\b{": 3,
            r"\i{": 3,
            r"\#": 9,
        }

        # h = highlight
        # ^ = apice
        # _ = pedice
        # b = bold
        # i = italic
        # # = hex color

        formattatori_trovati = []

        primo_formattatore = None

        valvola = 0

        for i in range(len(self.testo)):
            
            # controlla se viene trovato un formattatore tra tutti i formattatori disponibili
            for formattatore in formattatori:

                # se la substringa che va da i a i + len(form.) è uguale al form. -> trovato un candidato
                if self.testo[i:i+len(formattatore)] == formattatore:

                    # se questa è la prima volta che si trova un formattatore, me lo segno
                    if primo_formattatore is None:
                        primo_formattatore = i
                    
                    # in generale, tengo traccia dei formattatori trovati, così da sapere quando finisce la parentesi
                    formattatori_trovati.append([formattatore, i])
                    break

            if self.testo[i] == "}":
                for j in range(len(formattatori_trovati),0,-1):
                    if len(formattatori_trovati[j-1]) == 2:
                        formattatori_trovati[j-1].append(i)
                        break

            # controllo se il primo formattatore è stato chiuso
            if len(formattatori_trovati) > 0 and len(formattatori_trovati[0]) == 3:

                # controllo pre formattatore, presenza di testo default
                if formattatori_trovati[0][1] > valvola:
                    substringhe_create.append(SubStringa(self.colore, self.bold, self.italic, self.apice, self.pedice, self.highlight, self.testo[valvola:formattatori_trovati[0][1]]))


                # gestione del tag                    
                ris = SubStringa(self.colore, self.bold, self.italic, self.apice, self.pedice, self.highlight, None)
                ris.testo = self.testo[formattatori_trovati[0][1] + lookup_lenghts[formattatori_trovati[0][0]]: formattatori_trovati[0][2]]
                
                match formattatori_trovati[0][0]:
                    case r"\h{": ris.highlight = True
                    case r"\^{": ris.apice = True
                    case r"\_{": ris.pedice = True
                    case r"\b{": ris.bold = True
                    case r"\i{": ris.italic = True
                    case r"\#": ris.colore = MateUtils.hex2rgb(self.testo[formattatori_trovati[0][1] + 2 : formattatori_trovati[0][1] + 8])


                # controllo figli
                depth_controllo = ris.analisi()
                if len(depth_controllo) == 0:
                    substringhe_create.append(ris)
                else:
                    substringhe_create.append(depth_controllo)


                # ripristino il ciclo
                valvola = formattatori_trovati[0][2] + 1
                formattatori_trovati = []
                primo_formattatore = None


        substringhe_create.append(SubStringa(self.colore, self.bold, self.italic, self.apice, self.pedice, self.highlight, self.testo[valvola:]))
        
        return substringhe_create



class Animazione:

    def __init__(self, durata, type: str = "once") -> None:
        self.attiva = False
        self.durata = durata
        self.dt = 0

        match type:
            case "loop": self.type = 0
            case "once": self.type = 1
            case _: raise ValueError(f"Modalità di animazione non rispettata! Controlla.\nValori accettati 'once', 'loop'.\nValore passato: {type}")


    def riavvia(self):
        self.attiva = True
        self.dt = 0


    def update(self, dt: int) -> bool:
        '''
        Outputs:
        - True if still inside the animation
        - False if outside the animation
        '''
        if self.attiva and self.dt < self.durata:
            
            self.dt += dt

            if self.dt >= self.durata:
                self.attiva = False if self.type else True
                self.dt = 0

            return True

        else: 
            return False
        


class Font:
    def __init__(self, dim, latex_font=False) -> None:
        
        self.original = int(dim)

        self.latex_font = latex_font

        self.dim_font = self.original 

        if self.latex_font:        
            path_r = os.path.join('TEXTURES', 'century_r.TTF')
            path_b = os.path.join('TEXTURES', 'century_b.TTF')
            path_i = os.path.join('TEXTURES', 'century_i.TTF')
        else:
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
    
        if self.latex_font:    
            path_r = os.path.join('TEXTURES', 'century_r.TTF')
            path_b = os.path.join('TEXTURES', 'century_b.TTF')
            path_i = os.path.join('TEXTURES', 'century_i.TTF')
        else:
            path_r = os.path.join('TEXTURES', 'font_r.ttf')
            path_b = os.path.join('TEXTURES', 'font_b.ttf')
            path_i = os.path.join('TEXTURES', 'font_i.ttf')
        
        self.font_pyg_r = pygame.font.Font(path_r, round(self.dim_font))
        self.font_pyg_i = pygame.font.Font(path_i, round(self.dim_font))
        self.font_pyg_b = pygame.font.Font(path_b, round(self.dim_font))

        self.font_pixel_dim = self.font_pyg_r.size("a")


class ContextMenu(BaseElement):
    def __init__(self, x="", y="", anchor="lu", w="", h="", text="", hide=False, separator_size=2, bg=[25, 25, 25]) -> None:
        super().__init__(x, y, anchor, w, h, text, hide)

        self.inizializzato = False

        self.progression = 0
        self.max_progression = 0
        self.offset_progression = self.h
        self.bg = bg
        self.debug = False
        self.elements: dict[str, Label_Text | Bottone_Push | Bottone_Toggle | Entrata | Scroll | ContextMenu | ColorPicker] = {}
        self.separators = []
        self.separator_size = separator_size

    
    def disegnami(self, logica):

        if not self.hide:
            pygame.draw.rect(self.schermo, self.bg, [self.x, self.y, self.w, self.h], 0, 5)

            [ele.disegnami(logica) for index, ele in self.elements.items() if type(ele) != ColorPicker]
            [ele.disegnami(logica) for index, ele in self.elements.items() if type(ele) == ColorPicker]

            for sep in self.separators:
                pygame.draw.line(self.schermo, [60, 60, 60], [self.x + self.w * 0.01, sep], [self.x + self.w * 0.99, sep], self.separator_size)

            if self.debug:
                pygame.draw.circle(self.schermo, [255, 0, 0], self.lu, 5)
                pygame.draw.circle(self.schermo, [255, 0, 0], self.lc, 5)
                pygame.draw.circle(self.schermo, [255, 0, 0], self.ld, 5)
                pygame.draw.circle(self.schermo, [255, 0, 0], self.cu, 5)
                pygame.draw.circle(self.schermo, [255, 0, 0], self.cc, 5)
                pygame.draw.circle(self.schermo, [255, 0, 0], self.cd, 5)
                pygame.draw.circle(self.schermo, [255, 0, 0], self.ru, 5)
                pygame.draw.circle(self.schermo, [255, 0, 0], self.rc, 5)
                pygame.draw.circle(self.schermo, [255, 0, 0], self.rd, 5)


    def eventami(self, events, logica: 'Logica'):
        
        if logica.scroll_up:
            if self.progression > 0:
                self.progression -= 1            
                self.update_scroll(+1)
        if logica.scroll_down:
            if self.progression < self.max_progression - self.offset_progression:
                self.progression += 1            
                self.update_scroll(-1)

        [ele.eventami(events, logica) for index, ele in self.elements.items() if type(ele) != ColorPicker]
        
        self.hide_elements()

        for indice, ele in self.elements.items():
            if type(ele) == ColorPicker:
                pop_up_domanda_color = ele.eventami(events, logica)
            
                if pop_up_domanda_color:
                    return ele
        
        return 0


    def hide_elements(self):
        
        for index, element in self.elements.items():
            element.hide_plus_children(self.hide)

    
    def add_element(self, id: str, element: Label_Text):
        element.update_context_menu(self.x, self.y, self.w, self.h)
        self.elements[id] = element



    def update_window_change(self):

        self.x = float(self.ori_coords[0][:-2]) * self.pappardella["x_screen"] / 100
        self.y = float(self.ori_coords[1][:-2]) * self.pappardella["y_screen"] / 100
        self.w = float(self.ori_coords[2][:-2]) * self.pappardella["x_screen"] / 100
        self.h = float(self.ori_coords[3][:-2]) * self.pappardella["y_screen"] / 100

        match self.ori_coords[-1]:
            case "lu":
                self.x, self.y = (self.x - 0,                    self.y - 0)    
            case "cu":
                self.x, self.y = (self.x - self.w / 2,  self.y - 0)    
            case "ru":
                self.x, self.y = (self.x - self.w,      self.y - 0)    
            case "lc":
                self.x, self.y = (self.x - 0,                    self.y - self.h / 2)    
            case "cc":
                self.x, self.y = (self.x - self.w / 2,  self.y - self.h / 2)    
            case "rc":
                self.x, self.y = (self.x - self.w,      self.y - self.h / 2)    
            case "ld":
                self.x, self.y = (self.x - 0,                    self.y - self.h)    
            case "cd":
                self.x, self.y = (self.x - self.w / 2,  self.y - self.h)    
            case "rd":
                self.x, self.y = (self.x - self.w,      self.y - self.h)  
        
        for index, ele in self.elements.items():
            ele.update_context_menu(self.x, self.y, self.w, self.h)

        [ele.update_window_change() for index, ele in self.elements.items()]
        

    def update_scroll(self, pm: int):
        
        for index, ele in self.elements.items():
            
            if not type(ele.anchor) == tuple:
                new_values = list(ele._init_coords)
                new_values[1] += pm
                ele._init_coords = tuple(new_values)
            ele.update_window_change()

    
    def get_bottom_height(self):
        return self.h + self.y
    

    def get_y_top_side(self):
        return self._init_coords[1] * self.pappardella["y_screen"] / 100
    

    def add_separator(self, y):
        self.separators.append(y)



class Screen(BaseElement):

    def __init__(self, x="", y="", anchor="lu", w="", h="", hide=False, latex_font=False, screenshot_type=False):
        super().__init__(x, y, anchor, w, h, "", hide, latex_font=latex_font)

        self.screenshot_type = screenshot_type
        self.tavolozza = pygame.Surface((self.w, self.h))

    
    def update_window_change(self):
        super().update_window_change()
        self.tavolozza = pygame.Surface((self.w, self.h))
    

    def disegnami(self, logica):
        if not self.hide and not self.screenshot_type:
            self.schermo.blit(self.tavolozza, (self.x, self.y))


    def _clear_canvas(self, color=None):
        if color is None:
            self.tavolozza.fill(self.bg)
        else:
            self.tavolozza.fill(color)


    def _add_points(self, points, color, radius=1, width=0):
        for point in points:
            pygame.draw.circle(self.tavolozza, color, point[:2], ceil(radius), ceil(width))
    
    
    def _add_rectangle(self, coords4, color, width=0):
        pygame.draw.rect(self.tavolozza, color, coords4, ceil(width))
    
    
    def _add_line(self, coords2, color, width=1):
        pygame.draw.line(self.tavolozza, color, coords2[0], coords2[1], ceil(width))


    def _add_lines(self, points, color, size=1):
        for start, end in zip(points[:-1], points[1:]):
            pygame.draw.line(self.tavolozza, color, start, end, ceil(size))


    @staticmethod
    def _add_points_static(schermo, points, color, radius=1, width=0):
        for point in points:
            pygame.draw.circle(schermo, color, point[:2], ceil(radius), ceil(width))
    
    
    @staticmethod
    def _add_rectangle_static(schermo, coords4, color, width=0):
        pygame.draw.rect(schermo, color, coords4, ceil(width))
    
    
    @staticmethod
    def _add_line_static(schermo, coords2, color, width=1):
        pygame.draw.line(schermo, color, coords2[0], coords2[1], ceil(width))


    @staticmethod
    def _add_lines_static(schermo, points, color, size=1):
        for start, end in zip(points[:-1], points[1:]):
            pygame.draw.line(schermo, color, start, end, ceil(size))
    

    def _add_text(self, text, pos, size=1, anchor="lu", color=[100, 100, 100], rotation=0):
        
        if type(text) == list:

            need_reset = False
            if size != 1:
                need_reset = True
                self.font.scala_font(size)

            for text_i, pos_i, anchor_i, color_i, rotation_i in zip(text, pos, anchor, color, rotation):

                pre_rotation = self.font.font_pyg_r.render(text_i, True, color_i)
                
                if rotation_i != 0:
                    pre_rotation = pygame.transform.rotate(pre_rotation, rotation_i)

                nl = 0
                hl = self.font.font_pixel_dim[0] * len(text_i) / 2
                fl = self.font.font_pixel_dim[0] * len(text_i)

                nh = 0
                hh = self.font.font_pixel_dim[1] / 2 
                fh = self.font.font_pixel_dim[1] 


                match anchor_i:
                    case "lu": offset_x, offset_y = nl, nh 
                    case "cu": offset_x, offset_y = hl, nh
                    case "ru": offset_x, offset_y = fl, nh
                    case "lc": offset_x, offset_y = nl, hh
                    case "cc": offset_x, offset_y = hl, hh
                    case "rc": offset_x, offset_y = fl, hh
                    case "ld": offset_x, offset_y = nl, fh
                    case "cd": offset_x, offset_y = hl, fh
                    case "rd": offset_x, offset_y = fl, fh


                self.tavolozza.blit(pre_rotation, (pos_i[0] - offset_x, pos_i[1] - offset_y))
            
            if need_reset:
                need_reset = False
                self.font.scala_font(1/size)

        # make it bulk
        else:

            need_reset = False
            if size != 1:
                need_reset = True
                self.font.scala_font(size)

            pre_rotation = self.font.font_pyg_r.render(text, True, color)
            
            if rotation != 0:
                pre_rotation = pygame.transform.rotate(pre_rotation, rotation)

            nl = 0
            hl = self.font.font_pixel_dim[0] * len(text) / 2
            fl = self.font.font_pixel_dim[0] * len(text)

            nh = 0
            hh = self.font.font_pixel_dim[1] / 2 
            fh = self.font.font_pixel_dim[1] 


            match anchor:
                case "lu": offset_x, offset_y = nl, nh 
                case "cu": offset_x, offset_y = hl, nh
                case "ru": offset_x, offset_y = fl, nh
                case "lc": offset_x, offset_y = nl, hh
                case "cc": offset_x, offset_y = hl, hh
                case "rc": offset_x, offset_y = fl, hh
                case "ld": offset_x, offset_y = nl, fh
                case "cd": offset_x, offset_y = hl, fh
                case "rd": offset_x, offset_y = fl, fh


            self.tavolozza.blit(pre_rotation, (pos[0] - offset_x, pos[1] - offset_y))
            
            if need_reset:
                need_reset = False
                self.font.scala_font(1/size)

    
    def _paste_array(self, array, position):
        surface = pygame.surfarray.make_surface(array)
        self.tavolozza.blit(surface, (position[0],position[1]))
    
    
    def _generate_surface(self, array):
        return pygame.surfarray.make_surface(array)

    
    def _blit_surface(self, surface, position):
        self.tavolozza.blit(surface, (position[0],position[1]))


    def _extract_pixel_values(self, x, y, w, h):
        
        x, y, w, h = int(x), int(y), int(w), int(h)

        pixel_array = pygame.surfarray.array3d(self.tavolozza)

        return pixel_array[x : x+w, y : y+h]
    

    def _save_screenshot(self, path):
        try:
            self.screenshot_type = False
            self.disegnami(None)
            self.screenshot_type = True
            pygame.image.save(self.tavolozza, path)
            img = Image.open(path)
            img.save(path, dpi=(300, 300))

        except FileNotFoundError:
            pass
    

    def load_image(self, path:str):
        self.loaded_image = pygame.image.load(path)