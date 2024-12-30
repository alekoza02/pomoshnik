import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import ctypes
import psutil
import configparser
import os

from time import strftime

from GRAFICA._modulo_event_manager import EventManager
from GRAFICA._modulo_costruttore_scene import Costruttore


class Logica:
    def __init__(self) -> None:
        '''
        Inizializzazione di variabili che mi danno infomrazioni sull'UI / comandi da eseguire
        '''
        self.dragging = False
        self.init_dragging = False
        self.original_start_pos = (0,0)
        self.dragging_start_pos = (0,0)
        self.dragging_end_pos = (0,0)
        self.dragging_dx = 0
        self.dragging_dy = 0
        self.dragging_finished_FLAG = False
        self.mouse_pos = (0,0)

        self.skip_salto = False
        self.dt = 0
        self.trascorso = 0
        self.scena = 0
        
        self.click_sinistro = False
        
        self.doppio_click_sinistro = False
        self.elapsed_waiting_click_sinistro = 0
        self.wait_for_doppio_click = True
        self.mouse_pos_doppio_click = (0, 0)

        self.click_destro = False
        
        self.ctrl = False
        self.shift = False
        self.backspace = False
        self.left = False
        self.right = False
        self.tab = False

        self.acc_backspace = 0
        self.acc_left = 0
        self.acc_right = 0
        
        self.scroll_up = 0
        self.scroll_down = 0

        self.dropped_paths = []



