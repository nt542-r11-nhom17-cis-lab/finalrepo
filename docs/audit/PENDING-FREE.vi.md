# Triển khai 12 mục Free còn thiếu

Đợt này chỉ xử lý 12 mục còn NOT_TESTED của phạm vi 48 Free sau commit d48d6bc. Không triển khai lại 36 mục đã có bằng chứng; không mua/dùng Enterprise, không sửa main hay hai repo nguồn. Mọi thay đổi ở `audit/remaining-free-integration`. Công cụ đã chạy hoặc đã chuẩn bị không đồng nghĩa yêu cầu CIS đã đạt toàn bộ.

## Audit → Remediation → Re-audit

Audit lấy API GET hiện trạng với phân trang, đọc nguồn workflow, danh tính numeric ID và khóa phiên bản/hash của đầu vào. Remediation bổ sung guard build, monitor thay đổi mã, collector và preflight. Re-audit dùng unit tests từ chối và CI chạy thực trên nhánh audit. Không giả danh tài khoản khác để tạo approval; không đổi quyền hoặc thử mật khẩu mặc định.

| Mục | Triển khai/bằng chứng mới | Trạng thái và phần còn thiếu |
|---|---|---|
| 1.1.19 | Snapshot/digest protection và rulesets, so sánh với baseline qua audit_pending_free.py | PARTIAL. Classic 403 là UNKNOWN; rulesets nhìn thấy rỗng. So sánh không thay audit event actor/time; không đổi rule thật |
| 1.3.1 | Inventory thành viên/owners có phân trang, đối chiếu 4 collaborator và vai trò | PARTIAL. Danh sách thành viên nhìn thấy rỗng không phải tổng thành viên. Thiếu last-login, lịch rà được duyệt và quyết định thu hồi |
| 1.3.3 | Thử đọc org owners và kiểm kê quyền quản trị repo | MANUAL_REVIEW. Không suy 0 owner nhìn thấy thành organization không owner; cần người quản trị xác minh phạm vi và số tối thiểu |
| 1.3.4 | Thu field MFA requirement và thử filter 2fa_disabled | MANUAL_REVIEW. Field UNKNOWN, filter 422; không thay enforcement. Xác nhận người dùng về 3 tài khoản đã bật không thay policy bắt buộc |
| 1.3.6 | Thử kiểm kê lời mời, giữ kín email; liên kết quy trình dự thảo | MANUAL_REVIEW. API 403; chưa có approved-email list/approval và đối chiếu invitation thật |
| 1.3.13 | code_change_monitor.py: snapshot/hash workflow, thay đổi đường dẫn nhạy cảm, từ chối một số mẫu nguy hiểm | PARTIAL. Heuristic có giới hạn; chưa có phát hiện hành vi toàn diện hoặc xác nhận người nhận xử lý cảnh báo |
| 2.1.5 | Job condition và guard ID của ba người có quyền Write/Admin hiện tại | PARTIAL. Không thay ACL platform; writer có thể sửa chính workflow/policy, required review chưa được chứng minh |
| 2.1.6 | Kiểm context Actions, actor ID, rerun actor; anonymous GET runner metadata trả 403 | PARTIAL. Negative tests là kiểm logic; không phải đăng nhập thật bằng người khác hay kiểm mọi đường quản trị |
| 2.1.11 | Kiểm repo admin counts và thử Actions/runner administration GET | MANUAL_REVIEW. 1 repo Admin không chứng minh admin của toàn bộ hạ tầng hosted; cần owner duyệt số tối thiểu |
| 3.1.2 | supplier_intake.py lập ledger 43 đầu vào trực tiếp, version/hash và tình trạng supplier SBOM | MANUAL_REVIEW. 43/43 chưa có supplier-issued SBOM được xác minh; không dùng SBOM tự sinh hoặc GitHub export thay supplier |
| 5.2.3 | deployment_preflight.py chỉ đọc account/group/SSH flags, đã chạy thử workspace | NOT_TESTED cho production. Workspace không phải VM người dùng hoặc production; cần target thực tế được phép |
| 5.2.4 | Preflight không đọc password hash, không thử đăng nhập, không thay account | NOT_TESTED cho production. Không thể kết luận mật khẩu không mặc định từ account name hoặc SSH flag |

## Giới hạn quyền chạy build

`config/build-access.json` chỉ giữ ba principal có quyền thực đã được người dùng xác nhận và GET API đối chiếu: hieune-ui (Admin), Vuongdlx và HiepTran01 (Write). Numeric ID được ghim; dtk0106 (Read) không nằm trong danh sách. Không cấp hoặc thu hồi quyền GitHub nào.

Bốn workflow audit đang dùng được thêm điều kiện trước khi job khởi động: đúng repository ID, ref thuộc audit, actor ID và triggering actor trong danh sách. Sau checkout, build_access_guard.py kiểm thêm repository name, exact audited refs, event push/workflow_dispatch, cặp login/ID và rerun actor. Repo fork, main, Read actor, ID giả, event không cho phép và thiếu context bị từ chối trong negative tests. Việc chạy từ máy local không có context Actions cũng bị từ chối; môi trường local có thể giả biến nên không dùng nó làm bằng chứng xác thực người dùng.

