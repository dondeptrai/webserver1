Hướng Dẫn Sử Dụng Web Server

1. Giới Thiệu

Đây là một web server đơn giản, được viết bằng Python, có khả năng:

Phục vụ các tệp tĩnh như HTML, CSS, JavaScript và các định dạng hình ảnh phổ biến.
Xử lý và trả về kết quả của các tệp PHP nếu có yêu cầu.

------------------------------------------------------------------------------------


2. Chuẩn Bị Môi Trường

2.1 Cài Đặt Python
Web server này được viết bằng Python, vì vậy cần có Python phiên bản 3.x trở lên. Để kiểm tra Python đã được cài đặt chưa, bạn mở terminal và gõ lệnh:

python3 --version


2.2 Cài Đặt PHP
Server hỗ trợ xử lý các tệp PHP, vì vậy bạn không cần cài đặt trước PHP:

Windows: Web server sẽ tự động cài đặt PHP bằng choco (Chocolatey).
nếu choco không thể cài được thì chúng ta có thể cài php thủ công 
 Truy cập  https://www.php.net/downloads
 Nhấp vào nút “ Tải xuống ” của Windows.
 Trang web mới có nhiều tùy chọn khác nhau, hãy chọn phiên bản Thread safe, sau đó nhấp vào nút zip và Tải xuống.
 Bây giờ hãy kiểm tra tệp zip trong mục tải xuống trong hệ thống của bạn và giải nén nó.
 Sau khi giải nén, bạn sẽ có được thư mục đã giải nén.
 Bây giờ hãy sao chép thư mục đã giải nén.
 Bây giờ dán thư mục sao chép vào ổ đĩa Windows của bạn vào thư mục Program files.
 Bây giờ cửa sổ Permission xuất hiện để dán thư mục vào tệp chương trình rồi nhấp vào “Tiếp tục”.
 Sau khi dán thư mục, hãy sao chép địa chỉ của thư mục vào tệp chương trình.
 Bây giờ hãy nhấp vào Menu Bắt đầu và tìm kiếm “Chỉnh sửa biến môi trường hệ thống” và mở nó.
 Sau khi mở System, cửa sổ Variable New sẽ xuất hiện và nhấp vào “Environment Variables…”
 Bây giờ hãy vào tùy chọn “System variables” Path và nhấp đúp vào Path .
 Màn hình tiếp theo sẽ mở ra và nhấp vào nút “Mới”.
 Sau khi New Paste địa chỉ chúng ta sao chép từ file chương trình sang New và nhấp vào nút Enter .
 Bây giờ hãy nhấp vào nút OK .
 Bây giờ PHP của bạn đã được cài đặt trên máy tính của bạn. Bạn có thể kiểm tra bằng cách vào menu “ Start ” gõ Command Prompt. Mở nó   ra.
 Khi Command Prompt mở ra, nhập php -v



macOS: Web server sẽ dùng brew (Homebrew) để cài PHP.
Linux: Server hỗ trợ cài đặt PHP bằng apt hoặc yum tùy thuộc vào hệ điều hành.
Lưu ý: Nếu chưa có các công cụ như Chocolatey (Windows) hoặc Homebrew (macOS), bạn sẽ cần cài đặt chúng trước.

------------------------------------------------------------------------------------


3. Cấu Trúc Dự Án

Để sử dụng server, đặt các tệp mà bạn muốn phục vụ (HTML, CSS, JS, PHP, hình ảnh) trong thư mục dự án (nơi bạn chạy server). Server sẽ tự động tìm các tệp này khi có yêu cầu từ client.

Dự_Án_Web_Server/
|-- server.py          # Mã nguồn của server
|-- index.html         # Trang chủ (file mặc định)
|-- style.css          # Tệp CSS
|-- script.js          # Tệp JavaScript
|-- images/            # Thư mục chứa các hình ảnh
|-- test.php           # Trang PHP cho web động

* Lưu ý nếu bạn muốn chạy một web động bạn cần phải cài đặt cơ sở dữ liệu trước:
  
* Cài Đặt MySQL trên macOS
* 
  Cài Đặt MySQL qua Homebrew:
   brew update
   brew install mysql
  Khởi Động MySQL
  brew services start mysql

  
* Cài Đặt MySQL trên Windows
Bước 1: Tải MySQL Installer
Tải MySQL Installer từ trang chính thức: MySQL Installer for Windows.
Bước 2: Cài Đặt MySQL qua MySQL Installer
Chạy file cài đặt đã tải về và làm theo các bước hướng dẫn trên màn hình.
Chọn phiên bản MySQL và cài đặt các công cụ cần thiết.
Bước 3: Cấu Hình MySQL
Trong quá trình cài đặt, bạn sẽ được yêu cầu thiết lập mật khẩu cho tài khoản root.
Bước 4: Khởi Động MySQL
Sau khi cài đặt, MySQL sẽ được khởi động tự động. Bạn có thể kiểm tra bằng cách mở MySQL Command Line Client hoặc MySQL Workbench.


*Cài Đặt MySQL trên Linux (Ubuntu/Debian và CentOS/RHEL)

Đối với Ubuntu/Debian
Bước 1: Cập Nhật Gói

sudo apt update
Bước 2: Cài Đặt MySQL

sudo apt install mysql-server
Bước 3: Kiểm Tra và Khởi Động Dịch Vụ MySQL

sudo systemctl start mysql
sudo systemctl enable mysql


* Đối với CentOS/RHEL
Bước 1: Cài Đặt MySQL từ Kho Lưu Trữ

sudo yum install mysql-server
Bước 2: Khởi Động MySQL và Thiết Lập Mật Khẩu Root

sudo systemctl start mysqld
sudo mysql_secure_installation
Bước 3: Thiết Lập MySQL Tự Động Khởi Động

sudo systemctl enable mysqld

------------------------------------------------------------------------------------

4. Khởi Động Web Server

4.1 Chạy Server
Chạy lệnh sau trong thư mục chứa server.py:

python3 server.py <port>
Thay <port> bằng số cổng bạn muốn server lắng nghe (mặc định là 8080 nếu không cung cấp).
Ví dụ: python3 server.py 8001


4.2 Kiểm Tra Server
Mở trình duyệt và truy cập http://localhost:<port>.
Nếu bạn thấy nội dung của tệp index.html xuất hiện, server đã hoạt động thành công.

----------------------------------------------------------------------------------------


5. Cách Thức Hoạt Động

5.1 Xử Lý Các Tệp Tĩnh
Khi bạn yêu cầu một tệp HTML, CSS, JS hoặc hình ảnh, server sẽ trả về tệp đó với đúng loại MIME.
Ví dụ, yêu cầu http://localhost:8080/style.css sẽ trả về tệp style.css với Content-Type: text/css.
5.2 Xử Lý Tệp PHP
Nếu yêu cầu một tệp PHP, server sẽ chạy tệp đó bằng PHP và trả về kết quả HTML.
Ví dụ, yêu cầu http://localhost:8080/test.php sẽ trả về nội dung sau khi chạy test.php.
5.3 Phản Hồi 404
Nếu yêu cầu một tệp không tồn tại, server sẽ trả về mã lỗi 404 với thông báo "Page Not Found".


*************************************************************************************************************************
Web server này chỉ phù hợp cho môi trường phát triển hoặc học tập, không khuyến nghị sử dụng trong môi trường sản xuất.
*************************************************************************************************************************


















