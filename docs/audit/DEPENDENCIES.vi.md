# Chính sách dependency đề xuất cho lab

Tài liệu đề xuất trên nhánh review, chưa phải chính sách được tổ chức phê duyệt.

1. Liệt kê package, action, công cụ tải trực tiếp và môi trường runtime; không coi chỉ package ứng dụng mới là dependency.
2. Chọn nguồn chính thức, ghi URL, phiên bản, commit và hash; xác minh release/checksum hoặc attestation từ nguồn tin cậy trước khi cho phép sử dụng.
3. Pin action bằng full commit SHA, ưu tiên commit tương ứng release. SHA lock không thay kiểm chứng nguồn gốc.
4. Đối với yêu cầu tuổi package 3.1.8, tính ngày phát hành tới ngày đánh giá và ghi phiên bản. Không mặc định mọi action hiện có đều trên 60 ngày tuổi; chưa tự động nâng cấp để đạt tiêu chí.
5. Yêu cầu supplier SBOM và metadata ký, xác minh chữ ký theo root tin cậy. SBOM tự tạo trong lab không thay thế SBOM nhà cung cấp.
6. Quét CVE/license/ownership thay đổi định kỳ; xác định ngưỡng chặn và quy trình xử lý ngoại lệ. License NOASSERTION không có nghĩa license đã được chấp thuận.
7. Demo first-party dùng Python standard library, khóa SHA256 app/config tại lab-inputs.lock.json. Muốn thay input phải cập nhật lock trong cùng thay đổi được review; hash không thay chữ ký hoặc review.
8. Không thay khóa, allowlist, ngưỡng quét để làm xanh phát hiện. Phát hiện Gitleaks lịch sử được giữ nguyên; nếu là secret thật cần thu hồi trước khi thảo luận làm sạch lịch sử.
