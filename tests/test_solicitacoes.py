def test_fluxo_completo_solicitacao_tiss(client):
    # 1. Cadastra Clínica
    c_res = client.post("/clinicas/", json={"nome_fantasia": "Hospital Alfa", "cnpj": "11222333000144"})
    clinica_id = c_res.json()["id"]

    # 2. Cadastra Paciente
    p_res = client.post("/pacientes/", json={
        "clinica_id": clinica_id,
        "nome": "Paciente Teste",
        "cpf": "11122233344",
        "numero_carteira": "998877",
        "convenio": "Bradesco Saúde"
    })
    paciente_id = p_res.json()["id"]

    # 3. Registra e autentica Usuário
    client.post("/auth/registrar", json={
        "clinica_id": clinica_id,
        "nome": "Atendente",
        "email": "atendente@alfa.com",
        "senha": "123"
    })
    token = client.post("/auth/login", data={"username": "atendente@alfa.com", "password": "123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 4. Tenta criar solicitação SEM Token (deve falhar com 401)
    res_sem_auth = client.post("/solicitacoes/", json={
        "clinica_id": clinica_id,
        "paciente_id": paciente_id,
        "procedimento": "Radiografia"
    })
    assert res_sem_auth.status_code == 401

    # 5. Criar solicitação COM Token (deve retornar 201 com status pendente)
    res_sol = client.post("/solicitacoes/", json={
        "clinica_id": clinica_id,
        "paciente_id": paciente_id,
        "procedimento": "Radiografia de Tórax"
    }, headers=headers)
    
    assert res_sol.status_code == 201
    sol_id = res_sol.json()["id"]
    assert res_sol.json()["status"] == "pendente"

    # 6. Atualizar status para Autorizada
    res_patch = client.patch(f"/solicitacoes/{sol_id}/status", json={"status": "autorizada"}, headers=headers)
    assert res_patch.status_code == 200
    assert res_patch.json()["status"] == "autorizada"