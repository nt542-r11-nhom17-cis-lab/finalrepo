# Nhóm 4: 14 quy trình Audit–Remediation–Re-audit

Đủ quy trình không đồng nghĩa đủ triển khai hoặc đạt tuân thủ. Hướng dẫn dưới đây diễn giải để áp dụng lab; đối chiếu Audit/Remediation gốc tại trang tham chiếu khi thực hiện. Không tự thay settings, cấp quyền, xóa tài nguyên hoặc tác động main.

## 4.1.1 — Ensure all artifacts are signed by the build pipeline itself

CIS: **Manual**, trang 192.

**Audit:** Xác minh artifact do pipeline ký và gắn đúng commit.

**Remediation đề xuất:** Ký trong pipeline bằng danh tính quản lý được và kiểm chứng.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.1.2 — Ensure artifacts are encrypted before distribution

CIS: **Manual**, trang 195.

**Audit:** Kiểm plaintext/ciphertext ở đường phân phối và thử sửa ciphertext.

**Remediation đề xuất:** Mã hóa trước phân phối, xác thực integrity trước giải mã.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.1.3 — Ensure only authorized platforms have decryption capabilities of artifacts

CIS: **Manual**, trang 196.

**Audit:** Đối chiếu quyền giải mã, nơi giữ khóa và nền tảng được phép.

**Remediation đề xuất:** Giới hạn khóa giải mã cho nền tảng được ủy quyền.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.2.1 — Ensure the authority to certify artifacts is limited

CIS: **Manual**, trang 199.

**Audit:** Kiểm ai được ký/chứng nhận artifact và key policy.

**Remediation đề xuất:** Giới hạn signer, bảo vệ khóa và audit mọi lần dùng.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.2.2 — Ensure number of permitted users who may upload new artifacts is minimized

CIS: **Manual**, trang 200.

**Audit:** Kiểm registry uploader roles và nhu cầu công việc.

**Remediation đề xuất:** Giảm người được upload theo least privilege.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.2.3 — Ensure user access to the package registry utilizes Multi- Factor Authentication (MFA)

CIS: **Manual**, trang 201.

**Audit:** Kiểm MFA/SSO của người truy cập registry và ngoại lệ.

**Remediation đề xuất:** Bắt buộc MFA theo khả năng registry, quản lý recovery.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.2.4 — Ensure user management of the package registry is not local

CIS: **Manual**, trang 202.

**Audit:** Xác định registry identity provider và local accounts.

**Remediation đề xuất:** Dùng quản lý danh tính tập trung, giảm tài khoản local theo policy.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.2.5 — Ensure anonymous access to artifacts is revoked

CIS: **Manual**, trang 203.

**Audit:** Thử anonymous download của artifact cần bảo vệ.

**Remediation đề xuất:** Tắt anonymous access theo phạm vi và kiểm tra lại.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.2.6 — Ensure minimum number of administrators are set for the package registry

CIS: **Manual**, trang 205.

**Audit:** Kiểm kê registry admins và lý do cấp quyền.

**Remediation đề xuất:** Giảm admin và định kỳ review.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.3.1 — Ensure all signed artifacts are validated upon uploading the package registry

CIS: **Manual**, trang 208.

**Audit:** Thử upload artifact ký hợp lệ và artifact bị sửa vào registry lab.

**Remediation đề xuất:** Xác minh chữ ký trước chấp nhận upload, fail closed.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.3.2 — Ensure all versions of an existing artifact have their signatures validated

CIS: **Manual**, trang 210.

**Audit:** Kiểm mọi version và chữ ký, thử downgrade hoặc overwrite.

**Remediation đề xuất:** Xác minh mọi phiên bản và cấm overwrite không được phê duyệt.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.3.3 — Ensure changes in package registry configuration are audited

CIS: **Manual**, trang 212.

**Audit:** Đọc audit log thay đổi registry configuration.

**Remediation đề xuất:** Bật audit và cảnh báo thay đổi cấu hình.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.3.4 — Ensure webhooks of the repository are secured

CIS: **Manual**, trang 214.

**Audit:** Đọc webhook registry HTTPS/verification/auth metadata.

**Remediation đề xuất:** Bảo vệ webhook registry, kiểm tra certificate và nhận sự kiện.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 4.4.1 — Ensure artifacts contain information about their origin

CIS: **Manual**, trang 216.

**Audit:** Đọc provenance repo/commit/build/run và xác minh chữ ký.

**Remediation đề xuất:** Gắn thông tin nguồn gốc xác thực với digest artifact.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** registry, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.
