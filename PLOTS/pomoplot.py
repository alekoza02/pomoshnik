import numpy as np
from scipy.ndimage import gaussian_filter 
from MATEMATICA._modulo_mate_utils import MateUtils
from rdkit import Chem
from numba import njit
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from rdkit.Chem import rdChemReactions as Reactions
from rdkit import RDLogger
import os
from scipy.optimize import curve_fit

RDLogger.DisableLog('rdApp.*') 


NON_ESEGUIRE = False

if NON_ESEGUIRE:    
    from GRAFICA._modulo_UI import Logica, UI
    from GRAFICA._modulo_elementi_grafici import Label_Text, Screen, Entrata, Bottone_Toggle, Scroll, ColorPicker, Bottone_Push, RadioButton, Slider

from GRAFICA._modulo_elementi_grafici import Label_Text, Screen

GREEN = "\033[32m"
RED = '\033[31m'
RESET = '\033[0m'

class PomoPlot:
    def __init__(self):
        self.screen: 'Screen' = None

        # ------------------------------------------------------------------------------
        # ZONA GEOMETRIA
        # ------------------------------------------------------------------------------
        # self.plots: list[_Single1DPlot] = [_Single1DPlot(i) for i in ["fase0", "fase1", "fase2", "fase3"]]
        self.plots: list[_Single1DPlot] = []
        self.active_plot: _Single1DPlot = None
        
        self.plots2D: list[_Single2DPlot] = []
        self.active_plot2D: _Single2DPlot = None

        self.molecules: list[Molecule] = []
        self.storico_molecole: int = 0
        self.active_molecule: Molecule = None

        # ricerca il quadrato più grande disponibile all'interno dello schermo
        self.force_screen: bool = True
        # crea le coordinate di quest'area
        self.max_canvas_square: np.ndarray[float] = np.array([0., 0., 0., 0.]) 
        # crea le coordinate dell'area di solo plot
        self.max_plot_square: np.ndarray[float] = np.array([0., 0., 0., 0.]) 
        # crea le coordinate dell'area di solo plot in termini di valori nativi
        self.spazio_coordinate_native: np.ndarray[float] = np.array([-1., -1., 1., 1., -1., 1.]) 
        
        # ------------------------------------------------------------------------------
        # ZONA LABEL
        # ------------------------------------------------------------------------------
        # offset dei label in PIXEL

        self.show_bounding_box: bool = True

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

        self.coords_of_ticks: list[list] = [[], [], []]
        self.min_ticks = 3
        self.max_ticks = 9
        self.nice_values = [1, 2, 2.5, 5, 10]
        
        # contiene Title, label X, label Y, label 2Y, Legenda
        self.labels: list['Label_Text'] = [None, None, None, None, None]
        # ------------------------------------------------------------------------------
        # ZONA COLORI
        # ------------------------------------------------------------------------------
        self.unused_area_color: list[int] = np.array([40, 40, 40]) # FIX unify
        self.zoom_boundaries = np.array([0., 0., 1., 1.])

        self.zero_y = 0
        self.old_SMILE: str = ""

        self.old_pos_x_molecola = None
        self.old_pos_y_molecola = None
        self.old_dimensione_molecola = None

        self.spessore_scala_2Dplot = 5


    def link_ui(self, UI: 'UI'):
        """Richiesta UI pomoshnik, si puù modificare manualmente per adattarla alla propria UI. Serve per intereagire con il grafico"""
        self.scale_factor_viewport = 1

        # NEEDED, GENERATED HERE, NOT IMPORTED
        #############################################################################
        self.labels[0] = Label_Text(x="50%w", y="50%", anchor="cc", w="-*w", h="-*h", latex_font=True, no_parent=True)
        self.labels[1] = Label_Text(x="50%w", y="50%", anchor="cc", w="-*w", h="-*h", latex_font=True, no_parent=True)
        self.labels[2] = Label_Text(x="50%w", y="50%", anchor="cc", w="-*w", h="-*h", latex_font=True, no_parent=True)
        self.labels[3] = Label_Text(x="50%w", y="50%", anchor="cc", w="-*w", h="-*h", latex_font=True, no_parent=True)
        self.labels[4] = Label_Text(x="50%w", y="50%", anchor="cc", w="-*w", h="-*h", latex_font=True, no_parent=True)
        
        # NEEDED, IMPORTED
        self.screen = UI.costruttore.scene["main"].context_menu["main"].elements["viewport"]
        self.screen_render = UI.costruttore.scene["main"].context_menu["main"].elements["renderer"]
        #############################################################################

        self.UI_active_tab: 'RadioButton' = UI.costruttore.scene["main"].context_menu["main"].elements["modes"]

        self.UI_tools: 'RadioButton' = UI.costruttore.scene["main"].context_menu["main"].elements["tools"]
        self.UI_reset_tools: 'Bottone_Push' = UI.costruttore.scene["main"].context_menu["main"].elements["reset_zoom"]

        self.UI_x_plot_area: 'Entrata' = UI.costruttore.scene["main"].context_menu["item1"].elements["x_plot_area"]
        self.UI_y_plot_area: 'Entrata' = UI.costruttore.scene["main"].context_menu["item1"].elements["y_plot_area"]
        self.UI_w_plot_area: 'Entrata' = UI.costruttore.scene["main"].context_menu["item1"].elements["w_plot_area"]
        self.UI_h_plot_area: 'Entrata' = UI.costruttore.scene["main"].context_menu["item1"].elements["h_plot_area"]
        self.UI_size_plot_area: 'Entrata' = UI.costruttore.scene["main"].context_menu["item1"].elements["size_plot_area"]
        self.UI_mantain_proportions: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item1"].elements["mantain_prop"]
        
        self.UI_tema_chiaro: 'Bottone_Push' = UI.costruttore.scene["main"].context_menu["item1"].elements["tema_chiaro"]
        self.UI_tema_scuro: 'Bottone_Push' = UI.costruttore.scene["main"].context_menu["item1"].elements["tema_scuro"]
        
        self.UI_plot_area_color: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item1"].elements["plot_area_bg"]
        self.UI_canvas_area_color: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item1"].elements["canvas_area_bg"]
        
        self.UI_norma_perc: 'RadioButton' = UI.costruttore.scene["main"].context_menu["item1"].elements["norma_perc"]
        self.UI_overlap: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item1"].elements["overlap"]
        

        self.UI_plot_mode: 'RadioButton' = UI.costruttore.scene["main"].context_menu["item1"].elements["plot_mode"]

        self.UI_scroll_plots1D: 'Scroll' = UI.costruttore.scene["main"].context_menu["main"].elements["elenco_plots1D"]
        self.UI_scroll_plots2D: 'Scroll' = UI.costruttore.scene["main"].context_menu["main"].elements["elenco_plots2D"]
        self.UI_elenco_metadata: 'Scroll' = UI.costruttore.scene["main"].context_menu["main"].elements["elenco_metadata"]

        self.UI_plot_name: 'Entrata' = UI.costruttore.scene["main"].context_menu["item2"].elements["plot_name"]
        self.UI_plot_name2D: 'Entrata' = UI.costruttore.scene["main"].context_menu["item2"].elements["plot_name2D"]

        self.UI_spacing_x: 'Entrata' = UI.costruttore.scene["main"].context_menu["item2"].elements["spacing_x"]
        self.UI_spacing_y: 'Entrata' = UI.costruttore.scene["main"].context_menu["item2"].elements["spacing_y"]
        self.UI_colore_base2: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item2"].elements["colore_base2"]
        self.UI_colore_base1: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item2"].elements["colore_base1"]
        self.UI_flip_y: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item2"].elements["flip_y"]
        self.UI_flip_x: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item2"].elements["flip_x"]

        self.UI_scatter_size: 'Entrata' = UI.costruttore.scene["main"].context_menu["item2"].elements["scatter_size"]
        self.UI_scatter_border: 'Entrata' = UI.costruttore.scene["main"].context_menu["item2"].elements["scatter_border"]
        self.UI_function_size: 'Entrata' = UI.costruttore.scene["main"].context_menu["item2"].elements["function_size"]
        self.UI_dashed_density: 'Entrata' = UI.costruttore.scene["main"].context_menu["item2"].elements["dashed_density"]
        
        self.UI_column_x: 'Entrata' = UI.costruttore.scene["main"].context_menu["item2"].elements["column_x"]
        self.UI_column_y: 'Entrata' = UI.costruttore.scene["main"].context_menu["item2"].elements["column_y"]
        self.UI_column_ey: 'Entrata' = UI.costruttore.scene["main"].context_menu["item2"].elements["column_ey"]
        
        self.UI_scatter_toggle: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item2"].elements["scatter_toggle"]
        self.UI_function_toggle: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item2"].elements["function_toggle"]
        self.UI_dashed_toggle: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item2"].elements["dashed"]
        self.UI_error_bar: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item2"].elements["errorbar"]

        self.UI_colore_function: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item2"].elements["colore_function"]
        self.UI_colore_scatter: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item2"].elements["colore_scatter"]
        
        self.UI_gradient: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item2"].elements["gradient"]
        self.UI_grad_mode: 'RadioButton' = UI.costruttore.scene["main"].context_menu["item2"].elements["grad_mode"]

        self.UI_add_second_axis: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item2"].elements["add_second_axis"]
        
        self.UI_font_size_title: 'Entrata' = UI.costruttore.scene["main"].context_menu["item3"].elements["font_size_title"]
        self.UI_font_size_label_x: 'Entrata' = UI.costruttore.scene["main"].context_menu["item3"].elements["font_size_label_x"]
        self.UI_font_size_label_y: 'Entrata' = UI.costruttore.scene["main"].context_menu["item3"].elements["font_size_label_y"]
        self.UI_font_size_label_2y: 'Entrata' = UI.costruttore.scene["main"].context_menu["item3"].elements["font_size_label_2y"]
        
        self.UI_text_title: 'Entrata' = UI.costruttore.scene["main"].context_menu["item3"].elements["text_title"]
        self.UI_text_label_x: 'Entrata' = UI.costruttore.scene["main"].context_menu["item3"].elements["text_label_x"]
        self.UI_text_label_y: 'Entrata' = UI.costruttore.scene["main"].context_menu["item3"].elements["text_label_y"]
        self.UI_text_label_2y: 'Entrata' = UI.costruttore.scene["main"].context_menu["item3"].elements["text_label_2y"]
        self.UI_label_title_color: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item3"].elements["label_title_color"]
        self.UI_label_x_color: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item3"].elements["label_x_color"]
        self.UI_label_y_color: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item3"].elements["label_y_color"]
        self.UI_label_2y_color: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item3"].elements["label_2y_color"]

        self.UI_show_coords_projection: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item3"].elements["show_coords_projection"]
        self.UI_show_coords_value: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item3"].elements["show_coords_value"]

        self.UI_second_y_axis: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item4"].elements["second_y_axis"]
        self.UI_invert_x_axis: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item4"].elements["invert_x_axis"]
        self.UI_round_ticks_x: 'Entrata' = UI.costruttore.scene["main"].context_menu["item4"].elements["round_x"]
        self.UI_round_ticks_y: 'Entrata' = UI.costruttore.scene["main"].context_menu["item4"].elements["round_y"]
        self.UI_round_ticks_2y: 'Entrata' = UI.costruttore.scene["main"].context_menu["item4"].elements["round_2y"]
        
        self.UI_ax_color_x: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item4"].elements["ax_color_x"]
        self.UI_ax_color_y: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item4"].elements["ax_color_y"]
        self.UI_ax_color_2y: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item4"].elements["ax_color_2y"]
        self.UI_tick_color_x: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item4"].elements["tick_color_x"]
        self.UI_tick_color_y: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item4"].elements["tick_color_y"]
        self.UI_tick_color_2y: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item4"].elements["tick_color_2y"]
        
        self.UI_offset_ticks_ax_x: 'Entrata' = UI.costruttore.scene["main"].context_menu["item4"].elements["offset_y_label_x"]
        self.UI_offset_ticks_ax_y: 'Entrata' = UI.costruttore.scene["main"].context_menu["item4"].elements["offset_x_label_y"]
        
        self.UI_size_ticks: 'Entrata' = UI.costruttore.scene["main"].context_menu["item4"].elements["size_ticks"]
        
        self.UI_formatting_x: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item4"].elements["formatting_x"]
        self.UI_formatting_y: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item4"].elements["formatting_y"]
        
        self.UI_show_grid_x: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item4"].elements["show_grid_x"]
        self.UI_show_grid_y: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item4"].elements["show_grid_y"]
        self.UI_show_grid_2y: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item4"].elements["show_grid_2y"]
        self.UI_show_bounding_box: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item4"].elements["show_bounding_box"]
        
        self.UI_show_legend: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item5"].elements["show_legend"]
        self.UI_x_legend: 'Slider' = UI.costruttore.scene["main"].context_menu["item5"].elements["x_legend"]
        self.UI_y_legend: 'Slider' = UI.costruttore.scene["main"].context_menu["item5"].elements["y_legend"]
        self.UI_font_size_legend: 'Entrata' = UI.costruttore.scene["main"].context_menu["item5"].elements["font_size_legend"]
        self.UI_show_legend_background: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item5"].elements["show_legend_background"]
        self.UI_legend_bg_color: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item5"].elements["legend_color_background"]
        self.UI_transparent_background: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item5"].elements["transparent_background"]
        self.UI_blur_strenght: 'Entrata' = UI.costruttore.scene["main"].context_menu["item5"].elements["blur_strenght"]
        self.UI_show_icons: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item5"].elements["show_icons"]
        self.UI_match_color_text: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item5"].elements["match_color_text"]
        self.UI_color_text: 'ColorPicker' = UI.costruttore.scene["main"].context_menu["item5"].elements["color_text"]
        
        self.UI_text_2D_plot: 'Entrata' = UI.costruttore.scene["main"].context_menu["item5"].elements["text_2D_plot"]
        self.UI_size_scale_marker2D: 'Entrata' = UI.costruttore.scene["main"].context_menu["item5"].elements["size_scale_marker2D"]

        self.UI_import_single_plot1D: 'Bottone_Push' = UI.costruttore.scene["main"].context_menu["item6"].elements["import_single_plot1D"]
        self.UI_import_single_plot2D: 'Bottone_Push' = UI.costruttore.scene["main"].context_menu["item6"].elements["import_single_plot2D"]
        self.UI_import_multip_plot1D: 'Bottone_Push' = UI.costruttore.scene["main"].context_menu["item6"].elements["import_multip_plot1D"]
        self.UI_import_multip_plot2D: 'Bottone_Push' = UI.costruttore.scene["main"].context_menu["item6"].elements["import_multip_plot2D"]

        self.UI_save_single_plot: 'Bottone_Push' = UI.costruttore.scene["main"].context_menu["item7"].elements["save_single_plot"]

        self.UI_molecule_input: 'Entrata' = UI.costruttore.scene["main"].context_menu["item11"].elements["molecule_input"]
        self.UI_molecule_preview: 'Screen' = UI.costruttore.scene["main"].context_menu["item11"].elements["molecule_preview"]

        self.UI_add_molecola: 'Bottone_Push' = UI.costruttore.scene["main"].context_menu["item11"].elements["add_molecola"]
        self.UI_pos_x_molecola: 'Entrata' = UI.costruttore.scene["main"].context_menu["item11"].elements["pos_x_molecola"]
        self.UI_pos_y_molecola: 'Entrata' = UI.costruttore.scene["main"].context_menu["item11"].elements["pos_y_molecola"]
        self.UI_dimensione_molecola: 'Entrata' = UI.costruttore.scene["main"].context_menu["item11"].elements["dimensione_molecola"]

        self.UI_compute_derivative: 'Bottone_Push' = UI.costruttore.scene["main"].context_menu["item9"].elements["compute_derivative"]
        self.UI_output_derivative: 'Label_Text' = UI.costruttore.scene["main"].context_menu["item9"].elements["output_derivative"]

        self.UI_compute_interpolation: 'Bottone_Push' = UI.costruttore.scene["main"].context_menu["item9"].elements["compute"]
        self.UI_min_x_interpolation: 'Entrata' = UI.costruttore.scene["main"].context_menu["item9"].elements["min_x"]
        self.UI_max_x_interpolation: 'Entrata' = UI.costruttore.scene["main"].context_menu["item9"].elements["max_x"]
        self.UI_output_interpolation: 'Label_Text' = UI.costruttore.scene["main"].context_menu["item9"].elements["output"]
        self.UI_intersection_interpolation: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item9"].elements["intersection"]

        self.UI_curve_function: 'Entrata' = UI.costruttore.scene["main"].context_menu["item9"].elements["curve_function"]
        self.UI_param_0: 'Entrata' = UI.costruttore.scene["main"].context_menu["item9"].elements["param_0"]
        self.UI_param_1: 'Entrata' = UI.costruttore.scene["main"].context_menu["item9"].elements["param_1"]
        self.UI_param_2: 'Entrata' = UI.costruttore.scene["main"].context_menu["item9"].elements["param_2"]
        self.UI_param_3: 'Entrata' = UI.costruttore.scene["main"].context_menu["item9"].elements["param_3"]
        self.UI_compute_custom_curve: 'Bottone_Push' = UI.costruttore.scene["main"].context_menu["item9"].elements["compute_custom_curve"]
        self.UI_show_guess: 'Bottone_Toggle' = UI.costruttore.scene["main"].context_menu["item9"].elements["show_guess"]

        self.UI_l_param_0: 'Label_Text' = UI.costruttore.scene["main"].context_menu["item9"].elements["l_param_0"]
        self.UI_l_param_1: 'Label_Text' = UI.costruttore.scene["main"].context_menu["item9"].elements["l_param_1"]
        self.UI_l_param_2: 'Label_Text' = UI.costruttore.scene["main"].context_menu["item9"].elements["l_param_2"]
        self.UI_l_param_3: 'Label_Text' = UI.costruttore.scene["main"].context_menu["item9"].elements["l_param_3"]

        self.UI_presets1: 'Bottone_Push' = UI.costruttore.scene["main"].context_menu["item9"].elements["presets1"]
        self.UI_presets2: 'Bottone_Push' = UI.costruttore.scene["main"].context_menu["item9"].elements["presets2"]
        self.UI_presets3: 'Bottone_Push' = UI.costruttore.scene["main"].context_menu["item9"].elements["presets3"]

        self.UI_info3: 'Label_Text' = UI.costruttore.scene["main"].context_menu["item9"].elements["info3"]
    
    
    def update_attributes(self):
        """Richiesta UI pomoshnik, si puù modificare manualmente per adattarla alla propria UI. Serve per intereagire con il grafico"""

        # NO CHANGES PERFORMED ----------------------------------------------------------
        self.norma_perc = self.UI_norma_perc
        self.scroll_plots1D = self.UI_scroll_plots1D
        self.scroll_plots2D = self.UI_scroll_plots2D
        self.elenco_metadata = self.UI_elenco_metadata
        self.import_single_plot1D = self.UI_import_single_plot1D
        self.import_single_plot2D = self.UI_import_single_plot2D
        self.import_multip_plot1D = self.UI_import_multip_plot1D
        self.import_multip_plot2D = self.UI_import_multip_plot2D
        self.save_single_plot = self.UI_save_single_plot
        self.tools = self.UI_tools
        self.grad_mode = self.UI_grad_mode
        self.reset_tools = self.UI_reset_tools                              
        self.molecule_input = self.UI_molecule_input
        self.molecule_preview = self.UI_molecule_preview
        self.add_molecola = self.UI_add_molecola
        self.output_interpolation = self.UI_output_interpolation
        self.output_derivative = self.UI_output_derivative
        self.compute_interpolation = self.UI_compute_interpolation
        self.compute_derivative= self.UI_compute_derivative
        self.compute_custom_curve = self.UI_compute_custom_curve
        self.tema_chiaro = self.UI_tema_chiaro
        self.tema_scuro = self.UI_tema_scuro

        self.l_param_0 = self.UI_l_param_0
        self.l_param_1 = self.UI_l_param_1
        self.l_param_2 = self.UI_l_param_2
        self.l_param_3 = self.UI_l_param_3
        self.info3 = self.UI_info3

        # NO CHANGES PERFORMED ----------------------------------------------------------

        try:
            self.active_tab = [index for index, status in enumerate(self.UI_active_tab.toggles) if status.state_toggle][0]
        except IndexError:
            self.active_tab = -1

        self.x_plot_area = self.UI_x_plot_area.get_text()
        self.y_plot_area = self.UI_y_plot_area.get_text()
        self.w_plot_area = self.UI_w_plot_area.get_text()
        self.h_plot_area = self.UI_h_plot_area.get_text()
        self.size_plot_area = self.UI_size_plot_area.get_text()
        self.plot_area_color = self.UI_plot_area_color.get_color()
        self.canvas_area_color = self.UI_canvas_area_color.get_color()

        self.mantain_proportions = self.UI_mantain_proportions.state_toggle
        
        self.overlap = self.UI_overlap.state_toggle
        
        self.second_y_axis = self.UI_second_y_axis.state_toggle
        self.invert_x_axis = self.UI_invert_x_axis.state_toggle

        self.plot_name = self.UI_plot_name.get_text()
        self.plot_name2D = self.UI_plot_name2D.get_text()
        
        self.column_x = self.UI_column_x.get_text()
        self.column_y = self.UI_column_y.get_text()
        self.column_ey = self.UI_column_ey.get_text()
        
        self.spacing_x = self.UI_spacing_x.get_text()
        self.spacing_y = self.UI_spacing_y.get_text()
        
        self.colore_base1 = self.UI_colore_base1.get_color().astype(np.float64)
        self.colore_base2 = self.UI_colore_base2.get_color().astype(np.float64)
        self.flip_y = self.UI_flip_y.state_toggle
        self.flip_x = self.UI_flip_x.state_toggle

        self.scatter_size = self.UI_scatter_size.get_text()
        self.scatter_border = self.UI_scatter_border.get_text()
        self.function_size = self.UI_function_size.get_text()
        self.dashed_density = self.UI_dashed_density.get_text()
        
        self.scatter_toggle = self.UI_scatter_toggle.state_toggle
        self.function_toggle = self.UI_function_toggle.state_toggle
        self.dashed_toggle = self.UI_dashed_toggle.state_toggle
        self.error_bar = self.UI_error_bar.state_toggle

        self.colore_function = self.UI_colore_function.get_color()
        self.colore_scatter = self.UI_colore_scatter.get_color()
        
        self.gradient = self.UI_gradient.state_toggle

        self.add_second_axis = self.UI_add_second_axis.state_toggle
        
        self.font_size_title = self.UI_font_size_title.get_text()
        self.font_size_label_x = self.UI_font_size_label_x.get_text()
        self.font_size_label_y = self.UI_font_size_label_y.get_text()
        self.font_size_label_2y = self.UI_font_size_label_2y.get_text()
        
        self.text_title = self.UI_text_title.testo
        self.text_label_x = self.UI_text_label_x.testo
        self.text_label_y = self.UI_text_label_y.testo
        self.text_label_2y = self.UI_text_label_2y.testo
        self.label_title_color = self.UI_label_title_color.get_color()
        self.label_x_color = self.UI_label_x_color.get_color()
        self.label_y_color = self.UI_label_y_color.get_color()
        self.label_2y_color = self.UI_label_2y_color.get_color()

        self.offset_ticks_ax_x = self.UI_offset_ticks_ax_x.get_text()
        self.offset_ticks_ax_y = self.UI_offset_ticks_ax_y.get_text()

        self.size_ticks = self.UI_size_ticks.get_text()
        
        self.show_coords_projection = self.UI_show_coords_projection.state_toggle
        self.show_coords_value = self.UI_show_coords_value.state_toggle

        self.round_ticks_x = self.UI_round_ticks_x.get_text()
        self.round_ticks_y = self.UI_round_ticks_y.get_text()
        self.round_ticks_2y = self.UI_round_ticks_2y.get_text()  
        
        self.ax_color_x = self.UI_ax_color_x.get_color()
        self.ax_color_y = self.UI_ax_color_y.get_color()
        self.ax_color_2y = self.UI_ax_color_2y.get_color()
        self.tick_color_x = self.UI_tick_color_x.get_color()
        self.tick_color_y = self.UI_tick_color_y.get_color()
        self.tick_color_2y = self.UI_tick_color_2y.get_color()
        
        self.formatting_x = self.UI_formatting_x.state_toggle
        self.formatting_y = self.UI_formatting_y.state_toggle
        
        self.show_grid_x = self.UI_show_grid_x.state_toggle
        self.show_grid_y = self.UI_show_grid_y.state_toggle
        self.show_grid_2y = self.UI_show_grid_2y.state_toggle
        self.show_bounding_box = self.UI_show_bounding_box.state_toggle
        
        self.show_legend = self.UI_show_legend.state_toggle
        self.x_legend = self.UI_x_legend.get_value()
        self.y_legend = self.UI_y_legend.get_value()
        self.font_size_legend = self.UI_font_size_legend.get_text()
        self.show_legend_background = self.UI_show_legend_background.state_toggle
        self.legend_bg_color = self.UI_legend_bg_color.get_color()
        self.transparent_background = self.UI_transparent_background.state_toggle
        self.blur_strenght = self.UI_blur_strenght.get_text()
        self.show_icons = self.UI_show_icons.state_toggle
        self.match_color_text = self.UI_match_color_text.state_toggle
        self.color_text = self.UI_color_text.get_color()
        self.text_2D_plot = self.UI_text_2D_plot.get_text()
        self.size_scale_marker2D = self.UI_size_scale_marker2D.get_text()

        self.min_x_interpolation = self.UI_min_x_interpolation.get_text()
        self.max_x_interpolation = self.UI_max_x_interpolation.get_text()
        self.intersection_interpolation = self.UI_intersection_interpolation.state_toggle

        self.curve_function = self.UI_curve_function.get_text()
        self.param_0 = self.UI_param_0.get_text()
        self.param_1 = self.UI_param_1.get_text()
        self.param_2 = self.UI_param_2.get_text()
        self.param_3 = self.UI_param_3.get_text()
        self.show_guess = self.UI_show_guess.state_toggle

        self.pos_x_molecola = self.UI_pos_x_molecola.get_text()
        self.pos_y_molecola = self.UI_pos_y_molecola.get_text()        
        self.dimensione_molecola = self.UI_dimensione_molecola.get_text()        


    def update_plot_list(self, added_plot, active_on_load=False, substitute=False):
        

        if type(added_plot) == _Single1DPlot:
            if substitute:
                try:
                    nomi = [plot.nome for plot in self.scroll_plots1D.elementi]
                    where = nomi.index(added_plot.nome)
                    self.scroll_plots1D.remove_item_index(where)
                except ValueError as e:
                    ...
            self.scroll_plots1D.add_element_scroll(added_plot, active_on_load)
        
        elif type(added_plot) == _Single2DPlot:    
            self.scroll_plots2D.add_element_scroll(added_plot, active_on_load)
        

    def update(self, logica: 'Logica'):

        # cambio grafico attivo
        self.plot_mode = [index for index, state in enumerate(self.UI_plot_mode.cb_s) if state][0]

        if self.plot_mode == 0: 
            self.plots = self.scroll_plots1D.elementi
            self.scroll_plots = self.scroll_plots1D
        if self.plot_mode == 1: 
            self.plots = self.scroll_plots2D.elementi
            self.scroll_plots = self.scroll_plots2D
        

        old_active = self.active_plot
        if len(self.plots) > 0:

            self.active_plot: _Single1DPlot = self.plots[self.scroll_plots.ele_selected_index]

            if self.active_plot != old_active:
                
                try:
                    if self.plot_mode == 0:
                        self.UI_scatter_size.change_text(f"{self.active_plot.scatter_width}")
                        self.UI_scatter_border.change_text(f"{self.active_plot.scatter_border}")
                        self.UI_function_size.change_text(f"{self.active_plot.function_width}")
                        self.UI_plot_name.change_text(f"{self.active_plot.nome}")
                        self.UI_column_x.change_text(f"{self.active_plot.column_x}")
                        self.UI_column_y.change_text(f"{self.active_plot.column_y}")
                        self.UI_column_ey.change_text(f"{self.active_plot.column_ey}")
                        self.UI_scatter_toggle.state_toggle = self.active_plot.scatter
                        self.UI_function_toggle.state_toggle = self.active_plot.function
                        self.UI_dashed_toggle.state_toggle = self.active_plot.dashed
                        self.UI_error_bar.state_toggle = self.active_plot.errorbar
                        self.UI_dashed_density.change_text(f"{self.active_plot.dashed_traits}")
                        self.UI_colore_scatter.set_color(self.active_plot.scatter_color)
                        self.UI_colore_function.set_color(self.active_plot.function_color)
                        self.UI_gradient.state_toggle = self.active_plot.gradiente
                        self.UI_add_second_axis.state_toggle = self.active_plot.second_ax
                        
                        grad_status = [0, 0]
                        if self.active_plot.grad_mode == "hori":
                            grad_status[0] = 1
                        elif self.active_plot.grad_mode == "vert":
                            grad_status[1] = 1

                        self.grad_mode.set_state(grad_status)

                        if self.active_plot.data.shape[1] <= 2:
                            self.UI_error_bar.bg = np.array([70, 40, 40])
                        else:
                            self.UI_error_bar.bg = np.array([40, 70, 40])
                    
                    if self.plot_mode == 1:
                        self.UI_plot_name2D.change_text(f"{self.active_plot.nome}")
                        self.UI_colore_base1.change_text(f"{self.active_plot.colore_base1}")
                        self.UI_colore_base2.change_text(f"{self.active_plot.colore_base2}")
                        self.UI_flip_y.state_toggle = self.active_plot.flip_y
                        self.UI_flip_x.state_toggle = self.active_plot.flip_x
                        self.UI_spacing_x.change_text(f"{self.active_plot.spacing_x}")
                        self.UI_spacing_y.change_text(f"{self.active_plot.spacing_y}")
                        
                except Exception as e:
                    print(f"Non sono riuscito ad aggiornare: {e}")

        if not self.active_plot is None:
            if self.plot_mode == 0:
                self.active_plot.scatter_width = int(self.scatter_size)
                self.active_plot.scatter_border = int(self.scatter_border)
                self.active_plot.function_width = int(self.function_size)
                self.active_plot.dashed_traits = int(self.dashed_density)
                self.active_plot.scatter = self.scatter_toggle
                self.active_plot.dashed = self.dashed_toggle
                self.active_plot.errorbar = self.error_bar
                self.active_plot.function = self.function_toggle
                self.active_plot.function_color = self.colore_function
                self.active_plot.scatter_color = self.colore_scatter
                self.active_plot.nome = self.plot_name
                self.active_plot.gradiente = self.gradient
                self.active_plot.second_ax = self.add_second_axis
            
                try:
                    mode_grad = [i for i, ele in enumerate(self.grad_mode.cb_s) if ele][0]
                except IndexError:
                    mode_grad = 0

                match mode_grad:
                    case 0: self.active_plot.grad_mode = "hori"
                    case 1: self.active_plot.grad_mode = "vert"
                
                max_column_size = self.active_plot.data.shape[1]
                
                if int(self.column_x) <= max_column_size:
                    self.active_plot.column_x = int(self.column_x) 
                else: 
                    self.active_plot.column_x = max_column_size
                    self.UI_column_x.change_text(max_column_size)
                
                if int(self.column_y) <= max_column_size:
                    self.active_plot.column_y = int(self.column_y) 
                else: 
                    self.active_plot.column_y = max_column_size
                    self.UI_column_y.change_text(max_column_size)
                
                if int(self.column_ey) <= max_column_size:
                    self.active_plot.column_ey = int(self.column_ey) 
                else: 
                    self.active_plot.column_ey = max_column_size
                    self.UI_column_ey.change_text(max_column_size)


            elif self.plot_mode == 1:
                self.active_plot.nome = self.plot_name2D
                self.active_plot.colore_base1 = self.colore_base1
                self.active_plot.colore_base2 = self.colore_base2
                self.active_plot.flip_y = self.flip_y
                self.active_plot.flip_x = self.flip_x
                self.active_plot.spacing_x = float(self.spacing_x)
                self.active_plot.spacing_y = float(self.spacing_y)



        # import plots
        [self.import_plot_data(path, image=False) for path in self.import_single_plot1D.paths]
        [self.import_plot_data(path, image=True) for path in self.import_single_plot2D.paths]
        [self.import_plot_data(path, image=False) for path in self.import_multip_plot1D.paths]
        [self.import_plot_data(path, image=True) for path in self.import_multip_plot2D.paths]
            
        [self.import_plot_data(path, image=self.plot_mode) for path in logica.dropped_paths] # plot_mode == 0 -> False plot 1D, plot_mode == 1 -> True plot 2D 


        self.import_single_plot1D.paths = []            
        self.import_single_plot2D.paths = []            
        self.import_multip_plot1D.paths = []
        self.import_multip_plot2D.paths = []

        logica.dropped_paths = []

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

            self.screen._save_screenshot(self.save_single_plot.paths[-1])
            self.save_single_plot.paths.pop()
            
            self.scale_factor_viewport = self.scale_factor_backup
            
            self.screen_render = self.screen
            self.screen = self.screen_backup
        
            self.screen_render.hide = True
            self.screen.hide = False


        if not self.screen.bounding_box.collidepoint(logica.mouse_pos) and not self.tools.bounding_box.collidepoint(logica.mouse_pos) and logica.click_sinistro:
            self.tools.set_state([0 for _ in range(self.tools.cb_n)])


        # logica zoom mouse
        if self.tools.cb_s[0] and logica.dragging_finished_FLAG and self.screen.bounding_box.collidepoint(logica.mouse_pos) and logica.original_start_pos[0] != logica.dragging_end_pos[0] and logica.original_start_pos[1] != logica.dragging_end_pos[1] and not self.tools.toggles[0].bounding_box.collidepoint(logica.original_start_pos):
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

            # a bassi framerate potrebbe rompersi generare dati errati la posizione del mouse
            if self.zoom_boundaries[0] < 0: self.zoom_boundaries[0] = 0
            if self.zoom_boundaries[1] < 0: self.zoom_boundaries[1] = 0
            if self.zoom_boundaries[2] > 1: self.zoom_boundaries[2] = 1
            if self.zoom_boundaries[3] > 1: self.zoom_boundaries[3] = 1

        # logica zoom rotella
        if logica.scroll_down and self.screen.bounding_box.collidepoint(logica.mouse_pos):
            self.zoom_boundaries[0] -= logica.scroll_down * (self.zoom_boundaries[2] - self.zoom_boundaries[0]) / 20
            self.zoom_boundaries[1] -= logica.scroll_down * (self.zoom_boundaries[2] - self.zoom_boundaries[0]) / 20
            self.zoom_boundaries[2] += logica.scroll_down * (self.zoom_boundaries[3] - self.zoom_boundaries[1]) / 20
            self.zoom_boundaries[3] += logica.scroll_down * (self.zoom_boundaries[3] - self.zoom_boundaries[1]) / 20
        if logica.scroll_up and self.screen.bounding_box.collidepoint(logica.mouse_pos):
            self.zoom_boundaries[0] += logica.scroll_up * (self.zoom_boundaries[2] - self.zoom_boundaries[0]) / 20
            self.zoom_boundaries[1] += logica.scroll_up * (self.zoom_boundaries[2] - self.zoom_boundaries[0]) / 20
            self.zoom_boundaries[2] -= logica.scroll_up * (self.zoom_boundaries[3] - self.zoom_boundaries[1]) / 20
            self.zoom_boundaries[3] -= logica.scroll_up * (self.zoom_boundaries[3] - self.zoom_boundaries[1]) / 20


        # logica pan
        if self.tools.cb_s[1] and self.screen.bounding_box.collidepoint(logica.mouse_pos) and logica.dragging:
            self.zoom_boundaries[0] -= (self.zoom_boundaries[2] - self.zoom_boundaries[0]) * logica.dragging_dx / self.screen.w
            self.zoom_boundaries[1] -= (self.zoom_boundaries[3] - self.zoom_boundaries[1]) * logica.dragging_dy / self.screen.h
            self.zoom_boundaries[2] -= (self.zoom_boundaries[2] - self.zoom_boundaries[0]) * logica.dragging_dx / self.screen.w
            self.zoom_boundaries[3] -= (self.zoom_boundaries[3] - self.zoom_boundaries[1]) * logica.dragging_dy / self.screen.h


        # logica add coords
        if not self.tools.cb_s[2]:
            self.screen.last_click_pos_changed = False

        if self.tools.cb_s[2] and self.screen.bounding_box.collidepoint(logica.mouse_pos) and self.screen.last_click_pos_changed:
            self.screen.last_click_pos_changed = False

            min_info = [None, None]
            min_value = 1e6
            for index_plot, plot, status in zip(range(len(self.plots)), self.plots, self.scroll_plots.ele_mask):
                
                if status:
                    search = plot.data2plot[:, :2] - [logica.mouse_pos[0] - self.screen.x, logica.mouse_pos[1] - self.screen.y]
                    search = np.linalg.norm(search, axis=1)
                    index = np.argmin(search)
                    value = np.min(search)

                    if value < min_value:
                        
                        min_value = value

                        min_info[0] = index
                        min_info[1] = index_plot


            if self.plots[min_info[1]].display_coords.count(min_info[0]) == 0:
                self.plots[min_info[1]].display_coords.append(min_info[0])
            else:
                self.plots[min_info[1]].display_coords.remove(min_info[0])


        # reset pan & zoom
        if self.reset_tools.flag_foo:
            self.reset_tools.flag_foo = 0
            self.tools.set_state([0 for _ in range(self.tools.cb_n)])
            self.zoom_boundaries = np.array([0., 0., 1., 1.])


        # compute interpolation
        if self.plot_mode == 0 and self.compute_interpolation.flag_foo:
            self.compute_interpolation.flag_foo = False
            self.output_interpolation.change_text(self.linear_interpolation())


        # compute derivative
        if self.plot_mode == 0 and self.compute_derivative.flag_foo:
            self.compute_derivative.flag_foo = False
            self.output_derivative.change_text(self.derivative())


        # compute custom curve
        if self.plot_mode == 0 and self.compute_custom_curve.flag_foo:
            self.compute_custom_curve.flag_foo = False
            ris = self.fit_curve()
            form_x = "e" if self.formatting_x else "f"
            if ris is None:
                return
            
            labels = [self.l_param_0, self.l_param_1, self.l_param_2, self.l_param_3]
            for i in range(len(ris)):
                labels[i].change_text(f"{float(ris[i]):.{self.round_ticks_x}{form_x}}")
                

        if self.UI_presets1.flag_foo:
            self.UI_presets1.flag_foo = False
            self.UI_curve_function.change_text("p[0]+p[1]*np.exp(p[2]+(p[3]*x))")
        if self.UI_presets2.flag_foo:
            self.UI_presets2.flag_foo = False
            self.UI_curve_function.change_text("p[0]*np.exp(-((x-p[1])/p[2])**2/2)")
        if self.UI_presets3.flag_foo:
            self.UI_presets3.flag_foo = False
            self.UI_curve_function.change_text("p[0]+p[1]/(1+np.exp((-x+p[2])/p[3]))")


        # choose mode and hide unecessary UI
        if self.active_tab == 10:
            self.elenco_metadata.hide_plus_children(False)
            self.scroll_plots1D.hide_plus_children(True)
            self.scroll_plots1D.hide_plus_children(True)
        else:
            self.elenco_metadata.hide_plus_children(True)
            self.scroll_plots1D.hide_plus_children(self.plot_mode == 1)
            self.scroll_plots2D.hide_plus_children(self.plot_mode == 0)


        # change attributs due to different plot mode
        self.minimal_offset_data_x = 0.05 if self.plot_mode == 0 else 0.00
        self.minimal_offset_data_y = 0.05 if self.plot_mode == 0 else 0.00 


        # change with default theme light and dark
        if self.UI_tema_scuro.flag_foo:
            self.UI_tema_scuro.flag_foo = False
            self.UI_plot_area_color.set_color([30, 30, 30])
            self.UI_canvas_area_color.set_color([30, 30, 30])
            self.UI_ax_color_x.set_color([70, 70, 70])
            self.UI_ax_color_y.set_color([70, 70, 70])
            self.UI_ax_color_2y.set_color([70, 70, 70])
            self.UI_label_x_color.set_color([255, 255, 255])
            self.UI_label_y_color.set_color([255, 255, 255])
            self.UI_label_2y_color.set_color([255, 255, 255])
            self.UI_label_title_color.set_color([255, 255, 255])
            self.UI_tick_color_x.set_color([255, 255, 255])
            self.UI_tick_color_y.set_color([255, 255, 255])
            self.UI_tick_color_2y.set_color([255, 255, 255])
        
        if self.UI_tema_chiaro.flag_foo:
            self.UI_tema_chiaro.flag_foo = False
            self.UI_plot_area_color.set_color([255, 255, 255])
            self.UI_canvas_area_color.set_color([255, 255, 255])
            self.UI_ax_color_x.set_color([193, 193, 193])
            self.UI_ax_color_y.set_color([193, 193, 193])
            self.UI_ax_color_2y.set_color([193, 193, 193])
            self.UI_label_x_color.set_color([0, 0, 0])
            self.UI_label_y_color.set_color([0, 0, 0])
            self.UI_label_2y_color.set_color([0, 0, 0])
            self.UI_label_title_color.set_color([0, 0, 0])
            self.UI_tick_color_x.set_color([0, 0, 0])
            self.UI_tick_color_y.set_color([0, 0, 0])
            self.UI_tick_color_2y.set_color([0, 0, 0])


    def linear_interpolation(self) -> str:
        """Esegue un'interpolazione linare del grafico attivo in quel momento nel range selezionato. Restituisce un output stringa contenente tutti i dati relativi all'esito

        Returns
        -------
        str
            OUTPUT dell'interpolazione
        """
        try:    
            
            try:
                base_data = self.plots[self.scroll_plots.ele_selected_index]
            except IndexError as e:
                self.compute_interpolation.sound_error.play()
                return f"\\#dc143c{{ATTENZIONE! Carica un grafico prima.}}\n\nRaised error:\n\\i{{{e}}}"

            needed_indices = (base_data.data[:, base_data.column_x] >= MateUtils.inp2flo(self.min_x_interpolation, np.min(base_data.data[:, base_data.column_x]))) & (base_data.data[:, base_data.column_x] <= MateUtils.inp2flo(self.max_x_interpolation, np.max(base_data.data[:, base_data.column_x])))

            x = base_data.data[:, base_data.column_x]
            y = base_data.data[:, base_data.column_y]
            
            ey = base_data.data[:, base_data.column_ey] if base_data.data.shape[1] > 2 else None

            x = x[needed_indices]
            y = y[needed_indices]
            ey = ey[needed_indices] if base_data.data.shape[1] > 2 else None

            if len(x) < 3: 
                self.compute_interpolation.sound_error.play()
                return f"\\#dc143c{{ATTENZIONE! Punti insufficienti.}}\n\nPunti minimi richiesti: \\#ffdd60{{3}}\nPunti presenti nel grafico: \\#ffdd60{{{len(x)}}}"

            m = None
            q = None
            m_e = None
            q_e = None
            correlation = None
            correlation_type = ""

            if ey is None:
                # INIZIO LOGICA INTERPOLAZIONE NON PESATA ----------------------------------------------------------
                coeff, covar = np.polyfit(x, y, deg = 1, cov= True) 
                m, q = coeff
                m_e, q_e = np.sqrt(np.diag(covar))
            else:
                # INIZIO LOGICA INTERPOLAZIONE PESATA ----------------------------------------------------------
                coeff, covar = np.polyfit(x, y, deg = 1, w = 1/ey, cov= True)
                m, q = coeff
                m_e, q_e = np.sqrt(np.diag(covar))
            
            params_str = f"Output interpolazione lineare.\n\\#aaffaa{{{base_data.nome}}}\n\nm: {m:.{self.round_ticks_y}f} \\pm {m_e:.{self.round_ticks_y}f}\nq: {q:.{self.round_ticks_y}f} \\pm {q_e:.{self.round_ticks_y}f}\n"

            # compute interpolation plot
            y_i = np.zeros(len(x))

            for index, arg in enumerate(coeff[::-1]):
                if arg is None: return None
                y_i += x ** index * arg

            if ey is None:        
                correlation = 1 - np.sum( ( y - y_i )**2 ) /np.sum( ( y - (np.sum(y)/len(y)) )**2 )
                correlation_type = f"R\\^{{2}}"
                params_str += f"\n{correlation_type}: {correlation:.{self.round_ticks_y}f}"
            else:
                correlation_intera = np.sum(((y - y_i)/ey)**2)
                correlation_ridotta = np.sum(((y - y_i)/ey)**2) / (len(x)-2)
                correlation_type = fr"\chi\^{{2}}"
                params_str += f"\n{correlation_type}: {correlation_intera:.{self.round_ticks_y}f}\n{correlation_type} ridotto: {correlation_ridotta:.{self.round_ticks_y}f}"
            
            if self.intersection_interpolation:
                # Y = MX + Q -> X = - Q / M
                if -q / m < x[-1]:
                    data_interpolazione = np.array([[x[-1], y_i[-1]], [-q / m, 0]])
                elif x[0] < -q / m:
                    data_interpolazione = np.array([[x[0], y_i[0]], [-q / m, 0]])
            else:
                data_interpolazione = np.array([[x[0], y_i[0]], [x[-1], y_i[-1]]])
            self.update_plot_list(_Single1DPlot(f"Interpolazione_{base_data.nome}", data_interpolazione, ""))

            return params_str

        except RuntimeError as e:
            self.compute_interpolation.sound_error.play()
            return f"\\#dc143c{{ATTENZIONE! Interpolazione fallita.}}\n\nCausa più probabile:\n\\#ffdd60{{Dati troppo divergenti.}}\n\nPossibile soluzione:\n\\#ffdd60{{Scegliere un range di dati più lineare.}}\n\nRaised error:\n\\i{{{e}}}"


    def derivative(self) -> None:

        try:
            base_data = self.plots[self.scroll_plots.ele_selected_index]
            derivata = np.gradient(base_data.data[:, base_data.column_y])

            data_deri = np.vstack((base_data.data[:, base_data.column_x], derivata))
            data_deri = data_deri.transpose(1, 0)

            self.update_plot_list(_Single1DPlot(f"Derivata_{base_data.nome}", data_deri, ""))

            return f"Calcolato correttamente.\n(\\#aaffaa{{Derivata_{base_data.nome}}})"        
        
        except IndexError as e:
            self.compute_derivative.sound_error.play()
            return f"\\#dc143c{{ATTENZIONE! Carica un grafico prima.}}\n\nRaised error:\n\\i{{{e}}}"
                    
                    

    def fit_curve(self):

        mancano_valori = False
        entries = [self.UI_param_0, self.UI_param_1, self.UI_param_2, self.UI_param_3]
        num_params_usati = self.curve_function.count("p[")
        for i in range(num_params_usati):
            try:
                entries[i].bg = entries[i].bg_backup
                float(entries[i].testo) 
            except Exception:
                self.compute_custom_curve.sound_error.play()
                entries[i].bg = np.array([200, 60, 60])
                mancano_valori = True

        try:
            # Dynamically create the curve function using eval
            curve_func = eval(f"lambda x, *p: {self.curve_function}")
            
            plot = self.plots[self.scroll_plots.ele_selected_index]

            x = plot.data[:, plot.column_x]
            y = plot.data[:, plot.column_y]

            initial_guess = [self.param_0, self.param_1, self.param_2, self.param_3]
            initial_guess = [float(i) for i in initial_guess if i != ""]

            # PREVIEW --------------------------------
            if self.show_guess:
                y_interpolata_iniziale = curve_func(x, *initial_guess)  
                guess_curve_fit_data = np.vstack((x, y_interpolata_iniziale))
                guess_curve_fit_data = guess_curve_fit_data.transpose(1, 0)

                contains_invalid = np.isnan(guess_curve_fit_data).any() or np.isinf(guess_curve_fit_data).any()
                if not contains_invalid:
                    self.update_plot_list(_Single1DPlot(f"Guess Curve Fit", guess_curve_fit_data, ""), active_on_load=True, substitute=True)
            else:
                nomi = [plot.nome for plot in self.scroll_plots1D.elementi]
                try:
                    index = nomi.index("Guess Curve Fit")
                    self.scroll_plots1D.remove_item_index(index)
                except ValueError:
                    ...
            # PREVIEW --------------------------------


            if len(x) < len(initial_guess):
                self.compute_custom_curve.sound_error.play()
                raise ValueError(f"\\#dc143c{{ATTENZIONE! Punti insufficienti.}}\n\nRaised error:\n\\i{{Numero parametri: {len(initial_guess)}}}\n\\i{{Punti minimi richiesti: {len(initial_guess) + 1}}}\n\\i{{Punti presenti nel grafico: {len(x)}}}")
            
            # Fit the curve
            params, covariance = curve_fit(curve_func, x, y, p0=initial_guess)
            self.info3.change_text(f"Calcolato correttamente.\n(\\#aaffaa{{curve_fit_{plot.nome}}})")
            
            y_interpolata_finale = curve_func(x, *params) 

            curve_fit_data = np.vstack((x, y_interpolata_finale))
            curve_fit_data = curve_fit_data.transpose(1, 0)


            contains_invalid = np.isnan(curve_fit_data).any() or np.isinf(curve_fit_data).any()

            if contains_invalid:
                self.compute_custom_curve.sound_error.play()
                raise ValueError(f"\\#dc143c{{ATTENZIONE! Overflow, prova altri parametri.}}\n\nRaised error:\n\\i{{NaN data present in the calculations}}")

            self.update_plot_list(_Single1DPlot(f"curve_fit_{plot.nome}", curve_fit_data, ""), active_on_load=True, substitute=True)
            return params
        
        except IndexError as e:
            if mancano_valori:
                self.compute_custom_curve.sound_error.play()
                self.info3.change_text(f"\\#dc143c{{ATTENZIONE! Inserisci tutti i parametri.}}\n\nRaised error:\n\\i{{{e}}}")
            else:
                self.compute_custom_curve.sound_error.play()
                self.info3.change_text(f"\\#dc143c{{ATTENZIONE! Carica un grafico prima.}}\n\nRaised error:\n\\i{{{e}}}")
        except TypeError as e:
            ...
        except AttributeError as e:
            self.compute_custom_curve.sound_error.play()
            self.info3.change_text(f"\\#dc143c{{ATTENZIONE! Sintassi sbagliata.}}\n\nRaised error:\n\\i{{{e}}}")
            # self.UI_curve_function.change_text("")
        except ValueError as e:
            self.compute_custom_curve.sound_error.play()
            self.info3.change_text(f"{e}")
        except RuntimeError as e:
            self.compute_custom_curve.sound_error.play()
            self.info3.change_text(f"\\#dc143c{{ATTENZIONE! Convergenza non raggiunta.}}\n\nRaised error:\n\\i{{{e}}}")
        except SyntaxError as e:
            self.compute_custom_curve.sound_error.play()
            self.info3.change_text(f"\\#dc143c{{ATTENZIONE! Sinstassi sbaglaita.}}\n\nRaised error:\n\\i{{{e}}}")



    def plot(self, logica: 'Logica', screenshot=0):
        """Richiesta UI pomoshnik, si può utilizzare con altri metodi di disegno. coordinate, colori e dimensioni sono forniti per poter essere usati in qualunque formato."""

        # try:

        self.update_attributes()

        if not screenshot:
            self.update(logica)

        self._normalize_data2screen() # preparazione dati

        self._disegna_bg()      

        if self.plot_mode == 1: self._disegna_dati2D()
        if self.plot_mode == 1: self._disegna_ZBAR()

        if self.plot_mode == 0: self._disegna_gradiente()
        self._disegna_assi()
        self._disegna_labels(logica)
        self._disegna_ticks()

        if self.plot_mode == 0: self._disegna_dati1D()
        
        self._disegna_legend(logica)
        self._disegna_molecola(logica, screenshot)

        if not screenshot:
            self._disegna_mouse_coordinate(logica) # aggiungi secondo asse
            self._disegna_mouse_zoom(logica)

        # except Exception as e:
        #     ...
            # print("Frame drawing error.")


    def _disegna_ZBAR(self):

        if self.second_y_axis:

            for plot, status in zip(self.plots, self.scroll_plots.ele_mask):
                if status:
            
                    if self.zoom_boundaries[1] < 0:
                        self.zoom_boundaries[1] = 0
                    if self.zoom_boundaries[0] < 0:
                        self.zoom_boundaries[0] = 0
                    if self.zoom_boundaries[2] > 1:
                        self.zoom_boundaries[2] = 1
                    if self.zoom_boundaries[3] > 1:
                        self.zoom_boundaries[3] = 1

                    dimensioni = plot.data.shape

                    indice_inizio_x = dimensioni[0] * self.zoom_boundaries[0]
                    indice_inizio_y = dimensioni[1] * (1 - self.zoom_boundaries[3])
                    indice_fine_x = dimensioni[0] * self.zoom_boundaries[2]
                    indice_fine_y = dimensioni[1] * (1 - self.zoom_boundaries[1])

                    fa = plot.data[int(indice_inizio_x) : int(indice_fine_x), int(indice_inizio_y) : int(indice_fine_y), 2]

                    # fill la barra di altezza map colore
                    map_color_array = np.zeros((1, 255, 3))

                    for i in range(3):
                        map_color_array[:, :, i] = np.linspace(plot.colore_base2[i], plot.colore_base1[i], map_color_array.shape[1]).reshape(int(map_color_array.shape[0]), map_color_array.shape[1])

                    
                    self.screen._blit_surface(
                        self.screen._generate_surface(map_color_array), (self.max_plot_square[0] + self.max_plot_square[2] * 1.05, self.max_plot_square[1]), scale=(self.max_plot_square[2] * 0.05, self.max_plot_square[3]))

                    # disegna la barra di altezza map colore
                    self.screen._add_rectangle(
                        [self.max_plot_square[0] + self.max_plot_square[2] * 1.05, self.max_plot_square[1], self.max_plot_square[2] * 0.05, self.max_plot_square[3]], self.ax_color_2y, 3 * self.scale_factor_viewport
                    )

                    # aggiorno valore dei tick
                    fa_min = np.min(fa)
                    fa_max = np.max(fa - fa_min)


                    self.spazio_coordinate_native[4] = fa_min
                    self.spazio_coordinate_native[5] = fa_max
                    
                    # calcolo posizione dei tick
                    ticks_2y = self._find_optimal_ticks([self.spazio_coordinate_native[4], self.spazio_coordinate_native[5]])

                    # fast check for good and bad
                    fix = 1
                    while fix:
                        if ticks_2y[0] < self.spazio_coordinate_native[4]:
                            _ = ticks_2y.pop(0)
                        else:
                            fix = 0                
                    fix = 1
                    while fix:
                        if len(ticks_2y) > 0 and ticks_2y[-1] > self.spazio_coordinate_native[5]:
                            _ = ticks_2y.pop()
                        else:
                            fix = 0


                    coords_ticks_2y = ticks_2y
                    coords_ticks_2y -= self.spazio_coordinate_native[4]
                    coords_ticks_2y /= (self.spazio_coordinate_native[5] - self.spazio_coordinate_native[4] + 1e-6)
                    coords_ticks_2y *= (self.max_plot_square[3])  
                    coords_ticks_2y = self.max_plot_square[3] - coords_ticks_2y      
                    coords_ticks_2y += self.max_plot_square[1]

                    # preparo l'asse e il render
                    formattatore_2y = "e" if self.formatting_y else "f"
                    self.offset_2y_tick_value: int = (self.pixel_len_subdivisions + 25) * self.scale_factor_viewport
                    labels_info_text = []
                    labels_info_pos = []
                    labels_info_anchor = []
                    labels_info_color = []
                    labels_info_rotation = []

                    for index, coord in enumerate(coords_ticks_2y):
                        self.screen._add_line([[self.max_plot_square[0] + self.max_plot_square[2] * 1.1, coord], [self.max_plot_square[0] + self.max_plot_square[2] * 1.1 + self.pixel_len_subdivisions * self.scale_factor_viewport, coord]], self.ax_color_2y, 4 * self.scale_factor_viewport)

                        labels_info_text.append(f"{ticks_2y[index]:.{self.round_ticks_2y}{formattatore_2y}}")
                        labels_info_pos.append([self.max_plot_square[0] + self.max_plot_square[2] * 1.1 + self.offset_x_label + self.offset_x_tick_value, coord])
                        labels_info_anchor.append("lc")
                        labels_info_color.append(self.tick_color_2y)
                        labels_info_rotation.append(0)

                    # disegno il valore corrispondente
                    self.screen._add_text(labels_info_text, labels_info_pos, anchor=labels_info_anchor, size=float(self.size_ticks) * self.scale_factor_viewport, color=labels_info_color, rotation=labels_info_rotation)




    def _disegna_dati2D(self):
       
        for plot, status in zip(self.plots, self.scroll_plots.ele_mask):
            if status:
         
                if self.zoom_boundaries[1] < 0:
                    self.zoom_boundaries[1] = 0
                if self.zoom_boundaries[0] < 0:
                    self.zoom_boundaries[0] = 0
                if self.zoom_boundaries[2] > 1:
                    self.zoom_boundaries[2] = 1
                if self.zoom_boundaries[3] > 1:
                    self.zoom_boundaries[3] = 1

                dimensioni = plot.data.shape

                indice_inizio_x = dimensioni[0] * self.zoom_boundaries[0]
                indice_inizio_y = dimensioni[1] * (1 - self.zoom_boundaries[3])
                indice_fine_x = dimensioni[0] * self.zoom_boundaries[2]
                indice_fine_y = dimensioni[1] * (1 - self.zoom_boundaries[1])

                fa = plot.data[int(indice_inizio_x) : int(indice_fine_x), int(indice_inizio_y) : int(indice_fine_y), 2]

                color_changed = False
                if np.sum(plot.prev_colore_base2 != plot.colore_base2) != 0 or np.sum(plot.prev_colore_base1 != plot.colore_base1) != 0:
                    color_changed = True
                    plot.prev_colore_base2 = plot.colore_base2
                    plot.prev_colore_base1 = plot.colore_base1


                if np.shape(fa) != plot.previous_final_shape or color_changed:   
                    plot.previous_final_shape = np.shape(fa)
                    plot.previous_max_z = np.max(fa)
                    plot.previous_min_z = np.min(fa)

                    if plot.flip_y:
                        fa = fa[:, ::-1]
                    if plot.flip_x:
                        fa = fa[::-1, :]
                    
                    plot.final_array = colora_array(fa, plot.colore_base1, plot.colore_base2, plot.previous_max_z, plot.previous_min_z)

                self.screen._blit_surface(
                    self.screen._generate_surface(plot.final_array), 
                    (self.max_plot_square[0], self.max_plot_square[1]), 
                    scale=(self.max_plot_square[2], self.max_plot_square[3])
                )


    def _disegna_molecola(self, logica: 'Logica', screenshot: bool = 0):
        
        colore_generico = "A8A8A8"

        def molecola(stringa_SMILE, d, id):
            try:
                molecola = Chem.MolFromSmiles(stringa_SMILE)
                AllChem.Compute2DCoords(molecola)
                Draw.MolToFile(molecola, "./TEXTURES/" + (f'molecola_save{id}.svg'),(int(d),int(d)))
                return 1
            except:
                return 0

        def reazione(stringa_SMILE, d, id):
            try:
                rxn = Reactions.ReactionFromSmarts(stringa_SMILE, useSmiles=True)
                Draw.ReactionToImage(rxn, useSVG=True)
                nome = "./TEXTURES/" + (f'molecola_save{id}.svg')
                with open(nome, "w") as file:
                    file.write(Draw.ReactionToImage(rxn, useSVG=True, subImgSize=(int(d/(3+stringa_SMILE.count("."))),int(d))))

                return 1
            except:
                return 0

        def alpha(id):
            try:
                nome = "./TEXTURES/" + (f'molecola_save{id}.svg')
                with open(nome, "r") as file:
                    data = file.read()
                    data = data.replace(r"<rect style='opacity:1.0", r"<rect style='opacity:0")
                    data = data.replace("#000000", "#" + colore_generico)
                    data = data.replace("#191919", "#" + colore_generico)
                with open(nome, "w") as file:
                    file.write(data)
            except Exception as e:
                print(e)

        #############################################################################################################################
        #############################################################################################################################
        #############################################################################################################################

        try:
            for molecola_ele, status in zip(self.elenco_metadata.elementi, self.elenco_metadata.ele_mask): 
                if status:
                    path = f"./TEXTURES/molecola_save{molecola_ele.nome}.svg"

                    new_w, new_h = int(float(molecola_ele.size) * self.scale_factor_viewport), int(float(molecola_ele.size) * self.scale_factor_viewport)

                    # ----------------------------------------------------------------------
                    self.screen.load_image(path)
                    self.screen.scale_image((new_w, new_h))
                    self.screen.tavolozza.blit(self.screen.loaded_image, (molecola_ele.x * self.screen.w / 100 - new_w / 2, molecola_ele.y * self.screen.h / 100 - new_h / 2))
                    # ----------------------------------------------------------------------
                                        

        except FileNotFoundError:
            ...


        # Controlla se creare una nuova molecola o no
        if self.add_molecola.flag_foo:
            self.add_molecola.flag_foo = 0
            self.storico_molecole += 1
            self.elenco_metadata.add_element_scroll(Molecule(self.storico_molecole, "", 50, 50, 1000), True)
            self.elenco_metadata.ele_selected_index = len(self.elenco_metadata.elementi) - 1


        # aggiorna i valori della molecola attiva con i dati forniti dall'UI
        if not self.active_molecule is None:
            try:
                self.active_molecule.code = self.molecule_input.get_text()
                self.active_molecule.x = int(float(self.pos_x_molecola))
                self.active_molecule.y = int(float(self.pos_y_molecola))
                self.active_molecule.size = int(float(self.dimensione_molecola))

            except Exception as e:
                print(e)


        # controlla se è il caso di aggiornare l'UI con i dati della nuova molecola
        self.molecules = self.elenco_metadata.elementi
        old_active = self.active_molecule
        force_update = False
        if len(self.molecules) > 0:

            self.active_molecule: Molecule = self.molecules[self.elenco_metadata.ele_selected_index]

            if self.active_molecule != old_active:
                self.UI_pos_x_molecola.change_text(f"{self.active_molecule.x}")
                self.UI_pos_y_molecola.change_text(f"{self.active_molecule.y}")
                self.UI_dimensione_molecola.change_text(f"{self.active_molecule.size}") 
                self.UI_molecule_input.change_text(f"{self.active_molecule.code}")
                force_update = True


        # controlla se il codice SMILE è stato cambiato -> aggiorna il disegno basato sul codice SMILE fornito
        new_SMILE = self.molecule_input.testo
        if new_SMILE != self.old_SMILE or force_update:

            id_image = self.active_molecule.nome
            self.old_SMILE = new_SMILE

            esito = molecola(self.molecule_input.testo, self.molecule_preview.w, id_image)
            alpha(id_image)

            self.molecule_input.color_text = [200, 200, 200] if esito else [220, 20, 60]
        
            try:
                self.molecule_preview.tavolozza.fill([25, 25, 25])
                self.molecule_preview.load_image(f"./TEXTURES/molecola_save{id_image}.svg")
                self.molecule_preview._blit_surface(self.molecule_preview.loaded_image, (0, 0))
            except FileNotFoundError:
                ...


        # SMILE istruzioni: 
        # ATOMS:          C, O, N      [Na+], [13C], [O-]
        # BONDS:          CC, C-C, C=C, C#C, c1ccccc1
        # BRANCHING:      CC(C)O
        # STEREO:         "C[C@H](O)C" @ means centro tetraedrico, "C/C=C/C" / means E isomero, "C/C=C\C" \ means Z isomero 
        # CHARGE:         [NH4+], [O-]
        # ISOTOPI:        [13C]     
        # JOLLY:          *, [#6] 6->Carbon
        # DISCONNECT:     .
        # EXPL. H:        [CH4] (not shown in image)


    def _disegna_gradiente(self):
        
        for plot, status in zip(self.plots, self.scroll_plots.ele_mask):
            # disegno i dati se plot acceso
            if status:


                cond1 = plot.data2plot[:, plot.column_x] >= self.max_plot_square[0] + self.max_plot_square[2] * (self.minimal_offset_data_x - 0.005)
                cond2 = plot.data2plot[:, plot.column_y] >= self.max_plot_square[1] + self.max_plot_square[3] * (self.minimal_offset_data_y - 0.005)
                cond3 = plot.data2plot[:, plot.column_x] <= self.max_plot_square[0] + self.max_plot_square[2] * (1 - self.minimal_offset_data_x + 0.005)
                cond4 = plot.data2plot[:, plot.column_y] <= self.max_plot_square[1] + self.max_plot_square[3] * (1 - self.minimal_offset_data_y + 0.005)
                
                # Combine all conditions with logical AND
                combined_condition = cond1 & cond2 & cond3 & cond4

                extracted = plot.data2plot[combined_condition]
                extracted = np.vstack((extracted[:, plot.column_x], extracted[:, plot.column_y]))
                extracted = np.transpose(extracted, (1, 0))

                if len(extracted) < 2:
                    # exit the function if too few points
                    return

                if plot.gradiente and plot.grad_mode == "vert":
                    # VERTICAL
                    for x1, y1, x2, y2 in zip(extracted[:, plot.column_x].astype(int)[:-1], extracted[:, plot.column_y].astype(int)[:-1], extracted[:, plot.column_x].astype(int)[1:], extracted[:, plot.column_y].astype(int)[1:]):
                        if x1 > x2:
                            x1, x2 = x2, x1 
                        
                        m = (y2 - y1) / (x2 - x1)
                        for i in range(0, x2 - x1):
                            y_interpolated = int(y1 + m * i)
                            
                            colore = (self.max_plot_square[1] + self.max_plot_square[3] - y_interpolated) / (self.max_plot_square[1] + self.max_plot_square[3])
                            
                            colore_finale = np.array(self.plot_area_color) + (np.array(plot.function_color) - np.array(self.plot_area_color)) * colore
                            
                            self.screen._add_line([[x1 + i, self.max_plot_square[1] + self.max_plot_square[3] * (1 - self.minimal_offset_data_x + 0.005)], [x1 + i, y_interpolated]], colore_finale, 1)
                

                elif plot.gradiente and plot.grad_mode == "hori":
                    # HORIZONTAL

                    start_y = self.max_plot_square[1] + self.max_plot_square[3] * (1 - self.minimal_offset_data_y + 0.005)
                    end_y = self.max_plot_square[1] + self.max_plot_square[3] * (self.minimal_offset_data_y - 0.005)
                    start_x = self.max_plot_square[0] + self.max_plot_square[2] * (self.minimal_offset_data_x - 0.005)
                    end_x = self.max_plot_square[0] + self.max_plot_square[2] * (1 - self.minimal_offset_data_x + 0.005)
                    
                    gradient = np.zeros((int(end_x - start_x), int(start_y - end_y), 3), dtype=np.uint8)
                    
                    bg_color = self.plot_area_color

                    # CASO 1 -> 0 In mezzo al range
                    if self.zero_y > end_y and self.zero_y < start_y:
                        
                        # coloro il gradiente UPPER
                        limite = int(self.zero_y - end_y)
                        for i in range(3):
                            gradient[:, :limite, i] = np.tile(np.linspace(plot.function_color[i] / 2, bg_color[i], limite), (int(end_x - start_x), 1)).reshape(int(end_x - start_x), limite)
                        # coloro il gradiente LOWER
                        limite = int(start_y - self.zero_y)
                        if limite > 0:
                            for i in range(3):
                                gradient[:, -limite:, i] = np.tile(np.linspace(bg_color[i], plot.function_color[i] / 2, limite), (1, int(end_x - start_x))).reshape(int(end_x - start_x), limite)
                        
                        # rimozione X esterni
                        gradient[:int(np.min(extracted[:, 0]) - start_x + 1), :, :] = bg_color
                        gradient[int(np.max(extracted[:, 0]) - start_x - 1):, :, :] = bg_color
                        
                        self.screen._paste_array(gradient, (start_x, end_y))
                        
                        # lancio della maschera (zero fuori dagli estremi) UPPER  
                        for x1, y1, x2, y2 in zip(extracted[:, 0].astype(int)[:-1], extracted[:, 1].astype(int)[:-1], extracted[:, 0].astype(int)[1:], extracted[:, 1].astype(int)[1:]):

                            if x1 > x2:
                                x1, x2 = x2, x1 

                            m = (y2 - y1) / (x2 - x1)
                            
                            for i in range(0, x2 - x1):
                                y_interpolated = int(y1 + m * i)
                                obiettivo = y_interpolated if y_interpolated < self.zero_y else self.zero_y
                                self.screen._add_line([[x1 + i, end_y], [x1 + i, obiettivo]], bg_color, 1)

                        # lancio della maschera (zero fuori dagli estremi) LOWER
                        for x1, y1, x2, y2 in zip(extracted[:, 0].astype(int)[:-1], extracted[:, 1].astype(int)[:-1], extracted[:, 0].astype(int)[1:], extracted[:, 1].astype(int)[1:]):
                            
                            if x1 > x2:
                                x1, x2 = x2, x1 

                            m = (y2 - y1) / (x2 - x1)
                            
                            for i in range(0, x2 - x1):
                                y_interpolated = int(y1 + m * i)
                                obiettivo = y_interpolated if y_interpolated > self.zero_y else self.zero_y 
                                self.screen._add_line([[x1 + i, start_y], [x1 + i, obiettivo]], bg_color, 1)

                    else:
                        # CASO 2 -> Tutto sotto lo 0
                        if self.zero_y <= end_y: 
                            from_y = start_y
                            colore_start = bg_color
                            colore_finale = np.array(plot.function_color) / 2
                        
                        # CASO 3 -> Tutto sopra lo 0
                        elif self.zero_y >= start_y:
                            from_y = end_y
                            colore_start = np.array(plot.function_color) / 2
                            colore_finale = bg_color

                        # coloro il gradiente
                        for i in range(3):
                            gradient[:, :, i] = np.linspace(colore_start[i], colore_finale[i], int(start_y - end_y)).reshape(1, int(start_y - end_y))
                        
                        # rimozione X esterni
                        gradient[:int(np.min(extracted[:, 0]) - start_x + 1), :, :] = bg_color
                        gradient[int(np.max(extracted[:, 0]) - start_x - 1):, :, :] = bg_color

                        self.screen._paste_array(gradient, (start_x, end_y))
                        
                        # lancio della maschera (zero fuori dagli estremi)    
                        for x1, y1, x2, y2 in zip(extracted[:, 0].astype(int)[:-1], extracted[:, 1].astype(int)[:-1], extracted[:, 0].astype(int)[1:], extracted[:, 1].astype(int)[1:]):
                            
                            if x1 > x2:
                                x1, x2 = x2, x1 
                            
                            m = (y2 - y1) / (x2 - x1)
                            
                            for i in range(0, x2 - x1):
                                y_interpolated = int(y1 + m * i)
                                self.screen._add_line([[x1 + i, from_y], [x1 + i, y_interpolated]], bg_color, 1)


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
        
        if len([1 for status in self.scroll_plots.ele_mask if status]) > 0:

            try:

                value = self._extract_mouse_coordinate(logica.mouse_pos)
                value = self._transform_native_space(value)

                posizione = np.array(logica.mouse_pos)

                posizione[0] -= self.screen.x
                posizione[1] -= self.screen.y

                self.screen._add_text(f"({float(value[0]):.{int(self.round_ticks_x)}f}, {float(value[1]):.{int(self.round_ticks_y)}f})", size=1.2, pos=posizione, anchor="cd", color=[150, 160, 150])

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
        
        self.legend_position = [float(self.x_legend), float(self.y_legend)]               # done
        self.legend_draw_icogram = self.show_icons                                                 # NO                           
        self.legend_match_color_title = self.match_color_text                                      # NO               
        self.legend_color_title = self.color_text                                                   # NO   
        self.legend_show_background = self.show_legend_background                                  # done                   
        self.legend_color_background = self.legend_bg_color                                         # done           

        self.legend_transparent = self.transparent_background
        self.legend_blur_strenght = float(self.blur_strenght) * self.scale_factor_viewport

        if self.legend_draw_icogram:
            self.icon_size_pixel = 150 * self.scale_factor_viewport
        else:
            self.icon_size_pixel = 0

        
        
        if self.plot_mode == 0:

            if len([1 for status in self.scroll_plots.ele_mask if status]) > 0 and self.show_legend:


                legend_position = [self.max_plot_square[0] + self.max_plot_square[2] * self.legend_position[0], self.max_plot_square[1] + self.max_plot_square[3] * self.legend_position[1]]

                # legenda testo
                if self.legend_match_color_title:
                    self.labels[4].change_text("".join([f'\\#{MateUtils.rgb2hex(plot.function_color if plot.function else plot.scatter_color)}{{{plot.nome}}}\n' for plot, status in zip(self.plots, self.scroll_plots.ele_mask) if status])[:-1])
                else:
                    self.labels[4].color_text = self.legend_color_title
                    self.labels[4].change_text("".join([f'{plot.nome}\n' for plot, status in zip(self.plots, self.scroll_plots.ele_mask) if status])[:-1])

                self.labels[4].anchor = "cc"

                new_dim_legend = self.font_size_legend
                
                self.labels[4].change_font_size(float(new_dim_legend) * self.scale_factor_viewport)

                self.labels[4].recalc_geometry(f"{legend_position[0]}px", f"{legend_position[1]}px", anchor_point="cc", new_w="-*w", new_h=f"{self.labels[4].font.font_pixel_dim[1] * len([1 for status in self.scroll_plots.ele_mask if status])}px")

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
                                            colore_tratteggiato = plot.function_color if i % 2 == 0 else self.plot_area_color
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
                                    ], plot.scatter_color, plot.scatter_width * self.scale_factor_viewport, plot.scatter_border * self.scale_factor_viewport)


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
                                    ], plot.scatter_color, plot.scatter_width * self.scale_factor_viewport, plot.scatter_border * self.scale_factor_viewport)


                                plot_attivo_analizzato += 1

                    self.labels[4].disegnami(logica, 0, self.screen.tavolozza, 0, 0)
            
        elif self.plot_mode == 1:
            
            if len([1 for status in self.scroll_plots.ele_mask if status]) > 0 and self.show_legend:
                
                for plot, status in zip(self.plots, self.scroll_plots.ele_mask):

                    lenght_line = float(self.size_scale_marker2D)
                    lenght_line_px = (self.max_plot_square[2]) * lenght_line / (self.spazio_coordinate_native[2]) 



                legend_position = [self.max_plot_square[0] + self.max_plot_square[2] * self.legend_position[0], self.max_plot_square[1] + self.max_plot_square[3] * self.legend_position[1]]

                # legenda testo
                self.labels[4].color_text = self.legend_color_title
                self.labels[4].change_text(f"{self.text_2D_plot}")

                self.labels[4].anchor = "cc"

                new_dim_legend = self.font_size_legend
                
                self.labels[4].change_font_size(float(new_dim_legend) * self.scale_factor_viewport)

                self.labels[4].recalc_geometry(f"{legend_position[0]}px", f"{legend_position[1]}px {10 * self.scale_factor_viewport}px", anchor_point="cd", new_w="-*w", new_h="-*h")

                leg_lar = max(self.labels[4].w, abs(lenght_line_px)) + 24 * self.scale_factor_viewport
                leg_lar_2 = leg_lar / 2

                leg_alt = self.labels[4].h * 1.3 + 20 * self.scale_factor_viewport
                leg_alt_2 = leg_alt / 2


                if self.legend_transparent:
                    pixel_array = self.screen._extract_pixel_values(legend_position[0] - leg_lar_2, legend_position[1] - leg_alt_2, leg_lar, leg_alt)

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
                    self.screen._add_rectangle([legend_position[0] - leg_lar_2, legend_position[1] - leg_alt_2, leg_lar, leg_alt], self.legend_color_background)


                if self.legend_transparent:
                    self.labels[4].disegnami(logica, 0, superficie_alpha, - self.labels[4].w / 2 -self.labels[4].x + leg_lar_2, - self.labels[4].y)
                    self.screen._add_line_static(superficie_alpha, [[- abs(lenght_line_px) / 2 + leg_lar_2, + leg_alt - self.spessore_scala_2Dplot * self.scale_factor_viewport - 10], [leg_lar_2 + abs(lenght_line_px) / 2, leg_alt - self.spessore_scala_2Dplot * self.scale_factor_viewport - 10]], self.legend_color_title, self.spessore_scala_2Dplot * self.scale_factor_viewport)
                    self.screen._add_line_static(superficie_alpha, [[- abs(lenght_line_px) / 2 + leg_lar_2, + leg_alt - self.spessore_scala_2Dplot * self.scale_factor_viewport - 10], [- abs(lenght_line_px) / 2 + leg_lar_2, leg_alt - self.spessore_scala_2Dplot * self.scale_factor_viewport - 10 - leg_alt_2 / 2]], self.legend_color_title, self.spessore_scala_2Dplot * self.scale_factor_viewport)
                    self.screen._add_line_static(superficie_alpha, [[leg_lar_2 + abs(lenght_line_px) / 2, + leg_alt - self.spessore_scala_2Dplot * self.scale_factor_viewport - 10], [leg_lar_2 + abs(lenght_line_px) / 2, leg_alt - self.spessore_scala_2Dplot * self.scale_factor_viewport - 10 - leg_alt_2 / 2]], self.legend_color_title, self.spessore_scala_2Dplot * self.scale_factor_viewport)

                    self.screen._blit_surface(superficie_alpha, [legend_position[0] - leg_lar_2, legend_position[1] - leg_alt_2])
                        
                else:
                    # CASO NON TRASPARENTE        
                    self.labels[4].disegnami(logica, 0, self.screen.tavolozza, 0, 0)
                    self.screen._add_line([[legend_position[0] - leg_lar_2 - abs(lenght_line_px) / 2 + leg_lar_2, legend_position[1] + leg_alt_2 - self.spessore_scala_2Dplot * self.scale_factor_viewport - 10], [legend_position[0] - leg_lar_2 + leg_lar_2 + abs(lenght_line_px) / 2, leg_alt_2 - self.spessore_scala_2Dplot * self.scale_factor_viewport - 10 + legend_position[1]]], self.legend_color_title, self.spessore_scala_2Dplot * self.scale_factor_viewport)
                    self.screen._add_line([[legend_position[0] - leg_lar_2 - abs(lenght_line_px) / 2 + leg_lar_2, legend_position[1] + leg_alt_2 - self.spessore_scala_2Dplot * self.scale_factor_viewport - 10], [legend_position[0] - leg_lar_2 - abs(lenght_line_px) / 2 + leg_lar_2, leg_alt_2 - self.spessore_scala_2Dplot * self.scale_factor_viewport - 10 - leg_alt_2 / 2 + legend_position[1]]], self.legend_color_title, self.spessore_scala_2Dplot * self.scale_factor_viewport)
                    self.screen._add_line([[legend_position[0] - leg_lar_2 + leg_lar_2 + abs(lenght_line_px) / 2, legend_position[1] + leg_alt_2 - self.spessore_scala_2Dplot * self.scale_factor_viewport - 10], [legend_position[0] - leg_lar_2 + leg_lar_2 + abs(lenght_line_px) / 2, leg_alt_2 - self.spessore_scala_2Dplot * self.scale_factor_viewport - 10 - leg_alt_2 / 2 + legend_position[1]]], self.legend_color_title, self.spessore_scala_2Dplot * self.scale_factor_viewport)
            


    def _disegna_labels(self, logica: 'Logica'):

        new_dim_title = self.font_size_title
        new_dim_x = self.font_size_label_x
        new_dim_y = self.font_size_label_y
        new_dim_2y = self.font_size_label_2y
        
        if self.labels[0].font_size_update != float(new_dim_title) * self.scale_factor_viewport:
            self.labels[0].change_font_size(float(new_dim_title) * self.scale_factor_viewport)
    
        if self.labels[1].font_size_update != float(new_dim_x) * self.scale_factor_viewport:
            self.labels[1].change_font_size(float(new_dim_x) * self.scale_factor_viewport)
    
        if self.labels[2].font_size_update != float(new_dim_y) * self.scale_factor_viewport:
            self.labels[2].change_font_size(float(new_dim_y) * self.scale_factor_viewport)
        
        if self.second_y_axis:
            if self.labels[3].font_size_update != float(new_dim_2y) * self.scale_factor_viewport:
                self.labels[3].change_font_size(float(new_dim_2y) * self.scale_factor_viewport)

        # titolo
        self.labels[0].change_text(f"{self.text_title}")
        self.labels[0].recalc_geometry(f"{self.screen.x + self.max_plot_square[0] + self.max_plot_square[2] / 2}px", f"{self.screen.y + self.max_plot_square[1] / 2}px", new_w="-*w", new_h="-*h", anchor_point="cc")
        self.labels[0].color_text = self.label_title_color
        self.labels[0].disegnami(logica, 0, self.screen.tavolozza, DANG_offset_x=-self.screen.x, DANG_offset_y=-self.screen.y)
        
        # X label
        self.labels[1].change_text(f"{self.text_label_x}")
        self.labels[1].recalc_geometry(f"{self.screen.x + self.max_plot_square[0] + self.max_plot_square[2] / 2}px", f"{self.screen.y + self.max_plot_square[3] + 2 * self.max_plot_square[1] - 5}px", new_w="-*w", new_h="-*h", anchor_point="cd")
        self.labels[1].color_text = self.label_x_color
        self.labels[1].disegnami(logica, 0, self.screen.tavolozza, DANG_offset_x=-self.screen.x, DANG_offset_y=-self.screen.y)
        
        # Y label
        self.labels[2].change_text(f"{self.text_label_y}")
        self.labels[2].recalc_geometry(f"{self.screen.x}px", f"{self.screen.y + self.max_plot_square[1] + self.max_plot_square[3] / 2 - self.labels[2].font.font_pyg_r.size(self.labels[2].testo_diplayed[0])[0] / 2}px", new_w="-*w", new_h="-*h", anchor_point="lu")
        self.labels[2].color_text = self.label_y_color
        self.labels[2].disegnami(logica, 90, self.screen.tavolozza, DANG_offset_x=-self.screen.x, DANG_offset_y=-self.screen.y)
        
        # 2Y label
        if self.second_y_axis:
            self.labels[3].change_text(f"{self.text_label_2y}")
            self.labels[3].recalc_geometry(f"{self.screen.w}px n-*h", f"{self.screen.y + self.max_plot_square[1] + self.max_plot_square[3] / 2 - self.labels[3].font.font_pyg_r.size(self.labels[3].testo_diplayed[0])[0] / 2}px", new_w="-*w", new_h="-*h", anchor_point="lu")
            self.labels[3].color_text = self.label_2y_color
            self.labels[3].disegnami(logica, 90, self.screen.tavolozza, DANG_offset_y=-self.screen.y)
            

    def _get_nice_ticks(self):

        if self.invert_x_axis and self.plot_mode == 0:
            ticks_x = self._find_optimal_ticks([self.spazio_coordinate_native[2], self.spazio_coordinate_native[0]])
        else:
            ticks_x = self._find_optimal_ticks([self.spazio_coordinate_native[0], self.spazio_coordinate_native[2]])

        ticks_y = self._find_optimal_ticks([self.spazio_coordinate_native[1], self.spazio_coordinate_native[3]])
        ticks_2y = self._find_optimal_ticks([self.spazio_coordinate_native[4], self.spazio_coordinate_native[5]])

        self.coords_of_ticks = [ticks_x, ticks_y, ticks_2y]
        self.value_of_ticks = [ticks_x, ticks_y, ticks_2y]


    def _disegna_ticks(self):

        coords = self._get_plot_area_coord()

        formattatore_x = "e" if self.formatting_x else "f"
        formattatore_y = "e" if self.formatting_y else "f"
        formattatore_2y = "e" if self.formatting_y else "f"

        self.offset_x_tick_value: int = (self.pixel_len_subdivisions + 7) * self.scale_factor_viewport
        self.offset_y_tick_value: int = (self.pixel_len_subdivisions + 25) * self.scale_factor_viewport
        self.offset_2y_tick_value: int = (self.pixel_len_subdivisions + 25) * self.scale_factor_viewport

        labels_info_text = []
        labels_info_pos = []
        labels_info_anchor = []
        labels_info_color = []
        labels_info_rotation = []

        for index, coord in enumerate(self.coords_of_ticks[0]):
            if self.show_grid_x:
                self.screen._add_line([[coord, coords[3]], [coord, coords[1]]], self.ax_color_x, self.scale_factor_viewport)
            self.screen._add_line([[coord, coords[3]], [coord, coords[3] + self.pixel_len_subdivisions * self.scale_factor_viewport]], self.ax_color_x, 4 * self.scale_factor_viewport)

            labels_info_text.append(f"{self.value_of_ticks[0][index]:.{self.round_ticks_x}{formattatore_x}}")
            labels_info_pos.append([coord, coords[3] + float(self.offset_ticks_ax_y) * self.scale_factor_viewport])
            labels_info_anchor.append("cc")
            labels_info_color.append(self.tick_color_x)
            labels_info_rotation.append(0)


        for index, coord in enumerate(self.coords_of_ticks[1]):
            if self.show_grid_y:
                self.screen._add_line([[coords[0], coord], [coords[2], coord]], self.ax_color_y, self.scale_factor_viewport)
            self.screen._add_line([[coords[0], coord], [coords[0] - self.pixel_len_subdivisions * self.scale_factor_viewport, coord]], self.ax_color_y, 4 * self.scale_factor_viewport)

            labels_info_text.append(f"{self.value_of_ticks[1][index]:.{self.round_ticks_y}{formattatore_y}}")
            labels_info_pos.append([coords[0] + float(self.offset_ticks_ax_x) * self.scale_factor_viewport, coord])
            labels_info_anchor.append("rc")
            labels_info_color.append(self.tick_color_y)
            labels_info_rotation.append(0)
        

        if self.second_y_axis and self.plot_mode == 0:
            for index, coord in enumerate(self.coords_of_ticks[2]):
                if self.show_grid_2y:
                    self.screen._add_line([[coords[0], coord], [coords[2], coord]], self.ax_color_2y, self.scale_factor_viewport)
                self.screen._add_line([[coords[2], coord], [coords[2] + self.pixel_len_subdivisions * self.scale_factor_viewport, coord]], self.ax_color_2y, 4 * self.scale_factor_viewport)

                labels_info_text.append(f"{self.value_of_ticks[2][index]:.{self.round_ticks_2y}{formattatore_2y}}")
                labels_info_pos.append([coords[0] + self.max_plot_square[2] - float(self.offset_ticks_ax_x) * self.scale_factor_viewport, coord])
                labels_info_anchor.append("lc")
                labels_info_color.append(self.tick_color_2y)
                labels_info_rotation.append(0)

        # disegno il valore corrispondente
        self.screen._add_text(labels_info_text, labels_info_pos, anchor=labels_info_anchor, size=float(self.size_ticks) * self.scale_factor_viewport, color=labels_info_color, rotation=labels_info_rotation)


    def _disegna_assi(self):

        coords = self._get_plot_area_coord()

        if self.show_bounding_box:
            self.screen._add_line([[self.max_plot_square[0], self.max_plot_square[1]], [self.max_plot_square[0] + self.max_plot_square[2], self.max_plot_square[1]]], self.ax_color_x, 4 * self.scale_factor_viewport)
            self.screen._add_line([[self.max_plot_square[0] + self.max_plot_square[2], self.max_plot_square[1]], [self.max_plot_square[0] + self.max_plot_square[2], self.max_plot_square[1] + self.max_plot_square[3]]], self.ax_color_x, 4 * self.scale_factor_viewport)
        
        if self.second_y_axis:
            self.screen._add_line([[self.max_plot_square[0] + self.max_plot_square[2], self.max_plot_square[1]], [self.max_plot_square[0] + self.max_plot_square[2], self.max_plot_square[1] + self.max_plot_square[3]]], self.ax_color_2y, 4 * self.scale_factor_viewport)


        # si posizione sull'area del plot e setta un offset pari a self.offset_x_label o self.offset_y_label
        self.screen._add_line([[coords[0] - self.offset_x_label, coords[1]], [coords[0] - self.offset_x_label, coords[3]]], self.ax_color_y, 4 * self.scale_factor_viewport)
        self.screen._add_line([[coords[0], coords[3] + self.offset_y_label], [coords[2], coords[3] + self.offset_y_label]], self.ax_color_x, 4 * self.scale_factor_viewport)
    
                    
    def _disegna_dati1D(self):
        
        larg_error = self.max_plot_square[2] / 100

        for plot, status in zip(self.plots, self.scroll_plots.ele_mask):
            # disegno i dati se plot acceso
            if status:

                if plot.second_ax and not self.second_y_axis:
                    continue

                cond1 = plot.data2plot[:, plot.column_x] >= self.max_plot_square[0] + self.max_plot_square[2] * (self.minimal_offset_data_x - 0.005)
                cond2 = plot.data2plot[:, plot.column_y] >= self.max_plot_square[1] + self.max_plot_square[3] * (self.minimal_offset_data_y - 0.005)
                cond3 = plot.data2plot[:, plot.column_x] <=  self.max_plot_square[0] + self.max_plot_square[2] * (1 - self.minimal_offset_data_x + 0.005)
                cond4 = plot.data2plot[:, plot.column_y] <=  self.max_plot_square[1] + self.max_plot_square[3] * (1 - self.minimal_offset_data_y + 0.005)

                # Combine all conditions with logical AND
                combined_condition = cond1 & cond2 & cond3 & cond4

                extracted = plot.data2plot[combined_condition]

                if plot.data.shape[1] > 2:
                    extracted = np.vstack((extracted[:, plot.column_x], extracted[:, plot.column_y], extracted[:, plot.column_ey]))
                else:
                    extracted = np.vstack((extracted[:, plot.column_x], extracted[:, plot.column_y]))
    
                extracted = np.transpose(extracted, (1, 0))

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
                    self.screen._add_points(extracted[:, :2], plot.scatter_color, plot.scatter_width * self.scale_factor_viewport, plot.scatter_border * self.scale_factor_viewport)


                # Add the logic to transform the index into value and coordinate
                if len(plot.display_coords) > 0:
                    coords = [[plot.data2plot[index, 0], plot.data2plot[index, 1] - (13 * self.scale_factor_viewport + plot.scatter_width)] for index in plot.display_coords]
                    
                    if self.show_coords_value:
                        text = [f"({plot.data[index, 0]:.{self.round_ticks_x}f}, {plot.data[index, 1]:.{self.round_ticks_y}f})" for index in plot.display_coords]
                        self.screen._add_text(text, coords, anchor=["cd" for i in plot.display_coords], size=1 * self.scale_factor_viewport, color=[self.label_title_color for i in plot.display_coords], rotation=[0 for i in plot.display_coords])
                    
                    if self.show_coords_projection:
                        if plot.gradiente:
                            destinazione_proiezione = self.max_plot_square[3] * (1 - self.minimal_offset_data_y + 0.005) + self.max_plot_square[1]
                        else:
                            destinazione_proiezione = self.max_plot_square[3] + self.max_plot_square[1]

                        for index, coord in enumerate(coords):
                            self.screen._add_line([[coord[0], coord[1] + (13 * self.scale_factor_viewport + plot.scatter_width)], [coord[0], destinazione_proiezione]], width=1 * self.scale_factor_viewport, color=self.label_title_color)


    def _disegna_spezzata_tratteggiata(self, plot:'_Single1DPlot'):

        cond1 = plot.data2plot[:, plot.column_x] >= self.max_plot_square[0] + self.max_plot_square[2] * (self.minimal_offset_data_x - 0.005)
        cond2 = plot.data2plot[:, plot.column_y] >= self.max_plot_square[1] + self.max_plot_square[3] * (self.minimal_offset_data_y - 0.005)
        cond3 = plot.data2plot[:, plot.column_x] <= self.max_plot_square[0] + self.max_plot_square[2] * (1 - self.minimal_offset_data_x + 0.005)
        cond4 = plot.data2plot[:, plot.column_y] <= self.max_plot_square[1] + self.max_plot_square[3] * (1 - self.minimal_offset_data_y + 0.005)

        # Combine all conditions with logical AND
        combined_condition = cond1 & cond2 & cond3 & cond4

        extracted = plot.data2plot[combined_condition]

        if self.invert_x_axis:
            extracted = extracted[::-1, :]

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
                    colore = self.plot_area_color

                else:
                    colore = plot.function_color
                    
                self.screen._add_line([p1, new_point], colore, plot.function_width* self.scale_factor_viewport)

                p1 = new_point                


    def _disegna_bg(self):
        # setu-up canvas
        self.screen._clear_canvas(self.unused_area_color)
        # disegno area di plot BG
        self.screen.tavolozza.fill(self.canvas_area_color)
        # self.screen._add_rectangle(self.max_canvas_square, [255, 100, 100])
        self.screen._add_rectangle(self.max_plot_square, self.plot_area_color)
        

    def _normalize_data2screen(self, invert_y_coord=True):
        """Normalizes the data to the screen size"""
        
        self._get_native_data_bounds() # trovo i limiti anche per asse X, asse Y e asse 2°Y
        # ricerca dell'area di disegno
        self._find_max_square()

        numero_plot_attivi = len([active for active in self.scroll_plots.ele_mask if active])

        plot_attivi_analizzati = 0
        for plot, status in zip(self.plots, self.scroll_plots.ele_mask):
            # copia dei dati per trasformarle in screen coordinates
            if status and self.plot_mode == 0:

                try:
                    plot.data2plot = plot.data.copy()

                    if sum(self.norma_perc.buttons_state) > 0:
                        plot.data2plot[:, plot.column_y] -= np.min(plot.data2plot[:, plot.column_y])
                        plot.data2plot[:, plot.column_y] /= np.max(plot.data2plot[:, plot.column_y])

                        if self.norma_perc.buttons_state[1] and self.overlap:
                            plot.data2plot[:, plot.column_y] *= 100


                    # set dello 0
                    plot.data2plot[:, plot.column_x] -= self.spazio_coordinate_native[0]
                    # normalizzazione
                    plot.data2plot[:, plot.column_x] /= self.spazio_coordinate_native[2]
                    # adatto alla dimensione dell'area del plot
                    plot.data2plot[:, plot.column_x] *= (self.max_plot_square[2])
                    # traslo in base all'offset all'interno dell'area del plot
                    plot.data2plot[:, plot.column_x] += (self.max_canvas_square[2] * float(self.x_plot_area))
                    # traslo in base all'offset dell'area del plot nello schermo
                    plot.data2plot[:, plot.column_x] += self.max_canvas_square[0]
                    
                    if not plot.second_ax:

                        # stessa cosa ma per l'asse y
                        plot.data2plot[:, plot.column_y] -= self.spazio_coordinate_native[1]
                        plot.data2plot[:, plot.column_y] /= self.spazio_coordinate_native[3]
                        
                        if not self.overlap:
                            plot.data2plot[:, plot.column_y] += (1 - self.minimal_offset_data_y * 2) * plot_attivi_analizzati / numero_plot_attivi
                            
                        plot.data2plot[:, plot.column_y] *= (self.max_plot_square[3])
                        
                        # inverto i dati per avere le Y che aumentano salendo sullo schermo
                        if invert_y_coord:
                            plot.data2plot[:, plot.column_y] = self.max_canvas_square[3] * float(self.h_plot_area) - plot.data2plot[:, plot.column_y]
                        
                        plot.data2plot[:, plot.column_y] += (self.max_canvas_square[3] * float(self.y_plot_area))
                        plot.data2plot[:, plot.column_y] += self.max_canvas_square[1]
                        
                        # stessa cosa ma per errori y
                        if plot.data.shape[1] > 2:
                            plot.data2plot[:, plot.column_ey] /= self.spazio_coordinate_native[3]
                            plot.data2plot[:, plot.column_ey] *= (self.max_plot_square[3])
                    
                    elif plot.second_ax:

                        # stessa cosa ma per l'asse 2°y
                        plot.data2plot[:, plot.column_y] -= self.spazio_coordinate_native[4]
                        plot.data2plot[:, plot.column_y] /= self.spazio_coordinate_native[5]
                        
                        if not self.overlap:
                            plot.data2plot[:, plot.column_y] += (1 - self.minimal_offset_data_y * 2) * plot_attivi_analizzati / numero_plot_attivi
                            
                        plot.data2plot[:, plot.column_y] *= (self.max_plot_square[3])
                        
                        # inverto i dati per avere le Y che aumentano salendo sullo schermo
                        if invert_y_coord:
                            plot.data2plot[:, plot.column_y] = self.max_canvas_square[3] * float(self.h_plot_area) - plot.data2plot[:, plot.column_y]
                        
                        plot.data2plot[:, plot.column_y] += (self.max_canvas_square[3] * float(self.y_plot_area))
                        plot.data2plot[:, plot.column_y] += self.max_canvas_square[1]
                        
                        # stessa cosa ma per errori y
                        if plot.data.shape[1] > 2:
                            plot.data2plot[:, plot.column_ey] /= self.spazio_coordinate_native[5]
                            plot.data2plot[:, plot.column_ey] *= (self.max_plot_square[3])

                except IndexError:
                    ... 
                    
                plot_attivi_analizzati += 1


        # ticks x
        self.coords_of_ticks[0] -= self.spazio_coordinate_native[0]
        self.coords_of_ticks[0] /= (self.spazio_coordinate_native[2] + 1e-6)
        self.coords_of_ticks[0] *= (self.max_plot_square[2])
        self.coords_of_ticks[0] += (self.max_canvas_square[2] * float(self.x_plot_area))
        self.coords_of_ticks[0] += self.max_canvas_square[0]

        # ticks y
        self.coords_of_ticks[1] -= self.spazio_coordinate_native[1]
        self.coords_of_ticks[1] /= (self.spazio_coordinate_native[3] + 1e-6)
        self.coords_of_ticks[1] *= (self.max_plot_square[3])        
        if invert_y_coord:
            self.coords_of_ticks[1] = self.max_canvas_square[3] * float(self.h_plot_area) - self.coords_of_ticks[1]
        self.coords_of_ticks[1] += (self.max_canvas_square[3] * float(self.y_plot_area))
        self.coords_of_ticks[1] += self.max_canvas_square[1]
        
        # ticks 2y
        if self.second_y_axis:
            self.coords_of_ticks[2] -= self.spazio_coordinate_native[4]
            self.coords_of_ticks[2] /= (self.spazio_coordinate_native[5] + 1e-6)
            self.coords_of_ticks[2] *= (self.max_plot_square[3])        
            if invert_y_coord:
                self.coords_of_ticks[2] = self.max_canvas_square[3] * float(self.h_plot_area) - self.coords_of_ticks[2]
            self.coords_of_ticks[2] += (self.max_canvas_square[3] * float(self.y_plot_area))
            self.coords_of_ticks[2] += self.max_canvas_square[1]
        

        # Calcolo la posizione della coordinata Y=0
        # Questo permette di disegnare gradienti e assi cartesiani
        self.zero_y = 0
        self.zero_y -= self.spazio_coordinate_native[1]
        self.zero_y /= self.spazio_coordinate_native[3]
        self.zero_y *= (self.max_plot_square[3])
        
        # inverto i dati per avere le Y che aumentano salendo sullo schermo
        if invert_y_coord:
            self.zero_y = self.max_canvas_square[3] * float(self.h_plot_area) - self.zero_y
        
        self.zero_y += (self.max_canvas_square[3] * float(self.y_plot_area))
        self.zero_y += self.max_canvas_square[1]


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
                    self.max_canvas_square[0] + self.max_canvas_square[2] * float(self.x_plot_area),
                    self.max_canvas_square[1] + self.max_canvas_square[3] * float(self.y_plot_area),
                    self.max_canvas_square[2] * float(self.w_plot_area),
                    self.max_canvas_square[3] * float(self.h_plot_area),
                ])


            else:
                # area del plot coincide con lo schermo
                self.max_canvas_square = np.array([0, 0, self.screen.w, self.screen.h])
                self.max_plot_square = np.array([
                    self.max_canvas_square[2] * float(self.x_plot_area),
                    self.max_canvas_square[3] * float(self.y_plot_area),
                    self.max_canvas_square[2] * float(self.w_plot_area),
                    self.max_canvas_square[3] * float(self.h_plot_area),
                ])


    def _get_plot_area_coord(self):
        return (
            self.max_plot_square[0],
            self.max_plot_square[1],
            self.max_plot_square[0] + self.max_plot_square[2],
            self.max_plot_square[1] + self.max_plot_square[3],
        )


    def _get_native_data_bounds(self):
        self.spazio_coordinate_native = np.array([1e38, 1e38, -1e38, -1e38, 1e38, -1e38]) # Xmin, Ymin, Xmax, Ymax, 2Ymin, 2Ymax
        
        at_least_one = False
        for plot, status in zip(self.plots, self.scroll_plots.ele_mask):

            try:

                if status and self.plot_mode == 0 and not plot.second_ax:
                    at_least_one = True

                    if plot.errorbar and plot.data.shape[1] > 2:

                        # trova le coordinate minime tra tutti i grafici + errori
                        self.spazio_coordinate_native[0] = np.minimum(self.spazio_coordinate_native[0], np.min(plot.data[:, plot.column_x]))
                        self.spazio_coordinate_native[1] = np.minimum(self.spazio_coordinate_native[1], np.min(plot.data[:, plot.column_y] - plot.data[:, plot.column_ey]))
                        self.spazio_coordinate_native[2] = np.maximum(self.spazio_coordinate_native[2], np.max(plot.data[:, plot.column_x]))
                        self.spazio_coordinate_native[3] = np.maximum(self.spazio_coordinate_native[3], np.max(plot.data[:, plot.column_y] + plot.data[:, plot.column_ey]))

                    else:
                        # trova le coordinate minime tra tutti i grafici
                        self.spazio_coordinate_native[0] = np.minimum(self.spazio_coordinate_native[0], np.min(plot.data[:, plot.column_x]))
                        self.spazio_coordinate_native[1] = np.minimum(self.spazio_coordinate_native[1], np.min(plot.data[:, plot.column_y]))
                        self.spazio_coordinate_native[2] = np.maximum(self.spazio_coordinate_native[2], np.max(plot.data[:, plot.column_x]))
                        self.spazio_coordinate_native[3] = np.maximum(self.spazio_coordinate_native[3], np.max(plot.data[:, plot.column_y]))
                
                elif status and self.plot_mode == 0 and plot.second_ax:
                    at_least_one = True

                    if plot.errorbar and plot.data.shape[1] > 2:

                        # trova le coordinate minime tra tutti i grafici + errori
                        self.spazio_coordinate_native[0] = np.minimum(self.spazio_coordinate_native[0], np.min(plot.data[:, plot.column_x]))
                        self.spazio_coordinate_native[4] = np.minimum(self.spazio_coordinate_native[4], np.min(plot.data[:, plot.column_y] - plot.data[:, plot.column_ey]))
                        self.spazio_coordinate_native[2] = np.maximum(self.spazio_coordinate_native[2], np.max(plot.data[:, plot.column_x]))
                        self.spazio_coordinate_native[5] = np.maximum(self.spazio_coordinate_native[5], np.max(plot.data[:, plot.column_y] + plot.data[:, plot.column_ey]))

                    else:
                        # trova le coordinate minime tra tutti i grafici
                        self.spazio_coordinate_native[0] = np.minimum(self.spazio_coordinate_native[0], np.min(plot.data[:, plot.column_x]))
                        self.spazio_coordinate_native[4] = np.minimum(self.spazio_coordinate_native[4], np.min(plot.data[:, plot.column_y]))
                        self.spazio_coordinate_native[2] = np.maximum(self.spazio_coordinate_native[2], np.max(plot.data[:, plot.column_x]))
                        self.spazio_coordinate_native[5] = np.maximum(self.spazio_coordinate_native[5], np.max(plot.data[:, plot.column_y]))

                elif status and self.plot_mode == 1:
                    at_least_one = True

                    # trova le coordinate minime tra tutti i grafici
                    self.spazio_coordinate_native[0] = np.minimum(self.spazio_coordinate_native[0], plot.min_x) * plot.spacing_x
                    self.spazio_coordinate_native[1] = np.minimum(self.spazio_coordinate_native[1], plot.min_y) * plot.spacing_y
                    self.spazio_coordinate_native[2] = np.maximum(self.spazio_coordinate_native[2], plot.max_x) * plot.spacing_x
                    self.spazio_coordinate_native[3] = np.maximum(self.spazio_coordinate_native[3], plot.max_y) * plot.spacing_y

            except IndexError:
                ...


        if self.invert_x_axis and self.plot_mode == 0:                    
            self.spazio_coordinate_native = [self.spazio_coordinate_native[2], self.spazio_coordinate_native[1], self.spazio_coordinate_native[0], self.spazio_coordinate_native[3], self.spazio_coordinate_native[4], self.spazio_coordinate_native[5]]
        

        if sum(self.norma_perc.buttons_state) > 0:
            self.spazio_coordinate_native[1] = 0.0
           
        if self.norma_perc.buttons_state[1]:
            self.spazio_coordinate_native[3] = 100.0
            self.spazio_coordinate_native[5] = 100.0
        elif self.norma_perc.buttons_state[0]:
            self.spazio_coordinate_native[3] = 1.0
            self.spazio_coordinate_native[5] = 1.0
        
        if not self.overlap:
            self.spazio_coordinate_native[3] = 1.0 * len([active for plot, active in zip(self.plots, self.scroll_plots.ele_mask) if active and not plot.second_ax])
            self.spazio_coordinate_native[5] = 1.0 * len([active for plot, active in zip(self.plots, self.scroll_plots.ele_mask) if active and plot.second_ax])

        # ottengo i ticks belli
        if at_least_one:
            self._get_nice_ticks()

            if self.plot_mode == 0:
                
                if self.invert_x_axis:                    
                    # trova le coordinate minime tra tutti i grafici + ticks
                    self.spazio_coordinate_native[0] = np.maximum(self.spazio_coordinate_native[0], np.max(self.coords_of_ticks[0]))
                    self.spazio_coordinate_native[1] = np.minimum(self.spazio_coordinate_native[1], np.min(self.coords_of_ticks[1]))
                    self.spazio_coordinate_native[2] = np.minimum(self.spazio_coordinate_native[2], np.min(self.coords_of_ticks[0]))
                    self.spazio_coordinate_native[3] = np.maximum(self.spazio_coordinate_native[3], np.max(self.coords_of_ticks[1]))
                else:                    
                    # trova le coordinate minime tra tutti i grafici + ticks
                    self.spazio_coordinate_native[0] = np.minimum(self.spazio_coordinate_native[0], np.min(self.coords_of_ticks[0]))
                    self.spazio_coordinate_native[1] = np.minimum(self.spazio_coordinate_native[1], np.min(self.coords_of_ticks[1]))
                    self.spazio_coordinate_native[2] = np.maximum(self.spazio_coordinate_native[2], np.max(self.coords_of_ticks[0]))
                    self.spazio_coordinate_native[3] = np.maximum(self.spazio_coordinate_native[3], np.max(self.coords_of_ticks[1]))
                    


                # secondo asse
                if self.second_y_axis:
                    self.spazio_coordinate_native[4] = np.minimum(self.spazio_coordinate_native[4], np.min(self.coords_of_ticks[2]))
                    self.spazio_coordinate_native[5] = np.maximum(self.spazio_coordinate_native[5], np.max(self.coords_of_ticks[2]))

            if self.plot_mode == 1:
                # aggiungo offset per centramento dei punti al centro del pixel
                plot = [plot for plot, active in zip(self.plots, self.scroll_plots.ele_mask) if active][0]
                self.spazio_coordinate_native[0] -= plot.spacing_x / 2
                self.spazio_coordinate_native[1] -= plot.spacing_y / 2
                self.spazio_coordinate_native[2] += plot.spacing_x / 2
                self.spazio_coordinate_native[3] += plot.spacing_y / 2

                if self.mantain_proportions:
                    dimensioni = plot.data.shape

                    if self.zoom_boundaries[1] < 0:
                        self.zoom_boundaries[1] = 0
                    if self.zoom_boundaries[0] < 0:
                        self.zoom_boundaries[0] = 0
                    if self.zoom_boundaries[2] > 1:
                        self.zoom_boundaries[2] = 1
                    if self.zoom_boundaries[3] > 1:
                        self.zoom_boundaries[3] = 1

                    indice_inizio_x = dimensioni[0] * self.zoom_boundaries[0]
                    indice_inizio_y = dimensioni[1] * (1 - self.zoom_boundaries[3])
                    indice_fine_x = dimensioni[0] * self.zoom_boundaries[2]
                    indice_fine_y = dimensioni[1] * (1 - self.zoom_boundaries[1])
                        
                    fa = plot.data[int(indice_inizio_x) : int(indice_fine_x), int(indice_inizio_y) : int(indice_fine_y), :]

                    delta_x = np.max(fa[:, :, 0]) - np.min(fa[:, :, 0])
                    delta_y = np.max(fa[:, :, 1]) - np.min(fa[:, :, 1])
                    
                    rapporto = abs((delta_x + plot.spacing_x) / (delta_y + plot.spacing_y))
                    
                    if rapporto > 1:
                        self.y_plot_area = f"{float(self.y_plot_area) + float(self.size_plot_area) / 2}"
                        self.h_plot_area = f"{float(self.size_plot_area) / rapporto}"
                        self.y_plot_area = f"{float(self.y_plot_area) - float(self.size_plot_area) / 2}"
                        self.w_plot_area = f"{float(self.size_plot_area)}"
                    elif rapporto < 1:
                        self.h_plot_area = f"{float(self.size_plot_area)}"
                        self.x_plot_area = f"{float(self.x_plot_area) + float(self.size_plot_area) / 2}"
                        self.w_plot_area = f"{float(self.size_plot_area) * rapporto}"
                        self.x_plot_area = f"{float(self.x_plot_area) - float(self.size_plot_area) / 2}"


        swap_0 = self.spazio_coordinate_native[0] + (self.spazio_coordinate_native[2] - self.spazio_coordinate_native[0]) * self.zoom_boundaries[0]
        swap_1 = self.spazio_coordinate_native[1] + (self.spazio_coordinate_native[3] - self.spazio_coordinate_native[1]) * self.zoom_boundaries[1]
        swap_2 = self.spazio_coordinate_native[0] + (self.spazio_coordinate_native[2] - self.spazio_coordinate_native[0]) * self.zoom_boundaries[2]
        swap_3 = self.spazio_coordinate_native[1] + (self.spazio_coordinate_native[3] - self.spazio_coordinate_native[1]) * self.zoom_boundaries[3]

        if self.second_y_axis:    
            swap_4 = self.spazio_coordinate_native[4] + (self.spazio_coordinate_native[5] - self.spazio_coordinate_native[4]) * self.zoom_boundaries[1] 
            swap_5 = self.spazio_coordinate_native[4] + (self.spazio_coordinate_native[5] - self.spazio_coordinate_native[4]) * self.zoom_boundaries[3]


        self.spazio_coordinate_native[0] = swap_0
        self.spazio_coordinate_native[1] = swap_1
        self.spazio_coordinate_native[2] = swap_2
        self.spazio_coordinate_native[3] = swap_3
        if self.second_y_axis:    
            self.spazio_coordinate_native[4] = swap_4
            self.spazio_coordinate_native[5] = swap_5


        if at_least_one:
            self._get_nice_ticks()

            try:

                if self.invert_x_axis and self.plot_mode == 0:

                    fix = 1
                    while fix:
                        if self.coords_of_ticks[0][-1] > self.spazio_coordinate_native[0]:
                            _ = self.coords_of_ticks[0].pop()
                        else:
                            fix = 0
                
                    fix = 1
                    while fix:
                        if self.coords_of_ticks[0][0] < self.spazio_coordinate_native[2]:
                            _ = self.coords_of_ticks[0].pop(0)
                        else:
                            fix = 0
                    
                else:
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


                if self.plot_mode == 0:
                    fix = 1
                    while fix:
                        if self.coords_of_ticks[2][0] < self.spazio_coordinate_native[4]:
                            _ = self.coords_of_ticks[2].pop(0)
                        else:
                            fix = 0                
                    fix = 1
                    while fix:
                        if self.coords_of_ticks[2][-1] > self.spazio_coordinate_native[5]:
                            _ = self.coords_of_ticks[2].pop()
                        else:
                            fix = 0

            except IndexError:
                ...


        # applico lo spostamento dei dati in base all'offset minimo richiesto dagli assi cartesiani
        self.spazio_coordinate_native[0] -= (self.spazio_coordinate_native[2] - self.spazio_coordinate_native[0]) * self.minimal_offset_data_x
        self.spazio_coordinate_native[1] -= (self.spazio_coordinate_native[3] - self.spazio_coordinate_native[1]) * self.minimal_offset_data_y
        self.spazio_coordinate_native[2] += (self.spazio_coordinate_native[2] - self.spazio_coordinate_native[0]) * self.minimal_offset_data_x
        self.spazio_coordinate_native[3] += (self.spazio_coordinate_native[3] - self.spazio_coordinate_native[1]) * self.minimal_offset_data_y

        if self.second_y_axis:    
            self.spazio_coordinate_native[4] -= (self.spazio_coordinate_native[5] - self.spazio_coordinate_native[4]) * self.minimal_offset_data_y
            self.spazio_coordinate_native[5] += (self.spazio_coordinate_native[5] - self.spazio_coordinate_native[4]) * self.minimal_offset_data_y
    

        # modifica il valore della larghezza e altezza non come coordinate assolute, ma come relative al vertice iniziale
        self.spazio_coordinate_native[2] -= self.spazio_coordinate_native[0]
        self.spazio_coordinate_native[3] -= self.spazio_coordinate_native[1]
        self.spazio_coordinate_native[5] -= self.spazio_coordinate_native[4]


    def import_plot_data(self, path: str, divisore: str = None, separatore_decimale=".", image=False, retry_on_fail=True) -> None:
        
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
        
        if os.path.isdir(path):
            for new_path in [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
                self.import_plot_data(new_path, divisore, separatore_decimale, image, retry_on_fail)
            return
        

        # strange format types (.tif)
        if self.data_path.endswith((".tif", ".tiff")):
                
            import tifffile
            with tifffile.TiffFile(self.data_path) as tif:

                # save image data (pixels)
                image_data = tif.asarray()

                # save TAGS
                tif_tags: dict = {}
                for tag in tif.pages[0].tags.values():
                    name, value = tag.name, tag.value
                    tif_tags[name] = value

            # HEADER SECTION (AFM) -------------------------------
            import pspylib.tiff as tiff
            reader = tiff.TiffReader(self.data_path)

            a: dict = reader.data.scanHeader.scanHeader

            for i in range(len(list(a.keys()))):
                b = list(a.values())[i][0]
                if list(a.values())[i][1] == 'uint16':
                    c = chr(b[0])
                    for j in range(1,len(b)):
                        if chr(b[j]) != 0:
                            c = '{}{}'.format(c,chr(b[j]))
                if list(a.values())[i][1] == 'int32':
                    c = b
                if list(a.values())[i][1] == 'double64':
                    c = b
                
                # string cleaning from null characters 
                if type(c) == str:
                    c: str = c.replace('\x00', '')
                
                # important data savings (template)
                # if list(a.keys())[i] == "tag":
                #     save_var = c
            # HEADER SECTION (AFM) -------------------------------

            w, h = tif_tags["ImageLength"], tif_tags["ImageWidth"]

            # TRYING OUTPUT SEM DATA        
            try:
                converted = tif_tags["50431"].decode('utf-8', errors='replace')
                print(f"SEM stuff:\n{converted}\n{GREEN}SpacingX -> {converted[converted.find('PixelSizeX'):converted.find('PixelSizeX') + 27]}\nSpacingY -> {converted[converted.find('PixelSizeY'):converted.find('PixelSizeY') + 27]}{RESET}")
            except Exception as e:
                print(f"{e}\n\nNon riesco a caricare dati relativi al SEM (probabilmente non è un'immagine SEM)")
            
            # TRYING OUTPUT AFM DATA
            try:
                print("AFM stuff:\n")
                for key, value in a.items():
                    print(f"{key}={value[0]}")
                print(f"{GREEN}SpacingX -> {a['scanSizeWidth'][0] / a['width'][0]}")
                print(f"SpacingY -> {a['scanSizeHeight'][0] / a['height'][0]}{RESET}")
            except Exception as e:
                print(f"{e}\n\nNon riesco a caricare dati relativi all'AFM (probabilmente non è un'immagine AFM)")


            # ADAPT DATA FOR POMOPLOT -----------------------------------------------------------
            x_ind, y_ind = np.indices((w, h))

            risultato = np.stack((y_ind, x_ind, image_data), axis=-1)
            risultato = risultato[::-1, :, :]
            risultato = risultato.reshape(-1, 3)
            risultato = np.array(risultato, dtype=np.float64)

            nome = path.split('\\')[-1]
            nome = nome.split('/')[-1]

            self.update_plot_list(_Single2DPlot(f"2D{nome}", risultato, ""))

            return


        # SUPPORTO .CSV
        if self.data_path.endswith(".csv") or self.data_path.endswith(".CSV") and divisore is None: self.divisore = ","
        
        # SUPPORTO .dpt
        if self.data_path.endswith(".dpt"): self.divisore = ","

        # estrazione data
        try:
            with open(self.data_path, 'r') as file:
                data = [line for line in file]
        except UnicodeDecodeError:
            return

        # SUPPORTO FORMATO HEX utf-16-le
        if data[0].startswith(r"ÿþ"): 
            import codecs
            with codecs.open(self.data_path, 'r', encoding='utf-16-le') as file:
                data = [line.strip() for line in file]

        if separatore_decimale != ".":
            data = [i.replace(separatore_decimale, ".") for i in data]
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

                    if len(coordinate) == 1:
                        raise ValueError

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

            if data.shape[1] == 3 and image:
                self.update_plot_list(_Single2DPlot(f"2D{nome}", data, metadata_lst))
                self.scroll_plots2D.ele_selected_index = len(self.scroll_plots2D.elementi) - 1
            
            elif not image:
                # test ordinamento x
                indici = np.argsort(data[:, 0])
                data = data[indici]

                self.update_plot_list(_Single1DPlot(nome, data, metadata_lst))
                self.scroll_plots1D.ele_selected_index = len(self.scroll_plots1D.elementi) - 1

        except Exception as e:
            if (self.data_path.endswith(".csv") or self.data_path.endswith(".CSV")) and retry_on_fail: 
                self.import_plot_data(path, ";", separatore_decimale=",", retry_on_fail=False)
            else:
                print(f"Impossibile caricare il file: {path}\n{e}")


class _Single1DPlot:
    def __init__(self, nome, data, metadata):
        
        self.nome = nome
        self.metadata = metadata

        self.data = data

        self.data2plot: np.ndarray[float] = None

        self.column_x = 0
        self.column_y = 1
        self.column_ey = 2

        self.scatter = True
        self.scatter_width = 3
        self.scatter_border = 0
        self.function = True
        self.function_width = 2
        self.dashed = False
        self.dashed_traits = 99
        self.errorbar = True if data.shape[1] > 2 else False

        self.gradiente = False
        self.grad_mode = "ori"

        self.second_ax = False

        self.display_coords = []

        self.function_color = np.array([np.random.randint(50, 180), np.random.randint(50, 200), np.random.randint(50, 200)])
        self.scatter_color = self.function_color + 55


    def __str__(self):
        return f"{self.nome}"
    

    def __repr__(self):
        return f"{self.nome}"
    

class _Single2DPlot:
    def __init__(self, nome, data_input, metadata) -> None:
        
        # lettura dei dati: format da rispettare lettura standard da sinistra verso destra e a fine linea vado a capo: alta frequenze sulle X, bassa frequenza sulle Y

        # data
        self.nome = nome
        self.data = data_input
        self.data2plot = data_input

        self.colore_base2 = np.array([68, 1, 84], dtype=(np.float64))
        self.colore_base1 = np.array([253, 231, 37], dtype=(np.float64))
        self.prev_colore_base2 = np.array([68, 1, 84], dtype=(np.float64))
        self.prev_colore_base1 = np.array([253, 231, 37], dtype=(np.float64))
        self.flip_y = False
        self.flip_x = False

        # calcolo dimensione array
        indici = self.data[:, :2].copy()
    
        indici[:, 0] -= np.min(indici[:, 0])
        indici[:, 0] /= np.max(indici[:, 0])

        indici[:, 1] -= np.min(indici[:, 1])
        indici[:, 1] /= np.max(indici[:, 1])

        self.dim_x = len(np.unique(indici[:, 1]))   # FIX -> Dimension given by the wrong dimension
        self.dim_y = len(np.unique(indici[:, 0]))   # FIX -> Dimension given by the wrong dimension

        self.data = self.data.reshape(self.dim_x, self.dim_y, 3) 

        # calcolo dell'array di coordinate
        self.data = self.data.transpose(1, 0, 2)
        self.data = self.data[:, ::-1, :]

        
        self.spacing_x = abs(self.data[0, 0, 0] - self.data[1, 0, 0])
        self.spacing_y = abs(self.data[0, 0, 1] - self.data[0, 1, 1])

        self.dim_x = self.data.shape[0]
        self.dim_y = self.data.shape[1]
        self.w_div_h = self.dim_x / self.dim_y

        self.previous_final_shape = None
        self.max_x = np.max(self.data[:, :, 0])
        self.min_x = np.min(self.data[:, :, 0])
        self.max_y = np.max(self.data[:, :, 1])
        self.min_y = np.min(self.data[:, :, 1])
        self.previous_max_z = np.max(self.data[:, :, 2])
        self.previous_min_z = np.min(self.data[:, :, 2])


    def __str__(self):
        return f"{self.nome}"
    

    def __repr__(self):
        return f"{self.nome}"
    

class Molecule:
    def __init__(self, id, code, x, y, size):
        self.nome = id
        self.code = code
        self.x = x
        self.y = y
        self.size = size


    def __str__(self):
        return f"Molecola {self.nome}: {self.code[:30]}"


    def __repr__(self):
        return f"Molecola {self.nome}: {self.code[:30]}"


# COMPILED FUNCTIONS
def colora_array(data, color1, color2, max_z, min_z):
    # disegna la mappa a colori
    fa_norm = (data - min_z) / (max_z - min_z)

    color_delta = color2 - color1

    array_finale = heavy_calc(fa_norm, color1, color_delta)

    return array_finale.astype(np.uint8)


@njit()
def heavy_calc(fa_norm, color1, color_delta):
    return np.add(color1, np.multiply(fa_norm[..., None], color_delta))
