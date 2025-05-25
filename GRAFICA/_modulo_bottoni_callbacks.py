from tkinter import filedialog
import pygame
import time
import os

NON_ESEGUIRE = False

if NON_ESEGUIRE:    
    from GRAFICA._modulo_elementi_grafici import Bottone_Push

class BottoniCallbacks:
    @staticmethod
    def print_hello(bottone: 'Bottone_Push'):
        bottone.testo = "/green{Cliccato!}"


    @staticmethod
    def exit(bottone: 'Bottone_Push'):
        # init_sound = pygame.mixer.Sound("./TEXTURES/AUDIO_SC2/Battlecruiser_Pissed06.ogg")
        # init_sound.play()
        # time.sleep(4.5)
        exit()


    @staticmethod
    def load_file(bottone: 'Bottone_Push'):
        nomi = filedialog.askopenfilename()
        if nomi != "":
            bottone.paths = [nomi]


    @staticmethod
    def load_files(bottone: 'Bottone_Push'):
        nomi = filedialog.askopenfilenames()
        if nomi != "":
            bottone.paths = list(nomi)
    

    @staticmethod
    def save_file(bottone: 'Bottone_Push', extension=".png"):
        bottone.paths.append(filedialog.asksaveasfilename(title="Salva file", defaultextension=extension))
        

    @staticmethod
    def change_state(bottone: 'Bottone_Push'):
        bottone.flag_foo = not bottone.flag_foo


    @staticmethod
    def save_file():
        return filedialog.asksaveasfilename(title="Salva file", defaultextension=".json")
    
    
    @staticmethod
    def open_file():
        return filedialog.askopenfilename()