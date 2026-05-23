# app.py
"""Main entry point of the Synchronized Bazar Store desktop suite.
Can be run in desktop GUI mode or dev server mode using `--server-only`.
"""

import sys
from backend import create_app

app = create_app()

if __name__ == '__main__':
    # Parse command line arguments
    if '--server-only' in sys.argv:
        print("Starting Sync Bazar in Dev Server Mode...")
        app.run(host='127.0.0.1', port=5000, debug=True)
    else:
        print("Starting Sync Bazar in Desktop App Mode...")
        from flaskwebgui import FlaskUI
        # Instantiating FlaskUI running on Flask backend
        ui = FlaskUI(app=app, width=1280, height=800)
        ui.run()
