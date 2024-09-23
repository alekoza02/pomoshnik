def main():

    from GRAFICA._modulo_UI import UI
    
    app = UI()

    while app.running:

        app.start_cycle()

        ...

        app.end_cycle()



if __name__ == "__main__":

    main()