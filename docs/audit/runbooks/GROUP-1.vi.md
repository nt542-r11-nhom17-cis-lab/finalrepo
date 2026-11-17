# Nhóm 1: 50 quy trình Audit–Remediation–Re-audit

Đủ quy trình không đồng nghĩa đủ triển khai hoặc đạt tuân thủ. Hướng dẫn dưới đây diễn giải để áp dụng lab; đối chiếu Audit/Remediation gốc tại trang tham chiếu khi thực hiện. Phạm vi đợt đánh giá không bao gồm thay đổi settings, quyền người dùng, xóa tài nguyên hoặc chỉnh sửa main. Khi kiểm tra lại, ghi đối tượng, ref, người thực hiện, thời gian và bằng chứng trước/sau; các phép thử gây thay đổi chỉ thực hiện trên đối tượng thử được phê duyệt.

## 1.1.1 — Ensure any changes to code are tracked in a version control platform

CIS: **Manual**, trang 19.

**Audit:** Đối chiếu nguồn đang chạy với lịch sử Git và commit của mọi thay đổi.

**Remediation đề xuất:** Đưa nguồn chưa quản lý vào VCS; bắt buộc thay đổi qua quy trình review.

**Re-audit:** Tạo một thay đổi thử trên nhánh audit, kiểm tra diff/commit rồi đối chiếu SHA trong provenance.

**Nguồn bằng chứng cần có:** repository_files, branches, pull_requests.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.2 — Ensure any change to code can be traced back to its associated task

CIS: **Manual**, trang 20.

**Audit:** Lấy mẫu commit/PR và truy về issue hoặc task được giao.

**Remediation đề xuất:** Yêu cầu mã task và liên kết issue trong mẫu PR, kiểm tra thủ công tính đúng của liên kết.

**Re-audit:** Lấy mẫu commit/PR sau thay đổi quy trình, mở liên kết issue/task và đối chiếu nội dung thay đổi với nhiệm vụ; ghi riêng trường hợp thiếu hoặc liên kết sai.

**Nguồn bằng chứng cần có:** repository_files, branches, pull_requests.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.3 — Ensure any change to code receives approval of two strongly authenticated users

CIS: **Automated**, trang 22.

**Audit:** Đọc required approvals và kiểm thử PR thiếu hai reviewer độc lập; xác minh strong authentication.

**Remediation đề xuất:** Yêu cầu hai phê duyệt theo Audit và chính sách xác thực mạnh; xem xét bypass.

**Re-audit:** Trên PR thử, kiểm tra merge bị chặn khi chỉ có một approval và khi reviewer không đáp ứng xác thực mạnh; kiểm tra hai reviewer độc lập, đủ điều kiện cùng mọi check bắt buộc trước khi kết luận.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.4 — Ensure previous approvals are dismissed when updates are introduced to a code change proposal

CIS: **Manual**, trang 24.

**Audit:** Đọc dismiss-stale; đẩy commit thay đổi vào PR đã được duyệt.

**Remediation đề xuất:** Bật hủy phê duyệt cũ và kiểm tra yêu cầu review lại.

**Re-audit:** Phê duyệt PR thử rồi push thêm commit; ghi nhận approval cũ bị dismiss và merge vẫn bị chặn đến khi có review mới.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.5 — Ensure there are restrictions on who can dismiss code change reviews

CIS: **Manual**, trang 26.

**Audit:** Kiểm tra danh sách người/nhóm được dismiss review và bypass.

**Remediation đề xuất:** Giới hạn dismiss cho tài khoản tin cậy đã được phê duyệt.

**Re-audit:** Dùng tài khoản có quyền và không có quyền thử dismiss; lưu kết quả chấp nhận/từ chối.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.6 — Ensure code owners are set for extra sensitive code or configuration

CIS: **Manual**, trang 28.

**Audit:** Tìm CODEOWNERS, so đường dẫn nhạy cảm và quyền owner.

**Remediation đề xuất:** Khai báo owner có quyền phù hợp cho mã/cấu hình nhạy cảm.

**Re-audit:** Lấy mẫu file workflow, secret configuration và deployment; đối chiếu pattern CODEOWNERS với người có quyền thực tế và yêu cầu review của từng file.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.7 — Ensure code owner's review is required when a change affects owned code

