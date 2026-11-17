# Nhóm 2: 33 quy trình Audit–Remediation–Re-audit

Đủ quy trình không đồng nghĩa đủ triển khai hoặc đạt tuân thủ. Hướng dẫn dưới đây diễn giải để áp dụng lab; đối chiếu Audit/Remediation gốc tại trang tham chiếu khi thực hiện. Không tự thay settings, cấp quyền, xóa tài nguyên hoặc tác động main.

## 2.1.1 — Ensure each pipeline has a single responsibility

CIS: **Manual**, trang 123.

**Audit:** Kiểm tra trách nhiệm và quyền của từng pipeline.

**Remediation đề xuất:** Tách pipeline theo mục đích và giảm quyền mỗi pipeline.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.2 — Ensure all aspects of the pipeline infrastructure and configuration are immutable

CIS: **Manual**, trang 125.

**Audit:** Đối chiếu image/infrastructure/config với phiên bản và cơ chế sửa trực tiếp.

**Remediation đề xuất:** Mã hóa cấu hình, pin image và tái tạo thay vì sửa thủ công.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.3 — Ensure the build environment is logged

CIS: **Manual**, trang 127.

**Audit:** Kiểm tra log môi trường build và chính sách giữ log.

**Remediation đề xuất:** Ghi image version, tool versions và cấu hình cần thiết, che secrets.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.4 — Ensure the creation of the build environment is automated

CIS: **Manual**, trang 128.

**Audit:** Tạo lại môi trường build từ mã trong môi trường sạch.

**Remediation đề xuất:** Tự động hóa provisioning và ghi cấu hình trong VCS.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.5 — Ensure access to build environments is limited

CIS: **Manual**, trang 129.

**Audit:** Liệt kê người/app có quyền vào môi trường build.

**Remediation đề xuất:** Giảm quyền theo vai trò, rà soát định kỳ.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.6 — Ensure users must authenticate to access the build environment

CIS: **Manual**, trang 131.

**Audit:** Thử truy cập chưa xác thực trong môi trường kiểm thử.

**Remediation đề xuất:** Bắt buộc xác thực cho mọi đường quản trị build.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.7 — Ensure build secrets are limited to the minimal necessary scope

CIS: **Manual**, trang 132.

**Audit:** Đọc metadata phạm vi secrets mà không đọc giá trị.

**Remediation đề xuất:** Giới hạn secrets theo repo/environment/job, ưu tiên credentials ngắn hạn.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.8 — Ensure the build infrastructure is automatically scanned for vulnerabilities

CIS: **Manual**, trang 134.

**Audit:** Xem scan của hạ tầng build, phạm vi và chu kỳ cập nhật.

**Remediation đề xuất:** Quét hạ tầng phù hợp và theo dõi xử lý lỗ hổng.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.9 — Ensure default passwords are not used

CIS: **Manual**, trang 135.

**Audit:** Đối chiếu cấu hình dịch vụ với danh sách default credentials, không brute-force.

**Remediation đề xuất:** Loại mật khẩu mặc định và quản lý secrets đúng quy trình.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.10 — Ensure webhooks of the build environment are secured

CIS: **Manual**, trang 136.

**Audit:** Đọc cấu hình webhook build: HTTPS, certificate verification, auth.

**Remediation đề xuất:** Bảo vệ webhook build và kiểm tra lại endpoint.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.11 — Ensure minimum number of administrators are set for the build environment

CIS: **Manual**, trang 137.

**Audit:** Kiểm kê admin của build system và lý do cấp quyền.

**Remediation đề xuất:** Giảm admin tới mức tối thiểu cần thiết.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.1 — Ensure build workers are single-used

CIS: **Manual**, trang 139.

**Audit:** Kiểm tra runner lifecycle, reuse và dữ liệu tồn dư giữa job.

**Remediation đề xuất:** Dùng runner dùng một lần hoặc tái tạo và làm sạch được kiểm chứng.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.2 — Ensure build worker environments and commands are passed and not pulled

CIS: **Manual**, trang 140.

**Audit:** Kiểm tra nguồn lệnh/config được cung cấp cho worker.

**Remediation đề xuất:** Truyền lệnh/config từ controller tin cậy, tránh worker kéo lệnh tùy ý.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.3 — Ensure the duties of each build worker are segregated

CIS: **Manual**, trang 141.

**Audit:** Đối chiếu nhiệm vụ/credentials giữa các worker.

**Remediation đề xuất:** Tách worker theo nhiệm vụ và trust boundary.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.4 — Ensure build workers have minimal network connectivity

CIS: **Manual**, trang 142.

**Audit:** Kiểm tra egress policy và thử endpoint allowed/denied.

**Remediation đề xuất:** Giới hạn mạng tối thiểu, không nới rule để làm xanh test.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.5 — Ensure run-time security is enforced for build workers

CIS: **Manual**, trang 144.

**Audit:** Kiểm tra runtime security agent/policy và sự kiện thử nghiệm.

**Remediation đề xuất:** Áp dụng runtime protection và giám sát phản hồi.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.6 — Ensure build workers are automatically scanned for vulnerabilities

CIS: **Manual**, trang 145.

**Audit:** Quét package của worker đúng image/version.

