> Phụ lục kỹ thuật theo commit/phiên chạy được nêu trong tài liệu. Bảng kết quả tổng hợp hiện hành: [RESULTS.vi.md](RESULTS.vi.md).

# Kiểm thử tích hợp HTTPS và khắc phục registry

Nhánh triển khai: `audit/remaining-free-integration`, kế thừa bản biên tập báo cáo. Đợt này bổ sung dịch vụ thử nghiệm thật trên loopback và kiểm kê Organization bằng GET API. Không đổi main, Rulesets, quyền thành viên, MFA, webhook GitHub hoặc hai repo nguồn. Không tạo registry/production công khai và không dùng dịch vụ trả phí.

## 2. Phương pháp Audit → Remediation → Re-audit

### Webhook

Audit kiểm tra HTTPS, chữ ký `X-Hub-Signature-256`, event, delivery ID, kích thước và nội dung request. Remediation được hiện thực bằng `scripts/webhook_receiver.py`: TLS tối thiểu 1.2, HMAC SHA256 so sánh constant-time, chỉ nhận ping/push, giới hạn body 64 KiB, từ chối header không hợp lệ và lưu cache chống replay có giới hạn. Receiver không chạy shell, build hoặc deployment.

Re-audit dùng `scripts/webhook_integration.py` gửi request thật đến HTTPS loopback. Tổng cộng 11 phép thử xác nhận request hợp lệ được nhận, HMAC sai hoặc body bị sửa bị từ chối, cùng body không thể gửi lại chỉ bằng cách đổi delivery ID, event không cho phép bị chặn, dữ liệu sai định dạng/quá kích thước bị từ chối và client không tin chứng chỉ không thể kết nối. Cache ở bộ nhớ tồn tại 600 giây, mất khi khởi động lại và có thể từ chối payload hợp lệ trùng nội dung; triển khai thực tế cần chính sách/persistent store phù hợp.

Đây là delivery tổng hợp trong môi trường kiểm thử; chưa có GitHub delivery, endpoint bên ngoài hoặc build trigger thực tế. Tài khoản owner vẫn cần phê duyệt endpoint, quản lý secret và cấu hình webhook qua Settings.

### Registry và chuỗi cung ứng binary

Audit ban đầu dùng Distribution v3.1.2 từ release upstream, kiểm tra SHA256 archive/executable trước khi chạy. Bản quét filesystem đầu tiên không nhận diện binary Go nên không được dùng làm bằng chứng sạch. Chuyển sang Trivy rootfs, bật inventory package và thêm `verify_registry_scan.py` buộc có đúng bản ghi binary theo SHA đã khóa cùng danh sách package không rỗng.

Bản quét đúng nhận diện 104 package và báo tám HIGH. Remediation build lại source commit `3220848f15d9279c66a41aa0a257469e6aede1e9` bằng Go 1.27.4, cập nhật go-jose/v4 lên v4.1.6, klauspost/compress lên v1.18.7 và x/net lên v0.62.0. Cấu hình lưu SHA256 source archive, SDK archive, go.mod, go.sum và binary đầu ra. `build_registry.py` xác minh input, giải nén bằng data filter, build với module locks readonly, trimpath và buildvcs=false, chạy `go mod verify`, rồi đối chiếu SHA256 đầu ra. Không tắt GOSUMDB, không bỏ qua HIGH/CRITICAL. Go module locks là cấu hình build cần thiết, không phải SDK hoặc source cache được đưa vào repo.

Binary `3.1.2+cis.1` là bản build riêng từ source và dependency locks đã ghi nhận, không phải binary upstream. Chữ ký/provenance độc lập của toàn bộ supplier chưa được chứng minh. Trường `archive_sha256` trong kết quả integration gốc là checksum archive binary upstream dùng đối chiếu ban đầu; nguồn thực tế của bản rebuild nằm trong `build` của `config/registry-integration.lock.json`. Binary triển khai được đối chiếu bằng `binary_sha256`.

