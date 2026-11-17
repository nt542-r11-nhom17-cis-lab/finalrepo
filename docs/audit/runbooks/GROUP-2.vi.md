# Nhóm 2: 33 quy trình Audit–Remediation–Re-audit

Đủ quy trình không đồng nghĩa đủ triển khai hoặc đạt tuân thủ. Hướng dẫn dưới đây diễn giải để áp dụng lab; đối chiếu Audit/Remediation gốc tại trang tham chiếu khi thực hiện. Phạm vi đợt đánh giá không bao gồm thay đổi settings, quyền người dùng, xóa tài nguyên hoặc chỉnh sửa main. Khi kiểm tra lại, ghi đối tượng, ref, người thực hiện, thời gian và bằng chứng trước/sau; các phép thử gây thay đổi chỉ thực hiện trên đối tượng thử được phê duyệt.

## 2.1.1 — Ensure each pipeline has a single responsibility

CIS: **Manual**, trang 123.

**Audit:** Kiểm tra trách nhiệm và quyền của từng pipeline.

**Remediation đề xuất:** Tách pipeline theo mục đích và giảm quyền mỗi pipeline.

**Re-audit:** Đọc lại trigger, job, quyền và đầu ra của từng pipeline; đối chiếu một lần chạy thực với trách nhiệm đã mô tả, ghi các tác vụ vượt phạm vi cần tách.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.2 — Ensure all aspects of the pipeline infrastructure and configuration are immutable

CIS: **Manual**, trang 125.

**Audit:** Đối chiếu image/infrastructure/config với phiên bản và cơ chế sửa trực tiếp.

**Remediation đề xuất:** Mã hóa cấu hình, pin image và tái tạo thay vì sửa thủ công.

**Re-audit:** Đối chiếu source tree, image digest và log trước/sau mỗi lần tạo lại.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.3 — Ensure the build environment is logged

CIS: **Manual**, trang 127.

**Audit:** Kiểm tra log môi trường build và chính sách giữ log.

**Remediation đề xuất:** Ghi image version, tool versions và cấu hình cần thiết, che secrets.

**Re-audit:** Tải artifact, đối chiếu commit/run ID; kiểm tra không có token, secret hoặc home path.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.4 — Ensure the creation of the build environment is automated

CIS: **Manual**, trang 128.

**Audit:** Tạo lại môi trường build từ mã trong môi trường sạch.

**Remediation đề xuất:** Tự động hóa provisioning và ghi cấu hình trong VCS.

**Re-audit:** Tạo lại môi trường build từ cấu hình được quản lý phiên bản trên runner sạch; ghi commit, image và các bước provisioning, xác nhận không cần sửa tay để hoàn tất build.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.5 — Ensure access to build environments is limited

CIS: **Manual**, trang 129.

**Audit:** Liệt kê người/app có quyền vào môi trường build.

**Remediation đề xuất:** Giảm quyền theo vai trò, rà soát định kỳ.

**Re-audit:** Tài khoản Read không được sửa/kích hoạt trái phép; Write chỉ làm nhiệm vụ cần thiết.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.6 — Ensure users must authenticate to access the build environment

CIS: **Manual**, trang 131.

**Audit:** Thử truy cập chưa xác thực trong môi trường kiểm thử.

**Remediation đề xuất:** Bắt buộc xác thực cho mọi đường quản trị build.

**Re-audit:** Tài khoản chưa đăng nhập/không được cấp quyền không thể điều khiển build.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.7 — Ensure build secrets are limited to the minimal necessary scope

CIS: **Manual**, trang 132.

**Audit:** Đọc metadata phạm vi secrets mà không đọc giá trị.

**Remediation đề xuất:** Giới hạn secrets theo repo/environment/job, ưu tiên credentials ngắn hạn.

**Re-audit:** Kiểm tra job không dùng secret ngoài phạm vi; artifact không chứa private key.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.8 — Ensure the build infrastructure is automatically scanned for vulnerabilities

CIS: **Manual**, trang 134.

**Audit:** Xem scan của hạ tầng build, phạm vi và chu kỳ cập nhật.

**Remediation đề xuất:** Quét hạ tầng phù hợp và theo dõi xử lý lỗ hổng.

