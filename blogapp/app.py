from blogapp import create_app
from blogapp.config import DevelopmentConfig
from werkzeug.middleware.dispatcher import DispatcherMiddleware

if __name__ == "__main__":
    app = create_app(config_class_name=DevelopmentConfig)

    app.run(debug=False)