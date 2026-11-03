import pandas as pd

# Lista representativa com marcas consolidadas em calçados (esportivo, casual, feminino, infantil, botas e conforto)
marcas = [
    # Esportivo / Running / Sneaker
    "Nike", "Adidas", "Olympikus", "Mizuno", "Asics", "Puma", "Under Armour", "Fila", "New Balance", 
    "Skechers", "Reebok", "Converse", "Vans", "Rainha", "Topper", "Penalty", "Umbro", "Mormaii", "Diadora",
    # Feminino / Casual / Moda
    "Moleca", "Vizzano", "Beira Rio", "Modare", "Dakota", "Kolosh", "Mississipi", "Campesi", "Via Marte", 
    "Ramarim", "Comfortflex", "Usaflex", "Piccadilly", "Bottero", "Cravo e Canela", "Tanara", "Santa Lolla",
    "Arezzo", "Anacapri", "Schutz", "Luiza Barcelos", "Capodarte", "Jorge Bischoff", "Loucos e Santos",
    # Masculino / Casual / Social / Botas
    "Pegada", "Democrata", "Ferracini", "Rafarillo", "West Coast", "Macboot", "Bull Terrier", "Caterpillar",
    "Timberland", "Kildare", "Samello", "CNS", "Sergio K", "Osklen", "Reserva",
    # Sandálias / Chinelos / Verão
    "Havaianas", "Ipanema", "Rider", "Cartago", "Grendha", "Zaxy", "Melissa", "Kenner", "Crocs", "Birkenstock",
    # Infantil
    "Kidy", "Klin", "Pampili", "Bibi", "Ortopé", "Molekinha", "Molekinho", "Pimpolho", "Tip Toey Joey"
]

produtos = []
sku_counter = 1000

for marca in marcas:
    sku_counter += 1
    # Cria uma entrada padrão para cada marca com estoque de 2 pares por numeração
    produtos.append({
        "sku": f"SKU-{sku_counter}",
        "marca": marca,
        "categoria": "Calçados Gerais",
        "tamanhos_disponiveis": "35 (2 un), 36 (2 un), 37 (2 un), 38 (2 un), 39 (2 un), 40 (2 un), 41 (2 un), 42 (2 un), 43 (2 un)",
        "grade_estoque": "2 pares por número do 35 ao 43",
        "status": "Em Estoque"
    })

df = pd.DataFrame(produtos)
df.to_csv("estoque_pampa.csv", index=False, encoding="utf-8")
print(f"Sucesso! Planilha 'estoque_pampa.csv' gerada com {len(df)} marcas e estoque padrão.")