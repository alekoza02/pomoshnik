import pygame
from numpy import array
import pyperclip

NON_ESEGUIRE = False

if NON_ESEGUIRE:    
    from _modulo_costruttore_scene import Font
    from pygame.event import Event
    from _modulo_UI import Logica

from GRAFICA._modulo_database import Dizionario; diction = Dizionario()



class Label_Text:
    def __init__(self, x, y, text, scala, pappardella) -> None:
        
        self.schermo = pappardella["screen"]

        self.x: float = pappardella["moltiplicatore_x"] * x / 100 + pappardella["offset"]
        self.y: float = pappardella["ori_y"] * y / 100

        self.font: 'Font' = pappardella["font"]

        self.text_x: float = self.x
        self.text_y: float = self.y

        self.scala = scala

        self.testo: str = text
        self.color_text = (200, 200, 200)
    

    def disegnami(self, offset_x: int = 0, offset_y: int = 0, center=False):

        self.font.scala_font(self.scala)

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
                    self.schermo.blit(self.font.font_pyg_r.render("" + "█" * (len(substringa_analizzata.testo)) + "", True, [100, 100, 100]), (self.text_x + original_spacing_x * ( offset_highlight + offset_usato) + offset_x + centratura_x, self.text_y + offset_frase + offset_pedice_apice + offset_y + centratura_y))

                if substringa_analizzata.bold:
                    self.schermo.blit(self.font.font_pyg_b.render(substringa_analizzata.testo, True, substringa_analizzata.colore), (self.text_x + original_spacing_x * offset_usato + offset_x + centratura_x, self.text_y + offset_frase + offset_pedice_apice + offset_y + centratura_y))
                elif substringa_analizzata.italic:
                    self.schermo.blit(self.font.font_pyg_i.render(substringa_analizzata.testo, True, substringa_analizzata.colore), (self.text_x + original_spacing_x * offset_usato + offset_x + centratura_x, self.text_y + offset_frase + offset_pedice_apice + offset_y + centratura_y))
                else:
                    self.schermo.blit(self.font.font_pyg_r.render(substringa_analizzata.testo, True, substringa_analizzata.colore), (self.text_x + original_spacing_x * offset_usato + offset_x + centratura_x, self.text_y + offset_frase + offset_pedice_apice + offset_y + centratura_y))
                
                if substringa_analizzata.pedice or substringa_analizzata.apice:
                    self.font.scala_font(2)

                
                if substringa_analizzata.apice: offset_orizzontale_apice += substringa_analizzata.end
                elif substringa_analizzata.pedice: offset_orizzontale_pedice += substringa_analizzata.end
                else:
                    offset_orizzontale_apice += substringa_analizzata.end
                    offset_orizzontale_pedice += substringa_analizzata.end

                offset_orizzontale = max(offset_orizzontale_apice, offset_orizzontale_pedice)

                    
        self.font.scala_font(1 / self.scala)



class Bottone_Push(Label_Text):
    def __init__(self, x, y, w, h, function, text, scala, pappardella) -> None:
        super().__init__(x, y, text, scala, pappardella)

        self.bg = array(pappardella["bg_def"])
        
        self.contorno = 2

        self.w = pappardella["moltiplicatore_x"] * w / 100 + pappardella["offset"]
        self.h = pappardella["ori_y"] * h / 100

        self.callback = function

        self.animazione = Animazione(100, "once")
        self.hover = False

        self.bounding_box = pygame.Rect(self.x, self.y, self.w, self.h)

    
    def disegnami(self, logica: 'Logica'):

        colore = self.bg.copy()

        colore = self.animazione_press(logica.dt, colore)
        colore = self.animazione_hover(colore)

        pygame.draw.rect(self.schermo, colore, [self.x, self.y, self.w, self.h], self.contorno, 20)

        super().disegnami(self.w / 2, self.h / 2, center=True)

    
    def eventami(self, events: list['Event'], logica: 'Logica'):

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.bounding_box.collidepoint(event.pos):
                    self.callback(self)
                    self.animazione.riavvia()

        self.hover = True if self.bounding_box.collidepoint(logica.mouse_pos) else False
                    

    def animazione_press(self, dt: int, colore):
        
        if self.animazione.update(dt):

            self.contorno = 0
            colore += 20

        else: 
            self.contorno = 2
        
        return colore


    def animazione_hover(self, colore):
        if self.hover:
            self.contorno = 0
            colore += 10
        else:
            self.contorno = 2
        return colore



