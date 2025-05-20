import socketserver
import requests

class GPSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        raw_data = self.request.recv(1024).strip()
        print(f"Получены данные: {raw_data}")

        # 🔧 Здесь нужно будет парсить реальные координаты из raw_data
        # Пока сделаем заглушку для проверки интеграции с Flask
        device_id = "gf22-test"
        lat = 47.8253
        lon = 16.5137

        try:
            # Отправка данных во Flask API
            response = requests.post("http://localhost:5000/api/position", json={
                "device_id": device_id,
                "lat": lat,
                "lon": lon
            })
            print(f"Ответ Flask API: {response.status_code} {response.text}")
        except Exception as e:
            print(f"Ошибка при отправке в Flask: {e}")

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9000
    print(f"TCP-сервер запущен на {HOST}:{PORT}")
    with socketserver.TCPServer((HOST, PORT), GPSHandler) as server:
        server.serve_forever()
