from silvapermaculture import create_app, db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':  #The condition is true if we run the script directly.
    app.run(debug=False)
