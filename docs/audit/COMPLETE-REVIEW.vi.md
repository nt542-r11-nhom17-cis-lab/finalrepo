# Đợt bổ sung toàn bộ quy trình cho 120 tiêu chí

## Phạm vi thực hiện

Nhánh mới: `audit/cis-complete-runbooks`, phát triển từ nhánh review trước. Không merge, không push main, không đổi GitHub Settings, collaborator, Secrets, registry hoặc production. Hook pre-push được kích hoạt trong bản làm việc này, chỉ cho push `audit/*` tới finalrepo. Hook không phải branch protection trên máy chủ và có thể bị người dùng bypass; không tuyên bố nó bảo vệ mọi máy khác.

## Đã bổ sung

| Nhóm | Quy trình chi tiết | Số mục |
|---|---|---:|
| 1 Source Code | [Audit–Remediation–Re-audit từng mục](runbooks/GROUP-1.vi.md) | 50 |
| 2 Build Pipelines | [Audit–Remediation–Re-audit từng mục](runbooks/GROUP-2.vi.md) | 33 |
| 3 Dependencies | [Audit–Remediation–Re-audit từng mục](runbooks/GROUP-3.vi.md) | 12 |
| 4 Artifacts | [Audit–Remediation–Re-audit từng mục](runbooks/GROUP-4.vi.md) | 14 |
| 5 Deployment | [Audit–Remediation–Re-audit từng mục](runbooks/GROUP-5.vi.md) | 11 |

Mỗi mục có Audit, Remediation đề xuất, Re-audit, trang nguồn, nguồn bằng chứng, vai trò phụ trách và giới hạn thay đổi. [control-plans.json](control-plans.json) là bản máy đọc được. Không phải nội dung nào trong hướng dẫn cũng đã được áp dụng lên hệ thống thật.

## Công cụ mới và cách thực thi

| Công cụ | Đầu vào | Đầu ra | Phạm vi |
|---|---|---|---|
| audit_all.py | Một repo và 120 kế hoạch kiểm tra | JSON/CSV/summary, metadata và số lượng tài nguyên | GET-only, phân trang có giới hạn rõ; không xuất hook URL/secret hoặc danh sách định danh |
| audit_dependencies.py | Mọi action ref trong workflow | SHA, kiểm tra commit tồn tại, tag match, ngày release và tuổi | GitHub Actions; không thay supplier verification |
| registry_lab.py | Artifact và chữ ký từ lab | 13 kết quả positive/negative, chuỗi log | Registry policy mô phỏng offline; không có IdP hoặc MFA thật |
| scanner_selftest.py | Gitleaks đã xác minh checksum | 2 kết quả fixture sạch và credential giả | Chứng minh scanner hoạt động; không chứng minh chặn merge |
| pre-push hook + test | Remote/ref push | Cho phép audit/*; từ chối main/remote nguồn | Bảo vệ local trong bản làm việc này |

Gitleaks được tải từ release chính thức và kiểm SHA256 theo file đã commit trước giải nén/chạy. Checksum cùng nguồn release là bằng chứng một phần, chưa thay chữ ký phát hành hoặc trust root độc lập.

Workflow pipeline-io.yml chạy trên ref nhánh mới: API → supply-chain lab → unit tests → registry fixture → dependency inventory → scanner self-test → audit readiness 120 mục → artifacts. Workflow pipeline-security.yml kiểm tra toàn bộ cấu hình workflow của nhánh. Triggers main giữ nguyên; không kích hoạt PR hướng vào main trong đợt này.

## Cách đọc kết quả, tránh nhầm lẫn

Có hai lớp kết quả khác nhau:

1. **Thực thi chương trình/lab:** unit tests, negative tests, workflow và xuất file có chạy đúng không.
2. **Tuân thủ CIS thực tế:** cấu hình đúng phạm vi, bằng chứng đầy đủ, quyền/IdP/registry/production và khả năng thực thi chính sách có đáp ứng không.

`EVIDENCE_COLLECTED` chỉ nghĩa nguồn metadata cần thiết cho bước thu thập đã sẵn sàng; không có nghĩa Audit toàn mục đã hoàn thành. `BLOCKED_PREREQUISITE` chỉ rõ dữ liệu chưa có. Cả hai đều giữ compliance `MANUAL_REVIEW`. Bộ thu thập không biến lỗi HTTP, dữ liệu rỗng hoặc lab mô phỏng thành PASS toàn tiêu chí.

Thống kê PARTIAL/MANUAL_REVIEW/NOT_TESTED trong COVERAGE là mức triển khai/bằng chứng, không cùng thang đo với audit readiness. Bảng được cập nhật với kết quả lab/inventory bổ sung nhưng không xóa các thiếu sót thực tế.

## Những điều không thể hoàn tất chỉ bằng commit

Repo này thuộc tài khoản cá nhân, chưa có thông tin ba thành viên còn lại. Không thể tự tạo bằng chứng organization MFA, domain verification, SSH CA, IP allow list hoặc phân quyền bốn người bằng file Markdown. Cũng chưa có supplier, registry và production thực tế để áp dụng và kiểm chứng toàn bộ chính sách. Tạo lớp giả lập không biến nó thành IdP/MFA thật.

Ảnh cấu hình/tài khoản cần được chụp từ đối tượng thật bởi người có quyền. Sơ đồ và bảng tổng hợp nằm phần 2; phần 3 dùng chữ/bảng và dẫn bằng chứng. Không tạo screenshot giả, không bịa username hay tuyên bố mọi mục đạt.

Mục 3.1.8 có dữ liệu release age: một số phiên bản action chưa hơn 60 ngày, một số alias không có release date đáng tin. Không hạ phiên bản hay đánh dấu đạt để che phát hiện. Gitleaks lịch sử nguồn vẫn có phát hiện, không thêm allowlist/continue-on-error để che lỗi.

## An toàn và khôi phục

Main không đổi. Nhánh mới chỉ có file/config lab; không có database migration hoặc triển khai mạng. Không có thao tác xóa/force-push. Để bỏ đề xuất, không merge nhánh. Không cần rollback main. Không bật hook cho người khác tự động; người muốn sử dụng tự cấu hình `git config core.hooksPath .githooks` sau khi đọc file.

Kết quả remote và commit đã kiểm tra sẽ ghi trong [RESULTS.vi.md](RESULTS.vi.md). File xuất được lưu trong artifacts phiên chạy nhánh.
