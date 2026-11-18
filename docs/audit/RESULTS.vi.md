# Bổ sung phần chưa triển khai của 48 mục Free

Đợt này tập trung đúng 12 mục NOT_TESTED còn lại, không làm lại các mục đã có bằng chứng và không triển khai Enterprise. Đã thêm guard quyền chạy build, monitor thay đổi mã, collector GET-only cho 12 mục, ledger supplier và host preflight chỉ đọc. Kết quả: **32 PARTIAL, 14 MANUAL_REVIEW, 2 NOT_TESTED trong 48 mục**. Hai NOT_TESTED là 5.2.3/5.2.4, chưa có production target; không giả lập thành đã đạt. Toàn bảng: **80 PARTIAL, 28 MANUAL_REVIEW, 7 LAB_ONLY, 5 NOT_TESTED; full-control PASS=0**.

Chi tiết bằng chứng/giới hạn: [PENDING-FREE.vi.md](PENDING-FREE.vi.md). Các phần dưới là snapshot đợt trước.

---

# Kết quả bổ sung ngày 18/11/2026

Đã lưu ba báo cáo do người dùng chạy trên VMware: **29/29 kiểm tra lab PASS** (5 supply chain, 13 registry mô phỏng, 11 webhook HTTPS). Đây là bằng chứng người dùng cung cấp, chưa có attestation thực thi từ xa. GET API mới: một repo, bốn tài khoản nhìn thấy (1 Admin, 2 Write, 1 Read), tám nhánh và zero fork nhìn thấy; không đổi quyền hoặc xóa tài nguyên.

Re-audit trong workspace độc lập: **58 unit tests, 34 phép thử HTTPS PASS**, 32/32 hash wheel khớp PyPI, 9/9 action owner không đổi, zero Bandit HIGH. Hai mươi license còn cần review; không tự duyệt policy nhóm.

Đã lưu SBOM GitHub native và đối chiếu ảnh/xác nhận Settings. Ba mục ứng dụng 1.4.1–1.4.3 có bằng chứng thành phần, chuyển NOT_TESTED → PARTIAL. Tổng hiện hành: **75 PARTIAL, 23 MANUAL_REVIEW, 7 LAB_ONLY, 15 NOT_TESTED**. Trong 48 mục Free ban đầu: **27 PARTIAL, 9 MANUAL_REVIEW, 12 NOT_TESTED; zero full-control PASS**. Đây không phải chỉ còn 12 mục để hoàn tất: mọi mục PARTIAL vẫn có giới hạn.

Chi tiết và công việc còn lại: [CURRENT-REVIEW.vi.md](CURRENT-REVIEW.vi.md), [bảng 48 mục](REMAINING-FREE.vi.md). Các snapshot đợt trước bên dưới giữ số liệu của chính đợt đó.

---

# Cập nhật CodeQL Python

Đã đối chiếu SARIF trước/sau: hai cảnh báo do public digest bị heuristic nhận diện là secret → zero result với cùng 43 rule. Code `1ce411f`, run 44213133290. Có 52 regression tests, gồm kiểm tra vật liệu ký không xuất ra file/log. Chi tiết và giới hạn: [CODEQL.vi.md](CODEQL.vi.md). Mục 1.5.4 vẫn PARTIAL; số liệu đợt registry bên dưới giữ đúng snapshot của đợt đó.

# Kết quả hiện hành — kiểm thử HTTPS và registry source-build

Nhánh `audit/remaining-free-integration`; code kiểm tra `545c3a2ad044fa1292712b1c00bcb7244943fbbe`. Main vẫn `e052945db5b4a2bace480b5ab98446a8b82da02e`. Không đổi lịch sử, quyền hoặc Settings.

| Kiểm tra | Kết quả | Bằng chứng |
|---|---|---|
| Unit tests | 51 PASS | Log CI |
| Webhook HTTPS | 11 PASS | HMAC, replay, event/body policy và TLS trust negative tests |
| Registry HTTPS | 23 PASS | Auth, hai phiên bản, manifest/blob/signature download và tamper rejection |
| Native registry binary scan | 104 package; tám HIGH trước → zero HIGH/CRITICAL sau | Rootfs scan và coverage guard; không dùng output rỗng |
| Registry build | Pin source commit, Go 1.27.4, module locks và output SHA; mod verify thành công | config/registry-integration.lock.json, registry-source/go.mod/go.sum |
| Source SAST/SCA | Zero Bandit HIGH; 32/32 Python packages, zero advisory đã biết | Security artifact đã tải đọc |
| Current source secret scan | Zero finding | Không suy lịch sử main đã sạch |
| Workflow scan | SUCCESS | Zizmor |
| Settings và deployment | Không thay đổi | Registry/receiver chỉ ở loopback, dừng và xóa dữ liệu tạm sau test |

Run integration [44130146471](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44130146471), source/container [44130146389](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44130146389), workflow scan [44130148225](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44130148225) đều SUCCESS. Baseline [44127179185](https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/actions/runs/44127179185) thất bại đúng ngưỡng với tám HIGH; giữ làm bằng chứng trước khắc phục.

Xem [JSON kết quả](evidence/remaining-integration-summary.json), [CSV 34 phép thử HTTPS](evidence/remaining-integration-checks.csv), [mô tả triển khai và giới hạn](INTEGRATION.vi.md). Gói ZIP đã ký của đợt trước được giữ nguyên, không thay bằng snapshot mới hoặc chỉnh chữ ký.

Toàn bộ 120 tiêu chí: **72 PARTIAL, 23 MANUAL_REVIEW, 7 LAB_ONLY, 18 NOT_TESTED; zero full-control PASS**. Trong 48 mục hướng Free ban đầu: **24 PARTIAL, 9 MANUAL_REVIEW, 15 NOT_TESTED**. Mười tám NOT_TESTED toàn bảng gồm 15 mục hướng Free và ba mục tính năng Enterprise. Các mục PARTIAL cũng còn giới hạn/phạm vi cần hoàn thiện; kết quả thành phần không phải chứng nhận đạt CIS.

Các số liệu cũ thuộc từng đợt đo được lưu ở [RESULTS-HISTORY.vi.md](RESULTS-HISTORY.vi.md).
