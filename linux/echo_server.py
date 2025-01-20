import socket
import threading
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler
from io import BytesIO
from http import HTTPStatus


class HTTPRequestParser(BaseHTTPRequestHandler):
    """Парсинг HTTP-запросов для заголовков и методов"""
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = None
        self.error_message = None
        self.parse_request()

    def send_error(self, code, message=None, explain=None):
        """Подавляем вывод ошибок от BaseHTTPRequestHandler"""
        pass


def handle_client_connection(client_socket, client_address):
    """Обрабатывает соединение с клиентом в отдельном потоке"""
    try:
        # Получаем данные от клиента
        request_data = client_socket.recv(1024)
        if not request_data:
            return

        # Парсим запрос
        request = HTTPRequestParser(request_data)
        method = request.command
        path = request.path
        headers = {k: v for k, v in request.headers.items()}

        # Обрабатываем параметры запроса
        parsed_url = urlparse(path)
        query_params = parse_qs(parsed_url.query)
        status_code = query_params.get("status", ["200"])[0]

        try:
            # Преобразуем статус-код в сообщение
            status_code = int(status_code)
            status_message = HTTPStatus(status_code).phrase
        except (ValueError, KeyError):
            # Если статус некорректный, возвращаем "200 OK"
            status_code = 200
            status_message = HTTPStatus(200).phrase

        # Формируем тело ответа
        response_body = [
            f"Request Method: {method}",
            f"Request Source: {client_address}",
            f"Response Status: {status_code} {status_message}",
        ]
        response_body.extend(f"{k}: {v}" for k, v in headers.items())

        # Если запрос POST/PUT, добавляем тело
        if method in ("POST", "PUT"):
            content_length = int(headers.get("Content-Length", 0))
            body = request.rfile.read(content_length).decode("utf-8")
            response_body.append(f"Request Body: {body}")

        response_body = "\r\n".join(response_body)

        # Формируем HTTP-ответ
        response = (
            f"HTTP/1.1 {status_code} {status_message}\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
            "Connection: close\r\n\r\n"
            f"{response_body}"
        )

        # Отправляем ответ клиенту
        client_socket.sendall(response.encode("utf-8"))
    except Exception as e:
        print(f"Ошибка обработки запроса: {e}")
    finally:
        # Закрываем соединение с клиентом
        client_socket.close()


def start_server(host="127.0.0.1", port=5000, max_threads=15):
    """Запускает многопоточный сервер"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(max_threads)

    print(f"Сервер запущен на {host}:{port}")
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Подключился клиент: {client_address}")
            # Запускаем новый поток для обработки клиента
            client_thread = threading.Thread(
                target=handle_client_connection,
                args=(client_socket, client_address),
                daemon=True
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("Сервер остановлен")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
