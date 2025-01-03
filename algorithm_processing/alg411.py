from sys import maxsize
from stable_matching import (
    generate_responses,
    ppdictionary,
    flatten_preference_dictionary,
    generate_prefrence_list,
)
# Find all possible Stable Matchings (consistent with the Mathematical definition of Stable ie. no breaking pairs)


def refusal(current_woman, potential_huzz, marriages, male_pref, female_pref):
    print(current_woman, potential_huzz)
    current_huzz = marriages.get(current_woman)
    # if not married to anyone then just marry them off. gets rid of the dummy husband requirement.
    if current_huzz is None:
        current_huzz_index = maxsize
    else:
        current_huzz_index = female_pref[current_woman].index(current_huzz)
    potential_huzz_index = female_pref[current_woman].index(potential_huzz)
    # either case, potential huzz cannot get the same woman twice, so remove her from the list
    male_pref[potential_huzz].remove(current_woman)
    # Check if current woman prefers the potential husband more than who she is married to.
    if potential_huzz_index < current_huzz_index:
        # switch marriage
        marriages[current_woman] = potential_huzz
        # remove current woman from new husband's list because they cant get married again if she decides to divorce him.

        if current_huzz is None:
            return marriages

        return proposal(current_huzz, marriages, male_pref, female_pref)
    # call proposal on potential husband because he got turned down.
    return proposal(potential_huzz, marriages, male_pref, female_pref)


def proposal(current_bachelor, marriages, male_pref, female_pref):
    # instead of having a dummy male, we just call this function iif we want to match the male with their next prefered
    # partner.
    potential_wifey = male_pref[current_bachelor][0]
    return refusal(potential_wifey, current_bachelor, marriages, male_pref, female_pref)


def recursive_stable_matching(male_pref, female_pref):
    if len(male_pref) != len(female_pref):
        raise ValueError(
            "Male Pref and Female Pref must be the same size for this algorithm!"
        )
    marriages = {i: None for i in sorted(female_pref.keys())}

    for bachelor in male_pref.keys():
        marriages = proposal(bachelor, marriages, male_pref, female_pref)

    return marriages


def main():
    male = generate_responses(5, 5, 5)
    female = generate_responses(5, 5, 5)
    male_preference, female_preference = generate_prefrence_list(male, female)
    md, fd = flatten_preference_dictionary(male_preference, female_preference)

    print("Male Preference Table")
    ppdictionary(md)

    print("Female Preference Table")
    ppdictionary(fd)

    print("\nStable Matching:\n")
    matches = recursive_stable_matching(md, fd)

    ppdictionary(matches)


if __name__ == "__main__":
    main()
