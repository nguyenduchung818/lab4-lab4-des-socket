# Threat Model - Lab 3

## Thong tin nhom
- Thanh vien 1: Sinh vien 1 - MSSV: CHUA_CAP_NHAT
- Thanh vien 2: Sinh vien 2 - MSSV: CHUA_CAP_NHAT

## Assets
- Noi dung ban ro ma Sender gui cho Receiver.
- DES key 8 byte va IV 8 byte dung cho phien truyen hien tai.
- Tinh toan ven cua ciphertext va header do dai.
- Tinh san sang cua Receiver trong luc dang lang nghe ket noi.
- Log demo va ket qua giai ma dung cua he thong.

## Attacker model
Ke tan cong duoc gia dinh co kha nang nghe len luong TCP trong mang noi bo hoc tap, sua doi goi tin tren duong truyen, hoac gui packet loi/co y doc hai den Receiver. Ke tan cong khong can co quyen truy cap vao may chu noi bo cua nhom, nhung co the quan sat hoac chen du lieu neu mang khong duoc bao ve. Trong pham vi bai lab, attacker khong bao gom doi thu co kha nang pha khoa DES bang tan cong quy mo lon trong thoi gian ngan, nhung van co the loi dung thiet ke giao thuc yeu.

## Threats
- Lo thong tin bi mat: key va IV duoc gui plaintext tren cung ket noi nen nguoi nghe len co the giai ma ngay ciphertext.
- Sua doi du lieu: attacker co the thay doi header hoac ciphertext lam Receiver giai ma sai, loi padding, hoac in ra noi dung rac.
- Phat lai goi tin: packet cu co the bi gui lai do giao thuc khong co nonce, timestamp hay session identifier.
- Tu choi dich vu muc nhe: attacker gui do dai khong hop le hoac mo ket noi roi khong gui du du lieu, lam Receiver cho het timeout.
- Nham lan ve muc do an toan: nguoi dung co the tuong nham day la mo hinh bao mat san sang trien khai do co ma hoa DES.

## Mitigations
- Trong bai lab, chi demo tren may ca nhan/VM/mang noi bo va khong dung du lieu that de giam anh huong neu key bi lo.
- Kiem tra kich thuoc key, IV, ciphertext va xac thuc padding trong qua trinh giai ma de phat hien du lieu bat thuong som hon.
- Dong goi packet ro rang voi `length header` va dung `recv_exact()` de tranh doc thieu/du du lieu tren socket stream.
- Dat timeout cho socket Receiver de han che truong hop ket noi treo qua lau.
- Neu dua vao he thong that, can thay DES bang AES-GCM hoac dat kenh TLS de co bao mat, xac thuc va bao ve tinh toan ven.

## Residual risks
Du da co timeout va check padding, thiet ke hien tai van khong co xac thuc thong diep, khong co trao doi khoa an toan, va van de lo key/IV tren duong truyen chua duoc giai quyet. Vi vay he thong chi phu hop de hoc quy trinh ma hoa/giai ma va dong goi packet, khong phu hop cho du lieu nhay cam trong moi truong thuc te.
