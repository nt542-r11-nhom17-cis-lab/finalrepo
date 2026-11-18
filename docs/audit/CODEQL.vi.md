# Đối chiếu hai cảnh báo CodeQL về dữ liệu nhạy cảm

## Audit

CodeQL Python ghi nhận hai cảnh báo HIGH tại phần xuất JSON/log của `scripts/project_bundle.py`: `py/clear-text-logging-sensitive-data` và `py/clear-text-storage-sensitive-data`. SARIF của run 44149453062 cho thấy đường dữ liệu bắt đầu tại giá trị gán cho biến `trusted`, đi vào trường `signer_fingerprint_sha256_der` rồi được ghi ra verification.json và stdout.

Giá trị thực tế là SHA256 của DER khóa công khai, không phải khóa riêng hoặc credential. Helper gọi OpenSSL với `-pubin`, rồi băm DER bằng SHA256. Khóa riêng được tạo trong thư mục tạm riêng, giữ quyền 0600, dùng để ký và bị dọn khi hết scope. Kiểm thử bắt giữ vật liệu khóa sinh trong lần chạy và xác nhận PEM/body không xuất hiện trong các file xuất hoặc log; report chỉ có digest công khai và cờ boolean.

Mô hình nguồn dữ liệu của CodeQL có heuristic coi tên chứa `trusted` là generic secret; RHS của phép gán được đánh dấu là source. Chỉ đổi tên helper chưa đủ vì biến `trusted` vẫn giữ nguyên. Mã nhận diện tham khảo: https://github.com/github/codeql/blob/main/shared/concepts/codeql/concepts/internal/SensitiveDataHeuristics.qll và https://github.com/github/codeql/blob/main/python/ql/lib/semmle/python/dataflow/new/SensitiveDataSources.qll.

## Remediation

Tên dữ liệu được chuẩn hóa thành `public_digest_sha256`; tham số xác minh là `expected_public_digest_sha256`; helper `public_signing_digest` mô tả rõ cách tạo public DER identifier. Thuật toán, các phép xác minh chữ ký/hash, schema verification.json và CLI `--trusted-fingerprint` được giữ nguyên. Không mã hóa lại digest công khai, loại file khỏi phân tích, tắt query hoặc dismiss cảnh báo để đạt kết quả sạch.

Bổ sung regression test chứng minh vật liệu ký không được xuất ra file/log và khóa tạm không còn sau bước tạo bundle. Các test sửa payload, sửa manifest, khóa/digest sai và xác minh bản gốc tiếp tục chạy.

Workflow giữ SARIF trong Actions artifact một ngày để đọc data-flow khi connector không có quyền Code scanning API. SARIF không được commit vào Git. Quyền `security-events: write` phục vụ upload kết quả của nhánh audit; các action được ghim SHA và chú thích tag tương ứng để đáp ứng kiểm tra Zizmor.

## Re-audit và kết quả

| Kiểm tra | Trước | Sau |
|---|---|---|
| Kết quả SARIF | Hai cảnh báo | Zero result |
| Catalog rule | 43 | Cùng 43 rule, bao gồm hai rule ban đầu |
| Phân tích | Thành công | Thành công |
| Dữ liệu được xuất | Public SHA256 identifier | Cùng public SHA256 identifier |
| Regression tests | Có kiểm tra tamper/khóa sai | 52 tests, thêm kiểm tra vật liệu ký không vào file/log |

Code được phân tích lại: `1ce411fba512ccce4b7d0261d5020e400c348850`. Run trước: [44149453062](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44149453062); run sau: [44213133290](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44213133290). Đã tải và đọc SARIF, không suy kết quả từ biểu tượng workflow xanh. Hash catalog và thông tin kiểm tra lưu trong [codeql-review-summary.json](evidence/codeql-review-summary.json).

Đây là xử lý cảnh báo nhầm đối với định danh công khai và bổ sung kiểm chứng an toàn dữ liệu, không phải bằng chứng đã thu hồi một credential thật. Kết quả chỉ thuộc Python và tập query đã chạy trên nhánh audit. Mục 1.5.4 tiếp tục PARTIAL; không tự kết luận đạt toàn benchmark. Main, quyền thành viên, Enterprise và các gói bằng chứng đã ký không bị thay đổi.
