import random

# code from LINK: https://github.com/miethe/DnD-Character-Generator


class Dice_Roller:

    # This one rolls x amount of dice a single time
    # Example: Dice_Roller().roll_n_d_x(4, 6) is roll 4d6 once
    def roll_n_d_x(self, n_count, x_die_size):
        rolls = []
        for _ in range(n_count):
            # randrange is [x,y)
            rolls.append(random.randrange(1, x_die_size+1))
        return rolls

    def drop_low_and_tally(self, rolls):
        if not rolls:
            return rolls
        rolls.sort()
        return sum(rolls[1:])

    # Args needed when called are times rolled, what dice, and how many times that is rolled
    # Example: Dice_Roller().roll_ndx_y_times(4, 6, 7, True) is roll 4d6 7 times and drop the lowest
    def roll_ndx_y_times(self, times_rolled, die_size, total_iterations, drop_lowest=False):
        total_rolls = []
        if times_rolled == 0 or die_size == 0 or total_iterations == 0:
            return total_rolls
        for _ in range(total_iterations):
            rolls = self.roll_n_d_x(times_rolled, die_size)
            total_rolls.append(self.drop_low_and_tally(rolls))
        if drop_lowest:
            total_rolls.sort()
            return total_rolls[1:]
        else:
            return total_rolls


def _average(lst):
    return sum(lst) / len(lst)


if __name__ == "__main__":
    print(_average(Dice_Roller().roll_ndx_y_times(4, 6, 1000)))
