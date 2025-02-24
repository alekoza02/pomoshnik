import pygame
import numpy as np
from MATEMATICA._modulo_mate_utils import MateUtils
import pyperclip
import os
import json
import time
from PIL import Image
from math import ceil

NON_ESEGUIRE = False

if NON_ESEGUIRE:    
    from pygame.event import Event
    from _modulo_UI import Logica

    # formula per ricavare l'altezza del Font: floor(font_size * 0.16209 + 1)

from GRAFICA._modulo_database import Dizionario; diction = Dizionario()
from GRAFICA._modulo_bottoni_callbacks import BottoniCallbacks



class AudioTracks:
    def __init__(self):
        pygame.init()
        self.UI_sel = pygame.mixer.Sound("./TEXTURES/AUDIO_SC2/UI_sel.wav")
        self.UI_sel.set_volume(.2)
        self.UI_sel_old = pygame.mixer.Sound("./TEXTURES/AUDIO_SC2/UI_Button0_old.wav")
        self.UI_sel_old.set_volume(.2)
        self.UI_hov = pygame.mixer.Sound("./TEXTURES/AUDIO_SC2/UI_Nova_MouseOver1.wav")
        self.UI_hov.set_volume(.1)
        self.UI_open = pygame.mixer.Sound("./TEXTURES/AUDIO_SC2/UI_BnetWindowOpen.wav")
        self.UI_open.set_volume(.2)
        self.UI_close = pygame.mixer.Sound("./TEXTURES/AUDIO_SC2/UI_Popup_Type01_0.wav")
        self.UI_close.set_volume(.2)
        self.UI_typing = pygame.mixer.Sound("./TEXTURES/AUDIO_SC2/UI_TextCrawlType01.wav")
        self.UI_typing.set_volume(.2)
        self.UI_error = pygame.mixer.Sound("./TEXTURES/AUDIO_SC2/UI_Error.wav")
        self.UI_error.set_volume(.2) 


audio = AudioTracks()


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

    FULL_coord_window = None

    def __init__(self, x="", y="", anchor="lu", w="", h="", text="", hide=False, color_text=[200, 200, 200], latex_font=False, bg=None, tooltip="", show_tooltip=True) -> None:
        
        self.latex_font = latex_font
        self.is_child = False
        self.schermo = BaseElement.FULL_coord_window["screen"]

        self.color_text = color_text

        self.sound_select_birth = audio.UI_sel
        self.sound_select_death = audio.UI_sel
        self.sound_select = audio.UI_sel
        self.sound_hover = audio.UI_hov
        self.sound_typing = audio.UI_typing
        self.sound_error = audio.UI_error
        

        if bg is None:
            self.bg = np.array(BaseElement.FULL_coord_window["bg_def"])
        else:
            self.bg = np.array(bg)

        self.bg_backup = self.bg.copy()
        self.hide: bool = hide
        self.hide_from_window: bool = False
        self.hide_from_menu: bool = False

        self.testo: str = text
        self.testo_diplayed = (f"{self.testo}", 1) # (text, number of lines)
        
        self.font_size_update = BaseElement.FULL_coord_window["font_size"]
        self.font: Font = Font(self.font_size_update, self.latex_font)

        self.ori_coords = (x, y, w, h, anchor)

        self.need_update = False
        self.previous_hover = False

        self.x_Context = 0
        self.y_Context = 0
        self.w_Context = self.FULL_coord_window["x_screen"]
        self.h_Context = self.FULL_coord_window["y_screen"]

        self.move_x = 0
        self.move_y = 0

        self.show_tooltip = show_tooltip
        if self.show_tooltip:
            self.tooltip = tooltip
            if self.tooltip == "":
                self.tooltip = self.testo

        self.recalc_geometry(x, y, w, h, anchor)



    @classmethod
    def _init_scene(cls, FULL_coord_window) -> None:
        cls.FULL_coord_window = FULL_coord_window 


    def get_tooltip(self, logica: 'Logica'):
        if self.do_stuff:        
            if self.show_tooltip and self.bounding_box.collidepoint(logica.mouse_pos):
                return self.tooltip


    def disegnami(self, logica):
        ...

    
    def eventami(self, events, logica):
        ...


    def hover_sound(self, status):
        if self.previous_hover != status:
            self.previous_hover = self.hover
            if self.previous_hover:
                if not self.sound_hover is None:
                    self.sound_hover.play()


    def check_for_lost_focus(self, events, logica, force_closure=False):
        ...

    
    def change_text(self, text):
        self.testo = text


    def change_font_size(self, new_size):
        self.font_size_update = new_size
        self.font: Font = Font(new_size, self.latex_font)


    def update_window_change(self):
        self.recalc_geometry(*self.ori_coords)

    
    def update_context_menu(self, *args):
        if type(self) == Label_Text and self.no_parent: return # caso dei label non appartenenti a nessuno schermo -> ignora i limiti di posizione
        self.x_Context = args[0]
        self.y_Context = args[1]
        self.w_Context = args[2]
        self.h_Context = args[3]


    def recalc_geometry(self, new_x="", new_y="", new_w="", new_h="", anchor_point="", update_ori_coords=True):
        
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
                    
                    molt = 1
                    if "n" in sub_coord:
                        molt = -1
                    posizione_finale += molt * (self.font.font_pyg_r.size(self.testo_diplayed[0])[0])
                        
                elif "-*h" in sub_coord:
                    
                    molt = 1
                    if "n" in sub_coord:
                        molt = -1
                    posizione_finale += molt * (self.font.font_pyg_r.size(self.testo_diplayed[0])[1] * self.testo_diplayed[1]) # prendo l'altezza del carattere e la moltiplico per il numero di righe


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
        if update_ori_coords:
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

        # hides the element if it's outside the margins of the contextmenù
        if not self.is_child:
            self.hide_plus_children(self.y < self.y_Context or self.y > self.y_Context + self.h_Context, 0)


    def hide_plus_children(self, booleano, gerarchia=2):
        
        match gerarchia:
            case 0: self.hide_from_menu = booleano
            case 1: self.hide_from_window = booleano
            case 2: self.hide = booleano


    @property
    def do_stuff(self):
        return not self.hide and not self.hide_from_menu and not self.hide_from_window



    def move_update(self, debug=False):
        
        coord_x = f"{self.ori_coords[0]} {self.move_x}px"
        coord_y = f"{self.ori_coords[1]} {self.move_y}px"
    
        self.move_x, self.move_y = 0, 0

        self.recalc_geometry(coord_x, coord_y, *self.ori_coords[2:], update_ori_coords=debug)



