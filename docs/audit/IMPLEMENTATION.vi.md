# 3. Triển khai trên nhánh riêng

## 3.1 Mô hình và phân quyền

Repo đích: hieune-ui/finalrepo. Base main tại e052945db5b4a2bace480b5ab98446a8b82da02e. Nhánh triển khai: audit/cis-1-5-review. Các thành phần gồm người dùng, repository, GitHub API, hosted runner, artifact store và sandbox thư mục tạm. Runner chỉ triển khai app mô phỏng không mở cổng mạng; không kết nối production. Chi tiết hình mô hình/phương pháp nằm tại phần 2.

Chỉ hieune-ui đã được xác nhận có quyền admin ở lần kiểm tra trước. Chưa có danh sách ba username còn lại hoặc bằng chứng cấp quyền; bảng sau là đề xuất để nhóm điền, không thay đổi collaborator:

| Người/tài khoản | Quyền đề xuất | Nhóm phụ trách | Làm gì | Đầu ra | Minh chứng |
|---|---|---|---|---|---|
| hieune-ui | Admin hiện có, chưa đổi | Điều phối 1–5 | Xem xét thay đổi, điều phối Audit/Remediation | Nhánh và PR rà soát | Link nhánh, commit |
| TV2 – cần username | Write | 1 và 2 | Kiểm tra source/pipeline; script API | JSON/CSV, scanner logs | Phần 2 và catalog |
| TV3 – cần username | Write | 3 và 4 | Kiểm tra phụ thuộc, artifact, SBOM/chữ ký | Báo cáo lab và policy | Phần 2 và kết quả nhánh |
| TV4 – cần username | Write nếu review PR; Read nếu chỉ đọc | 5 và kiểm chứng | Kiểm tra deployment sandbox, tổng hợp kết quả | Bảng đối chiếu và nhận xét | Phần 2 và kết quả nhánh |

Không cấp quyền thay người dùng. Hai người review độc lập với tác giả PR cần được xác định khi thử nghiệm tiêu chí phê duyệt. Không dùng tài khoản chung.

## 3.2 Triển khai Manual

| Mục | Audit đã làm | Kết quả | Remediation/kiểm tra còn lại |
|---|---|---|---|
| 1.1.3/.4/.9/.16/.17/.20 | Script đọc cấu hình và nghiên cứu hướng dẫn Audit | Classic protection trả 403 ở snapshot; chưa kết luận | Người có quyền chụp Settings và thử PR/nhánh lab; không đổi main |
| 1.2.1 | Đọc chính sách có sẵn và kiểm tra file qua API | Có SECURITY.md; chưa có kênh liên hệ cụ thể | Chốt kênh báo cáo riêng tư hợp lệ, không tự bịa email |
| 1.5.1 | Đọc phát hiện Gitleaks từ lần chạy tích hợp | Có credential-shaped values trong lịch sử nguồn | Xác minh nguồn gốc; nếu thật phải thu hồi; kế hoạch làm sạch lịch sử cần riêng, không rewrite main |
| 2.3.1/.2 | Đọc YAML và các bước input/output | Có workflow-as-code, input/output minh họa | Xác nhận phạm vi toàn bộ pipeline |
| 3.1.7 | Kiểm tra refs action và khóa đầu vào lab | SHA action đã cố định; input hash được kiểm tra | Xác minh provenance/tag và mọi phụ thuộc ngoài lab |
| 4.1.1/.2/.3 | Xem quy trình ký và mã hóa sandbox | Có mô phỏng, chưa phải quản lý khóa production | Thiết lập danh tính tin cậy, quyền giải mã và registry ngoài phạm vi |
| 5.1.1/.6/.7 | Tách deploy/demo.json, kiểm tra hash trong lock | Có cấu hình tách tệp và pin hash; vẫn cùng repo | Xác nhận mức tách biệt theo chính sách; không kết luận đạt riêng nhờ tách thư mục |
| 5.2.1/.2 | Chạy triển khai sandbox tự động và kiểm tra tái lập ZIP | Thành công cục bộ | Chưa triển khai production hay chứng minh tái lập môi trường production |