**Re-audit:** Đọc JSON scanner, kiểm tra coverage và lỗi kết nối phải được báo; không chỉ nhìn CI xanh.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.9 — Ensure default passwords are not used

CIS: **Manual**, trang 135.

**Audit:** Đối chiếu cấu hình dịch vụ với danh sách default credentials, không brute-force.

**Remediation đề xuất:** Loại mật khẩu mặc định và quản lý secrets đúng quy trình.

**Re-audit:** Xác nhận credential cũ bị từ chối; scanner HEAD/lịch sử có phạm vi ghi rõ.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.10 — Ensure webhooks of the build environment are secured

CIS: **Manual**, trang 136.

**Audit:** Đọc cấu hình webhook build: HTTPS, certificate verification, auth.

**Remediation đề xuất:** Bảo vệ webhook build và kiểm tra lại endpoint.

**Re-audit:** Delivery sai chữ ký/replay bị từ chối; không lộ secret trong log.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.1.11 — Ensure minimum number of administrators are set for the build environment

CIS: **Manual**, trang 137.

**Audit:** Kiểm kê admin của build system và lý do cấp quyền.

**Remediation đề xuất:** Giảm admin tới mức tối thiểu cần thiết.

**Re-audit:** Owner duyệt danh sách và thử bằng tài khoản không admin.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.1 — Ensure build workers are single-used

CIS: **Manual**, trang 139.

**Audit:** Kiểm tra runner lifecycle, reuse và dữ liệu tồn dư giữa job.

**Remediation đề xuất:** Dùng runner dùng một lần hoặc tái tạo và làm sạch được kiểm chứng.

**Re-audit:** Đối chiếu runner/job ID của hai lần build độc lập và bằng chứng hủy môi trường; xác nhận dữ liệu của lần đầu không tồn tại ở worker lần sau. Không suy ra chỉ từ tên ubuntu runner.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.2 — Ensure build worker environments and commands are passed and not pulled

CIS: **Manual**, trang 140.

**Audit:** Kiểm tra nguồn lệnh/config được cung cấp cho worker.

**Remediation đề xuất:** Truyền lệnh/config từ controller tin cậy, tránh worker kéo lệnh tùy ý.

**Re-audit:** Đối chiếu smoke test không mạng; thử tác vụ cần mạng phải thất bại trong container thử.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.3 — Ensure the duties of each build worker are segregated

CIS: **Manual**, trang 141.

**Audit:** Đối chiếu nhiệm vụ/credentials giữa các worker.

**Remediation đề xuất:** Tách worker theo nhiệm vụ và trust boundary.

**Re-audit:** Đối chiếu từng worker với vai trò build/test/publish/deploy, danh tính và quyền; thử một thao tác ngoài vai trò phải bị từ chối trên môi trường thử.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.4 — Ensure build workers have minimal network connectivity

CIS: **Manual**, trang 142.

**Audit:** Kiểm tra egress policy và thử endpoint allowed/denied.

**Remediation đề xuất:** Giới hạn mạng tối thiểu, không nới rule để làm xanh test.

**Re-audit:** Kiểm tra egress policy bằng kết nối tới đích được phép và không được phép từ worker; lưu rule/log. Phân biệt container network none với quyền mạng của host runner.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.5 — Ensure run-time security is enforced for build workers

CIS: **Manual**, trang 144.

**Audit:** Kiểm tra runtime security agent/policy và sự kiện thử nghiệm.

**Remediation đề xuất:** Áp dụng runtime protection và giám sát phản hồi.

**Re-audit:** Thử ghi root FS/mở mạng trong container thử phải thất bại; kiểm tra log run.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.6 — Ensure build workers are automatically scanned for vulnerabilities

CIS: **Manual**, trang 145.

**Audit:** Quét package của worker đúng image/version.

**Remediation đề xuất:** Quét định kỳ và xử lý CVE theo ngưỡng đã thống nhất.

**Re-audit:** Chạy scanner trên image/worker thực và đối chiếu digest với worker được sử dụng; ghi severity, lỗi quét và coverage. Image demo không thay báo cáo toàn bộ host.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.7 — Ensure build workers' deployment configuration is stored in a version control platform

CIS: **Manual**, trang 146.

**Audit:** Đối chiếu cấu hình triển khai worker với Git commit.

**Remediation đề xuất:** Lưu cấu hình worker trong VCS và review thay đổi.

