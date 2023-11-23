from flask import Flask, render_template, request, jsonify
from urllib.parse import parse_qs
import os

class Server:

    PRESET_IMG_LOCATION = "static/preset_images"

    app = Flask(__name__)

    backend = None
    ui = None

    @staticmethod
    @app.route('/')
    def index():
        # TODO: Cleanup
        return render_template('index.html', leds=Server.backend.leds,
                               presets=Server.backend.presets.load_last_presets(),
                               curr_preset=Server.backend.get_curr_preset(),
                               get_image_url_for_preset=Server.get_image_url_for_preset,
                               animations=['static', 'random', 'sth_else'],
                               Server=Server)

    @staticmethod
    @app.route('/update', methods=['POST'])
    def update_slider():
        index = int(request.form['index'])
        value = int(request.form['value'])
        if 0 <= index < len(Server.backend.leds):
            Server.backend.leds[index].brightness = value
            return f"Brightness updated for {Server.backend.leds[index].name}"
        return f"Invalid index: {index}"

    @staticmethod
    @app.route('/updateColor', methods=['POST'])
    def update_color():
        index = int(request.form['index'])
        color_value = request.form['value']
        if 0 <= index < len(Server.backend.leds):
            Server.backend.leds[index].color = color_value
            return f"Color updated for {Server.backend.leds[index].name}"
        return f"Invalid index: {index}"

    @staticmethod
    @app.route('/updateAnimation', methods=['POST'])
    def update_animation():
        index = int(request.form['index'])
        animation_name = request.form['value']
        if 0 <= index < len(Server.backend.leds):
            Server.backend.leds[index].animation = animation_name
            return f"Animation updated for {Server.backend.leds[index].name} to {animation_name}"
        return f"Invalid index: {index}"


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

    @staticmethod
    @app.route('/markSelected', methods=['POST'])
    def markSelectedPreset():
        preset_name = request.form['name']
        if Server.backend.presets.markAsSelected(preset_name):
            return jsonify(success=True)
        return jsonify(success=False, message=f"Error Marking preset as selected! Already marked?")

    @staticmethod
    @app.route('/unmarkSelected', methods=['POST'])
    def unmarkSelectedPreset():
        preset_name = request.form['name']
        if Server.backend.presets.unmarkAsSelected(preset_name):
            return jsonify(success=True)
        return jsonify(success=False, message=f"Error UnMarking preset as selected! Already unmarked?")

    @staticmethod
    @app.route('/getSelectedPresets', methods=['GET'])
    def load_selected_presets():
        print("Called")
        presets = Server.backend.presets.load_selected_presets()
        #presets = ["clone_" + x.strip() for x in presets]
        presets = [x.strip() for x in presets]
        return jsonify(success=True, message=f"{presets}")

    @staticmethod
    def get_image_url_for_preset(preset_name):

        if not os.path.exists(f"{Server.PRESET_IMG_LOCATION}/{preset_name}.jpg"):
            ok = Server.backend.presets.create_preset_img(preset_name)
        else:
            ok = True

        if ok:
            return f"/{Server.PRESET_IMG_LOCATION}/{preset_name}.jpg"
        return f"/{Server.PRESET_IMG_LOCATION}/no_img.jpg"

    @staticmethod
    def get_curr_preset_car_img(preset_name):

        need_path = f"/static/car_icon_{preset_name}.jpg"
        if not os.path.exists(need_path):
            ok = Server.backend.presets.create_car_icon_preset(preset_name)
        else:
            ok = True

        if ok:
            return need_path
        return f"/static/car_icon_default.jpg"



if __name__ == '__main__':
   Server.app.run(debug=True)

