# Cập nhật triển khai tích hợp HTTPS

Trạng thái mới nhất nằm trong [INTEGRATION.vi.md](INTEGRATION.vi.md): registry source-build đã được khắc phục tám HIGH, 51 unit tests và 34 phép thử HTTPS thành công. Đợt triển khai trước bên dưới được giữ để mô tả topology/phân quyền nền; số liệu hiện hành dùng RESULTS.vi.md và COVERAGE.vi.md. Hình mới thuộc METHOD.vi.md phần 2; phần 3 chỉ chữ/bảng.

# 3. Triển khai trên nhánh riêng

## 3.1 Mô hình và phân quyền

Repository hiện tại là `nt542-r11-nhom17-cis-lab/finalrepo`, public, thuộc Organization Free. Nhánh triển khai đợt này là `audit/free-controls-completion`, kế thừa các nhánh audit trước. Không merge hoặc sửa `main`; SHA đối chiếu trước/sau là `e052945db5b4a2bace480b5ab98446a8b82da02e`. Không tác động hai repo nguồn. Hình mô hình/phương pháp thuộc phần 2 trong METHOD.vi.md; phần 3 chỉ mô tả bằng chữ và bảng.

Mô hình gồm các tài khoản GitHub, repository chứa mã/cấu hình được quản lý phiên bản, GitHub API đọc hiện trạng, GitHub-hosted runner Ubuntu 24.04, container demo không có mạng và kho Actions artifact tách khỏi đĩa runner. Ba workflow phụ trách kiểm tra nguồn/container, kiểm tra bảo mật workflow và thu thập bằng chứng Free. Worker dùng token `contents: read`, checkout không lưu credential. Khóa ký RSA tạm nằm trong thư mục tạm riêng, không được đưa vào gói kết quả. Chữ ký cùng job chứng minh tính toàn vẹn có giới hạn; chưa thay danh tính ký release được tin cậy. Chưa có registry riêng hay production thật do nhóm cung cấp.

Snapshot GET API dưới danh tính người dùng đọc được bốn tài khoản. Đây là quyền quan sát được, không phải bằng chứng mọi quyền kế thừa/tổng thành viên đã được kiểm kê. Workflow token chỉ nhìn thấy hai collaborator trong cùng đợt; không dùng số này làm tổng thành viên. Nguồn: `evidence/free-collaborator-roles.json` và `evidence/free-controls-results.json`.

| Tài khoản nhìn thấy qua API người dùng | Quyền hiện tại | Nhiệm vụ đề xuất để nhóm xác nhận | Đầu ra cần có | Kết quả đã xác minh |
|---|---|---|---|---|
| hieune-ui | Admin | Điều phối, rà quyền/cấu hình Organization và phê duyệt kết quả | Bảng quyền, bằng chứng Settings, nhánh audit | Có nhánh/commit và CI; chưa thay Settings hoặc cấp quyền |
| Vuongdlx | Write | Source/build, kiểm tra nhóm 1–2 | JSON/CSV API, log scanner, kiểm thử PR trên nhánh thử | Đã xác minh quyền Write; chưa có bằng chứng tài khoản này thực hiện nhiệm vụ đề xuất |
| HiepTran01 | Read | Rà supplier/dependency/artifact, nhóm 3–4 | SBOM/provenance supplier, nhận xét license/registry | Đã xác minh quyền Read; muốn push cần owner quyết định cấp quyền thích hợp |
| dtk0106 | Read | Kiểm chứng triển khai, tổng hợp nhóm 5 | Bảng triển khai và log môi trường được phép | Đã xác minh quyền Read; chưa có production thực tế hoặc bằng chứng thực hiện nhiệm vụ |

