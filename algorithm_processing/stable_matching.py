import numpy as np
import bisect


NUMBER_OF_PEOPLE = 20
NUMBER_OF_CATEGORIES = 5
NUMBER_OF_QUESTIONS = 10


def generate_responses():
    # the first index will correspond to the i'th person and their reponse
    # the second index will correspond to the j'th category of questions.
    # the third index will correspond to the k'th question within the i'th category of questions.

    # we add one to the number of total questions because the first response will be the weight
    # for the entire category of those questions.

    # we also add 1 to the entire matrix because it gives us 0 weights and values, which is like what?

    responses = (
        np.random.binomial(
            n=4,
            p=0.5,
            size=(
                NUMBER_OF_PEOPLE,
                NUMBER_OF_CATEGORIES,
                NUMBER_OF_QUESTIONS + 1,
            ),
        )
        + 1
    )

    return responses


def generate_homo_preference_list(popn):
    result_dict = {}

    for man_index in range(len(popn) - 1):
        current_man = popn[man_index]

        if result_dict.get(man_index) is None:
            result_dict[man_index] = []

        male_weight = current_man[:, 0]
        male_responses = current_man[:, 1:]

        for woman_index in range(man_index + 1, len(popn)):
            current_woman = popn[woman_index]

            female_weight = current_woman[:, 0]
            female_responses = current_woman[:, 1:]

            result = male_responses - female_responses

            if result_dict.get(woman_index) is None:
                result_dict[woman_index] = []

            male_weighted_distance = np.sqrt(
                male_weight.reshape((len(male_weight), 1)) * (result * result)
            ).sum(1)
            female_weighted_distance = np.sqrt(
                female_weight.reshape((len(female_weight), 1)) * (result * result)
            ).sum(1)

            male_weighted_distance = np.mean(male_weighted_distance) + np.var(
                male_weighted_distance
            )
            female_weighted_distance = np.mean(female_weighted_distance) + np.var(
                female_weighted_distance
            )

            bisect.insort(
                result_dict[man_index],
                {"name": woman_index, "value": male_weighted_distance},
                key=lambda x: x["value"],
            )

            bisect.insort(
                result_dict[woman_index],
                {"name": man_index, "value": female_weighted_distance},
                key=lambda x: x["value"],
            )

    return result_dict


# TODO: need to deal with the case where there is an inequal pool. probably figure out who the least prefered person is
# delete them from everything and have a special state for them .
def generate_prefrence_list(male, female):
    # print("\nPreference List Calculations: ")

    if len(male) != len(female):
        raise ValueError(
            "Both pools have to be of same size! Cannot run Stable Matching with inequal pools."
        )

    male_dict = {}
    female_dict = {}

    for man_index in range(len(male)):
        current_man = male[man_index]

        male_dict[man_index] = []
        male_weight = current_man[:, 0]
        male_responses = current_man[:, 1:]

        for woman_index in range(len(female)):
            current_woman = female[woman_index]
            female_weight = current_woman[:, 0]
            female_responses = current_woman[:, 1:]

            result = male_responses - female_responses

            # print(f"{male_responses}\n{female_responses}\n{result}\n{result.sum(1)}\n")
            # print(f"MW:{male_weight}|FW:{female_weight}")

            if female_dict.get(woman_index) is None:
                female_dict[woman_index] = []

            # assume a weight scale where 1-5 where lower means you care less.
            # we then take the euclidean distance between the two response vectors for the entire category.
            # then we multiply the scalar weigth. if the distance was a high and we care a lot:
            # ie. the weight is high and distance is high then the final resultant distance is going to be
            # high as well. if the distance is medium but the weight is high, any small discrepency will get
            # scaled up. all other anomalies get dealt with by the Stable Mathcing Algorithm and the
            # assymetry of the eucledian distance calculations.

            male_weighted_distance = np.sqrt(
                male_weight.reshape((len(male_weight), 1)) * (result * result)
            ).sum(1)
            female_weighted_distance = np.sqrt(
                female_weight.reshape((len(female_weight), 1)) * (result * result)
            ).sum(1)

            # the idea here is that once you have the weighted eucledian distnace for each category.
            # we then take the mean of all the categories as our final score. i would think about how we could implement
            # adding variability to the mix but i feel like the mean takes care of it.

            # TODO: Is there anything other than just the raw mean we can do to better represent the similarity in categories.
            # for example: a high range (high - low) is bad because there is something that the two people were similar on but something
            # disasterous happened that skewed them away. but at the same time we do want that

            male_weighted_distance = np.mean(male_weighted_distance) + np.var(
                male_weighted_distance
            )
            female_weighted_distance = np.mean(female_weighted_distance) + np.var(
                female_weighted_distance
            )

            # print(f"M{man_index} & F{woman_index}: {male_weighted_distance}")
            # print(f"F{woman_index} & M{man_index}: {female_weighted_distance}")

            # insert such that it is in ascending order ie. lower distance matches, those are better matches, are ahead in the list.
            # for men use the male_weighted_distance and for women use the corresponding.

            bisect.insort(
                male_dict[man_index],
                {"name": woman_index, "value": male_weighted_distance},
                key=lambda x: x["value"],
            )

            bisect.insort(
                female_dict[woman_index],
                {"name": man_index, "value": female_weighted_distance},
                key=lambda x: x["value"],
            )

    # print("")
    return male_dict, female_dict