Re-audit nhận diện 104 package trong binary mới, zero HIGH/CRITICAL theo dữ liệu scanner của lần chạy. Hash binary build local và CI trùng giá trị đã khóa. Các test đầu vào độc hại xác nhận archive không thể ghi ra ngoài thư mục giải nén, binary không khớp SHA bị từ chối và báo cáo scanner rỗng/sai binary/thiếu inventory không thể được chấp nhận.

Hình tổng hợp trước/sau nằm trong phần 2 của METHOD.vi.md, không phải ảnh chụp giao diện. Kết quả scanner phụ thuộc thời điểm và phạm vi package được nhận diện; không suy thành zero mọi mức độ lỗ hổng hoặc tuân thủ toàn benchmark.



Yêu cầu tuổi phiên bản của mục 3.1.8 chưa được xác nhận đạt cho bộ build mới. SDK và dependency có bản vá cần được đối chiếu ngày phát hành; các ngoại lệ triển khai sớm phải do owner xem xét theo policy. Việc khắc phục HIGH không tự xác nhận tuân thủ yêu cầu tuổi package.

## 3. Triển khai và kết quả

### 3.1 Mô hình

GitHub-hosted runner checkout nhánh audit bằng token contents:read. Python receiver và Distribution registry chạy thành tiến trình riêng dưới tài khoản runner, chỉ bind 127.0.0.1 trên port tạm. OpenSSL tạo TLS certificate và khóa ký tạm trong thư mục riêng; registry dùng bcrypt htpasswd với một publisher thử nghiệm. Dữ liệu registry và credential được dọn khi kết thúc test; report không chứa khóa riêng, password, header Authorization hoặc payload webhook.

Registry nhận artifact OCI qua HTTPS. Pipeline kiểm tra chữ ký trước upload, lưu manifest, artifact và sidecar signature; sau đó tải lại manifest/blob/chữ ký và kiểm tra digest/chữ ký. Hai phiên bản 0.1.0/0.1.1 được kiểm kê bằng tags API. Chữ ký bị sửa và artifact bị sửa phải thất bại. Đây là kiểm tra client/pipeline, chưa có admission policy bắt registry tự từ chối mọi upload không ký. Basic-auth account chưa có MFA, IdP ngoài hoặc RBAC đọc/ghi theo user.

Phân công bốn tài khoản và quyền quan sát được tiếp tục theo IMPLEMENTATION.vi.md; đợt này không cấp hoặc thu hồi quyền. Registry thử không phải tài khoản GitHub của thành viên và không thay bằng chứng MFA của Organization.

### 3.2 Audit và phần cần owner xác minh

| Mục | Kết quả thực tế | Phạm vi còn thiếu |
|---|---|---|
| 1.2.7 | Một repo API-visible; có trạng thái archive và tuổi lần push | Owner xác nhận toàn bộ inventory, lịch rà và quyết định archive; không tự archive finalrepo |
| 1.4.4, 2.1.10 | Receiver HTTPS thật qua 11 phép thử | Endpoint được duyệt, GitHub/build delivery thật, vận hành và replay store bền vững |
| 4.2.2, 4.2.5 | Registry HTTPS/bcrypt thật; một publisher, ẩn danh bị trả 401 | Quyền toàn hệ thống, RBAC và deployment bền vững |
| 4.3.2 | Xác minh hai phiên bản sau download, gồm manifest/artifact/sidecar signature | Mọi artifact thực tế, trust root và registry-side admission |
| 5.1.4 | Đã rà API-visible role counts và CODEOWNERS | Full effective access, bảo vệ/review bắt buộc và deployment target; protection API còn 403 |

Ba mục 1.2.7/1.4.4/2.1.10 chuyển từ NOT_TESTED sang PARTIAL. Ba mục registry 4.2.2/4.2.5/4.3.2 chuyển từ mô hình offline LAB_ONLY sang bằng chứng tích hợp PARTIAL. Mục 5.1.4 chuyển sang MANUAL_REVIEW. Không có mục được chuyển sang full-control PASS chỉ từ các test trên.

