from app import create_app
from app.monitoring.monitoring_engine import start_monitoring_engine

app = create_app()

if __name__ == "__main__":
    start_monitoring_engine()
    app.run(debug=True)
