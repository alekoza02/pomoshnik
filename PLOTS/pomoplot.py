import numpy as np

NON_ESEGUIRE = False

if NON_ESEGUIRE:    
    from GRAFICA._modulo_UI import Logica, UI
    from GRAFICA._modulo_elementi_grafici import Label_Text, Screen, Entrata


class PomoPlot:
    def __init__(self):
        self.screen: 'Screen' = None

        # ------------------------------------------------------------------------------
        # ZONA GEOMETRIA
        # ------------------------------------------------------------------------------
        self.plots: list[_Single1DPlot] = [_Single1DPlot(i) for i in ["fase0", "fase1", "fase2", "fase3"]]
        
        # ricerca il quadrato più grande disponibile all'interno dello schermo
        self.force_screen: bool = True
        # crea le coordinate di quest'area
        self.max_canvas_square: np.ndarray[float] = np.array([0., 0., 0., 0.]) 
        # crea le coordinate dell'area di solo plot
        self.max_plot_square: np.ndarray[float] = np.array([0., 0., 0., 0.]) 
        # crea le coordinate dell'area di solo plot in termini di valori nativi
        self.spazio_coordinate_native: np.ndarray[float] = np.array([0., 0., 0., 0.]) 
        
        # percentuali di utilizzo dell'area dedicata al plot in PERCENTUALE
        self.x_plot_area: float = 0.15
        self.y_plot_area: float = 0.1
        self.w_plot_area: float = 0.8
        self.h_plot_area: float = 0.8

        # ------------------------------------------------------------------------------
        # ZONA LABEL
        # ------------------------------------------------------------------------------
        # offset dei label in PIXEL
        self.formatting_x = "f"
        self.formatting_y = "f"

        self.draw_bounding_box: bool = True

        self.n_subdivisions_x: int = 5
        self.n_subdivisions_y: int = 5
        self.n_subdivisions_x_small: int = 5
        self.n_subdivisions_y_small: int = 5
        self.pixel_len_subdivisions: int = 20
        self.pixel_len_subdivisions_small: int = 7
        self.subdivision_x_centerd: bool = False
        self.subdivision_y_centerd: bool = False
    
        self.offset_x_label: int = 0 
        self.offset_y_label: int = 0 
        self.offset_x_tick_value: int = self.pixel_len_subdivisions + 10 
        self.offset_y_tick_value: int = self.pixel_len_subdivisions + 15
        
        self.minimal_offset_data_x = 0.05
        self.minimal_offset_data_y = 0.05

        self.ticks_type: bool = True # True -> automatic, False -> geometry based

        self.coords_of_ticks: list[list] = [[], []]
        self.min_ticks = 3
        self.max_ticks = 8
        self.nice_values = [1, 2, 2.5, 5, 10]
        self.round_ticks_x: int = 1
        self.round_ticks_y: int = 1

        # contiene Title, label X, label Y, label 2Y, Legenda
        self.labels: list['Label_Text'] = [None, None, None, None, None]

        # ------------------------------------------------------------------------------
        # ZONA COLORI
        # ------------------------------------------------------------------------------
        self.color_x_axis: list[int] = np.array([200, 200, 200])
        self.color_y_axis: list[int] = np.array([200, 200, 200])
        self.plot_area_color: list[int] = np.array([50, 50, 50])
        self.canvas_area_color: list[int] = np.array([45, 45, 45])
        self.unused_area_color: list[int] = np.array([40, 40, 40])



    def link_ui(self, UI: 'UI'):
        """Richiesta UI pomoshnik, si puù modificare manualmente per adattarla alla propria UI. Serve per intereagire con il grafico"""
        self.screen = UI.costruttore.scene["main"].screens["viewport"]
        self.labels[0] = UI.costruttore.scene["main"].label["title"]
        self.labels[1] = UI.costruttore.scene["main"].label["label_x"]
        self.labels[2] = UI.costruttore.scene["main"].label["label_y"]

        self.font_size_title: 'Entrata' = UI.costruttore.scene["main"].drop_menu["main"].elements["font_size_title"]
        self.font_size_label_x: 'Entrata' = UI.costruttore.scene["main"].drop_menu["main"].elements["font_size_label_x"]
        self.font_size_label_y: 'Entrata' = UI.costruttore.scene["main"].drop_menu["main"].elements["font_size_label_y"]
        
        self.text_title: 'Entrata' = UI.costruttore.scene["main"].drop_menu["main"].elements["text_title"]
        self.text_label_x: 'Entrata' = UI.costruttore.scene["main"].drop_menu["main"].elements["text_label_x"]
        self.text_label_y: 'Entrata' = UI.costruttore.scene["main"].drop_menu["main"].elements["text_label_y"]


    def update(self):
        ...


    def plot(self, logica: 'Logica'):
        """Richiesta UI pomoshnik, si può utilizzare con altri metodi di disegno. coordinate, colori e dimensioni sono forniti per poter essere usati in qualunque formato."""
        
        self._disegna_bg()
        self._disegna_assi()
        self._disegna_labels(logica)
        self._disegna_ticks()
        self._disegna_dati()
            

    def _disegna_labels(self, logica: 'Logica'):

        new_dim_title = self.font_size_title.get_text()
        new_dim_x = self.font_size_label_x.get_text()
        new_dim_y = self.font_size_label_y.get_text()

        if float(new_dim_title) != self.labels[0].font_size:
            self.labels[0].change_font_size(float(new_dim_title))
        if float(new_dim_x) != self.labels[1].font_size:
            self.labels[1].change_font_size(float(new_dim_x))
        if float(new_dim_y) != self.labels[2].font_size:
            self.labels[2].change_font_size(float(new_dim_y))

        # titolo
        self.labels[0].change_text(f"{self.text_title.get_text()}")
        self.labels[0].recalc_geometry(f"{self.screen.x + self.max_plot_square[0] + self.max_plot_square[2] / 2}", f"{self.screen.y + self.max_plot_square[1] / 2}", anchor_point="cc")
        self.labels[0].disegnami(logica)
        
        # X label
        self.labels[1].change_text(f"{self.text_label_x.get_text()}")
        self.labels[1].recalc_geometry(f"{self.screen.x + self.max_plot_square[0] + self.max_plot_square[2] / 2}", f"{self.screen.y + self.max_plot_square[3] + 2 * self.max_plot_square[1]}", anchor_point="cd")
        self.labels[1].disegnami(logica)
        
        # Y label
        self.labels[2].change_text(f"{self.text_label_y.get_text()}")
        self.labels[2].recalc_geometry(f"{self.screen.x + self.max_canvas_square[0]}", f"{self.screen.y + self.max_plot_square[1] + self.max_plot_square[3] / 2 - self.labels[2].font.font_pixel_dim[0] * self.labels[2].len_testo_diplayed / 2}", anchor_point="lu")
        self.labels[2].disegnami(logica, 90)


    def _get_nice_ticks(self):

        ticks_x = self._find_optimal_ticks([self.spazio_coordinate_native[0], self.spazio_coordinate_native[2]])
        ticks_y = self._find_optimal_ticks([self.spazio_coordinate_native[1], self.spazio_coordinate_native[3]])

        self.coords_of_ticks = [ticks_x, ticks_y]
        self.value_of_ticks = [ticks_x, ticks_y]


    def _disegna_ticks(self):

        coords = self._get_plot_area_coord()

        if self.ticks_type:

            for index, coord in enumerate(self.coords_of_ticks[0]):
                self.screen._add_line([[coord, coords[3]], [coord, coords[1]]], [100, 100, 100])
                self.screen._add_line([[coord, coords[3]], [coord, coords[3] + self.pixel_len_subdivisions]], self.color_y_axis)

                # disegno il valore corrispondente
                self.screen._add_text(f"{self.value_of_ticks[0][index]:.{self.round_ticks_x}{self.formatting_x}}", [coord, coords[3] + self.offset_y_label + self.offset_y_tick_value], anchor="cc")
                
            for index, coord in enumerate(self.coords_of_ticks[1]):
                self.screen._add_line([[coords[0], coord], [coords[2], coord]], [100, 100, 100])
                self.screen._add_line([[coords[0], coord], [coords[0] - self.pixel_len_subdivisions, coord]], self.color_y_axis)

                # disegno il valore corrispondente
                self.screen._add_text(f"{self.value_of_ticks[1][index]:.{self.round_ticks_y}{self.formatting_y}}", [coords[0] - self.offset_x_label - self.offset_y_tick_value, coord], anchor="rc")


        else:

            ###########
            # TICKS Y #
            ###########
            
            # calcolo spaziatura tra segni grandi e segni piccoli
            delta_y = abs((coords[1] - coords[3]) / self.n_subdivisions_x)
            delta_y_small = abs(delta_y / self.n_subdivisions_x_small)
            
            # controlla se la lineetta dev'essere centrata o meno
            offset_lineetta = self.pixel_len_subdivisions / 2 if self.subdivision_x_centerd else 0
            offset_lineetta_small = self.pixel_len_subdivisions_small / 2 if self.subdivision_x_centerd else 0
            
            for n in range(self.n_subdivisions_x + 1):

                # disegno le linee grande separate da delta_y
                self.screen._add_line([[coords[0] - self.offset_x_label + offset_lineetta, coords[1] + delta_y * n], [coords[0] - self.offset_x_label - self.pixel_len_subdivisions + offset_lineetta, coords[1] + delta_y * n]], self.color_y_axis)
                
                # disegno il valore corrispondente
                self.screen._add_text(f"{self.n_subdivisions_x - n}", [coords[0] - self.offset_x_label - self.offset_y_tick_value, coords[1] + delta_y * n], anchor="rc")
                
                # se fosse anche per n == self.n_subdivisions_x, allora avrebbe disegnato un settore in più del dovuto, dato che n indica l'inizio del settore
                if n < self.n_subdivisions_x:

                    for n1 in range(self.n_subdivisions_x_small + 1):
                        # disegno le linee piccole separate da delta_y_small   
                        self.screen._add_line([[coords[0] - self.offset_x_label + offset_lineetta_small, coords[1] + delta_y * n + delta_y_small * n1], [coords[0] - self.offset_x_label - self.pixel_len_subdivisions_small + offset_lineetta_small, coords[1] + delta_y * n + delta_y_small * n1]], self.color_y_axis)
        
            ###########
            # TICKS X #
            ###########

            # calcolo spaziatura tra segni grandi e segni piccoli
            delta_x = abs((coords[0] - coords[2]) / self.n_subdivisions_y)
            delta_x_small = abs(delta_x / self.n_subdivisions_y_small)
            
            # controlla se la lineetta dev'essere centrata o meno
            offset_lineetta = self.pixel_len_subdivisions / 2 if self.subdivision_y_centerd else 0
            offset_lineetta_small = self.pixel_len_subdivisions_small / 2 if self.subdivision_y_centerd else 0
            
            for n in range(self.n_subdivisions_y + 1):

                # disegno le linee grande separate da delta_x
                self.screen._add_line([[coords[0] + delta_x * n, coords[3] + self.offset_y_label - offset_lineetta], [coords[0] + delta_x * n, coords[3] + self.offset_y_label + self.pixel_len_subdivisions - offset_lineetta]], self.color_x_axis)

                # disegno il valore corrispondente
                self.screen._add_text(f"{n}", [coords[0] + delta_x * n, coords[3] + self.offset_y_label + self.offset_y_tick_value], anchor="cu")

                # se fosse anche per n == self.n_subdivisions_y, allora avrebbe disegnato un settore in più del dovuto, dato che n indica l'inizio del settore
                if n < self.n_subdivisions_y:

                    for n1 in range(self.n_subdivisions_y_small + 1):
                        # disegno le linee piccole separate da delta_x_small 
                        self.screen._add_line([[coords[0] + delta_x * n + delta_x_small * n1, coords[3] + self.offset_y_label - offset_lineetta_small], [coords[0] + delta_x * n + delta_x_small * n1, coords[3] + self.offset_y_label + self.pixel_len_subdivisions_small - offset_lineetta_small]], self.color_x_axis)
        


    def _disegna_assi(self):

        coords = self._get_plot_area_coord()

        if self.draw_bounding_box:
            self.screen._add_line([[self.max_plot_square[0], self.max_plot_square[1]], [self.max_plot_square[0] + self.max_plot_square[2], self.max_plot_square[1]]], self.color_x_axis, 1)
            self.screen._add_line([[self.max_plot_square[0] + self.max_plot_square[2], self.max_plot_square[1]], [self.max_plot_square[0] + self.max_plot_square[2], self.max_plot_square[1] + self.max_plot_square[3]]], self.color_x_axis, 1)

        # si posizione sull'area del plot e setta un offset pari a self.offset_x_label o self.offset_y_label
        self.screen._add_line([[coords[0] - self.offset_x_label, coords[1]], [coords[0] - self.offset_x_label, coords[3]]], self.color_y_axis)
        self.screen._add_line([[coords[0], coords[3] + self.offset_y_label], [coords[2], coords[3] + self.offset_y_label]], self.color_x_axis)
    
                    
    def _disegna_dati(self):
        # preparazione dati
        self._normalize_data2screen()

        for plot in self.plots:
            # disegno i dati
            self.screen._add_points(plot.data2plot, plot.scatter_color, plot.scatter_width)
            self.screen._add_lines(plot.data2plot, plot.function_color, plot.function_width)


    def _disegna_bg(self):
        # setu-up canvas
        self.screen._clear_canvas(self.unused_area_color)
        # disegno area di plot BG
        self.screen._add_rectangle(self.max_canvas_square, self.canvas_area_color)
        self.screen._add_rectangle(self.max_plot_square, self.plot_area_color)
        

    def _normalize_data2screen(self, invert_y_coord=True):
        """Normalizes the data to the screen size"""
        
        # ricerca dell'area di disegno
        self._find_max_square()
        self._get_native_data_bounds()


        for plot in self.plots:
            # copia dei dati per trasformarle in screen coordinates
            plot.data2plot = plot.data.copy()

            # set dello 0
            plot.data2plot[:, 0] -= self.spazio_coordinate_native[0]
            # normalizzazione
            plot.data2plot[:, 0] /= self.spazio_coordinate_native[2]
            # adatto alla dimensione dell'area del plot
            plot.data2plot[:, 0] *= (self.max_plot_square[2])
            # traslo in base all'offset all'interno dell'area del plot
            plot.data2plot[:, 0] += (self.max_canvas_square[2] * self.x_plot_area)
            # traslo in base all'offset dell'area del plot nello schermo
            plot.data2plot[:, 0] += self.max_canvas_square[0]
            

            # stessa cosa ma per l'asse y
            plot.data2plot[:, 1] -= self.spazio_coordinate_native[1]
            plot.data2plot[:, 1] /= self.spazio_coordinate_native[3]
            plot.data2plot[:, 1] *= (self.max_plot_square[3])
            
            # inverto i dati per avere le Y che aumentano salendo sullo schermo
            if invert_y_coord:
                plot.data2plot[:, 1] = self.max_canvas_square[3] * self.h_plot_area - plot.data2plot[:, 1]
            
            plot.data2plot[:, 1] += (self.max_canvas_square[3] * self.y_plot_area)
            plot.data2plot[:, 1] += self.max_canvas_square[1]


        # ticks x
        self.coords_of_ticks[0] -= self.spazio_coordinate_native[0]
        self.coords_of_ticks[0] /= self.spazio_coordinate_native[2]
        self.coords_of_ticks[0] *= (self.max_plot_square[2])
        self.coords_of_ticks[0] += (self.max_canvas_square[2] * self.x_plot_area)
        self.coords_of_ticks[0] += self.max_canvas_square[0]

        # ticks y
        self.coords_of_ticks[1] -= self.spazio_coordinate_native[1]
        self.coords_of_ticks[1] /= self.spazio_coordinate_native[3]
        self.coords_of_ticks[1] *= (self.max_plot_square[3])        
        if invert_y_coord:
            self.coords_of_ticks[1] = self.max_canvas_square[3] * self.h_plot_area - self.coords_of_ticks[1]
        self.coords_of_ticks[1] += (self.max_canvas_square[3] * self.y_plot_area)
        self.coords_of_ticks[1] += self.max_canvas_square[1]
        


    def _find_equivalent_pixels(self, values, ax="x"):
        
        coords = self._get_plot_area_coord()

        if ax == "x":
            delta_values = abs(self.spazio_coordinate_native[2])
            delta_pixels = abs(coords[0] - coords[2]) * 0.9
            pixel_offset = values[0] - self.spazio_coordinate_native[0] 
        if ax == "y":
            delta_values = abs(self.spazio_coordinate_native[3])
            delta_pixels = abs(coords[1] - coords[3]) * 0.9
            pixel_offset = values[-1] - self.spazio_coordinate_native[3] 

        if delta_pixels != 0 and delta_values != 0:
            conversion_factor = delta_values / delta_pixels # how much values fit in 1 pixel
        else:
            conversion_factor = 1

        values = np.array(values)
        values -= np.min(values)

        values /= conversion_factor

        ancoraggio = coords[0] if ax == "x" else coords[1]
        
        if ax == "y":
            save = np.min(values)
            values -= save
            values = - values
            values -= np.min(values)
            values += save

        if ax == "x":
            values += pixel_offset / conversion_factor 
            values += abs(coords[0] - coords[2]) * 0.05
        elif ax == "y":
            values -= (pixel_offset - self.spazio_coordinate_native[1]) / conversion_factor 
            values -= abs(coords[1] - coords[3]) * 0.05

        values += ancoraggio

        return values


    def _find_optimal_ticks(self, start_values):
 
        def power_converter(value):

            if value >= 0:
                return float("1" + "0" * value)            
            else:
                return 1 / float("1" + "0" * -value)            


        all_combinations = []
        power_per_tick = []

        delta = start_values[-1] - start_values[0]    

        for n_ticks in range(self.min_ticks, self.max_ticks + 1):
            
            spacing = abs(delta / n_ticks)

            run = 1
            power = 0
            safe = 0

            while run:
                if spacing * power_converter(power) // self.nice_values[0] <= 1:
                    power += 1
                elif spacing * power_converter(power) // self.nice_values[-1] >= 1:
                    power -= 1

                if spacing * power_converter(power) // self.nice_values[0] >= 1 and spacing * power_converter(power) // self.nice_values[-1] <= 1:
                    run = 0
                
                safe += 1
                if safe > 1024:
                    run = 0

            
            all_combinations.append([abs(spacing * power_converter(power) - value) for value in self.nice_values])
            power_per_tick.append(power_converter(-power))
            
        best_from_tick = []
        for single_tick in all_combinations:
            best_from_tick.append([min(single_tick), single_tick.index(min(single_tick))])

        minimo = np.inf
        indice_valore = 0
        indice_tick = 0

        
        for index, contendente in enumerate(best_from_tick):
            
            if contendente[0] <= minimo:
                minimo = contendente[0]
                indice_valore = contendente[1]
                indice_tick = index


        new_start = round(start_values[0] / (self.nice_values[indice_valore] * power_per_tick[indice_tick])) * (self.nice_values[indice_valore] * power_per_tick[indice_tick])
        
        ris = [round(new_start + self.nice_values[indice_valore] * power_per_tick[indice_tick] * i, 3) for i in range(0, indice_tick + self.min_ticks + 2)]
            
        # decido se tenere l'ultimo elemento
        while abs(start_values[-1] - ris[-1]) > abs(start_values[-1] - ris[-2]):
            _ = ris.pop()
            # print(f"DEBUG: eliminato il punto {_} perchè troppo lontano")


        return ris

    
    def _find_max_square(self):
        
        # se ho uno schermo su cui disegnare
        if not self.screen is None:

            # se è richiesto formato quadrato
            if self.force_screen:
                
                # trovo l'asse principale
                if self.screen.w > self.screen.h:
                    # caso orizzontale, setto offset dell'area nello schermo e la sua dimensione
                    offset_x = (self.screen.w - self.screen.h) / 2
                    offset_y = 0
                    dimension = self.screen.h
                else:
                    # caso verticale, setto offset dell'area nello schermo e la sua dimensione
                    offset_x = 0
                    offset_y = (self.screen.h - self.screen.w) / 2
                    dimension = self.screen.w 
            
                self.max_canvas_square = np.array([offset_x, offset_y, dimension, dimension])
                self.max_plot_square = np.array([
                    self.max_canvas_square[0] + self.max_canvas_square[2] * self.x_plot_area,
                    self.max_canvas_square[1] + self.max_canvas_square[3] * self.y_plot_area,
                    self.max_canvas_square[2] * self.w_plot_area,
                    self.max_canvas_square[3] * self.h_plot_area,
                ])


            else:
                # area del plot coincide con lo schermo
                self.max_canvas_square = np.array([0, 0, self.screen.w, self.screen.h])
                self.max_plot_square = np.array([
                    self.max_canvas_square[2] * self.x_plot_area,
                    self.max_canvas_square[3] * self.y_plot_area,
                    self.max_canvas_square[2] * self.w_plot_area,
                    self.max_canvas_square[3] * self.h_plot_area,
                ])



    def _get_plot_area_coord(self):
        return (
            self.max_canvas_square[0] + self.max_canvas_square[2] * self.x_plot_area,
            self.max_canvas_square[1] + self.max_canvas_square[3] * self.y_plot_area,
            self.max_canvas_square[0] + self.max_canvas_square[2] * (self.x_plot_area + self.w_plot_area),
            self.max_canvas_square[1] + self.max_canvas_square[3] * (self.y_plot_area + self.h_plot_area),
        )



    def _get_native_data_bounds(self):
        self.spazio_coordinate_native = np.array([np.inf, np.inf, -np.inf, -np.inf])
        
        for plot in self.plots:
            # trova le coordinate minime tra tutti i grafici
            self.spazio_coordinate_native[0] = np.minimum(self.spazio_coordinate_native[0], np.min(plot.data[:, 0]))
            self.spazio_coordinate_native[1] = np.minimum(self.spazio_coordinate_native[1], np.min(plot.data[:, 1]))
            self.spazio_coordinate_native[2] = np.maximum(self.spazio_coordinate_native[2], np.max(plot.data[:, 0]))
            self.spazio_coordinate_native[3] = np.maximum(self.spazio_coordinate_native[3], np.max(plot.data[:, 1]))

        # ottengo i ticks belli
        self._get_nice_ticks()

        # trova le coordinate minime tra tutti i grafici + ticks
        self.spazio_coordinate_native[0] = np.minimum(self.spazio_coordinate_native[0], np.min(self.coords_of_ticks[0]))
        self.spazio_coordinate_native[1] = np.minimum(self.spazio_coordinate_native[1], np.min(self.coords_of_ticks[1]))
        self.spazio_coordinate_native[2] = np.maximum(self.spazio_coordinate_native[2], np.max(self.coords_of_ticks[0]))
        self.spazio_coordinate_native[3] = np.maximum(self.spazio_coordinate_native[3], np.max(self.coords_of_ticks[1]))

        # applico lo spostamento dei dati in base all'offset minimo richiesto dagli assi cartesiani
        self.spazio_coordinate_native[0] -= (self.spazio_coordinate_native[2] - self.spazio_coordinate_native[0]) * self.minimal_offset_data_x
        self.spazio_coordinate_native[1] -= (self.spazio_coordinate_native[3] - self.spazio_coordinate_native[1]) * self.minimal_offset_data_y
        self.spazio_coordinate_native[2] += (self.spazio_coordinate_native[2] - self.spazio_coordinate_native[0]) * self.minimal_offset_data_x
        self.spazio_coordinate_native[3] += (self.spazio_coordinate_native[3] - self.spazio_coordinate_native[1]) * self.minimal_offset_data_y

        # modifica il valore della larghezza e altezza non come coordinate assolute, ma come relative al vertice iniziale
        self.spazio_coordinate_native[2] -= self.spazio_coordinate_native[0]
        self.spazio_coordinate_native[3] -= self.spazio_coordinate_native[1]