class Label_Text(BaseElement):

    def __init__(self, x="", y="", anchor="lu", w="", h="", text="", hide=False, color_text=[200, 200, 200], latex_font=False, no_parent=False) -> None:
        super().__init__(x, y, anchor, w, h, text, hide, color_text, latex_font=latex_font, show_tooltip=False)
        self.debug = False
        self.no_parent = no_parent

        self.h_Context = 1e6
        self.w_Context = 1e6


    def disegnami(self, logica, vertical=False, DANG_surface=None, DANG_offset_x=0, DANG_offset_y=0):

        surface_to_use = self.schermo if DANG_surface is None else DANG_surface

        if self.need_update:
            self.recalc_geometry(*self.ori_coords)

        if self.do_stuff:

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

                if vertical:
                    elenco_substringhe = elenco_substringhe[::-1]

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
                        if vertical:
                            pre_rotation = pygame.transform.rotate(pre_rotation, 90)
                        else:
                            surface_to_use.blit(pre_rotation, (self.x + original_spacing_x * offset_highlight + offset_usato + DANG_offset_x, self.y + offset_frase + offset_pedice_apice + DANG_offset_y))

                    if substringa_analizzata.bold:
                        pre_rotation = self.font.font_pyg_b.render(substringa_analizzata.testo, True, substringa_analizzata.colore)
                        if vertical:
                            pre_rotation = pygame.transform.rotate(pre_rotation, 90)
                            surface_to_use.blit(pre_rotation, (self.x + offset_frase + offset_pedice_apice + DANG_offset_x, self.y + offset_usato + DANG_offset_y))
                        else:
                            surface_to_use.blit(pre_rotation, (self.x + offset_usato + DANG_offset_x, self.y + offset_frase + offset_pedice_apice + DANG_offset_y))
                    
                    elif substringa_analizzata.italic:
                        pre_rotation = self.font.font_pyg_i.render(substringa_analizzata.testo, True, substringa_analizzata.colore)
                        if vertical:
                            pre_rotation = pygame.transform.rotate(pre_rotation, 90)
                            surface_to_use.blit(pre_rotation, (self.x + offset_frase + offset_pedice_apice + DANG_offset_x, self.y + offset_usato + DANG_offset_y))
                        else:
                            surface_to_use.blit(pre_rotation, (self.x + offset_usato + DANG_offset_x, self.y + offset_frase + offset_pedice_apice + DANG_offset_y))
                    
                    else:
                        pre_rotation = self.font.font_pyg_r.render(substringa_analizzata.testo, True, substringa_analizzata.colore)
                        if vertical:
                            pre_rotation = pygame.transform.rotate(pre_rotation, 90)
                            surface_to_use.blit(pre_rotation, (self.x + offset_frase + offset_pedice_apice + DANG_offset_x, self.y + offset_usato + DANG_offset_y))
                        else:
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


    def change_text(self, text, highlight=False):
        if self.latex_font:
            old_text = self.testo
            self.testo = text
            if old_text != self.testo:
                self.need_update = True
        else:
            if len(text) != len(self.testo):
                self.need_update = True
            self.testo = text


    def get_tooltip(self, logica):
        return None



class Bottone_Push(BaseElement):

    def __init__(self, x="", y="", anchor="lu", w="", h="", function=None, text="", hide=False, disable=False, bg=None, tooltip="") -> None:
        super().__init__(x, y, anchor, w, h, text, hide, bg=bg, tooltip=tooltip)

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


        if self.do_stuff:

            colore = self.bg.copy()
            
            if not self.disable:
                colore = self.animazione_press(logica.dt, colore)
                colore = self.animazione_hover(colore)

            colore = [s_colore if s_colore <= 255 else 255 for s_colore in colore]

            pygame.draw.rect(self.schermo, [100, 100, 100], [self.x-1, self.y-1, self.w+2, self.h+2], 1, self.smussatura)
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

        if self.do_stuff:

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.bounding_box.collidepoint(event.pos):
                        if not self.sound_select is None: self.sound_select.play()
                        self.animazione.riavvia()
                        self.callback(self)

            self.hover = True if self.bounding_box.collidepoint(logica.mouse_pos) else False
            self.hover_sound(self.hover)
                    

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
        self.label_title.update_context_menu(*args)
        super().update_context_menu(*args)


    def update_window_change(self):
        self.label_title.update_window_change()
        super().update_window_change()
        try:
            self.load_texture()
        except FileNotFoundError:
            ...


    def move_update(self):
        self.label_title.move_update()
        super().move_update()


    def hide_plus_children(self, booleano, gerarchia=2):
        
        match gerarchia:
            case 0: self.hide_from_menu = booleano
            case 1: self.hide_from_window = booleano
            case 2: self.hide = booleano

        super().hide_plus_children(booleano, gerarchia)
        try: self.label_title.hide = booleano
        except: ...
    
        
        
class Bottone_Toggle(BaseElement):
    def __init__(self, x="", y="", anchor="lu", w="", h="", state=False, type_checkbox=True, text="", hide=False, disable=False, text_on_right=True, tooltip="") -> None:
        super().__init__(x, y, anchor, w, h, text, hide, tooltip=tooltip)
        
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

        if self.do_stuff:

            colore = self.bg.copy()

            colore = self.animazione_press(colore)
            colore = self.animazione_hover(colore)

            if self.checkbox:

                pygame.draw.rect(self.schermo, colore, [self.x, self.y, self.w, self.h], self.contorno, self.smussatura)
                pygame.draw.rect(self.schermo, [100, 100, 100], [self.x-1, self.y-1, self.w+2, self.h+2], 1, self.smussatura)

                if self.state_toggle:
                    pygame.draw.rect(self.schermo, [255, 255, 255], [self.x + 4, self.y + 4, self.w - 8, self.h - 8], self.contorno, self.smussatura)


                self.label_title.disegnami(logica)
            
            else:

                pygame.draw.rect(self.schermo, colore, [self.x, self.y, self.w, self.h], self.contorno, self.smussatura)
                pygame.draw.rect(self.schermo, [100, 100, 100], [self.x-1, self.y-1, self.w+2, self.h+2], 1, self.smussatura)

                if self.texture is None:
                    self.label_title.disegnami(logica)
                else:
                    self.schermo.blit(self.texture, (self.x, self.y))


    def eventami(self, events: list['Event'], logica: 'Logica'):

        if self.do_stuff:

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.bounding_box.collidepoint(event.pos):
                        if self.state_toggle:
                            if not self.sound_select_death is None: self.sound_select_death.play()
                            self.state_toggle = False
                        else:
                            if not self.sound_select_birth is None: self.sound_select_birth.play()
                            self.state_toggle = True

            self.hover = True if self.bounding_box.collidepoint(logica.mouse_pos) else False
            self.hover_sound(self.hover)


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


    def move_update(self, debug=False):
        self.label_title.move_update()
        super().move_update(debug=debug)


    def update_context_menu(self, *args):
        self.label_title.update_context_menu(*args)
        super().update_context_menu(*args)


    def update_window_change(self):
        self.label_title.update_window_change()
        super().update_window_change()
        try:
            self.load_texture()
        except FileNotFoundError:
            ...


    def hide_plus_children(self, booleano, gerarchia=2):
        
        match gerarchia:
            case 0: self.hide_from_menu = booleano
            case 1: self.hide_from_window = booleano
            case 2: self.hide = booleano
                
        super().hide_plus_children(booleano, gerarchia)
        try: self.label_title.hide_plus_children(booleano)
        except: ...


