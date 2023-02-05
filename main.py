import random
import timeit


def create_full_graph(number_of_vertex):
    graph = []
    for i in range(0, number_of_vertex-1):
        for j in range(i+1, number_of_vertex):
            graph.append([i, j])
    return graph


def create_graph(number_of_vertex, numer_edges_removed):
    graph = create_full_graph(number_of_vertex)
    for i in range(1, numer_edges_removed+1):
        del graph[random.randint(0, len(graph)-1)]
    return graph


def generate_base_population(size_population, size_subject):
    generation = []
    for i in range(size_population):
        subject = []
        for j in range(size_subject):
            subject.append(random.randint(0, 1))
        generation.append(subject)
    return generation


def generate_object_assessment(subject, graph):
    object_assessment = 0
    for i in subject:
        if i == 1:
            object_assessment += 1
    for i in graph:
        if subject[i[0]] == 0 and subject[i[1]] == 0:
            object_assessment += 1000
    return object_assessment


def chose_to_battle(generation):
    chosen_subjects = []
    a = random.randint(0, len(generation)-1)
    b = random.randint(0, len(generation)-1)
    while a == b:
        b = random.randint(0, len(generation)-1)
    chosen_subjects.append(generation[a])
    chosen_subjects.append(generation[b])
    return chosen_subjects


def selection(generation, graph):
    new_generation = []
    for i in range(len(generation)):
        list_of_fighters = chose_to_battle(generation)
        fighter1 = list_of_fighters[0]
        fighter2 = list_of_fighters[1]
        if generate_object_assessment(fighter1, graph) > generate_object_assessment(fighter2, graph):
            new_generation.append(fighter2)
        else:
            new_generation.append(fighter1)
    return new_generation


def mutating(generation):
    for i in range(0, len(generation)-1):
        if random.randint(0, 100) < 100:
            for j in range(0, len(generation[i])-1):
                if random.randint(0, 100) < 20:
                    if generation[i][j] == 0:
                        generation[i][j] = 1
                    else:
                        generation[i][j] = 0
    return generation


def rate_adaptation(generation, best_subject, graph):
    best_score = generate_object_assessment(best_subject, graph)
    new_best_subject = best_subject
    for i in generation:
        if generate_object_assessment(i, graph) < best_score:
            best_score = generate_object_assessment(i, graph)
            new_best_subject = i.copy()
    return new_best_subject


def evolution_algorithm(size_of_population, size_subject, i_counter, graph):
    generation = generate_base_population(size_of_population, size_subject)
    best_subject = generation[0]
    for i in range(i_counter):
        best_subject = rate_adaptation(generation, best_subject, graph)
        generation = selection(generation, graph)
        generation = mutating(generation)
    # print(best_subject)
    print(generate_object_assessment(best_subject, graph))
    return best_subject


example_graph = create_graph(25, 150)
print(timeit.timeit(stmt='evolution_algorithm(100, 25, 1000, example_graph)', globals=globals(), number=10)/10)
# evolution_algorithm(250, 25, 10000, example_graph)
print(example_graph)
