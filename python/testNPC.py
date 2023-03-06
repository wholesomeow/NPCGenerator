
def main():
    response = ['ESum1: This person i...knowledge.', 'ESum2: This person i... balance. ', 'ESum3: This person i... others.  ',
                'DesireSum: The funda...ul tasks. ', 'FearSum: An inherent...tuations. ', 'MentalSum: This char...at hand . ', 'MotiveSum: Their str...n moment .']
    holding = []

    # if statement
    thisThing = 1
    if thisThing == 0:
        print("This thing was true")
    elif thisThing == 1:
        print("This thing was not true")
    else:
        print("It was neither")

    print("___________________")

    # for loop
    for item in response:
        print(item)

    for num in range(3):
        print(num)

    print("___________________")

    # while loop
    i = 0
    while i < 10:
        print(i)
        i += 1


if __name__ == "__main__":
    main()