class RadioButton(BaseElement):
    def __init__(self, x="", y="", anchor="lu", w="", h="", axis="x", bg=None, cb_n=1, cb_s=[False], cb_t=["Default item"], cb_tooltips=[""], title="", multiple_choice=False, hide=False, type_checkbox=True, w_button="30px", h_button="30px", always_one_active=False, default_active=0) -> None:
        super().__init__(x, y, anchor, w, h, title, hide, show_tooltip=False)

        if not bg is None:
            self.bg = bg

        self.main_ax = axis

        self.always_one_active = always_one_active
        self.default_active = default_active
        
        self.title = title
        self.multiple_choice = multiple_choice

        self.hide = hide

        self.type_checkbox = type_checkbox

        self.cb_n, self.cb_s, self.cb_t, self.cb_tooltips = cb_n, cb_s, cb_t, cb_tooltips

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
        
        for index, state, text, tooltip in zip(range(cb_n), cb_s, cb_t, cb_tooltips):
            
            match self.main_ax:
                case "x": 
                        spacing = (self.w - float(self.w_button_calcoli[:-2]) * cb_n) / (cb_n - 1)
                        self.toggles.append(Bottone_Toggle(f"{self.x}px {index * (float(self.w_button_calcoli[:-2]) + spacing)}px", f"{self.y}px", "lu", w_button, h_button, state, type_checkbox, text=text, hide=hide, tooltip=tooltip))
                        self.toggles[-1].sound_select_birth = audio.UI_sel_old
                        self.toggles[-1].sound_select_death = audio.UI_sel_old
                case "y":
                        spacing = (self.h - float(self.h_button_calcoli[:-2]) * cb_n) / (cb_n - 1)
                        self.toggles.append(Bottone_Toggle(f"{self.x}px", f"{self.y}px {index * (float(self.h_button_calcoli[:-2]) + spacing)}px", "lu", w_button, h_button, state, type_checkbox, text=text, hide=hide, tooltip=tooltip))
                        self.toggles[-1].sound_select_birth = audio.UI_sel_old
                        self.toggles[-1].sound_select_death = audio.UI_sel_old
                    
                case _: raise TypeError(f"Invalid mode {self.main_ax}, accepted types: 'x', 'y'.")
        
        for bottone in self.toggles:
            bottone.is_child = True
            if bottone.state_toggle:
                bottone.bg = np.array([80, 100, 80])
            else:
                bottone.bg = self.bg + 10 



    def disegnami(self, logica):

        if self.do_stuff:
            pygame.draw.rect(self.schermo, self.bg, [self.x, self.y, self.w, self.h], 0, 5)

            for bottone in self.toggles:
                if bottone.state_toggle:
                    bottone.bg = np.array([80, 100, 80])
                else:
                    bottone.bg = self.bg + 10

            [bottone.disegnami(logica) for bottone in self.toggles]


    def eventami(self, events, logica):

        if self.do_stuff:

            old_state = self.buttons_state

            [bottone.eventami(events, logica) for bottone in self.toggles]
            
            new_state = self.buttons_state

            if not self.multiple_choice:
                ele_vecchio, ele_nuovo = self.check_for_diff(old_state, new_state)

                if not ele_nuovo is None and not ele_vecchio is None:
                    self.toggles[ele_vecchio].state_toggle = False

            self.cb_s = [b.state_toggle for b in self.toggles]

            if self.always_one_active and sum(self.cb_s) == 0:
                self.cb_s[self.default_active] = 1
                self.toggles[self.default_active].state_toggle = 1


    @property
    def buttons_state(self):
        return [bottone.state_toggle for bottone in self.toggles]


    def get_tooltip(self, logica):
        return [tog.get_tooltip(logica) for tog in self.toggles]


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

        if self.w_button[-2:] == "%w":
            self.w_button_calcoli = f"{float(self.w_button[:-2]) * self.one_percent_x}px"
        if self.w_button[-2:] == "%h":
            self.w_button_calcoli = f"{float(self.w_button[:-2]) * self.one_percent_y}px"
        if self.h_button[-2:] == "%w":
            self.h_button_calcoli = f"{float(self.h_button[:-2]) * self.one_percent_x}px"
        if self.h_button[-2:] == "%h":
            self.h_button_calcoli = f"{float(self.h_button[:-2]) * self.one_percent_y}px"
        
        for index in range(self.cb_n):
            
            self.toggles[index].ori_coords = list(self.toggles[index].ori_coords)
            
            match self.main_ax:
                case "x": 
                        spacing = (self.w - float(self.w_button_calcoli[:-2]) * self.cb_n) / (self.cb_n - 1)
                        self.toggles[index].ori_coords[0] = f"{self.x}px {index * (float(self.w_button_calcoli[:-2]) + spacing)}px" 
                        self.toggles[index].ori_coords[1] = f"{self.y}px" 
                        self.toggles[index].ori_coords[2] = self.w_button_calcoli
                        self.toggles[index].ori_coords[3] = self.h_button_calcoli
                        
                case "y":
                        spacing = (self.h - float(self.h_button_calcoli[:-2]) * self.cb_n) / (self.cb_n - 1)
                        self.toggles[index].ori_coords[0] = f"{self.x}px"
                        self.toggles[index].ori_coords[1] = f"{self.y}px {index * (float(self.h_button_calcoli[:-2]) + spacing)}px"
                        self.toggles[index].ori_coords[2] = self.w_button_calcoli
                        self.toggles[index].ori_coords[3] = self.h_button_calcoli
                        
                case _: raise TypeError(f"Invalid mode {self.main_ax}, accepted types: 'x', 'y'.")
            
            self.toggles[index].ori_coords = tuple(self.toggles[index].ori_coords)
            self.toggles[index].update_window_change()


    def update_context_menu(self, *args):
        super().update_context_menu(*args)
        

    def hide_plus_children(self, booleano, gerarchia=2):
        
        match gerarchia:
            case 0: self.hide_from_menu = booleano
            case 1: self.hide_from_window = booleano
            case 2: self.hide = booleano

        super().hide_plus_children(booleano, gerarchia)
        try: [ele.hide_plus_children(booleano, gerarchia) for ele in self.toggles]
        except Exception as e: ... # Happens that the RadioButton is told to hide elements, when they still have not been created 


    def move_update(self):
        for ele in self.toggles:
            ele.move_y = self.move_y
            ele.move_update()
        
        super().move_update()


class Entrata(BaseElement):
    def __init__(self, x="", y="", anchor="lu", w="", h="", text="", title="Entrata", hide=False, lunghezza_max=None, solo_numeri=False, num_valore_minimo=None, num_valore_massimo=None, is_hex=False, tooltip="") -> None:       
        super().__init__(x, y, anchor, w, h, text, hide, tooltip=tooltip)

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

        if self.do_stuff:

            colore = self.bg.copy()

            colore = self.animazione_press(colore)
            colore = self.animazione_hover(colore)

            self.label_title.disegnami(logica)

            pygame.draw.rect(self.schermo, colore, [self.x, self.y, self.w, self.h], self.contorno)
            pygame.draw.rect(self.schermo, [100, 100, 100], [self.x-1, self.y-1, self.w+2, self.h+2], 1)

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
        
        if self.do_stuff:

            if self.selezionato:
                self.return_previous_text = True
                self.eventami_scrittura(events, logica)

                if self.solo_numeri:
                    numero_equivalente = MateUtils.inp2flo(self.testo, None)

                    if numero_equivalente is None:
                        self.color_text = np.array([255, 0, 0])
                    else:
                        self.color_text = np.array([200, 200, 200])
            else:
                self.return_previous_text = False
                self.previous_text = self.testo


            if logica.dragging and self.selezionato:

                self.highlight_region[0] = self.get_puntatore_pos(logica.mouse_pos[0])
                self.highlight_region[1] = self.get_puntatore_pos(logica.original_start_pos[0])
                self.update_puntatore_pos(logica.mouse_pos)
                self.animazione_puntatore.riavvia()

            self.hover = True if self.bounding_box.collidepoint(logica.mouse_pos) else False
            self.hover_sound(self.hover)


    def check_for_lost_focus(self, events, logica, force_closure=False):

        if force_closure:
            self.selezionato = False
            self.return_previous_text = False
            _ = self.get_text()         # update of the value to avoid lost info 

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
                            if self.do_stuff and not self.sound_select is None: self.sound_select.play()
                            self.animazione_puntatore.riavvia()


    def eventami_scrittura(self, events: list['Event'], logica: 'Logica'):
        
        if self.do_stuff:

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

                    # SOUND / AUDIO
                    self.sound_typing.play()
                    
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


    def get_text(self, real_time=False) -> str:
        
        if real_time:
            return f"{self.testo}"

        if self.return_previous_text:
            restituisco = f"{self.previous_text}"
        else:
            restituisco = f"{self.testo}"
        
        if self.solo_numeri:
            numero_equivalente = MateUtils.inp2flo(restituisco, None)

            if numero_equivalente is None:
                self.color_text = np.array([255, 0, 0])
                return self.num_valore_minimo

            else:
                self.color_text = np.array((200, 200, 200))

                if not self.num_valore_minimo is None and numero_equivalente > self.num_valore_massimo:
                    self.change_text(f"{self.num_valore_massimo}")
                    return self.get_text()
                elif not self.num_valore_massimo is None and numero_equivalente < self.num_valore_minimo:
                    self.change_text(f"{self.num_valore_minimo}")
                    return self.get_text()
                else:
                    return restituisco


        elif self.is_hex:
            if MateUtils.hex2rgb(restituisco, std_return=None) is None:
                self.color_text = np.array([255, 0, 0])
                return "aaaaaa"
            else:
                self.color_text = np.array([200, 200, 200])
                return restituisco

        else:
            return restituisco


    def hide_plus_children(self, booleano, gerarchia=2):
        
        match gerarchia:
            case 0: self.hide_from_menu = booleano
            case 1: self.hide_from_window = booleano
            case 2: self.hide = booleano

        super().hide_plus_children(booleano, gerarchia)
        try: self.label_title.hide = booleano
        except: ...


    def move_update(self):
        self.label_title.move_update()
        super().move_update()


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
            ele.bg += np.array([10, 10, 10])

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
        self.ele_toggle[len(self.elementi) - 1].state_toggle = stato


    def remove_selected_item(self):
        if len(self.elementi) > 0:
            self.elementi.pop(self.ele_selected_index)
            self.ele_mask.pop(self.ele_selected_index)
            if self.ele_selected_index == len(self.elementi) and self.ele_selected_index > 0:
                self.ele_selected_index -= 1

                if self.elemento_attivo < 0:
                    self.ele_first -= 1
    

    def remove_item_index(self, index):
        if len(self.elementi) > 0:
            self.elementi.pop(index)
            self.ele_mask.pop(index)
            if index == len(self.elementi) and index > 0:
                index -= 1

                if self.elemento_attivo < 0:
                    self.ele_first -= 1


    def get_tooltip(self, logica):
        return None


    @property
    def elemento_attivo(self):
        elemento = self.ele_selected_index - self.ele_first
        return elemento


    def disegnami(self, logica: 'Logica'):

        if self.do_stuff:

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
        
        if self.do_stuff:

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
            ele.bg += np.array([10, 10, 10])


    def hide_plus_children(self, booleano, gerarchia=2):
        
        match gerarchia:
            case 0: self.hide_from_menu = booleano
            case 1: self.hide_from_window = booleano
            case 2: self.hide = booleano

        super().hide_plus_children(booleano, gerarchia)
        try: [ele.hide_plus_children(booleano, gerarchia) for ele in self.ele_toggle]
        except: ...
        
        try: self.label_title.hide = booleano
        except: ...


