from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), nullable=False)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    room = db.Column(db.String(20))
    updated_at = db.Column(db.DateTime, server_default=db.func.now())


# Создаём таблицы
with app.app_context():
    db.create_all()



@app.route('/api/position', methods=['GET', 'POST'])
def update_position():
    if request.method == 'POST':
        data = request.json
    else:  # Если GET
        data = request.args

    device_id = data.get('device_id')
    lat = data.get('lat')
    lon = data.get('lon')

    try:
        data = request.json
        device_id = data.get('device_id')
        lat = data.get('lat')
        lon = data.get('lon')

        if None in (device_id, lat, lon):
            return jsonify({"error": "Missing required fields"}), 400

        room = "101"  # Заглушка
        new_device = Device(device_id=device_id, lat=lat, lon=lon, room=room)

        db.session.add(new_device)
        db.session.commit()

        return jsonify({'status': 'ok'})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# API для фронтенда
@app.route('/api/devices', methods=['GET'])
def get_devices():
    devices = Device.query.order_by(Device.updated_at.desc()).all()
    devices_data = [{
        'device_id': d.device_id,
        'lat': d.lat,
        'lon': d.lon,
        'room': d.room
    } for d in devices]
    return jsonify(devices_data)

CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)