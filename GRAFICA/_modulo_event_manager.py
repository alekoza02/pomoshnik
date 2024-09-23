import pygame

NON_ESEGUIRE = False

if NON_ESEGUIRE:    
    from _modulo_UI import Logica



class EventManager:

    def __init__(self) -> None:
        self.entrata_attiva = None


    def event_manage_ui(self, eventi: pygame.event, logica: 'Logica'):

        # Stato di tutti i tasti
        keys = pygame.key.get_pressed()

        # CONTROLLO CARATTERI SPECIALI
        logica.ctrl = keys[pygame.K_LCTRL]
        logica.shift = keys[pygame.K_LSHIFT]
        logica.backspace = keys[pygame.K_BACKSPACE]
        logica.left = keys[pygame.K_LEFT]
        logica.right = keys[pygame.K_RIGHT]
        logica.tab = keys[pygame.K_TAB]


        # reset variabili
        logica.click_sinistro = False
        logica.click_destro = False

        # scena main UI
        for event in eventi:

            # MOUSE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    logica.click_sinistro = True

                if event.button == 3:

                    logica.click_destro = True
                    logica.dragging = True
                    logica.original_start_pos = logica.mouse_pos
                    logica.dragging_end_pos = logica.mouse_pos
                
                if event.button == 4:
                    logica.scroll_up += 1
                if event.button == 5:
                    logica.scroll_down += 1

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3: 
                    logica.dragging = False
                    logica.dragging_end_pos = logica.mouse_pos

            if event.type == pygame.MOUSEMOTION:
                if logica.dragging:
                    logica.dragging_start_pos = logica.dragging_end_pos
                    logica.dragging_end_pos = logica.mouse_pos
                    logica.dragging_dx = logica.dragging_end_pos[0] - logica.dragging_start_pos[0]
                    logica.dragging_dy = - logica.dragging_end_pos[1] + logica.dragging_start_pos[1] # sistema di riferimento invertito

            
            # input -> tastiera con caratteri e backspace
            if self.entrata_attiva != None:

                if " " in self.entrata_attiva.text: ricercatore = " " 
                elif "\\" in self.entrata_attiva.text: ricercatore = "\\"
                elif "/" in self.entrata_attiva.text: ricercatore = "/"
                else: ricercatore = None

                if event.type == pygame.TEXTINPUT:           
                    self.entrata_attiva.text = self.entrata_attiva.text[:self.entrata_attiva.puntatore] + event.text + self.entrata_attiva.text[self.entrata_attiva.puntatore:]
                    self.entrata_attiva.puntatore += len(event.text)
                    self.entrata_attiva.dt_animazione = 0

                if event.type == pygame.KEYDOWN:
                    
                    tx = self.entrata_attiva.text
                            
                    if event.key == pygame.K_BACKSPACE:
                        if logica.ctrl:
                            if ricercatore is None:
                                self.entrata_attiva.puntatore = 0
                                self.entrata_attiva.text = "" 
                            else:
                                nuovo_puntatore = tx[:self.entrata_attiva.puntatore].rstrip().rfind(ricercatore)+1
                                text2eli = tx[nuovo_puntatore : self.entrata_attiva.puntatore]
                                self.entrata_attiva.puntatore = nuovo_puntatore
                                self.entrata_attiva.text = tx.replace(text2eli, "") 

                        else:
                            if self.entrata_attiva.puntatore != 0:
                                self.entrata_attiva.text = self.entrata_attiva.text[:self.entrata_attiva.puntatore-1] + self.entrata_attiva.text[self.entrata_attiva.puntatore:]
                            if self.entrata_attiva.puntatore > 0:
                                self.entrata_attiva.puntatore -= 1

                    if event.key == pygame.K_LEFT:
                        if self.entrata_attiva.puntatore > 0:
                            if logica.ctrl:
                                if ricercatore is None:
                                    self.entrata_attiva.puntatore = 0
                                else:
                                    self.entrata_attiva.puntatore = tx[:self.entrata_attiva.puntatore].rstrip().rfind(ricercatore)+1
                            else: 
                                self.entrata_attiva.puntatore -= 1

                    if event.key == pygame.K_RIGHT:
                        if self.entrata_attiva.puntatore < len(self.entrata_attiva.text):
                            if logica.ctrl:

                                if ricercatore is None:
                                    self.entrata_attiva.puntatore = len(self.entrata_attiva.text)
                                else:

                                    # trovo l'indice di dove inizia la frase
                                    start = tx.find(tx[self.entrata_attiva.puntatore:].lstrip(), self.entrata_attiva.puntatore, len(tx))
                                    # se non la trovo mi blocco dove sono partito
                                    if start == -1: start = self.entrata_attiva.puntatore

                                    # se la trovo, cerco la parola successiva
                                    found = tx.find(ricercatore, start, len(tx))
                                    # se non la trovo guardo mi posizione nell'ultimo carattere diverso da uno spazio
                                    if found == -1: found = len(tx.rstrip())

                                    self.entrata_attiva.puntatore = found
                                    
                            else:
                                self.entrata_attiva.puntatore += 1

                    self.entrata_attiva.dt_animazione = 0 

        if logica.backspace:
            logica.acc_backspace += 1
            if logica.acc_backspace > 20:
                if self.entrata_attiva.puntatore != 0:
                    self.entrata_attiva.text = self.entrata_attiva.text[:self.entrata_attiva.puntatore-1] + self.entrata_attiva.text[self.entrata_attiva.puntatore:]
                if self.entrata_attiva.puntatore > 0:
                    self.entrata_attiva.puntatore -= 1
        else: 
            logica.acc_backspace = 0

        if logica.left:
            logica.acc_left += 1
            if logica.acc_left > 20:
                if logica.ctrl:
                    self.entrata_attiva.puntatore = self.entrata_attiva.text[:self.entrata_attiva.puntatore].rstrip().rfind(ricercatore)+1
                elif self.entrata_attiva.puntatore > 0: self.entrata_attiva.puntatore -= 1
                self.entrata_attiva.dt_animazione = 0 
        else: 
            logica.acc_left = 0
        
        if logica.right:
            logica.acc_right += 1
            if logica.acc_right > 20:
                if logica.ctrl:
                    tx = self.entrata_attiva.text
                    # trovo l'indice di dove inizia la frase
                    start = tx.find(tx[self.entrata_attiva.puntatore:].lstrip(), self.entrata_attiva.puntatore, len(tx))
                    # se non la trovo mi blocco dove sono partito
                    if start == -1: start = self.entrata_attiva.puntatore

                    # se la trovo, cerco la parola successiva
                    found = tx.find(ricercatore, start, len(tx))
                    # se non la trovo guardo mi posizione nell'ultimo carattere diverso da uno spazio
                    if found == -1: found = len(tx.rstrip())

                    self.entrata_attiva.puntatore = found
                        
                elif self.entrata_attiva.puntatore < len(self.entrata_attiva.text): self.entrata_attiva.puntatore += 1
                self.entrata_attiva.dt_animazione = 0 
        else: 
            logica.acc_right = 0