**Re-audit:** Đối chiếu archive HEAD với cấu hình worker được triển khai và commit/tree trong provenance.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.2.8 — Ensure resource consumption of build workers is monitored

CIS: **Manual**, trang 148.

**Audit:** Theo dõi CPU/RAM/disk trong tải thực tế và cảnh báo.

**Remediation đề xuất:** Thiết lập monitoring và kiểm tra đường cảnh báo.

**Re-audit:** Chạy tải thử có giới hạn được phê duyệt; kiểm tra CPU/RAM/disk metrics và cảnh báo đến người nhận, ghi ngưỡng và thời gian thay vì chỉ ảnh tiến trình.

**Nguồn bằng chứng cần có:** repository_files, build_platform_admin.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.1 — Ensure all build steps are defined as code

CIS: **Manual**, trang 150.

**Audit:** So toàn bộ bước build với YAML/script đang version-control.

**Remediation đề xuất:** Đưa các bước build vào mã và loại bước không truy vết.

**Re-audit:** Đối chiếu log build mới với các step trong workflow ở đúng commit; ghi mọi lệnh triển khai thủ công hoặc cấu hình ngoài Git chưa được quản lý.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.2 — Ensure steps have clearly defined build stage input and output

CIS: **Manual**, trang 151.

**Audit:** Kiểm tra contract input/output từng stage.

**Remediation đề xuất:** Khai báo, kiểm tra schema/hash và fail khi output không hợp lệ.

**Re-audit:** Cấp input hợp lệ và input thiếu/sai cho step thử; đối chiếu schema/nội dung/hash output và kiểm tra input không hợp lệ không tạo đầu ra được chấp nhận.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.3 — Ensure output is written to a separate, secured storage repository

CIS: **Manual**, trang 152.

**Audit:** Xác định kho output, quyền truy cập và tách biệt nguồn.

**Remediation đề xuất:** Lưu output vào kho riêng được bảo vệ và kiểm soát quyền.

**Re-audit:** Tải artifact từ run, xác minh fingerprint/chữ ký; thử quyền truy cập bằng user phù hợp.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.4 — Ensure changes to pipeline files are tracked and reviewed

CIS: **Manual**, trang 153.

**Audit:** Lấy mẫu thay đổi workflow và review tương ứng.

**Remediation đề xuất:** Bắt buộc review pipeline file, ghi lịch sử và code owner.

**Re-audit:** Tạo PR thử sửa workflow, truy commit về task và kiểm tra review bắt buộc bởi người phù hợp; xác nhận thay đổi chưa review không được đưa vào nhánh đích thử.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.5 — Ensure access to build process triggering is minimized

CIS: **Manual**, trang 154.

**Audit:** Kiểm kê ai có thể dispatch/rerun/trigger qua token hoặc event.

**Remediation đề xuất:** Giới hạn trigger, runner và quyền token theo nhu cầu.

**Re-audit:** Push nhánh đúng tạo run; nhánh khác không kích hoạt workflow bổ sung; tài khoản Read không điều khiển được build.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.6 — Ensure pipelines are automatically scanned for misconfigurations

CIS: **Manual**, trang 155.

**Audit:** Quét misconfiguration toàn bộ pipeline files.

**Remediation đề xuất:** Bổ sung scanner và sửa cấu hình không an toàn.

**Re-audit:** Quét workflow ở commit đánh giá và dùng fixture misconfiguration để kiểm tra detection/gate; rà lỗi phân tích hoặc file bị loại trừ trước khi ghi kết quả.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.7 — Ensure pipelines are automatically scanned for vulnerabilities

CIS: **Manual**, trang 156.

**Audit:** Kiểm tra vulnerability scanner cho pipeline và tools được dùng.

**Remediation đề xuất:** Quét thành phần pipeline và xử lý lỗ hổng.

**Re-audit:** Đọc report/log run; thêm fixture không an toàn chỉ trong unit/offline hoặc nhánh thử riêng để xác nhận scanner bắt lỗi.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.3.8 — Ensure scanners are in place to identify and prevent sensitive data in pipeline files

CIS: **Automated**, trang 157.

**Audit:** Đưa dữ liệu giả vào pipeline fixture và xác minh secret scanner phát hiện.