class ColorPicker(BaseElement):
    def __init__(self, x="", y="", anchor="lu", w="", h="", initial_color=[200, 200, 200], text="", hide=False, bg=None, tooltip="") -> None:
        super().__init__(x, y, anchor, w, h, text, hide, tooltip=tooltip)
        

        self.label_title = Label_Text(anchor=(f"lc rc (10px) (0px)", self), w="-*w", h="-*h", text=text, hide=hide)

        self.opener = Bottone_Push(anchor=("cc cc (0px) (0px)", self), w=w, h=h, function=BottoniCallbacks.change_state, hide=hide)
        self.opener.suppress_animation = True
        self.opener.contorno = 0
        self.opener.bg = initial_color
        self.open_call = False

        self.update_mouse_position = False

        self.title = text
        
        self.picked_color = initial_color

    
    def set_color(self, color):
        self.picked_color = color
        self.opener.bg = color


    def disegnami(self, logica):
        self.label_title.disegnami(logica)
        self.opener.disegnami(logica)


    def eventami(self, events, logica: 'Logica'):

        if self.do_stuff:
            self.opener.eventami(events, logica)


    def receive_popup_answer(self, colore):
        self.set_color(colore)


    def send_popup_request(self):
        return self.picked_color


    def check_open_popup_call(self):
        if self.opener.flag_foo:
            self.opener.flag_foo = False
            # The end call will be made by the windows manager, here we just initiate it
            self.open_call = True

        
        return self.open_call


    def hide_plus_children(self, booleano, gerarchia=2):
        
        match gerarchia:
            case 0: self.hide_from_menu = booleano
            case 1: self.hide_from_window = booleano
            case 2: self.hide = booleano

        super().hide_plus_children(booleano, gerarchia)
        
        try: self.label_title.hide_plus_children(booleano, gerarchia)
        except: ...
        
        try: self.opener.hide_plus_children(booleano, gerarchia)
        except: ...

    
    def move_update(self):
        
        self.label_title.move_update()
        self.opener.move_update()

        super().move_update()


    def get_color(self):
        return np.array(self.picked_color)


    def update_context_menu(self, *args):
        super().update_context_menu(*args)
        self.label_title.update_context_menu(*args)
        self.opener.update_context_menu(*args)
        

    def update_window_change(self):
        super().update_window_change()
        self.label_title.update_window_change()
        self.opener.update_window_change()
        



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

        if "{" in self.testo:

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




class Collapsable_Window(BaseElement):
    def __init__(self, x="", y="", anchor="lu", w="", h="", text="", hide=False, color_text=[200, 200, 200], latex_font=False, bg=None, closed=False, group=1):
        super().__init__(x, y, anchor, w, h, text, hide, color_text, latex_font, bg)
        self.expand_button: Bottone_Toggle = Bottone_Toggle(anchor=(f"lu lu (10px) (10px)", self), w=f"40px", h=f"40px", state=not closed, text=">")
        self.expand_button.sound_select_death = audio.UI_close
        self.expand_button.sound_select_birth = audio.UI_open
        
        self.h_chiuso = f"60px"
        self.h_aperto = self.ori_coords[3]
        self.delta_h = float(self.bounding_box[3]) - float(self.h_chiuso[:-2])
        self.flag_OPEN = False
        self.child_id: dict[str, BaseElement] = {}
        self.group = group

        self.initialize_window = True


    def get_tooltip(self, logica):
        return self.expand_button.get_tooltip(logica)


    def eventami(self, events, logica):
        self.expand_button.eventami(events, logica)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.expand_button.bounding_box.collidepoint(event.pos) or self.initialize_window:
                self.initialize_window = False
                if not self.expand_button.state_toggle:
                    self.recalc_geometry(*self.ori_coords[:3], self.h_chiuso, self.ori_coords[-1])
                    self.expand_button.update_window_change()
                    self.expand_button.label_title.change_text(r"\#606060{\b{>}}" + f" {self.testo}")
                    [ele.hide_plus_children(True, 1) for index, ele in self.child_id.items()]
                    self.flag_OPEN = False

                elif self.expand_button.state_toggle:
                    self.delta_h = float(self.bounding_box[3]) - float(self.h_chiuso[:-2])
                    self.recalc_geometry(*self.ori_coords[:3], self.h_aperto, self.ori_coords[-1])
                    self.expand_button.update_window_change()
                    self.expand_button.label_title.change_text(r"\#606060{\b{V}}" + f" {self.testo}")
                    [ele.hide_plus_children(False, 1) for index, ele in self.child_id.items()]
                    self.flag_OPEN = True


    def disegnami(self, logica, max_height):
        if self.do_stuff:
            if self.bounding_box[1] + self.bounding_box[3] > max_height:
                pygame.draw.rect(self.schermo, self.bg, [self.bounding_box[0], self.bounding_box[1], self.bounding_box[2], max_height - self.bounding_box[1]])
            else:
                pygame.draw.rect(self.schermo, self.bg, self.bounding_box)
            self.expand_button.disegnami(logica)


    def update_context_menu(self, *args):
        super().update_context_menu(*args)
        self.expand_button.update_context_menu(*args)


    def update_window_change(self):
        super().update_window_change()
        self.expand_button.update_window_change()

    
    def move_update(self):
        self.expand_button.move_y = self.move_y
        self.expand_button.move_update(debug=True)
        self.expand_button.update_window_change()
        super().move_update()

    
    def hide_plus_children(self, booleano, gerarchia=2):
        
        match gerarchia:
            case 0: self.hide_from_menu = booleano
            case 1: self.hide_from_window = booleano
            case 2: self.hide = booleano
                
        super().hide_plus_children(booleano, gerarchia)
        try: self.expand_button.hide_plus_children(booleano)
        except: ...



