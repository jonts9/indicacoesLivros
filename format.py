import json
import re
from collections import defaultdict

# Lê o conteúdo do arquivo indicacoes.txt
with open("indicacoes.txt", "r", encoding="utf-8") as file:
    raw_text = file.read()

# Inicialização
book_data = defaultdict(list)
current_age_group = None

# Quebra o texto em linhas
lines = raw_text.strip().splitlines()

i = 0
while i < len(lines):
    line = lines[i].strip()
    
    # Detectar nova faixa etária
    if re.match(r"^\d+-\d+ anos$", line):
        current_age_group = line
        i += 1
        continue

    # Verifica se a linha atual é um título de livro e a próxima uma URL
    if current_age_group and i + 1 < len(lines):
        title = line
        url = lines[i + 1].strip()
        if re.match(r"^https?://", url):
            book_data[current_age_group].append({
                "title": title,
                "url": url
            })
            i += 2
            continue
    i += 1

# Converter para JSON formatado
json_output = json.dumps(book_data, indent=2, ensure_ascii=False)

# Salvar em arquivo (opcional)
with open("indicacoes.json", "w", encoding="utf-8") as f:
    f.write(json_output)

# Mostrar resultado
print(json_output)