CIS: **Manual**, trang 30.

**Audit:** Đọc required code-owner review và thử PR sửa file có owner.

**Remediation đề xuất:** Bắt buộc code-owner review trên quy tắc có hiệu lực.

**Re-audit:** PR sửa file thuộc sở hữu phải bị chặn khi chưa có Code Owner approval.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.8 — Ensure inactive branches are periodically reviewed and removed

CIS: **Manual**, trang 32.

**Audit:** Liệt kê nhánh, ngày commit cuối, chủ sở hữu và biên bản rà soát.

**Remediation đề xuất:** Đặt lịch rà soát; chỉ xóa nhánh sau khi xác nhận không còn sử dụng.

**Re-audit:** Đối chiếu danh sách trước/sau và lịch rà soát tháng tiếp theo.

**Nguồn bằng chứng cần có:** repository_files, branches, pull_requests.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.9 — Ensure all checks have passed before merging new code

CIS: **Manual**, trang 34.

**Audit:** Đọc required checks; thử PR có check thất bại.

**Remediation đề xuất:** Bắt buộc checks phù hợp và kiểm soát bypass trước merge.

**Re-audit:** Cho một required check thất bại trên PR thử và kiểm tra merge bị chặn; chạy lại thành công, đối chiếu tên check với rule và rà mọi bypass actor.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.10 — Ensure open Git branches are up to date before they can be merged into code base

CIS: **Manual**, trang 36.

**Audit:** Kiểm tra strict/up-to-date requirement và PR tụt sau base.

**Remediation đề xuất:** Bật yêu cầu nhánh cập nhật trước merge hoặc cơ chế tương đương.

**Re-audit:** Cập nhật base branch thử sau khi CI xanh; PR cũ phải yêu cầu cập nhật/chạy lại.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.11 — Ensure all open comments are resolved before allowing code change merging

CIS: **Manual**, trang 38.

**Audit:** Kiểm tra conversation resolution và PR còn comment chưa giải quyết.

**Remediation đề xuất:** Bắt buộc giải quyết hội thoại trước merge.

**Re-audit:** Để một review thread chưa resolve: merge bị chặn; resolve rồi kiểm tra lại.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.12 — Ensure verification of signed commits for new changes before merging

CIS: **Manual**, trang 40.

**Audit:** Kiểm tra required signatures và commit verification.

**Remediation đề xuất:** Bắt buộc commit ký được nền tảng xác minh; quản lý khóa người ký.

**Re-audit:** Commit không ký phải bị từ chối; commit ký hợp lệ phải được nhận khi đủ điều kiện còn lại.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.13 — Ensure linear history is required

CIS: **Manual**, trang 42.

**Audit:** Đọc linear-history rule và lịch sử merge.

**Remediation đề xuất:** Bật linear history và chọn cách merge phù hợp.

**Re-audit:** Thử merge commit vào nhánh thử phải bị chặn; squash/rebase đúng policy được nhận.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.14 — Ensure branch protection rules are enforced for administrators

CIS: **Manual**, trang 44.

**Audit:** Xem enforce-admins và các bypass actor.

**Remediation đề xuất:** Áp dụng bảo vệ cho admin; giảm ngoại lệ theo chính sách.

**Re-audit:** Admin thử push/merge thiếu điều kiện trên nhánh thử phải bị chặn.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.15 — Ensure pushing or merging of new code is restricted to specific individuals or teams

CIS: **Manual**, trang 46.

**Audit:** Đọc push restrictions và danh sách team/user.

**Remediation đề xuất:** Chỉ cho người/nhóm được phê duyệt push hoặc merge.

**Re-audit:** Tài khoản ngoài danh sách thử push/merge bị từ chối; người hợp lệ vẫn cần đủ review/CI.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.16 — Ensure force push code to branches is denied

CIS: **Manual**, trang 48.

**Audit:** Đọc force-push rule; thử trên nhánh disposable được bảo vệ.

**Remediation đề xuất:** Cấm force push và xem lại bypass.

**Re-audit:** Chỉ trên nhánh thử được bảo vệ, thử cập nhật non-fast-forward bằng tài khoản được phép kiểm thử; lưu thông báo từ chối và cấu hình bypass. Không thử trên main.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.17 — Ensure branch deletions are denied