class ContextMenu(BaseElement):
    def __init__(self, x="", y="", anchor="lu", w="", h="", text="", hide=False, separator_size=2, bg=[25, 25, 25], scrollable=True, root=False, ) -> None:
        super().__init__(x, y, anchor, w, h, text, hide)

        self.root = root
        self.previous_hide = None

        self.inizializzato = False

        self.progression = 0
        self.max_progression = 0
        self.offset_progression = 0
        self.scrollable = scrollable

        self.bg = bg
        self.debug = False
        self.elements: dict[str, BaseElement] = {}
        self.windows: dict[str, Collapsable_Window] = {}
        self.windows_delta_h: dict[str, float] = {}
        self.separators = []
        self.separator_size = separator_size
        self.max_window_group = 0

        if self.root:
            self.PRIVATE_tooltip_label = Label_Text(x="0.5%w", y="99.5%h", anchor="ld", w="-*w", h="-*h", text="\\h{Tooltip initialized}")
            self.PRIVATE_tooltip_label.font = Font(round(self.font_size_update * 0.8), self.PRIVATE_tooltip_label.latex_font)
            self.add_element("PRIV_tooltip", self.PRIVATE_tooltip_label)
    

    def disegnami(self, logica):

        if not self.hide:
            pygame.draw.rect(self.schermo, self.bg, [self.x, self.y, self.w, self.h], 0, 5)
            [ele.disegnami(logica, self.y + self.h) for index, ele in self.windows.items()]

            [ele.disegnami(logica) for index, ele in self.elements.items() if index != "PRIV_tooltip"]
            
            for sep in self.separators:
                if sep > 0:
                    pygame.draw.line(self.schermo, [60, 60, 60], [self.x + self.w * 0.01, sep + self.y], [self.x + self.w * 0.99, sep + self.y], self.separator_size)


    def search_for_tooltip(self, logica: 'Logica'):
        if self.do_stuff:
            return [ele.get_tooltip(logica) for index, ele in self.elements.items()]


    def change_tooltip(self, message):
        if self.root:
            self.PRIVATE_tooltip_label.change_text(f"{message}", highlight=True)
            self.PRIVATE_tooltip_label.disegnami(None)

    
    def get_tooltip(self, logica):
        return None


    def eventami(self, events, logica: 'Logica'):
        
        if not self.hide:

            # Classic event
            [ele.check_for_lost_focus(events, logica) for index, ele in self.elements.items()]
            [ele.eventami(events, logica) for index, ele in self.windows.items()]
            [ele.eventami(events, logica) for index, ele in self.elements.items()]


            # Scroll update
            if self.bounding_box.collidepoint(logica.mouse_pos):
                if logica.scroll_up:
                    if self.progression > 0:
                        self.progression -= 25            
                if logica.scroll_down:
                    if self.progression < self.max_progression:
                        self.progression += 25            
            
            self.update_scroll(- self.progression)
        

            for i in range(0, self.max_window_group):
                # calcolo degli offset vari storati in un dizionario
                dizionario_altezze = {}
                delta_rimuovere = 0
                for index, ele in self.windows.items():
                    if ele.group == i + 1:
                        if ele.flag_OPEN:
                            ele.delta_h = float(ele.bounding_box[3]) - float(ele.h_chiuso[:-2])
            
                        if not ele.flag_OPEN:
                            delta_rimuovere -= ele.delta_h
                        dizionario_altezze[index] = delta_rimuovere

                
                # muovo gli elementi in base alla finestra in cui si trovano
                for index_window, window in self.windows.items():
                    if window.group == i + 1:
                        for index_elemento, elemento in window.child_id.items():
                            elemento.move_y += dizionario_altezze[index_window]


            # Bulk move di tutti gli elementi
            [ele.move_update() for index, ele in self.elements.items()]
            [ele.move_update() for index, ele in self.windows.items()]
        
        return 0


    def hide_elements(self):
        
        if self.previous_hide != self.hide:

            # If there's an external reason to hide an element (outside the ContextMenù)
            # it shouldn't be constantly being updated from this function, only when the ContextMenù visibility changes.
            for index, element in self.elements.items():

                if element.y > self.y:
                    element.hide_plus_children(self.hide, 0)

        self.previous_hide = self.hide

    
    def add_element(self, id: str, element: Label_Text, window: str = None):
        element.update_context_menu(self.x, self.y, self.w, self.h)
        self.elements[id] = element

        if not window is None:
            self.windows[window].child_id[id] = element
            element.is_in_window = True
        else:
            element.is_in_window = False

        # update max height of the context menù
        pos_y_ele = [ele.y for index, ele in self.elements.items()]
        altezze_ele = [ele.h for index, ele in self.elements.items()]

        pos_y_windows = [windows.y for index, windows in self.windows.items()]
        altezze_windows = [windows.h for index, windows in self.windows.items()]

        pos_y, altezze = max(pos_y_ele, pos_y_windows), max(altezze_ele, altezze_windows)

        max_depth = max([i+j for i, j in zip(pos_y, altezze)])
        
        self.max_progression = max_depth

    
    def add_window(self, id: str, window: Collapsable_Window):
        window.update_context_menu(self.x, self.y, self.w, self.h)
        self.windows[id] = window
        self.windows_delta_h[id] = float(window.h) - float(window.h_chiuso[:-2])
        self.max_window_group = max(self.max_window_group, window.group)

        # update max height of the context menù
        pos_y_ele = [ele.y for index, ele in self.elements.items()]
        altezze_ele = [ele.h for index, ele in self.elements.items()]

        pos_y_windows = [windows.y for index, windows in self.windows.items()]
        altezze_windows = [windows.h for index, windows in self.windows.items()]

        pos_y, altezze = max(pos_y_ele, pos_y_windows), max(altezze_ele, altezze_windows)

        max_depth = max([i+j for i, j in zip(pos_y, altezze)])

        self.max_progression = max_depth


    def update_window_change(self):

        self.x = float(self.ori_coords[0][:-2]) * self.FULL_coord_window["x_screen"] / 100
        self.y = float(self.ori_coords[1][:-2]) * self.FULL_coord_window["y_screen"] / 100
        self.w = float(self.ori_coords[2][:-2]) * self.FULL_coord_window["x_screen"] / 100
        self.h = float(self.ori_coords[3][:-2]) * self.FULL_coord_window["y_screen"] / 100

        self.bounding_box = pygame.Rect(self.x, self.y, self.w, self.h)

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
        for index, ele in self.windows.items():
            ele.update_context_menu(self.x, self.y, self.w, self.h)

        [ele.update_window_change() for index, ele in self.elements.items()]
        [ele.update_window_change() for index, ele in self.windows.items()]

        self.windows_delta_h = {key : float(window.h) - float(window.h_chiuso[:-2]) for key, window in self.windows.items()}


    def update_scroll(self, pm: int):
        if self.scrollable:
            for _, ele in self.elements.items():
                ele.move_y += pm
                
            for _, window in self.windows.items():
                window.move_y += pm
                
    
    def add_separator(self, y):
        self.separators.append(y)