Trong 48 mục hướng Free ban đầu: **24 PARTIAL, 9 MANUAL_REVIEW, 15 NOT_TESTED**. Trong 27 mục cần triển khai/xác minh ở đợt trước, ba mục đã có thêm triển khai thành phần; 24 mục còn ở mức cần xác minh hoặc chưa triển khai. Các mục PARTIAL cũng chưa hoàn tất toàn bộ yêu cầu.

### 3.3 Tool / step → kết quả

| Tool / step | Kết quả | Đầu ra |
|---|---|---|
| Unit tests và negative tests | 51 PASS | Log CI |
| webhook_integration.py | 11 PASS, receiver dừng sau test | JSON trong artifact integration |
| registry_integration.py | 23 PASS, hai phiên bản, registry dừng sau test | JSON trong artifact integration |
| build_registry.py + lockfiles | SDK/source/module/binary hash được đối chiếu; mod verify thành công | Cấu hình build và SHA trong report |
| Trivy rootfs + coverage guard | 104 package; tám HIGH trước, zero HIGH/CRITICAL sau | Scanner JSON và coverage JSON |
| inventory_organization.py | GET-only; repo và role counts theo caller; policy không đủ quyền giữ MANUAL_REVIEW | Organization inventory JSON |
| Bandit / pip-audit / coverage | Zero HIGH; 32/32 package Python, zero advisory đã biết | Security artifact |
| Gitleaks current source | Zero finding | Không có tuyên bố lịch sử main đã sạch |
| Zizmor | Workflow scan SUCCESS | Log workflow security |

Code đã kiểm tra: `545c3a2ad044fa1292712b1c00bcb7244943fbbe`.

| Workflow | Run | Kết quả |
|---|---|---|
| HTTPS integration và registry binary scan | [44130146471](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44130146471) | SUCCESS; artifact đã tải và đọc |
| Source/container và các audit trước | [44130146389](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44130146389) | SUCCESS; security artifact đã tải và đọc |
| Workflow security | [44130148225](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44130148225) | SUCCESS |
| Baseline upstream có HIGH | [44127179185](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44127179185) | Gate thất bại đúng yêu cầu; được giữ làm before-remediation evidence |

File xuất kết quả được chọn để lưu trong nhánh: [JSON tổng hợp](evidence/remaining-integration-summary.json) và [CSV 34 phép thử HTTPS](evidence/remaining-integration-checks.csv). Raw scanner/integration output thuộc artifact của đúng run; không đưa SDK, binary, private keys, password, source/module cache hoặc build log tạm vào Git.

## Công việc còn cần điều kiện thực tế

Mười lăm mục hướng Free còn NOT_TESTED: 1.1.19; 1.3.1/1.3.3/1.3.4/1.3.6/1.3.13; 1.4.1/1.4.2/1.4.3; 2.1.5/2.1.6/2.1.11; 3.1.2; 5.2.3/5.2.4. Owner cần bằng chứng policy/audit log UI, phân công và MFA; supplier cần cung cấp SBOM; production cần môi trường được phép và quyền thực tế. API HTTP 403 không chứng minh các mục đó cần Enterprise.

Chín mục MANUAL_REVIEW của phạm vi 48: 1.1.5/1.1.10/1.1.11/1.1.12/1.1.13/1.1.14/1.1.15, 1.3.7 và 5.1.4. Các bước thao tác đã có trong PROCEDURES.vi.md; dùng nhánh thử riêng, không đổi main. Các mục thiếu điều kiện triển khai không được tự động đổi thành N/A hoặc PASS. Ba mục tính năng Enterprise 1.3.10–1.3.12 vẫn giữ riêng ngoài phạm vi 48 mục hướng Free.