**Remediation đề xuất:** Quét định kỳ và xử lý CVE theo ngưỡng đã thống nhất.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.7 — Ensure build workers' deployment configuration is stored in a version control platform

CIS: **Manual**, trang 146.

**Audit:** Đối chiếu cấu hình triển khai worker với Git commit.

**Remediation đề xuất:** Lưu cấu hình worker trong VCS và review thay đổi.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.8 — Ensure resource consumption of build workers is monitored

CIS: **Manual**, trang 148.

**Audit:** Theo dõi CPU/RAM/disk trong tải thực tế và cảnh báo.

**Remediation đề xuất:** Thiết lập monitoring và kiểm tra đường cảnh báo.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.1 — Ensure all build steps are defined as code

CIS: **Manual**, trang 150.

**Audit:** So toàn bộ bước build với YAML/script đang version-control.

**Remediation đề xuất:** Đưa các bước build vào mã và loại bước không truy vết.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.2 — Ensure steps have clearly defined build stage input and output

CIS: **Manual**, trang 151.

**Audit:** Kiểm tra contract input/output từng stage.

**Remediation đề xuất:** Khai báo, kiểm tra schema/hash và fail khi output không hợp lệ.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.3 — Ensure output is written to a separate, secured storage repository

CIS: **Manual**, trang 152.

**Audit:** Xác định kho output, quyền truy cập và tách biệt nguồn.

**Remediation đề xuất:** Lưu output vào kho riêng được bảo vệ và kiểm soát quyền.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.4 — Ensure changes to pipeline files are tracked and reviewed

CIS: **Manual**, trang 153.

**Audit:** Lấy mẫu thay đổi workflow và review tương ứng.

**Remediation đề xuất:** Bắt buộc review pipeline file, ghi lịch sử và code owner.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.5 — Ensure access to build process triggering is minimized

CIS: **Manual**, trang 154.

**Audit:** Kiểm kê ai có thể dispatch/rerun/trigger qua token hoặc event.

**Remediation đề xuất:** Giới hạn trigger, runner và quyền token theo nhu cầu.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.6 — Ensure pipelines are automatically scanned for misconfigurations

CIS: **Manual**, trang 155.

**Audit:** Quét misconfiguration toàn bộ pipeline files.

**Remediation đề xuất:** Bổ sung scanner và sửa cấu hình không an toàn.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.7 — Ensure pipelines are automatically scanned for vulnerabilities

CIS: **Manual**, trang 156.

**Audit:** Kiểm tra vulnerability scanner cho pipeline và tools được dùng.

**Remediation đề xuất:** Quét thành phần pipeline và xử lý lỗ hổng.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.8 — Ensure scanners are in place to identify and prevent sensitive data in pipeline files

CIS: **Automated**, trang 157.

**Audit:** Đưa dữ liệu giả vào pipeline fixture và xác minh secret scanner phát hiện.

**Remediation đề xuất:** Quét mọi pipeline, chặn theo chính sách và không dùng secret thật để thử.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.4.1 — Ensure all artifacts on all releases are signed

CIS: **Manual**, trang 159.

**Audit:** Kiểm kê mọi release và mọi artifact có chữ ký hợp lệ.

**Remediation đề xuất:** Ký tất cả release artifacts và xác minh trước phân phối.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** sandbox, supplier.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.4.2 — Ensure all external dependencies used in the build process are locked

CIS: **Manual**, trang 160.

**Audit:** Kiểm kê dependency và lock/version/hash thực tế.

**Remediation đề xuất:** Khóa mọi external dependency theo phiên bản xác minh.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** sandbox, supplier.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.4.3 — Ensure dependencies are validated before being used

CIS: **Manual**, trang 162.

**Audit:** Đối chiếu hash/chữ ký với trusted source trước sử dụng.

**Remediation đề xuất:** Xác minh checksum/signature/attestation trước chạy công cụ.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** sandbox, supplier.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.4.4 — Ensure the build pipeline creates reproducible artifacts

CIS: **Manual**, trang 164.

**Audit:** Build lặp lại cùng input trong môi trường đã kiểm soát.

**Remediation đề xuất:** Loại yếu tố không xác định và so byte/hash đầu ra.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** sandbox, supplier.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.4.5 — Ensure pipeline steps produce a Software Bill of Materials (SBOM)

CIS: **Manual**, trang 165.

**Audit:** Đọc SBOM, kiểm package coverage và liên kết artifact digest.

**Remediation đề xuất:** Sinh SBOM mỗi build đúng phạm vi và định dạng được chấp nhận.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** sandbox, supplier.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.4.6 — Ensure pipeline steps sign the Software Bill of Materials (SBOM) produced

CIS: **Manual**, trang 166.

**Audit:** Kiểm chữ ký SBOM và danh tính signer.

**Remediation đề xuất:** Ký SBOM bằng danh tính tin cậy và xác minh khi sử dụng.

**Re-audit:** Lặp lại Audit trên cùng đối tượng sau khắc phục; ghi before/after, người thực hiện, thời điểm, ref, bằng chứng và thử trường hợp bị từ chối. Không sửa main hoặc settings trong đợt này.

**Nguồn bằng chứng cần có:** sandbox, supplier.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.
