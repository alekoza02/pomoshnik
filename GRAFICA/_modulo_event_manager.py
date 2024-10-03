import pygame
import time

NON_ESEGUIRE = False

if NON_ESEGUIRE:    
    from GRAFICA._modulo_UI import Logica
    from GRAFICA._modulo_costruttore_scene import Scena



class EventManager:

    def __init__(self) -> None:
        self.entrata_attiva = None
        self.elapsed_dragging = 0


    def event_manage_ui(self, eventi: pygame.event, scena: 'Scena', logica: 'Logica'):

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
                    
                    if time.perf_counter() - logica.elapsed_waiting_click_sinistro >= 0.2:
                        logica.wait_for_doppio_click = True

                    if logica.wait_for_doppio_click:
                        logica.wait_for_doppio_click = False
                        logica.elapsed_waiting_click_sinistro = time.perf_counter()
                    else:
                        logica.wait_for_doppio_click = True
                        logica.elapsed_waiting_click_sinistro = time.perf_counter() - logica.elapsed_waiting_click_sinistro

                    if logica.elapsed_waiting_click_sinistro > 0 and logica.elapsed_waiting_click_sinistro < 0.2:
                        logica.doppio_click_sinistro = True
                        logica.mouse_pos_doppio_click = pygame.mouse.get_pos()
                    else:
                        logica.doppio_click_sinistro = False
                        
                    logica.init_dragging = True
                    logica.original_start_pos = logica.mouse_pos
                    logica.dragging_end_pos = logica.mouse_pos

                if event.button == 3:
                    logica.click_destro = True
                
                if event.button == 4:
                    logica.scroll_up += 1
                if event.button == 5:
                    logica.scroll_down += 1

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: 
                    self.elapsed_dragging = 0
                    logica.dragging = False
                    logica.init_dragging = False
                    logica.dragging_end_pos = logica.mouse_pos

            if event.type == pygame.MOUSEMOTION:
                
                if logica.init_dragging:
                    self.elapsed_dragging += logica.dt
                    
                    if self.elapsed_dragging > 100:
                    
                        logica.dragging = True
                        logica.dragging_start_pos = logica.dragging_end_pos
                        logica.dragging_end_pos = logica.mouse_pos
                        logica.dragging_dx = logica.dragging_end_pos[0] - logica.dragging_start_pos[0]
                        logica.dragging_dy = - logica.dragging_end_pos[1] + logica.dragging_start_pos[1] # sistema di riferimento invertito


        # ENTRATE DI ENTRATE
        # raccolta di tutti i testi già presenti nelle entrate
        test_entr_attiva: list[str] = [indice for indice, elemento in scena.entrate.items() if elemento.selezionato]

        # logica per cui se ci sono entrate nella scena -> aggiorna il testo, indice e il testo generico modificabile
        if len(test_entr_attiva) > 0:
            self.entrata_attiva = scena.entrate[test_entr_attiva[0]]
            # gestione eventi entrata attiva
            self.entrata_attiva.eventami_scrittura(eventi, logica)
            
        # gestione eventi di tutte le UI
        scena.gestisci_eventi(eventi, logica)