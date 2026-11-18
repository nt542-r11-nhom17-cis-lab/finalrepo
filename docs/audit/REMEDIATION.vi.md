> Phụ lục kỹ thuật của lần đo trước. Kết quả tổng hợp hiện hành: [RESULTS.vi.md](RESULTS.vi.md); mô hình hiện hành: [IMPLEMENTATION.vi.md](IMPLEMENTATION.vi.md).

# Khắc phục cấu hình và bổ sung kiểm tra còn thiếu

Nhánh mới: `audit/remediate-config-and-scans`. Code kiểm tra: `4e1c9663acb9e9ecc89ac2233e4dcbe5d6b4001c`. Không merge, không sửa main, không chỉnh Settings hoặc cấp quyền. Snapshot main trước/sau vẫn e052945db5b4a2bace480b5ab98446a8b82da02e.

## Đã khắc phục và kiểm tra lại

| Vấn đề | Khắc phục trên nhánh | Re-audit thực tế | Giới hạn |
|---|---|---|---|
| Credential ghi cứng trong database_config.py | Chỉ đọc từ biến môi trường, không có giá trị mặc định cho credential; .env được ignore | Gitleaks cây mã hiện tại: 0 phát hiện; test config PASS | Commit cũ vẫn chứa dữ liệu; chưa thu hồi credential hoặc làm sạch lịch sử |
| Không xác minh input DB_PORT | Kiểm tra số nguyên trong khoảng 1–65535 | Test giá trị hợp lệ và 0/65536/chuỗi sai: PASS | Không kiểm thử kết nối database thật |
| Alpine cũ, base image chưa pin | Alpine 3.24.4 có digest cố định lấy từ DockerHub metadata | Build thành công; scan image 0 HIGH/CRITICAL tại thời điểm chạy | Không có bảo đảm không còn LOW/MEDIUM hoặc CVE tương lai |
| Chưa smoke-test container thật | Run với --network none, --read-only, --cap-drop ALL, no-new-privileges | Output đúng, container chạy non-root theo Dockerfile | Đây là demo ngắn, không phải dịch vụ production |
| Scanner trước chỉ quan sát, thiếu image scan | Bổ sung source/IaC scan và image-package scan với exit-code 1, HIGH/CRITICAL | Cả hai gate PASS; JSON report đã tải và đọc | Required status checks của main chưa đổi; scanner license không thay license policy |
| Thiếu code owner và truy vết task | CODEOWNERS cho file nhạy cảm, chỉ @hieune-ui đã xác minh; mẫu PR yêu cầu task/issue, before/after/evidence | File có trên nhánh | Không cấp quyền, không enforce owner review và không tự điền ba username còn thiếu |

## Kết quả remote

- [Workflow source/container + API + các lab, SBOM và chữ ký](https://github.com/hieune-ui/finalrepo/actions/runs/44066141741): SUCCESS.
- [Zizmor kiểm tra workflow](https://github.com/hieune-ui/finalrepo/actions/runs/44066147171): SUCCESS.
- 11 unit tests: PASS.
- Đã tải và đọc artifact `remediation-security-44066141741`: current-source-gitleaks.json không có phát hiện; Trivy source và image không có finding được báo trong ngưỡng HIGH/CRITICAL đã chọn.
- `cis-review-44066141741` có API JSON/CSV, dependency inventory, readiness 120 mục và các lab. Đã tải archive và đọc summary; đây không phải kiểm chứng mọi điều kiện CIS.
- `pipeline-signed-output-44066141741` có output/SBOM runner/chữ ký. Không tuyên bố signer có danh tính tin cậy production.

Ảnh thực tế đặt tại phần 2, METHOD.vi.md. Phần 3, IMPLEMENTATION.vi.md chỉ ghi chữ/bảng và dẫn bằng chứng.

## Những phần còn thiếu, không được che bằng run xanh

Lịch sử Git vẫn chứa phát hiện nguồn. Chỉ bỏ credential ở HEAD không xóa commit cũ. Nếu đó là secret thật, chủ sở hữu phải thu hồi/rotation trước, rồi thống nhất kế hoạch làm sạch lịch sử và mọi fork/cache; đợt này không rewrite main hoặc force-push. Workflow quét full history cũ không bị đổi thành scan HEAD và không thêm allowlist/continue-on-error. Job scan current source mới được ghi tên và phạm vi riêng.

Chưa có bốn username, organization/IdP phù hợp, supplier, registry và production thực tế để hoàn tất các kiểm soát tương ứng. API classic protection còn bị giới hạn quyền. Chính sách tuổi package vẫn có các action chưa hơn 60 ngày hoặc chưa xác định release date. Không hạ phiên bản chỉ để qua điều kiện tuổi, không gán PASS khi thiếu dữ liệu.

Bảng cập nhật ghi 42 PARTIAL, 10 LAB_ONLY, 7 MANUAL_REVIEW, 61 NOT_TESTED. Đã có hướng dẫn cho đủ 120 mục; số trên là mức triển khai thực tế, không phải phần trăm đạt.
