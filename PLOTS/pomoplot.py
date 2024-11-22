import numpy as np
from scipy.ndimage import gaussian_filter 
from MATEMATICA._modulo_mate_utils import MateUtils
from PIL import Image

NON_ESEGUIRE = False

if NON_ESEGUIRE:    
    from GRAFICA._modulo_UI import Logica, UI
    from GRAFICA._modulo_elementi_grafici import Label_Text, Screen, Entrata, Bottone_Toggle, Scroll, ColorPicker, Bottone_Push, RadioButton


class PomoPlot:
    def __init__(self):
        self.screen: 'Screen' = None

        # ------------------------------------------------------------------------------
        # ZONA GEOMETRIA
        # ------------------------------------------------------------------------------
        # self.plots: list[_Single1DPlot] = [_Single1DPlot(i) for i in ["fase0", "fase1", "fase2", "fase3"]]
        self.plots: list[_Single1DPlot] = []
        self.active_plot: _Single1DPlot = None

        # ricerca il quadrato più grande disponibile all'interno dello schermo
        self.force_screen: bool = True
        # crea le coordinate di quest'area
        self.max_canvas_square: np.ndarray[float] = np.array([0., 0., 0., 0.]) 
        # crea le coordinate dell'area di solo plot
        self.max_plot_square: np.ndarray[float] = np.array([0., 0., 0., 0.]) 
        # crea le coordinate dell'area di solo plot in termini di valori nativi
        self.spazio_coordinate_native: np.ndarray[float] = np.array([-1., -1., 1., 1.]) 
        
        # ------------------------------------------------------------------------------
        # ZONA LABEL
        # ------------------------------------------------------------------------------
        # offset dei label in PIXEL

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
        
        # contiene Title, label X, label Y, label 2Y, Legenda
        self.labels: list['Label_Text'] = [None, None, None, None, None]
        # ------------------------------------------------------------------------------
        # ZONA COLORI
        # ------------------------------------------------------------------------------
        self.unused_area_color: list[int] = np.array([40, 40, 40]) # FIX unify
        self.zoom_boundaries = np.array([0., 0., 1., 1.])



    def link_ui(self, UI: 'UI'):
        """Richiesta UI pomoshnik, si puù modificare manualmente per adattarla alla propria UI. Serve per intereagire con il grafico"""
        self.screen = UI.costruttore.scene["main"].screens["viewport"]
        self.screen_render = UI.costruttore.scene["main"].screens["renderer"]

        self.scale_factor_viewport = 1

        self.tools: 'RadioButton' = UI.costruttore.scene["main"].bottoni_r["tools"]
        self.reset_tools: 'Bottone_Push' = UI.costruttore.scene["main"].bottoni_p["reset_zoom"]

        self.labels[0] = UI.costruttore.scene["main"].label["title"]
        self.labels[1] = UI.costruttore.scene["main"].label["label_x"]
        self.labels[2] = UI.costruttore.scene["main"].label["label_y"]
        self.labels[4] = UI.costruttore.scene["main"].label["legend"]

        self.x_plot_area: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item1"].elements["x_plot_area"]
        self.y_plot_area: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item1"].elements["y_plot_area"]
        self.w_plot_area: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item1"].elements["w_plot_area"]
        self.h_plot_area: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item1"].elements["h_plot_area"]
        self.plot_area_color: 'ColorPicker' = UI.costruttore.scene["main"].drop_menu["item1"].elements["plot_area_bg"]
        self.canvas_area_color: 'ColorPicker' = UI.costruttore.scene["main"].drop_menu["item1"].elements["canvas_area_bg"]
        
        
        self.scroll_plots: 'Scroll' = UI.costruttore.scene["main"].scrolls["elenco_plots"]

        self.plot_name: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item2"].elements["plot_name"]

        self.scatter_size: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item2"].elements["scatter_size"]
        self.function_size: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item2"].elements["function_size"]
        self.dashed_density: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item2"].elements["dashed_density"]
        
        self.scatter_toggle: 'Bottone_Toggle' = UI.costruttore.scene["main"].drop_menu["item2"].elements["scatter_toggle"]
        self.function_toggle: 'Bottone_Toggle' = UI.costruttore.scene["main"].drop_menu["item2"].elements["function_toggle"]
        self.dashed_toggle: 'Bottone_Toggle' = UI.costruttore.scene["main"].drop_menu["item2"].elements["dashed"]
        self.error_bar: 'Bottone_Toggle' = UI.costruttore.scene["main"].drop_menu["item2"].elements["errorbar"]

        self.colore_function: 'ColorPicker' = UI.costruttore.scene["main"].drop_menu["item2"].elements["colore_function"]
        self.colore_scatter: 'ColorPicker' = UI.costruttore.scene["main"].drop_menu["item2"].elements["colore_scatter"]

        self.font_size_title: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item3"].elements["font_size_title"]
        self.font_size_label_x: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item3"].elements["font_size_label_x"]
        self.font_size_label_y: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item3"].elements["font_size_label_y"]
        
        self.text_title: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item3"].elements["text_title"]
        self.text_label_x: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item3"].elements["text_label_x"]
        self.text_label_y: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item3"].elements["text_label_y"]
        self.label_title_color: 'ColorPicker' = UI.costruttore.scene["main"].drop_menu["item3"].elements["label_title_color"]
        self.label_x_color: 'ColorPicker' = UI.costruttore.scene["main"].drop_menu["item3"].elements["label_x_color"]
        self.label_y_color: 'ColorPicker' = UI.costruttore.scene["main"].drop_menu["item3"].elements["label_y_color"]

        self.round_ticks_x: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item4"].elements["round_x"]
        self.round_ticks_y: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item4"].elements["round_y"]
        
        self.ax_color_x: 'ColorPicker' = UI.costruttore.scene["main"].drop_menu["item4"].elements["ax_color_x"]
        self.ax_color_y: 'ColorPicker' = UI.costruttore.scene["main"].drop_menu["item4"].elements["ax_color_y"]
        self.tick_color_x: 'ColorPicker' = UI.costruttore.scene["main"].drop_menu["item4"].elements["tick_color_x"]
        self.tick_color_y: 'ColorPicker' = UI.costruttore.scene["main"].drop_menu["item4"].elements["tick_color_y"]
        
        self.formatting_x: 'Bottone_Toggle' = UI.costruttore.scene["main"].drop_menu["item4"].elements["formatting_x"]
        self.formatting_y: 'Bottone_Toggle' = UI.costruttore.scene["main"].drop_menu["item4"].elements["formatting_y"]
        
        self.show_grid_x: 'Bottone_Toggle' = UI.costruttore.scene["main"].drop_menu["item4"].elements["show_grid_x"]
        self.show_grid_y: 'Bottone_Toggle' = UI.costruttore.scene["main"].drop_menu["item4"].elements["show_grid_y"]
        
        self.show_legend: 'Bottone_Toggle' = UI.costruttore.scene["main"].drop_menu["item5"].elements["show_legend"]
        self.x_legend: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item5"].elements["x_legend"]
        self.y_legend: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item5"].elements["y_legend"]
        self.font_size_legend: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item5"].elements["font_size_legend"]
        self.show_legend_background: 'Bottone_Toggle' = UI.costruttore.scene["main"].drop_menu["item5"].elements["show_legend_background"]
        self.legend_bg_color: 'ColorPicker' = UI.costruttore.scene["main"].drop_menu["item5"].elements["legend_color_background"]
        self.transparent_background: 'Bottone_Toggle' = UI.costruttore.scene["main"].drop_menu["item5"].elements["transparent_background"]
        self.blur_strenght: 'Entrata' = UI.costruttore.scene["main"].drop_menu["item5"].elements["blur_strenght"]
        self.show_icons: 'Bottone_Toggle' = UI.costruttore.scene["main"].drop_menu["item5"].elements["show_icons"]
        self.match_color_text: 'Bottone_Toggle' = UI.costruttore.scene["main"].drop_menu["item5"].elements["match_color_text"]
        self.color_text: 'ColorPicker' = UI.costruttore.scene["main"].drop_menu["item5"].elements["color_text"]

        self.import_single_plot: 'Bottone_Push' = UI.costruttore.scene["main"].drop_menu["item6"].elements["import_single_plot"]
        self.import_multip_plot: 'Bottone_Push' = UI.costruttore.scene["main"].drop_menu["item6"].elements["import_multip_plot"]

        self.save_single_plot: 'Bottone_Push' = UI.costruttore.scene["main"].drop_menu["item7"].elements["save_single_plot"]


    def update_plot_list(self, added_plot):
        self.scroll_plots.add_element_scroll(added_plot, False)
        

    def update(self, logica: 'Logica'):

        # cambio grafico attivo
        self.plots = self.scroll_plots.elementi
        old_active = self.active_plot
        if len(self.scroll_plots.elementi) > 0:

            self.active_plot: _Single1DPlot = self.scroll_plots.elementi[self.scroll_plots.ele_selected_index]

            if self.active_plot != old_active:

                self.zoom_boundaries = np.array([0., 0., 1., 1.])

                self.scatter_size.change_text(f"{self.active_plot.scatter_width}")
                self.function_size.change_text(f"{self.active_plot.function_width}")
                self.plot_name.change_text(f"{self.active_plot.nome}")
                self.scatter_toggle.state_toggle = self.active_plot.scatter
                self.function_toggle.state_toggle = self.active_plot.function
                self.dashed_toggle.state_toggle = self.active_plot.dashed
                self.error_bar.state_toggle = self.active_plot.errorbar
                self.dashed_density.change_text(f"{self.active_plot.dashed_traits}")
                self.colore_scatter.set_color(self.active_plot.scatter_color)
                self.colore_function.set_color(self.active_plot.function_color)

                if self.active_plot.data.shape[1] <= 2:
                    self.error_bar.bg = np.array([70, 40, 40])
                else:
                    self.error_bar.bg = np.array([40, 70, 40])


        # import plots
        [self.import_plot_data(path) for path in self.import_single_plot.paths]
        [self.import_plot_data(path) for path in self.import_multip_plot.paths]
            
        self.import_single_plot.paths = []            
        self.import_multip_plot.paths = []


        # salvataggio screenshot
        if len(self.save_single_plot.paths) > 0:

            self.scale_factor_renderer = self.screen_render.w / self.screen.w

            self.screen_backup = self.screen
            self.screen = self.screen_render

            self.screen_backup.hide = True
            self.screen.hide = False

            self.scale_factor_backup = self.scale_factor_viewport
            self.scale_factor_viewport = self.scale_factor_renderer

            self.plot(logica, screenshot=1)
            self.plot(logica, screenshot=1)

            # self.screen.load_image()
            # self.screen.tavolozza.blit(self.screen.loaded_image, (self.screen.x, self.screen.y))
            
            self.screen._save_screenshot(self.save_single_plot.paths[-1])
            self.save_single_plot.paths.pop()
            
            self.scale_factor_viewport = self.scale_factor_backup
            
            self.screen_render = self.screen
            self.screen = self.screen_backup
        
            self.screen_render.hide = True
            self.screen.hide = False

        self.screen._add_points([
            [self.max_plot_square[0], self.max_plot_square[1]],
            [self.max_plot_square[2], self.max_plot_square[3]],
        ], [255, 255, 255], 10)
        
        # logica zoom mouse
        if self.tools.cb_s[0] and logica.dragging_finished_FLAG and self.screen.bounding_box.collidepoint(logica.mouse_pos) and logica.original_start_pos[0] != logica.dragging_end_pos[0] and logica.original_start_pos[1] != logica.dragging_end_pos[1]:
            logica.dragging_finished_FLAG = False
            
            dragging_1 = self._extract_mouse_coordinate(logica.original_start_pos)          # x1 and y1
            dragging_2 = self._extract_mouse_coordinate(logica.dragging_end_pos)            # x2 and y2
            
            dragging_1[0], dragging_2[0] = min(dragging_1[0], dragging_2[0]), max(dragging_1[0], dragging_2[0])
            dragging_1[1], dragging_2[1] = min(dragging_1[1], dragging_2[1]), max(dragging_1[1], dragging_2[1])

            dragging_1 = dragging_1.astype(np.float64)
            dragging_2 = dragging_2.astype(np.float64)

            dragging_1[0] -= self.max_plot_square[2] * self.minimal_offset_data_x
            dragging_2[0] -= self.max_plot_square[2] * self.minimal_offset_data_x
            dragging_1[1] -= self.max_plot_square[3] * self.minimal_offset_data_y
            dragging_2[1] -= self.max_plot_square[3] * self.minimal_offset_data_y

            dragging_1[0] /= self.max_plot_square[2] * (1 - self.minimal_offset_data_x * 2)
            dragging_2[0] /= self.max_plot_square[2] * (1 - self.minimal_offset_data_x * 2)
            dragging_1[1] /= self.max_plot_square[3] * (1 - self.minimal_offset_data_y * 2)
            dragging_2[1] /= self.max_plot_square[3] * (1 - self.minimal_offset_data_y * 2)

            dragging_1[1] = 1 - dragging_1[1]
            dragging_2[1] = 1 - dragging_2[1]

            dragging_1[1], dragging_2[1] = dragging_2[1], dragging_1[1]

            x1 = self.zoom_boundaries[0] + dragging_1[0] * (self.zoom_boundaries[2] - self.zoom_boundaries[0])
            x2 = self.zoom_boundaries[0] + dragging_2[0] * (self.zoom_boundaries[2] - self.zoom_boundaries[0])

            y1 = self.zoom_boundaries[1] + dragging_1[1] * (self.zoom_boundaries[3] - self.zoom_boundaries[1])
            y2 = self.zoom_boundaries[1] + dragging_2[1] * (self.zoom_boundaries[3] - self.zoom_boundaries[1])

            self.zoom_boundaries = np.array([x1, y1, x2, y2])


        # logica zoom rotella
        if logica.scroll_down and self.screen.bounding_box.collidepoint(logica.mouse_pos):
            self.zoom_boundaries[0] -= logica.scroll_down * (self.zoom_boundaries[2] - self.zoom_boundaries[0]) / 100
            self.zoom_boundaries[1] -= logica.scroll_down * (self.zoom_boundaries[2] - self.zoom_boundaries[0]) / 100
            self.zoom_boundaries[2] += logica.scroll_down * (self.zoom_boundaries[3] - self.zoom_boundaries[1]) / 100
            self.zoom_boundaries[3] += logica.scroll_down * (self.zoom_boundaries[3] - self.zoom_boundaries[1]) / 100
        if logica.scroll_up and self.screen.bounding_box.collidepoint(logica.mouse_pos):
            self.zoom_boundaries[0] += logica.scroll_up * (self.zoom_boundaries[2] - self.zoom_boundaries[0]) / 100
            self.zoom_boundaries[1] += logica.scroll_up * (self.zoom_boundaries[2] - self.zoom_boundaries[0]) / 100
            self.zoom_boundaries[2] -= logica.scroll_up * (self.zoom_boundaries[3] - self.zoom_boundaries[1]) / 100
            self.zoom_boundaries[3] -= logica.scroll_up * (self.zoom_boundaries[3] - self.zoom_boundaries[1]) / 100


        # logica pan
        if self.tools.cb_s[1] and self.screen.bounding_box.collidepoint(logica.mouse_pos) and logica.dragging:
            self.zoom_boundaries[0] -= (self.zoom_boundaries[2] - self.zoom_boundaries[0]) * logica.dragging_dx / self.screen.w
            self.zoom_boundaries[1] -= (self.zoom_boundaries[3] - self.zoom_boundaries[1]) * logica.dragging_dy / self.screen.h
            self.zoom_boundaries[2] -= (self.zoom_boundaries[2] - self.zoom_boundaries[0]) * logica.dragging_dx / self.screen.w
            self.zoom_boundaries[3] -= (self.zoom_boundaries[3] - self.zoom_boundaries[1]) * logica.dragging_dy / self.screen.h


        # reset pan & zoom
        if self.reset_tools.flag_foo:
            self.reset_tools.flag_foo = 0
            self.tools.set_state([0, 0])
            self.zoom_boundaries = np.array([0., 0., 1., 1.])




    def plot(self, logica: 'Logica', screenshot=0):
        """Richiesta UI pomoshnik, si può utilizzare con altri metodi di disegno. coordinate, colori e dimensioni sono forniti per poter essere usati in qualunque formato."""

        if not screenshot:
            self.update(logica)

        self._disegna_bg()
        self._disegna_assi()
        self._disegna_labels(logica)
        self._disegna_ticks()
        self._disegna_dati()
        self._disegna_legend(logica)

        if not screenshot:
            self._disegna_mouse_coordinate(logica)
            self._disegna_mouse_zoom(logica)
            

    def _disegna_mouse_zoom(self, logica: 'Logica'):
        
        if logica.dragging and self.tools.cb_s[0]:

            rectangle = [logica.original_start_pos[0], logica.original_start_pos[1], logica.dragging_end_pos[0], logica.dragging_end_pos[1]]

            rectangle[0], rectangle[2] = min(rectangle[0], rectangle[2]), max(rectangle[0], rectangle[2])
            rectangle[1], rectangle[3] = min(rectangle[1], rectangle[3]), max(rectangle[1], rectangle[3])

            rectangle[2] -= rectangle[0]
            rectangle[3] -= rectangle[1]

            rectangle[0] -= self.screen.x
            rectangle[1] -= self.screen.y

            self.screen._add_rectangle(rectangle, [0, 255, 0], 2)

        if logica.dragging and self.tools.cb_s[1]:
            x1 = logica.original_start_pos[0] - self.screen.x
            y1 = logica.original_start_pos[1] - self.screen.y
            x2 = logica.dragging_end_pos[0] - self.screen.x
            y2 = logica.dragging_end_pos[1] - self.screen.y
            self.screen._add_line([[x1, y1], [x2, y2]], [0, 255, 0], 2)


    def _disegna_mouse_coordinate(self, logica: 'Logica'):
        
        try:

            value = self._extract_mouse_coordinate(logica.mouse_pos)
            value = self._transform_native_space(value)

            posizione = np.array(logica.mouse_pos)

            posizione[0] -= self.screen.x
            posizione[1] -= self.screen.y

            self.screen._add_text(f"({float(value[0]):.{int(self.round_ticks_x.get_text())}f}, {float(value[1]):.{int(self.round_ticks_y.get_text())}f})", size=1.2, pos=posizione, anchor="cd", color=[150, 160, 150])

        except Exception as e:
            print(e)


    def _transform_native_space(self, value):

        value = value.astype(float)

        value[0] /= self.max_plot_square[2]
        value[1] /= self.max_plot_square[3]

        value[1] = 1 - value[1]

        value[0] *= self.spazio_coordinate_native[2]
        value[1] *= self.spazio_coordinate_native[3]
        
        value[0] += self.spazio_coordinate_native[0]
        value[1] += self.spazio_coordinate_native[1]

        return value


    def _extract_mouse_coordinate(self, pos: tuple[int]) -> tuple[float]:
        pos = np.array(pos)

        pos[0] -= self.screen.x
        pos[1] -= self.screen.y

        pos[0] -= self.max_plot_square[0]
        pos[1] -= self.max_plot_square[1]
        
        return pos


    def _disegna_legend(self, logica: 'Logica'):

        if len([1 for status in self.scroll_plots.ele_mask if status]) > 0 and self.show_legend.state_toggle:

            self.legend_position = [float(self.x_legend.get_text()), float(self.y_legend.get_text())]               # done
            self.legend_draw_icogram = self.show_icons.state_toggle                                                 # NO                           
            self.legend_match_color_title = self.match_color_text.state_toggle                                      # NO               
            self.legend_color_title = self.color_text.get_color()                                                   # NO   
            self.legend_show_background = self.show_legend_background.state_toggle                                  # done                   
            self.legend_color_background = self.legend_bg_color.get_color()                                         # done           

            self.legend_transparent = self.transparent_background.state_toggle
            self.legend_blur_strenght = float(self.blur_strenght.get_text()) * self.scale_factor_viewport

            if self.legend_draw_icogram:
                self.icon_size_pixel = 150 * self.scale_factor_viewport
            else:
                self.icon_size_pixel = 0

            legend_position = [self.max_plot_square[0] + self.max_plot_square[2] * self.legend_position[0], self.max_plot_square[1] + self.max_plot_square[3] * self.legend_position[1]]

            # legenda testo
            if self.legend_match_color_title:
                self.labels[4].change_text("".join([f'\\#{MateUtils.rgb2hex(plot.function_color if plot.function else plot.scatter_color)}{{{plot.nome}}}\n' for plot, status in zip(self.plots, self.scroll_plots.ele_mask) if status])[:-1])
            else:
                self.labels[4].color_text = self.legend_color_title
                self.labels[4].change_text("".join([f'{plot.nome}\n' for plot, status in zip(self.plots, self.scroll_plots.ele_mask) if status])[:-1])

            self.labels[4].anchor = "cc"

            new_dim_legend = self.font_size_legend.get_text()
            
            self.labels[4].change_font_size(float(new_dim_legend) * self.scale_factor_viewport)

            self.labels[4].recalc_geometry(f"{legend_position[0]}", f"{legend_position[1]}", anchor_point="cc")

            offset_icona = self.labels[4].h / len([1 for status in self.scroll_plots.ele_mask if status])
            plot_attivo_analizzato = 0

            inizio_legenda = self.labels[4].h * 0.15


            leg_lar, leg_lar_2 = self.labels[4].w + 24 * self.scale_factor_viewport, (self.labels[4].w + 24 * self.scale_factor_viewport) / 2
            leg_alt, leg_alt_2 = self.labels[4].h * 1.3, self.labels[4].h * 1.3 / 2

            if self.legend_transparent:
                pixel_array = self.screen._extract_pixel_values(legend_position[0] - leg_lar_2 - self.icon_size_pixel, legend_position[1] - leg_alt_2, leg_lar + self.icon_size_pixel, leg_alt)

                if not self.legend_show_background:
                    superficie_alpha = self.screen._generate_surface(pixel_array)
                    
            
                else:

                    pixel_array = gaussian_filter(pixel_array, sigma=(self.legend_blur_strenght, self.legend_blur_strenght, 0))
                    pixel_array = pixel_array.astype(np.float64)
                    pixel_array[:, :, 0] = pixel_array[:, :, 0] * self.legend_color_background[0] / 255
                    pixel_array[:, :, 1] = pixel_array[:, :, 1] * self.legend_color_background[1] / 255
                    pixel_array[:, :, 2] = pixel_array[:, :, 2] * self.legend_color_background[2] / 255
                
                    superficie_alpha = self.screen._generate_surface(pixel_array)

            elif not self.legend_transparent and self.legend_show_background:
                self.screen._add_rectangle([legend_position[0] - leg_lar_2 - self.icon_size_pixel, legend_position[1] - leg_alt_2, leg_lar + self.icon_size_pixel, leg_alt], self.legend_color_background)


            if self.legend_transparent:
                if self.legend_draw_icogram:
            
                    # CASO TRASPARENTE
                    for plot, status in zip(self.plots, self.scroll_plots.ele_mask):
                        if status:
                            if plot.function:
                                if plot.dashed:
                                    for i in range(5):
                                        colore_tratteggiato = plot.function_color if i % 2 == 0 else self.plot_area_color.get_color()
                                        self.screen._add_line_static(superficie_alpha, [
                                            [self.icon_size_pixel * 3 / 4 - self.icon_size_pixel * 0.125 * (i + 1), inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato], 
                                            [self.icon_size_pixel * 3 / 4 - self.icon_size_pixel * 0.125 * i , inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato]
                                        ], colore_tratteggiato, plot.function_width * self.scale_factor_viewport)
                                else:
                                    self.screen._add_line_static(superficie_alpha, [
                                        [self.icon_size_pixel * 3 / 4, inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato], 
                                        [self.icon_size_pixel / 8 , inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato]
                                    ], plot.function_color, plot.function_width * self.scale_factor_viewport)

                            if plot.errorbar:
                                    self.screen._add_line_static(superficie_alpha, [
                                        [self.icon_size_pixel / 2 - self.icon_size_pixel * 0.0625, inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato + offset_icona / 3], 
                                        [self.icon_size_pixel / 2 - self.icon_size_pixel * 0.0625, inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato - offset_icona / 3]
                                    ], plot.function_color, plot.function_width * self.scale_factor_viewport)
                                    
                                    self.screen._add_line_static(superficie_alpha, [
                                        [self.icon_size_pixel / 2 - self.icon_size_pixel * 0.0625 - 7 * self.scale_factor_viewport, inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato + offset_icona / 3], 
                                        [self.icon_size_pixel / 2 - self.icon_size_pixel * 0.0625 + 7 * self.scale_factor_viewport, inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato + offset_icona / 3]
                                    ], plot.function_color, plot.function_width * self.scale_factor_viewport)

                                    self.screen._add_line_static(superficie_alpha, [
                                        [self.icon_size_pixel / 2 - self.icon_size_pixel * 0.0625 - 7 * self.scale_factor_viewport, inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato - offset_icona / 3], 
                                        [self.icon_size_pixel / 2 - self.icon_size_pixel * 0.0625 + 7 * self.scale_factor_viewport, inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato - offset_icona / 3]
                                    ], plot.function_color, plot.function_width * self.scale_factor_viewport)


                            if plot.scatter:
                                self.screen._add_points_static(superficie_alpha, [
                                    [self.icon_size_pixel / 2 - self.icon_size_pixel * 0.0625, inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato]
                                ], plot.scatter_color, plot.scatter_width * self.scale_factor_viewport)


                            plot_attivo_analizzato += 1

                self.labels[4].disegnami(logica, 0, superficie_alpha, -self.labels[4].x + self.icon_size_pixel, -self.labels[4].y + self.labels[4].h * 0.15)

                self.screen._blit_surface(superficie_alpha, [legend_position[0] - leg_lar_2 - self.icon_size_pixel, legend_position[1] - leg_alt_2])
                    
            else:
                
                if self.legend_draw_icogram:

                    # CASO NON TRASPARENTE
                    
                    for plot, status in zip(self.plots, self.scroll_plots.ele_mask):
                        if status:
                            if plot.function:
                                if plot.dashed:
                                    for i in range(5):
                                        colore_tratteggiato = plot.function_color if i % 2 == 0 else self.legend_color_background
                                        self.screen._add_line([
                                            [legend_position[0] - leg_lar_2 - self.icon_size_pixel + self.icon_size_pixel * 3 / 4 - self.icon_size_pixel * 0.125 * (i + 1), legend_position[1] - leg_alt_2 + inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato], 
                                            [legend_position[0] - leg_lar_2 - self.icon_size_pixel + self.icon_size_pixel * 3 / 4 - self.icon_size_pixel * 0.125 * i , legend_position[1] - leg_alt_2 + inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato]
                                        ], colore_tratteggiato, plot.function_width * self.scale_factor_viewport)
                                else:
                                    self.screen._add_line([
                                        [legend_position[0] - leg_lar_2 - self.icon_size_pixel + self.icon_size_pixel * 3 / 4, legend_position[1] - leg_alt_2 + inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato], 
                                        [legend_position[0] - leg_lar_2 - self.icon_size_pixel + self.icon_size_pixel / 8 , legend_position[1] - leg_alt_2 + inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato]
                                    ], plot.function_color, plot.function_width * self.scale_factor_viewport)

                            if plot.errorbar:
                                    self.screen._add_line([
                                        [legend_position[0] - leg_lar_2 - self.icon_size_pixel + self.icon_size_pixel / 2 - self.icon_size_pixel * 0.0625, legend_position[1] - leg_alt_2 + inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato + offset_icona / 3], 
                                        [legend_position[0] - leg_lar_2 - self.icon_size_pixel + self.icon_size_pixel / 2 - self.icon_size_pixel * 0.0625, legend_position[1] - leg_alt_2 + inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato - offset_icona / 3]
                                    ], plot.function_color, plot.function_width * self.scale_factor_viewport)
                                    
                                    self.screen._add_line([
                                        [legend_position[0] - leg_lar_2 - self.icon_size_pixel + self.icon_size_pixel / 2 - self.icon_size_pixel * 0.0625 - 7 * self.scale_factor_viewport, legend_position[1] - leg_alt_2 + inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato + offset_icona / 3], 
                                        [legend_position[0] - leg_lar_2 - self.icon_size_pixel + self.icon_size_pixel / 2 - self.icon_size_pixel * 0.0625 + 7 * self.scale_factor_viewport, legend_position[1] - leg_alt_2 + inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato + offset_icona / 3]
                                    ], plot.function_color, plot.function_width * self.scale_factor_viewport)

                                    self.screen._add_line([
                                        [legend_position[0] - leg_lar_2 - self.icon_size_pixel + self.icon_size_pixel / 2 - self.icon_size_pixel * 0.0625 - 7 * self.scale_factor_viewport, legend_position[1] - leg_alt_2 + inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato - offset_icona / 3], 
                                        [legend_position[0] - leg_lar_2 - self.icon_size_pixel + self.icon_size_pixel / 2 - self.icon_size_pixel * 0.0625 + 7 * self.scale_factor_viewport, legend_position[1] - leg_alt_2 + inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato - offset_icona / 3]
                                    ], plot.function_color, plot.function_width * self.scale_factor_viewport)


                            if plot.scatter:
                                self.screen._add_points([
                                    [legend_position[0] - leg_lar_2 - self.icon_size_pixel + self.icon_size_pixel / 2 - self.icon_size_pixel * 0.0625, legend_position[1] - leg_alt_2 + inizio_legenda + offset_icona / 2 + offset_icona * plot_attivo_analizzato],
                                ], plot.scatter_color, plot.scatter_width * self.scale_factor_viewport)


                            plot_attivo_analizzato += 1

                self.labels[4].disegnami(logica, 0, self.screen.tavolozza, 0, 0)
            

    def _disegna_labels(self, logica: 'Logica'):

        if not self.active_plot is None:
            self.active_plot.scatter_width = int(self.scatter_size.get_text())
            self.active_plot.function_width = int(self.function_size.get_text())
            self.active_plot.dashed_traits = int(self.dashed_density.get_text())
            self.active_plot.scatter = self.scatter_toggle.state_toggle
            self.active_plot.dashed = self.dashed_toggle.state_toggle
            self.active_plot.errorbar = self.error_bar.state_toggle
            self.active_plot.function = self.function_toggle.state_toggle
            self.active_plot.function_color = self.colore_function.get_color()
            self.active_plot.scatter_color = self.colore_scatter.get_color()
            self.active_plot.nome = self.plot_name.get_text()

        new_dim_title = self.font_size_title.get_text()
        new_dim_x = self.font_size_label_x.get_text()
        new_dim_y = self.font_size_label_y.get_text()
        
        self.labels[0].change_font_size(float(new_dim_title) * self.scale_factor_viewport)
        self.labels[1].change_font_size(float(new_dim_x) * self.scale_factor_viewport)
        self.labels[2].change_font_size(float(new_dim_y) * self.scale_factor_viewport)

        # titolo
        self.labels[0].change_text(f"{self.text_title.get_text()}")
        self.labels[0].recalc_geometry(f"{self.screen.x + self.max_plot_square[0] + self.max_plot_square[2] / 2}", f"{self.screen.y + self.max_plot_square[1] / 2}", anchor_point="cc")
        self.labels[0].color_text = self.label_title_color.get_color()
        self.labels[0].disegnami(logica, 0, self.screen.tavolozza, DANG_offset_x=-self.screen.x, DANG_offset_y=-self.screen.y)
        
        # X label
        self.labels[1].change_text(f"{self.text_label_x.get_text()}")
        self.labels[1].recalc_geometry(f"{self.screen.x + self.max_plot_square[0] + self.max_plot_square[2] / 2}", f"{self.screen.y + self.max_plot_square[3] + 2 * self.max_plot_square[1]}", anchor_point="cd")
        self.labels[1].color_text = self.label_x_color.get_color()
        self.labels[1].disegnami(logica, 0, self.screen.tavolozza, DANG_offset_x=-self.screen.x, DANG_offset_y=-self.screen.y)
        
        # Y label
        self.labels[2].change_text(f"{self.text_label_y.get_text()}")
        self.labels[2].recalc_geometry(f"{self.screen.x + self.max_canvas_square[0]}", f"{self.screen.y + self.max_plot_square[1] + self.max_plot_square[3] / 2 - self.labels[2].len_testo_diplayed / 2}", anchor_point="lu")
        self.labels[2].color_text = self.label_y_color.get_color()
        self.labels[2].disegnami(logica, 90, self.screen.tavolozza, DANG_offset_x=-self.screen.x, DANG_offset_y=-self.screen.y)


    def _get_nice_ticks(self):

        ticks_x = self._find_optimal_ticks([self.spazio_coordinate_native[0], self.spazio_coordinate_native[2]])
        ticks_y = self._find_optimal_ticks([self.spazio_coordinate_native[1], self.spazio_coordinate_native[3]])

        self.coords_of_ticks = [ticks_x, ticks_y]
        self.value_of_ticks = [ticks_x, ticks_y]


    def _disegna_ticks(self):

        coords = self._get_plot_area_coord()

        formattatore_x = "e" if self.formatting_x.state_toggle else "f"
        formattatore_y = "e" if self.formatting_y.state_toggle else "f"

        self.offset_x_tick_value: int = (self.pixel_len_subdivisions + 7) * self.scale_factor_viewport
        self.offset_y_tick_value: int = (self.pixel_len_subdivisions + 25) * self.scale_factor_viewport

        labels_info_text = []
        labels_info_pos = []
        labels_info_anchor = []
        labels_info_color = []
        labels_info_rotation = []

        for index, coord in enumerate(self.coords_of_ticks[0]):
            if self.show_grid_x.state_toggle:
                self.screen._add_line([[coord, coords[3]], [coord, coords[1]]], self.ax_color_x.get_color(), self.scale_factor_viewport)
            self.screen._add_line([[coord, coords[3]], [coord, coords[3] + self.pixel_len_subdivisions * self.scale_factor_viewport]], self.ax_color_x.get_color(), 4 * self.scale_factor_viewport)

            labels_info_text.append(f"{self.value_of_ticks[0][index]:.{self.round_ticks_x.get_text()}{formattatore_x}}")
            labels_info_pos.append([coord, coords[3] + self.offset_y_label + self.offset_y_tick_value])
            labels_info_anchor.append("cc")
            labels_info_color.append(self.tick_color_x.get_color())
            labels_info_rotation.append(0)


        for index, coord in enumerate(self.coords_of_ticks[1]):
            if self.show_grid_y.state_toggle:
                self.screen._add_line([[coords[0], coord], [coords[2], coord]], self.ax_color_y.get_color(), self.scale_factor_viewport)
            self.screen._add_line([[coords[0], coord], [coords[0] - self.pixel_len_subdivisions * self.scale_factor_viewport, coord]], self.ax_color_y.get_color(), 4 * self.scale_factor_viewport)

            labels_info_text.append(f"{self.value_of_ticks[1][index]:.{self.round_ticks_y.get_text()}{formattatore_y}}")
            labels_info_pos.append([coords[0] - self.offset_x_label - self.offset_x_tick_value, coord])
            labels_info_anchor.append("rc")
            labels_info_color.append(self.tick_color_y.get_color())
            labels_info_rotation.append(0)

        # disegno il valore corrispondente
        self.screen._add_text(labels_info_text, labels_info_pos, anchor=labels_info_anchor, size=1.5 * self.scale_factor_viewport, color=labels_info_color, rotation=labels_info_rotation)


    def _disegna_assi(self):

        coords = self._get_plot_area_coord()

        if self.draw_bounding_box:
            self.screen._add_line([[self.max_plot_square[0], self.max_plot_square[1]], [self.max_plot_square[0] + self.max_plot_square[2], self.max_plot_square[1]]], self.ax_color_x.get_color(), 4 * self.scale_factor_viewport)
            self.screen._add_line([[self.max_plot_square[0] + self.max_plot_square[2], self.max_plot_square[1]], [self.max_plot_square[0] + self.max_plot_square[2], self.max_plot_square[1] + self.max_plot_square[3]]], self.ax_color_x.get_color(), 4 * self.scale_factor_viewport)

        # si posizione sull'area del plot e setta un offset pari a self.offset_x_label o self.offset_y_label
        self.screen._add_line([[coords[0] - self.offset_x_label, coords[1]], [coords[0] - self.offset_x_label, coords[3]]], self.ax_color_y.get_color(), 4 * self.scale_factor_viewport)
        self.screen._add_line([[coords[0], coords[3] + self.offset_y_label], [coords[2], coords[3] + self.offset_y_label]], self.ax_color_x.get_color(), 4 * self.scale_factor_viewport)
    
                    
    def _disegna_dati(self):
        # preparazione dati
        self._normalize_data2screen()

        larg_error = self.max_plot_square[2] / 100

        for plot, status in zip(self.plots, self.scroll_plots.ele_mask):
            # disegno i dati se plot acceso
            if status:

                cond1 = plot.data2plot[:, :2][:, 0] >= self.max_plot_square[0] + self.max_plot_square[2] * (self.minimal_offset_data_x - 0.005)
                cond2 = plot.data2plot[:, :2][:, 1] >= self.max_plot_square[1] + self.max_plot_square[3] * (self.minimal_offset_data_y - 0.005)
                cond3 = plot.data2plot[:, :2][:, 0] <=  self.max_plot_square[0] + self.max_plot_square[2] * (1 - self.minimal_offset_data_x + 0.005)
                cond4 = plot.data2plot[:, :2][:, 1] <=  self.max_plot_square[1] + self.max_plot_square[3] * (1 - self.minimal_offset_data_y + 0.005)

                # Combine all conditions with logical AND
                combined_condition = cond1 & cond2 & cond3 & cond4

                extracted = plot.data2plot[combined_condition]

                if plot.function:
    
                    if plot.dashed:
                        self._disegna_spezzata_tratteggiata(plot)
                    else:
                        self.screen._add_lines(extracted[:, :2], plot.function_color, plot.function_width * self.scale_factor_viewport)
    
                if plot.errorbar and plot.data.shape[1] > 2:

                    for x, y, e in zip(extracted[:, 0], extracted[:, 1], extracted[:, 2]):
                        self.screen._add_line([[x, y], [x, y + e]], plot.function_color, plot.function_width * self.scale_factor_viewport)
                        self.screen._add_line([[x, y], [x, y - e]], plot.function_color, plot.function_width * self.scale_factor_viewport)
                        self.screen._add_line([[x - larg_error, y + e], [x + larg_error, y + e]], plot.function_color, plot.function_width * self.scale_factor_viewport)
                        self.screen._add_line([[x - larg_error, y - e], [x + larg_error, y - e]], plot.function_color, plot.function_width * self.scale_factor_viewport)
                        
                if plot.scatter:
                    self.screen._add_points(extracted[:, :2], plot.scatter_color, plot.scatter_width * self.scale_factor_viewport)


    def _disegna_spezzata_tratteggiata(self, plot:'_Single1DPlot'):

        cond1 = plot.data2plot[:, :2][:, 0] >= self.max_plot_square[0] + self.max_plot_square[2] * (self.minimal_offset_data_x - 0.005)
        cond2 = plot.data2plot[:, :2][:, 1] >= self.max_plot_square[1] + self.max_plot_square[3] * (self.minimal_offset_data_y - 0.005)
        cond3 = plot.data2plot[:, :2][:, 0] <=  self.max_plot_square[0] + self.max_plot_square[2] * (1 - self.minimal_offset_data_x + 0.005)
        cond4 = plot.data2plot[:, :2][:, 1] <=  self.max_plot_square[1] + self.max_plot_square[3] * (1 - self.minimal_offset_data_y + 0.005)

        # Combine all conditions with logical AND
        combined_condition = cond1 & cond2 & cond3 & cond4

        extracted = plot.data2plot[combined_condition]

        lunghezze_parziali = extracted[:-1, :2] - extracted[1:, :2]
        lunghezze_parziali = np.linalg.norm(lunghezze_parziali, axis=1)
        lunghezza_totale = np.sum(lunghezze_parziali)
        
        subdivisions = plot.dashed_traits
        subdivisions_len = lunghezza_totale / subdivisions

        percorso = 0

        for p1, p2 in zip(extracted[:-1, :2], extracted[1:, :2]):
    
            new_point = p1
            iters = 0

            versore = np.array(p2) - np.array(p1)
            versore /= np.linalg.norm(versore)

            starting_color = not (percorso // subdivisions_len) % 2 == 0

            while 1:

                if not (new_point[0] != p2[0] and iters < subdivisions):
                    # print(f"WHILE DEBUG: {new_module}")
                    break

                iters += 1

                new_module = subdivisions_len - percorso % subdivisions_len 

                if new_module < 0.01:
                    new_module = subdivisions_len 


                new_point = p1 + versore * new_module
                
                if new_point[0] >= p2[0]:
                    
                    delta_x = np.array(p2) - np.array(p1)
                    delta_x = np.linalg.norm(delta_x)
                    percorso +=  delta_x
                    new_point = p2

                else:
                    percorso += new_module

                if (iters + starting_color) % 2 == 0:
                    colore = self.plot_area_color.get_color()

                else:
                    colore = plot.function_color
                    
                self.screen._add_line([p1, new_point], colore, plot.function_width* self.scale_factor_viewport)

                p1 = new_point                


    def _disegna_bg(self):
        # setu-up canvas
        self.screen._clear_canvas(self.unused_area_color)
        # disegno area di plot BG
        self.screen.tavolozza.fill(self.canvas_area_color.get_color())
        self.screen._add_rectangle(self.max_plot_square, self.plot_area_color.get_color())
        

    def _normalize_data2screen(self, invert_y_coord=True):
        """Normalizes the data to the screen size"""
        
        # ricerca dell'area di disegno
        self._find_max_square()
        self._get_native_data_bounds()


        for plot, status in zip(self.plots, self.scroll_plots.ele_mask):
            # copia dei dati per trasformarle in screen coordinates
            if status:
                plot.data2plot = plot.data.copy()

                # set dello 0
                plot.data2plot[:, 0] -= self.spazio_coordinate_native[0]
                # normalizzazione
                plot.data2plot[:, 0] /= self.spazio_coordinate_native[2]
                # adatto alla dimensione dell'area del plot
                plot.data2plot[:, 0] *= (self.max_plot_square[2])
                # traslo in base all'offset all'interno dell'area del plot
                plot.data2plot[:, 0] += (self.max_canvas_square[2] * float(self.x_plot_area.get_text()))
                # traslo in base all'offset dell'area del plot nello schermo
                plot.data2plot[:, 0] += self.max_canvas_square[0]
                
                # stessa cosa ma per l'asse y
                plot.data2plot[:, 1] -= self.spazio_coordinate_native[1]
                plot.data2plot[:, 1] /= self.spazio_coordinate_native[3]
                plot.data2plot[:, 1] *= (self.max_plot_square[3])
                
                # inverto i dati per avere le Y che aumentano salendo sullo schermo
                if invert_y_coord:
                    plot.data2plot[:, 1] = self.max_canvas_square[3] * float(self.h_plot_area.get_text()) - plot.data2plot[:, 1]
                
                plot.data2plot[:, 1] += (self.max_canvas_square[3] * float(self.y_plot_area.get_text()))
                plot.data2plot[:, 1] += self.max_canvas_square[1]
                
                # stessa cosa ma per errori y
                if plot.data.shape[1] > 2:
                    plot.data2plot[:, 2] /= self.spazio_coordinate_native[3]
                    plot.data2plot[:, 2] *= (self.max_plot_square[3])


        # ticks x
        self.coords_of_ticks[0] -= self.spazio_coordinate_native[0]
        self.coords_of_ticks[0] /= (self.spazio_coordinate_native[2] + 1e-6)
        self.coords_of_ticks[0] *= (self.max_plot_square[2])
        self.coords_of_ticks[0] += (self.max_canvas_square[2] * float(self.x_plot_area.get_text()))
        self.coords_of_ticks[0] += self.max_canvas_square[0]

        # ticks y
        self.coords_of_ticks[1] -= self.spazio_coordinate_native[1]
        self.coords_of_ticks[1] /= (self.spazio_coordinate_native[3] + 1e-6)
        self.coords_of_ticks[1] *= (self.max_plot_square[3])        
        if invert_y_coord:
            self.coords_of_ticks[1] = self.max_canvas_square[3] * float(self.h_plot_area.get_text()) - self.coords_of_ticks[1]
        self.coords_of_ticks[1] += (self.max_canvas_square[3] * float(self.y_plot_area.get_text()))
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
        
        ris = [round(new_start + self.nice_values[indice_valore] * power_per_tick[indice_tick] * i, 12) for i in range(0, indice_tick + self.min_ticks + 2)]
            
        # decido se tenere l'ultimo elemento
        while len(ris) > 3 and abs(start_values[-1] - ris[-1]) > abs(start_values[-1] - ris[-2]):
            _ = ris.pop()
            # print(f"DEBUG: eliminato il punto {_} perchè troppo lontano, {start_values}")

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
                    self.max_canvas_square[0] + self.max_canvas_square[2] * float(self.x_plot_area.get_text()),
                    self.max_canvas_square[1] + self.max_canvas_square[3] * float(self.y_plot_area.get_text()),
                    self.max_canvas_square[2] * float(self.w_plot_area.get_text()),
                    self.max_canvas_square[3] * float(self.h_plot_area.get_text()),
                ])


            else:
                # area del plot coincide con lo schermo
                self.max_canvas_square = np.array([0, 0, self.screen.w, self.screen.h])
                self.max_plot_square = np.array([
                    self.max_canvas_square[2] * float(self.x_plot_area.get_text()),
                    self.max_canvas_square[3] * float(self.y_plot_area.get_text()),
                    self.max_canvas_square[2] * float(self.w_plot_area.get_text()),
                    self.max_canvas_square[3] * float(self.h_plot_area.get_text()),
                ])



    def _get_plot_area_coord(self):
        return (
            self.max_canvas_square[0] + self.max_canvas_square[2] * float(self.x_plot_area.get_text()),
            self.max_canvas_square[1] + self.max_canvas_square[3] * float(self.y_plot_area.get_text()),
            self.max_canvas_square[0] + self.max_canvas_square[2] * (float(self.x_plot_area.get_text()) + float(self.w_plot_area.get_text())),
            self.max_canvas_square[1] + self.max_canvas_square[3] * (float(self.y_plot_area.get_text()) + float(self.h_plot_area.get_text())),
        )



    def _get_native_data_bounds(self):
        self.spazio_coordinate_native = np.array([np.inf, np.inf, -np.inf, -np.inf])
        
        at_least_one = False
        for plot, status in zip(self.plots, self.scroll_plots.ele_mask):
            if status:
                at_least_one = True

                if plot.errorbar and plot.data.shape[1] > 2:

                    # trova le coordinate minime tra tutti i grafici + errori
                    self.spazio_coordinate_native[0] = np.minimum(self.spazio_coordinate_native[0], np.min(plot.data[:, 0]))
                    self.spazio_coordinate_native[1] = np.minimum(self.spazio_coordinate_native[1], np.min(plot.data[:, 1] - plot.data[:, 2]))
                    self.spazio_coordinate_native[2] = np.maximum(self.spazio_coordinate_native[2], np.max(plot.data[:, 0]))
                    self.spazio_coordinate_native[3] = np.maximum(self.spazio_coordinate_native[3], np.max(plot.data[:, 1] + plot.data[:, 2]))

                else:
                    # trova le coordinate minime tra tutti i grafici
                    self.spazio_coordinate_native[0] = np.minimum(self.spazio_coordinate_native[0], np.min(plot.data[:, 0]))
                    self.spazio_coordinate_native[1] = np.minimum(self.spazio_coordinate_native[1], np.min(plot.data[:, 1]))
                    self.spazio_coordinate_native[2] = np.maximum(self.spazio_coordinate_native[2], np.max(plot.data[:, 0]))
                    self.spazio_coordinate_native[3] = np.maximum(self.spazio_coordinate_native[3], np.max(plot.data[:, 1]))

        # ottengo i ticks belli
        if at_least_one:
            self._get_nice_ticks()

            # trova le coordinate minime tra tutti i grafici + ticks
            self.spazio_coordinate_native[0] = np.minimum(self.spazio_coordinate_native[0], np.min(self.coords_of_ticks[0]))
            self.spazio_coordinate_native[1] = np.minimum(self.spazio_coordinate_native[1], np.min(self.coords_of_ticks[1]))
            self.spazio_coordinate_native[2] = np.maximum(self.spazio_coordinate_native[2], np.max(self.coords_of_ticks[0]))
            self.spazio_coordinate_native[3] = np.maximum(self.spazio_coordinate_native[3], np.max(self.coords_of_ticks[1]))

        else:
            self.spazio_coordinate_native = np.array([0., 0., 1., 1.])

        swap_0 = self.spazio_coordinate_native[0] + (self.spazio_coordinate_native[2] - self.spazio_coordinate_native[0]) * self.zoom_boundaries[0]
        swap_1 = self.spazio_coordinate_native[1] + (self.spazio_coordinate_native[3] - self.spazio_coordinate_native[1]) * self.zoom_boundaries[1]
        swap_2 = self.spazio_coordinate_native[0] + (self.spazio_coordinate_native[2] - self.spazio_coordinate_native[0]) * self.zoom_boundaries[2]
        swap_3 = self.spazio_coordinate_native[1] + (self.spazio_coordinate_native[3] - self.spazio_coordinate_native[1]) * self.zoom_boundaries[3]

        self.spazio_coordinate_native[0] = swap_0
        self.spazio_coordinate_native[1] = swap_1
        self.spazio_coordinate_native[2] = swap_2
        self.spazio_coordinate_native[3] = swap_3

        if at_least_one and self.zoom_boundaries[0] != 0 and self.zoom_boundaries[1] != 0 and self.zoom_boundaries[2] != 1 and self.zoom_boundaries[3] != 1:
            self._get_nice_ticks()

            try:

                fix = 1
                while fix:
                    if self.coords_of_ticks[0][0] < self.spazio_coordinate_native[0]:
                        _ = self.coords_of_ticks[0].pop(0)
                    else:
                        fix = 0
            
                fix = 1
                while fix:
                    if self.coords_of_ticks[0][-1] > self.spazio_coordinate_native[2]:
                        _ = self.coords_of_ticks[0].pop()
                    else:
                        fix = 0

                fix = 1
                while fix:
                    if self.coords_of_ticks[1][0] < self.spazio_coordinate_native[1]:
                        _ = self.coords_of_ticks[1].pop(0)
                    else:
                        fix = 0
            
                fix = 1
                while fix:
                    if self.coords_of_ticks[1][-1] > self.spazio_coordinate_native[3]:
                        _ = self.coords_of_ticks[1].pop()
                    else:
                        fix = 0

            except IndexError:
                ...


        # applico lo spostamento dei dati in base all'offset minimo richiesto dagli assi cartesiani
        self.spazio_coordinate_native[0] -= (self.spazio_coordinate_native[2] - self.spazio_coordinate_native[0]) * self.minimal_offset_data_x
        self.spazio_coordinate_native[1] -= (self.spazio_coordinate_native[3] - self.spazio_coordinate_native[1]) * self.minimal_offset_data_y
        self.spazio_coordinate_native[2] += (self.spazio_coordinate_native[2] - self.spazio_coordinate_native[0]) * self.minimal_offset_data_x
        self.spazio_coordinate_native[3] += (self.spazio_coordinate_native[3] - self.spazio_coordinate_native[1]) * self.minimal_offset_data_y

        # modifica il valore della larghezza e altezza non come coordinate assolute, ma come relative al vertice iniziale
        self.spazio_coordinate_native[2] -= self.spazio_coordinate_native[0]
        self.spazio_coordinate_native[3] -= self.spazio_coordinate_native[1]


    def import_plot_data(self, path: str, divisore: str = None) -> None:
        
        """Importa un tipo di file e genera un plot con le X, Y e gli errori sulle Y (raccoglie rispettivamente le prime 3 colonne)

        Parameters
        ----------
        path : str
            Path al singolo file
        divisore : str, optional
            Divisore delle colonne all'interno del file. Se non specificato, lo cerca di ricavare in autonomia, by default None
        """
        self.data_path = path
        self.divisore = divisore
        
        # SUPPORTO .CSV
        if self.data_path.endswith(".csv"): self.divisore = ","

        # estrazione data
        with open(self.data_path, 'r') as file:
            data = [line for line in file]

        # SUPPORTO FORMATO HEX utf-16-le
        if data[0].startswith(r"ÿþ"): 
            import codecs
            with codecs.open(self.data_path, 'r', encoding='utf-16-le') as file:
                data = [line.strip() for line in file]

        data = [i.split(self.divisore) for i in data]

        # controllo dati indesiderati
        for coordinate in data:
            if "\n" in coordinate:
                coordinate.remove("\n")
    
        # controllo tipologia float dei dati, se non è un float lo carico nel metadata
        metadata_str = ""
        counter_non_metadata = 0
        counter_domanda = True

        for coordinate in data[::-1]:
            for elemento in coordinate:
                try:
                    float(elemento)
                    if counter_domanda:
                        counter_non_metadata += 1
                        if counter_non_metadata > 3:
                            counter_non_metadata = 0
                            counter_domanda = False
                            metadata_str += f"...\n"

                except ValueError:
                    data.remove(coordinate)
                    for _ in coordinate:
                        metadata_str += f"{_}\t"
                    metadata_str += f"\n"
                    counter_domanda = True
                    break
    
        metadata_str += "Metadata / Non converted lines:\n"

        # reverse metadata
        metadata_lst = [f"{i}\n" if f"{i[-1:]}" != "\n" else f"{i}" for i in metadata_str.split("\n")][::-1]
        
        # remove "\n" and "\t\n"
        for _ in range(metadata_lst.count("\n")):
            metadata_lst.remove("\n")
        for _ in range(metadata_lst.count("\t\n")):
            metadata_lst.remove("\t\n")

        # controllo presenza dati None 
        data = [i for i in data if i]
    
        try:
            # CONVERSIONE ARRAY DI FLOATS
            if len(data[0]) != len(data[1]): data.pop(0)
            data = np.array(data).astype(float)    
            
            nome = path.split('\\')[-1]
            nome = nome.split('/')[-1]

            # test ordinamento x
            indici = np.argsort(data[:, 0])
            data = data[indici]

            self.update_plot_list(_Single1DPlot(nome, data, metadata_lst))

        except:
            print(f"Impossibile caricare il file: {path}")


class _Single1DPlot:
    def __init__(self, nome, data, metadata):
        
        self.nome = nome
        self.metadata = metadata

        self.data = data

        self.data2plot: np.ndarray[float] = None

        self.scatter = True
        self.scatter_width = 3
        self.function = True
        self.function_width = 1
        self.dashed = False
        self.dashed_traits = 21
        self.errorbar = True if data.shape[1] > 2 else False

        self.scatter_color = [100, 100, 255]
        self.function_color = [80, 80, 200]


    def __str__(self):
        return f"{self.nome}"
    

    def __repr__(self):
        return f"{self.nome}"