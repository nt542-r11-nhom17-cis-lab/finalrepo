# Đợt bổ sung sau chuyển Organization

Xem [ORGANIZATION.vi.md](ORGANIZATION.vi.md), [bảng 120 mục mới nhất](COVERAGE.vi.md). Các kết quả/địa chỉ phía dưới được giữ như lịch sử; không dùng số liệu cũ thay kết quả mới.

# Đợt khắc phục mới nhất

Xem [REMEDIATION.vi.md](REMEDIATION.vi.md): credential HEAD đã bỏ, base image pin digest, container smoke test và source/image scan có ngưỡng chặn đã PASS. Số liệu/kết quả phía dưới là lịch sử review trước.

# Cập nhật đợt bổ sung toàn bộ quy trình

Xem [COMPLETE-REVIEW.vi.md](COMPLETE-REVIEW.vi.md) và [bảng 120 mục cập nhật](COVERAGE.vi.md). Đã có 120 runbook, thu thập readiness và lab bổ sung; không có tuyên bố đạt toàn benchmark. Các thống kê/kết quả phía dưới thuộc lần review trước, giữ lại để truy vết.

# Rà soát 5 nhóm CIS GitHub Benchmark v1.2.0

## Kết luận hiện trạng

Chưa đủ căn cứ kết luận đạt toàn bộ 5 nhóm. Repo trước rà soát có scanner và workflow demo chủ yếu nhóm 1–2, SBOM runner và chữ ký lab. Thiếu danh mục đầy đủ, phương pháp Audit/Remediation có đối chiếu, script GitHub API, quản trị dependency, registry và deployment thực tế. Nhánh này bổ sung phần có thể thực hiện an toàn; không thay main, quyền người dùng hoặc hai repo gốc.

| Nhóm CIS | Số tiêu chí | Trước rà soát | Bổ sung trên nhánh | Chưa chứng minh |
|---|---:|---|---|---|
| 1 Source Code | 50 | Gitleaks, SECURITY.md, scanner; placeholder CIS 1.1 | Audit API và checklist | Protection, MFA, thành viên, quyền, PR thực tế |
| 2 Build Pipelines | 33 | Build demo, Actionlint, Zizmor, runner, SBOM runner | API + lab được gọi từ workflow nhánh; báo cáo | Toàn hạ tầng build, cô lập đầy đủ, cổng chặn |
| 3 Dependencies | 12 | SHA action ở một số workflow | Khóa input first-party; policy dependency; SBOM có phạm vi | Supplier SBOM, ownership monitoring, package age, provenance tin cậy |
| 4 Artifacts | 14 | Chữ ký khóa lab | Artifact/SBOM/provenance ký; mã hóa và negative tests | Registry, MFA/SSO, phân quyền khóa, mọi version/release |
| 5 Deployment | 11 | Chưa có triển khai | Config riêng, kiểm tra hash, triển khai sandbox tự động | Production, quyền production, kiểm soát mật khẩu thực tế |

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

## 2. Phương pháp và hình minh họa

Xem [METHOD.vi.md](METHOD.vi.md): 2.1 Manual có workflow chung; 2.2 Automated; 2.3 Remote Automated/GitHub API. Tất cả hình phương pháp và vị trí ảnh thực nghiệm được tập trung tại phần 2. Sơ đồ là hình minh họa gốc, không phải screenshot kết quả.

## 3. Triển khai

Xem [IMPLEMENTATION.vi.md](IMPLEMENTATION.vi.md): mô hình, bảng phân công bốn người, triển khai Manual và Automated. Phần 3 dùng chữ/bảng và dẫn lại bằng chứng phần 2. Ba username còn thiếu không được tự đặt; không cấp quyền tài khoản khi chưa xác định người nhận.

## 4. Kết quả

- [Bảng tất cả 120 tiêu chí](COVERAGE.vi.md), [CSV](COVERAGE.csv).
- [Kết quả chạy trên nhánh](RESULTS.vi.md).
- [Chính sách dependency đề xuất](DEPENDENCIES.vi.md).
- [Checklist Audit–Remediation cho các mục được chọn](CHECKLIST.vi.md).

Bảng bao gồm cả những việc chưa làm và lý do. Trạng thái PARTIAL nghĩa là có một phần bằng chứng hoặc lab, không phải PASS. NOT_TESTED nghĩa là chưa thực hiện, không tự suy ra FAIL hay không áp dụng. MANUAL_REVIEW nghĩa là cần thêm quyền, con người hoặc bằng chứng. Chưa tiêu chí nào được tuyên bố PASS toàn diện chỉ từ chạy script.

## Những yêu cầu còn cần dữ liệu thật

Ảnh Settings/PR, ba tài khoản nhóm còn lại, minh chứng cấp quyền, registry, nhà cung cấp và production chưa có. Không thể tự bổ sung bằng chứng của hệ thống chưa tồn tại hoặc thay cấu hình main trái yêu cầu. Catalog và checklist nêu các bước cần làm tiếp.

Nguồn: CIS GitHub Benchmark v1.2.0, PDF do người dùng cung cấp; trang 2–5 (mục lục), 13–15 (phân loại/profile), trang của từng khuyến nghị trong catalog. API: https://docs.github.com/en/rest/branches/branch-protection và https://docs.github.com/en/rest/repos/rules .