class UI:
    
    def __init__(self) -> None:
        '''
        Inizializzazione applicazione
        '''

        pygame.init()
        self.init_screen_data()

        # custom mouse
        # pygame.mouse.set_visible(False)
        # path = os.path.join('TEXTURES', 'mouse.png') 
        # self.custom_mouse_icon = pygame.image.load(path)

        self.BG: tuple[int] = (30, 30, 30)

        self.fullscreen = False
        
        self.clock = pygame.time.Clock()
        self.max_fps: int = 0
        self.current_fps: int = 0
        self.running: int = 1

        self.logica = Logica()
        self.event_manager = EventManager()
        self.costruttore = Costruttore(self.MAIN, self.w_screen * 0.9, self.h_screen * 0.9, self.h_screen / 75)
        self.costruttore.scene["main"].disegna_scena_inizio_ciclo(self.logica)
        self.costruttore.scene["main"].disegna_scena_fine_ciclo(self.logica)

        self.cpu_sample: list[int] = [0 for i in range(100)]

    
    def go_fullscreen(self):
        self.MAIN = pygame.display.set_mode((self.w_screen, self.h_screen), pygame.FULLSCREEN)
        self.fullscreen = True


    def exit_fullscreen(self):
        self.MAIN = pygame.display.set_mode((self.w_screen * 0.9, self.h_screen * 0.9), pygame.RESIZABLE)
        self.fullscreen = False

    
    def init_screen_data(self):
        
        # DPI aware
        ctypes.windll.user32.SetProcessDPIAware()
        screen_info = pygame.display.Info()
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

        # impostazione dimensione schermi e rapporti
        self.w_screen: int = int(screen_info.current_w * scale_factor)
        self.h_screen: int = int(screen_info.current_h * scale_factor)

        self.w, self.h = self.w_screen * 0.9, self.h_screen * 0.9

        # generazione finestra
        self.MAIN = pygame.display.set_mode((self.w_screen * 0.9, self.h_screen * 0.9), pygame.RESIZABLE)


    def update_screen_data(self):
        old_w, old_h = self.w, self.h
        self.w, self.h = self.MAIN.get_size()
        return (old_w == self.w and old_h == self.h)


    def colora_bg(self) -> None:
        '''
        Colora la finestra con il colore dello sfondo (self.BG)
        '''
        self.MAIN.fill((30, 30, 30))


        # for i in range(10):
        #     pygame.draw.line(self.costruttore.screen, [60, 255, 60], [i*self.w/10, 0], [i*self.w/10, self.h], 1)
        #     pygame.draw.line(self.costruttore.screen, [60, 60, 255], [0, i*self.h/10], [self.w, i*self.h/10], 1)
        #     pygame.draw.line(self.costruttore.screen, [60, 255, 60], [0, i*self.w/10], [self.w, i*self.w/10], 1)

        # pygame.draw.line(self.costruttore.screen, [255, 0, 0], [self.w/2, 0], [self.w/2, self.h], 1)
        # pygame.draw.line(self.costruttore.screen, [255, 0, 0], [0, self.h/2], [self.w, self.h/2], 1)
        

    def mouse_icon(self) -> None:
        '''
        Ottiene la posizione del mouse attuale e ci disegna sopra l'icona custom 
        Assicurarsi che in UI ci sia pygame.mouse.set_visible(False)
        '''
        mouse = self.logica.mouse_pos
        self.MAIN.blit(self.custom_mouse_icon, mouse)


    def start_cycle(self):
        # impostazione inizio giro
        self.logica.dt = self.clock.tick(self.max_fps)
        self.logica.trascorso += 1
        self.colora_bg()

        self.logica.dragging_dx = 0
        self.logica.dragging_dy = 0

        if self.logica.scroll_up > 0: self.logica.scroll_up -= (1 + self.logica.scroll_up / 3)
        else: self.logica.scroll_up = 0

        if self.logica.scroll_down > 0: self.logica.scroll_down -= (1 + self.logica.scroll_down / 3)
        else: self.logica.scroll_down = 0

        self.logica.mouse_pos = pygame.mouse.get_pos()

        eventi = pygame.event.get()

        for event in eventi:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    if self.fullscreen:
                        self.exit_fullscreen()
                    else: 
                        self.go_fullscreen()

        if not self.update_screen_data():
            self.costruttore.recalc(self.w, self.h)

        self.event_manager.event_manage_ui(eventi, self.costruttore.scene["main"], self.logica)
        self.costruttore.scene["main"].disegna_scena_inizio_ciclo(self.logica)
        


    def end_cycle(self) -> None:
        '''
        Controlla se la combinazione di uscita è stata selezionata -> Uscita
        Altrimenti aggiornamento pagina
        '''

        # self.mouse_icon()

        self.costruttore.scene["main"].disegna_scena_fine_ciclo(self.logica)

        # aggiornamento
        self.current_fps = self.clock.get_fps()

        # PC status
        self.pc_attributes()

        # uscita
        keys = pygame.key.get_pressed()
        key_combo = [pygame.K_ESCAPE, pygame.K_SPACE]
        if all(keys[key] for key in key_combo):
            self.running = 0
            self.clear_cache()
        
        
        pygame.display.flip()


    def clear_cache(self):
        try:
            for filename in os.listdir("TEXTURES"):
                # Construct the full path to the file
                filepath = os.path.join("TEXTURES", filename)

                # Check if it's a file and contains the name
                if os.path.isfile(filepath) and "molecola" in filename:
                    os.remove(filepath)
        except Exception as e:
            print(f"An error occurred: {e}")


    def pc_attributes(self):
        
        self.costruttore.scene["main"].context_menu["main"].elements["memory"].change_text(r"\h{ " + f' Memory: {psutil.Process().memory_info().rss / 1024**2:>7.2f} MB' + " }")
        
        if psutil.Process().memory_info().rss / 1024**2 > 4000:
            self.costruttore.scene["main"].context_menu["main"].elements["memory"].change_text(r"\#dc143c{" + self.costruttore.scene["main"].context_menu["main"].elements["memory"].testo + "}")

        # -----------------------------------------------------------------------------

        self.cpu_sample.pop(0)
        self.cpu_sample.append(psutil.cpu_percent(interval=0))
        self.costruttore.scene["main"].context_menu["main"].elements["cpu"].change_text(r"\h{ " + f" CPU: {sum(self.cpu_sample) / len(self.cpu_sample):>3.0f}%" + " }")

        if sum(self.cpu_sample) / len(self.cpu_sample) > 30 and sum(self.cpu_sample) / len(self.cpu_sample) <= 70:
            self.costruttore.scene["main"].context_menu["main"].elements["cpu"].change_text(r"\#ffdd60{" + self.costruttore.scene["main"].context_menu["main"].elements["cpu"].testo + "}")

        if sum(self.cpu_sample) / len(self.cpu_sample) > 70:
            self.costruttore.scene["main"].context_menu["main"].elements["cpu"].change_text(r"\#dc143c{" + self.costruttore.scene["main"].context_menu["main"].elements["cpu"].testo + "}")

        # -----------------------------------------------------------------------------
        
        self.costruttore.scene["main"].context_menu["main"].elements["fps"].change_text(r"\h{ " + f"FPS: {self.current_fps:>6.2f}" + " }")
        
        if self.current_fps < 60 and self.current_fps >= 24:
            self.costruttore.scene["main"].context_menu["main"].elements["fps"].change_text(r"\#ffdd60{" + self.costruttore.scene["main"].context_menu["main"].elements["fps"].testo + "}")

        if self.current_fps < 24:
            self.costruttore.scene["main"].context_menu["main"].elements["fps"].change_text(r"\#dc143c{" + self.costruttore.scene["main"].context_menu["main"].elements["fps"].testo + "}")
        
        # -----------------------------------------------------------------------------
        
        self.costruttore.scene["main"].context_menu["main"].elements["clock"].change_text(r"\h{ " + f" {strftime("%X, %x")}" " }")

        # -----------------------------------------------------------------------------

        battery = psutil.sensors_battery()

        if battery:
            
            simbolo_corretto = ""
            caso_simbolo = battery.percent // 10
            
            match caso_simbolo:
                case 0: simbolo_corretto = "󰢟" if battery.power_plugged else "󰂎";   # 0%
                case 1: simbolo_corretto = "󰢜" if battery.power_plugged else "󰁺";   # 10%
                case 2: simbolo_corretto = "󰂆" if battery.power_plugged else "󰁻";   # 20%
                case 3: simbolo_corretto = "󰂇" if battery.power_plugged else "󰁼";   # 30%
                case 4: simbolo_corretto = "󰂈" if battery.power_plugged else "󰁽";   # 40%
                case 5: simbolo_corretto = "󰢝" if battery.power_plugged else "󰁾";   # 50%
                case 6: simbolo_corretto = "󰂉" if battery.power_plugged else "󰁿";   # 60%
                case 7: simbolo_corretto = "󰢞" if battery.power_plugged else "󰂀";   # 70%
                case 8: simbolo_corretto = "󰂊" if battery.power_plugged else "󰂁";   # 80%
                case 9: simbolo_corretto = "󰂋" if battery.power_plugged else "󰂂";   # 90%
                case 10: simbolo_corretto = "󰂅" if battery.power_plugged else "󰁹";  # 100%


            self.costruttore.scene["main"].context_menu["main"].elements["battery"].change_text(r"\h{ " + f"{simbolo_corretto} {battery.percent:>3}%" + " }")

            if battery.percent < 20 and battery.percent >= 10:
                self.costruttore.scene["main"].context_menu["main"].elements["battery"].change_text(r"\#ffdd60{" + self.costruttore.scene["main"].context_menu["main"].elements["battery"].testo + "}")

            if battery.percent < 10:
                self.costruttore.scene["main"].context_menu["main"].elements["battery"].change_text(r"\#dc143c{" + self.costruttore.scene["main"].context_menu["main"].elements["battery"].testo + "}")


    @staticmethod
    def graceful_quit():
        pygame.quit()
