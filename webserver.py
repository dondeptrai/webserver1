import os
import socket
import subprocess
import sys

# Đảm bảo đầu ra được mã hóa bằng utf-8
sys.stdout.reconfigure(encoding='utf-8')
HOST, PORT = 'localhost', 8080

# Lấy đường dẫn của thư mục hiện tại
PROJECT_ROOT = os.getcwd()


def get_mime_type(file_path):
    """Xác định loại MIME dựa trên phần mở rộng của tệp."""
    if file_path.endswith(".html"):
        return "text/html"
    elif file_path.endswith(".css"):
        return "text/css"
    elif file_path.endswith(".js"):
        return "application/javascript"
    elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
        return "image/jpeg"
    elif file_path.endswith(".png"):
        return "image/png"
    elif file_path.endswith(".gif"):
        return "image/gif"
    elif file_path.endswith(".svg"):
        return "image/svg+xml"
    elif file_path.endswith(".ico"):
        return "image/x-icon"
    return "text/plain"


def find_file(requested_file):
    """Tìm tệp theo đường dẫn yêu cầu."""
    file_path = os.path.join(PROJECT_ROOT, requested_file.lstrip('/'))
    print(f"Tìm kiếm file: {file_path}")
    return file_path if os.path.exists(file_path) else None


def handle_php(file_path):
    """Thực thi tệp PHP và trả về kết quả."""
    try:
        # Sử dụng php-cgi để thực thi file PHP và lấy kết quả trả về
        result = subprocess.run([r"/usr/local/bin/php", file_path], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout  # Trả về kết quả thực thi PHP
        else:
            return f"PHP Error: {result.stderr}"  # Nếu có lỗi, trả về lỗi
    except Exception as e:
        return f"Error: {str(e)}"  # Nếu có ngoại lệ, trả về lỗi


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Đang phục vụ trên cổng {PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        with client_socket:
            print(f"Kết nối từ {client_address}")
            request = client_socket.recv(1024).decode()
            print(f"Yêu cầu: {request}")

            # Xử lý dòng yêu cầu
            request_line = request.splitlines()[0]
            requested_file = request_line.split(" ")[1]

            # Nếu yêu cầu là "/", trả về file index.html
            if requested_file == '/':
                requested_file = '/index.html'

            # Tìm file trên hệ thống
            file_path = find_file(requested_file)

            if file_path:
                # Kiểm tra nếu file là PHP
                if file_path.endswith(".php"):
                    print(f"Xử lý file PHP: {file_path}")
                    # Xử lý file PHP bằng php-cgi
                    php_output = handle_php(file_path)
                    response = f'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n{php_output}'.encode()
                else:
                    # Đọc và trả về file tĩnh
                    mime_type = get_mime_type(file_path)
                    with open(file_path, 'rb') as file:
                        file_content = file.read()
                    response = f'HTTP/1.1 200 OK\nContent-Type: {mime_type}\n\n'.encode() + file_content
            else:
                # Nếu file không tồn tại, trả về 404
                print(f"File không tồn tại: {requested_file}")
                response = 'HTTP/1.1 404 NOT FOUND\n\nPage Not Found'.encode()

            # Gửi phản hồi đến client
            client_socket.sendall(response)