Đây là guard của workflow trên nhánh audit, không phải hệ thống đăng nhập mới. Workflow source vẫn có thể được writer sửa. Cần bảo vệ/review workflow và kiểm toàn bộ đường quản trị trước khi kết luận toàn mục. Quyền token vẫn giữ contents:read; CodeQL giữ security-events:write chỉ ở job upload SARIF. Không thêm secret, OIDC hoặc token write mới.

## Theo dõi thay đổi mã và rule

code_change_monitor.py so hai commit Git, ghi đường dẫn nhạy cảm và SHA256 workflow. Job dùng checkout fetch-depth=2 để đọc parent thật. Các mẫu bị chặn gồm cấu hình pull_request_target, permissions:write-all và persist-credentials:true ở dạng được checker hỗ trợ. Đây là kiểm tra mẫu hẹp, chạy bổ sung cho Zizmor; không phải parser YAML tổng quát, không thay phát hiện hành vi insider hoặc runtime.

Artifact CI ghi `review_required` khi có thay đổi nhạy cảm. Nó không gửi tin cho thành viên, không xác nhận họ đã đọc và không bịa incident acknowledgment. `tracked_worktree_dirty` phân biệt nguồn đang sửa với snapshot commit. Nội dung đường dẫn không được thực thi thành shell command.

Baseline policy lưu digest từ GET đọc được. Classic protection 403, thiếu field hoặc snapshot trước không đọc được đều cho UNKNOWN. Rulesets có thể có snapshot nhưng chưa có phép đổi rule thật và audit event. Không gọi Organization Audit Log API cần Enterprise, không POST ruleset và không sửa main. Cảnh báo drift chỉ là yêu cầu review, không kết luận ai sửa hoặc có vi phạm.

## Supplier và production

Ledger supplier gồm 32 wheel PyPI, 9 action repo/ref, base image và registry binary custom. Phạm vi là đầu vào trực tiếp được chọn, không phải mọi package bắc cầu hoặc mọi supplier của nhóm. Release upstream Distribution v3.1.2 có provenance asset nhưng không có asset mang tên SBOM trong danh sách được rà; binary custom khác upstream, không suy provenance upstream xác nhận custom build.

Không có supplier SBOM nào được công cụ này xác minh. Việc inventory chuyển mục sang MANUAL_REVIEW vì đã đối chiếu thiếu bằng chứng, không phải đã đáp ứng yêu cầu. Supplier cần cung cấp tài liệu đúng artifact/version; policy tiếp nhận và xử lý ngoại lệ cần nhóm phê duyệt.

Host preflight chỉ chạy đọc trên cloud workspace ở đợt này. Nó ghi root/group flags và số account, không xuất username, password hash, private key, env hoặc chi tiết lỗi sshd. sshd -T không đọc được trả UNKNOWN; ngay cả khi đọc được cũng chưa giải quyết mọi Match block, sudo/IdP/cloud IAM hoặc cấu hình daemon đang chạy. Không nâng quyền, không tự kết nối VM và không thử password. Không chuyển hai mục production sang PARTIAL chỉ vì có script.

## Tái kiểm tra và đầu ra

```bash
python3 -m unittest discover -s tests -v
python3 scripts/audit_pending_free.py --previous docs/audit/evidence/pending-free-baseline.json
python3 scripts/supplier_intake.py
python3 scripts/code_change_monitor.py
python3 scripts/deployment_preflight.py
```

Các lệnh collector cần mạng/API phù hợp nhưng không yêu cầu token mới. Dùng quyền hiện có; API chặn không tự động xin hoặc nâng quyền. Không đưa token vào command/chat. build_access_guard.py được CI gọi; chạy local không có context sẽ trả mã 2 đúng chủ đích.

Bằng chứng đã lưu: [baseline GET](evidence/pending-free-baseline.json), [supplier intake](evidence/supplier-intake-review.json), [preflight cloud](evidence/pending-cloud-preflight.json). CI lưu báo cáo mới của collector, guard và monitor cùng artifact integration; scope/privilege của CI khác token người dùng nên kết quả có thể khác, không ghi đè baseline cũ thành cùng một phép đo.

Sau đối chiếu: **32 PARTIAL, 14 MANUAL_REVIEW, 2 NOT_TESTED trong 48 mục Free**. Toàn 120: **80 PARTIAL, 28 MANUAL_REVIEW, 7 LAB_ONLY, 5 NOT_TESTED**; ba trong năm NOT_TESTED là Enterprise ngoài phạm vi Free. **Full-control PASS=0**. Còn điều kiện thực tế ở cả PARTIAL/MANUAL_REVIEW, không chỉ hai mục production.
