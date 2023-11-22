from flask import Flask, render_template, request, jsonify
from urllib.parse import parse_qs


class Server:

    app = Flask(__name__)

    backend = None
    ui = None

    @staticmethod
    @app.route('/')
    def index():
        return render_template('index.html', leds=Server.backend.leds,
                               presets=Server.backend.presets.load_last_presets(),
                               curr_preset=Server.backend.get_curr_preset())

    @staticmethod
    @app.route('/update', methods=['POST'])
    def update_slider():
        index = int(request.form['index'])
        value = int(request.form['value'])
        if 0 <= index < len(Server.backend.leds):
            Server.backend.leds[index].brightness = value
            return "Slider updated"
        return "Invalid index"

    @staticmethod
    @app.route('/updateColor', methods=['POST'])
    def update_color():
        index = int(request.form['index'])
        color_value = request.form['value']
        if 0 <= index < len(Server.backend.leds):
            Server.backend.leds[index].color = color_value
            return "Color updated"
        return "Invalid index"

    @staticmethod
    @app.route('/savePreset', methods=['POST'])
    def save_preset():
        preset_name = request.form['name']
        Server.backend.presets.save_preset(preset_name, Server.backend.leds)
        return f"Preset '{preset_name}' saved successfully!"

    @staticmethod
    @app.route('/loadPreset', methods=['POST'])
    def load_preset():
        preset_name = request.form['name']
        if Server.ui.ledScreen.toggle_button(preset_name):
        #if Server.backend.presets.load_preset(preset_name, Server.backend.leds):
            return jsonify(success=True)
        return jsonify(success=False, message=f"Preset '{preset_name}' not found.")

    @staticmethod
    @app.route('/deletePreset', methods=['POST'])
    def delete_preset():
        preset_name = request.form['name']
        if Server.backend.presets.delete_preset(preset_name):
            return jsonify(success=True)
        return jsonify(success=False, message=f"No preset found with name '{preset_name}'!")

    @staticmethod
    @app.route('/toggleExhaustFlap', methods=['POST'])
    def toggle_exhaust_flap():
        if Server.ui.flapScreen.toggle_button("Exhaust Flap"):
            return jsonify(success=True)
        return jsonify(success=False, message=f"Error toggling Exhaust flap button!")

if __name__ == '__main__':
   Server.app.run(debug=True)
