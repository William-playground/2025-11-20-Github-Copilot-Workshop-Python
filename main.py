from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """ポモドーロタイマーのメインページ"""
    return render_template('index.html')

if __name__ == '__main__':
    # For production, set debug=False. Use environment variable to control debug mode.
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
