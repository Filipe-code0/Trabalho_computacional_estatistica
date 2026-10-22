# Importação das bibliotecas para o script

# Ciência de dados 
import polars as pl

# Grafícos
import matplotlib.pyplot as plt
plt.matplotlib.use('TkAgg')

pl.Config.set_tbl_cols(-1)
# pl.Config.set_tbl_rows(-1)

dados = pl.read_csv('Zomato_Restauran_Dataset.csv')

print(30*'-')

# Letra C)

# Tira os restaurantes cujo o preço está em uma moeda diferente de dollar
dados = dados.filter(pl.col('Currency') == "Dollar($)")

# Agrupando as avaliações
grupo_avaliacoes = dados.partition_by("Rating text", as_dict=True)

# listas
lista_df = []
lista_medianas = []
lista_categorias = []

# Relaciona cada agrupamento a uma lista, além de tirar a mediana de cada agrupamento 
for avaliacao, df in grupo_avaliacoes.items():
    lista_categorias.append(avaliacao[0])                                   #lista de categorias
    lista_df.append(df)                                                     #lista de conjuntos de dados
    medianas = df.select(pl.col("Average Cost for two").median()).item()    #calcula as medianas
    lista_medianas.append(medianas)                                         #lista de medianas

plt.plot(lista_categorias, lista_medianas)

plt.title('Medianas de preços (preço médio para duas pessoas) por Tipo de Avaliação', fontsize=14, fontweight='bold')
plt.xlabel("Avaliação", fontsize=12, fontweight='bold')
plt.ylabel("Mediana do valor", fontsize=12, fontweight='bold')
plt.show()


teste = dados.filter(pl.col('Average Cost for two') == 25)
print(f'As medianas do conjunto de dados se dão todas em 25, provavelmente 25 foi usado como padrão para quando o dataset não tinha esse valor causando esse fenomeno estranho de medianas iguais.')
print(f'Quantidade de linha com preço = 25: {teste.shape[0]}')
print(f'Quantidade de linha usadas na analise: {dados.shape}')

print(30*'-')

# Letra D)

# Limpa a tela do gráfico para criar o próximo gráfico
plt.clf()

# Correlação entre preço e quantidade de avaliações

variavel_quantitativa = dados["Votes"]
eixo_y = [1] * len(variavel_quantitativa)
plt.scatter(variavel_quantitativa, eixo_y)

# Alterações esteticas do gráfico

plt.title('Distribuição de Avaliações', fontsize=14, fontweight='bold')
plt.xlabel('Quantidade de Avaliações (Votos)', fontsize=12, fontweight='bold')
plt.yticks([])
plt.show()
