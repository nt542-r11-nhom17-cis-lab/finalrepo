# Bản gộp thử nghiệm CIS GitHub Lab

## Phạm vi
Bản này lấy repo nhóm làm nền, bổ sung 5 workflow từ repo cá nhân. Hai repo gốc không bị thay đổi. Commit nguồn được ghi trong sources.json.

## Những gì giữ nguyên
Toàn bộ file đã được theo dõi của repo nhóm, gồm app-build.yml, cis-scanners.yml, SECURITY.md, Dockerfile và database_config.py. README gốc cũng giữ nguyên. Vì vậy lỗi Gitleaks đã có ở repo nhóm có thể tiếp tục xuất hiện; không coi đây là lỗi do gộp và không tắt scanner để làm xanh giả.

## Điều chỉnh khi nhập
- pipeline-security.yml: chỉ chạy workflow_dispatch trong giai đoạn tích hợp. Zizmor quét cả thư mục workflows nên có thể phát hiện vấn đề có sẵn trong workflow nhóm, ví dụ action dùng @master. Không bỏ qua phát hiện để giả lập đạt CIS.
- cis-1-1-scan.yml: chỉ chạy thủ công, đặt tên DEMO ONLY và thông báo rõ chỉ là placeholder echo, không thực hiện quét bảo mật; thêm contents: read.
- pipeline-io.yml, runner-check.yml, resource-monitor.yml: giữ nguyên nội dung nguồn, vốn đã chạy thủ công.
- CODEOWNERS cá nhân được lưu dưới tên docs/integration/SOURCE_CODEOWNERS.txt để tham khảo, không kích hoạt. Chưa xác minh các tài khoản có quyền Write trong repo đích. Chỉ tạo CODEOWNERS chính thức sau khi thống nhất phân công và xác minh quyền.

## Thử nghiệm trên repo mới
1. Tạo repo GitHub thử nghiệm trống, KHÔNG khởi tạo README/license/gitignore.
2. Clone repo nhóm về một thư mục mới trên máy của bạn.
3. Tạo nhánh integration/combined-cis-lab rồi áp dụng integration.patch bằng git apply --check trước, sau đó git apply.
4. git add . và git commit thay đổi.
5. Thêm remote sandbox trỏ đến repo MỚI. Không đổi origin của hai repo gốc.
6. Push nhánh tích hợp thành main của sandbox: git push sandbox integration/combined-cis-lab:main.
7. Trong Actions của sandbox, chạy lần lượt 4 workflow thực: Pipeline Input Output, Runner Resource Monitor, Runner Check, Pipeline Security Scan. Không cần chạy placeholder.
8. Kiểm tra log, tải artifacts và ghi nhận phát hiện. Runner Check có quét package với fail-build: false nên xanh không có nghĩa hết CVE. Kiểm tra mạng hiện chỉ ghi nhận khả năng truy cập; chưa khẳng định assert chính sách allow/block.
9. Chỉ sau khi các chức năng cần thiết được kiểm chứng mới tạo PR về repo nhóm; không merge tự động. Chưa đặt workflow lọc paths làm required check nếu chưa xử lý trường hợp bị skip.

## Giới hạn
Không sao chép được Settings, Secrets, Rulesets, branch protection, collaborators, CodeQL default setup, lịch sử Actions hoặc artifacts bằng cách gộp file. Phải kiểm tra/cấu hình riêng trong sandbox. Workflow chỉ dispatch cần có trên default branch để chạy thuận tiện.

SBOM hiện là inventory package Ubuntu của runner, không phải SBOM ứng dụng. Chữ ký dùng khóa lab tạm, minh họa ký/xác minh và chống sửa đổi, chưa thiết lập danh tính tin cậy production.

Không đưa token vào file hoặc lệnh chia sẻ. Không dùng force push hay git pull hai lịch sử không liên quan để gộp trực tiếp vào repo gốc.
