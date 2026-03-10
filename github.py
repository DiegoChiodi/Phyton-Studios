import os

email = "dchiodigoncalves@gmail.com"
name = 'DiegoChiodi'

print("✉️ Configurando email...")
command_1 = f"git config user.email \"{email}\""
os.system(command_1)
print("🧑‍🦱 Configurando nome de usuário...")
command_2 = f"git config user.email \"{name}\""
os.system(command_2)

print("🆕 Adicionando modificações...")
command_3 = "git add *"
os.system(command_3)

m_commit = input("Digite o nome do commit")
while(len(m_commit) < 5):
    print("⚠️ Mensagem muito pequena para um commit")
    m_commit = input("Digite o nome do commit novamente")



print("🆗 Commitando...")
command_4 = f"git commit -m \"{m_commit}\""
os.system(command_4)

print("🛜 Enviando projeto ao GitHub")
command_5 = "git push"
os.system(command_5)