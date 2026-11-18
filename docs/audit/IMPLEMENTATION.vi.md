# 3. Triển khai thực nghiệm

## 3.1 Môi trường và phạm vi

Mã nguồn và cấu hình nằm trong repository public `nt542-r11-nhom17-cis-lab/finalrepo`, thuộc Organization Free. Nhánh tổng hợp là `audit/remaining-free-integration`; main được giữ tại `e052945db5b4a2bace480b5ab98446a8b82da02e`. Hai repository nguồn không thay đổi. Hình mô hình và ảnh thực nghiệm nằm trong phần 2 của [METHOD.vi.md](METHOD.vi.md); phần này trình bày bằng chữ và bảng.

| Thành phần | Môi trường và chức năng | Giới hạn |
|---|---|---|
| Repository/Organization | Lưu nguồn, quyền cộng tác, Settings và Actions | Một số endpoint quản trị bị giới hạn quyền |
| CI | GitHub-hosted runner Ubuntu 24.04 | Không đại diện toàn bộ cấu hình hạ tầng nhà cung cấp |
| Container demo | Non-root, read-only, bỏ capabilities và mạng trong smoke test | Chỉ container được kiểm thử |
| Webhook receiver | HTTPS loopback, HMAC SHA256, request policy | Delivery tổng hợp, không cài webhook trên GitHub |
| Registry | Distribution custom build, TLS, bcrypt, hai phiên bản OCI | Không có IdP/MFA thật hoặc registry-side signature admission |
| VMware lab | Ubuntu 22.04.4 LTS, Python 3.10.12 | Không phải production; VM do người thực nghiệm vận hành |

## 3.2 Tài khoản và quyền

GET inventory đọc được bốn collaborator với 1 Admin, 2 Write và 1 Read. Đây là phạm vi nhìn thấy của token; không thay kiểm kê toàn bộ quyền kế thừa hoặc Org Owners. Danh sách thành viên/owner công khai rỗng không có nghĩa organization không có thành viên hoặc owner.

| Tài khoản | Quyền repo được xác nhận | MFA theo xác nhận của người thực nghiệm |
|---|---|---|
| hieune-ui | Admin | Đã bật |
| Vuongdlx | Write | Đã bật |
| HiepTran01 | Write | Đã bật |
| dtk0106 | Read | Chưa hoàn tất |

Nguồn: [inventory](evidence/organization-review-2026-11-18.json), [bảng Settings](evidence/manual-settings-review.json). API MFA vẫn UNKNOWN; xác nhận của cá nhân không thay chính sách cưỡng chế MFA. Chưa có phê duyệt lựa chọn repo Admin dự phòng hoặc bằng chứng hai reviewer độc lập đã thực hiện một PR thử. CODEOWNERS không tự cấp quyền và không tự bắt buộc review.

## 3.3 Kiểm tra cấu hình GitHub

| Phạm vi | Quan sát từ giao diện | Giới hạn kiểm chứng |
|---|---|---|
| Quyền nền | Base permissions: No permission, đã có ảnh sau tải lại | Cần đối chiếu toàn bộ grant trực tiếp/kế thừa |
| Quyền thành viên | Tắt tạo team, delete/transfer repo, đổi visibility và xóa issue theo các ảnh đã kiểm tra | Một số cấu hình cần xác nhận lưu và hiệu lực theo vai trò |
| Ứng dụng | ChatGPT Codex Connector giới hạn ở finalrepo; đã rà quyền hiển thị | Cần biện minh đủ quyền và hồ sơ phê duyệt/rà định kỳ |
| Webhook GitHub | Trang repo và organization không có hook tại thời điểm quan sát | Tách biệt với receiver loopback thử nghiệm |
| Secret Protection | Đã bật; Push protection On; zero native alert mở tại thời điểm quan sát | Không suy lịch sử sạch hoặc credential cũ đã thu hồi |
| Dependabot | Dependency graph/alerts On; hai auto-dismiss presets Disabled | Security/version updates chưa bật; zero alert không chứng minh mọi dependency an toàn |

