import numpy as np
from numpy import random

chromosome_length = 10
no_of_genes = 20
Teachers = np.array(
    ["Sir Javad Ahmed", "Sir Umair Arshad", "Mam Amina", "Mam Labiba", "Mam Amna Irum", "Sir Hassan Mustafa",
     "Sir Kashif Munir", "Sir Muhammad Asim", "Sir Saad", "Sir Ejaz"])
Classes = np.array(["ALGO", "AI", "HCI", "SMD", "TM", "CNET", "CP", "OS", "DB"])
Sections = np.array(["A", "B", "C", "D", "E"])
Duration = np.array(["0830", "0930", "1030", "1130", "1230", "0130", "0230", "0330", "0430"])
Days = np.array(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
Rooms = np.array([101, 102, 103, 201, 202, 203, 301, 302, 303, 401, 402, 403, 501, 502, 503])

def get_random_gene():
    return [random.choice(Teachers), random.choice(Sections), random.choice(Classes), random.choice(Duration),
            random.choice(Days), random.choice(Rooms)]


def get_choromosomes_array():
    Chromosomes_array = []
    for i in range(no_of_genes):
        gene = get_random_gene()
        Chromosomes_array.append(gene)
    return Chromosomes_array


def calculate_fitness(chromosome):
    score = 0
    two_teacher_at_same_time = True
    two_secs_at_same_time = True
    two_classes_at_same_time = True
    three_consecutive_classes = True
    three_consecutive_secs = True
    no_class_friday=True
    for i in range(len(chromosome)):
        teacher = chromosome[i][0]
        section = chromosome[i][1]
        classes = chromosome[i][2]
        time = chromosome[i][3]
        day = chromosome[i][4]
        room = chromosome[i][5]
        for j in range(i + 1, len(chromosome)):
            # No teacher can hold two classes at same time
            if two_teacher_at_same_time and teacher == chromosome[j][0] and time == chromosome[j][3]:
                two_teacher_at_same_time = False
            # No section can listen for two classes at same time
            if two_secs_at_same_time and classes == chromosome[j][2] and section == chromosome[j][1] and time == \
                    chromosome[j][3]:
                two_secs_at_same_time = False
            # No classroom can hold two classes at same time
            if two_classes_at_same_time and day == chromosome[j][4] and room == chromosome[j][5] and section == \
                    chromosome[j][1] and time == chromosome[j][3]:
                two_classes_at_same_time = False
            if no_class_friday and day== "Friday" and time=="1230":
                no_class_friday=False
    for i in range(len(chromosome) - 1):
        teacher = chromosome[i][0]
        for j in range(i + 1, len(chromosome) - 1):
            if three_consecutive_classes and teacher == chromosome[j][0] and teacher == chromosome[j + 1][0]:
                three_consecutive_classes = False
    for i in range(len(chromosome) - 1):
        section = chromosome[i][1]
        for j in range(i + 1, len(chromosome) - 1):
            # print (i,j)
            if three_consecutive_secs and section == chromosome[j][1] and section == chromosome[j + 1][
                1]:
                three_consecutive_secs = False
                # print("found 3 consecutives")

    if two_teacher_at_same_time:
        score += 1
    if two_classes_at_same_time:
        score += 1
    if two_secs_at_same_time:
        score += 1
    if three_consecutive_classes:
        score += 1
    if no_class_friday:
        score+=1
    if three_consecutive_secs:
        score += 1
    return score


def roulette_wheel_selection(populations_array):
    fitness_array = []
    probs = []
    pops_idx = []
    for i in range(len(populations_array)):
        fitness_array.append(calculate_fitness(populations_array[i]))
    # print(fitness_array)
    for i in range(len(fitness_array)):
        probs.append(fitness_array[i] / sum(fitness_array))
    for i in range(len(populations_array)):
        pops_idx.append(i)
    return np.random.choice(pops_idx, 2, probs)


def crossover(chromosome1, chromosome2):
    c1 = []
    c2 = []
    rand = random.randint(0, no_of_genes + 1)
    # print(rand)
    for i in range(rand):
        c1.append(chromosome1[i])
        c2.append(chromosome2[i])
    c1_ = []
    c2_ = []
    for i in range(rand, no_of_genes):
        c1_.append(chromosome1[i])
        c2_.append(chromosome2[i])
    c1__ = []
    c2__ = []
    for i in range(len(c1)):
        c1__.append(c1[i])
    for i in range(len(c2_)):
        c1__.append(c2_[i])
    for i in range(len(c2)):
        c2__.append(c2[i])
    for i in range(len(c1_)):
        c2__.append(c1_[i])
    return c1__, c2__


def replace_with_lowest_fitness(c1, c2):
    fitness_array = []
    for i in range(len(populations_array)):
        fitness_array.append(calculate_fitness(populations_array[i]))
    lowest = fitness_array[0]
    lowest2 = None
    for i in fitness_array[1:]:
        if i < lowest:
            lowest2 = lowest
            lowest = i
        elif lowest2 == None or lowest2 > i:
            lowest2 = i
    lowest_idx = fitness_array.index(lowest)
    lowest2_idx = fitness_array.index(lowest2)
    if calculate_fitness(c1) > lowest:
        populations_array[lowest] = c1
        mutation(populations_array[lowest_idx])
    if calculate_fitness(c2) > lowest2:
        populations_array[lowest2] = c2
        mutation(populations_array[lowest2_idx])


def mutation(c):
    mutation_rate = random.randint(0, 100)
    if mutation_rate > 3:
        return
    gene_idx = random.randint(0, len(c))
    rand_duration = random.choice(Duration)
    # print("here")
    # print(c[gene_idx][3],rand_duration)
    c[gene_idx][3] = rand_duration


def best_chromosome():
    fitness_array = []
    for i in range(len(populations_array)):
        fitness_array.append(calculate_fitness(populations_array[i]))
    maxim = 0
    maxim = max(fitness_array)
    maxim_idx = fitness_array.index(maxim)
    return populations_array[maxim_idx]


# main
populations_array = []
for i in range(chromosome_length):
    chromosome = get_choromosomes_array()
    populations_array.append(chromosome)
generations = 0
while (True):
    print(generations, "generation")
    print(calculate_fitness(best_chromosome()))
    if calculate_fitness(best_chromosome()) >= 5:
        print(best_chromosome())
        break
    childrens = 4
    for i in range(childrens // 2):
        selected_chromosome = roulette_wheel_selection(populations_array)
        chr1, chr2 = crossover(populations_array[selected_chromosome[0]], populations_array[selected_chromosome[1]])
        replace_with_lowest_fitness(chr1, chr2)
        generations += 1
