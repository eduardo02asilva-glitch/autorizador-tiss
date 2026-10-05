import time
import requests

BASE_URL = "http://127.0.0.1:8000"

def obter_token_bot():
    """Realiza o login do sistema/bot para obter o token JWT."""
    payload = {
        "username": "medico@clinica.com",
        "password": "123456"
    }
    response = requests.post(
        f"{BASE_URL}/auth/login", 
        data=payload
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("❌ Falha na autenticação do Robô TISS:", response.text)
        return None

def processar_solicitacoes_pendentes():
    """Processa as solicitações TISS pendentes."""
    token = obter_token_bot()
    if not token:
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 1. Buscar solicitações
    res = requests.get(f"{BASE_URL}/solicitacoes/", headers=headers)
    if res.status_code != 200:
        print("❌ Erro ao listar solicitações:", res.text)
        return

    solicitacoes = res.json()
    pendentes = [s for s in solicitacoes if s["status"] == "pendente"]

    print(f"\n🤖 Robô TISS: Encontradas {len(pendentes)} solicitações pendentes.")

    for item in pendentes:
        sol_id = item["id"]
        procedimento = item["procedimento"]
        print(f"⏳ Processando Guia #{sol_id} - Procedimento: {procedimento}...")
        
        # Simula o tempo de validação com o portal do convénio TISS
        time.sleep(2)

        # Regra simples de exemplo: se o procedimento contiver "Negado", nega; caso contrário, autoriza
        novo_status = "negada" if "negado" in procedimento.lower() else "autorizada"

        # 2. Atualizar o status na API
        patch_res = requests.patch(
            f"{BASE_URL}/solicitacoes/{sol_id}/status",
            json={"status": novo_status},
            headers=headers
        )

        if patch_res.status_code == 200:
            print(f"✅ Guia #{sol_id} atualizada com sucesso para: {novo_status.upper()}")
        else:
            print(f"❌ Erro ao atualizar Guia #{sol_id}:", patch_res.text)

if __name__ == "__main__":
    print("🚀 Iniciando execução do Robô Autorizador TISS...")
    processar_solicitacoes_pendentes()