class Slider(BaseElement):
    def __init__(self, x="", y="", anchor="lu", w="", h="", title="", color_text=[200, 200, 200], initial_value=0, min_value=0, max_value=1, hide=False, bg=None, tooltip="", show_tooltip=True):
        super().__init__(x, y, anchor, w, h, "", hide, color_text, False, bg, tooltip, show_tooltip)

        self.value = initial_value
        self.keep_updating = False

        self.min_value = min_value
        self.max_value = max_value

        self.label_title = Label_Text(anchor=("rc lc (-30px) (0)", self), w="-*w", h="-*h", color_text=color_text, text=title)
        self.indicatore = Entrata(anchor=("lc rc (30px) (0)", self), w="-*w", h="-*h", title="", text=f"-------", lunghezza_max=6, solo_numeri=True, num_valore_minimo=min_value, num_valore_massimo=max_value, tooltip="Indicatore relativo al valore dello slider.")


    def get_value(self):
        return (self.max_value - self.min_value) * self.value + self.min_value

    
    def get_value_normalized(self, inp_value):
        return (inp_value - self.min_value) / (self.max_value - self.min_value)


    def disegnami(self, logica):
        if self.do_stuff:
            self.label_title.disegnami(logica)
            self.indicatore.disegnami(logica)
            pygame.draw.rect(self.schermo, self.bg, [self.x, self.y + self.h / 2 - self.h / 5, self.w, self.h / 2.5], 0, border_radius=2)
            pygame.draw.rect(self.schermo, [150, 200, 150], [self.x, self.y + self.h / 2 - self.h / 5, self.w * self.value, self.h / 2.5], 0, border_radius=2)
            pygame.draw.circle(self.schermo, [60, 60, 60], [self.x + self.w * self.value, self.y + self.h / 2], self.h / 2, 0)
            pygame.draw.circle(self.schermo, [255, 255, 255], [self.x + self.w * self.value, self.y + self.h / 2], self.h / 5, 0)



    def eventami(self, events, logica: 'Logica'):
        if self.do_stuff:

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.bounding_box.collidepoint(event.pos):
                        self.keep_updating = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.keep_updating = False

            if self.indicatore.selezionato:
                self.indicatore.eventami(events, logica)
                try:
                    self.value = self.get_value_normalized(float(self.indicatore.get_text(real_time=True)))
                except Exception:
                    ...
            else:
                self.indicatore.change_text(f"{self.get_value():.3f}")


            if self.keep_updating:
                self.value = (logica.mouse_pos[0] - self.x) / self.w
                if self.value < 0:
                    self.value = 0      
                if self.value > 1:
                    self.value = 1      


    def hide_plus_children(self, booleano, gerarchia=2):
        
        match gerarchia:
            case 0: self.hide_from_menu = booleano
            case 1: self.hide_from_window = booleano
            case 2: self.hide = booleano

        super().hide_plus_children(booleano, gerarchia)
        try: 
            self.label_title.hide = booleano
            self.indicatore.hide = booleano
        except: ...


    def move_update(self):
        self.label_title.move_update()
        self.indicatore.move_update()
        super().move_update()


    def update_context_menu(self, *args):
        super().update_context_menu(*args)
        self.label_title.update_context_menu(*args)
        self.indicatore.update_context_menu(*args)


    def update_window_change(self):
        super().update_window_change()
        self.label_title.update_window_change()
        self.indicatore.update_window_change()


    def check_for_lost_focus(self, events, logica, force_closure=False):
        self.indicatore.check_for_lost_focus(events, logica, force_closure)


