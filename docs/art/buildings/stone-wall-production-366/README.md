# Tường thành đá — ba mẫu chính

Yêu cầu hiện hành của người dùng: bỏ toàn bộ tường thành gỗ khỏi game; chỉ tập trung tường đá chân thực theo trục X, Y và góc. Không mở thư viện hình T/cross/mixedGate lớn.

Ba whole2D PNG được tạo bằng công cụ imagegen có sẵn, mỗi mẫu một call/zero retry. Khung1254, pivot627900, xuất đồng nhất runtime128/render42.3225; không crop/fit/warp/mirror/ghép ảnh. Nguồn lớn và raw/tool gốc được giữ nguyên.

- X: [ảnh gốc](../stone-wall-X-362/raw.png), [prompt](../stone-wall-X-362/prompt.txt), [receipt](../stone-wall-X-362/receipt.json).
- Y: [ảnh gốc](../stone-wall-Y-364/raw.png), [prompt](../stone-wall-Y-364/prompt.txt), [receipt](../stone-wall-Y-364/receipt.json).
- Góc: [ảnh gốc](../stone-wall-corner-365/raw.png), [prompt](../stone-wall-corner-365/prompt.txt), [receipt](../stone-wall-corner-365/receipt.json).

[Bindings](selected-bindings.json) cố định ba nguồn và runtime. X dùng chung4 mask0/1/2/3; Y dùng chung3 mask4/8/12; góc whole mask5. Các hình nối hoặc state chưa có tranh riêng dùng nativeSTONE fallback, không quay/lật/ghép PNG. Cổng giữ chức năng nhưng dùng fallback đá, không còn wings/trụ gỗ. Đây chưa phải animatedconstruction/collapse/hit hoặc toàn bộ building acceptance.

361 đã phát hiện PNG tải đủ nhưng realraster routegate chỉ cho fort nên mặc định vẽ native fallback; receipt/ảnh/original optionalmenu diagnostic HOLD giữ nguyên.368 sửa đúng routegate trước freshbuild/actualscene. Final gameplay intake và public deployment nằm trong receipt hiện hành, không suy từ packaging/ảnh nguồn.

15 payload tường/cổng gỗ và25descriptor cũ được loại khỏi active candidate và giữ byte-pinned trong retired-wood-custody cùng raw/history/rollback. Không loại resourcewood/cây/nhà khác hoặc đổi economy/simulation/path/ownership.
