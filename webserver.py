import os
import socket
import subprocess
import shutil
import platform
import sys


HOST = 'localhost'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080 
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

def install_php():
    """Cài đặt PHP nếu chưa có, dựa trên hệ điều hành hiện tại."""
    os_name = platform.system()
    try:
        if os_name == "Windows":
            print("Đang cài đặt PHP trên Windows...")
            subprocess.run(["choco", "install", "php", "-y"], check=True)
        elif os_name == "Darwin":
            print("Đang cài đặt PHP trên macOS...")
            subprocess.run(["brew", "install", "php"], check=True)
        elif os_name == "Linux":
            print("Đang cài đặt PHP trên Linux...")
            if shutil.which("apt"):
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "php"], check=True)
            elif shutil.which("yum"):
                subprocess.run(["sudo", "yum", "install", "-y", "php"], check=True)
        else:
            print("Hệ điều hành không được hỗ trợ tự động cài PHP.")
    except subprocess.CalledProcessError as e:
        print(f"Lỗi cài đặt PHP: {e}")

def get_php_path():
    """Kiểm tra và trả về đường dẫn PHP nếu có, hoặc tiến hành cài đặt nếu cần."""
    php_path = shutil.which("php")
    if not php_path:
        print("PHP chưa được cài đặt. Đang tiến hành cài đặt...")
        install_php()
        php_path = shutil.which("php")
    return php_path

def handle_php(file_path, php_path):
    """Thực thi tệp PHP và trả về kết quả."""
    try:
        result = subprocess.run([php_path, file_path], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else f"PHP Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

def find_file(requested_file):
    """Tìm tệp theo đường dẫn yêu cầu."""
    file_path = os.path.join(PROJECT_ROOT, requested_file.lstrip('/'))
    print(f"Tìm kiếm file: {file_path}")
    return file_path if os.path.exists(file_path) else None

def start_server():
    """Khởi chạy server và xử lý các yêu cầu."""
    php_path = get_php_path()
    if not php_path:
        print("Không thể tìm thấy hoặc cài đặt PHP.")
        return

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

                
                request_line = request.splitlines()[0]
                requested_file = request_line.split(" ")[1]

                
                if requested_file == '/':
                    requested_file = '/index.html'

                
                file_path = find_file(requested_file)

                if file_path:
                    # Kiểm tra nếu file là PHP
                    if file_path.endswith(".php"):
                        print(f"Xử lý file PHP: {file_path}")
                        php_output = handle_php(file_path, php_path)
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

# Khởi động server
start_server()
