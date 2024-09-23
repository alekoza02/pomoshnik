NON_ESEGUIRE = False

if NON_ESEGUIRE:    
    from GRAFICA._modulo_elementi_grafici import Bottone

class BottoniCallbacks:
    def print_hello(bottone: 'Bottone'):
        bottone.text = "/green{Cliccato!}"