CIS: **Manual**, trang 50.

**Audit:** Đọc deletion rule; thử xóa nhánh disposable, không main.

**Remediation đề xuất:** Cấm xóa nhánh được bảo vệ.

**Re-audit:** Thử xóa đúng nhánh thử có rule chống xóa bằng tài khoản được phép kiểm thử; đối chiếu kết quả bị từ chối. Kết thúc thử nghiệm bằng quy trình thu hồi rule thử, không tác động nhánh khác.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.18 — Ensure any merging of code is automatically scanned for risks

CIS: **Manual**, trang 52.

**Audit:** Đối chiếu mọi PR merge với scanner và kết quả chạy.

**Remediation đề xuất:** Gắn scanner vào quy trình merge, yêu cầu check thành công.

**Re-audit:** Kiểm tra CI trên commit nhánh mới; sau đó thử PR có lỗi mẫu an toàn trên nhánh thử và xác nhận bị chặn.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.19 — Ensure any changes to branch protection rules are audited

CIS: **Manual**, trang 54.

**Audit:** Tìm sự kiện thay đổi protection/ruleset trong audit log và cơ chế cảnh báo.

**Remediation đề xuất:** Lưu audit log, phân công người nhận và kiểm tra cảnh báo.

**Re-audit:** Owner đổi một rule của nhánh thử, tìm đúng actor/time/action trong log rồi phục hồi cấu hình thử.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.20 — Ensure branch protection is enforced on the default branch

CIS: **Manual**, trang 56.

**Audit:** Lấy default branch qua API và đối chiếu effective protection.

**Remediation đề xuất:** Áp dụng protection cho đúng default branch.

**Re-audit:** Đọc default_branch hiện tại qua API và đối chiếu Rulesets/classic protection thực sự áp dụng ref đó; rà bypass và lưu cấu hình. Thử hành vi trên nhánh riêng có rule tương đương, ghi rõ giới hạn phạm vi.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.2.1 — Ensure all public repositories contain a SECURITY.md file

CIS: **Manual**, trang 59.

**Audit:** Đọc SECURITY.md và xác minh kênh báo cáo riêng tư.

**Remediation đề xuất:** Bổ sung policy và kênh tiếp nhận đã được chủ repo xác nhận.

**Re-audit:** Mở SECURITY.md trên từng repo public, kiểm tra phiên bản được hỗ trợ và kênh báo cáo riêng tư đang hoạt động; phân biệt chính sách kế thừa với file tại repo.

**Nguồn bằng chứng cần có:** repository_files.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.2.2 — Ensure repository creation is limited to specific members

CIS: **Manual**, trang 61.

**Audit:** Đọc quyền tạo repository ở cấp tổ chức.

**Remediation đề xuất:** Giới hạn tạo repository cho nhóm được phê duyệt.

**Re-audit:** Đối chiếu policy tạo repository với vai trò được duyệt; tài khoản ngoài danh sách thử tạo repo trong phạm vi được cho phép phải bị từ chối.

**Nguồn bằng chứng cần có:** repository, organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.2.3 — Ensure repository deletion is limited to specific users

CIS: **Manual**, trang 63.

**Audit:** Đọc quyền xóa repository và phân quyền quản trị.

**Remediation đề xuất:** Giới hạn quyền xóa; có quy trình phê duyệt và khôi phục.

**Re-audit:** Kiểm tra quyền xóa repo của từng vai trò và log thay đổi; nếu cần thử hành vi, chỉ dùng repo tạm đã được phê duyệt, không dùng finalrepo.

**Nguồn bằng chứng cần có:** repository, organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.2.4 — Ensure issue deletion is limited to specific users

CIS: **Manual**, trang 66.

**Audit:** Kiểm tra quyền xóa issue theo vai trò và audit log.

**Remediation đề xuất:** Giới hạn quyền xóa issue theo nhu cầu công việc.

**Re-audit:** Tạo issue thử không chứa dữ liệu quan trọng; kiểm tra vai trò không được phép không thể xóa, đối chiếu quyền và audit log của tài khoản thực hiện.

**Nguồn bằng chứng cần có:** repository, organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.2.5 — Ensure all copies (forks) of code are tracked and accounted for

CIS: **Manual**, trang 68.