def flatten_preference_dictionary(male_dict, female_dict=None):
    if female_dict is not None:
        return {i: [j["name"] for j in male_dict[i]] for i in male_dict.keys()}, {
            i: [j["name"] for j in female_dict[i]] for i in female_dict.keys()
        }
    return {i: [j["name"] for j in male_dict[i]] for i in male_dict.keys()}


# Stable Matching Algorithm [Self-Implemented based on https://medium.com/@satyalumesh/gale-shapley-algorithm-for-stable-matching-easyexpalined-17ee51ec0dfa]


def stable_matching_hetero(male_pref, female_pref):
    free_men = list(male_pref.keys())

    # remove positional biases
    np.random.shuffle(free_men)

    matches = {i: "" for i in free_men}
    married_women = {}

    while len(free_men) != 0:
        # select a free man
        bachelor = free_men[0]
        # select his favorite wifey in order of preference:
        for wifey in male_pref[bachelor]:
            # if wifey is uncuffed,  cuff her!!!!
            if married_women.get(wifey) is None:
                matches[bachelor] = wifey
                married_women[wifey] = bachelor
                # print(f"M{bachelor} and F{wifey} get Married !")
                free_men.remove(bachelor)
                break
            # if wifey is married to someone else currently, then we need to see if we will home-wreck
            op = married_women[wifey]
            # if the index of bachelor is lower than the op's (wifey's current partner) we can swap
            if female_pref[wifey].index(op) > female_pref[wifey].index(bachelor):
                matches.pop(op)
                matches[bachelor] = wifey
                married_women[wifey] = bachelor
                # print(
                #     f"F{wifey} and M{op} get divorced but M{bachelor} and F{wifey} get Married !"
                # )
                free_men.remove(bachelor)
                free_men.append(op)
                break
    return matches


def stable_matching_homo(pref):
    free_people = list(pref.keys())

    if len(free_people) % 2 != 0:
        raise ValueError("Must have an even mating pool to run Stable Matching.")

    np.random.shuffle(free_people)

    matches = {}

    while len(free_people) != 0:
        bachelor = free_people[0]

        for wifey in pref[bachelor]:
            if matches.get(wifey) is None:
                matches[bachelor] = wifey
                matches[wifey] = bachelor
                # print(f"{bachelor} & {wifey} get Married !")
                free_people.remove(bachelor)
                free_people.remove(wifey)
                break

            op = matches[wifey]

            # print(f"W{wifey} | OP:{op} | Bach:{bachelor}")

            if pref[wifey].index(op) > pref[wifey].index(bachelor):
                matches.pop(op)
                matches[bachelor] = wifey
                matches[wifey] = bachelor
                # print(f"{op} & {wifey} get Divorced !")
                # print(f"{bachelor} & {wifey} get Married !")
                free_people.remove(bachelor)
                free_people.append(op)
                break

    return matches


# Brute Force All Pairings: O() algorithm that we will memoize:
# Idea: Create a Matrix of (m x f) iterate over all possible non overlapping diagonals. Those a
def brute_force_all_pairings(male, female):
    if len(male) != len(female):
        raise ValueError("Matching Pools must be of the same size")
    return


# Accessory Functions:


# Pretty Print Dictionary
def ppdictionary(dic):
    print("{")
    for key in dic.keys():
        print(f"{key}: {dic[key]}")
    print("}")


def test_random_stable_matching_hetero():
    print("\nStable Matching Hetero Demo:\n")

    male = generate_responses()

    female = generate_responses()

    print("Male:")

    print(male)

    print("Female:")

    print(female)

    male_preference, female_preference = generate_prefrence_list(male, female)

    md, fd = flatten_preference_dictionary(male_preference, female_preference)

    print("Male Preference Table")

    ppdictionary(md)

    print("Female Preference Table")

    ppdictionary(fd)

    print("\nStable Matching:\n")

    matches = stable_matching_hetero(md, fd)

    print("")

    ppdictionary(matches)


def test_random_stable_matching_homo():
    print("\nStable Matching Homo Demo:\n")
    popn1 = generate_responses()
    popn2 = generate_responses()

    popn = popn1 | popn2

    result = flatten_preference_dictionary(generate_homo_preference_list(popn))

    ppdictionary(result)
    print("")

    matches = stable_matching_homo(result)

    ppdictionary(matches)
    print("")

    return


if __name__ == "__main__":
    test_random_stable_matching_hetero()
    # test_random_stable_matching_homo()
