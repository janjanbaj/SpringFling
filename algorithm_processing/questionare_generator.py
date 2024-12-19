import numpy as np


NUMBER_OF_PEOPLE = 4
NUMBER_OF_CATEGORIES = 5
NUMBER_OF_TOTAL_QUESTIONS = 3


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
                NUMBER_OF_TOTAL_QUESTIONS + 1,
            ),
        )
        + 1
    )

    return responses


def generate_prefrence_list(male, female):
    male_dict = {}
    female_dict = {}
    match_directory = {}

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

            # assume a weight scale where 1-5 where lower means you care less.
            # we then take the euclidean distance between the two response vectors for the entire category.
            # then we multiply the scalar weigth. if the distance was a high and we care a lot:
            # ie. the weight is high and distance is high then the final resultant distance is going to be
            # high as well. if the distance is medium but the weight is high, any small discrepency will get
            # scaled up. all other anomalies get dealt with by the Stable Mathcing Algorithm and the
            # assymetry of the eucledian distance calculations.

            male_weighted_distance = np.sqrt(male_weight.reshape((len(male_weight), 1)) * (result * result)).sum(1)
            female_weighted_distance = np.sqrt(female_weight.reshape((len(female_weight), 1)) * (result * result)).sum(1)






if __name__ == "__main__":
    male = generate_responses()

    female = generate_responses()

    print(male)

    generate_prefrence_list(male, female)
