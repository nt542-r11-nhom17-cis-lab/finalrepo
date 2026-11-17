# Nhóm 1: 50 quy trình Audit–Remediation–Re-audit

Đủ quy trình không đồng nghĩa đủ triển khai hoặc đạt tuân thủ. Hướng dẫn dưới đây diễn giải để áp dụng lab; đối chiếu Audit/Remediation gốc tại trang tham chiếu khi thực hiện. Không tự thay settings, cấp quyền, xóa tài nguyên hoặc tác động main.

## 1.1.1 — Ensure any changes to code are tracked in a version control platform

CIS: **Manual**, trang 19.

**Audit:** Đối chiếu nguồn đang chạy với lịch sử Git và commit của mọi thay đổi.

**Remediation đề xuất:** Đưa nguồn chưa quản lý vào VCS; bắt buộc thay đổi qua quy trình review.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, branches, pull_requests.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.2 — Ensure any change to code can be traced back to its associated task

CIS: **Manual**, trang 20.

**Audit:** Lấy mẫu commit/PR và truy về issue hoặc task được giao.

**Remediation đề xuất:** Yêu cầu mã task và liên kết issue trong mẫu PR, kiểm tra thủ công tính đúng của liên kết.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, branches, pull_requests.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.3 — Ensure any change to code receives approval of two strongly authenticated users

CIS: **Automated**, trang 22.

**Audit:** Đọc required approvals và kiểm thử PR thiếu hai reviewer độc lập; xác minh strong authentication.

**Remediation đề xuất:** Yêu cầu hai phê duyệt theo Audit và chính sách xác thực mạnh; xem xét bypass.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.4 — Ensure previous approvals are dismissed when updates are introduced to a code change proposal

CIS: **Manual**, trang 24.

**Audit:** Đọc dismiss-stale; đẩy commit thay đổi vào PR đã được duyệt.

**Remediation đề xuất:** Bật hủy phê duyệt cũ và kiểm tra yêu cầu review lại.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.5 — Ensure there are restrictions on who can dismiss code change reviews

CIS: **Manual**, trang 26.

**Audit:** Kiểm tra danh sách người/nhóm được dismiss review và bypass.

**Remediation đề xuất:** Giới hạn dismiss cho tài khoản tin cậy đã được phê duyệt.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.6 — Ensure code owners are set for extra sensitive code or configuration

CIS: **Manual**, trang 28.

**Audit:** Tìm CODEOWNERS, so đường dẫn nhạy cảm và quyền owner.

**Remediation đề xuất:** Khai báo owner có quyền phù hợp cho mã/cấu hình nhạy cảm.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.7 — Ensure code owner's review is required when a change affects owned code

CIS: **Manual**, trang 30.

**Audit:** Đọc required code-owner review và thử PR sửa file có owner.

**Remediation đề xuất:** Bắt buộc code-owner review trên quy tắc có hiệu lực.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.8 — Ensure inactive branches are periodically reviewed and removed

CIS: **Manual**, trang 32.

**Audit:** Liệt kê nhánh, ngày commit cuối, chủ sở hữu và biên bản rà soát.

**Remediation đề xuất:** Đặt lịch rà soát; chỉ xóa nhánh sau khi xác nhận không còn sử dụng.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, branches, pull_requests.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.9 — Ensure all checks have passed before merging new code

CIS: **Manual**, trang 34.

**Audit:** Đọc required checks; thử PR có check thất bại.

**Remediation đề xuất:** Bắt buộc checks phù hợp và kiểm soát bypass trước merge.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.10 — Ensure open Git branches are up to date before they can be merged into code base

CIS: **Manual**, trang 36.

**Audit:** Kiểm tra strict/up-to-date requirement và PR tụt sau base.

**Remediation đề xuất:** Bật yêu cầu nhánh cập nhật trước merge hoặc cơ chế tương đương.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.11 — Ensure all open comments are resolved before allowing code change merging

