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


##def all_refusal(
##    current_woman, potential_huzz, marriages, male_pref, female_pref, success, unchanged
##):
##    current_huzz = marriages.get(current_woman)
##    if current_huzz[0] == "-":
##        current_huzz = current_huzz[1:]
##    current_huzz_index = female_pref[current_woman].index(current_huzz)
##    potential_huzz_index = female_pref[current_woman].index(potential_huzz)
##
##    male_pref[current_huzz].remove(current_woman)
##
##    if potential_huzz_index < current_huzz_index:
##        marriages[current_woman] = potential_huzz
##
##        # call all_proposal on current_huzz
##        if current_huzz is None:
##            return marriages
##
##        marriages = all_proposal(
##            current_huzz, marriages, male_pref, female_pref, success, unchanged
##        )
##    else:
##        # call all_proposal on potential_huzz
##        marriages = all_proposal(
##            potential_huzz, marriages, male_pref, female_pref, success, unchanged
##        )
##    return marriages
##
##
##def all_proposal(
##    current_bachelor, marriages, male_pref, female_pref, success, unchanged
##):
##    if current_bachelor[0] == "-":
##        success = True
##        current_bachelor = current_bachelor[1:]
##    elif (
##        current_bachelor is None
##        or len(male_pref[current_bachelor]) == 0
##        or unchanged[current_bachelor] is False
##    ):
##        success = False
##    else:
##        potential_wifey = male_pref[current_bachelor][0]
##        marriages = all_refusal(
##            potential_wifey,
##            current_bachelor,
##            marriages,
##            male_pref,
##            female_pref,
##            success,
##            unchanged,
##        )
##    return marriages
##
##
##def all_break_marriage(
##    current_man, marriages, male_pref, female_pref, success, unchanged, stable_marriages
##):
##    # break marriage, by making them take the worst choices. testing if this would work.
##    marriages[stable_marriages[0][current_man]] = "-" + current_man
##    marriages = all_proposal(
##        current_man, marriages, male_pref, female_pref, success, unchanged
##    )
##    if success is False:
##        unchanged[current_man] = False
##        return
##    # we have found a stable marriage:
##    stable_marriages.append(flip_keys_values(marriages))
##    current_man_index = male_pref.keys().index(current_man)
##
##    for next_man in list(male_pref.keys())[current_man_index : len(male_pref)]:
##        all_break_marriage(
##            next_man,
##            marriages,
##            male_pref,
##            female_pref,
##            success,
##            unchanged,
##            stable_marriages,
##        )
##    for j in range(current_man_index + 1, len(male_pref)):
##        unchanged[j] = True
##    unchanged[current_man] = False
##    return marriages
##
##
##def all_stable_matchings(male_pref, female_pref):
##    male_optimal = recursive_stable_matching(male_pref, female_pref)
##    stable_marriages = [male_optimal]
##    success = False
##    unchanged = {i: False for i in male_pref.keys()}
##    for current_man in male_pref.keys():
##        all_break_marriage(
##            current_man,
##            male_optimal,
##            male_pref,
##            female_pref,
##            success,
##            unchanged,
##            stable_marriages,
##        )
##        male_optimal = stable_marriages[0]
##        success = False
##        unchanged = {i: False for i in male_pref.keys()}
##
##    return stable_marriages


## def all_stable_marriages(male_pref, female_pref):
##     stable_matches = []
##     unchanged = {i: True for i in male_pref.keys()}
##     # since men are the keys in this convention, we are getting the index of their matches in
##     # the male optimal solution.
##     man_list = sorted(list(male_pref.keys()))
##     starting_marriage = {i: None for i in sorted(female_pref.keys())}
##     male_count = {i: 0 for i in man_list}
##     woman_list = sorted(list(female_pref.keys()))
##
##     def found_stable_marriage(marriage):
##         stable_matches.append(marriage)
##         return
##
##     def refusal(current_woman, potential_huzz, marriages):
##         current_huzz = marriages.get(current_woman)
##         # if not married to anyone then just marry them off. gets rid of the dummy husband requirement.
##         if current_huzz is None:
##             current_huzz_index = maxsize
##         else:
##             current_huzz = current_huzz.lstrip("-")
##             current_huzz_index = female_pref[current_woman].index(current_huzz)
##         potential_huzz_index = female_pref[current_woman].index(potential_huzz)
##         # either case, potential huzz cannot get the same woman twice, so increase their count.
##         male_count[potential_huzz] += 1
##         # Check if current woman prefers the potential husband more than who she is married to.
##         if potential_huzz_index < current_huzz_index:
##             # switch marriage
##             marriages[current_woman] = potential_huzz
##             # remove current woman from new husband's list because they cant get married again if she decides to divorce him.
##
##             if current_huzz is None:
##                 return False
##
##             return proposal(current_huzz, marriages)
##         # call proposal on potential husband because he got turned down.
##         return proposal(potential_huzz, marriages)
##
##     def proposal(current_bachelor, marriages):
##         if current_bachelor[0] == "-":
##             current_bachelor = current_bachelor.lstrip("-")
##         if (
##             male_count[current_bachelor] == len(male_pref.keys()) - 1
##             or unchanged[current_bachelor] is False
##         ):
##             return False
##             # instead of having a dummy male, we just call this function iif we want to match the male with their next prefered
##             # partner.
##         male_count[current_bachelor] += 1
##         potential_wifey = male_pref[current_bachelor][male_count[current_bachelor]]
##         refusal(potential_wifey, current_bachelor, marriages)
##         return True
##
##     def break_marriage(man, marriage):
##         # break the marriage for man by reversing the search since marriage is indexed by women.
##         marriage[male_pref[man][male_count[man]]] = "-" + man
##         success = proposal(man, marriage)
##         if success:
##             found_stable_marriage(marriage)
##             man_index = man_list.index(man)
##             for next_man in man_list[man_index : len(man_list) - 1]:
##                 break_marriage(next_man, marriage)
##             for next_man in man_list[man_index + 1 : len(man_list) - 1]:
##                 unchanged[next_man] = True
##         unchanged[man] = False
##         return
##
##     for man in man_list:
##         proposal(man, starting_marriage)
##     found_stable_marriage(starting_marriage)
##     print("Male-Optimal")
##     ppdictionary(starting_marriage)
##
##     for man in man_list:
##         break_marriage(man, starting_marriage)
##
##     print(stable_matches)
##
##     return stable_matches


def all_stable_matching():
    stable_matches = []


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

    mariages = all_stable_marriages(mdGS, fdGS)
    for mar in mariages:
        print(f"\n{ppdictionary(mar)}\n")


if __name__ == "__main__":
    main()
