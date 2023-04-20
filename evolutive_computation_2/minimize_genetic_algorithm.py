import math
import random
import matplotlib.pyplot as plt
import numpy


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

    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


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


def select_parents(population, individual_size, k, min_val, max_val):
    """
    Seleciona os pais para reprodução usando o método da roleta viciada.
    Retorna uma lista com os índices dos pais selecionados.
    """
    scores = [(evaluate(*decode(individual, individual_size, min_val, max_val)), individual) for individual in population]

    # Classificar os indivíduos com base em seu desempenho
    scores.sort()
    # Selecionar os indivíduos mais bem classificados (elite) para a próxima geração
    ranked_individuals = [individual for (score, individual) in scores]
    elite = ranked_individuals[:k]

    # Criar a nova população de descendentes aleatórios
    parent_indices = []
    while len(parent_indices) < len(population) - k:
        # Selecionar dois pais aleatoriamente da população
        parent1 = random.choice(ranked_individuals)
        parent2 = random.choice(ranked_individuals)
        parent_indices.append(parent1)
        parent_indices.append(parent2)

    return scores, elite + parent_indices


# algoritmo genético
def genetic_algorithm(pop_size, individual_size, generations, k, crossover_rate, mutation_rate, min_val, max_val):
    # cria a população inicial
    scores = []
    pop = create_population(pop_size, individual_size)

    best_bitstring = ''
    best_x = 0
    best_y = 0
    best_score = pop_size
    stagnation = 0

    # Executar o loop principal do algoritmo genético
    for generation in range(generations):
        # Seleciona os pais para reprodução
        scores, parent_indices = select_parents(pop, individual_size, k, min_val, max_val)

        # o melhor indivíduo
        best_bitstring_ = scores[0][1]
        best_x_, best_y_ = decode(best_bitstring_, individual_size, min_val, max_val)
        best_score_ = evaluate(best_x_, best_y_)

        if best_score_ < best_score:
            best_bitstring = best_bitstring_
            best_x, best_y = best_x_, best_y_
            best_score = best_score_
            stagnation = 0
        else:
            stagnation += 1
            if stagnation > 400:
                return generation - stagnation, best_score


        # Realiza o crossover e a mutação dos filhos
        children = []
        for i in range(0, len(parent_indices), 2):
            parent1 = parent_indices[i]
            parent2 = parent_indices[i + 1]
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2
            child1 = mutation(child1, mutation_rate)
            child2 = mutation(child2, mutation_rate)

            # Adiciona os filhos à nova população
            children.append(child1)
            children.append(child2)

        pop = children

    # retorna a melhor solução encontrada
    return generation - stagnation, best_score


def main():
    # Definir os parâmetros do algoritmo genético
    pop_size = 100  # tamanho da população
    k = 10  # tamanho da elite, que será mantida na próxima geração
    mutation_rate = 0.1  # taxa de mutação
    crossover_rate = 1  # taxa de crossover
    generations = 1000  # número de gerações
    bits = 20  # número de bits usados para representar cada variável
    min_val = -10  # valor mínimo das variáveis
    max_val = 10  # valor máximo das variáveis

    genetic_algorithm(pop_size, bits, generations, k, crossover_rate, mutation_rate, min_val, max_val)

    generation_list = []
    best_solution_list = []

    for i in range(0, 200):
        generation, best_solution = genetic_algorithm(pop_size, bits, generations, k, crossover_rate, mutation_rate, min_val, max_val)

        generation_list.append(generation)
        best_solution_list.append(best_solution)
    #
    print('Geração máxima: ', max(generation_list))
    print('Geração mínima: ', min(generation_list))
    print('Geração média: ', numpy.mean(generation_list))
    print('Desvio padrão: ', numpy.std(generation_list))

    print('Solução máxima: ', max(best_solution_list))
    print('Solução mínima: ', min(best_solution_list))
    print('Solução média: ', numpy.mean(best_solution_list))
    print('Solução padrão: ', numpy.std(best_solution_list))

    plt.plot(generation_list)
    plt.ylabel('Geração')
    plt.show()


if __name__ == '__main__':
    main()
