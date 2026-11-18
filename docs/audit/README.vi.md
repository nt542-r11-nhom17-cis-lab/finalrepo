# Báo cáo thực nghiệm CIS GitHub Benchmark v1.2.0

## 1. Giới thiệu benchmark

### 1.1 Tổng quan

CIS GitHub Benchmark do Center for Internet Security phát hành, cung cấp hướng dẫn đánh giá và tăng cường bảo mật chuỗi cung ứng phần mềm sử dụng GitHub. Tài liệu được dùng trong đề tài là phiên bản 1.2.0, ngày 18/02/2026. CIS không phải Cisco. Các khuyến nghị cần được áp dụng theo đúng phiên bản, phạm vi công nghệ và điều kiện của môi trường được kiểm tra.

GitHub không chỉ lưu mã nguồn. Nền tảng còn tham gia quản lý quyền cộng tác, quy trình review, chạy pipeline, sử dụng thư viện bên ngoài, tạo sản phẩm phần mềm và triển khai. Một thay đổi thiếu kiểm soát ở bất kỳ giai đoạn nào đều có thể ảnh hưởng sản phẩm cuối cùng. Vì vậy benchmark chia nội dung thành năm nhóm: Source Code, Build Pipelines, Dependencies, Artifacts và Deployment. Năm nhóm là các phần của benchmark, không phải cách đánh số chương báo cáo môn học.

Nhóm Source Code tập trung vào truy vết thay đổi, phê duyệt, bảo vệ nhánh, quản lý repository, tài khoản và ứng dụng bên thứ ba, cùng công cụ phát hiện rủi ro trong mã. Ví dụ, có scanner nhưng người dùng vẫn có thể bypass hoặc merge khi checks thất bại thì chưa chứng minh được cơ chế ngăn thay đổi mất an toàn. Việc bảo vệ mã nguồn cần kết hợp cấu hình và thử nghiệm hành vi.

Nhóm Build Pipelines xem xét môi trường build, runner, chỉ dẫn pipeline và tính toàn vẹn. Một job chạy thành công không đồng nghĩa môi trường build an toàn: scanner có thể được cấu hình chỉ ghi nhận phát hiện mà không làm job thất bại; runner inventory không bao phủ mọi thành phần; chữ ký bằng khóa tạm chỉ minh họa khả năng ký và xác minh. Báo cáo cần chỉ rõ đối tượng, đầu vào, đầu ra và giới hạn của từng phép kiểm tra.

Nhóm Dependencies đề cập xác minh package, SBOM của nhà cung cấp, metadata build, pin phiên bản, tuổi package và chính sách sử dụng. Pin action vào SHA giúp ổn định tham chiếu nhưng không tự chứng minh commit đó có nguồn gốc đáng tin hoặc package không có lỗ hổng. Đề tài hiện không có thư viện ứng dụng bên thứ ba để kiểm thử đầy đủ, trong khi action và công cụ tải về vẫn là phụ thuộc cần quản lý.

Nhóm Artifacts xem xét ký, mã hóa, quyền truy cập, package registry và nguồn gốc sản phẩm. Cần phân biệt GitHub Actions artifacts với một package registry có chính sách upload/download và quản trị độc lập. Việc upload thành công một ZIP hoặc SBOM không chứng minh mọi release đã ký, mọi version được xác minh hoặc người tải xuống đều có quyền giải mã phù hợp.

Nhóm Deployment bao gồm quản lý cấu hình và môi trường triển khai. Tách cấu hình thành tệp riêng là bước tổ chức, chưa đủ chứng minh kiểm soát quyền độc lập. Tương tự, ZIP tái lập không chứng minh toàn bộ môi trường production tái lập. Đề tài bổ sung triển khai tự động vào thư mục sandbox tạm để kiểm chứng kỹ thuật mà không tác động hệ thống thật.

Mỗi khuyến nghị có mã, tiêu đề, phân loại đánh giá, profile, mô tả, lý do, hướng dẫn Audit và Remediation. Phân loại Automated cho biết phép đánh giá kỹ thuật có thể tự động hóa; Manual vẫn cần một phần xác minh của con người. Trong bản này có 120 tiêu chí, gồm 118 Manual và 2 Automated: 1.1.3 và 2.3.8. Việc dùng scanner không được đổi phân loại gốc trong bảng báo cáo.

Profile Level 1 và Level 2 giúp tổ chức lựa chọn mức tăng cường phù hợp; Level 2 mở rộng Level 1. Không nên lấy một số mục Level 2 đã chạy trong lab để tuyên bố đạt toàn profile. Kết quả phải trình bày từng tiêu chí, bằng chứng, giới hạn và lý do chưa thực hiện. Những trường hợp chưa có hệ thống production hoặc chưa được cấp quyền đánh giá được ghi rõ, không mặc định không áp dụng.

Trong môn Lập trình kịch bản, giá trị của đề tài nằm ở khả năng biến hướng dẫn kiểm tra thành quy trình lặp lại, lưu kết quả có cấu trúc và xử lý đúng lỗi, thiếu quyền hay thiếu bằng chứng. Đề tài chọn một phương pháp Audit–Remediation–Re-audit, dùng giao diện, script và runner từ xa để thực hiện. Các script không tự thay đổi cấu hình main. Khi có phát hiện, cần phân biệt lỗi thực thi công cụ, cấu hình chưa đáp ứng và phát hiện rủi ro thật; từ đó mới đề xuất khắc phục đúng đối tượng.

### 1.2 Nội dung benchmark

Danh mục được trích cấu trúc từ PDF người dùng cung cấp, đối chiếu đủ 120 mã, không đính kèm lại PDF công khai. Tên và trang tham chiếu nằm trong catalog.json. Hai bảng theo phân loại chính thức có STT, tên và mô tả ngắn:

- [1.2.1 Manual](MANUAL.vi.md): 118 tiêu chí.
- [1.2.2 Automated](AUTOMATED.vi.md): 2 tiêu chí.

## Cấu trúc báo cáo

| Phần | Nội dung |
|---|---|
| [2. Phương pháp](METHOD.vi.md) | Audit → Remediation → Re-audit; phân biệt Manual/Automated/Remote; hình minh họa |
| [3. Triển khai](IMPLEMENTATION.vi.md) | Môi trường, tài khoản, công cụ, CI, registry và VMware |
| [4. Kết quả](RESULTS.vi.md) | Các phép đo, workflow run, kết luận và giới hạn |
| [Đối chiếu 120 tiêu chí](COVERAGE.vi.md) | Trạng thái và bằng chứng từng mục; có bản CSV |
| [Quy trình thực hành](PROCEDURES.vi.md) | Các bước thao tác thủ công trong phạm vi Free |
| [Runbook nhóm 1](runbooks/GROUP-1.vi.md), [2](runbooks/GROUP-2.vi.md), [3](runbooks/GROUP-3.vi.md), [4](runbooks/GROUP-4.vi.md), [5](runbooks/GROUP-5.vi.md) | Audit, Remediation và Re-audit theo từng mã CIS |

## Phạm vi kết luận

Báo cáo kết hợp kiểm tra bằng công cụ và thao tác thủ công có hướng dẫn. Các công cụ, môi trường thực thi và nguồn bằng chứng được nêu trong phần triển khai. Kết quả lab, báo cáo được cung cấp và xác nhận của cá nhân được phân biệt với phép đo CI/API; không suy thành kiểm chứng production hoặc phê duyệt quy trình nhóm.
