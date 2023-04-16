import math
import random


# função de avaliação
def evaluate(individual):
    # converte a string de bits para um valor inteiro
    x = fx = int(individual, 2) / (2**len(individual)-1)
    # calcula o valor da função f(x)
    return 2 ** (-2 * ((x - 0.1) / 0.9) ** 2) * (math.sin(5 * math.pi * x)) ** 6


# criação de uma população inicial de indivíduos
def create_population(population_size, individual_size):
    population = []
    for i in range(population_size):
        # cria uma string de bits aleatória com o tamanho do indivíduo
        individual = ''.join(random.choice(['0', '1']) for _ in range(individual_size))
        population.append(individual)
    return population


# seleção de indivíduos por torneio
def tournament_selection(population, k):
    # escolhe aleatoriamente k indivíduos da população
    tournament = random.sample(population, k)
    # retorna o indivíduo com o maior fitness
    return max(tournament, key=evaluate)


# crossover de dois indivíduos
def crossover(individual1, individual2):
    # escolhe um ponto de corte aleatório na string de bits
    crossover_point = random.randint(1, len(individual1) - 1)
    # realiza o crossover
    new_individual1 = individual1[:crossover_point] + individual2[crossover_point:]
    new_individual2 = individual2[:crossover_point] + individual1[crossover_point:]
    # retorna os novos indivíduos gerados
    return new_individual1, new_individual2


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
def genetic_algorithm(population_size, individual_size, generations, k, crossover_rate, mutation_rate):
    # cria a população inicial
    population = create_population(population_size, individual_size)

    # inicializa a melhor solução encontrada
    best_solution = None
    best_fitness = float('-inf')

    # executa as gerações
    for generation in range(generations):
        # avalia o fitness da população atual
        fitness_values = [evaluate(individual) for individual in population]

        # encontra o melhor indivíduo da população atual
        current_best = max(population, key=evaluate)
        current_best_fitness = evaluate(current_best)

        # atualiza a melhor solução encontrada
        if current_best_fitness > best_fitness:
            best_solution = current_best
            best_fitness = current_best_fitness

        # imprime o progresso do algoritmo
        print(f'Generation {generation}: best fitness = {best_fitness}')

        # seleciona os indivíduos para reprodução
        parents = [tournament_selection(population, k) for _ in range(population_size)]

        # realiza o crossover entre os pais
        offspring = []
        for i in range(0, population_size, 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2
            offspring.append(child1)
            offspring.append(child2)

        # realiza a mutação nos filhos gerados
        for i in range(population_size):
            offspring[i] = mutation(offspring[i], mutation_rate)

        # substitui a população anterior pela nova população gerada
        population = offspring

    # converte a string de bits da melhor solução para um valor inteiro
    best_solution_int = float(best_solution)

    # imprime a melhor solução encontrada
    print(f'Best solution: x = {best_solution_int}, f(x) = {best_fitness}')


def main():
    population_size = 100
    individual_size = 32
    generations = 100
    k = 10
    crossover_rate = 0.8
    mutation_rate = 0.01

    genetic_algorithm(population_size, individual_size, generations, k, crossover_rate, mutation_rate)


if __name__ == '__main__':
    main()
