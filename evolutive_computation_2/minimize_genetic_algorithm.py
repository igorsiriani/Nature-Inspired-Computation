import math
import random


# função de avaliação
def evaluate(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2


# funções de decodificação
def decode(bitstring, bits, min_val, max_val):
    # dividimos a string em dois pedaços, um para x e outro para y
    x_bits = bitstring[:bits]
    y_bits = bitstring[bits:]
    # convertemos cada pedaço para um número decimal
    x = min_val + (max_val - min_val) / (2 ** bits - 1) * int(x_bits, 2)
    y = min_val + (max_val - min_val) / (2 ** bits - 1) * int(y_bits, 2)
    return x, y


# criação de uma população inicial de indivíduos
def create_population(pop_size, bits):
    pop = []
    for i in range(pop_size):
        # criamos uma string aleatória de bits para representar cada indivíduo
        bitstring = ''.join(random.choice(['0', '1']) for _ in range(2 * bits))
        pop.append(bitstring)
    return pop


# crossover de dois indivíduos
def crossover(parent1, parent2):
    # Criar um descendente cruzando os pais
    child = ''
    for bit1, bit2 in zip(parent1, parent2):
        child += random.choice([bit1, bit2])
    return child


# mutação de um indivíduo
def mutation(individual, mutation_rate):
    # converte a string de bits para uma lista de caracteres
    individual = list(individual)
    # para cada bit na string, aplica a mutação com a taxa definida
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = '0' if individual[i] == '1' else '1'
    # retorna a string de bits mutada
    return ''.join(individual)


# algoritmo genético
def genetic_algorithm(pop_size, individual_size, generations, k, crossover_rate, mutation_rate, min_val, max_val):
    # cria a população inicial
    scores = []
    pop = create_population(pop_size, individual_size)

    # Executar o loop principal do algoritmo genético
    for generation in range(generations):
        # Avaliar a função de fitness para cada indivíduo na população
        scores = [(evaluate(*decode(individual, individual_size, min_val, max_val)), individual) for individual in pop]

        # Classificar os indivíduos com base em seu desempenho
        scores.sort()
        # Selecionar os indivíduos mais bem classificados (elite) para a próxima geração
        ranked_individuals = [individual for (score, individual) in scores]
        elite = ranked_individuals[:k]
        # Criar a nova população de descendentes aleatórios
        offspring = []
        while len(offspring) < pop_size - k:
            # Selecionar dois pais aleatoriamente da população
            parent1 = random.choice(ranked_individuals)
            parent2 = random.choice(ranked_individuals)

            if random.random() < crossover_rate:
                child = crossover(parent1, parent2)
            else:
                child = random.choice([parent1, parent2])

            # Aplicar mutação ao filho
            mutant = mutation(child, mutation_rate)
            # Adicionar o filho mutante à nova população
            offspring.append(mutant)
            # Combinar a elite e a nova população para formar a próxima geração
        pop = elite + offspring

    # Retornar o melhor indivíduo encontrado
    best_bitstring = scores[0][1]
    best_x, best_y = decode(best_bitstring, individual_size, min_val, max_val)
    best_score = evaluate(best_x, best_y)

    # imprime a melhor solução encontrada
    print(f"Melhor solução encontrada: x={best_x}, y={best_y}, score={best_score}")


def main():
    # Definir os parâmetros do algoritmo genético
    pop_size = 100  # tamanho da população
    k = 10  # tamanho da elite, que será mantida na próxima geração
    mutation_rate = 0.01  # taxa de mutação
    crossover_rate = 0.8  # taxa de crossover
    generations = 1000  # número de gerações
    bits = 20  # número de bits usados para representar cada variável
    min_val = -10  # valor mínimo das variáveis
    max_val = 10  # valor máximo das variáveis

    genetic_algorithm(pop_size, bits, generations, k, crossover_rate, mutation_rate, min_val, max_val)


if __name__ == '__main__':
    main()