**Audit:** Đối chiếu danh sách forks, visibility và người chịu trách nhiệm.

**Remediation đề xuất:** Kiểm kê forks định kỳ; xử lý bản sao không còn cần thiết.

**Re-audit:** So sánh số fork API với danh sách đã rà; lưu ngày và người duyệt.

**Nguồn bằng chứng cần có:** forks, organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.2.6 — Ensure all code projects are tracked for changes in visibility status

CIS: **Manual**, trang 70.

**Audit:** Đọc audit log visibility change và cấu hình theo dõi.

**Remediation đề xuất:** Cảnh báo/lưu vết thay đổi visibility, giới hạn người được đổi.

**Re-audit:** Đổi visibility của repo thử đã được phê duyệt; xác nhận inventory và audit log ghi được trạng thái trước/sau, actor và thời gian. Không đổi visibility finalrepo.

**Nguồn bằng chứng cần có:** repository, organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.2.7 — Ensure inactive repositories are reviewed and archived periodically

CIS: **Manual**, trang 72.

**Audit:** Lấy ngày cập nhật repo và biên bản đánh giá trạng thái.

**Remediation đề xuất:** Đặt lịch rà soát và archive sau khi chủ sở hữu xác nhận.

**Re-audit:** Kiểm tra trạng thái Archived của repo thử được phép và biên bản rà soát.

**Nguồn bằng chứng cần có:** repository, organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.1 — Ensure inactive users are reviewed and removed periodically

CIS: **Manual**, trang 75.

**Audit:** Đối chiếu thành viên, hoạt động gần nhất và nhu cầu truy cập.

**Remediation đề xuất:** Thu hồi thành viên không còn nhu cầu qua quy trình đã phê duyệt.

**Re-audit:** Người được thu hồi không còn truy cập repo riêng thử; lưu danh sách trước/sau đã che PII.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.2 — Ensure team creation is limited to specific members

CIS: **Manual**, trang 77.

**Audit:** Kiểm tra quyền tạo team của organization members.

**Remediation đề xuất:** Chỉ cho người được giao nhiệm vụ tạo team.

**Re-audit:** Kiểm tra policy tạo team và ngoại lệ owner; tài khoản thành viên thường thử tạo team trong môi trường thử phải tuân theo giới hạn đã duyệt.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.3 — Ensure minimum number of administrators are set for the organization

CIS: **Manual**, trang 79.

**Audit:** Kiểm kê organization owners/admins và lý do từng quyền.

**Remediation đề xuất:** Giảm admin tới mức cần thiết và bảo đảm phương án dự phòng.

**Re-audit:** Xuất bảng vai trò đã che PII và giải thích từng owner.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.4 — Ensure Multi-Factor Authentication (MFA) is required for contributors of new code

CIS: **Manual**, trang 81.

**Audit:** Kiểm tra MFA bắt buộc cho người đóng góp, kể cả ngoài tổ chức.

**Remediation đề xuất:** Bật và kiểm chứng chính sách MFA theo phạm vi người đóng góp.

**Re-audit:** Tài khoản không MFA không được cấp/giữ quyền đóng góp theo policy; lưu ảnh xác nhận không lộ recovery codes.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.5 — Ensure the organization is requiring members to use Multi- Factor Authentication (MFA)

CIS: **Manual**, trang 83.

**Audit:** Đọc yêu cầu MFA của tổ chức và trạng thái thực thi.

**Remediation đề xuất:** Bắt buộc MFA; chuẩn bị recovery trước khi áp dụng.

**Re-audit:** Owner đối chiếu yêu cầu MFA và toàn bộ phạm vi thành viên/ngoại lệ; kiểm tra tình huống tài khoản chưa bật MFA theo quy trình được phê duyệt, không công khai recovery codes.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.6 — Ensure new members are required to be invited using company-approved email

CIS: **Manual**, trang 85.

**Audit:** Đối chiếu email lời mời với domain được công ty chấp thuận.

**Remediation đề xuất:** Dùng danh sách domain/email được phép trong quy trình mời.

**Re-audit:** Đối chiếu invitation/audit log với email được duyệt, che địa chỉ trong báo cáo công khai.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.7 — Ensure two administrators are set for each repository

CIS: **Manual**, trang 87.

