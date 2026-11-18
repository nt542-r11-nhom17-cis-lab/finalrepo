# Đối chiếu bằng chứng và công việc còn thiếu ngày 18/11/2026

Nhánh `audit/remaining-free-integration`. Không sửa main hoặc hai repo nguồn, không đổi quyền, bật yêu cầu MFA, cài app, tạo webhook GitHub, xóa nhánh hoặc archive repo. Ba mục Enterprise 1.3.10/1.3.11/1.3.12 tiếp tục nằm ngoài phạm vi triển khai Free.

## Bằng chứng VMware

Người dùng chạy script trong Ubuntu 22.04.4 LTS, Python 3.10.12; màn hình ban đầu cho thấy 2 CPU, RAM khoảng 2 GiB và phân vùng root còn 4.3 GiB. Việc tăng RAM lên 4 GiB đã được hướng dẫn nhưng chưa có đầu ra xác nhận; không ghi là đã thực hiện. Người dùng xác nhận tạo venv và chuyển báo cáo qua SCP. Chưa có phép đo cấu hình SSH, quyền toàn host hoặc tài khoản mặc định.

| Báo cáo | Kết quả do báo cáo ghi nhận | Phạm vi |
|---|---|---|
| supply-chain/results.json | 5/5 PASS | Input locks, artifact tái lập, chữ ký/tamper, mã hóa và triển khai tạm cục bộ |
| registry-lab/results.json | 13/13 PASS | Mô hình offline với role/MFA claim giả lập; không phải registry thực |
| webhook-https/results.json | 11/11 PASS | HTTPS loopback, HMAC, replay, request policy và TLS trust; dữ liệu tổng hợp |

Tổng 29/29 là số phép thử, không phải số tiêu chí CIS đạt. Đây là báo cáo người dùng cung cấp; không có signed attestation ràng buộc nguồn thực thi/commit của VM. Kiểm tra file không thay cho quan sát thực thi độc lập. Dịch vụ webhook báo đã dừng, không xuất credential. Replay cache ở bộ nhớ tồn tại 600 giây và mất khi restart; identical body có thể bị từ chối dù hợp lệ. Không xác nhận delivery thật từ GitHub, registry triển khai trên VM, production hoặc MFA thật từ các test mô phỏng.

Bản gốc nhỏ chỉ gồm ba JSON nằm trong [vm-lab-results.tar.gz](evidence/vm-lab-results.tar.gz). Bản tổng hợp có SHA256 từng báo cáo và archive: [vm-lab-review.json](evidence/vm-lab-review.json). Có thể tái kiểm tra:

```bash
python3 scripts/import_vm_evidence.py docs/audit/evidence/vm-lab-results.tar.gz --output reports/vm-evidence/results.json
```

Importer đọc đúng ba member cho phép, không giải nén đường dẫn hoặc thực thi nội dung archive; từ chối file thiếu, trùng, sai loại, quá kích thước hoặc kết quả không rõ. FAIL được giữ lại và CLI trả mã lỗi. Nó chỉ xác nhận cấu trúc/kết quả báo cáo khai báo, không xác thực danh tính máy hoặc chính sách CIS.

## Settings, ứng dụng và SBOM

[manual-settings-review.json](evidence/manual-settings-review.json) phân biệt ảnh/xác nhận người dùng với phép đo API. Ảnh hội thoại chưa được lưu thành bộ ảnh độc lập trong repo; cần giữ nguồn gốc này khi trình bày. Không bịa screenshot hoặc suy HTTP 403 thành cấu hình tắt.

- 1.4.1: đã xem giới hạn cài app cho repo admin; còn xác nhận lưu/tải lại và approval trail.
- 1.4.2: đã rà app hiện có và mục đích sử dụng; còn chu kỳ rà/người chịu trách nhiệm được nhóm duyệt.
- 1.4.3: app được giới hạn ở finalrepo; cần biện minh đầy đủ quyền, kể cả issues/PR. Không tự gỡ connector đang dùng.
- Base permissions No permission, giới hạn team/delete/transfer/visibility/issue, Secret Protection/Push protection và Dependabot đã có quan sát UI. Bảng JSON nêu phần nào còn thiếu xác nhận lưu hoặc hiệu lực.

Ba mục ứng dụng chuyển NOT_TESTED sang PARTIAL. Các mục chính sách khác giữ trạng thái cần kiểm tra khi chưa đủ re-audit.

SBOM GitHub native được giữ nguyên trong [github-native-sbom.spdx.json](evidence/github-native-sbom.spdx.json), có [bản đối chiếu](evidence/github-native-sbom-review.json): SPDX 2.3, tạo ngày 17/11/2026 18:11:52 UTC (18/11 lúc 01:11:52 giờ Việt Nam), 10 package gồm repo và 9 action/version entries của 8 action repo. Nó mô tả snapshot main lúc xuất, không phải toàn bộ audit checkout; không bao phủ 32 Python wheels/104 Go components hoặc thay SBOM do mọi supplier phát hành. Không có package checksum/license và chưa xác minh chữ ký tài liệu.