Kết luận toàn bộ 120 tiêu chí nằm trong COVERAGE.csv và COVERAGE.vi.md. Không lấy job thành công làm kết quả đạt tiêu chí.

## 3.3 Triển khai Automated/Remote Automated

Các file mới gồm scripts/audit_github.py, scripts/supply_chain_lab.py, lab-inputs.lock.json, deploy/demo.json, app first-party mẫu, test và tài liệu. Workflow pipeline-io.yml chỉ thay trên nhánh review để checkout nhánh, gọi hai script và upload reports. Main không được chỉnh sửa hoặc merge.

| Tác vụ | Lệnh/công cụ | Đầu ra | Trạng thái |
|---|---|---|---|
| Audit API local | python3 scripts/audit_github.py --repo hieune-ui/finalrepo | results.json, results.csv | Có snapshot, xem phần 2 |
| Kiểm thử API lỗi/quyền | python3 -m unittest discover -s tests -v | 4 kiểm thử | PASS local |
| Lab chuỗi cung ứng | python3 scripts/supply_chain_lab.py | ZIP, SBOM, provenance, ciphertext, signatures, JSON | PASS local; phiên remote ghi riêng |
| Kiểm tra workflow | actionlint | Lỗi cú pháp | PASS local |
| Remote | Dispatch pipeline-io.yml với ref nhánh review | Artifact cis-review-RUN_ID | Xem RESULTS.vi.md |
| Rà soát workflow remote | Dispatch pipeline-security.yml cùng ref | Zizmor logs | Xem RESULTS.vi.md |

Báo cáo chứa khóa công khai tạm nhưng không chứa khóa riêng hoặc password giải mã. File encrypted là minh họa; artifact zip plaintext cùng được lưu phục vụ lab nên không tuyên bố bảo mật phân phối production. Workflow sandbox không chứng minh registry riêng đã xác minh upload hoặc giới hạn truy cập artifact.

## Đợt bổ sung trên nhánh audit/cis-complete-runbooks

Bổ sung 120 runbook và control-plans.json, audit_all.py, audit_dependencies.py, registry_lab.py, scanner_selftest.py, checksum Gitleaks, hook pre-push local và 4 test bổ sung (tổng 8). Phần 2 giải thích hình/bằng chứng; tại đây chỉ ghi chữ/bảng. Các vai trò nhóm trước vẫn là đề xuất vì chưa có ba username. Không cấp quyền thật. Kết quả bổ sung có registry fixture 13 phép thử và scanner 2 phép thử; không cộng chúng thành số tiêu chí CIS đạt. Nhánh main, collaborator/settings và hai repo nguồn không được thay đổi.

## Đợt khắc phục nguồn và container — nhánh audit/remediate-config-and-scans

Đã bỏ secret khỏi cấu hình hiện tại, đọc env, thêm test port/secret defaults và .env.example. Đã pin Alpine 3.24.4 bằng digest chính thức, thêm source-security job làm điều kiện trước job lab. Job build container, chạy không mạng/read-only/non-root và quét source/IaC cùng image với gate HIGH/CRITICAL. Cả hai job và workflow Zizmor đã SUCCESS; 11 unit tests PASS. File JSON source/image/Gitleaks đã được tải đọc và lưu trong evidence. Hình nằm ở phần 2 (Hình 2.7).

CODEOWNERS mới chỉ đề xuất trên nhánh, dùng tài khoản admin hieune-ui đã xác minh; không kích hoạt policy của main hoặc mời thêm người. Mẫu PR yêu cầu task/issue và bằng chứng before/after. Ảnh/config IdP, registry và production vẫn cần hệ thống thật và người có quyền.
