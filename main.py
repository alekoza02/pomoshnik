def main():

    from GRAFICA._modulo_UI import UI
    from PLOTS.pomoplot import PomoPlot

    app = UI()
    plot = PomoPlot()
    plot.link_ui(app)
    # plot.import_plot_data(r"C:\Users\aless\Desktop\default\spettro_3v.txt")

    while app.running:

        app.start_cycle()

        plot.update()
        plot.plot(app.logica)

        app.end_cycle()


if __name__ == "__main__":

    main()