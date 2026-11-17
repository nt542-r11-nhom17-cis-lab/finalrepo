# Bổ sung 48 tiêu chí theo hướng miễn phí

Nhánh `audit/free-controls-completion`, kế thừa `audit/organization-controls`; không merge vào `main`. Phạm vi là 48 mục NOT_TESTED của snapshot trước, loại ba mục Enterprise 1.3.10/1.3.11/1.3.12. Có hướng dẫn riêng Audit → Remediation → Re-audit cho **48/48 mục** trong [FREE-CONTROLS.vi.md](FREE-CONTROLS.vi.md), báo cáo được tổ chức riêng trong docs/audit.

## Kết quả theo mức triển khai

| Trong 48 mục ban đầu | Số mục | Ý nghĩa |
|---|---:|---|
| Có thêm triển khai/bằng chứng thành phần | 21 | PARTIAL; vẫn cần hoàn thiện phạm vi/hiệu lực |
| Đã rà nhưng cần owner/quyền kiểm tra tiếp | 8 | MANUAL_REVIEW; không xem lỗi quyền là FAIL/PASS cấu hình |
| Chưa có triển khai thực tế | 19 | NOT_TESTED; có hướng dẫn và lý do cụ thể |
| Đủ bằng chứng toàn bộ tiêu chí | 0 | Không báo đạt bằng mô phỏng hoặc CI xanh |

Toàn bộ 120 mục hiện có 66 PARTIAL, 22 MANUAL_REVIEW, 10 LAB_ONLY và 22 NOT_TESTED. Trong 22 NOT_TESTED còn 19 mục của phạm vi Free và ba mục cần tính năng Enterprise tương ứng. Các mục PARTIAL/MANUAL_REVIEW/LAB_ONLY cũng chưa hoàn tất.

## Các phần đã bổ sung và giới hạn

| Mục CIS | Bằng chứng/kết quả thành phần | Phần chưa hoàn tất |
|---|---|---|
| 1.1.1 | project-bundle/provenance.json + source.zip | Đã đóng gói đúng commit/tree từ Git; chưa chứng minh mọi thay đổi ngoài checkout đều được quản lý. |
| 1.1.7 | .github/CODEOWNERS + free-controls/results.json | Có Code Owner được xác định; protection API 403, chưa chứng minh bắt buộc review. |
| 1.1.8 | governance/results.json | Đã lấy branch/SHA/tuổi commit; chưa có owner review định kỳ và quyết định xóa. Không tự xóa. |
| 1.1.18 | .github/workflows/pipeline-io.yml + source scanner run | Đã tự động quét push nhánh audit; chưa bắt buộc mọi merge hoặc áp rule main. |
| 1.2.5 | governance/results.json | Đã kiểm kê fork qua API có phân trang; cần ledger mục đích/người phê duyệt và lịch rà soát. |
| 2.1.2 | Dockerfile + requirements-security.lock + runtime.json | Có digest/SHA/hash pins và source commit; GitHub-hosted runner image vẫn do nhà cung cấp cập nhật. |
| 2.1.3 | runtime.json | Đã ghi allowlist OS/tool/runner image/commit/run metadata; retention 7 ngày, chưa có policy lưu log được nhóm duyệt. |
| 2.1.7 | project-bundle/verification.json + workflow permissions | Token contents:read; khóa ký tạm không xuất; chưa xác minh mọi secret/credential của nền tảng. |
| 2.1.8 | trivy-image.json + python-package-audit.json | Đã quét image/toolchain; không thay quét toàn hạ tầng host runner. |
| 2.1.9 | database_config.py + current-source-gitleaks.json | Source dùng env, không hardcode credential ở HEAD; chưa xoay credential cũ hoặc chứng minh mọi tài khoản build không mặc định. |
| 2.2.2 | pipeline-io runtime checks | Demo truyền lệnh cục bộ, không mạng; job scanner khác vẫn tải tool/package nên chưa đạt mọi worker. |
| 2.2.5 | pipeline-io runtime checks | Đã kiểm tra non-root, CapEff=0, NoNewPrivs=1 và từ chối ghi; chưa có runtime detection cho mọi worker. |
| 2.2.7 | source.zip + Dockerfile + workflows | Cấu hình demo/worker workflow nằm trong Git; chưa đối chiếu provisioning bên nhà cung cấp. |
| 2.3.3 | free-controls run artifact metadata | Có artifact ngoài đĩa runner và retention; repo public, chưa có kho riêng an toàn với kiểm thử ACL. |
| 2.3.5 | .github/workflows/free-controls.yml + access snapshot | Trigger bổ sung chỉ đúng nhánh audit, không cấp token write; chưa áp least privilege cho toàn bộ người kích hoạt build. |
| 2.3.7 | pipeline-security Zizmor run | Đã tự động quét mọi workflow của nhánh; chưa có required check thực thi trên main. |
| 2.4.1 | project-bundle/manifest.json + manifest.sig | Đã ký ba payload bundle của run và thử chống sửa; không phải mọi artifact/mọi release, khóa chưa có trust authority production. |
| 3.1.3 | project-bundle/provenance.json + manifest.sig | Đã ký metadata commit/tree/source hash; chưa phải signed provenance độc lập từ mọi supplier. |
| 3.1.4 | dependency-graph/results.json | Đã xuất 32 node/145 quan hệ khai báo (32 active ở môi trường mặc định); còn Actions/OS/binary/extras resolution. |
| 3.1.6 | project-bundle/project.spdx.json + manifest.sig | Đã ký SBOM 32 scanner wheels của đúng commit; chưa bao phủ mọi thành phần phần mềm. |
| 3.2.4 | action-owners/results.json + config/action-owners.json | Đã theo dõi numeric repo/owner ID cho 8 Actions và chặn drift/lỗi; chưa theo dõi maintainers của 32 PyPI packages. |

