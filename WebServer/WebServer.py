from core import create_app
from core.instance.config import FlaskConfig

app = create_app()

if __name__ == '__main__':
    flask = FlaskConfig()