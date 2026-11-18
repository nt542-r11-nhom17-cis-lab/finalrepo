# CIS GitHub Benchmark — Lab bảo mật chuỗi cung ứng phần mềm

Thực nghiệm đánh giá theo **CIS GitHub Benchmark v1.2.0**, gồm 120 tiêu chí thuộc năm nhóm: Source Code, Build Pipelines, Dependencies, Artifacts và Deployment.

Repository: `nt542-r11-nhom17-cis-lab/finalrepo`. Nhánh thực nghiệm tổng hợp: **`audit/remaining-free-integration`**. `main` và hai repository nguồn được giữ nguyên.

**Báo cáo hoàn chỉnh:** [Báo cáo thực nghiệm CIS GitHub Benchmark](docs/report/BAO-CAO.vi.md), gồm bốn phần, danh mục và bảng đối chiếu đủ 120 tiêu chí.

## Báo cáo

| Nội dung | Tài liệu |
|---|---|
| Giới thiệu và phạm vi | [Tổng quan](docs/audit/README.vi.md) |
| Audit → Remediation → Re-audit; hình minh họa | [Phương pháp](docs/audit/METHOD.vi.md) |
| Mô hình, phân quyền, công cụ và môi trường VM | [Triển khai](docs/audit/IMPLEMENTATION.vi.md) |
| Kết quả, phiên chạy và giới hạn | [Kết quả thực nghiệm](docs/audit/RESULTS.vi.md) |
| Đối chiếu từng tiêu chí | [Bảng 120 tiêu chí](docs/audit/COVERAGE.vi.md), [CSV](docs/audit/COVERAGE.csv) |
| Thao tác kiểm tra thủ công | [Quy trình thực hành](docs/audit/PROCEDURES.vi.md) và [runbook năm nhóm](docs/audit/runbooks/GROUP-1.vi.md) |

## Kiểm tra

```bash
python3 -m unittest discover -s tests -v
python3 scripts/supply_chain_lab.py
python3 scripts/webhook_integration.py
```

Registry integration cần binary khớp SHA256 trong `config/registry-integration.lock.json`; xem [phụ lục HTTPS/registry](docs/audit/INTEGRATION.vi.md). Các báo cáo được sinh trong `reports/`. Credential và khóa riêng không được đưa vào repository.

## Workflow thực nghiệm

| Workflow | Chức năng |
|---|---|
| pipeline-io.yml | Unit tests, SAST/SCA, container, SBOM và kiểm tra chữ ký |
| pipeline-security.yml | Zizmor kiểm tra cấu hình workflow |
| remaining-integration.yml | HTTPS webhook/registry, scan binary và thu thập bằng chứng |
| codeql.yml | CodeQL Python và SARIF |

Các workflow trên chỉ thực hiện phần thực nghiệm trên nhánh audit được cho phép, có guard danh tính chạy build. Các workflow kế thừa khác phục vụ những phép thử riêng; phạm vi và giới hạn nằm trong báo cáo. CI thành công không đồng nghĩa đạt toàn bộ CIS.

## Nguồn tích hợp

- https://github.com/NT542-R11-Nhom-17-D-an/NT542.R11---Nhom-17---Do-an
- https://github.com/dtk01062006/cis-github-actions-lab

Commit nguồn và phạm vi tích hợp: [sources.json](docs/integration/sources.json), [tài liệu tích hợp](docs/integration/README.vi.md). Lịch sử và bằng chứng các lần đo được giữ để đối chiếu; kết quả lab không được suy thành tuân thủ production.
