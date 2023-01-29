import time
import asyncio
import json
from socket import timeout
from requests_html import AsyncHTMLSession
from http.client import responses

# Build lists for links and subcontent links
links, subLinks = [], []
for num in range(1, 10):
    links.append(f'https://www.enneagraminstitute.com/type-{num}')

for num in range(1, 10):
    for count in range(1, 10):
        subLinks.append(
            f'https://www.enneagraminstitute.com/relationship-type-{num}-with-type-{count}')


async def connection(asession, link):
    print("Current link: " + str(link))
    r = await asession.get(link)
    output = []
    response = r.html.find('div.sqs-block-content')
    for item in response:
        result = item.text
        if result:
            output.append(result)

    return output


async def main(links, int):
    asession = AsyncHTMLSession()
    if int == 0:
        tasks = (connection(asession, link) for link in links)
    elif int == 1:
        tasks = (connection(asession, link) for link in subLinks)

    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    subWriteKeys = ["title", "positives", "negatives", "privacyPolicy"]
    s_writeKeys = ["title", "briefDesc", "overview", "listen", "levelOfDevelopment", "compatibiltiy",
                   "Misidentification", "Addictions", "growthRecommendations", "learnMore", "privacyPolicy"]
    writeKeys = ["title", "briefDesc", "overview", "listen", "levelOfDevelopment", "Compatibiltiy",
                 "Misidentification", "Addictions", "growthRecommendations", "learnMore", "privacyPolicy"]

    # Collect main data
    start = time.perf_counter()
    results = asyncio.run(main(links, 0))
    end = time.perf_counter() - start
    print(f'Total collection time: {end} seconds')

    # Collect sub data
    start = time.perf_counter()
    s_results = asyncio.run(main(subLinks, 1))
    end = time.perf_counter() - start
    print(f'Total collection time: {end} seconds')

    # Remove redundant entries
    matchStr = 'Privacy Policy\xa0|\xa0Terms of Use\nCopyright 2021, The Enneagram Institute®. All rights Reserved.'
    remList = []
    for s_count, item in enumerate(s_results):
        if item[0] == matchStr:
            remList.append(s_count)
        elif item[0] == "":
            remList.append(s_count)
        else:
            pass

    revRem = list(reversed(remList))
    for index in revRem:
        del s_results[index]

    # Write sub data to file
    subWrite = []
    for count, item in enumerate(s_results):
        writeDict = {}
        for i, v in enumerate(item):
            writeDict.update({subWriteKeys[i]: v})
        subWrite.append(writeDict)

    # Write main data to file
    outWrite = []
    for count, item in enumerate(results):
        writeDict = {}
        for i, v in enumerate(item):
            if count == 2:
                writeDict.update({s_writeKeys[i]: v})
            else:
                writeDict.update({writeKeys[i]: v})
        outWrite.append(writeDict)
    outWrite.append(subWrite)

    with open("json/enneagramData.json", "w") as f:
        f.write(json.dumps(outWrite, indent=4))
