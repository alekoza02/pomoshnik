from tkinter import filedialog
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