**Audit:** Kiểm kê repository admins và xác minh có hai quản trị viên phù hợp.

**Remediation đề xuất:** Bố trí hai quản trị viên độc lập theo yêu cầu, không chia sẻ tài khoản.

**Re-audit:** Hai người tự đăng nhập kiểm tra đúng quyền; tài khoản developer không có admin.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.8 — Ensure strict base permissions are set for repositories

CIS: **Manual**, trang 89.

**Audit:** Đọc default/base repository permission của tổ chức.

**Remediation đề xuất:** Chọn quyền nền tối thiểu và cấp thêm theo team.

**Re-audit:** Đọc base permission và toàn bộ quyền cấp thêm qua team/collaborator; dùng tài khoản thử không có grant bổ sung để xác nhận quyền truy cập hiệu lực.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.9 — Ensure an organization’s identity is confirmed with a “Verified” badge

CIS: **Manual**, trang 91.

**Audit:** Kiểm tra Verified badge và bằng chứng sở hữu domain.

**Remediation đề xuất:** Xác minh domain chính thức bằng quy trình GitHub.

**Re-audit:** Đối chiếu domain được xác minh bằng DNS với website/email Organization và huy hiệu Verified trên giao diện; chỉ ghi đạt khi bằng chứng cùng thuộc đúng Organization.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.10 — Ensure Source Code Management (SCM) email notifications are restricted to verified domains

CIS: **Manual**, trang 93.

**Audit:** Đọc giới hạn email notification tới verified domains.

**Remediation đề xuất:** Giới hạn thông báo tới domain tổ chức đã xác minh.

**Re-audit:** Trên gói hỗ trợ tính năng, đối chiếu domain thông báo với danh sách đã xác minh/phê duyệt và kiểm tra địa chỉ ngoài danh sách không nhận thông báo theo policy; thiếu tính năng ghi rõ giới hạn gói.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.11 — Ensure an organization provides SSH certificates

CIS: **Manual**, trang 95.

**Audit:** Kiểm tra SSH CA/certificate policy và vòng đời chứng chỉ.

**Remediation đề xuất:** Cấp SSH certificate qua CA được quản lý, có thu hồi và gia hạn.

**Re-audit:** Đối chiếu SSH CA được cài với CA được duyệt; thử certificate hợp lệ, hết hạn và certificate ký bởi CA khác trên đối tượng thử được phép, ghi kết quả truy cập.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.12 — Ensure Git access is limited based on IP addresses

CIS: **Manual**, trang 97.

**Audit:** Kiểm tra IP allow list và thử nguồn truy cập được phép/không được phép.

**Remediation đề xuất:** Thiết lập allow list theo mạng công việc, giữ đường khôi phục.

**Re-audit:** Thử truy cập Git có xác thực từ IP được phép và IP ngoài allow list; ghi địa chỉ nguồn đã che và kết quả. Không dùng truy cập public ẩn danh để kết luận hiệu lực IP policy.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.13 — Ensure anomalous code behavior is tracked

CIS: **Manual**, trang 99.

**Audit:** Đọc cơ chế phát hiện hành vi bất thường và mẫu cảnh báo.

**Remediation đề xuất:** Giám sát bất thường, có người nhận và quy trình xử lý.

**Re-audit:** Tạo sự kiện an toàn trên nhánh thử, xác nhận cảnh báo đến người trực và ghi xử lý.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.4.1 — Ensure administrator approval is required for every installed application

CIS: **Manual**, trang 101.

**Audit:** Liệt kê ứng dụng và quy trình owner approval.

**Remediation đề xuất:** Bắt buộc admin phê duyệt ứng dụng trước cấp quyền.

**Re-audit:** Thành viên thường yêu cầu cài app thử, owner phải phê duyệt trước khi app có quyền.

**Nguồn bằng chứng cần có:** organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.4.2 — Ensure stale applications are reviewed and inactive ones are removed

CIS: **Manual**, trang 103.

**Audit:** Đối chiếu app installation với hoạt động và chủ sở hữu.

**Remediation đề xuất:** Rà soát định kỳ, gỡ app không dùng sau xác nhận.

**Re-audit:** Đối chiếu sổ app trước/sau; xác nhận CI cần thiết vẫn hoạt động.

