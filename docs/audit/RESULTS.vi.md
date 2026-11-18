# 4. Kết quả thực nghiệm

## 4.1 Phạm vi bằng chứng

Kết quả được chia theo môi trường thực thi: GitHub Actions, kiểm tra API, workspace kiểm thử và VM VMware. Phép thử thành công chỉ chứng minh điều kiện được kiểm tra tại thời điểm đo. HTTP 403/422, field thiếu hoặc quyền nhìn thấy không đầy đủ được giữ là UNKNOWN/MANUAL_REVIEW.

## 4.2 Kiểm tra tự động

Code kiểm thử: `f9e044e7544cdee8d54512b2b6ff0ba9b173e664` trên nhánh `audit/remaining-free-integration`.

| Kiểm tra | Kết quả | Bằng chứng |
|---|---|---|
| Unit/negative tests | 71 PASS | CI và log kiểm thử |
| CodeQL Python | Zero result, 43 rule; executionSuccessful=true | SARIF của run 44252615619 |
| Webhook HTTPS | 11 PASS | HMAC, replay, event/body policy và TLS trust |
| Registry HTTPS | 23 PASS; hai phiên bản | Auth, manifest/blob/signature download và tamper rejection |
| Binary registry | Scan và package-coverage guard thành công | CI integration; không chấp nhận kết quả rỗng |
| Build execution guard | execution_allowed=true cho actor hợp lệ | Artifact integration; negative unit tests cho context không hợp lệ |
| Code change monitor | Zero finding thuộc tập mẫu kiểm tra; có yêu cầu review đường dẫn nhạy cảm | Artifact integration |
| Supplier intake | 43 đầu vào trực tiếp chưa có supplier SBOM được xác minh | evidence/supplier-intake-review.json |

| Workflow | Run | Kết quả |
|---|---|---|
| Pipeline Security Scan | [44252615595](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44252615595) | SUCCESS |
| CodeQL Python Audit | [44252615619](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44252615619) | SUCCESS |
| Pipeline Input Output | [44252615513](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44252615513) | SUCCESS |
| Remaining Free integrations | [44252615584](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44252615584) | SUCCESS |

Kết quả kiểm kê độc lập ngày 18/11/2026: 32/32 wheel hash khớp PyPI; 20 license cần review theo policy chưa phê duyệt; numeric identity của 9 action repo/owner không đổi; zero Bandit HIGH trong scripts. Các JSON tương ứng nằm trong `evidence/*review-2026-11-18.json` và `evidence/current-review-summary.json`.

## 4.3 VMware lab

| Nhóm kiểm thử | Kết quả | Nguồn |
|---|---|---|
| Supply chain | 5/5 PASS | Báo cáo JSON được cung cấp |
| Registry policy fixture | 13/13 PASS | Mô hình offline, không có IdP/MFA thật |
| Webhook HTTPS loopback | 11/11 PASS | Báo cáo JSON được cung cấp |
| Quyền triển khai OS | cisdeploy không có sudo; mode 700; nobody bị từ chối | Đầu ra terminal được cung cấp |
| Cấu hình SSH | Root login no, empty passwords no; user/cisdeploy đăng nhập lại được | Đầu ra/xác nhận của người thực nghiệm |
| Trạng thái mật khẩu | root L; user và cisdeploy P | passwd -S; không thu mật khẩu/hash |

Các báo cáo và xác nhận là bằng chứng được cung cấp từ VM, không có signed remote attestation hoặc quan sát trực tiếp của công cụ thu thập. Hai mục 5.2.3/5.2.4 có bằng chứng thành phần trong lab. Chưa kiểm production, toàn bộ service accounts hoặc chứng minh nguồn mật khẩu user; trạng thái P không xác nhận mật khẩu không mặc định. Xem [triển khai](IMPLEMENTATION.vi.md#37-triển-khai-trên-vmware) và [biên bản](evidence/vm-access-review.json).

## 4.4 Đối chiếu CIS

| Phạm vi | PARTIAL | MANUAL_REVIEW | LAB_ONLY | NOT_TESTED | Full-control PASS |
|---|---:|---:|---:|---:|---:|
| Toàn bộ 120 tiêu chí | 82 | 28 | 7 | 3 | 0 |
| 48 tiêu chí Free được lựa chọn | 34 | 14 | 0 | 0 | 0 |

Ba NOT_TESTED là 1.3.10/1.3.11/1.3.12 thuộc tính năng Enterprise, ngoài phạm vi triển khai Free. Không có mục NOT_TESTED trong nhóm 48 chỉ có nghĩa từng mục đã có bước triển khai hoặc kiểm tra; không có nghĩa cả 48 đã đáp ứng đầy đủ yêu cầu. Mỗi giới hạn được ghi trong [COVERAGE.vi.md](COVERAGE.vi.md) và [CSV](COVERAGE.csv).

Các phần còn thiếu gồm hiệu lực review/protection, phê duyệt và hồ sơ rà định kỳ, MFA bắt buộc, email mời được duyệt, supplier evidence, quyền và credential trên production. Quy trình dự thảo và mô hình offline không thay bằng chứng thực thi.

## 4.5 Truy vết

Bằng chứng gốc, SPDX, JSON/CSV và gói đã ký được giữ nguyên trong `evidence/`. Không chỉnh gói đã ký để thay nội dung lịch sử. [RESULTS-HISTORY.vi.md](RESULTS-HISTORY.vi.md) lưu các snapshot trước; [INTEGRATION.vi.md](INTEGRATION.vi.md) trình bày phép đo registry trước/sau, [CODEQL.vi.md](CODEQL.vi.md) giải thích hai cảnh báo public digest. Source/runner/package inventory có thời điểm và phạm vi riêng, không dùng số liệu cũ thay phép đo hiện hành.
