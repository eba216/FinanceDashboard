#! /usr/bin/env python 
import os

from app import create_app 

app = create_app()
app.config["SECRET_KEY"] = os.urandom(24).hex()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)