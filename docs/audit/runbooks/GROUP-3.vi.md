# Nhóm 3: 12 quy trình Audit–Remediation–Re-audit

Đủ quy trình không đồng nghĩa đủ triển khai hoặc đạt tuân thủ. Hướng dẫn dưới đây diễn giải để áp dụng lab; đối chiếu Audit/Remediation gốc tại trang tham chiếu khi thực hiện. Không tự thay settings, cấp quyền, xóa tài nguyên hoặc tác động main.

## 3.1.1 — Ensure third-party artifacts and open-source libraries are verified

CIS: **Manual**, trang 169.

**Audit:** Đối chiếu third-party package với checksum/chữ ký/nguồn tin cậy.

**Remediation đề xuất:** Chỉ nhận package đã xác minh, ghi lại trust root.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** supplier, organization_policy.

**Người phụ trách:** TV3 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 3.1.2 — Ensure Software Bill of Materials (SBOM) is required from all third-party suppliers

CIS: **Manual**, trang 171.

**Audit:** Kiểm kê nhà cung cấp và SBOM cho từng thành phần.

**Remediation đề xuất:** Yêu cầu supplier SBOM trong quy trình tiếp nhận.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** supplier, organization_policy.

**Người phụ trách:** TV3 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 3.1.3 — Ensure signed metadata of the build process is required and verified

CIS: **Manual**, trang 173.

**Audit:** Kiểm signed build metadata và đối chiếu artifact digest.

**Remediation đề xuất:** Yêu cầu provenance ký, xác minh signer và nội dung.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** supplier, organization_policy.

**Người phụ trách:** TV3 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 3.1.4 — Ensure dependencies are monitored between open-source components

CIS: **Manual**, trang 175.

**Audit:** Đọc dependency graph và thay đổi quan hệ/transitive dependencies.

**Remediation đề xuất:** Theo dõi graph, cập nhật và xử lý thay đổi bất thường.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** supplier, organization_policy.

**Người phụ trách:** TV3 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 3.1.5 — Ensure trusted package managers and repositories are defined and prioritized

CIS: **Manual**, trang 176.

**Audit:** Đọc cấu hình package manager, registry precedence và namespace.

**Remediation đề xuất:** Chỉ cho nguồn tin cậy, ưu tiên đúng registry để giảm dependency confusion.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** supplier, organization_policy.

**Người phụ trách:** TV3 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 3.1.6 — Ensure a signed Software Bill of Materials (SBOM) of the code is supplied

CIS: **Manual**, trang 178.

**Audit:** Kiểm SBOM của mã giao cho bên nhận và chữ ký.

**Remediation đề xuất:** Cung cấp signed SBOM gắn với phiên bản artifact.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** supplier, organization_policy.

**Người phụ trách:** TV3 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 3.1.7 — Ensure dependencies are pinned to a specific, verified version

CIS: **Manual**, trang 180.

**Audit:** Kiểm mọi dependency pinned và bằng chứng verified version.

**Remediation đề xuất:** Pin phiên bản/hash đã được xác minh qua review.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** supplier, organization_policy.

**Người phụ trách:** TV3 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 3.1.8 — Ensure all packages used are more than 60 days old

CIS: **Manual**, trang 182.

**Audit:** Tính tuổi phiên bản từ ngày phát hành tin cậy tới ngày kiểm tra.

**Remediation đề xuất:** Chọn phiên bản hơn 60 ngày theo yêu cầu, xử lý ngoại lệ theo chính sách.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** supplier, organization_policy.

**Người phụ trách:** TV3 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 3.2.1 — Ensure an organization-wide dependency usage policy is enforced

CIS: **Manual**, trang 185.

**Audit:** Đối chiếu chính sách dependency đã phê duyệt với enforcement.

**Remediation đề xuất:** Áp dụng policy toàn tổ chức và quản lý ngoại lệ có hạn.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** supplier, organization_policy.

**Người phụ trách:** TV3 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 3.2.2 — Ensure packages are automatically scanned for known vulnerabilities

CIS: **Manual**, trang 186.

**Audit:** Kiểm lịch SCA scan và freshness của vulnerability database.

**Remediation đề xuất:** Quét CVE tự động định kỳ và trước phát hành.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** supplier, organization_policy.

**Người phụ trách:** TV3 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 3.2.3 — Ensure packages are automatically scanned for license implications

CIS: **Manual**, trang 187.

**Audit:** Đọc license inventory, policy và mẫu vi phạm.

**Remediation đề xuất:** Quét license tự động và buộc xử lý vi phạm.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** supplier, organization_policy.

**Người phụ trách:** TV3 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 3.2.4 — Ensure packages are automatically scanned for ownership change

CIS: **Manual**, trang 189.

**Audit:** Đối chiếu package owner hiện tại với baseline đáng tin.

**Remediation đề xuất:** Giám sát ownership change, cảnh báo và review trước dùng bản mới.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** supplier, organization_policy.

**Người phụ trách:** TV3 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.
