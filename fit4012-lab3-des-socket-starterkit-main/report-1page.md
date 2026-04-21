# Report 1 page - Lab 3

## Thong tin nhom
- Thanh vien 1: Sinh vien 1 - MSSV: CHUA_CAP_NHAT
- Thanh vien 2: Sinh vien 2 - MSSV: CHUA_CAP_NHAT

## Muc tieu
Bai lab xay dung he thong Sender/Receiver truyen ban tin qua TCP socket, trong do du lieu duoc ma hoa bang DES-CBC. Muc tieu ky thuat la hieu ro vai tro cua DES key 8 byte, IV 8 byte, padding PKCS#7 va header do dai 4 byte de Receiver biet can doc bao nhieu ciphertext. Muc tieu kiem thu la xac nhan he thong gui nhan dung o local, kiem tra tinh dung dan cua packet, va co negative test cho truong hop sai key va bi sua doi ciphertext. Muc tieu bao mat la nhan dien day chi la mo hinh hoc tap, khong phai giao thuc an toan de dua vao thuc te.

## Phan cong thuc hien
Thanh vien 1 tap trung vao sender, tao key/IV, goi `encrypt_des_cbc()` va `build_packet()` de gui dung thu tu `key + iv + length + ciphertext`. Thanh vien 2 tap trung vao receiver, nhan du lieu bang `recv_exact()`, tach header, giai ma va in ban ro. Ca nhom cung bo sung bo test trong `tests/`, viet threat model, tong hop log demo va hoan thien cac file nop bai.

## Cach lam
File `des_socket_utils.py` cung cap cac ham `pad()`, `unpad()`, ma hoa/giai ma DES-CBC, dong goi header va nhan du lieu du so byte. `sender.py` doc message tu bien moi truong hoac ban phim, ma hoa ban tin, sau do mo ket noi TCP den Receiver va gui toan bo packet. `receiver.py` lang nghe mot ket noi, nhan 20 byte header gom key, IV va do dai ciphertext, sau do nhan phan du lieu con lai va giai ma de khoi phuc ban tin goc. Nhom viet 5 test gom roundtrip padding, kiem tra header, integration local sender/receiver, negative test tamper va negative test wrong key.

## Ket qua
He thong dat duoc luong gui/nhan co ban theo yeu cau de bai. Sender in ra thong bao gui thanh cong cung `Key`, `IV`, `Ciphertext`; Receiver in ra ban tin da giai ma. Bo test tu dong bao phu ca happy path lan negative path de giam nguy co nop bai nhung sai contract packet. Log chay that duoc luu trong thu muc `logs/` de minh chung cho ca gui va nhan.

## Ket luan
Qua bai lab, nhom hieu ro hon cach ket hop ma hoa doi xung voi socket TCP va vi sao can dong khung packet ro rang de ben nhan phan tach du lieu chinh xac. Bai lab cung cho thay DES la thuat toan cu, va viec gui key/IV dang plaintext tren cung ket noi la mot diem yeu rat lon. Huong cai tien trong thuc te la dung AES-GCM hoac TLS, ket hop xac thuc thong diep va co co che trao doi khoa an toan.
