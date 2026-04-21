# Peer Review Response

## Thong tin nhom
- Thanh vien 1: Sinh vien 1 - MSSV: CHUA_CAP_NHAT
- Thanh vien 2: Sinh vien 2 - MSSV: CHUA_CAP_NHAT

## Thanh vien 1 gop y cho thanh vien 2
Phan Receiver da dung luong nhan `header -> ciphertext`, nhung can nhan manh hon viec kiem soat timeout va ghi log de luc demo de doi chieu output. Ngoai ra, can giai thich ro tai sao phai dung `recv_exact()` thay vi goi `recv()` mot lan tren socket stream.

## Thanh vien 2 gop y cho thanh vien 1
Phan Sender da gui dung packet contract, nhung can bo sung mo ta ro hon trong README ve thu tu `key + iv + length + ciphertext` va cach lay message tu bien moi truong de de test tu dong. Nen doi chieu them output `Key`, `IV`, `Ciphertext` voi log thuc te de tranh sai dinh dang khi demo.

## Nhom da sua gi sau gop y
Nhom da cap nhat README de mo ta ro hon phan chia vai tro, contract packet va cach chay tren PowerShell. Cac file bao cao va threat model duoc viet lai day du thay cho placeholder de khop yeu cau nop bai. Nhom giu bo 5 test bao gom ca integration va negative cases de verify luong sender/receiver, dong thoi bo sung log demo trong thu muc `logs/` de co minh chung khi nop bai.