class Bottone_Toggle(Label_Text):
    def __init__(self, x, y, state, text, scala, pappardella) -> None:
        super().__init__(x, y, text, scala, pappardella)

        self.bg = array(pappardella["bg_def"])
        
        self.contorno = 2

        self.w = pappardella["moltiplicatore_x"] * 1 / 100 + pappardella["offset"]
        self.h = self.w

        self.state_toggle = state

        self.animazione = Animazione(-1, "once")
        self.hover = False

        self.bounding_box = pygame.Rect(self.x, self.y, self.w, self.h)


    def disegnami(self):
        
        colore = self.bg.copy()

        colore = self.animazione_press(colore)
        colore = self.animazione_hover(colore)

        pygame.draw.rect(self.schermo, colore, [self.x, self.y, self.w, self.h], self.contorno, 5)

        if self.state_toggle:
            pygame.draw.rect(self.schermo, [80, 170, 80], [self.x + 4, self.y + 4, self.w - 8, self.h - 8], self.contorno, 5)


        super().disegnami(self.font.font_pixel_dim[0] * 3, 0, center=False)
    

    def eventami(self, events: list['Event'], logica: 'Logica'):

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



class Entrata(Label_Text):
    def __init__(self, x, y, w, h, text, scala, pappardella) -> None:
        super().__init__(x, y, text, scala, pappardella)

        self.bg = array(pappardella["bg_def"])
        
        self.contorno = 2

        self.w = pappardella["moltiplicatore_x"] * w / 100 + pappardella["offset"]
        self.h = pappardella["ori_y"] * h / 100

        self.testo = text
        self.offset_grafico_testo = 5
        self.puntatore_pos = 0
        self.selected: list[int] = [0, 0]

        self.selezionato = False
        self.hover = False

        self.animazione_puntatore = Animazione(1000, "loop")
        self.animazione_puntatore.attiva = True

        self.bounding_box = pygame.Rect(self.x, self.y, self.w, self.h)
        

    def disegnami(self, logica: 'Logica'):

        colore = self.bg.copy()

        colore = self.animazione_press(colore)
        colore = self.animazione_hover(colore)

        pygame.draw.rect(self.schermo, colore, [self.x, self.y, self.w, self.h], self.contorno, 5)
        
        self.font.scala_font(self.scala)


        if self.selezionato:
            pygame.draw.rect(self.schermo, [20, 100, 100], [self.x + self.font.font_pixel_dim[0] * self.selected[0] + self.offset_grafico_testo, self.y, self.font.font_pixel_dim[0] * (self.selected[1] - self.selected[0]), self.h], 0, 5)

        # testo
        self.schermo.blit(self.font.font_pyg_r.render(self.testo, True, self.color_text), (self.text_x + self.offset_grafico_testo, self.text_y + self.h / 2 - self.font.font_pixel_dim[1] / 2))

        # puntatore flickerio
        self.animazione_puntatore.update(logica.dt)
        if self.selezionato and self.animazione_puntatore.dt < 500:
            offset_puntatore_pos = self.font.font_pixel_dim[0] * self.puntatore_pos
            pygame.draw.rect(self.schermo, [200, 200, 200], [self.x + self.offset_grafico_testo + offset_puntatore_pos, self.y, 2, self.h], 0)
    
        self.font.scala_font(1 / self.scala)


    def eventami(self, events: list['Event'], logica: 'Logica'):
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.bounding_box.collidepoint(event.pos):
                        
                        if self.selezionato:
                            self.selected = [0, 0]
                            self.update_puntatore_pos(event.pos)
                        else:    
                            self.selezionato = True
                            self.selected = [len(self.testo), 0]
                            self.puntatore_pos = len(self.testo)

                        self.animazione_puntatore.riavvia()

                    else:
                        self.selezionato = False
                        self.selected = [0, 0]
                        

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.bounding_box.collidepoint(event.pos):
                        if self.selezionato:
                            self.animazione_puntatore.riavvia()
                        

            # selected
            if logica.dragging and self.selezionato:

                self.selected[0] = self.get_puntatore_pos(logica.mouse_pos[0])
                self.selected[1] = self.get_puntatore_pos(logica.original_start_pos[0])
                self.update_puntatore_pos(logica.mouse_pos)
                self.animazione_puntatore.riavvia()

        self.hover = True if self.bounding_box.collidepoint(logica.mouse_pos) else False



    def eventami_scrittura(self, events: list['Event'], logica: 'Logica'):
        
        def move_selected(dir: bool, amount: int = 1):
            if dir:
                if self.selected == [0, 0]:
                    self.selected = [self.puntatore_pos, self.puntatore_pos]

                if self.selected[0] < len(self.testo):
                    self.selected[0] += amount
            
            else:
                if self.selected == [0, 0]:
                    self.selected = [self.puntatore_pos, self.puntatore_pos]

                if self.selected[0] > 0:
                    self.selected[0] -= amount


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
        for event in events:
            
            if event.type == pygame.TEXTINPUT:         
                
                apertura = ""
                chiusura = ""

                if event.text == '{' or event.text == "[" or event.text == "(":
                    apertura = event.text
                    match event.text:
                        case "{": chiusura = "}"
                        case "[": chiusura = "]"
                        case "(": chiusura = ")"



                if self.selected != [0, 0]:

                    min_s = min(self.selected[0], self.selected[1])
                    max_s = max(self.selected[0], self.selected[1])
                    
                    if apertura != "":
                        self.testo = self.testo[:min_s] + apertura + self.testo[min_s : max_s] + chiusura + self.testo[max_s:]
                        self.selected[0] += 1
                        self.selected[1] += 1
                        self.puntatore_pos += 1

                    else:
    
                        self.testo = self.testo[:min_s] + event.text + self.testo[max_s:]
                        self.puntatore_pos = len(self.testo[:min_s]) + len(event.text)
                        self.selected = [0, 0]

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
                    
                    min_s = min(self.selected[0], self.selected[1])
                    max_s = max(self.selected[0], self.selected[1])

                    pyperclip.copy(self.testo[min_s : max_s])
                
                    self.selected = [0, 0]

                if logica.ctrl and event.key == pygame.K_v:
                    
                    incolla = pyperclip.paste()
                    self.testo = f"{self.testo[:self.puntatore_pos]}{incolla}{self.testo[self.puntatore_pos:]}"
                    self.puntatore_pos = len(self.testo[:self.puntatore_pos]) + len(incolla)

                    self.selected = [0, 0]
                
                if logica.ctrl and event.key == pygame.K_x:
                    
                    if self.selected != [0, 0]:
                        min_s = min(self.selected[0], self.selected[1])
                        max_s = max(self.selected[0], self.selected[1])

                        pyperclip.copy(self.testo[min_s : max_s])
                    
                        self.selected = [0, 0]
                        
                        self.testo = self.testo[:min_s] + self.testo[max_s:]
                        self.puntatore_pos = len(self.testo[:min_s])
 

                # HOME and END
                if event.key == pygame.K_HOME:
                    self.puntatore_pos = 0
                    reset_animation = True
                    if logica.shift:
                        self.selected = [self.puntatore_pos, 0]
                    else:
                        self.selected = [0, 0]

                

                if event.key == pygame.K_END:
                    self.puntatore_pos = len(self.testo)
                    reset_animation = True
                    if logica.shift:
                        self.selected = [self.puntatore_pos, len(self.testo)]
                    else:
                        self.selected = [0, 0]


                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    reset_animation = True

                    if self.selected[1] - self.selected[0] != 0:

                        min_s = min(self.selected[0], self.selected[1])
                        max_s = max(self.selected[0], self.selected[1])

                        self.testo = self.testo[:min_s] + self.testo[max_s:]

                        self.puntatore_pos = min_s
                        self.selected = [0, 0]

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
                                self.selected = [0, 0]

                            self.puntatore_pos = puntatore_left

                        else: 

                            self.puntatore_pos -= 1

                            if logica.shift:

                                move_selected(0)
            
                            else:
                                reset_animation = True
                                self.selected = [0, 0]


                if event.key == pygame.K_RIGHT:

                    if self.puntatore_pos < len(self.testo):
                        
                        if logica.ctrl:
                            
                            puntatore_right = find_ricercatore(self, 1)
                            
                            if logica.shift:

                                move_selected(1, puntatore_right - self.puntatore_pos)
            
                            else:
                                reset_animation = True
                                self.selected = [0, 0]

                            self.puntatore_pos = puntatore_right

                        else: 

                            self.puntatore_pos += 1

                            if logica.shift:

                                move_selected(1)
            
                            else:
                                reset_animation = True
                                self.selected = [0, 0]


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