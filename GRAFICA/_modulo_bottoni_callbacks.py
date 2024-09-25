NON_ESEGUIRE = False

if NON_ESEGUIRE:    
    from GRAFICA._modulo_elementi_grafici import Bottone_Push

class BottoniCallbacks:
    def print_hello(bottone: 'Bottone_Push'):
        bottone.testo = "/green{Cliccato!}"