# Đợt bổ sung sau chuyển Organization

Xem [ORGANIZATION.vi.md](ORGANIZATION.vi.md), [bảng 120 mục mới nhất](COVERAGE.vi.md). Các kết quả/địa chỉ phía dưới được giữ như lịch sử; không dùng số liệu cũ thay kết quả mới.

# Đợt khắc phục mới nhất

Xem [REMEDIATION.vi.md](REMEDIATION.vi.md): credential HEAD đã bỏ, base image pin digest, container smoke test và source/image scan có ngưỡng chặn đã PASS. Số liệu/kết quả phía dưới là lịch sử review trước.

# Kết quả mới nhất — audit/cis-complete-runbooks

Code đã chạy: `574c0f16fe8b81961bcd5d16d0dd40008d31d47b`.

| Kiểm tra | Kết quả | Bằng chứng |
|---|---|---|
| API, 120-control evidence readiness, dependency inventory, supply-chain/registry/scanner labs, SBOM/chữ ký | SUCCESS | [Run 44064853230](https://github.com/hieune-ui/finalrepo/actions/runs/44064853230) |
| Zizmor kiểm tra workflow của nhánh | SUCCESS | [Run 44064859042](https://github.com/hieune-ui/finalrepo/actions/runs/44064859042) |
| Unit tests (8), supply-chain lab (5), registry fixture (13), scanner fixture (2) | PASS | Các bước trong workflow tổng hợp |
| Main không đổi | Đã đối chiếu SHA | e052945db5b4a2bace480b5ab98446a8b82da02e |

Artifacts thực tế: `cis-review-44064853230` (API JSON/CSV, readiness 120 mục, dependency report, lab reports), `pipeline-signed-output-44064853230` (SBOM runner và chữ ký). Ảnh thực tế trước/sau cập nhật runtime được đặt ở phần 2, METHOD.vi.md. Trang summary sau cập nhật không còn annotation cảnh báo Node.js 20 của checkout.

Mức triển khai hiện ghi 39 PARTIAL, 10 LAB_ONLY, 7 MANUAL_REVIEW và 64 NOT_TESTED. Đủ 120 runbook không biến các mục đó thành PASS. Bộ readiness thực hiện thu thập/kiểm tra điều kiện, không thay Audit thủ công toàn bộ tiêu chí. Các kết quả cũ phía dưới giữ lại để truy vết.

# Cập nhật đợt bổ sung toàn bộ quy trình

Xem [COMPLETE-REVIEW.vi.md](COMPLETE-REVIEW.vi.md) và [bảng 120 mục cập nhật](COVERAGE.vi.md). Đã có 120 runbook, thu thập readiness và lab bổ sung; không có tuyên bố đạt toàn benchmark. Các thống kê/kết quả phía dưới thuộc lần review trước, giữ lại để truy vết.

# Kết quả kiểm chứng nhánh review

## Đã chạy local

| Kiểm tra | Kết quả | Giới hạn |
|---|---|---|
| Catalog 120 mã duy nhất | PASS | 118 Manual, 2 Automated; không phải chứng nhận tuân thủ |
| 4 kiểm thử xử lý lỗi API/quyền | PASS | Fixture kiểm tra phân loại, không thay dữ liệu thực |
| 5 phép kiểm tra supply-chain sandbox | PASS | Khóa input, ZIP tái lập, ký/negative test, mã hóa/negative test, local deployment |
| Actionlint toàn bộ workflow | PASS | Kiểm tra cú pháp và logic hỗ trợ |
| git diff --check | PASS | Không phát hiện whitespace errors |
| API repository thực tế | Có dữ liệu | Protection HTTP 403; cần đánh giá bổ sung |

## Đã chạy remote trên nhánh audit/cis-1-5-review

Commit code đã kiểm tra: c594dfc53ef76ae359d51ed75d5e8e71741bacfa.

| Workflow | Kết quả | Minh chứng |
|---|---|---|
| API + supply-chain sandbox + SBOM/chữ ký runner | SUCCESS | [Run 44061920719](https://github.com/hieune-ui/finalrepo/actions/runs/44061920719) |
| Zizmor kiểm tra mọi workflow của nhánh | SUCCESS | [Run 44061926508](https://github.com/hieune-ui/finalrepo/actions/runs/44061926508) |

Artifact `cis-review-44061920719` chứa results.json/results.csv của API và kết quả lab; artifact `pipeline-signed-output-44061920719` chứa SBOM runner/chữ ký. Đã xác nhận các bước API/lab/upload thực sự success và artifact tồn tại qua metadata. Trạng thái success là kiểm tra chương trình, không phải PASS 120 tiêu chí. API permissions không được mở rộng, các tiêu chí cần Settings vẫn MANUAL_REVIEW.

Mọi thay đổi chỉ ở nhánh review. Đã đối chiếu main vẫn e052945db5b4a2bace480b5ab98446a8b82da02e; hai repo nguồn không được push. Không tạo PR để tránh tự kích hoạt workflow pull_request lên main; dùng link nhánh để xem trước.
