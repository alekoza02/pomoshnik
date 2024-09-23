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
        self.original_start_pos = (0,0)
        self.dragging_start_pos = (0,0)
        self.dragging_end_pos = (0,0)
        self.dragging_dx = 0
        self.dragging_dy = 0
        self.mouse_pos = (0,0)

        self.skip_salto = False
        self.dt = 0
        self.trascorso = 0
        self.scena = 0
        
        self.click_sinistro = False
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



class UI:
    
    def __init__(self) -> None:
        '''
        Inizializzazione applicazione
        '''

        # DPI aware
        pygame.init()
        ctypes.windll.user32.SetProcessDPIAware()
        screen_info = pygame.display.Info()
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

        # custom mouse
        pygame.mouse.set_visible(False)
        path = os.path.join('TEXTURES', 'mouse.png') 
        self.custom_mouse_icon = pygame.image.load(path)

        # impostazione dimensione schermi e rapporti
        self.w: int = int(screen_info.current_w * scale_factor)
        self.h: int = int(screen_info.current_h * scale_factor)

        self.aspect_ratio_nativo: float = 2880 / 1800
        self.moltiplicatore_x: float = self.h * self.aspect_ratio_nativo
        self.rapporto_ori_x: float = self.w / 2880
        self.rapporto_ori_y: float = self.h / 1800
        self.shift_ori: float = (self.w - self.moltiplicatore_x) / 2

        # generazione finestra
        self.MAIN = pygame.display.set_mode((self.w, self.h))
        self.BG: tuple[int] = (30, 30, 30)
        
        self.clock = pygame.time.Clock()
        self.max_fps: int = 0
        self.current_fps: int = 0
        self.running: int = 1

        self.logica = Logica()
        self.event_manager = EventManager()
        self.costruttore = Costruttore(self.MAIN, self.shift_ori, self.moltiplicatore_x, self.rapporto_ori_x, self.rapporto_ori_y)

        self.cpu_sample: list[int] = [0 for i in range(100)]

        
    def colora_bg(self) -> None:
        '''
        Colora la finestra con il colore dello sfondo (self.BG)
        Inoltre disegna uno sfondo di colore (25, 25, 25) per gli aspect ratio diversi da 2880 x 1800
        '''
        self.MAIN.fill((25, 25, 25))
        pygame.draw.rect(self.MAIN, self.BG, [self.shift_ori, 0, self.w - 2 * self.shift_ori, self.h])


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
        self.logica.mouse_pos = pygame.mouse.get_pos()

        eventi = pygame.event.get()

        self.event_manager.event_manage_ui(eventi, self.logica)

        self.costruttore.scene["main"].disegna_scena(self.logica)
        self.costruttore.scene["main"].gestisci_eventi(eventi, self.logica)


    def end_cycle(self) -> None:
        '''
        Controlla se la combinazione di uscita è stata selezionata -> Uscita
        Altrimenti aggiornamento pagina
        '''

        self.mouse_icon()

        # aggiornamento
        self.current_fps = self.clock.get_fps()

        # PC status
        self.pc_attributes()

        # uscita
        keys = pygame.key.get_pressed()
        key_combo = [pygame.K_ESCAPE, pygame.K_SPACE]
        if all(keys[key] for key in key_combo):
            self.running = 0

        self.costruttore.font.scala_font(-1)
            
        pygame.display.flip()
        


    def pc_attributes(self):
        
        self.costruttore.scene["main"].label["memory"].text = "/high{ " + f' Memory: {psutil.Process().memory_info().rss / 1024**2:>7.2f} MB' + " }"
        
        if psutil.Process().memory_info().rss / 1024**2 > 4000:
            self.costruttore.scene["main"].label["memory"].color_bg = (255, 100, 100)
        else:
            self.costruttore.scene["main"].label["memory"].color_bg = (100, 100, 100)

        # -----------------------------------------------------------------------------

        self.cpu_sample.pop(0)
        self.cpu_sample.append(psutil.cpu_percent(interval=0))
        self.costruttore.scene["main"].label["cpu"].text = "/high{ " + f" CPU: {sum(self.cpu_sample) / len(self.cpu_sample):>3.0f}%" + " }"

        self.costruttore.scene["main"].label["cpu"].color_bg = (100, 100, 100)

        if sum(self.cpu_sample) / len(self.cpu_sample) > 30:
            self.costruttore.scene["main"].label["cpu"].color_bg = (150, 150, 100)

        if sum(self.cpu_sample) / len(self.cpu_sample) > 70:
            self.costruttore.scene["main"].label["cpu"].color_bg = (255, 100, 100)

        # -----------------------------------------------------------------------------
        
        self.costruttore.scene["main"].label["fps"].text = "/high{ " + f"FPS: {self.current_fps:>6.2f}" + " }"
        
        self.costruttore.scene["main"].label["fps"].color_bg = (100, 100, 100)
        
        if self.current_fps < 60:
            self.costruttore.scene["main"].label["fps"].color_bg = (150, 150, 100)

        if self.current_fps < 24:
            self.costruttore.scene["main"].label["fps"].color_bg = (255, 100, 100)
        
        # -----------------------------------------------------------------------------
        
        self.costruttore.scene["main"].label["clock"].text = "/high{ " + f" {strftime("%X, %x")}" " }"
        
        self.costruttore.scene["main"].label["clock"].color_bg = (100, 100, 100)
        
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


            self.costruttore.scene["main"].label["battery"].text = "/high{ " + f"{simbolo_corretto} {battery.percent:>5.1f}%" + " }"

            self.costruttore.scene["main"].label["battery"].color_bg = (100, 100, 100)

            if battery.percent < 20:
                self.costruttore.scene["main"].label["battery"].color_bg = (150, 150, 100)

            if battery.percent < 10:
                self.costruttore.scene["main"].label["battery"].color_bg = (255, 100, 100)


    @staticmethod
    def salva_screenshot(path, schermo):
        try:
            pygame.image.save(schermo, path)
        except FileNotFoundError:
            pass