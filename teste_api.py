import requests

BASE_URL = "http://127.0.0.1:5000/api"

def print_resposta(nome, resp):
    print(f"\n--- {nome} ---")
    print(f"Status: {resp.status_code}")
    print(resp.json())

# 1. Health check
resp = requests.get(f"{BASE_URL}/health")
print_resposta("Health check", resp)

# 2. Registrar paciente
resp = requests.post(f"{BASE_URL}/auth/registro", json={
    "email": "paciente3@teste.com",
    "senha": "123456",
    "tipo": "paciente",
    "nome_completo": "Maria Teste"
})
print_resposta("Registro paciente", resp)

# 3. Registrar profissional
resp = requests.post(f"{BASE_URL}/auth/registro", json={
    "email": "psico3@teste.com",
    "senha": "123456",
    "tipo": "profissional",
    "nome_completo": "Dr. Joao",
    "crp": "06/11111"
})
print_resposta("Registro profissional", resp)

# 4. Login paciente
resp = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "paciente3@teste.com",
    "senha": "123456"
})
print_resposta("Login paciente", resp)
token_paciente = resp.json()["access_token"]
headers_paciente = {"Authorization": f"Bearer {token_paciente}"}

# 5. Login profissional
resp = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "psico3@teste.com",
    "senha": "123456"
})
print_resposta("Login profissional", resp)
token_profissional = resp.json()["access_token"]
headers_profissional = {"Authorization": f"Bearer {token_profissional}"}

# 6. Profissional pega o PRÓPRIO id (rota nova que você vai adicionar)
resp = requests.get(f"{BASE_URL}/profissionais/perfil", headers=headers_profissional)
print_resposta("Profissional consulta o próprio perfil", resp)
profissional_id = resp.json()["id"]

# 7. Agendar consulta (agora usando o profissional_id correto)
resp = requests.post(f"{BASE_URL}/consultas", json={
    "profissional_id": profissional_id,
    "data_hora": "2026-10-15T14:00:00"
}, headers=headers_paciente)
print_resposta("Agendar consulta", resp)
consulta_id = resp.json().get("consulta_id")

# 8. Paciente lista consultas
resp = requests.get(f"{BASE_URL}/consultas", headers=headers_paciente)
print_resposta("Paciente lista consultas", resp)

# 9. Profissional confirma consulta
resp = requests.patch(f"{BASE_URL}/consultas/{consulta_id}/status", json={
    "status": "confirmada"
}, headers=headers_profissional)
print_resposta("Profissional confirma consulta", resp)

# 10. Paciente tenta confirmar (deve dar 403)
resp = requests.patch(f"{BASE_URL}/consultas/{consulta_id}/status", json={
    "status": "confirmada"
}, headers=headers_paciente)
print_resposta("Paciente tenta confirmar (deve dar 403)", resp)