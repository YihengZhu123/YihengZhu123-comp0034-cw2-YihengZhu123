from blogapp import create_app

if __name__ == "__main__":
    # use default DevelopmentConfig
    app = create_app()

    app.run(debug=False)