class PopUp():
    def __init__(self, x, y, anchor, w, h):
        
        self.active = False
        self.conferma_uscita = False                    # richiede la conferma di uscita: False = Accettata e terminata, True = Lanciata ma non accetta e non terminata
        self.prima_entrata_bb = False

        self.packet_in = None
        self.packet_out = None

        self.context_menu: ContextMenu = ContextMenu(x=x, y=y, anchor=anchor, w=w, h=h, scrollable=False)
        self.context_menu.update_window_change()

    
    def start_connection(self, input):
        self.packet_in = input

    
    def end_connection(self):
        return self.packet_out


    def disegnami(self, logica):
        if self.active:
            self.context_menu.disegnami(logica)


    def eventami(self, eventi, logica: 'Logica', ask_for_exit=False):
        if self.active:
            bb = pygame.Rect(self.context_menu.x - self.context_menu.w // 4, self.context_menu.y - self.context_menu.h // 4, 1.5 * self.context_menu.w, 1.5 * self.context_menu.h)
            in_bb = bb.collidepoint(logica.mouse_pos)
            
            if not self.prima_entrata_bb and in_bb:
                self.prima_entrata_bb = True

            if not in_bb and self.prima_entrata_bb or ask_for_exit:
                [ele.check_for_lost_focus(eventi, logica, force_closure=True) for index, ele in self.context_menu.elements.items()]
                self.active = False
                self.conferma_uscita = True
                self.prima_entrata_bb = False


    def _COLOR_save(self, color, index):
        # Se il file esiste, lo carichiamo, altrimenti inizializziamo un dizionario vuoto
        if os.path.exists('GRAFICA/cache_colors.json'):
            with open('GRAFICA/cache_colors.json', "r") as f:
                dati = json.load(f)
        else:
            dati = {}

        hex_color = MateUtils.rgb2hex(color)

        if index == "recent":
            colori = dati[index]
            hex_color = MateUtils.rgb2hex(color)
            if not hex_color in colori:
                colori[MateUtils.rgb2hex(color)] = -1
                colori = {k: v + 1 for k, v in colori.items() if v < 8}
                dati[index] = colori

        elif index == "frequent":
            if hex_color in dati[index]:
                dati[index][hex_color] += 1
            else:
                dati[index][hex_color] = 1

        # Salviamo i dati aggiornati nel file
        with open('GRAFICA/cache_colors.json', "w") as f:
            json.dump(dati, f, indent=4)


    def _COLOR_load(self, index):
        """Returns a generator of the top 10 most used colors."""
        if not os.path.exists('GRAFICA/cache_colors.json'):
            return []  # Return an empty iterator if file doesn't exist

        with open('GRAFICA/cache_colors.json', "r") as f:
            data = json.load(f)

        colori = data[index]

        if not colori:
            return []  # Return an empty iterator if no colors are stored

        # Sort colors by frequency in descending order
        sorted_colors = sorted(colori.items(), key=lambda x: x[1], reverse=True)

        return sorted_colors


class PopUp_color_palette_easy(PopUp):
    def __init__(self, x, y, anchor, w, h):
        super().__init__(x, y, anchor, w, h)

        self.open_next = False
        self.update_return_color = False
        self.pos_indicatore_x, self.pos_indicatore_y = 0, 0
        self.init = True

        colori = [
            [255, 0, 0], [255, 128, 0], [255, 255, 0], [0, 255, 0], [0, 255, 255], [0, 128, 255], [128, 0, 255], [0, 0, 0],
            [255, 50, 50], [255, 153, 50], [255, 255, 50], [50, 255, 50], [50, 255, 255], [50, 153, 255], [153, 50, 255], [60, 60, 60],
            [255, 100, 100], [255, 181, 100], [255, 255, 100], [100, 255, 100], [100, 255, 255], [100, 181, 255], [181, 100, 255], [120, 120, 120],
            [255, 150, 150], [255, 206, 150], [255, 255, 150], [150, 255, 150], [150, 255, 255], [150, 206, 255], [206, 150, 255], [180, 180, 180],
            [255, 200, 200], [255, 231, 200], [255, 255, 200], [200, 255, 200], [200, 255, 255], [200, 231, 255], [231, 200, 255], [255, 255, 255],
        ]

        self.recent = [[0, 0, 0] for i in range(9)]
        self.frequent = [[0, 0, 0] for i in range(9)]

        for x in range(8):
            for y in range(5):
                adder = 0
                if x == 7:
                    adder = 1

                self.context_menu.add_element(f"bottone{x}_{y}", Bottone_Push(x=f"{11 * (x + adder) + 1}%w", y=f"{6 * y + 2}%w", anchor="lu", w="10%w", h="5%w", disable=True, function=BottoniCallbacks.change_state, bg=colori[y * 8 + x]))
                self.context_menu.elements[f"bottone{x}_{y}"].contorno = 0
        
        for x in range(9):
            self.context_menu.add_element(f"bottone_recent{x}", Bottone_Push(x=f"{11 * x + 1}%w", y=f"{35}%w", anchor="lu", w="10%w", h="5%w", disable=True, function=BottoniCallbacks.change_state, bg=self.recent[x]))
            self.context_menu.elements[f"bottone_recent{x}"].contorno = 0
        
        for x in range(9):
            self.context_menu.add_element(f"bottone_frequent{x}", Bottone_Push(x=f"{11 * x + 1}%w", y=f"{44}%w", anchor="lu", w="10%w", h="5%w", disable=True, function=BottoniCallbacks.change_state, bg=self.frequent[x]))
            self.context_menu.elements[f"bottone_frequent{x}"].contorno = 0
        
        self.context_menu.add_element("cancel", Bottone_Push(x="100%w", y="100%h", anchor="rd", w="12.5%w", h="7.5%h", text="\\#dc143c{Cancel}", function=BottoniCallbacks.change_state))
        self.context_menu.add_element("more_option", Bottone_Push(x="80%w", y="100%h", anchor="rd", w="17%w", h="7.5%h", text="\\#aaff00{More options}", function=BottoniCallbacks.change_state))

        self.context_menu.update_window_change()

        self.main_color = [0, 0, 0]


    def disegnami(self, logica):

        if self.active:
            ...

        super().disegnami(logica)


    def eventami(self, eventi, logica: 'Logica'):

        if self.active:

            if self.init:
                self.init = False

                colori = self._COLOR_load("frequent")
                colori_recent = self._COLOR_load("recent")
                controlled_colors = 0
                controlled_colors_recent = 0

                for index, bottone in self.context_menu.elements.items():
                    if "frequent" in index:
                        try:
                            colore = colori[controlled_colors]
                            controlled_colors += 1
                            bottone.bg = MateUtils.hex2rgb(colore[0])
                        except IndexError as e:
                            ...
                    elif "recent" in index:
                        try:
                            colore = colori_recent[controlled_colors_recent]
                            controlled_colors_recent += 1
                            bottone.bg = MateUtils.hex2rgb(colore[0])
                        except IndexError as e:
                            ...



            self.context_menu.eventami(eventi, logica)

            for indice, bottone in self.context_menu.elements.items():
                if "bottone" in indice:
                    if bottone.flag_foo:
                        bottone.flag_foo = False
                        self.main_color = bottone.bg
                        self.update_return_color = True
                        super().eventami(eventi, logica, True)

            if self.context_menu.elements["cancel"].flag_foo:
                self.context_menu.elements["cancel"].flag_foo = False
                self.update_return_color = False
                super().eventami(eventi, logica, True)
            
            elif self.context_menu.elements["more_option"].flag_foo:
                self.context_menu.elements["more_option"].flag_foo = False
                self.open_next = True
                super().eventami(eventi, logica, True)
            
            else:
                super().eventami(eventi, logica)


    def start_connection(self, input):
        super().start_connection(input)
        self.init = True
        self.main_color = self.packet_in
        self.original = self.packet_in

    
    def end_connection(self):

        if self.update_return_color:
            self.packet_out = self.main_color
            self._COLOR_save(self.packet_out, "frequent")
            self._COLOR_save(self.packet_out, "recent")
        else:
            self.packet_out = self.packet_in

        self.update_return_color = False
        return super().end_connection()
    
        
    def update_window_change(self):
        self.context_menu.update_window_change()
        [ele.update_window_change() for index, ele in self.context_menu.elements.items()]



class PopUp_color_palette_hard(PopUp):
    def __init__(self, x, y, anchor, w, h):
        super().__init__(x, y, anchor, w, h)

        self.update_return_color = False
        self.pos_indicatore_x, self.pos_indicatore_y = 0, 0

        self.context_menu.add_element("entrata_hex", Entrata(x="100%w -5%h", y="5%h", w="10%w", h="30px", anchor="ru", text="dc143c", title="HEX", is_hex=True))
        self.context_menu.add_element("entrata_R", Entrata(x="100%w -5%h", y="5%h 80px", w="5%w", h="30px", anchor="ru", text="220", title="R", lunghezza_max=4, num_valore_massimo=255, num_valore_minimo=0, solo_numeri=True))
        self.context_menu.add_element("entrata_G", Entrata(x="100%w -5%h", y="5%h 120px", w="5%w", h="30px", anchor="ru", text="20", title="G", lunghezza_max=4, num_valore_massimo=255, num_valore_minimo=0, solo_numeri=True))
        self.context_menu.add_element("entrata_B", Entrata(x="100%w -5%h", y="5%h 160px", w="5%w", h="30px", anchor="ru", text="60", title="B", lunghezza_max=4, num_valore_massimo=255, num_valore_minimo=0, solo_numeri=True))

        self.context_menu.add_element("preview", Bottone_Push(x="97.5%h", y="80%h", anchor="ld", w="15%w", h="75%h", disable=True))
        self.context_menu.add_element("ok", Bottone_Push(x="100%w", y="100%h", anchor="rd", w="10%w", h="7.5%h", text="\\#aaff00{OK}", function=BottoniCallbacks.change_state))
        self.context_menu.add_element("cancel", Bottone_Push(x="87.5%w", y="100%h", anchor="rd", w="12.5%w", h="7.5%h", text="\\#dc143c{Cancel}", function=BottoniCallbacks.change_state))

        self.context_menu.add_element("color_array", Screen(x="5%h", y="5%h", w="90%h", h="75%h", anchor="lu"))
        self.context_menu.add_element("inten_array", Screen(x="5%h", y="82.5%h", w="90%h", h="4.5%h", anchor="lu"))
        self.context_menu.add_element("slider_RGB", Slider(x="5%h", y="95%h", w="90%h", h="5%h", initial_value=1, anchor="ld"))

        self.context_menu.update_window_change()

        self.main_color = [0, 0, 0]


    def disegnami(self, logica):

        if self.active:
            try:
                self.context_menu.elements["preview"].bg = self.main_color
                self.context_menu.elements["preview"].contorno = 0
            except:
                ...

            self.context_menu.elements["color_array"]._clear_canvas()
            self.context_menu.elements["color_array"]._paste_array(self.generate_array_color() * 255, (0, 0))
            
            self.context_menu.elements["inten_array"]._clear_canvas()
            self.context_menu.elements["inten_array"]._paste_array(self.generate_inten_color() * 255, (0, 0))

            self.context_menu.elements["color_array"]._add_points([[self.pos_indicatore_x, self.pos_indicatore_y]], [255, 255, 255], 10, 3)
            self.context_menu.elements["color_array"]._add_points([[self.pos_indicatore_x, self.pos_indicatore_y]], [0, 0, 0], 12, 2)
            self.context_menu.elements["color_array"]._add_points([[self.pos_indicatore_x, self.pos_indicatore_y]], [0, 0, 0], 7, 2)
        
        super().disegnami(logica)


    def eventami(self, eventi, logica: 'Logica'):
        
        if self.active:
            self.context_menu.eventami(eventi, logica)

            if self.context_menu.elements["entrata_hex"].selezionato:
                self.main_color = MateUtils.hex2rgb(self.context_menu.elements["entrata_hex"].get_text(real_time=True))      # per display del colore attuale

                self.context_menu.elements["entrata_R"].change_text(f"{self.main_color[0]}")
                self.context_menu.elements["entrata_G"].change_text(f"{self.main_color[1]}")
                self.context_menu.elements["entrata_B"].change_text(f"{self.main_color[2]}")
                self.rgb_to_xy(self.main_color)
            
            elif self.context_menu.elements["entrata_R"].selezionato or self.context_menu.elements["entrata_G"].selezionato or self.context_menu.elements["entrata_B"].selezionato:
                self.main_color = [MateUtils.inp2int(self.context_menu.elements["entrata_R"].get_text(real_time=True)), MateUtils.inp2int(self.context_menu.elements["entrata_G"].get_text(real_time=True)), MateUtils.inp2int(self.context_menu.elements["entrata_B"].get_text(real_time=True))]      # per display del colore attuale

                self.context_menu.elements["entrata_hex"].change_text(MateUtils.rgb2hex(self.main_color))
                self.rgb_to_xy(self.main_color)


            for event in eventi:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or logica.dragging:
                    if self.context_menu.elements["color_array"].bounding_box.collidepoint(logica.mouse_pos):
                        self.pos_indicatore_x = logica.mouse_pos[0] - self.context_menu.elements["color_array"].x
                        self.pos_indicatore_y = logica.mouse_pos[1] - self.context_menu.elements["color_array"].y
                        self.update_text_from_coords()
                    
                    elif self.context_menu.elements["slider_RGB"].keep_updating:
                        self.update_text_from_coords()


            if self.context_menu.elements["ok"].flag_foo:
                self.context_menu.elements["ok"].flag_foo = False
                self.update_return_color = True
                super().eventami(eventi, logica, True)

            elif self.context_menu.elements["cancel"].flag_foo:
                self.context_menu.elements["cancel"].flag_foo = False
                self.update_return_color = False
                super().eventami(eventi, logica, True)
            
            else:
                super().eventami(eventi, logica)


    def start_connection(self, input):
        super().start_connection(input)
        self.main_color = self.packet_in
        self.original = self.packet_in

        self.context_menu.elements["entrata_hex"].change_text(MateUtils.rgb2hex(self.main_color))
        self.context_menu.elements["entrata_R"].change_text(f"{self.main_color[0]}")
        self.context_menu.elements["entrata_G"].change_text(f"{self.main_color[1]}")
        self.context_menu.elements["entrata_B"].change_text(f"{self.main_color[2]}")
        self.rgb_to_xy(self.main_color)

    
    def end_connection(self):

        if self.update_return_color:
            self.main_color = MateUtils.hex2rgb(self.context_menu.elements["entrata_hex"].get_text())                  # per il return
            self.packet_out = self.main_color
            self._COLOR_save(self.packet_out, "frequent")
            self._COLOR_save(self.packet_out, "recent")
        else:
            self.packet_out = self.packet_in

        self.update_return_color = False
        return super().end_connection()
    

    def update_text_from_coords(self):
        intensity = self.context_menu.elements["slider_RGB"].value
        saturation = self.pos_indicatore_y / self.context_menu.elements["color_array"].h
        rgb = self.pos_indicatore_x / self.context_menu.elements["color_array"].w

        baseline = saturation * 255
        free_delta = 255 - baseline
        
        rgb *= 6
        resto = rgb - int(rgb)
        resto *= free_delta

        if 0 < rgb and rgb <= 1:
            risultato = np.array([free_delta, resto, 0]) + baseline
        elif 1 < rgb and rgb <= 2:
            risultato = np.array([free_delta - resto, free_delta, 0]) + baseline
        elif 2 < rgb and rgb <= 3:
            risultato = np.array([0, free_delta, resto]) + baseline
        elif 3 < rgb and rgb <= 4:
            risultato = np.array([0, free_delta - resto, free_delta]) + baseline
        elif 4 < rgb and rgb <= 5:
            risultato = np.array([resto, 0, free_delta]) + baseline
        elif 5 < rgb and rgb <= 6:
            risultato = np.array([free_delta, 0, free_delta - resto]) + baseline
        else:
            return
        
        if saturation < 0 or saturation > 1:
            return

        self.main_color = risultato * intensity

        self.context_menu.elements["entrata_hex"].change_text(MateUtils.rgb2hex(self.main_color.astype(int)))

        self.context_menu.elements["entrata_R"].change_text(f"{round(self.main_color[0])}")
        self.context_menu.elements["entrata_G"].change_text(f"{round(self.main_color[1])}")
        self.context_menu.elements["entrata_B"].change_text(f"{round(self.main_color[2])}")

    
    def generate_inten_color(self):
        w = round(self.context_menu.elements["color_array"].w)
        h = round(self.context_menu.elements["color_array"].h)
        mat = np.zeros((w, h, 3))

        for x in range(w):
            # controls Hue
            mat[x, :, :] = x / w

        return mat


    def generate_array_color(self):
        w = round(self.context_menu.elements["color_array"].w)
        h = round(self.context_menu.elements["color_array"].h)
        mat = np.zeros((w, h, 3))

        for x in range(w):
            # controls Hue
            mat[x, :, :] = PopUp_color_palette_hard.interpolation(x / w) 

        for y in range(h):
            # controls Saturation
            mat[:, y, :] *= 1 - (y / w)
            mat[:, y, :] += (y / w)

        # controls Intensity
        mat[:, :, :] *= self.context_menu.elements["slider_RGB"].value

        return mat


    def rgb_to_xy(self, rgb):
            
        w = round(self.context_menu.elements["color_array"].w)
        h = round(self.context_menu.elements["color_array"].h)
        
        r, g, b = np.array(rgb) / 255.0  # Normalizzazione
        x, y = 0, 0

        max_v = max(r, g, b)
        min_v = min(r, g, b)

        # Calcolo dell'intensità
        intensity = max_v
        
        # Calcolo della saturazione
        y = 1 - ((max_v - min_v) / max_v)
        y *= h

        
        r, g, b = (rgb - np.min(rgb)) / (np.max(rgb) - np.min(rgb))

        # match della possibile combinazione
        # 100 -> 110 -> 010 -> 011 -> 001 -> 101 -> 100
        #  0  ->  1  ->  2  ->  3  ->  4  ->  5  ->  6
        if r == 1:
            # tonalità di rosso
            if g == 0:
                x = - b * w / 6 + 6 * w / 6
            elif b == 0:
                x = g * w / 6 + 0 * w / 6

        elif g == 1:
            # tonalità di verde
            if r == 0:
                x = b * w / 6 + 2 * w / 6
            elif b == 0:
                x = - r * w / 6 + 2 * w / 6

        elif b == 1:
            if r == 0:
                x = - g * w / 6 + 4 * w / 6
            elif g == 0:
                x = r * w / 6 + 4 * w / 6

        self.pos_indicatore_x = x
        self.pos_indicatore_y = y
        self.context_menu.elements["slider_RGB"].value = intensity


    @staticmethod
    def interpolation(value):
        # 100 -> 110 -> 010 -> 011 -> 001 -> 101 -> 100
        #  0  ->  1  ->  2  ->  3  ->  4  ->  5  ->  6
        normalization_factor = 1 / 6
        index = value // normalization_factor
        inner_interpolation = (value % normalization_factor) / (1/6)

        def interpolate(x1, y1, z1, x2, y2, z2, value):
            if value == 0:
                x, y, z = x1, y1, z1
            else:
                x = x1 + (x2 - x1) * value
                y = y1 + (y2 - y1) * value
                z = z1 + (z2 - z1) * value
            return np.array([x, y, z])

        if index == 0:
            return interpolate(1, 0, 0, 1, 1, 0, inner_interpolation)
        elif index == 1:
            return interpolate(1, 1, 0, 0, 1, 0, inner_interpolation)
        elif index == 2:
            return interpolate(0, 1, 0, 0, 1, 1, inner_interpolation)
        elif index == 3:
            return interpolate(0, 1, 1, 0, 0, 1, inner_interpolation)
        elif index == 4:
            return interpolate(0, 0, 1, 1, 0, 1, inner_interpolation)
        elif index == 5:
            return interpolate(1, 0, 1, 1, 0, 0, inner_interpolation)
        elif index == 6:
            return np.array([1, 0, 0])
        

    def update_window_change(self):
        self.context_menu.update_window_change()
        [ele.update_window_change() for index, ele in self.context_menu.elements.items()]


class Screen(BaseElement):

    def __init__(self, x="", y="", anchor="lu", w="", h="", hide=False, latex_font=False, screenshot_type=False, tooltip="", show_tooltip=True):
        super().__init__(x, y, anchor, w, h, "", hide, latex_font=latex_font, tooltip=tooltip, show_tooltip=show_tooltip)

        self.screenshot_type = screenshot_type
        self.tavolozza = pygame.Surface((self.w, self.h))
        self.last_click_pos = (-1, -1)
        self.last_click_pos_changed = False


    def eventami(self, events, logica: 'Logica'):

        if self.hide == False or self.screenshot_type == False:

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.bounding_box.collidepoint(event.pos):
                        self.last_click_pos = logica.mouse_pos
                        self.last_click_pos_changed = True

    
    def update_window_change(self):
        super().update_window_change()
        self.tavolozza = pygame.transform.scale(self.tavolozza, (self.w, self.h))
    

    def disegnami(self, logica):
        if self.do_stuff and not self.screenshot_type:
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

    
    def _blit_surface(self, surface, position, scale=[1, 1]):
        if scale != [1, 1]:
            surface = pygame.transform.scale(surface, scale)
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

        except Exception:
            pass
    

    def load_image(self, path:str):
        self.loaded_image = pygame.image.load(path)
    
    
    def scale_image(self, scale:tuple):
        self.loaded_image = pygame.transform.scale(self.loaded_image, scale)