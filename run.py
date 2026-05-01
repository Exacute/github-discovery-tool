import os
import sys
from app import create_app
from app.routes import register_blueprints

app = create_app()
register_blueprints(app)

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
