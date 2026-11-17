# Các mục chọn vì Audit có thể thực hiện rõ trong lab

| CIS | Audit | Remediation được đề xuất | Re-audit/bằng chứng | Đã thực hiện đến đâu |
|---|---|---|---|---|
| 1.1.3 | Đọc yêu cầu review và số approval | Yêu cầu hai approval theo Audit, kiểm chứng danh tính/xác thực mạnh | PR thiếu review bị chặn, đủ review và checks mới merge được | API read-only; chưa đổi main |
| 1.1.4 | Đọc dismiss-stale | Bật hủy phê duyệt cũ | PR đã review nhận commit mới phải review lại | API read-only; chưa thử PR |
| 1.1.9 | Xác định required checks | Bắt buộc checks hợp lệ và xem bypass | PR có check thất bại bị chặn | API read-only; cần Settings |
| 1.1.16 | Kiểm tra force push và bypass | Cấm force push theo chính sách | Thử trên nhánh lab được bảo vệ, không main | Chưa đổi quy tắc repository |
| 1.1.17 | Kiểm tra deletion và bypass | Cấm xóa nhánh được bảo vệ | Thử với nhánh disposable, không xóa main | Chưa đổi quy tắc repository |
| 1.1.20 | Xác định default branch và quy tắc có hiệu lực | Áp dụng quy tắc bảo vệ | Đối chiếu classic/rulesets và hành vi | API 403 không kết luận FAIL |
| 1.2.1 | Đọc SECURITY.md của repo public | Bổ sung kênh liên hệ riêng tư cụ thể | Đọc policy và thử luồng báo cáo theo quyền | File đã có; kênh chưa được nhóm chốt |
| 2.3.1 | Xem build steps trong YAML | Đưa bước thủ công còn thiếu vào code | Đối chiếu mã với run | Có bằng chứng pipeline lab |
| 2.3.2 | Kiểm tra input/output các stage | Khai báo và kiểm tra đầu ra | So byte, hash và dữ liệu artifact | Demo input/output đã có |
| 2.4.2 | Kiểm kê dependency và pin | Lock phiên bản/hash xác minh | So input với lock | First-party lock, action SHA; chưa đủ mọi công cụ |
| 2.4.4 | Build cùng input nhiều lần | Loại yếu tố không xác định | Hai ZIP giống byte | PASS phép thử lab, không phải toàn tiêu chí |
| 2.4.5/.6 | Tạo SBOM và kiểm chữ ký | Sinh/ký SBOM mỗi build | Verify gốc, từ chối bản sửa | Lab, chưa root tin cậy production |
| 3.1.7 | Đọc phiên bản/hash/nguồn | Pin verified versions | So lock và review provenance | Một phần; chưa xác minh mọi supplier |
| 4.1.1 | Kiểm artifact được pipeline ký | Ký bằng danh tính được quản lý | Verify và negative test | Khóa tạm lab |
| 4.1.2 | Kiểm mã hóa trước phân phối | Thiết lập mã hóa và xác thực | Verify ciphertext trước giải mã; roundtrip | Demo; plaintext vẫn lưu cho mục đích học |
| 4.1.3 | Xác định người/nền tảng giữ khóa | Giới hạn quyền giải mã, quản lý vòng đời khóa | Kiểm thử người không quyền không giải mã được | Chỉ khóa tạm trong thư mục private; chưa quản trị production |
| 4.4.1 | Kiểm thông tin nguồn gốc | Gắn repo, SHA, run ID và config hash | Verify provenance đã ký | Lab provenance, không tuyên bố SLSA |
| 5.1.1 | Xác định mức tách biệt cấu hình | Tách theo kiến trúc/quyền phù hợp | Review quyền và vị trí quản lý | Tệp riêng cùng repo; chưa đủ kết luận |
| 5.1.6/.7 | Kiểm config trước sử dụng | Xác minh manifest và pin phiên bản | Hash mismatch phải từ chối | Local lock; chưa signer production |
| 5.2.1 | Theo dõi triển khai | Mã hóa quy trình triển khai | Workflow thực thi và smoke test | Triển khai thư mục tạm |
| 5.2.2 | Kiểm tái lập môi trường | Khóa môi trường và config | Tái tạo môi trường độc lập | ZIP tái lập chưa chứng minh môi trường tái lập |
