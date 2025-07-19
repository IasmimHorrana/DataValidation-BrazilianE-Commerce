# 3. Padronização de Código

Este projeto segue boas práticas de desenvolvimento em Python, com foco em código limpo, organizado e consistente. Para isso, foram configuradas ferramentas automáticas de formatação e verificação, integradas ao processo de commit com o **pre-commit**.



## 🧼 Ferramentas Utilizadas

### ✅ `black` — Formatador de código

- Formatador de código automático que segue a PEP8 e impõe um estilo consistente.

### ✅ `isort` — Organização de imports
- Organiza automaticamente os blocos de import em ordem lógica e separada por grupos.

### ✅ `flake8` — Análise de estilo e erros
- flake8 é um verificador de estilo que detecta erros comuns e más práticas no código.

### ⚙️ pyproject.toml — Configuração unificada
- As configurações das ferramentas estão centralizadas no arquivo pyproject.toml
### 🔁 .pre-commit-config.yaml — Automatização com Pre-commit
- O arquivo .pre-commit-config.yaml configura os hooks que serão executados automaticamente antes de cada commit, garantindo que o código esteja formatado e validado.
- Garanta que o .pre-commit-config.yaml esteja na raiz do projeto.

## 🚀 Configurando o Pre-commit
Após instalar as dependências com poetry, execute:
```
poetry run pre-commit install
```
Esse comando registra os hooks para serem executados automaticamente antes de cada git commit.

**Para rodar manualmente em todos os arquivos:**
```
poetry run pre-commit run --all-files
```
### 💡 Boas práticas e dicas
- Ao usar pre-commit, seu código será automaticamente formatado e validado antes de cada commit.
- Use o VS Code com extensão do Black + isort para aplicar os padrões automaticamente ao salvar.
- Evite linhas muito longas: O limite adotado é de 88 caracteres.
- Separe imports por grupo: Bibliotecas padrão, externas e internas (o isort faz isso por você).
- Nunca edite código formatado manualmente: deixe o Black cuidar disso.
- Use # noqa apenas quando necessário: evite ignorar regras do flake8 sem motivo.