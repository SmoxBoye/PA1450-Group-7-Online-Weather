"""Application entry point."""
from application import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='192.168.1.13', port="8080", debug=True)
