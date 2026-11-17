# Kết quả kiểm tra bản gộp

Hai repo gốc không bị thay đổi. Bản gộp ở `hieune-ui/finalrepo`. Mỗi dòng dẫn đến phiên chạy và commit đã kiểm tra; các workflow khác nhau có thể được chạy ở các commit khác nhau.

| Workflow | Trạng thái | Kết luận | Minh chứng |
|---|---|---|---|
| Dedicated Application Build Pipeline | completed | success | [Run 44058799508](https://github.com/hieune-ui/finalrepo/actions/runs/44058799508) |
| CIS 1.5 & 2.1 Security Pipeline | completed | failure | [Run 44058799530](https://github.com/hieune-ui/finalrepo/actions/runs/44058799530) |
| CIS - Pipeline Security Scan | completed | success | [Run 44058801337](https://github.com/hieune-ui/finalrepo/actions/runs/44058801337) |
| CIS - Pipeline Input Output | completed | success | [Run 44058355321](https://github.com/hieune-ui/finalrepo/actions/runs/44058355321) |
| CIS - Runner Resource Monitor | completed | success | [Run 44058362039](https://github.com/hieune-ui/finalrepo/actions/runs/44058362039) |
| CIS - Runner Check | completed | success | [Run 44058368799](https://github.com/hieune-ui/finalrepo/actions/runs/44058368799) |

## Diễn giải

- Gitleaks: FAIL do credential-shaped values trong lịch sử `database_config.py` của repo nhóm. Không xác minh tính hiệu lực của credential. Không thêm allowlist hay bỏ qua mã lỗi. Artifact JSON đã được tạo bằng --redact; không tái xuất credential trong tài liệu này.
- Actionlint và Trivy trong workflow scanner: các job đã thực thi thành công. Trivy chưa được cấu hình làm cổng chặn theo ngưỡng, vì vậy success không đồng nghĩa không có phát hiện.
- Pipeline Security Scan: sau khắc phục đã thành công. Đã cố định SHA action, chọn Trivy release, tắt credential persistence, thêm concurrency/timeouts.
- Pipeline Input Output: đã tạo artifact chứa đầu ra, SBOM package Ubuntu runner, chữ ký và public key lab.
- Runner Resource Monitor: giám sát tác vụ mẫu, không phải hệ thống giám sát thường trực.
- Runner Check: hoàn thành; quét package sử dụng fail-build: false, nên success không đồng nghĩa không có CVE.
- Placeholder CIS 1.1 chỉ echo, không tính là kiểm tra bảo mật và không cần chạy để xác nhận tích hợp.
- Các chỉnh sửa workflow chỉ nằm trong finalrepo. CODEOWNERS nguồn chưa kích hoạt. Settings/Secrets/Rulesets/CodeQL default setup chưa sao chép.

## Giới hạn truy xuất bằng chứng

Đã xác nhận artifacts tồn tại qua GitHub API. Tải archive bằng CLI trong môi trường này gặp HTTP Forbidden tại máy chủ lưu trữ artifact; có thể mở phiên chạy trên GitHub để tải trực tiếp. Không coi việc kiểm tra metadata là đã xác minh đầy đủ nội dung archive.
