import math
import random
import matplotlib.pyplot as plt
import numpy


# função de avaliação
def evaluate(individual):
    # converte a string de bits para um valor inteiro
    x = int(individual, 2) / (2**len(individual)-1)
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

    best_list = []
    stagnation = 0

    # executa as gerações
    for generation in range(generations):
        # avalia o fitness da população atual
        fitness_values = [evaluate(individual) for individual in population]

        # encontra o melhor indivíduo da população atual
        current_best = max(population, key=evaluate)
        current_best_fitness = evaluate(current_best)
        best_list.append(evaluate(current_best))

        # atualiza a melhor solução encontrada
        if current_best_fitness > best_fitness:
            best_solution = current_best
            best_fitness = current_best_fitness
            stagnation = 0
        else:
            stagnation += 1
            if stagnation > 400:
                best_solution_int = int(best_solution, 2) / (2**len(best_solution)-1)
                return generation - stagnation, round(best_solution_int, 2)

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
    best_solution_int = int(best_solution, 2) / (2**len(best_solution)-1)
    print(f'Best solution: x = {best_solution_int}, f(x) = {best_fitness}')

    # retorna a geração da melhor solução encontrada
    return generation - stagnation, round(best_solution_int, 2)


def main():
    # Definir os parâmetros do algoritmo genético
    population_size = 100  # tamanho da população
    individual_size = 32  # número de bits usados para representar cada variável
    generations = 1000  # número de gerações
    k = 10  # tamanho mantida na próxima geração
    crossover_rate = 0.5  # taxa de crossover
    mutation_rate = 0.1  # taxa de mutação

    generation_list = []
    best_solution_list = []

    for i in range(0, 200):
        generation, best_solution_int = genetic_algorithm(population_size, individual_size, generations, k, crossover_rate, mutation_rate)

        generation_list.append(generation)
        best_solution_list.append(best_solution_int)

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