CIS: **Manual**, trang 38.

**Audit:** Kiểm tra conversation resolution và PR còn comment chưa giải quyết.

**Remediation đề xuất:** Bắt buộc giải quyết hội thoại trước merge.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.12 — Ensure verification of signed commits for new changes before merging

CIS: **Manual**, trang 40.

**Audit:** Kiểm tra required signatures và commit verification.

**Remediation đề xuất:** Bắt buộc commit ký được nền tảng xác minh; quản lý khóa người ký.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.13 — Ensure linear history is required

CIS: **Manual**, trang 42.

**Audit:** Đọc linear-history rule và lịch sử merge.

**Remediation đề xuất:** Bật linear history và chọn cách merge phù hợp.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.14 — Ensure branch protection rules are enforced for administrators

CIS: **Manual**, trang 44.

**Audit:** Xem enforce-admins và các bypass actor.

**Remediation đề xuất:** Áp dụng bảo vệ cho admin; giảm ngoại lệ theo chính sách.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.15 — Ensure pushing or merging of new code is restricted to specific individuals or teams

CIS: **Manual**, trang 46.

**Audit:** Đọc push restrictions và danh sách team/user.

**Remediation đề xuất:** Chỉ cho người/nhóm được phê duyệt push hoặc merge.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.16 — Ensure force push code to branches is denied

CIS: **Manual**, trang 48.

**Audit:** Đọc force-push rule; thử trên nhánh disposable được bảo vệ.

**Remediation đề xuất:** Cấm force push và xem lại bypass.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.17 — Ensure branch deletions are denied

CIS: **Manual**, trang 50.

**Audit:** Đọc deletion rule; thử xóa nhánh disposable, không main.

**Remediation đề xuất:** Cấm xóa nhánh được bảo vệ.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.18 — Ensure any merging of code is automatically scanned for risks

CIS: **Manual**, trang 52.

**Audit:** Đối chiếu mọi PR merge với scanner và kết quả chạy.

**Remediation đề xuất:** Gắn scanner vào quy trình merge, yêu cầu check thành công.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.19 — Ensure any changes to branch protection rules are audited

CIS: **Manual**, trang 54.

**Audit:** Tìm sự kiện thay đổi protection/ruleset trong audit log và cơ chế cảnh báo.

**Remediation đề xuất:** Lưu audit log, phân công người nhận và kiểm tra cảnh báo.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.1.20 — Ensure branch protection is enforced on the default branch

CIS: **Manual**, trang 56.

**Audit:** Lấy default branch qua API và đối chiếu effective protection.

**Remediation đề xuất:** Áp dụng protection cho đúng default branch.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, branches, pull_requests, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.2.1 — Ensure all public repositories contain a SECURITY.md file

CIS: **Manual**, trang 59.

**Audit:** Đọc SECURITY.md và xác minh kênh báo cáo riêng tư.

**Remediation đề xuất:** Bổ sung policy và kênh tiếp nhận đã được chủ repo xác nhận.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.2.2 — Ensure repository creation is limited to specific members

CIS: **Manual**, trang 61.

**Audit:** Đọc quyền tạo repository ở cấp tổ chức.

**Remediation đề xuất:** Giới hạn tạo repository cho nhóm được phê duyệt.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.2.3 — Ensure repository deletion is limited to specific users

CIS: **Manual**, trang 63.

**Audit:** Đọc quyền xóa repository và phân quyền quản trị.

**Remediation đề xuất:** Giới hạn quyền xóa; có quy trình phê duyệt và khôi phục.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.2.4 — Ensure issue deletion is limited to specific users

CIS: **Manual**, trang 66.

**Audit:** Kiểm tra quyền xóa issue theo vai trò và audit log.

**Remediation đề xuất:** Giới hạn quyền xóa issue theo nhu cầu công việc.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.2.5 — Ensure all copies (forks) of code are tracked and accounted for

CIS: **Manual**, trang 68.

