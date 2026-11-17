# Kiểm tra và bổ sung sau chuyển Organization

## Repo và giới hạn thay đổi

Repo hiện tại: `nt542-r11-nhom17-cis-lab/finalrepo`, repository ID **1461201903** không đổi. Main giữ `e052945db5b4a2bace480b5ab98446a8b82da02e`. Nhánh bổ sung: `audit/organization-controls`, phát triển từ bản khắc phục đã kiểm tra. Không thay Settings, MFA, team, thành viên, Secrets hoặc main.

Remote của bản làm việc và hook pre-push đã cập nhật sang URL Organization. Hook chỉ cho `audit/*`, tiếp tục chặn main và các repo nguồn. File config/repository-target.json ghi canonical repo ID và SHA main làm mốc đối chiếu. Các URL/snapshot lịch sử trong evidence được giữ nguyên để không làm sai bằng chứng cũ.

## Những gì Organization đã mở khóa và những gì vẫn bị chặn

`scripts/audit_organization.py` xác minh owner là Organization rồi dùng GET đọc metadata, kiểm tra 8 trường cấu hình, HTTP của membership và webhook. Không xuất billing email, username thành viên, hook URL, secret hoặc raw audit log.

Snapshot cục bộ cho thấy:

| Nhóm kiểm tra | Kết quả |
|---|---|
| Repo thuộc Organization | Đã xác nhận |
| MFA bắt buộc | Trường không được trả; UNKNOWN, không suy ra disabled |
| Quyền nền/create/delete/team/visibility | Trường bị lọc hoặc không có; UNKNOWN |
| Verified flag | `is_verified=false`: phát hiện cấu hình, cần domain thật để xác minh |
| Self membership | HTTP 403; chưa chứng minh token có quyền đọc tổ chức |
| Danh sách thành viên | API-visible page có 0 mục; KHÔNG kết luận tổ chức không có thành viên/admin |
| Webhooks | HTTP 404; KHÔNG kết luận không có webhook |
| Classic protection | HTTP 403 ở lần kiểm tra; chưa xác minh yêu cầu review/checks |

Repo admin và organization-settings visibility là hai quyền khác nhau. Tạo Organization không tự bật MFA, verified domain, SSH CA, IP allow list hoặc các chính sách CIS. Một số tính năng phụ thuộc gói GitHub/IdP và điều kiện hệ thống.

## Bổ sung triển khai thực tế

| Nội dung | Triển khai | Kết quả local | Giới hạn |
|---|---|---|---|
| Audit tổ chức | GET-only, CSV/JSON và kiểm thử missing/null/403 | 8 phép kiểm tra thành phần; 6 unit tests mới | 7 trường UNKNOWN; không thay settings |
| SAST Python | Bandit 1.9.4, quét scripts/examples/database_config.py, ngưỡng HIGH | 0 HIGH | Không tuyên bố không có LOW/MEDIUM hay mọi loại lỗ hổng |
| Dependency scan | pip-audit 2.10.1 với lock và require-hashes | Không có lỗ hổng đã biết được báo | Scanner toolchain, không phải supplier/app toàn tổ chức |
| Khóa toolchain | 32 package direct/transitive pin version và wheel SHA256 | 32/32 khớp metadata PyPI | Python 3.12 / Linux x86_64; hash không thay trust root/chữ ký supplier |
| License và tuổi package | Metadata PyPI + chính sách đề xuất | 20 package cần manual review | Chính sách chưa được Organization phê duyệt; wheel upload age không tự là tuổi phiên bản gốc |
| Bảo vệ main ở bản làm việc | Hook canonical Organization URL + unit tests | Chặn main, cho audit/* | Không phải server-side branch protection |

Workflow pipeline-io.yml của nhánh thực thi kiểm tra source/container, SAST/SCA/toolchain, Audit API/Organization, lab và artifacts. Zizmor kiểm tra cấu hình workflow. Bằng chứng remote, commit và ảnh được ghi sau khi chạy thực tế; không đánh dấu đã chạy trước khi xác nhận.

## Các bước thủ công cần chủ Organization để hoàn tất kiểm chứng

1. Organization **Settings → Member privileges**: ghi nhận Base permissions, repository creation/deletion/visibility và team creation; chụp ảnh có tên org, thời điểm. Chưa áp dụng thay đổi nếu có nguy cơ khóa người dùng hoặc ảnh hưởng quy trình main.
2. **Settings → Authentication security**: xác minh tài khoản owner đã có MFA và recovery, sau đó mới xem xét yêu cầu MFA cho mọi thành viên. Không bật từ script khi chưa kiểm tra recovery.
3. **Settings → Verified & approved domains**: cần tên miền nhóm thực sự sở hữu và quyền DNS để xác minh. Không dùng domain trường học/công ty khi không được ủy quyền.
4. **People/Teams**: cần ba username còn lại và vai trò đã thống nhất; không tự mời hoặc cấp admin cho tài khoản đoán được từ commit.
5. **Settings → GitHub Apps/Installed GitHub Apps**: kiểm tra app được phê duyệt, repo selection và quyền đọc Organization. Kết nối hiện đọc repo nhưng không đủ bằng chứng quản trị tổ chức; không tự mở rộng quyền.
6. **Repo Settings → Rules/Branches**: cần evidence cấu hình và kiểm thử trên nhánh lab riêng. Đợt này không bật protection của main hoặc merge thay đổi.

Ảnh bằng chứng đặt tại phần 2, METHOD.vi.md. Phần 3 mô tả/bảng trong IMPLEMENTATION.vi.md. Những trường hợp chưa có screenshot/dữ liệu thật vẫn được ghi rõ trong bảng 120 tiêu chí.

## Những phần không được biến thành PASS bằng mô phỏng

Registry/IdP/production/supplier thực tế vẫn chưa được cung cấp. Credential cũ còn trong lịch sử, cần xác minh/thu hồi nếu từng dùng thật; không rewrite main. Các package/action dưới 60 ngày và license chưa xác định vẫn là findings/manual review, không nới policy chỉ để làm xanh.

## Khắc phục độ bao phủ dependency audit

Lần chạy đầu c22d271 thành công nhưng report dependency chỉ liệt kê 30/32 package; pip và packaging không xuất hiện trong chế độ resolver đó. Đã kiểm tra lại bằng chế độ đọc trực tiếp lock fully-pinned/hashed (`--require-hashes --disable-pip --strict`), đủ 32/32 và 0 advisory. `--disable-pip` chỉ bỏ bước tạo môi trường resolver nội bộ, không tắt truy vấn lỗ hổng. Bước install trước đó vẫn dùng require-hashes; metadata wheel được đối chiếu PyPI độc lập. Thêm verify_dependency_coverage.py để bắt buộc tên và version trong báo cáo khớp toàn bộ lock, không có package skipped và không có advisory; báo cáo thiếu package sẽ fail. Thêm bốn regression tests (tổng 21). Kết quả remote sau sửa được ghi riêng.
