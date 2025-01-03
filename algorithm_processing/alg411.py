from sys import maxsize
from stable_matching import (
    generate_responses,
    ppdictionary,
    flatten_preference_dictionary,
    generate_prefrence_list,
    stable_matching_hetero,
)

"""Recursive Stable Marriage:"""


def refusal(current_woman, potential_huzz, marriages, male_pref, female_pref):
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


def flip_keys_values(indict):
    return {indict[i]: i for i in indict.keys()}


def recursive_stable_matching(male_pref, female_pref):
    if len(male_pref) != len(female_pref):
        raise ValueError(
            "Male Pref and Female Pref must be the same size for this algorithm!"
        )
    marriages = {i: None for i in sorted(female_pref.keys())}

    for bachelor in male_pref.keys():
        marriages = proposal(bachelor, marriages, male_pref, female_pref)

    # as the algorithm puts women as the keys, we have to flip to be consistent with estalbished conventions of Gale-Shapley and other work.
    return flip_keys_values(marriages)


# Find all possible Stable Matchings (consistent with the Mathematical definition of Stable ie. no breaking pairs)

"""All Stable Matching Using Recursive Stable Matching:"""


def all_refusal(
    current_woman, potential_huzz, marriages, male_pref, female_pref, success, unchanged
):
    current_huzz = marriages.get(current_woman)
    if current_huzz[0] == "-":
        current_huzz = current_huzz[1:]
    current_huzz_index = female_pref[current_woman].index(current_huzz)
    potential_huzz_index = female_pref[current_woman].index(potential_huzz)

    male_pref[current_huzz].remove(current_woman)

    if potential_huzz_index < current_huzz_index:
        marriages[current_woman] = potential_huzz

        # call all_proposal on current_huzz
        if current_huzz is None:
            return marriages

        marriages = all_proposal(
            current_huzz, marriages, male_pref, female_pref, success, unchanged
        )
    else:
        # call all_proposal on potential_huzz
        marriages = all_proposal(
            potential_huzz, marriages, male_pref, female_pref, success, unchanged
        )
    return marriages


def all_proposal(
    current_bachelor, marriages, male_pref, female_pref, success, unchanged
):
    if current_bachelor[0] == "-":
        success = True
        current_bachelor = current_bachelor[1:]
    elif (
        current_bachelor is None
        or len(male_pref[current_bachelor]) == 0
        or unchanged[current_bachelor] is False
    ):
        success = False
    else:
        potential_wifey = male_pref[current_bachelor][0]
        marriages = all_refusal(
            potential_wifey,
            current_bachelor,
            marriages,
            male_pref,
            female_pref,
            success,
            unchanged,
        )
    return marriages


def all_break_marriage(
    current_man, marriages, male_pref, female_pref, success, unchanged, stable_marriages
):
    # break marriage, by making them take the worst choices. testing if this would work.

    marriages[male_pref[current_man][-1]] = "-" + current_man
    marriages = all_proposal(
        current_man, marriages, male_pref, female_pref, success, unchanged
    )
    if success is False:
        unchanged[current_man] = False
        return
    # we have found a stable marriage:
    stable_marriages.append(flip_keys_values(marriages))
    current_man_index = male_pref.keys().index(current_man)

    for next_man in list(male_pref.keys())[current_man_index : len(male_pref)]:
        all_break_marriage(
            next_man,
            marriages,
            male_pref,
            female_pref,
            success,
            unchanged,
            stable_marriages,
        )
    for j in range(current_man_index + 1, len(male_pref)):
        unchanged[j] = True
    unchanged[current_man] = False
    return marriages


def all_stable_matchings(male_pref, female_pref):
    male_optimal = recursive_stable_matching(male_pref, female_pref)
    stable_marriages = [male_optimal]
    success = False
    unchanged = {i: False for i in male_pref.keys()}
    for current_man in male_pref.keys():
        all_break_marriage(
            current_man,
            male_optimal,
            male_pref,
            female_pref,
            success,
            unchanged,
            stable_marriages,
        )
    return stable_marriages


def main():
    male = generate_responses(5, 5, 5)
    female = generate_responses(5, 5, 5)
    male_preference, female_preference = generate_prefrence_list(male, female)
    # md, fd = flatten_preference_dictionary(male_preference, female_preference)
    mdGS, fdGS = flatten_preference_dictionary(male_preference, female_preference)

    # print("Male Preference Table")
    # ppdictionary(md)

    # print("Female Preference Table")
    # ppdictionary(fd)

    # print("\nStable Matching:(Recursive)\n")
    # matches = recursive_stable_matching(md, fd)

    # ppdictionary(matches)

    # print("\nStable Matching:(Gale-Shapley)\n")
    # matches = stable_matching_hetero(mdGS, fdGS)

    # ppdictionary(matches)

    # print(
    #    "Both Gale-Shapley and Recursive Must Be Identical as they are both give Male-Optimal Solutions"
    # )

    mariages = all_stable_matchings(mdGS, fdGS)
    for mar in mariages:
        print(f"\n{ppdictionary(mar)}\n")


if __name__ == "__main__":
    main()