Chi tiết provenance và phần chưa xác minh được giữ trong `evidence/manual-settings-review.json`. Ảnh hội thoại chưa được lưu thành bộ ảnh độc lập trong repository. Dữ liệu API 403/422, trường thiếu hoặc response không đủ schema được ghi UNKNOWN; không suy ra false hoặc PASS.

## 3.4 Công cụ và đầu ra

| Công cụ | Đầu ra chính | Phạm vi |
|---|---|---|
| audit_github.py, audit_organization.py | Cấu hình API và trạng thái quyền đọc | GET-only, cấu hình thành phần |
| audit_all.py, audit_free_controls.py | Readiness 120/48 tiêu chí | Không phải công cụ chứng nhận tuân thủ |
| inventory_governance.py, inventory_organization.py | Repo, branch, fork và role counts | Không tự xóa, archive hoặc đổi quyền |
| audit_dependencies.py, monitor_action_owners.py | Action refs, numeric repo/owner IDs | Chín action repo ở snapshot đã đo |
| audit_python_toolchain.py, dependency_graph.py | Hash, license, tuổi phiên bản và graph | 32 scanner wheels; policy license chưa phê duyệt |
| project_bundle.py | Source ZIP, SPDX, provenance, signed manifest | Khóa ký tạm; có kiểm thử sửa dữ liệu/khóa sai |
| supply_chain_lab.py | Artifact/SBOM/provenance, mã hóa và local deployment | Sandbox, không production |
| registry_lab.py | Các phép kiểm role/MFA claim | Mô hình offline, không xác minh MFA thật |
| webhook_integration.py, registry_integration.py | Kết quả HTTPS dương/âm | Tiến trình loopback riêng, tự dừng sau test |
| build_registry.py, verify_registry_scan.py | Binary ghim hash và kiểm coverage scanner | Không chấp nhận scan rỗng/sai binary |
| import_vm_evidence.py | Hash và tổng hợp báo cáo VM | Báo cáo được cung cấp, không signed remote attestation |
| build_access_guard.py | Kết quả kiểm danh tính chạy build | Guard trong workflow, không thay GitHub ACL/MFA |
| code_change_monitor.py | Diff đường dẫn nhạy cảm, hash workflow, finding | Heuristic giới hạn, không xác nhận người nhận cảnh báo |
| audit_pending_free.py | GET evidence và policy digest comparison | Không truy cập Audit Log API Enterprise |
| supplier_intake.py | Ledger version/hash và supplier SBOM còn thiếu | 43 đầu vào trực tiếp được chọn |
| deployment_preflight.py | Metadata account/group/SSH chỉ đọc | Không đọc hash mật khẩu, thử login hoặc thay account |

## 3.5 Giới hạn quyền chạy build và giám sát

`config/build-access.json` giữ numeric ID của ba tài khoản có Write/Admin hiện tại. Bốn workflow audit kiểm repository ID, nhánh audit, actor ID và triggering actor trước khi khởi động job; sau checkout, guard kiểm thêm exact ref, event và cặp login/ID. Không cấp quyền mới. Negative unit tests bao phủ main, fork, Read actor, ID sai, rerun không được phép và thiếu context.

Guard local có thể bị giả context nên chỉ kết quả chạy trên nền tảng có giá trị đối chiếu danh tính CI. Người có quyền sửa workflow vẫn có thể sửa policy; cần required reviews/protection trước khi kết luận đầy đủ. Token giữ contents:read; CodeQL chỉ có security-events:write trong job upload SARIF.

Monitor đọc hai snapshot Git và hash workflow, ghi `review_required` khi thay đổi đường dẫn nhạy cảm. Checker bổ sung từ chối một số dạng pull_request_target, permissions:write-all và persist-credentials:true; Zizmor vẫn là phép quét cấu hình riêng. Đây không phải parser YAML tổng quát hay hệ thống phát hiện hành vi toàn diện. Artifact không chứng minh người phụ trách đã đọc/xử lý cảnh báo.

Snapshot ruleset được so bằng digest. Classic protection bị 403 hoặc thiếu baseline cho UNKNOWN. Không đổi rule để tạo event, không xác nhận actor/time của thay đổi thực và không gọi API Audit Log Enterprise.

## 3.6 Dependency, supplier và artifact

