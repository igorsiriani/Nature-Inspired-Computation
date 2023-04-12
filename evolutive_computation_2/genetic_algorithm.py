import random

# Define a bitstring do número 0
TARGET_BITSTRING = [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1]

# Define o tamanho da população e a taxa de mutação
POPULATION_SIZE = 10
MUTATION_RATE = 0.01

# Define o número máximo de gerações
MAX_GENERATIONS = 1000


def evaluate_individual(individual):
    """
    Avalia a qualidade de um indivíduo comparando sua bitstring com a bitstring do número 0.
    Retorna o número de bits iguais entre as duas bitstrings.
    """
    quality = 0
    for i in range(len(TARGET_BITSTRING)):
        if individual[i] == TARGET_BITSTRING[i]:
            quality += 1
    return quality


def select_parents(population):
    """
    Seleciona os pais para reprodução usando o método da roleta viciada.
    Retorna uma lista com os índices dos pais selecionados.
    """
    total_quality = sum([evaluate_individual(individual) for individual in population])
    probabilities = [evaluate_individual(individual) / total_quality for individual in population]
    parent_indices = []
    for i in range(len(population) // 2):
        parent1_index = random.choices(range(len(population)), weights=probabilities)[0]
        parent2_index = random.choices(range(len(population)), weights=probabilities)[0]
        parent_indices.append(parent1_index)
        parent_indices.append(parent2_index)
    return parent_indices


def crossover(parent1, parent2):
    """
    Realiza o crossover de um ponto entre dois pais e retorna os dois filhos resultantes.
    """
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def mutate(individual):
    """
    Realiza a mutação de um bit do indivíduo com a taxa de mutação especificada.
    """
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            individual[i] = 1 - individual[i]
    return individual


# Gera a população inicial com bitstrings aleatórias
population = [[random.randint(0, 1) for _ in range(len(TARGET_BITSTRING))] for _ in range(POPULATION_SIZE)]

# Repete o processo por várias gerações
for generation in range(MAX_GENERATIONS):
    # Avalia a qualidade de cada indivíduo na população
    quality_scores = [evaluate_individual(individual) for individual in population]

    # Verifica se a qualidade máxima foi atingida e imprime o resultado
    if max(quality_scores) == len(TARGET_BITSTRING):
        print(f"Indivíduo encontrado na geração {generation}!")
        break

    # Seleciona os pais para reprodução
    parent_indices = select_parents(population)

    # Realiza o crossover e a mutação dos filhos
    children = []
    for i in range(0, len(parent_indices), 2):
        parent1 = population[parent_indices[i]]
        parent2 = population[parent_indices[i + 1]]
        child1, child2 = crossover(parent1, parent2)
        child1 = mutate(child1)
        child2 = mutate(child2)

        # Adiciona os filhos à nova população
        children.append(child1)
        children.append(child2)

    # Seleciona os melhores indivíduos da população atual
    sorted_indices = sorted(range(len(quality_scores)), key=lambda k: quality_scores[k], reverse=True)
    best_individuals = [population[i] for i in sorted_indices[:int(POPULATION_SIZE / 10)]]

    # Cria a nova população misturando os melhores indivíduos com os filhos gerados
    population = random.sample(best_individuals + children, POPULATION_SIZE)

    print("População final:")
    for individual in population:
        print(individual)