**Audit:** Đối chiếu danh sách forks, visibility và người chịu trách nhiệm.

**Remediation đề xuất:** Kiểm kê forks định kỳ; xử lý bản sao không còn cần thiết.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** forks, organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.2.6 — Ensure all code projects are tracked for changes in visibility status

CIS: **Manual**, trang 70.

**Audit:** Đọc audit log visibility change và cấu hình theo dõi.

**Remediation đề xuất:** Cảnh báo/lưu vết thay đổi visibility, giới hạn người được đổi.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.2.7 — Ensure inactive repositories are reviewed and archived periodically

CIS: **Manual**, trang 72.

**Audit:** Lấy ngày cập nhật repo và biên bản đánh giá trạng thái.

**Remediation đề xuất:** Đặt lịch rà soát và archive sau khi chủ sở hữu xác nhận.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository, organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.1 — Ensure inactive users are reviewed and removed periodically

CIS: **Manual**, trang 75.

**Audit:** Đối chiếu thành viên, hoạt động gần nhất và nhu cầu truy cập.

**Remediation đề xuất:** Thu hồi thành viên không còn nhu cầu qua quy trình đã phê duyệt.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.2 — Ensure team creation is limited to specific members

CIS: **Manual**, trang 77.

**Audit:** Kiểm tra quyền tạo team của organization members.

**Remediation đề xuất:** Chỉ cho người được giao nhiệm vụ tạo team.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.3 — Ensure minimum number of administrators are set for the organization

CIS: **Manual**, trang 79.

**Audit:** Kiểm kê organization owners/admins và lý do từng quyền.

**Remediation đề xuất:** Giảm admin tới mức cần thiết và bảo đảm phương án dự phòng.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.4 — Ensure Multi-Factor Authentication (MFA) is required for contributors of new code

CIS: **Manual**, trang 81.

**Audit:** Kiểm tra MFA bắt buộc cho người đóng góp, kể cả ngoài tổ chức.

**Remediation đề xuất:** Bật và kiểm chứng chính sách MFA theo phạm vi người đóng góp.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.5 — Ensure the organization is requiring members to use Multi- Factor Authentication (MFA)

CIS: **Manual**, trang 83.

**Audit:** Đọc yêu cầu MFA của tổ chức và trạng thái thực thi.

**Remediation đề xuất:** Bắt buộc MFA; chuẩn bị recovery trước khi áp dụng.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.6 — Ensure new members are required to be invited using company-approved email

CIS: **Manual**, trang 85.

**Audit:** Đối chiếu email lời mời với domain được công ty chấp thuận.

**Remediation đề xuất:** Dùng danh sách domain/email được phép trong quy trình mời.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.7 — Ensure two administrators are set for each repository

CIS: **Manual**, trang 87.

**Audit:** Kiểm kê repository admins và xác minh có hai quản trị viên phù hợp.

**Remediation đề xuất:** Bố trí hai quản trị viên độc lập theo yêu cầu, không chia sẻ tài khoản.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.8 — Ensure strict base permissions are set for repositories

CIS: **Manual**, trang 89.

**Audit:** Đọc default/base repository permission của tổ chức.

**Remediation đề xuất:** Chọn quyền nền tối thiểu và cấp thêm theo team.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.9 — Ensure an organization’s identity is confirmed with a “Verified” badge

CIS: **Manual**, trang 91.

**Audit:** Kiểm tra Verified badge và bằng chứng sở hữu domain.

**Remediation đề xuất:** Xác minh domain chính thức bằng quy trình GitHub.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.10 — Ensure Source Code Management (SCM) email notifications are restricted to verified domains

CIS: **Manual**, trang 93.

**Audit:** Đọc giới hạn email notification tới verified domains.

**Remediation đề xuất:** Giới hạn thông báo tới domain tổ chức đã xác minh.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.11 — Ensure an organization provides SSH certificates

CIS: **Manual**, trang 95.

