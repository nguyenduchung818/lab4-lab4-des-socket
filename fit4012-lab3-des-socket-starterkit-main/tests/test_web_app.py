from app import create_app, state
from des_socket_utils import encrypt_des_cbc


def test_web_dashboard_homepage_loads():
    app = create_app()
    app.testing = True
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert "<title>DES Tool</title>" in page
    assert "Gửi bản tin" in page
    assert "Giải mã" in page


def test_web_dashboard_rejects_empty_message():
    app = create_app()
    app.testing = True
    client = app.test_client()

    response = client.post(
        "/sender/send",
        data={"host": "127.0.0.1", "port": "6000", "message": ""},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Bạn cần nhập bản tin trước khi gửi." in response.get_data(as_text=True)


def test_web_dashboard_can_decrypt_hex_payload():
    app = create_app()
    app.testing = True
    client = app.test_client()
    key, iv, ciphertext = encrypt_des_cbc(b"Xin chao FIT4012", key=b"12345678", iv=b"abcdefgh")

    response = client.post(
        "/decrypt",
        data={
            "key_hex": key.hex(),
            "iv_hex": iv.hex(),
            "ciphertext_hex": ciphertext.hex(),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert "Giải mã thủ công thành công." in page
    assert "Xin chao FIT4012" in page