**Remediation đề xuất:** Quét mọi pipeline, chặn theo chính sách và không dùng secret thật để thử.

**Re-audit:** Chèn secret giả vào fixture pipeline, xác nhận scanner chặn; quét lại workflow thực và phân biệt source hiện tại với lịch sử, không dùng credential thật làm mẫu.

**Nguồn bằng chứng cần có:** repository_files, required_check_enforcement.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.4.1 — Ensure all artifacts on all releases are signed

CIS: **Manual**, trang 159.

**Audit:** Kiểm kê mọi release và mọi artifact có chữ ký hợp lệ.

**Remediation đề xuất:** Ký tất cả release artifacts và xác minh trước phân phối.

**Re-audit:** Xác minh mọi payload trong manifest; sửa một byte hoặc thay key phải thất bại.

**Nguồn bằng chứng cần có:** sandbox, supplier.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.4.2 — Ensure all external dependencies used in the build process are locked

CIS: **Manual**, trang 160.

**Audit:** Kiểm kê dependency và lock/version/hash thực tế.

**Remediation đề xuất:** Khóa mọi external dependency theo phiên bản xác minh.

**Re-audit:** Kiểm kê Actions, base image, wheel, binary tải và phụ thuộc gián tiếp; xác minh mỗi mục khóa bằng SHA/digest/hash phù hợp, ghi rõ thành phần còn dùng tag hoặc tải động.

**Nguồn bằng chứng cần có:** sandbox, supplier.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.4.3 — Ensure dependencies are validated before being used

CIS: **Manual**, trang 162.

**Audit:** Đối chiếu hash/chữ ký với trusted source trước sử dụng.

**Remediation đề xuất:** Xác minh checksum/signature/attestation trước chạy công cụ.

**Re-audit:** Thay một byte của bản sao dependency trong sandbox và kiểm tra xác minh hash/chữ ký thất bại trước khi sử dụng; đối chiếu trust root đã được phê duyệt cho dependency gốc.

**Nguồn bằng chứng cần có:** sandbox, supplier.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.4.4 — Ensure the build pipeline creates reproducible artifacts

CIS: **Manual**, trang 164.

**Audit:** Build lặp lại cùng input trong môi trường đã kiểm soát.

**Remediation đề xuất:** Loại yếu tố không xác định và so byte/hash đầu ra.

**Re-audit:** Build hai lần trong môi trường sạch từ cùng source commit và bộ dependency khóa; so hash artifact, điều tra mọi chênh lệch timestamp/nội dung thay vì chỉ so tên file.

**Nguồn bằng chứng cần có:** sandbox, supplier.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.4.5 — Ensure pipeline steps produce a Software Bill of Materials (SBOM)

CIS: **Manual**, trang 165.

**Audit:** Đọc SBOM, kiểm package coverage và liên kết artifact digest.

**Remediation đề xuất:** Sinh SBOM mỗi build đúng phạm vi và định dạng được chấp nhận.

**Re-audit:** Phân tích SBOM của đúng run, đối chiếu package/phiên bản/hash với inventory build; ghi các thành phần OS/tool/application bị thiếu, không coi inventory rỗng là đạt.

**Nguồn bằng chứng cần có:** sandbox, supplier.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.

## 2.4.6 — Ensure pipeline steps sign the Software Bill of Materials (SBOM) produced

CIS: **Manual**, trang 166.

**Audit:** Kiểm chữ ký SBOM và danh tính signer.

**Remediation đề xuất:** Ký SBOM bằng danh tính tin cậy và xác minh khi sử dụng.

**Re-audit:** Dùng fingerprint hoặc identity ký được tin cậy từ nguồn riêng để xác minh SBOM; sửa bản sao SBOM và thử khóa sai phải bị từ chối. Ghi rõ khóa lab tạm thời nếu dùng.

**Nguồn bằng chứng cần có:** sandbox, supplier.

**Người phụ trách:** TV2 (vai trò đề xuất; cần username thật).

**Giới hạn:** Nhánh mới hoặc sandbox; cấu hình tổ chức/registry/production chỉ đề xuất, không áp dụng. Bằng chứng thật trên đúng phạm vi; ảnh phần 2, mô tả/bảng phần 3. Không dùng sơ đồ hoặc kết quả mô phỏng thay screenshot thực nghiệm.
