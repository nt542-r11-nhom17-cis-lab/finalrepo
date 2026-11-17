# Nhóm 4: 14 quy trình Audit–Remediation–Re-audit

Đủ quy trình không đồng nghĩa đủ triển khai hoặc đạt tuân thủ. Hướng dẫn dưới đây diễn giải để áp dụng lab; đối chiếu Audit/Remediation gốc tại trang tham chiếu khi thực hiện. Phạm vi đợt đánh giá không bao gồm thay đổi settings, quyền người dùng, xóa tài nguyên hoặc chỉnh sửa main. Khi kiểm tra lại, ghi đối tượng, ref, người thực hiện, thời gian và bằng chứng trước/sau; các phép thử gây thay đổi chỉ thực hiện trên đối tượng thử được phê duyệt.

## 4.1.1 — Ensure all artifacts are signed by the build pipeline itself

CIS: **Manual**, trang 192.

**Audit:** Xác minh artifact do pipeline ký và gắn đúng commit.

**Remediation đề xuất:** Ký trong pipeline bằng danh tính quản lý được và kiểm chứng.

**Re-audit:** Xác minh chữ ký artifact của đúng pipeline/run và quyền truy cập signer; thử artifact sửa và khóa sai bị từ chối. Ghi rõ signer lab nếu chưa có danh tính production.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.1.2 — Ensure artifacts are encrypted before distribution

CIS: **Manual**, trang 195.

**Audit:** Kiểm plaintext/ciphertext ở đường phân phối và thử sửa ciphertext.

**Remediation đề xuất:** Mã hóa trước phân phối, xác thực integrity trước giải mã.

**Re-audit:** Kiểm tra artifact được mã hóa trước khi chuyển khỏi pipeline và khóa không nằm trong gói; xác minh ciphertext trước giải mã, thử ciphertext bị sửa phải bị từ chối.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.1.3 — Ensure only authorized platforms have decryption capabilities of artifacts

CIS: **Manual**, trang 196.

**Audit:** Đối chiếu quyền giải mã, nơi giữ khóa và nền tảng được phép.

**Remediation đề xuất:** Giới hạn khóa giải mã cho nền tảng được ủy quyền.

**Re-audit:** Trên nền tảng được phép, kiểm tra giải mã thành công; nền tảng/tài khoản không có grant phải bị từ chối. Đối chiếu quyền secret manager và audit log, không chỉ dùng fixture offline.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.2.1 — Ensure the authority to certify artifacts is limited

CIS: **Manual**, trang 199.

**Audit:** Kiểm ai được ký/chứng nhận artifact và key policy.

**Remediation đề xuất:** Giới hạn signer, bảo vệ khóa và audit mọi lần dùng.

**Re-audit:** Đối chiếu danh sách signer/certifier với policy và quyền KMS/CA; tài khoản không được cấp thử ký hoặc cấp chứng nhận phải bị từ chối.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.2.2 — Ensure number of permitted users who may upload new artifacts is minimized

CIS: **Manual**, trang 200.

**Audit:** Kiểm registry uploader roles và nhu cầu công việc.

**Remediation đề xuất:** Giảm người được upload theo least privilege.

**Re-audit:** Rà toàn bộ quyền upload theo user/team/service account; dùng tài khoản Read thử upload bị từ chối và tài khoản publisher đúng phạm vi được chấp nhận.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.2.3 — Ensure user access to the package registry utilizes Multi- Factor Authentication (MFA)

CIS: **Manual**, trang 201.

**Audit:** Kiểm MFA/SSO của người truy cập registry và ngoại lệ.

**Remediation đề xuất:** Bắt buộc MFA theo khả năng registry, quản lý recovery.

**Re-audit:** Kiểm tra policy MFA của registry thật và danh tính được áp dụng; tài khoản chưa đáp ứng MFA không được thao tác theo phạm vi policy, ghi ngoại lệ cho service account.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.2.4 — Ensure user management of the package registry is not local

