from silvapermaculture import create_app

app = create_app()


if __name__ == '__main__':  #The condition is true if we run the script directly.
    app.run(debug=True)