GitHub native SPDX 2.3 được giữ nguyên trong [github-native-sbom.spdx.json](evidence/github-native-sbom.spdx.json): 10 package gồm repo và 9 action/version entries của 8 repo Actions, tạo 17/11/2026 18:11:52 UTC. Export mô tả main lúc xuất, không bao phủ mọi thành phần của audit branch, Python hay Go. Chưa xác minh chữ ký export; package records không có license/checksum.

Ledger supplier có 32 PyPI wheels, 9 Actions, base image và registry binary custom. Chưa có supplier-issued SBOM được xác minh cho 43 đầu vào này. SBOM do nhóm hoặc GitHub tổng hợp không thay tài liệu do supplier phát hành. License policy và quy trình [governance](GOVERNANCE-DRAFT.vi.md) vẫn là dự thảo chưa được nhóm phê duyệt.

Registry custom được build bằng SDK/source/module locks đã ghim. Kết quả trước/sau scan và 23 phép thử HTTPS được mô tả trong [INTEGRATION.vi.md](INTEGRATION.vi.md). Chữ ký được pipeline/client kiểm tra, không phải chính sách admission của registry. [CODEQL.vi.md](CODEQL.vi.md) ghi riêng việc đối chiếu hai cảnh báo public digest và phân tích lại cùng bộ rule.

## 3.7 Triển khai trên VMware

Ba báo cáo gốc gồm 5 phép thử supply chain, 13 phép thử registry mô phỏng và 11 phép thử webhook HTTPS. [Archive](evidence/vm-lab-results.tar.gz) chỉ chứa ba JSON; [review](evidence/vm-lab-review.json) có hash và scope. Tổng 29 PASS là phép thử lab, không phải 29 tiêu chí CIS. Archive được kiểm cấu trúc/kích thước/member; không giải nén đường dẫn hoặc thực thi nội dung. Chưa có signed attestation ràng buộc VM/commit.

Người thực nghiệm tiếp tục cấu hình tài khoản OS và kiểm tra qua SSH trên VMware. [Biên bản](evidence/vm-access-review.json) ghi rõ nguồn là đầu ra terminal và xác nhận trong phiên hướng dẫn, không phải phép đo từ API hoặc signed remote attestation.

| Kiểm tra | Kết quả được cung cấp |
|---|---|
| Quyền cisdeploy | Chỉ nhóm cisdeploy; `sudo -l -U cisdeploy` báo không được chạy sudo |
| Thư mục triển khai | `/opt/cis-deploy-lab`, owner/group cisdeploy, mode 700 |
| Người được cấp quyền | cisdeploy tạo được file, kể cả sau SSH login |
| Người không được cấp quyền | nobody tạo file bị Permission denied |
| Mật khẩu OS | root L; user và cisdeploy P; không xuất password/hash |
| SSH root và mật khẩu rỗng | PermitRootLogin no, PermitEmptyPasswords no theo xác nhận cấu hình hiệu lực |
| Kiểm tra sau reload | user và cisdeploy đăng nhập được từ phiên PowerShell mới |

Tài khoản quản trị user vẫn có sudo theo nhu cầu quản lý VM. Quyền 700 không chặn root hoặc quản trị viên được ủy quyền. Trạng thái P chỉ xác nhận có mật khẩu, không chứng minh không dùng mật khẩu mặc định; nguồn mật khẩu user chưa được xác nhận độc lập. Chưa rà mọi service/application account. Hai mục 5.2.3/5.2.4 vì vậy có bằng chứng thành phần trong lab, không phải xác nhận tuân thủ production.

## 3.8 Phạm vi chưa kiểm chứng đầy đủ

Các điều kiện còn thiếu nằm ở từng dòng [COVERAGE.vi.md](COVERAGE.vi.md): bảo vệ/review hiệu lực, hồ sơ rà định kỳ, MFA bắt buộc, approved-email invitations, đầy đủ supplier evidence và production. Ba mục Enterprise 1.3.10/1.3.11/1.3.12 nằm ngoài phạm vi triển khai Free. Không thay lỗi quyền API, mô phỏng hoặc tài liệu dự thảo thành PASS toàn tiêu chí.
