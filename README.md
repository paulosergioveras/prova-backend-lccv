# Prova back-end para o LCCV edital nº 003/2026

## Instalação

Siga os passos abaixo para rodar o projeto localmente:

```bash
# 1. Clone o repositório
git clone https://github.com/paulosergioveras/prova-backend-lccv.git
cd prova-backend-lccv

# 2. Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Criar arquivo .env a partir do modelo
cp .env.example .env          # macOS/Linux
copy .env.example .env        # Windows

# 5. (Opcional) Edite o .env para ajustar variáveis de ambiente, 
#    como SECRET_KEY, DEBUG, DATABASE_URL, etc.

# 6. Rodar migrações do banco de dados
python manage.py migrate

# 7. Criar superusuário
python manage.py createsuperuser

# 8. Iniciar o servidor de desenvolvimento
python manage.py runserver

## Documentação da API

Swagger UI: http://localhost:8000/swagger/