class _Single1DPlot:
    def __init__(self, mode: str):
        self.data: np.ndarray[float] = np.array([[x - 100, np.pi * 10 * (x - 100) / 100] for x in range(201)], dtype=np.float64)
        
        match mode:
            case "fase0":
                self.data[:, 1] = (self.data[:, 1] / 10) ** 2 * np.sin(self.data[:, 1] + 0 * np.pi / 4)
                self.scatter_color = [255, 0, 0]
                self.function_color = [224, 0, 0]
            case "fase1":
                self.data[:, 1] = (self.data[:, 1] / 10) ** 2 * np.sin(self.data[:, 1] + 1 * np.pi / 4)
                self.scatter_color = [255, 64, 64]
                self.function_color = [224, 32, 32]
            case "fase2":
                self.data[:, 1] = (self.data[:, 1] / 10) ** 2 * np.sin(self.data[:, 1] + 2 * np.pi / 4)
                self.scatter_color = [255, 128, 128]
                self.function_color = [224, 94, 94]
            case "fase3":
                self.data[:, 1] = (self.data[:, 1] / 10) ** 2 * np.sin(self.data[:, 1] + 3 * np.pi / 4)
                self.scatter_color = [255, 192, 192]
                self.function_color = [224, 160, 160]
            
        self.data2plot: np.ndarray[float] = None

        self.scatter = True
        self.scatter_width = 3
        self.function = True
        self.function_width = 1