import pygame
from numpy import array
from MATEMATICA._modulo_mate_utils import MateUtils
import pyperclip
import os

NON_ESEGUIRE = False

if NON_ESEGUIRE:    
    from pygame.event import Event
    from _modulo_UI import Logica

from GRAFICA._modulo_database import Dizionario; diction = Dizionario()



class BaseElement:

    pappardella = None

    def __init__(self, x=0, y=0, w=0, h=0, mantain_proportion=False, text="", scala=1, hide=False) -> None:
        
        self.schermo = BaseElement.pappardella["screen"]

        self.font: Font = Font(24 * BaseElement.pappardella["rapporto_y"] * scala)

        self.scala = scala

        self.testo: str = text
        self.color_text = (200, 200, 200)
        self.bg = array(BaseElement.pappardella["bg_def"])

        self.hide: bool = hide

        self.recalc_geometry("percentage", x, y, w, h, mantain_proportion)


    @classmethod
    def _init_scene(cls, pappardella) -> None:
        cls.pappardella = pappardella 


    def disegnami(self, logica):
        ...

    
    def eventami(self, events, logica):
        ...


    def recalc_geometry(self, mode="percentage", new_x=-1, new_y=-1, new_w=-1, new_h=-1, mantain_proportion=False):

        self.mantain_prop = mantain_proportion

        match mode:
            case "percentage": proportion_x, proportion_y = self.pappardella["moltiplicatore_x"] / 100, self.pappardella["ori_y"] / 100
            case "pixel": proportion_x, proportion_y = 1, 1

        if self.mantain_prop:
            if new_x > -1: self.x: float = new_x * proportion_x + self.pappardella["offset"]
            if new_y > -1: self.y: float = new_y * proportion_x
            if new_w > -1: self.w: float = new_w * proportion_x
            if new_h > -1: self.h: float = new_h * proportion_x

        else:
            if new_x > -1: self.x: float = new_x * proportion_x + self.pappardella["offset"]
            if new_y > -1: self.y: float = new_y * proportion_y
            if new_w > -1: self.w: float = new_w * proportion_x
            if new_h > -1: self.h: float = new_h * proportion_y
    
        self.recalc_BB()


    def recalc_BB(self, offset_x=0, offset_y=0, offset_w=0, offset_h=0):
        self.bounding_box = pygame.Rect(self.x + offset_x, self.y + offset_y, self.w + offset_w, self.h + offset_h)


    def pixel2percentage(value, axis="x"):
        if axis == "x": return value * 100 / BaseElement.pappardella["moltiplicatore_x"]
        if axis == "y": return value * 100 / BaseElement.pappardella["ori_y"]


    def percentage2pixel(value, axis="x"):
        if axis == "x": return value * BaseElement.pappardella["moltiplicatore_x"] / 100
        if axis == "y": return value * BaseElement.pappardella["ori_y"] / 100



