# Nhóm 5: 11 quy trình Audit–Remediation–Re-audit

Đủ quy trình không đồng nghĩa đủ triển khai hoặc đạt tuân thủ. Hướng dẫn dưới đây diễn giải để áp dụng lab; đối chiếu Audit/Remediation gốc tại trang tham chiếu khi thực hiện. Không tự thay settings, cấp quyền, xóa tài nguyên hoặc tác động main.

## 5.1.1 — Ensure deployment configuration files are separated from source code

CIS: **Manual**, trang 219.

**Audit:** Kiểm vị trí quản lý config deploy và trust boundary với source.

**Remediation đề xuất:** Tách config theo kiến trúc/quyền phù hợp, không chỉ đổi thư mục.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** production, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 5.1.2 — Ensure changes in deployment configuration are audited

CIS: **Manual**, trang 220.

**Audit:** Lấy mẫu thay đổi deploy config và audit/review trail.

**Remediation đề xuất:** Version-control cấu hình và ghi review/approval.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** production, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 5.1.3 — Ensure scanners are in place to identify and prevent sensitive data in deployment configuration

CIS: **Manual**, trang 221.

**Audit:** Quét config deployment với secret scanner và fixture giả.

**Remediation đề xuất:** Ngăn secret plaintext, dùng secret manager và scanner.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** production, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 5.1.4 — Limit access to deployment configurations

CIS: **Manual**, trang 222.

**Audit:** Đọc quyền thay config deployment và danh sách approver.

**Remediation đề xuất:** Giới hạn quyền theo môi trường, review độc lập.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** production, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 5.1.5 — Scan Infrastructure as Code (IaC)

CIS: **Manual**, trang 224.

**Audit:** Kiểm kê deployment IaC và report misconfiguration.

**Remediation đề xuất:** Quét mọi IaC thực dùng và xử lý phát hiện.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** production, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 5.1.6 — Ensure deployment configuration manifests are verified

CIS: **Manual**, trang 225.

**Audit:** Kiểm chữ ký/hash deployment manifest trước áp dụng.

**Remediation đề xuất:** Xác minh manifest theo trust root trước sử dụng.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** production, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 5.1.7 — Ensure deployment configuration manifests are pinned to a specific, verified version

CIS: **Manual**, trang 226.

**Audit:** Đối chiếu deployment manifest với phiên bản/digest đã phê duyệt.

**Remediation đề xuất:** Pin manifest và dependency phiên bản được xác minh.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** production, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 5.2.1 — Ensure deployments are automated

CIS: **Manual**, trang 229.

**Audit:** Theo dõi pipeline triển khai và thao tác thủ công còn lại.

**Remediation đề xuất:** Mã hóa deployment và kiểm tra smoke/rollback.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** production, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 5.2.2 — Ensure the deployment environment is reproducible

CIS: **Manual**, trang 230.

**Audit:** Tái tạo môi trường từ input/config đã khóa và so cấu hình.

**Remediation đề xuất:** Khóa môi trường, tự động provisioning, kiểm chứng tái lập môi trường.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** production, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 5.2.3 — Ensure access to production environment is limited

CIS: **Manual**, trang 231.

**Audit:** Kiểm kê production identities, roles, network và break-glass.

**Remediation đề xuất:** Giới hạn quyền production và audit truy cập.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** production, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 5.2.4 — Ensure default passwords are not used

CIS: **Manual**, trang 232.

**Audit:** Kiểm tra cấu hình production không còn default password, không đăng nhập thử tùy tiện.

**Remediation đề xuất:** Thay default credentials, quản lý bí mật và vòng đời rotation.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** production, identity_provider.

**Người phụ trách:** TV4 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.
