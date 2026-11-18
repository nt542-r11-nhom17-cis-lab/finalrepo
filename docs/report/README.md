# Báo cáo thực nghiệm

[Báo cáo đầy đủ](BAO-CAO.vi.md) trình bày bốn phần: giới thiệu benchmark; phương pháp Audit → Remediation → Re-audit; triển khai; kết quả đối chiếu 120 tiêu chí.

Hình minh họa và ảnh gốc được đặt trong phần 2. Phần 3 chỉ dùng chữ/bảng và liên kết tới file xuất. Các kết quả được gắn phạm vi, phiên chạy và giới hạn; không suy kiểm thử lab thành tuân thủ production.

Danh mục có 118 Manual và 2 Automated, giữ nhãn CIS. Bảng kết quả phân biệt bằng chứng thành phần, cần xác minh thủ công, mô hình lab và chưa triển khai. JSON/CSV/SPDX gốc nằm trong `../audit/evidence/`; bảng máy đọc được ở `../audit/COVERAGE.csv`.

## Quy ước và bằng chứng bổ sung

Báo cáo dùng nhãn tiếng Việt theo bảng ánh xạ ở mục 4.1; CSV giữ mã máy ở result và nhãn hiển thị ở result_label. Phụ lục B liệt kê 10 ảnh Settings/terminal VM cần chụp, cùng hồ sơ quản trị/MFA/supplier còn thiếu. Snapshot kiểm thử và tài liệu được phân biệt trong mục 4.2.
