from app import app
import os
from livereload import Server

if __name__ == '__main__':
    # Enable debug mode
    app.debug = True
    
    # Create LiveReload server
    server = Server(app.wsgi_app)

    # Watch for changes in template directory
    server.watch('templates/')
    
    # Watch for changes in Python files
    server.watch('*.py')
    
    # Run the development server
    server.serve(port=5001, host='127.0.0.1') 