# Dự thảo quy trình rà soát nhóm

Trạng thái: **DRAFT — CHƯA ĐƯỢC NHÓM PHÊ DUYỆT**. Đây là tài liệu chuẩn bị, không phải bằng chứng đã vận hành định kỳ hoặc lời xác nhận của thành viên. Không tự phân công, cấp quyền hoặc xóa dữ liệu.

| Phạm vi | Nhịp đề xuất | Nội dung rà và bằng chứng |
|---|---|---|
| Thành viên/quyền | Hằng tháng; khi có người vào/rời nhóm | Kiểm tra người, nhiệm vụ, quyền trực tiếp/kế thừa, admin dự phòng, MFA; owner duyệt thu hồi hoặc giữ quyền |
| Repo, fork và nhánh | Hằng tháng | Inventory đầy đủ; ghi mục đích, người dùng, PR chưa xong; tuổi commit chỉ dùng gợi ý. Không xóa trước quyết định owner |
| GitHub Apps/OAuth/webhook | Hằng tháng và trước cài mới | Mục đích, repo scope, permissions, người phê duyệt, hoạt động gần đây; thu hẹp/gỡ sau duyệt |
| Audit log | Hằng tuần và sau thay đổi quyền/rule/visibility | Actor, UTC timestamp, repo, action, lý do và biên bản xử lý. Free dùng UI; không bắt buộc Audit Log API Enterprise |
| Supplier và package | Khi thêm/nâng phiên bản; rà hằng tháng | Nguồn phát hành, hash, tuổi bản, SBOM/provenance/chữ ký nếu có, license; ngoại lệ có lý do/người duyệt |
| Triển khai lab | Trước/sau mỗi đợt | Phạm vi được phép, commit, môi trường, kiểm tra trước/sau và rollback; tách lab khỏi production |

Mời thành viên: owner xác nhận người và email được nhóm duyệt ở sổ riêng; không công khai địa chỉ cá nhân trong repo public. Trên Free, quy trình này không chứng minh nền tảng cưỡng chế approved-email. Không tự bật tính năng Enterprise.

Review thay đổi: tác giả tạo PR vào nhánh sandbox; Vương và Hiệp là ứng viên reviewer độc lập có Write theo người dùng xác nhận. Cần quyết định nhóm và test thật trước khi khẳng định enforcement. Không dùng tài khoản chung hoặc tự tạo approval thay thành viên. Không đổi target thành main.

Mẫu biên bản mỗi kỳ: thời gian + phạm vi + commit/report hash + người rà + tài nguyên + phát hiện + quyết định/ngoại lệ + người phê duyệt + ngày rà tiếp. Chưa điền tên người rà hoặc chữ ký nếu người đó chưa thực hiện. Bằng chứng chứa password, token, email riêng, hook endpoint hoặc recovery code không được commit.

Điều kiện chuyển từ dự thảo sang áp dụng: nhóm chọn người chịu trách nhiệm/phê duyệt từng phạm vi và xác nhận nhịp rà; lưu biên bản kỳ đầu có bằng chứng thực. Không suy tài liệu này thành đạt các tiêu chí định kỳ.

Công cụ hỗ trợ rà hiện có: audit_pending_free.py (GET evidence), code_change_monitor.py (code/rule-review support), supplier_intake.py (missing supplier evidence), deployment_preflight.py (read-only host preflight). Không thay việc người được giao thực hiện/phê duyệt kỳ rà. Xem PENDING-FREE.vi.md để phân biệt kết quả đo và phần còn thiếu.
