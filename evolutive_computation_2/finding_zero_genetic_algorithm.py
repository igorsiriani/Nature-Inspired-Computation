import random
import matplotlib.pyplot as plt
import numpy


def evaluate_individual(individual, TARGET_BITSTRING):
    """
    Avalia a qualidade de um indivíduo comparando sua bitstring com a bitstring do número 0.
    Retorna o número de bits iguais entre as duas bitstrings.
    """
    quality = 0
    for i in range(len(TARGET_BITSTRING)):
        if individual[i] == TARGET_BITSTRING[i]:
            quality += 1
    return quality


def select_parents(population, TARGET_BITSTRING):
    """
    Seleciona os pais para reprodução usando o método da roleta viciada.
    Retorna uma lista com os índices dos pais selecionados.
    """
    scores = [(evaluate_individual(individual, TARGET_BITSTRING), individual) for individual in population]

    # Classificar os indivíduos com base em seu desempenho
    scores.sort()
    # Selecionar os indivíduos mais bem classificados (elite) para a próxima geração
    ranked_individuals = [individual for (score, individual) in scores]
    elite = ranked_individuals[:10]

    # Criar a nova população de descendentes aleatórios
    parent_indices = []
    while len(parent_indices) < len(population) - 10:
        # Selecionar dois pais aleatoriamente da população
        parent1 = random.choice(ranked_individuals)
        parent2 = random.choice(ranked_individuals)
        parent_indices.append(parent1)
        parent_indices.append(parent2)

    return elite + parent_indices


def crossover(parent1, parent2):
    """
    Realiza o crossover de um ponto entre dois pais e retorna os dois filhos resultantes.
    """
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def mutate(individual, MUTATION_RATE):
    """
    Realiza a mutação de um bit do indivíduo com a taxa de mutação especificada.
    """
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            individual[i] = 1 - individual[i]
    return individual


# algoritmo genético
def genetic_algorithm(POPULATION_SIZE, MAX_GENERATIONS, MUTATION_RATE, CROSSOVER_RATE, TARGET_BITSTRING):
    # Gera a população inicial com bitstrings aleatórias
    population = [[random.randint(0, 1) for _ in range(len(TARGET_BITSTRING))] for _ in range(POPULATION_SIZE)]

    # Repete o processo por várias gerações
    for generation in range(MAX_GENERATIONS):
        # Avalia a qualidade de cada indivíduo na população
        quality_scores = [evaluate_individual(individual, TARGET_BITSTRING) for individual in population]

        # Verifica se a qualidade máxima foi atingida e imprime o resultado
        if max(quality_scores) == len(TARGET_BITSTRING):
            return generation

        # Seleciona os pais para reprodução
        parent_indices = select_parents(population, TARGET_BITSTRING)

        # Realiza o crossover e a mutação dos filhos
        children = []
        for i in range(0, len(parent_indices), 2):
            parent1 = parent_indices[i]
            parent2 = parent_indices[i + 1]
            if random.random() < CROSSOVER_RATE:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2
            child1 = mutate(child1, MUTATION_RATE)
            child2 = mutate(child2, MUTATION_RATE)

            # Adiciona os filhos à nova população
            children.append(child1)
            children.append(child2)

        # Seleciona os melhores indivíduos da população atual
        sorted_indices = sorted(range(len(quality_scores)), key=lambda k: quality_scores[k], reverse=True)
        best_individuals = [population[i] for i in sorted_indices[:int(POPULATION_SIZE / 10)]]

        # Cria a nova população misturando os melhores indivíduos com os filhos gerados
        population = random.sample(best_individuals + children, POPULATION_SIZE)

        # print("População final:")
        # for individual in population:
        #     print(individual)


def main():
    # Definir os parâmetros do algoritmo genético
    # Define a bitstring do número 0
    TARGET_BITSTRING = [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1]

    # Define o tamanho da população e a taxa de mutação
    POPULATION_SIZE = 300
    MUTATION_RATE = 0
    CROSSOVER_RATE = 1

    # Define o número máximo de gerações
    MAX_GENERATIONS = 10000

    generation_list = []

    for i in range(0, 200):
        generation = genetic_algorithm(POPULATION_SIZE, MAX_GENERATIONS, MUTATION_RATE, CROSSOVER_RATE,
                                       TARGET_BITSTRING)

        generation_list.append(generation)

    print('Geração máxima: ', max(generation_list))
    print('Geração mínima: ', min(generation_list))
    print('Geração média: ', numpy.mean(generation_list))
    print('Desvio padrão: ', numpy.std(generation_list))
    plt.plot(generation_list)
    plt.ylabel('Geração')
    plt.show()


if __name__ == '__main__':
    main()
