def main():

    try:

        from GRAFICA._modulo_UI import UI
        from PLOTS.pomoplot import PomoPlot

        app = UI()
        plot = PomoPlot()
        plot.link_ui(app)
        # plot.import_plot_data("C:\\users\\aless\\desktop\\default\\led_corrente_V_interpolazione.txt")
        # plot.import_plot_data("C:\\users\\aless\\desktop\\default\\spettro_3v.txt")
        # plot.import_plot_data("C:\\users\\aless\\desktop\\default\\polarizzazione_diretta.txt")
        # plot.import_plot_data("C:\\users\\aless\\desktop\\default\\polarizzazione_inversa.txt")
        
        while app.running:
            app.start_cycle()

            plot.plot(app.logica)

            app.end_cycle()

        UI.graceful_quit()

    except Exception:

        RESET = "\033[0m"  # Reset dei colori
        RED = "\033[31m"   # Testo rosso
        GREEN = "\033[32m" # Testo verde

        import traceback

        UI.graceful_quit()

        # Get the formatted traceback as a string
        traceback_info = traceback.format_exc(chain=1)

        traceback_info = traceback_info.split("\\")[-1]
        traceback_info = traceback_info.split("/")[-1]

        traceback_info = traceback_info.replace('"', "", 1)
        traceback_info = traceback_info.replace('\n', "\n\n", 1)

        traceback_info = traceback_info[:traceback_info.find("line")] + GREEN + traceback_info[traceback_info.find("line") : traceback_info.find(", in ")] + RESET + traceback_info[traceback_info.find(", in "):]
        
        print(f"\n\n\n{RED}ATTENZIONE PROGRAMMA ARRESTATO!{RESET}\n\n{traceback_info}\n\n")
        input("Premi un tasto qualsiasi per uscire...")


if __name__ == "__main__":

    PROFILATORE = 0

    if PROFILATORE:
        import yappi
        yappi.start()

    main()
    
    if PROFILATORE:
        yappi.stop()
        func_stats = yappi.get_func_stats()
        func_stats.save('profilatore.prof', type='pstat')
