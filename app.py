"""
Flask wrapper for Maze Game
Provides web interface and launches the Pygame game
"""

from flask import Flask, render_template_string, jsonify
from flask_cors import CORS
import subprocess
import os
import sys

app = Flask(__name__)
CORS(app)

# Get the directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    """Serve the game interface page"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Maze Game</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                text-align: center;
            }
            h1 {
                font-size: 3em;
                margin-bottom: 20px;
                color: #333;
            }
            .icon {
                font-size: 5em;
                margin-bottom: 20px;
            }
            p {
                color: #666;
                line-height: 1.8;
                margin-bottom: 30px;
                font-size: 1.1em;
            }
            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 40px;
                font-size: 1.2em;
                border-radius: 10px;
                cursor: pointer;
                transition: transform 0.3s, box-shadow 0.3s;
                text-decoration: none;
                display: inline-block;
                margin: 10px;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            }
            .info-box {
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 20px;
                margin: 20px 0;
                text-align: left;
                border-radius: 5px;
            }
            .info-box h3 {
                color: #667eea;
                margin-bottom: 10px;
            }
            .info-box ul {
                margin-left: 20px;
                color: #666;
            }
            .info-box li {
                margin: 8px 0;
            }
            .status {
                margin-top: 20px;
                padding: 15px;
                border-radius: 10px;
                font-weight: 600;
            }
            .status.success {
                background: #d4edda;
                color: #155724;
            }
            .status.error {
                background: #f8d7da;
                color: #721c24;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="icon">🎮</div>
            <h1>Maze Game</h1>
            <p>Navigate through procedurally generated mazes to reach the exit!</p>
            
            <button class="btn" onclick="launchGame()">🚀 Launch Game</button>
            <a href="/api/status" class="btn" style="background: #6c757d;">ℹ️ Game Info</a>
            
            <div class="info-box">
                <h3>How to Play</h3>
                <ul>
                    <li><strong>WASD</strong> or <strong>Arrow Keys</strong>: Move your player</li>
                    <li><strong>Goal</strong>: Reach the yellow exit square</li>
                    <li><strong>R</strong>: Restart after winning</li>
                    <li><strong>ESC</strong>: Quit the game</li>
                </ul>
            </div>
            
            <div class="info-box">
                <h3>Features</h3>
                <ul>
                    <li>Procedurally generated mazes</li>
                    <li>Unique maze every game</li>
                    <li>Smooth controls</li>
                    <li>Simple, fun gameplay</li>
                </ul>
            </div>
            
            <div id="status"></div>
        </div>
        
        <script>
            async function launchGame() {
                const statusDiv = document.getElementById('status');
                statusDiv.innerHTML = '<div class="status">Launching game...</div>';
                
                try {
                    const response = await fetch('/api/launch', {
                        method: 'POST'
                    });
                    const data = await response.json();
                    
                    if (data.success) {
                        statusDiv.innerHTML = '<div class="status success">✅ Game launched! Check your screen for the game window.</div>';
                    } else {
                        statusDiv.innerHTML = '<div class="status error">❌ ' + data.error + '</div>';
                    }
                } catch (error) {
                    statusDiv.innerHTML = '<div class="status error">❌ Error: ' + error.message + '</div>';
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route('/api/status')
def status():
    """Get game status and information"""
    return jsonify({
        'name': 'Maze Game',
        'type': 'desktop',
        'description': 'A Python-based maze game built with Pygame',
        'status': 'ready',
        'features': [
            'Procedural maze generation',
            'Smooth player controls',
            'Win condition',
            'Simple, fun gameplay'
        ]
    })


@app.route('/api/launch', methods=['POST'])
def launch():
    """Launch the Pygame game"""
    try:
        # Get the path to main.py
        main_py = os.path.join(BASE_DIR, 'main.py')
        
        # Activate venv and run the game
        venv_python = os.path.join(BASE_DIR, 'venv', 'bin', 'python3')
        
        if not os.path.exists(venv_python):
            # Fallback to system python
            venv_python = 'python3'
        
        # Launch game in background
        subprocess.Popen(
            [venv_python, main_py],
            cwd=BASE_DIR,
            start_new_session=True
        )
        
        return jsonify({
            'success': True,
            'message': 'Game launched successfully!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5107))
    print(f"🎮 Maze Game Web Interface")
    print(f"📊 Running on http://localhost:{port}")
    print(f"💡 Use the 'Launch Game' button to start the Pygame game")
    app.run(host='0.0.0.0', port=port, debug=False)
