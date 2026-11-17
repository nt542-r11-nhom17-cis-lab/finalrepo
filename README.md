# CIS GitHub Benchmark — Combined Lab

Bản gộp độc lập của hai lab, phục vụ thực hành CIS GitHub Benchmark v1.2.0. Hai repository nguồn không bị thay đổi.

## Nguồn
- https://github.com/NT542-R11-Nhom-17-D-an/NT542.R11---Nhom-17---Do-an
- https://github.com/dtk01062006/cis-github-actions-lab

Commit nguồn: [sources.json](docs/integration/sources.json).

## Workflow
| File | Chức năng | Kích hoạt |
|---|---|---|
| app-build.yml | Tạo đầu ra build mô phỏng | Push main |
| cis-scanners.yml | Gitleaks, Actionlint, Trivy | Push/PR vào main |
| pipeline-security.yml | Zizmor quét cấu hình toàn bộ workflow | Chạy thủ công |
| pipeline-io.yml | Kiểm tra input/output, SBOM runner, ký/xác minh bằng khóa lab | Chạy thủ công |
| resource-monitor.yml | Theo dõi CPU, RAM, đĩa trong tác vụ mẫu | Chạy thủ công |
| runner-check.yml | Kiểm tra runner, mạng và quét inventory package Ubuntu | Chạy thủ công |
| cis-1-1-scan.yml | Placeholder, chỉ echo; KHÔNG quét bảo mật | Chạy thủ công |

Mở **Actions → chọn workflow → Run workflow** để chạy thủ công. SBOM và chữ ký tải ở mục Artifacts của phiên chạy Pipeline Input Output; báo cáo Gitleaks được lưu ngay cả khi phát hiện secret.

## Cách đọc kết quả
- Gitleaks có thể báo FAIL vì các chuỗi credential đã tồn tại trong lịch sử repository nguồn. Đây là phát hiện bảo mật, không phải xung đột merge. Không có allowlist hoặc bỏ qua lỗi để làm xanh kiểm tra. Báo cáo Gitleaks mới dùng redaction.
- Trivy và quét runner hiện là quan sát kết quả; job xanh không chứng minh không có CVE. Xem log và phạm vi quét.
- SBOM chứa package Ubuntu của runner; chữ ký dùng khóa tạm cho thí nghiệm, chưa là quy trình ký release production.
- Workflow demo không phải bằng chứng đạt CIS.
- Settings, collaborators, branch protection, Rulesets, Secrets, CodeQL default setup và lịch sử Actions không được sao chép từ repo nguồn.

## Thay đổi chỉ trong repo tích hợp
Lần nhập đầu giữ nguyên file repo nhóm. Sau kiểm tra thực tế, bản tích hợp cố định SHA các action còn dùng tag/branch, tắt persist-credentials của checkout, bổ sung concurrency/timeouts và lưu báo cáo Gitleaks đã che secret. CODEOWNERS nguồn chỉ được lưu tham khảo, chưa kích hoạt vì chưa xác minh quyền người sở hữu mã trong repo này.

Chi tiết: [hướng dẫn tích hợp](docs/integration/README.vi.md).

## Kết quả đã chạy

Xem [bảng kết quả và liên kết từng phiên chạy](docs/integration/RESULTS.vi.md).

## Rà soát đủ 5 nhóm CIS — nhánh review

[Báo cáo và đối chiếu 120 tiêu chí](docs/audit/README.vi.md), [phương pháp Audit–Remediation](docs/audit/METHOD.vi.md), [triển khai](docs/audit/IMPLEMENTATION.vi.md). Có script API read-only và lab nhóm 3–5; các mục thiếu quyền/supplier/registry/production ghi rõ chưa kiểm chứng. Không có tuyên bố đạt toàn benchmark.