## 27 mục cần owner/quyền/môi trường thực tế trước khi triển khai tiếp

Tám mục đã rà nhưng còn cần xác minh và 19 mục chưa triển khai ở bảng dưới. Nhấn liên kết để xem thao tác Audit, Remediation, Re-audit và minh chứng cần chụp; không chỉ là danh sách tên.

| Mục | Trạng thái | Điều kiện còn thiếu / công việc cần thực hiện |
|---|---|---|
| [1.1.5](FREE-CONTROLS.vi.md#cis-1-1-5) | MANUAL_REVIEW | API protection 403; cần owner và hai tài khoản thử thật. |
| [1.1.10](FREE-CONTROLS.vi.md#cis-1-1-10) | MANUAL_REVIEW | Cần quyền Settings và PR thử; không áp dụng main. |
| [1.1.11](FREE-CONTROLS.vi.md#cis-1-1-11) | MANUAL_REVIEW | Thiếu hiệu lực rule và kiểm thử nhiều tài khoản. |
| [1.1.12](FREE-CONTROLS.vi.md#cis-1-1-12) | MANUAL_REVIEW | Git author hoặc hash commit không thay bằng chứng chữ ký. |
| [1.1.13](FREE-CONTROLS.vi.md#cis-1-1-13) | MANUAL_REVIEW | Chưa đổi rule hoặc rewrite lịch sử. |
| [1.1.14](FREE-CONTROLS.vi.md#cis-1-1-14) | MANUAL_REVIEW | Không thử trên main để tránh khóa công việc nhóm. |
| [1.1.15](FREE-CONTROLS.vi.md#cis-1-1-15) | MANUAL_REVIEW | Không tự thay quyền hoặc mời người chưa được xác định. |
| [1.1.19](FREE-CONTROLS.vi.md#cis-1-1-19) | NOT_TESTED | Không dùng API Enterprise làm điều kiện bắt buộc của phương án Free; cần ảnh/log UI. |
| [1.2.7](FREE-CONTROLS.vi.md#cis-1-2-7) | NOT_TESTED | Đổi trạng thái repo thật cần quyết định nhóm. |
| [1.3.1](FREE-CONTROLS.vi.md#cis-1-3-1) | NOT_TESTED | Thiếu danh tính thật và owner review; không suy tổng thành viên từ public members. |
| [1.3.3](FREE-CONTROLS.vi.md#cis-1-3-3) | NOT_TESTED | Chưa có quyết định phân công vai trò và xác nhận danh sách quản trị viên. |
| [1.3.4](FREE-CONTROLS.vi.md#cis-1-3-4) | NOT_TESTED | Thay đổi yêu cầu MFA có thể ảnh hưởng thành viên, cần owner thao tác sau rà soát. |
| [1.3.6](FREE-CONTROLS.vi.md#cis-1-3-6) | NOT_TESTED | Cần email và đồng ý của các thành viên; chưa có thông tin nên không mời. |
| [1.3.7](FREE-CONTROLS.vi.md#cis-1-3-7) | MANUAL_REVIEW | Snapshot người dùng thấy một admin (hieune-ui); cần owner xác minh toàn bộ quyền kế thừa và nhóm quyết định admin thứ hai. Không tự cấp quyền. |
| [1.3.13](FREE-CONTROLS.vi.md#cis-1-3-13) | NOT_TESTED | Chưa có kênh nhận cảnh báo, ngưỡng hành vi và vận hành thực tế. |
| [1.4.1](FREE-CONTROLS.vi.md#cis-1-4-1) | NOT_TESTED | Connector không có quyền quản lý policy app. |
| [1.4.2](FREE-CONTROLS.vi.md#cis-1-4-2) | NOT_TESTED | Không tự gỡ Connector hoặc app có thể đang dùng. |
| [1.4.3](FREE-CONTROLS.vi.md#cis-1-4-3) | NOT_TESTED | Cần ảnh cấu hình cài đặt; không suy least privilege từ quyền admin của user. |
| [1.4.4](FREE-CONTROLS.vi.md#cis-1-4-4) | NOT_TESTED | Chưa có endpoint webhook thực; không tạo webhook gửi dữ liệu ra ngoài. |
| [2.1.5](FREE-CONTROLS.vi.md#cis-2-1-5) | NOT_TESTED | API quản trị Actions 403; cần owner kiểm tra UI. |
| [2.1.6](FREE-CONTROLS.vi.md#cis-2-1-6) | NOT_TESTED | Chưa có bằng chứng thực về mọi đường truy cập; repo public cho phép đọc log không phải quyền điều khiển. |
| [2.1.10](FREE-CONTROLS.vi.md#cis-2-1-10) | NOT_TESTED | Không có endpoint build webhook được nhóm chỉ định. |
| [2.1.11](FREE-CONTROLS.vi.md#cis-2-1-11) | NOT_TESTED | Thiếu username và cấu hình build platform; không tự hạ quyền. |
| [3.1.2](FREE-CONTROLS.vi.md#cis-3-1-2) | NOT_TESTED | Chưa có bộ SBOM gốc từ mọi nhà cung cấp. |
| [5.1.4](FREE-CONTROLS.vi.md#cis-5-1-4) | NOT_TESTED | Chưa có deployment target/quyền thật; CODEOWNERS chưa là enforcement. |
| [5.2.3](FREE-CONTROLS.vi.md#cis-5-2-3) | NOT_TESTED | Không có production được nhóm chỉ định; không tự triển khai cloud trả phí. |
| [5.2.4](FREE-CONTROLS.vi.md#cis-5-2-4) | NOT_TESTED | Chưa có môi trường production hoặc secret manager để kiểm chứng kết quả đăng nhập. |

## Thứ tự thao tác thủ công đề xuất

1. Owner đối chiếu People/Collaborators và quyền kế thừa; xác nhận bốn tài khoản trong snapshot có đúng thành viên nhóm. Hai tài khoản hiện Read không thể tự push. Không tự cấp Admin cho cả nhóm; mục 1.3.7 cần quyết định người quản trị thứ hai và xem ảnh hưởng.
2. Mỗi người tự bật MFA, cất recovery codes riêng; owner rà người bị ảnh hưởng trước khi bật yêu cầu MFA Organization. Không lưu mật khẩu, token hoặc recovery codes trong tài liệu công khai hoặc repository.
3. Tạo nhánh thử và áp ruleset chỉ khớp đúng nhánh thử theo hướng dẫn; kiểm tra thiếu review, commit không ký, unresolved thread, admin bypass. Không đổi rule hoặc thử trên main.
4. Rà app, webhook, quyền Actions/runner/secrets qua Settings; bổ sung ảnh/log đã che dữ liệu. HTTP 403 trong script là thiếu quyền kết nối, không chứng minh cần Enterprise.
5. Cung cấp môi trường registry/storage/production được phép và bộ SBOM/provenance của nhà cung cấp nếu muốn hoàn tất nhóm 3–5. Công cụ miễn phí không tự tạo bằng chứng cho hạ tầng chưa tồn tại.

Ảnh thuộc phần 2 của báo cáo (METHOD.vi.md); phần 3 chỉ chữ/bảng trong IMPLEMENTATION.vi.md. Chưa bổ sung ảnh Settings mới vì chưa có thao tác owner thực tế. Không dùng sơ đồ làm ảnh cấu hình giả. Kết quả cũ/ảnh cũ phải giữ nhãn run cũ.

## Giới hạn và an toàn

Không thay Settings/Rulesets, MFA, quyền thành viên, secret, main hoặc hai repo nguồn; không xóa branch/repo, không tạo release, không triển khai production, không mua gói. Mẫu ruleset là file đề xuất, chưa áp dụng. Khóa ký tạm ở cùng job chỉ chứng minh tính toàn vẹn của bundle run đó; không thay danh tính ký release production. Snapshot owner numeric ID là baseline quan sát, cần nhóm review supplier; thay đổi phải được review chứ không tự cập nhật baseline.

## Run và file xuất kết quả

Code đã kiểm tra: `f1df426fb33f05fbdf64f04d5068a6d6c97085bf`. Các run 44108703310 (Free), 44108703867 (source/container/API/SBOM), 44108703323 (Zizmor) đều SUCCESS. Đã tải và đọc artifact, xác minh fingerprint bundle bằng log của đúng run. Xem RESULTS.vi.md và [file ZIP xuất kết quả](evidence/free-controls-export.zip), hoặc JSON/CSV 48 dòng trong evidence. Các phép kiểm tra thành phần: 37 tests; zero Bandit HIGH, zero advisory trên 32 package, 32 hash wheel khớp; 20 license vẫn cần review.

## Phạm vi bản biên tập

Bản biên tập chuẩn hóa thuật ngữ, hướng dẫn và cấu trúc báo cáo; không thay số liệu kiểm tra, trạng thái tiêu chí hoặc danh tính người thực hiện. Gói `evidence/free-controls-export.zip` là bản lưu của các run đã ghi nhận, được giữ nguyên để kiểm tra hash/chữ ký. Tài liệu bên trong source snapshot phản ánh commit của lần chạy, có thể khác văn bản hiện hành. Các lần đo trước được lưu riêng trong RESULTS-HISTORY.vi.md.
