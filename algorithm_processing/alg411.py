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


class StableMatchingAll:
    def __init__(self, male_pref, female_pref) -> None:
        self.male_choice = male_pref
        self.female_choice = female_pref
        self.success = False
        self.man_list = sorted(list(male_pref.keys()))
        self.unchanged = {i: True for i in self.man_list}
        self.marriage = {i: None for i in female_pref.keys()}
        self.male_count = {i: 0 for i in self.man_list}
        self.stable = []

    def refusal(self, potential_man, woman, male_count, marriage):
        current_husband = marriage[woman]
        current_husband_index = maxsize
        # print(f"WM:{woman} | PM:{potential_man} | CM: {current_husband}")
        if current_husband is not None:
            current_husband_index = self.female_choice[woman].index(
                current_husband.lstrip("-")
            )
        potential_man_index = self.female_choice[woman].index(potential_man)
        # increase count such that potential_man will never be matched with woman
        male_count[potential_man] += 1
        if potential_man_index < current_husband_index:
            marriage[woman] = potential_man
            # call proposal on current hus
            if current_husband is None:
                return
            # swap with pm if cm gets cucked and cm is negative
            # if current_husband[0] == "-":
            #    marriage[
            #        self.male_choice[potential_man][male_count[potential_man] - 1]
            #    ] = current_husband.lstrip("-")

            return self.proposal(current_husband, male_count, marriage)
        # call propossal on potential man
        return self.proposal(potential_man, male_count, marriage)

    def proposal(self, man, male_count, marriage):
        # print(f"Trying to Marry:{man} | {male_count}")
        if man[0] == "-":
            self.success = True
        elif male_count[man] == len(self.man_list) or self.unchanged[man] is False:
            self.success = False
        else:
            # self.male_count[man] += 1
            self.refusal(
                man, self.male_choice[man][male_count[man]], male_count, marriage
            )
        return

    def found_stable(self, marriage):
        # print(f"Found Stable Marriage: { {marriage[i]:i for i in marriage} }")
        self.stable.append(marriage.copy())
        return

    def break_marriage(self, man, marriage):
        # print(man, self.male_choice[man], self.male_count[man])
        # male count points to the next woman so you have to subtract one
        temp = marriage.copy()
        marriage[self.male_choice[man][self.male_count[man] - 1]] = "-" + man
        self.proposal(man, self.male_count.copy(), marriage)
        if self.success:
            print(man, self.male_choice[man][self.male_count[man] - 1])
            print(f"Temp: {flip_keys_values(temp)}")
            print(f"Soln: {flip_keys_values(marriage)}")
            self.found_stable(marriage)

            for next in self.man_list[self.man_list.index(man) : -2]:
                marriage = self.break_marriage(next, marriage)

            for next in self.man_list[self.man_list.index(man) + 1 : -2]:
                self.unchanged[next] = True
        else:
            print("Used Backup")
            marriage = temp

        self.unchanged[man] = False
        return marriage

    def all_stable(self):
        for man in self.man_list:
            self.proposal(man, self.male_count, self.marriage)

        self.found_stable(self.marriage)

        for man in self.man_list[0:-2]:
            self.break_marriage(man, self.marriage.copy())
        # [ppdictionary(flip_keys_values(i)) for i in self.stable]


def main():
    # male = generate_responses(10, 5, 5)
    # female = generate_responses(10, 5, 5)
    # male_preference, female_preference = generate_prefrence_list(male, female)
    # md, fd = flatten_preference_dictionary(male_preference, female_preference)
    # mdGS, fdGS = flatten_preference_dictionary(male_preference, female_preference)

    # Sample from the paper
    mpl = [
        [5, 7, 1, 2, 6, 8, 4, 3],
        [2, 3, 7, 5, 4, 1, 8, 6],
        [8, 5, 1, 4, 6, 2, 3, 7],
        [3, 2, 7, 4, 1, 6, 8, 5],
        [7, 2, 5, 1, 3, 6, 8, 4],
        [1, 6, 7, 5, 8, 4, 2, 3],
        [2, 5, 7, 6, 3, 4, 8, 1],
        [3, 8, 4, 5, 7, 2, 6, 1],
    ]
    fpl = [
        [5, 3, 7, 6, 1, 2, 8, 4],
        [8, 6, 3, 5, 7, 2, 1, 4],
        [1, 5, 6, 2, 4, 8, 7, 3],
        [8, 7, 3, 2, 4, 1, 5, 6],
        [6, 4, 7, 3, 8, 1, 2, 5],
        [2, 8, 5, 4, 6, 3, 7, 1],
        [7, 5, 2, 1, 8, 6, 4, 3],
        [7, 4, 1, 5, 2, 3, 6, 8],
    ]
    md = {f"{i+1}M": [f"{j}F" for j in mpl[i]] for i in range(len(mpl))}
    fd = {f"{i+1}F": [f"{j}M" for j in fpl[i]] for i in range(len(fpl))}
    print("Male Preference Table")
    ppdictionary(md)

    print("Female Preference Table")
    ppdictionary(fd)

    # print("\nStable Matching:(Recursive)\n")
    # matches = recursive_stable_matching(md, fd)

    # ppdictionary(matches)

    # print("\nStable Matching:(Gale-Shapley)\n")
    # matches = stable_matching_hetero(mdGS, fdGS)

    # ppdictionary(matches)

    # print(
    #    "Both Gale-Shapley and Recursive Must Be Identical as they are both give Male-Optimal Solutions"
    # )

    print("\nStable Matching:(Recursive/All)\n")
    st = StableMatchingAll(md, fd)
    st.all_stable()


if __name__ == "__main__":
    main()
