class MateUtils:
    
    @staticmethod
    def hex2rgb(colore: str, std_return=[255, 0, 255]) -> list[int]:
        '''Accetta SOLO il formato: 123456'''
        try:
            r = int(colore[0:2], base=16)
            g = int(colore[2:4], base=16)
            b = int(colore[4:6], base=16)
            return [r,g,b]
        except ValueError:
            return std_return


    @staticmethod
    def rgb2hex(colore: list[int], scala=1, std_return="ff00ff") -> str:
        '''Accetta SOLO il formato: [255, 255, 255]'''
        try:
            colore = [int(col * 255) if scala == 255 else int(col) for col in colore]
            r = hex(colore[0])
            g = hex(colore[1])
            b = hex(colore[2])

            if colore[0] == 0:
                r += "0"
            if colore[1] == 0:
                g += "0"
            if colore[2] == 0:
                b += "0"

            if len(r[2:]) == 1:
                r = r[:2] + "0" + r[2:]
            if len(g[2:]) == 1:
                g = g[:2] + "0" + g[2:]
            if len(b[2:]) == 1:
                b = b[:2] + "0" + b[2:]

            return f"{r[2:]}{g[2:]}{b[2:]}"
        except ValueError:
            return std_return

    
    @staticmethod
    def inp2int(valore: str, std_return: int = 0) -> int:
        try:
            return int(valore)
        except ValueError:
            return std_return


    @staticmethod
    def inp2flo(valore: str, std_return: float = 0.0) -> float:
        try:
            return float(valore)
        except:
            return std_return