CIS: **Manual**, trang 202.

**Audit:** Xác định registry identity provider và local accounts.

**Remediation đề xuất:** Dùng quản lý danh tính tập trung, giảm tài khoản local theo policy.

**Re-audit:** Đối chiếu người dùng registry với IdP/SSO bên ngoài và đường đăng nhập local; vô hiệu user thử tại IdP theo quy trình được duyệt, kiểm tra registry thu hồi quyền tương ứng.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.2.5 — Ensure anonymous access to artifacts is revoked

CIS: **Manual**, trang 203.

**Audit:** Thử anonymous download của artifact cần bảo vệ.

**Remediation đề xuất:** Tắt anonymous access theo phạm vi và kiểm tra lại.

**Re-audit:** Thử tải artifact từ registry thật khi không đăng nhập và bằng tài khoản không có grant; đối chiếu HTTP/ACL. Không dùng registry giả lập hoặc repo public để kết luận.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.2.6 — Ensure minimum number of administrators are set for the package registry

CIS: **Manual**, trang 205.

**Audit:** Kiểm kê registry admins và lý do cấp quyền.

**Remediation đề xuất:** Giảm admin và định kỳ review.

**Re-audit:** Xuất danh sách admin hiệu lực của registry, đối chiếu nhu cầu công việc và ngoại lệ; tài khoản thường không được đổi cấu hình/quyền quản trị.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.3.1 — Ensure all signed artifacts are validated upon uploading the package registry

CIS: **Manual**, trang 208.

**Audit:** Thử upload artifact ký hợp lệ và artifact bị sửa vào registry lab.

**Remediation đề xuất:** Xác minh chữ ký trước chấp nhận upload, fail closed.

**Re-audit:** Upload artifact ký hợp lệ và bản sao sai/thiếu chữ ký tới registry thử; registry phải từ chối bản không hợp lệ trước khi artifact được phân phối.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.3.2 — Ensure all versions of an existing artifact have their signatures validated

CIS: **Manual**, trang 210.

**Audit:** Kiểm mọi version và chữ ký, thử downgrade hoặc overwrite.

**Remediation đề xuất:** Xác minh mọi phiên bản và cấm overwrite không được phê duyệt.

**Re-audit:** Liệt kê mọi phiên bản artifact trong phạm vi, xác minh từng chữ ký với trust policy tương ứng; ghi phiên bản thiếu chữ ký hoặc không thể xác minh.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.3.3 — Ensure changes in package registry configuration are audited

CIS: **Manual**, trang 212.

**Audit:** Đọc audit log thay đổi registry configuration.

**Remediation đề xuất:** Bật audit và cảnh báo thay đổi cấu hình.

**Re-audit:** Thay đổi cấu hình vô hại trên registry thử đã được duyệt; kiểm tra log lưu actor, thời gian và cấu hình trước/sau, kiểm tra quyền sửa/xóa log.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.3.4 — Ensure webhooks of the repository are secured

CIS: **Manual**, trang 214.

**Audit:** Đọc webhook registry HTTPS/verification/auth metadata.

**Remediation đề xuất:** Bảo vệ webhook registry, kiểm tra certificate và nhận sự kiện.

**Re-audit:** Gửi webhook thử hợp lệ, sai chữ ký và replay tới endpoint registry được phép; kiểm tra TLS, HMAC và event allowlist, bảo đảm request sai bị từ chối.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.4.1 — Ensure artifacts contain information about their origin

CIS: **Manual**, trang 216.

**Audit:** Đọc provenance repo/commit/build/run và xác minh chữ ký.

**Remediation đề xuất:** Gắn thông tin nguồn gốc xác thực với digest artifact.

**Re-audit:** Đối chiếu metadata nguồn gốc với commit, run ID, builder và digest artifact; xác minh chữ ký metadata và kiểm tra sửa commit/digest làm xác minh thất bại.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.
