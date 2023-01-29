import json

import enneagramScraper


def findWings(count):
    count += 1
    output = []
    match count:
        case 1:
            wings = [9, 2]
            output.append(wings)
        case 2:
            wings = [1, 3]
            output.append(wings)
        case 3:
            wings = [2, 4]
            output.append(wings)
        case 4:
            wings = [3, 5]
            output.append(wings)
        case 5:
            wings = [4, 6]
            output.append(wings)
        case 6:
            wings = [5, 7]
            output.append(wings)
        case 7:
            wings = [6, 8]
            output.append(wings)
        case 8:
            wings = [7, 9]
            output.append(wings)
        case 9:
            wings = [8, 1]
            output.append(wings)

    return output


def inputPreProc(input):
    result, temp, mainData, subData = [], [], [], []
    output = {}
    matchStr = "Privacy Policy\xa0|\xa0Terms of Use\nCopyright 2021, The Enneagram Institute®. All rights Reserved."
    writeKeys = ["title", "briefDesc", "overview", "listen", "levelOfDevelopment", "Compatibiltiy",
                 "Misidentification", "Addictions", "growthRecommendations", "learnMore", "privacyPolicy"]
    for i_count, item in enumerate(input):
        if i_count == 2:
            temp = list(item.values())
            t_count = 0
            for count, index in enumerate(writeKeys):
                if index == "overview":
                    output.update({writeKeys[count]: "Content coming"})
                elif index == "privacyPolicy":
                    output.update({writeKeys[count]: matchStr})
                else:
                    output.update({writeKeys[count]: temp[t_count]})
                    t_count += 1
            result.append(output)
        elif i_count < 9:
            result.append(item)

    # Process main data
    for i_res in result:
        resTemp = list(i_res.values())
        strList = []
        for each in resTemp:
            strip_each = each.splitlines()
            strList.append(strip_each)
        mainData.append(strList)

    # Process sub data
    for s_res in item:
        s_resTemp = list(s_res.values())
        s_strList = []
        for s_each in s_resTemp:
            s_strip_each = s_each.splitlines()
            s_strList.append(s_strip_each)
        subData.append(s_strList)

    return mainData, subData


def convertScrapedData(mainInput, subInput):
    # Ingests scraped data and outputs to json
    output = {}
    bufferList, subBufferList = [], []
    keyList = ["typeID", "keyWords", "briefDesc", "basicFear", "basicDesire", "wings", "keyMotivations", "overview",
               "addictions", "growthRecommendations"]

    for count, item in enumerate(mainInput):
        print("###---------------------------------------###")
        print("Content compilation started for Type " + str(count + 1))
        result = []
        collectResult = {}
        for inCount, value in enumerate(item):
            # TODO: Compile compatibility in separate dicts in final Enneagram dict
            match inCount:
                case 0:
                    # Add the typeID value
                    print("Compiling typeID")
                    result.append(count + 1)

                    # Get the content for keyWords value, move "and", and add split list to result
                    tList = []
                    temp = str(value[3])
                    changeTemp = temp.replace("and", "")
                    changeTemp = changeTemp.replace(" ", "")
                    tList = changeTemp.split(",")
                    result.append(tList)

                case 1:
                    # Add briefDesc value
                    print("Compiling briefDesc")
                    temp = str(value[1])
                    changeTemp = temp.replace(u"\xa0", " ")
                    result.append(changeTemp)

                    # Add basicFear and basicDesire values
                    print("Compiling basicFear")
                    temp = str(value[2])
                    changeTemp = temp.replace("Basic Fear: ", "")
                    result.append(changeTemp)

                    print("Compiling basicDesire")
                    temp = str(value[3])
                    changeTemp = temp.replace("Basic Desire: ", "")
                    result.append(changeTemp)

                    # Add wing values
                    print("Compiling wings")
                    appendWings = findWings(count)
                    result.append(appendWings)

                    # Add keyMotivations
                    print("Compiling keyMotivations")
                    temp = str(value[6])
                    changeTemp = temp.replace(u"\xa0", "")
                    changeTemp.replace("Key Motivations: ", "")
                    result.append(changeTemp)

                    # CONSIDER: Adding the Direction of Stress and Growth

                case 2:
                    # Add full Type Overview
                    print("Skipping compilation for overview")
                    result.append("Content TBD")

                case 7:
                    # Add addictions values
                    print("Compiling addictions")
                    result.append(value[1])

                case 8:
                    # Add growthRecommendations values
                    print("Compiling growthRecommendations")
                    tList = []
                    tList.append(value[2])
                    tList.append(value[3])
                    tList.append(value[4])
                    tList.append(value[5])
                    tList.append(value[6])
                    result.append(tList)

        # Combine result and keyList into collectResult and dump to output
        for collect_index, collect_value in enumerate(keyList):
            collectResult.update({collect_value: result[collect_index]})
        bufferList.append(collectResult)
    output.update({"mainData": bufferList})

    priCount, secCount, startInt = 1, 1, 1
    for iter in subInput:
        subOutput = {}
        for index_iter, each_iter in enumerate(iter):
            match index_iter:
                case 0:
                    subOutput.update(
                        {"compatibilityMatrix": [priCount, secCount]})
                case 1:
                    if len(iter[index_iter]) == 3:
                        pos_1 = each_iter[1]
                        pos_2 = each_iter[2]
                    elif len(iter[index_iter]) == 7:
                        pos_1 = each_iter[1]
                        pos_2 = each_iter[2]
                        pos_3 = each_iter[4]
                        pos_4 = each_iter[5]
                    else:
                        pos_1 = each_iter[0]
                        pos_2 = each_iter[1]
                    subOutput.update({"goodSpots": f"{pos_1} {pos_2}"})
                case 2:
                    if len(iter[index_iter - 1]) == 7:
                        pos_1 = pos_3
                        pos_2 = pos_4
                    else:
                        pos_1 = each_iter[0]
                        pos_2 = each_iter[1]
                    subOutput.update({"troubleSpots": f"{pos_1} {pos_2}"})
        if secCount < 9:
            secCount += 1
        else:
            priCount += 1
            startInt += 1
            secCount = startInt
        subBufferList.append(subOutput)
    output.update({"subData": subBufferList})

    return output


def main():
    with open("json/enneagramData.json", "r") as f:
        scrapeData = json.load(f)

    mainScrape, subScrape = inputPreProc(scrapeData)
    output = convertScrapedData(mainScrape, subScrape)

    print("Compilation finished... writing file")

    with open("json/enneagramDataCompiled.json", "w") as writefile:
        writefile.write(json.dumps(output, indent=4))
    print("Writing finished")


if __name__ == "__main__":
    main()