class Label_Text(BaseElement):

    def __init__(self, x=0, y=0, text="", scala=1, hide=False):
        super().__init__(x, y, 0, 0, False, text, scala, hide)


    def disegnami(self, logica, offset_x: int = 0, offset_y: int = 0, center=False):

        if not self.hide:

            # sostituzione caratteri speciali
            testo_analisi = SubStringa.analisi_caratteri_speciali(self.testo)

            for index, frase in enumerate(testo_analisi.split("\n")):

                # offset multi-riga
                offset_frase = index * self.font.font_pixel_dim[1]
        
                # analisi dei tag composti da "\tag{...}"
                elenco_substringhe = SubStringa.start_analize(frase)
                
                original_spacing_x = self.font.font_pixel_dim[0]
                original_spacing_y = self.font.font_pixel_dim[1]

                offset_orizzontale = 0
                offset_orizzontale_apice = 0
                offset_orizzontale_pedice = 0

                for substringa_analizzata in elenco_substringhe:

                    centratura_x = - (center * original_spacing_x * len(substringa_analizzata.testo) / 2)
                    centratura_y = - (center * original_spacing_y // 2)
            
                    if substringa_analizzata.apice:
                        offset_highlight = - 0.5

                        offset_usato = offset_orizzontale_apice  
                    elif substringa_analizzata.pedice:
                        offset_highlight = - 0.5

                        offset_usato = offset_orizzontale_pedice 
                    else:
                        offset_highlight = - 1 

                        offset_usato = offset_orizzontale
                        offset_orizzontale_apice = offset_orizzontale
                        offset_orizzontale_pedice = offset_orizzontale

                    if substringa_analizzata.colore is None: substringa_analizzata.colore = self.color_text

                    offset_pedice_apice = original_spacing_y * 0.5 if substringa_analizzata.pedice else - original_spacing_y * 0.1 if substringa_analizzata.apice else 0

                    if substringa_analizzata.pedice or substringa_analizzata.apice:
                        self.font.scala_font(0.5)

                    if substringa_analizzata.highlight:
                        self.schermo.blit(self.font.font_pyg_r.render("" + "█" * (len(substringa_analizzata.testo)) + "", True, [100, 100, 100]), (self.x + original_spacing_x * ( offset_highlight + offset_usato) + offset_x + centratura_x, self.y + offset_frase + offset_pedice_apice + offset_y + centratura_y))

                    if substringa_analizzata.bold:
                        self.schermo.blit(self.font.font_pyg_b.render(substringa_analizzata.testo, True, substringa_analizzata.colore), (self.x + original_spacing_x * offset_usato + offset_x + centratura_x, self.y + offset_frase + offset_pedice_apice + offset_y + centratura_y))
                    elif substringa_analizzata.italic:
                        self.schermo.blit(self.font.font_pyg_i.render(substringa_analizzata.testo, True, substringa_analizzata.colore), (self.x + original_spacing_x * offset_usato + offset_x + centratura_x, self.y + offset_frase + offset_pedice_apice + offset_y + centratura_y))
                    else:
                        self.schermo.blit(self.font.font_pyg_r.render(substringa_analizzata.testo, True, substringa_analizzata.colore), (self.x + original_spacing_x * offset_usato + offset_x + centratura_x, self.y + offset_frase + offset_pedice_apice + offset_y + centratura_y))
                    
                    if substringa_analizzata.pedice or substringa_analizzata.apice:
                        self.font.scala_font(2)

                    
                    if substringa_analizzata.apice: offset_orizzontale_apice += substringa_analizzata.end
                    elif substringa_analizzata.pedice: offset_orizzontale_pedice += substringa_analizzata.end
                    else:
                        offset_orizzontale_apice += substringa_analizzata.end
                        offset_orizzontale_pedice += substringa_analizzata.end

                    offset_orizzontale = max(offset_orizzontale_apice, offset_orizzontale_pedice)


class Bottone_Push(BaseElement):

    def __init__(self, x=0, y=0, w=0, h=0, function=None, mantain_proportion=False, text="", scala=1, hide=False, disable=False):
        super().__init__(x, y, w, h, mantain_proportion, text, scala, hide)

        self.contorno = 2

        self.callback = function

        if self.callback is None:
            def Fuffa(): ...
            self.callback = Fuffa

        self.animazione = Animazione(100, "once")
        self.hover = False

        self.disable: bool = disable
        self.suppress_animation: bool = False

        self.lable_title = Label_Text(x=x, y=y, text=text, scala=scala)

        self.smussatura = 20

    
    def disegnami(self, logica: 'Logica'):

        if not self.hide:

            colore = self.bg.copy()
            
            if not self.disable:
                colore = self.animazione_press(logica.dt, colore)
                colore = self.animazione_hover(colore)

            colore = [s_colore if s_colore <= 255 else 255 for s_colore in colore]

            pygame.draw.rect(self.schermo, colore, [self.x, self.y, self.w, self.h], self.contorno, self.smussatura)

            self.lable_title.disegnami(logica, self.w / 2, self.h / 2, center=True)

    
    def eventami(self, events: list['Event'], logica: 'Logica'):

        if not self.hide or not self.disable:

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.bounding_box.collidepoint(event.pos):
                        self.callback()
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
        self.lable_title.testo = text


class Bottone_Toggle(BaseElement):
    def __init__(self, x=0, y=0, w=0, h=0, state=False, type_checkbox=True, mantain_proportion=False, text="", scala=1, hide=False):
        super().__init__(x, y, w, h, mantain_proportion, text, scala, hide)
        
        
        self.contorno = 2

        if type_checkbox:            
            self.recalc_geometry(new_w=1, new_h=1, mantain_proportion=True)

        self.label_title = Label_Text(x=x, y=y, text=text)

        self.checkbox = type_checkbox

        self.state_toggle = state

        self.animazione = Animazione(-1, "once")
        self.hover = False

        self.disable: bool = False

        self.smussatura = 5


    def disegnami(self, logica):

        if not self.hide:

            colore = self.bg.copy()

            colore = self.animazione_press(colore)
            colore = self.animazione_hover(colore)

            if self.checkbox:

                pygame.draw.rect(self.schermo, colore, [self.x, self.y, self.w, self.h], self.contorno, self.smussatura)

                if self.state_toggle:
                    pygame.draw.rect(self.schermo, [255, 255, 255], [self.x + 4, self.y + 4, self.w - 8, self.h - 8], self.contorno, self.smussatura)


                self.label_title.disegnami(logica, self.font.font_pixel_dim[0] * 2.5, (self.h - self.font.font_pixel_dim[1]) / 2, center=False)
            
            else:

                pygame.draw.rect(self.schermo, colore, [self.x, self.y, self.w, self.h], self.contorno, self.smussatura)
                self.label_title.disegnami(logica, self.w / 2, self.h / 2, center=True)


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



class RadioButton(BaseElement):
    def __init__(self, x=0, y=0, w=0, h=0, mantain_proportion=False, axis="x", cb_n=1, cb_s=False, cb_t="Default item", title="", multiple_choice=False, scala=1, hide=False, type_checkbox=True, w_button=1, h_button=1):
        super().__init__(x, y, w, h, mantain_proportion, title, scala, hide)

        self.w_button = w_button
        self.h_button = h_button

        self.main_ax = axis
        
        self.title = title
        self.multiple_choice = multiple_choice

        self.hide = hide

        self.type_checkbox = type_checkbox

        ry = BaseElement.pappardella["moltiplicatore_x"] / BaseElement.pappardella["ori_y"] # rapporto y

        self.toggles: list[Bottone_Toggle] = []
        for index, state, text  in zip(range(cb_n), cb_s, cb_t):
            
            match self.main_ax:
                case "x": 
                    if self.type_checkbox:
                        spacing = (w - (self.w_button * cb_n)) / (cb_n - 1)
                        self.toggles.append(Bottone_Toggle(x + index * (self.w_button + spacing), y, self.w_button, self.h_button, state, type_checkbox, text=text, scala=scala, hide=hide))

                    else:
                        spacing = (w - (self.w_button * cb_n)) / (cb_n - 1)
                        self.toggles.append(Bottone_Toggle(x + index * (self.w_button + spacing), y, self.w_button, self.h_button, state, type_checkbox, text=text, scala=scala, hide=hide))

                case "y":
                    if self.type_checkbox:

                        spacing = (h - (self.h_button * cb_n * ry)) / (cb_n - 1)

                        self.toggles.append(Bottone_Toggle(x, y + index * (self.h_button * ry + spacing), self.w_button, self.h_button, state, type_checkbox, text=text, scala=scala, hide=hide))
                    
                    else:
                        spacing = (h - (self.h_button * cb_n)) / (cb_n - 1)

                        self.toggles.append(Bottone_Toggle(x, y + index * (self.h_button + spacing), self.w_button, self.h_button, state, type_checkbox, text=text, scala=scala, hide=hide))

                case _: raise TypeError(f"Invalid mode {self.main_ax}, accepted types: 'x', 'y'.")

            
        for ele in self.toggles:
            ele.bg += array([10, 10, 10])



    def disegnami(self, logica):
        pygame.draw.rect(self.schermo, self.bg, [self.x, self.y, self.w, self.h], 0, 5)
        [bottone.disegnami(logica) for bottone in self.toggles]


    def eventami(self, events, logica):

        old_state = self.buttons_state

        [bottone.eventami(events, logica) for bottone in self.toggles]
        
        new_state = self.buttons_state

        if not self.multiple_choice:
            ele_vecchio, ele_nuovo = self.check_for_diff(old_state, new_state)

            if not ele_nuovo is None and not ele_vecchio is None:
                self.toggles[ele_vecchio].state_toggle = False


    @property
    def buttons_state(self):
        return [bottone.state_toggle for bottone in self.toggles]


    def check_for_diff(self, list1, list2):

        elemento_vecchio = None
        elemento_nuovo = None

        for index, state1, state2 in zip(range(len(list1)), list1, list2):
            if state1 != state2:
                elemento_nuovo = index

            if state1 == state2 and state1 == 1:
                elemento_vecchio = index

        return elemento_vecchio, elemento_nuovo



class Entrata(BaseElement):
    def __init__(self, x=0, y=0, w=0, h=0, mantain_proportion=False, text="", scala=1, hide=False, lunghezza_max=None, solo_numeri=False, num_valore_minimo=None, num_valore_massimo=None, is_hex=False):
        super().__init__(x, y, w, h, mantain_proportion, text, scala, hide)
        
        
        self.contorno = 2

        self.offset_grafico_testo = 5
        self.puntatore_pos = 0
        self.highlight_region: list[int] = [0, 0]

        self.selezionato = False
        self.hover = False

        self.lunghezza_max = lunghezza_max
        self.solo_numeri = solo_numeri
        self.num_valore_minimo = num_valore_minimo
        self.num_valore_massimo = num_valore_massimo
        self.is_hex = is_hex

        self.animazione_puntatore = Animazione(1000, "loop")
        self.animazione_puntatore.attiva = True



    def disegnami(self, logica: 'Logica'):

        if not self.hide:

            colore = self.bg.copy()

            colore = self.animazione_press(colore)
            colore = self.animazione_hover(colore)

            pygame.draw.rect(self.schermo, colore, [self.x, self.y, self.w, self.h], self.contorno, 5)

            if self.selezionato:
                pygame.draw.rect(self.schermo, [90, 90, 90], [self.x + self.font.font_pixel_dim[0] * self.highlight_region[0] + self.offset_grafico_testo, self.y, self.font.font_pixel_dim[0] * (self.highlight_region[1] - self.highlight_region[0]), self.h], 0, 5)

            # testo
            self.schermo.blit(self.font.font_pyg_r.render(self.testo, True, self.color_text), (self.x + self.offset_grafico_testo, self.y + self.h / 2 - self.font.font_pixel_dim[1] / 2))

            # puntatore flickerio
            self.animazione_puntatore.update(logica.dt)
            if self.selezionato and self.animazione_puntatore.dt < 500:
                offset_puntatore_pos = self.font.font_pixel_dim[0] * self.puntatore_pos
                pygame.draw.rect(self.schermo, [200, 200, 200], [self.x + self.offset_grafico_testo + offset_puntatore_pos, self.y, 2, self.h], 0)


    def eventami(self, events: list['Event'], logica: 'Logica'):
        
        if not self.hide:

            if self.selezionato:
                self.eventami_scrittura(events, logica)

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


            if self.solo_numeri:
                numero_equivalente = MateUtils.inp2flo(self.testo, None)

                if numero_equivalente is None:
                    self.color_text = array([255, 0, 0])

                else:
                    self.color_text = array((200, 200, 200))

                    if numero_equivalente > self.num_valore_massimo:
                        self.change_text(f"{self.num_valore_massimo}")
                    elif numero_equivalente < self.num_valore_minimo:
                        self.change_text(f"{self.num_valore_minimo}")


            if self.is_hex:
                if MateUtils.hex2rgb(self.testo, std_return=None) is None:
                    self.color_text = array([255, 0, 0])
                else:
                    self.color_text = array([200, 200, 200])


            if reset_animation:
                self.animazione_puntatore.riavvia()



    def update_puntatore_pos(self, pos: tuple[int]):
        x, y = pos
        
        self.puntatore_pos = self.get_puntatore_pos(x)


    def get_puntatore_pos(self, x: int):
        ris = round((x - self.x - self.offset_grafico_testo) / (self.font.font_pixel_dim[0] * self.scala))
    
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
            self.contorno = 2
        
        return colore


    def animazione_hover(self, colore):
        if self.hover:
            self.contorno = 0
            colore += 10
        elif not self.selezionato:
            self.contorno = 2
        return colore
    

    def change_text(self, text):
        self.testo = text



class Scroll(BaseElement):
    def __init__(self, x=0, y=0, w=0, h=0, mantain_proportion=False, text="", scala=1, hide=False):
        super().__init__(x, y, w, h, mantain_proportion, text, scala, hide)
        
        self.titolo = "Scroll console..."
        self.color_text_selected = (40, 100, 40)

        self.bg_selected = (60, 70, 70)
        
        self.contorno = 2

        self.no_dragging_animation = False

        self.elementi = [i for i in range(100)]
        self.ele_mask = [False for _ in range(len(self.elementi))]
        self.ele_selected_index = 0
        self.ele_first = 0
        
        self.ele_max = int((self.h - self.font.font_pixel_dim[1] * 2) // self.font.font_pixel_dim[1])

        # creazione toggles
        y_bottone = self.font.font_pixel_dim[1] * 100 / BaseElement.pappardella["ori_y"]    
        y_centratura_toggle = 100 * (((self.font.font_pixel_dim[1]) - (BaseElement.pappardella["moltiplicatore_x"] * 1 / 100)) / 2) / BaseElement.pappardella["ori_y"] 
        self.ele_toggle = [Bottone_Toggle(x=x + w * 0.01, y=y + y_centratura_toggle + y_bottone * (i + 2), state=False, text="") for i in range(self.ele_max)]

        for ele in self.ele_toggle:
            ele.bg += array([10, 10, 10])

        self.offset_grafico_testo = self.w * 0.02 + self.ele_toggle[0].w

        self.selezionato = False
        self.hover = False

        self.animazione_puntatore = Animazione(1000, "loop")
        self.animazione_puntatore.attiva = True

        self.bounding_box = pygame.Rect(self.x + self.offset_grafico_testo, self.y, self.w - self.offset_grafico_testo, self.h)


    @property
    def elemento_attivo(self):
        return self.selected + self.first_element


    def disegnami(self, logica: 'Logica'):

        # creazione titolo
        self.font.scala_font(1.5)
        
        pygame.draw.rect(self.schermo, self.bg, [self.x, self.y, self.w, self.h], 0, 5)
        
        self.schermo.blit(self.font.font_pyg_r.render(f"{self.titolo}", True, self.color_text), (self.x + self.offset_grafico_testo, self.y + self.font.font_pixel_dim[1] / 1.5 - self.font.font_pixel_dim[1] / 2))
        
        self.font.scala_font(1 / 1.5)

        # creazione elementi (righe)
        alt_font = self.font.font_pixel_dim[1]

        for chunck in range(int((self.h - alt_font * 2) // alt_font)):
            
            if self.ele_selected_index == chunck + self.ele_first:
                colore = self.bg_selected
            else:
                colore_bg = self.bg.copy()
                colore_var1 = colore_bg + 10
                colore_var2 = colore_bg + 20
                colore = colore_var1 if chunck % 2 == 0 else colore_var2

            pygame.draw.rect(self.schermo, colore, [self.x + self.offset_grafico_testo, (self.y + alt_font * 2) + alt_font * chunck, self.w - self.offset_grafico_testo, alt_font], 0, 5)
    

        # creazione elementi (testo)
        self.ele_max = int((self.h - self.font.font_pixel_dim[1] * 2) // self.font.font_pixel_dim[1])
        for ele_iterator in range(self.ele_max):
            
            if self.ele_first + ele_iterator >= len(self.elementi):
                break

            testo = f"{self.elementi[self.ele_first + ele_iterator]}"

            if self.ele_selected_index == ele_iterator + self.ele_first:
                colore = self.color_text_selected
            else:
                colore = self.color_text
                

            self.schermo.blit(self.font.font_pyg_r.render(testo, True, colore), (self.x + self.offset_grafico_testo + 5, self.y + (alt_font * (2 + ele_iterator))))
        

        # creazione toggles
        [bottone.disegnami(logica) for bottone in self.ele_toggle]

        # disegno elementi grafici di drag
        if logica.dragging and not self.no_dragging_animation:

            if self.bounding_box.collidepoint(logica.mouse_pos):

                pygame.draw.rect(self.schermo, self.bg_selected, [logica.mouse_pos[0], logica.mouse_pos[1], self.w - self.offset_grafico_testo, self.font.font_pixel_dim[1]], 0, 5)
                self.schermo.blit(self.font.font_pyg_r.render(f"{self.elementi[self.ele_selected_index]}", True, self.color_text_selected), (logica.mouse_pos[0] + 5, logica.mouse_pos[1]))

                # mostro dove finisce l'elemento
                elemento_finale = round((logica.mouse_pos[1] - self.y - self.font.font_pixel_dim[1] // 2) // self.font.font_pixel_dim[1]) - 2 + 1 # il +1 è per risolvere un problema grafico in cui il calcolo non tiene conto che l'operazione non è ancora stata eseguita
                pygame.draw.rect(self.schermo, [255, 200, 0], [self.x + self.offset_grafico_testo, (self.y + alt_font * 2) + alt_font * elemento_finale, self.w - self.offset_grafico_testo, 1], 0, 5)



    def eventami(self, events: list['Event'], logica: 'Logica'):
        
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
                        self.ele_selected_index = self.ele_first + round((logica.mouse_pos[1] - self.y) // self.font.font_pixel_dim[1]) - 2
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
                        rilascio = self.ele_first + round((logica.mouse_pos[1] - self.y - self.font.font_pixel_dim[1] // 2) // self.font.font_pixel_dim[1]) - 2
                        
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



class ColorPicker(BaseElement):
    def __init__(self, x=0, y=0, w=0, h=0, initial_color=[200, 200, 200], mantain_proportion=False, text="", scala=1, hide=False):
        super().__init__(x, y, w, h, mantain_proportion, text, scala, hide)
        
        self.opener = Bottone_Push(x, y, w, h, self.apri_picker, hide=hide)
        self.opener.suppress_animation = True
        self.opener.contorno = 0

        self.title = text
        
        self.palette = Palette(x + w / 2, y, initial_color)
        self.picked_color = initial_color

    
    def disegnami(self, logica):
        self.opener.disegnami(logica)
        self.palette.disegnami(logica)
    

    def eventami(self, events, logica):
        self.opener.eventami(events, logica)
        self.palette.eventami(logica, events)

        if not self.palette.toggle:
            self.opener.bg = array(self.palette.colore_scelto) * self.palette.intensity
            self.picked_color = array(self.palette.colore_scelto) * self.palette.intensity

    
    def apri_picker(self):
        self.palette.toggle = False if self.palette.toggle else True

    
    def get_color(self):
        return self.picked_color



class Palette(BaseElement):
    def __init__(self, x=0, y=0, initial_color=[200, 200, 200]):
        super().__init__(x, y, 0, 0, False, "", 1, False)

        width = 20

        x_pos = (x - width / 2)
        if x_pos <= 0:
            x_pos = 0
        if x_pos >= (100 - width):
            x_pos = (100 - width)
        
        y_pos = (y - 20)
        if y_pos <= 0:
            y_pos = (y + 3)

        self.recalc_geometry("percentage", x_pos, y_pos, width, width)
        self.recalc_BB(-100, -100, 200, 200)

        self.colore_scelto = initial_color
        self.intensity = 1
        self.update_color_value = False

        self.toggle = False

        ###### generazione colori ###### 

        def generate_color_function(color):
            def return_selected_color():
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

        offset_palette_gradiente = 0.5

        larghezza_palette_gradiente = width * 0.72
        altezza_palette_gradiente = width * 0.85

        larghezza_chunck_palette = larghezza_palette_gradiente / 11
        altezza_chunck_palette = altezza_palette_gradiente / 11

        one_pixel_width = BaseElement.pixel2percentage(1, "x")
        one_pixel_height = BaseElement.pixel2percentage(1, "y")

        self.colori_bottoni = [Bottone_Push(x=offset_palette_gradiente + x_pos + (i % 11) * larghezza_chunck_palette, 
                                            y=offset_palette_gradiente + y_pos + (i // 11) * altezza_chunck_palette, 
                                            w=larghezza_chunck_palette + one_pixel_width, 
                                            h=altezza_chunck_palette + one_pixel_height, 
                                            function=foo) for i, foo in zip(range(len(color_functions)), color_functions)]
        
        for bottone, colore in zip(self.colori_bottoni, colori):
            bottone.original_color = array(colore)
            bottone.suppress_animation = True
            bottone.contorno = 0
            bottone.smussatura = 0

        ###### generazione intensità ###### 

        def generate_intens_function(intensity):
            def return_selected_intensity():
                self.intensity = intensity
                self.update_color_value = True
            return return_selected_intensity
        
        intensities = [0.0, 0.12, 0.24, 0.36, 0.48, 0.6, 0.76, 0.88, 1.0]
        intensities = intensities[::-1]

        intensities_functions = [generate_intens_function(intens) for intens in intensities]
        
        self.intens_bottoni = [Bottone_Push(x=offset_palette_gradiente + x_pos + width * 0.77, 
                                            y=offset_palette_gradiente + y_pos + (i % 11) * altezza_chunck_palette, 
                                            w=larghezza_chunck_palette, 
                                            h=altezza_chunck_palette + one_pixel_height, 
                                            function=foo) for i, foo in zip(range(len(color_functions)), intensities_functions)]

        for bottone, colore in zip(self.intens_bottoni, intensities):
            bottone.bg = array([colore, colore , colore]) * 255
            bottone.suppress_animation = True
            bottone.contorno = 0
            bottone.smussatura = 0

        ###### generazione preview ###### 
        self.preview_button = Bottone_Push(x=offset_palette_gradiente + x_pos + width * 0.875, 
                                           y=offset_palette_gradiente + y_pos, 
                                           w=larghezza_chunck_palette * 1.3, 
                                           h=altezza_chunck_palette * 9,
                                           disable=True)
        self.preview_button.contorno = 0

        ###### generazione entrate ###### 

        self.RGB_inputs = [Entrata(x=offset_palette_gradiente + x_pos + i * width / 4, 
                                   y=offset_palette_gradiente + y_pos + width * .8, 
                                   w=width / 6, 
                                   h=2, 
                                   text=f"{self.colore_scelto[i]}", 
                                   lunghezza_max=3, solo_numeri=True, num_valore_minimo=0, num_valore_massimo=255) for i in range(3)]
        
        for index, entrata in enumerate(self.RGB_inputs):
            entrata.bg = array([90, 90, 90])
            entrata.bg[index] = 180

        self.HEX_input = Entrata(x=offset_palette_gradiente + x_pos + 3 * width / 4, 
                                 y=offset_palette_gradiente + y_pos + width * .8, 
                                 w=width / 5, 
                                 h=2, 
                                 text=f"{MateUtils.rgb2hex(self.colore_scelto)}", 
                                 lunghezza_max=6, is_hex=True)
        self.HEX_input.bg = array([60, 60, 60])


    def disegnami(self, logica):

        if self.toggle:

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

        if not self.bounding_box.collidepoint(logica.mouse_pos): self.toggle = False
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.toggle = False
                        
        if self.toggle:
            if self.update_color_value:
                colore_nuovo = array(self.colore_scelto) * self.intensity
                self.RGB_inputs[0].testo = f"{int(colore_nuovo[0])}" 
                self.RGB_inputs[1].testo = f"{int(colore_nuovo[1])}" 
                self.RGB_inputs[2].testo = f"{int(colore_nuovo[2])}" 
                self.HEX_input.testo = f"{MateUtils.rgb2hex(colore_nuovo)}"
                self.update_color_value = False

            [bottone.eventami(events, logica) for bottone in self.colori_bottoni]
            [bottone.eventami(events, logica) for bottone in self.intens_bottoni]

            [entrata.eventami(events, logica) for entrata in self.RGB_inputs]
            for index, entrata in enumerate(self.RGB_inputs):
                if entrata.selezionato:
                    self.colore_scelto[index] = MateUtils.inp2int(entrata.testo)
                    self.intensity = 1
                    self.HEX_input.testo = MateUtils.rgb2hex([self.RGB_inputs[0].testo, self.RGB_inputs[1].testo, self.RGB_inputs[2].testo])


            self.HEX_input.eventami(events, logica)
            if self.HEX_input.selezionato:
                self.colore_scelto = array(MateUtils.hex2rgb(self.HEX_input.testo))
                self.intensity = 1
                
                for colore, entrata in zip(self.colore_scelto, self.RGB_inputs):
                    entrata.change_text(f"{colore}")


class SubStringa:
    def __init__(self, colore, bold, italic, apice, pedice, highlight, testo) -> None:
        
        self.colore: tuple[int] = colore
        
        self.bold: bool = bold
        self.italic: bool = italic
        self.apice: bool = apice
        self.pedice: bool = pedice
        self.highlight: bool = highlight
        
        self.testo: str = testo


    @property
    def end(self):
        lung = len(self.testo)
        if self.apice or self.pedice:
            lung *= 0.5
        return lung 


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

        formattatori=(r"\red{", r"\orange{", r"\yellow{", r"\green{", r"\lblue{", r"\blue{", r"\violet{", r"\high{", r"\^{", r"\_{", r"\bold{", r"\italic{")

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
                ris.testo = self.testo[formattatori_trovati[0][1] + len(formattatori_trovati[0][0]): formattatori_trovati[0][2]]
                
                match formattatori_trovati[0][0]:
                    case r"\red{": ris.colore = (255, 100, 100)
                    case r"\orange{": ris.colore = (255, 150, 100)
                    case r"\yellow{": ris.colore = (200, 200, 100)
                    case r"\green{": ris.colore = (100, 255, 100)
                    case r"\lblue{": ris.colore = (100, 255, 255)
                    case r"\blue{": ris.colore = (100, 100, 255)
                    case r"\violet{": ris.colore = (255, 100, 255)
                    case r"\high{": ris.highlight = True
                    case r"\^{": ris.apice = True
                    case r"\_{": ris.pedice = True
                    case r"\bold{": ris.bold = True
                    case r"\italic{": ris.italic = True

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
    def __init__(self, dim) -> None:
        
        self.original = int(dim)

        self.dim_font = self.original 
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
    
        path_r = os.path.join('TEXTURES', 'font_r.ttf')
        path_b = os.path.join('TEXTURES', 'font_b.ttf')
        path_i = os.path.join('TEXTURES', 'font_i.ttf')
        self.font_pyg_r = pygame.font.Font(path_r, round(self.dim_font))
        self.font_pyg_i = pygame.font.Font(path_i, round(self.dim_font))
        self.font_pyg_b = pygame.font.Font(path_b, round(self.dim_font))
        self.font_pixel_dim = self.font_pyg_r.size("a")



class DropMenu(BaseElement):
    def __init__(self, x=0, y=0, w=0, h=0):
        super().__init__(x, y, w, h, mantain_proportion=False, text="", scala=1, hide=False)

        self.w_working_area = BaseElement.percentage2pixel(w - 2, "x")
        self.h_working_area = BaseElement.percentage2pixel(h - 6.5, "y")

        self.x_anchor_working_area = BaseElement.percentage2pixel(x + 1, "x") + BaseElement.pappardella["offset"]
        self.y_anchor_working_area = BaseElement.percentage2pixel(y + 5.5, "y")
        
        self.h_chiuso = BaseElement.percentage2pixel(4.5, "y")

        self.contorno = 3
        self.smussatura = 5

        self.aperto = False

        def apertura_chiusura():
            self.aperto = False if self.aperto else True
            if self.aperto:
                self.bottone_apertura.change_text("v")
            else:
                self.bottone_apertura.change_text(">")
                
                
        font_dim = w / 3
        font_dim = min(font_dim, 3)

        w_apertura = w / 4
        w_apertura = min(w_apertura, 4.5)

        self.bottone_apertura = Bottone_Push(x, y, w_apertura, font_dim * 1.5, apertura_chiusura, text=">", scala=font_dim)
        self.titolo = Label_Text(x + w/3, y + font_dim * .75, "Titolo", font_dim / 2)

        self.elements = []

    
    def disegnami(self, logica: 'Logica'):

        if self.aperto:
            pygame.draw.rect(self.schermo, self.bg, [self.x, self.y, self.w, self.h], self.contorno, self.smussatura)

            # DEBUG VISUALIZE
            # pygame.draw.rect(self.schermo, [255, 0, 0], [self.x + self.convert_perc2pixel(1, "x"), self.y + self.convert_perc2pixel(5.5, "y"), self.w - self.convert_perc2pixel(2, "x"), self.h - self.convert_perc2pixel(6.5, "y")], self.contorno, self.smussatura)
            # pygame.draw.circle(self.schermo, [0, 255, 0], [self.x_anchor_working_area, self.y_anchor_working_area], 20)
            # pygame.draw.circle(self.schermo, [0, 0, 255], [self.x_anchor_working_area + self.w_working_area, self.y_anchor_working_area + self.h_working_area], 20)

        else:
            pygame.draw.rect(self.schermo, self.bg, [self.x, self.y, self.w, self.h_chiuso], self.contorno, self.smussatura)

        self.bottone_apertura.disegnami(logica)
        self.titolo.disegnami(logica, offset_x=len(self.titolo.testo) * self.titolo.font.font_pixel_dim[0] / 2, center=True)
        
        if self.aperto:
            [element.disegnami(logica) for element in self.elements]


    
    def eventami(self, events, logica: 'Logica'):
        self.bottone_apertura.eventami(events, logica)

        if self.aperto:
            [element.eventami(events, logica) for element in self.elements]
        

    def convert_perc2pixel(self, value, axis):
        
        match axis:
            case "x": return self.pappardella["moltiplicatore_x"] * value / 100
            case "y": return self.pappardella["ori_y"] * value / 100


    def add_element(self, element: Bottone_Push, mantain_prop=False):

        self.basis_change(element, mantain_prop=mantain_prop)
        self.elements.append(element)

    
    def basis_change(self, element: Bottone_Push, mantain_prop=False):

        if mantain_prop:
            larghezza = element.w / self.pappardella["moltiplicatore_x"]
            altezza = element.h / self.pappardella["moltiplicatore_x"]
            pos_x = (element.x - self.pappardella["offset"]) / self.pappardella["moltiplicatore_x"]
            pos_y = element.y / self.pappardella["moltiplicatore_x"]

            element.w = self.w_working_area * larghezza
            element.h = self.h_working_area * altezza
            element.x = pos_x * self.w_working_area + self.x_anchor_working_area
            element.y = pos_y * self.h_working_area + self.y_anchor_working_area
            
            element.bounding_box = pygame.Rect(element.x, element.y, element.w, element.h)

        else:
            larghezza = element.w / self.pappardella["moltiplicatore_x"]
            altezza = element.h / self.pappardella["ori_y"]
            pos_x = (element.x - self.pappardella["offset"]) / self.pappardella["moltiplicatore_x"]
            pos_y = element.y / self.pappardella["ori_y"]

            element.w = self.w_working_area * larghezza
            element.h = self.h_working_area * altezza
            element.x = pos_x * self.w_working_area + self.x_anchor_working_area
            element.y = pos_y * self.h_working_area + self.y_anchor_working_area
            
            element.bounding_box = pygame.Rect(element.x, element.y, element.w, element.h)