## Quyền và MFA

GET inventory mới: một repo nhìn thấy, bốn tài khoản (1 Admin, 2 Write, 1 Read), tám nhánh, zero fork nhìn thấy, phân trang đầy đủ. [Organization](evidence/organization-review-2026-11-18.json), [branches/forks](evidence/governance-review-2026-11-18.json). API app/invitations/org hooks còn 403; không suy ra danh sách rỗng. Không xóa/đổi quyền dựa vào tuổi branch.

| Tài khoản | Quyền repo do người dùng xác nhận | MFA do người dùng xác nhận | Giới hạn |
|---|---|---|---|
| hieune-ui | Admin | Đã bật | Chưa có kiểm thử rule/bypass đầy đủ |
| Vuongdlx | Write | Đã bật | Có thể review độc lập; chưa có approval thử thật |
| HiepTran01 | Write | Đã bật | Cập nhật thay snapshot Read cũ; chưa có approval thử thật |
| dtk0106 | Read | Chưa hoàn tất | Không tính approval Read vào required Write+ reviewers |

MFA trong API inventory vẫn UNKNOWN; bảng này là xác nhận của người dùng. Chưa yêu cầu MFA toàn organization khi Dương chưa chuẩn bị xong. Chỉ có một repo Admin quan sát được; không tự nâng quyền hoặc ghi có admin dự phòng. Vai trò thực hiện các nhóm công việc và CODEOWNERS mới vẫn cần quyết định của nhóm.

## Các phần có thể tiếp tục tự động hóa và các điều kiện còn thiếu

Đã hoàn thiện việc nhập bằng chứng, kiểm kê GET, giữ SBOM native, cập nhật bảng 120/48 mục và chuẩn bị quy trình nhóm. [REMAINING-FREE.vi.md](REMAINING-FREE.vi.md) liệt kê trạng thái/giới hạn của đủ 48 mục.

| Nhóm | Việc đã chuẩn bị / có thể làm bằng code | Điều kiện chưa thể tự thay thế |
|---|---|---|
| Review/bảo vệ nhánh | Mẫu ruleset chỉ cho audit/protection-sandbox, test plan từng mục | Quyền đọc/apply rules và hai reviewer thật; không PR vào main |
| Quyền, thành viên, app, audit log | Inventory, bảng vai trò, bản nháp quy trình | Nhóm phê duyệt cadence/role; audit log UI; danh sách email mời được duyệt giữ riêng |
| MFA | Ghi nhận phạm vi thiếu và hướng dẫn | Từng người tự thiết lập; không dùng fixture registry thay MFA thật |
| Supplier/license | Locks, hash checks, SBOM native và toolchain inventory | SBOM/provenance/chữ ký supplier và quyết định duyệt license thực tế |
| Deployment | Supply-chain local demo và báo cáo VM | Quyền production, toàn bộ account/default passwords chưa được kiểm thử; VM chỉ là lab |
| Registry/webhook thực | Đã có dịch vụ loopback thật trong môi trường kiểm thử | Chưa có bằng chứng registry trên VM hoặc GitHub delivery đến endpoint được duyệt |

Tổng hiện hành: **75 PARTIAL, 23 MANUAL_REVIEW, 7 LAB_ONLY, 15 NOT_TESTED; full-control PASS=0**. Trong 48 mục Free ban đầu: **27 PARTIAL, 9 MANUAL_REVIEW, 12 NOT_TESTED**. Không chỉ còn 12 mục để hoàn thành: tất cả PARTIAL/MANUAL_REVIEW cũng còn điều kiện.

## Re-audit độc lập trong workspace

Đã chạy lại 58 unit tests, 11 webhook HTTPS checks và 23 registry HTTPS checks (hai phiên bản), đều thành công trong workspace của người triển khai. Không ghi các kết quả này là chạy trên VM người dùng. 32/32 wheel hash khớp PyPI; 20 license vẫn cần quyết định thủ công theo policy chưa phê duyệt. Numeric identity của 9 action repo/owner không đổi; zero Bandit HIGH ở scripts. Chưa lặp quét Go CVE database trong bước local này; baseline quét 104 package của đợt trước giữ thời điểm riêng.

[Bản tổng hợp re-audit](evidence/current-review-summary.json), [webhook](evidence/webhook-reaudit-2026-11-18.json), [registry](evidence/registry-reaudit-2026-11-18.json), [wheel/license](evidence/python-toolchain-review-2026-11-18.json), [action owner](evidence/action-owners-review-2026-11-18.json).
