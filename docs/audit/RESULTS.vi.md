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