Không tự thay quyền, thêm Code Owner hay mời người. Nhóm cần xác nhận các tài khoản có đúng người dự kiến. Mục 1.3.7 còn cần owner xác minh full effective access và chọn admin thứ hai nếu áp dụng theo yêu cầu CIS; không nâng cả nhóm thành Admin. Kiểm thử hai reviewer cần danh tính thật, không dùng tài khoản chung. Kết quả CI chỉ xác nhận tác vụ tự động đã chạy; chưa có bằng chứng ba tài khoản còn lại thực hiện nhiệm vụ được đề xuất.

## 3.2 Triển khai Manual

Phương pháp là Audit → Remediation → Re-audit; manual là cách thực hiện. Đã đối chiếu inventory với mã tiêu chí, thử GET cấu hình, đọc scope kết quả và chuẩn bị hướng dẫn riêng cho 48 mục. Các thay đổi Settings chưa được thực hiện; không báo đã khắc phục khi chỉ có file đề xuất.

| Mục | Audit thực hiện / kết quả | Đạt hay chưa | Bước tiếp theo |
|---|---|---|---|
| 1.1.5/.10/.11/.12/.13/.14/.15 | Classic protection API HTTP 403 | MANUAL_REVIEW | Owner đọc rule có hiệu lực và bypass; thử trên đúng nhánh `audit/protection-sandbox` |
| 1.1.7 | Có CODEOWNERS, nhưng rule bắt buộc review chưa đọc được | PARTIAL | Xác minh người sở hữu có quyền và PR thiếu review bị chặn |
| 1.1.8, 1.2.5 | Inventory đọc sáu nhánh, không có fork nhìn thấy; không xóa tài nguyên | PARTIAL | Owner xác nhận mục đích/hoạt động, lập lịch rà soát và biên bản |
| 1.3.7 | Snapshot người dùng thấy một admin; token CI có phạm vi nhìn thấy khác | MANUAL_REVIEW | Owner xác minh toàn bộ quyền kế thừa và chọn admin thứ hai; chưa tự cấp quyền |
| 1.3.4, 1.3.6, 1.4.1–1.4.4 | Chưa có Settings/MFA/app/webhook evidence đủ quyền | NOT_TESTED | Thực hiện các bước cụ thể trong FREE-CONTROLS.vi.md, che thông tin nhạy cảm |
| 3.1.2 | Chưa có SBOM gốc từ mọi supplier | NOT_TESTED | Thu thập supplier-issued SBOM; SBOM do nhóm tạo không thay tài liệu supplier |
| 5.2.3/.4 | Chưa có production được nhóm cho phép | NOT_TESTED | Cung cấp môi trường và người quản trị; không dùng sandbox làm bằng chứng production |

Mẫu `config/protection-sandbox.ruleset.json` chỉ khớp `refs/heads/audit/protection-sandbox`, không có bypass; chưa được POST/apply. Cần hai reviewer thật và cấu hình ký commit trước khi áp dụng. Mẫu không bao gồm mọi yêu cầu status checks/push restrictions; hướng dẫn nêu phần owner phải hoàn thiện. Không tạo PR vào main, không thử force-push/xóa trên main. Ảnh Settings và kiểm thử owner cần bổ sung ở phần 2; mỗi ảnh phải ghi đúng cấu hình, thời điểm và run được kiểm tra.

Danh sách đầy đủ 48 mục và Audit/Remediation/Re-audit: [FREE-CONTROLS.vi.md](FREE-CONTROLS.vi.md). Bảng 27 mục cần điều kiện tiếp theo: [FREE-COMPLETION.vi.md](FREE-COMPLETION.vi.md). Hai mươi mốt mục có bằng chứng thành phần cũng còn các giới hạn cần xử lý, không phải đã đạt hoàn toàn.

## 3.3 Triển khai tự động hóa và Remote Automated

CIS vẫn phân loại 118 Manual, hai Automated (1.1.3 và 2.3.8). Việc viết script cho mục Manual không đổi nhãn CIS. Workflow bổ sung tự chạy khi push đúng `audit/free-controls-completion`; không thêm trigger mới lên main, không dùng pull_request_target, không cấp token write. Hai workflow cũ pipeline-io và pipeline-security giữ workflow_dispatch và được thêm trigger đúng nhánh này.

