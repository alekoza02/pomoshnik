import pygame
from numpy import array

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

        self.text: str = text
        self.color_text = (200, 200, 200)
    

    def disegnami(self, offset_x: int = 0, offset_y: int = 0, center=False):

        self.font.scala_font(self.scala)

        # sostituzione caratteri speciali
        testo_analisi = SubStringa.analisi_caratteri_speciali(self.text)

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
                centratura_y = 0
        
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
                    self.schermo.blit(self.font.font_pyg_r.render("" + "█" * (len(substringa_analizzata.testo)) + "", True, self.color_bg), (self.text_x + original_spacing_x * ( offset_highlight + offset_usato) + offset_x + centratura_x, self.text_y - original_spacing_y // 2 + offset_frase + offset_pedice_apice + offset_y + centratura_y))

                if substringa_analizzata.bold:
                    self.schermo.blit(self.font.font_pyg_b.render(substringa_analizzata.testo, True, substringa_analizzata.colore), (self.text_x + original_spacing_x * offset_usato + offset_x + centratura_x, self.text_y - original_spacing_y // 2 + offset_frase + offset_pedice_apice + offset_y + centratura_y))
                elif substringa_analizzata.italic:
                    self.schermo.blit(self.font.font_pyg_i.render(substringa_analizzata.testo, True, substringa_analizzata.colore), (self.text_x + original_spacing_x * offset_usato + offset_x + centratura_x, self.text_y - original_spacing_y // 2 + offset_frase + offset_pedice_apice + offset_y + centratura_y))
                else:
                    self.schermo.blit(self.font.font_pyg_r.render(substringa_analizzata.testo, True, substringa_analizzata.colore), (self.text_x + original_spacing_x * offset_usato + offset_x + centratura_x, self.text_y - original_spacing_y // 2 + offset_frase + offset_pedice_apice + offset_y + centratura_y))
                
                if substringa_analizzata.pedice or substringa_analizzata.apice:
                    self.font.scala_font(2)

                
                if substringa_analizzata.apice: offset_orizzontale_apice += substringa_analizzata.end
                elif substringa_analizzata.pedice: offset_orizzontale_pedice += substringa_analizzata.end
                else:
                    offset_orizzontale_apice += substringa_analizzata.end
                    offset_orizzontale_pedice += substringa_analizzata.end

                offset_orizzontale = max(offset_orizzontale_apice, offset_orizzontale_pedice)

                    
        self.font.scala_font(1 / self.scala)



class Bottone(Label_Text):
    def __init__(self, x, y, w, h, function, text, scala, pappardella) -> None:
        super().__init__(x, y, text, scala, pappardella)

        self.bg = array(pappardella["bg_def"])
        
        self.contorno = 2

        self.w = pappardella["moltiplicatore_x"] * w / 100 + pappardella["offset"]
        self.h = pappardella["ori_y"] * h / 100

        self.callback = function

        self.animazione = Animazione(100)
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
        if self.animazione.attiva and self.animazione.dt < self.animazione.durata:
            
            self.contorno = 0
            colore += 20
            self.animazione.dt += dt

            if self.animazione.dt > self.animazione.durata:
                self.animazione.attiva = False
                self.animazione.dt = 0

        else: 
            self.contorno = 2
        
        return colore


    def animazione_hover(self, colore):
        if self.hover:
            self.contorno = 0
            colore += 10
        else:
            self.contorno = 1
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

        formattatori=("/red{", "/orange{", "/yellow{", "/green{", "/lblue{", "/blue{", "/violet{", "/high{", "/^{", "/_{", "/bold{", "/italic{")

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
                    case "/red{": ris.colore = (255, 100, 100)
                    case "/orange{": ris.colore = (255, 150, 100)
                    case "/yellow{": ris.colore = (200, 200, 100)
                    case "/green{": ris.colore = (100, 255, 100)
                    case "/lblue{": ris.colore = (100, 255, 255)
                    case "/blue{": ris.colore = (100, 100, 255)
                    case "/violet{": ris.colore = (255, 100, 255)
                    case "/high{": ris.highlight = True
                    case "/^{": ris.apice = True
                    case "/_{": ris.pedice = True
                    case "/bold{": ris.bold = True
                    case "/italic{": ris.italic = True

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
    def __init__(self, durata) -> None:
        self.attiva = False
        self.durata = durata
        self.dt = 0

    def riavvia(self):
        self.attiva = True
        self.dt = 0