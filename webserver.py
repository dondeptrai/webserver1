import os
import socket
import subprocess
import sys
import shutil
import platform

sys.stdout.reconfigure(encoding='utf-8')
HOST, START_PORT = 'localhost', 8080
PROJECT_ROOT = os.getcwd()

def check_port_in_use(port):
    """Kiểm tra xem cổng đã được sử dụng chưa và hiển thị dịch vụ sử dụng cổng đó."""
    try:
        result = subprocess.run(
            ["lsof", "-i", f":{port}"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None

def find_available_port(start_port=START_PORT):
    """Tìm cổng trống bằng cách kiểm tra từ cổng ban đầu và tăng dần nếu cổng đã bị chiếm."""
    port = start_port
    while check_port_in_use(port):
        print(f"Cổng {port} đã bị chiếm, thử cổng {port + 1}...")
        port += 1
    return port

def install_php():
    """Cài đặt PHP dựa trên hệ điều hành hiện tại."""
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
    """Xác định đường dẫn PHP."""
    php_path = shutil.which("php")
    if php_path:
        print(f"PHP đã được cài đặt tại: {php_path}")
        return php_path
    else:
        print("PHP chưa được cài đặt. Đang tiến hành cài đặt...")
        install_php()
        php_path = shutil.which("php")
        if php_path:
            print(f"PHP đã được cài đặt thành công tại: {php_path}")
            return php_path
        else:
            print("Không thể cài đặt PHP tự động. Vui lòng cài đặt thủ công.")
            return None

def handle_php(file_path):
    """Thực thi tệp PHP và trả về kết quả."""
    php_path = get_php_path()
    if php_path is None:
        return "Không tìm thấy PHP trên hệ điều hành này."
    
    try:
        result = subprocess.run([php_path, file_path], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Lỗi PHP: {result.stderr}"
    except Exception as e:
        return f"Lỗi: {str(e)}"

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

# Tìm cổng trống
PORT = find_available_port(START_PORT)

print(f"Đang sử dụng cổng {PORT} để chạy server...")

# Tạo và khởi chạy server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server đang phục vụ trên cổng {PORT}")

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
                    # Xử lý file PHP bằng PHP
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
