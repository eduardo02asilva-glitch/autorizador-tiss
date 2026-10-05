def test_registrar_usuario(client):
    # 1. Cria a clínica obrigatória primeiro
    res_clinica = client.post("/clinicas/", json={"nome_fantasia": "Clínica Teste", "cnpj": "12345678000199"})
    assert res_clinica.status_code == 201
    clinica_id = res_clinica.json()["id"]

    # 2. Testa o registro do usuário
    res_user = client.post("/auth/registrar", json={
        "clinica_id": clinica_id,
        "nome": "Dr. Teste",
        "email": "drteste@clinica.com",
        "senha": "senha_segura_123"
    })
    assert res_user.status_code == 201
    data = res_user.json()
    assert data["email"] == "drteste@clinica.com"
    assert "senha" not in data  # Garante que a senha não é exposta na resposta

def test_login_usuario(client):
    # Setup: cria clínica e usuário
    res_clinica = client.post("/clinicas/", json={"nome_fantasia": "Clínica Teste", "cnpj": "12345678000199"})
    clinica_id = res_clinica.json()["id"]

    client.post("/auth/registrar", json={
        "clinica_id": clinica_id,
        "nome": "Dr. Teste",
        "email": "drteste@clinica.com",
        "senha": "senha_segura_123"
    })

    # Teste de Login Sucesso
    res_login = client.post("/auth/login", data={
        "username": "drteste@clinica.com",
        "password": "senha_segura_123"
    })
    assert res_login.status_code == 200
    token_data = res_login.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # Teste de Login Com Senha Incorreta
    res_erro = client.post("/auth/login", data={
        "username": "drteste@clinica.com",
        "password": "senha_errada"
    })
    assert res_erro.status_code == 401