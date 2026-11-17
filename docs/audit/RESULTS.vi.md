# Kết quả đợt bổ sung 48 mục theo hướng miễn phí

Nhánh: `audit/free-controls-completion`. Code được kiểm tra: `f1df426fb33f05fbdf64f04d5068a6d6c97085bf`. Không merge vào main. Các kết quả Organization trước bên dưới là lịch sử, không thay thống kê hiện tại.

| Kiểm tra | Kết quả | Bằng chứng |
|---|---|---|
| Free controls evidence | SUCCESS | [Run 44108703310](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44108703310) |
| Source/container + API/SBOM/lab | SUCCESS | [Run 44108703867](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44108703867) |
| Zizmor toàn bộ workflow | SUCCESS | [Run 44108703323](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44108703323) |
| Tests | 37 PASS | Log CI, gồm negative tests chữ ký/owner drift/phân trang/quyền/dependency |
| Scanner toolchain | 32/32 package đúng phiên bản; zero advisory đã biết; 32 hash khớp | evidence/free-python-package-audit.json, free-dependency-coverage.json, free-python-toolchain.json |
| License | 20 cần review | Không tự coi policy đề xuất là được nhóm duyệt |
| Dependency relationships | 32 node, 145 cạnh khai báo, 32 active mặc định, zero lỗi | evidence/free-dependency-graph.json |
| Bandit / Gitleaks HEAD / Trivy source-image | Zero HIGH / zero HEAD finding / zero HIGH-CRITICAL theo phạm vi | Artifact đã tải đọc; không suy lịch sử credential đã sạch |
| Action ownership | Tám cặp repository/owner numeric ID không đổi | evidence/free-action-owners.json; chưa bao phủ PyPI maintainers |
| Bundle | Ba payload xác minh được, sửa payload bị từ chối; fingerprint khớp log run | evidence/free-bundle-verification.json và ZIP xuất kết quả |
| Runtime hardening | Non-root, CapEff=0, NoNewPrivs=1, ghi root filesystem bị từ chối | Log pipeline; chưa bảo vệ toàn bộ worker/host |
| Main | SHA trước/sau không đổi | e052945db5b4a2bace480b5ab98446a8b82da02e |

Đã tải và đọc cả Free, security và review artifact. Bundle được kiểm tra lại bên ngoài CI bằng fingerprint lấy từ log của đúng run đã xác thực. File xuất kết quả: [free-controls-export.zip](evidence/free-controls-export.zip); JSON/CSV xem [free-controls-results.json](evidence/free-controls-results.json), [free-controls-results.csv](evidence/free-controls-results.csv). Tổng hợp có SHA ZIP: [free-completion-summary.json](evidence/free-completion-summary.json).

Trong 48 mục: 21 PARTIAL mới, tám MANUAL_REVIEW mới, 19 vẫn NOT_TESTED; có hướng dẫn riêng cho cả 48. Bộ readiness khác với mức triển khai: năm mục đủ nguồn thu thập khai báo, 43 còn thiếu nguồn; không gọi năm mục đó là PASS. Toàn bộ 120 mục: **66 PARTIAL, 22 MANUAL_REVIEW, 10 LAB_ONLY, 22 NOT_TESTED; zero full-control PASS**. Trong 22 NOT_TESTED gồm 19 mục hướng Free và ba mục Enterprise.

Xem [FREE-COMPLETION.vi.md](FREE-COMPLETION.vi.md) để biết mục nào đã bổ sung, mục nào cần bạn làm và vì sao; [FREE-CONTROLS.vi.md](FREE-CONTROLS.vi.md) có thao tác Audit/Remediation/Re-audit theo từng mã. Mục PARTIAL vẫn còn giới hạn, không được báo hoàn tất. Không đổi Settings, role, secret, main hoặc hai repo nguồn. Không mua gói, tạo registry/production hay mời người. Mẫu ruleset chỉ là đề xuất cho nhánh thử, chưa áp dụng.

---

## Lịch sử các đợt trước — số liệu dưới đây không phải thống kê mới nhất

# Kết quả xác minh mới nhất trên Organization

Nhánh: `audit/organization-controls`. Code đã chạy: `4003107b0cda7e8b3c5f395f9911274336e98ec6`. Các commit tài liệu sau đó không thay đổi code đã kiểm tra.

| Kiểm tra | Kết quả | Minh chứng |
|---|---|---|
| Workflow source/container, SAST/SCA, API/Organization, SBOM và lab | SUCCESS | [Run 44077094456](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44077094456) |
| Zizmor kiểm tra cấu hình workflow | SUCCESS | [Run 44077100177](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44077100177) |
| Unit tests | 21 PASS | Job source-security của workflow tổng hợp |
| Bandit | 0 HIGH | evidence/bandit-org-run.json |
| Package vulnerability audit | 32/32 đúng tên và phiên bản; 0 advisory | evidence/dependency-coverage-org-run.json và python-package-audit-org-run.json |
| Hash wheel | 32/32 khớp PyPI | evidence/python-toolchain-org-run.json |
| License | 20 mục cần review | Policy đề xuất chưa được Organization phê duyệt |
| Organization settings | 7 trường UNKNOWN; is_verified=false | evidence/organization-after-install.json |
| Main | SHA không đổi | e052945db5b4a2bace480b5ab98446a8b82da02e |

Đã tải và đọc cả security artifact và review artifact. Không chỉ dựa vào biểu tượng xanh. Bộ kiểm tra coverage bắt buộc báo cáo đủ mọi package trong lock; không cho phép missing/skipped package hoặc sai phiên bản.

Artifacts: `remediation-security-44077094456`, `cis-review-44077094456`, `pipeline-signed-output-44077094456`. Ảnh thật thuộc phần 2, METHOD.vi.md; phần 3 chỉ ghi chữ/bảng và tham chiếu ảnh.

Kết quả này không chứng minh cả 120 tiêu chí đạt. Mức triển khai vẫn là 45 PARTIAL, 14 MANUAL_REVIEW, 10 LAB_ONLY, 51 NOT_TESTED. Các mục IdP/MFA, domain, thành viên, registry, supplier và production còn thiếu bằng chứng thật; lịch sử credential không bị rewrite. Không đổi Organization Settings, quyền thành viên, main hoặc hai repo nguồn.

## Lịch sử các đợt kiểm tra trước

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
