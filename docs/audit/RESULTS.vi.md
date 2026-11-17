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

Xem [FREE-COMPLETION.vi.md](FREE-COMPLETION.vi.md) để biết mục nào đã bổ sung, các điều kiện còn thiếu và nguyên nhân; [FREE-CONTROLS.vi.md](FREE-CONTROLS.vi.md) có thao tác Audit/Remediation/Re-audit theo từng mã. Mục PARTIAL vẫn còn giới hạn, không được báo hoàn tất. Không đổi Settings, role, secret, main hoặc hai repo nguồn. Không mua gói, tạo registry/production hay mời người. Mẫu ruleset chỉ là đề xuất cho nhánh thử, chưa áp dụng.

## Phụ lục kết quả cũ

Các đợt kiểm tra trước được giữ tại [RESULTS-HISTORY.vi.md](RESULTS-HISTORY.vi.md). Số liệu lịch sử không thay thế bảng kết quả hiện hành.