**Audit:** Kiểm tra SSH CA/certificate policy và vòng đời chứng chỉ.

**Remediation đề xuất:** Cấp SSH certificate qua CA được quản lý, có thu hồi và gia hạn.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.12 — Ensure Git access is limited based on IP addresses

CIS: **Manual**, trang 97.

**Audit:** Kiểm tra IP allow list và thử nguồn truy cập được phép/không được phép.

**Remediation đề xuất:** Thiết lập allow list theo mạng công việc, giữ đường khôi phục.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.3.13 — Ensure anomalous code behavior is tracked

CIS: **Manual**, trang 99.

**Audit:** Đọc cơ chế phát hiện hành vi bất thường và mẫu cảnh báo.

**Remediation đề xuất:** Giám sát bất thường, có người nhận và quy trình xử lý.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** collaborators, organization_policy, identity_provider.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.4.1 — Ensure administrator approval is required for every installed application

CIS: **Manual**, trang 101.

**Audit:** Liệt kê ứng dụng và quy trình owner approval.

**Remediation đề xuất:** Bắt buộc admin phê duyệt ứng dụng trước cấp quyền.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.4.2 — Ensure stale applications are reviewed and inactive ones are removed

CIS: **Manual**, trang 103.

**Audit:** Đối chiếu app installation với hoạt động và chủ sở hữu.

**Remediation đề xuất:** Rà soát định kỳ, gỡ app không dùng sau xác nhận.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.4.3 — Ensure the access granted to each installed application is limited to the least privilege needed

CIS: **Manual**, trang 105.

**Audit:** Đọc permissions và repository selection của từng app.

**Remediation đề xuất:** Thu hẹp app scopes và repository access theo least privilege.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** organization_policy.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.4.4 — Ensure only secured webhooks are used

CIS: **Manual**, trang 107.

**Audit:** Kiểm tra HTTPS và SSL verification của webhook mà không xuất secret.

**Remediation đề xuất:** Chuyển endpoint sang HTTPS hợp lệ và bật SSL verification.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** webhooks.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.5.1 — Ensure scanners are in place to identify and prevent sensitive data in code

CIS: **Manual**, trang 110.

**Audit:** Kiểm tra secret scanner, mẫu phát hiện giả và cơ chế chặn.

**Remediation đề xuất:** Bật scanner/chặn theo chính sách; thu hồi secret thật trước xử lý lịch sử.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.5.2 — Ensure scanners are in place to secure Continuous Integration (CI) pipeline instructions

CIS: **Manual**, trang 112.

**Audit:** Quét mọi workflow bằng công cụ kiểm tra cấu hình CI.

**Remediation đề xuất:** Sửa insecure instructions; giữ required security check.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.5.3 — Ensure scanners are in place to secure Infrastructure as Code (IaC) instructions

CIS: **Manual**, trang 114.

**Audit:** Kiểm kê IaC và xem report misconfiguration.

**Remediation đề xuất:** Quét mọi IaC được sử dụng và xử lý cấu hình mất an toàn.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.5.4 — Ensure scanners are in place for code vulnerabilities

CIS: **Manual**, trang 116.

**Audit:** Kiểm tra code-scanning setup và report trên đúng commit.

**Remediation đề xuất:** Thiết lập SAST/code scanning phù hợp ngôn ngữ và xử lý findings.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.5.5 — Ensure scanners are in place for open-source vulnerabilities in used packages

CIS: **Manual**, trang 118.

**Audit:** Kiểm kê dependency, Dependabot và SCA report.

**Remediation đề xuất:** Bật giám sát dependency và xử lý phiên bản có CVE.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 1.5.6 — Ensure scanners are in place for open-source license issues in used packages

CIS: **Manual**, trang 120.

**Audit:** Đối chiếu package licenses với chính sách sử dụng.

**Remediation đề xuất:** Thiết lập license scanner và xử lý giấy phép không được phép.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV1 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.