**Nguồn bằng chứng cần có:** organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.4.3 — Ensure the access granted to each installed application is limited to the least privilege needed

CIS: **Manual**, trang 105.

**Audit:** Đọc permissions và repository selection của từng app.

**Remediation đề xuất:** Thu hẹp app scopes và repository access theo least privilege.

**Re-audit:** Thử đọc repo không được cấp phải thất bại; repo được cấp vẫn hoạt động.

**Nguồn bằng chứng cần có:** organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.4.4 — Ensure only secured webhooks are used

CIS: **Manual**, trang 107.

**Audit:** Kiểm tra HTTPS và SSL verification của webhook mà không xuất secret.

**Remediation đề xuất:** Chuyển endpoint sang HTTPS hợp lệ và bật SSL verification.

**Re-audit:** Gửi delivery hợp lệ và payload sửa/chữ ký sai; endpoint phải từ chối trường hợp sai.

**Nguồn bằng chứng cần có:** webhooks.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.5.1 — Ensure scanners are in place to identify and prevent sensitive data in code

CIS: **Manual**, trang 110.

**Audit:** Kiểm tra secret scanner, mẫu phát hiện giả và cơ chế chặn.

**Remediation đề xuất:** Bật scanner/chặn theo chính sách; thu hồi secret thật trước xử lý lịch sử.

**Re-audit:** Dùng fixture secret giả trong thư mục/nhánh thử, xác nhận scanner phát hiện và gate thất bại; chạy lại trên source hiện tại và lịch sử theo hai phạm vi riêng, ghi các credential cần thu hồi.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.5.2 — Ensure scanners are in place to secure Continuous Integration (CI) pipeline instructions

CIS: **Manual**, trang 112.

**Audit:** Quét mọi workflow bằng công cụ kiểm tra cấu hình CI.

**Remediation đề xuất:** Sửa insecure instructions; giữ required security check.

**Re-audit:** Quét toàn bộ workflow và đối chiếu log scanner với commit được đánh giá; dùng cấu hình không an toàn trong fixture để xác nhận detection, không đưa workflow nguy hiểm vào nhánh đang vận hành.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.5.3 — Ensure scanners are in place to secure Infrastructure as Code (IaC) instructions

CIS: **Manual**, trang 114.

**Audit:** Kiểm kê IaC và xem report misconfiguration.

**Remediation đề xuất:** Quét mọi IaC được sử dụng và xử lý cấu hình mất an toàn.

**Re-audit:** Quét tập IaC đã kiểm kê, xác nhận scanner hỗ trợ đúng định dạng; thử fixture có misconfiguration và kiểm tra gate chặn. Nếu chưa có IaC thực tế, ghi thiếu phạm vi.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.5.4 — Ensure scanners are in place for code vulnerabilities

CIS: **Manual**, trang 116.

**Audit:** Kiểm tra code-scanning setup và report trên đúng commit.

**Remediation đề xuất:** Thiết lập SAST/code scanning phù hợp ngôn ngữ và xử lý findings.

**Re-audit:** Chạy SAST trên toàn bộ mã thuộc phạm vi, kiểm tra lỗi phân tích và ngưỡng severity; đối chiếu phát hiện với phiên bản công cụ và xác nhận mẫu lỗi kiểm thử được nhận diện.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.5.5 — Ensure scanners are in place for open-source vulnerabilities in used packages

CIS: **Manual**, trang 118.

**Audit:** Kiểm kê dependency, Dependabot và SCA report.

**Remediation đề xuất:** Bật giám sát dependency và xử lý phiên bản có CVE.

**Re-audit:** Đối chiếu danh sách dependency thực với báo cáo SCA theo tên/phiên bản; kiểm tra không có package bị bỏ qua và advisory vượt ngưỡng làm gate thất bại.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.5.6 — Ensure scanners are in place for open-source license issues in used packages

CIS: **Manual**, trang 120.

**Audit:** Đối chiếu package licenses với chính sách sử dụng.

**Remediation đề xuất:** Thiết lập license scanner và xử lý giấy phép không được phép.

**Re-audit:** So từng license expression với policy đã phê duyệt; các license thiếu/không rõ hoặc ngoài danh sách phải được review, ghi quyết định và người phê duyệt thay vì chỉ đếm scanner finding.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.
