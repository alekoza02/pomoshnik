def main():

    from GRAFICA._modulo_UI import UI
    
    app = UI()

    while app.running:

        app.start_cycle()

        # DEBUG ZONE
        # app.costruttore.scene["main"].label["vis"].testo = f"{app.costruttore.scene["main"].entrate["entrata"].testo}"
        # DEBUG ZONE

        app.end_cycle()



if __name__ == "__main__":

    main()