| Tool / step | Đầu ra | Kết quả thành phần / giới hạn |
|---|---|---|
| record_runtime.py | runtime.json | Allowlist OS/Python/OpenSSL/runner image/commit/run; không dump env hoặc token |
| audit_free_controls.py | free-controls/results.json và CSV | Đủ 48 dòng: năm đủ nguồn khai báo cho bước thu thập, 43 còn thiếu nguồn; full-control PASS=0 |
| inventory_governance.py | governance/results.json | Sáu nhánh với SHA/tuổi commit, zero fork API-visible; phân trang đầy đủ, zero thao tác xóa |
| monitor_action_owners.py | action-owners/results.json | Tám cặp repo/owner numeric ID không đổi; lỗi API/owner đổi/action mới phải được review, không tự cập nhật baseline |
| project_bundle.py | source.zip, project.spdx.json, provenance.json, signed manifest, public key, verification.json | Ba payload khớp chữ ký/hash; sửa payload/manifest hoặc dùng fingerprint sai bị từ chối. Fingerprint đối chiếu với log run đã xác thực |
| dependency_graph.py trong môi trường tool đã khóa hash | dependency-graph/results.json | 32 node, 145 quan hệ khai báo; 32 cạnh active ở môi trường mặc định, zero lỗi; không khẳng định mọi extra đã resolve |
| Unit tests | Log CI | 37 PASS; có thử API bị từ chối/phân trang dở dang, owner drift, thiếu/sai dependency, sửa manifest/payload và khóa sai |
| Bandit, pip-audit và kiểm tra coverage/hash | JSON trong security artifact | Zero Bandit HIGH; đúng 32 package, zero advisory đã biết, 32 hash wheel khớp PyPI; 20 license còn cần review |
| Gitleaks current tree | current-source-gitleaks.json | Zero phát hiện ở source hiện tại; không có tuyên bố lịch sử đã sạch hoặc credential cũ đã thu hồi |
| Docker/Trivy | JSON scanner và log runtime | Zero HIGH/CRITICAL theo phạm vi scan; kiểm tra non-root, CapEff=0, NoNewPrivs=1 và từ chối ghi. Không thay quét/bảo vệ toàn bộ host runner |
| Zizmor | Log workflow security | Quét mọi workflow; finding thiếu tên job ở run đầu đã sửa, run xác nhận thành công |
| upload-artifact | Artifact ngoài runner, retention bảy ngày | Bảo toàn kết quả; repo public, chưa phải kho output riêng tư có ACL được kiểm thử |

Code được xác minh: `f1df426fb33f05fbdf64f04d5068a6d6c97085bf`. Các commit báo cáo sau đó không thay code đã được kiểm tra.

| Workflow | Run | Kết quả |
|---|---|---|
| Free controls evidence | [44108703310](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44108703310) | SUCCESS; đã tải, đọc và xác minh bundle theo fingerprint từ log |
| Source/container, API, SBOM/lab | [44108703867](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44108703867) | SUCCESS; đã tải và đọc security/review artifact |
| Workflow security | [44108703323](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44108703323) | SUCCESS |

File xuất kết quả lưu lâu dài trong nhánh: [free-controls-export.zip](evidence/free-controls-export.zip), chứa các đầu ra Free/security/review của đúng những run trên, bao gồm signed source bundle. JSON/CSV 48 mục cũng có bản riêng trong evidence. SHA256 của ZIP nằm ở `evidence/free-completion-summary.json`. Không lưu private signing key. Kết quả chi tiết và thống kê 120 mục nằm trong RESULTS.vi.md và COVERAGE.csv; CI xanh không phải chứng nhận đạt CIS.
