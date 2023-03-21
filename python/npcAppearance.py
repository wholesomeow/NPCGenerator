import random


class npcAppearance:
    def __init__(self, npcInfoPreAppearance):
        self.appearance = {"Height": "",
                           "Weight": "",
                           "Age": "",
                           "Gender": "",
                           "Race": "",
                           "Coverings": None,
                           "Face": "",
                           "Body": ""}
        self.infoList = npcInfoPreAppearance

        self.appearance.update({"Race": self.infoList[0]})
        self.appearance.update({"Age": self.infoList[1]})
        self.appearance.update({"Gender": self.infoList[5]})

    def imperialToMetric(self, imperial, mode):
        # Converts input imperial to metric based on mode
        # Mode 0 is inches to cm
        # Mode 1 is lbs to kg

        metric = 0
        match mode:
            case 0:
                metric = imperial * 2.54
            case 1:
                metric = imperial * 0.453592

        return metric

    def chooseCoveringColor(self, covering):
        description = {}

        coveringType = ['Hair', 'Fur', 'Feathers']
        selection = []

        descriptor_NonSurface = ['Beautiful', 'Colorful', 'Elegant', 'Bright', 'Shiny', 'Radiant', 'Symmetrical', 'Luminous', 'Lushious', 'Brilliant',
                                 'Brushed', 'Flawless', 'Striking', 'Stunning', 'Vibrant', 'Mesmerizing', 'Serene', 'Graceful', 'Majestic',
                                 'Exquisite', 'Eye-catching', 'Sophisticated', 'Harmonious', 'Refreshing', 'Charming', 'Ugly', 'Dull', 'Drab',
                                 'Patchy', 'Thinning', 'Faded', 'Frizzy', 'Dingy', 'Greying', 'Messy', 'Distracting', 'Unappealing', 'Unsightly',
                                 'Cluttered', 'Chaotic', 'Matted', 'Gaudy', 'Homely', 'Tasteless', 'Tarnished', 'Dated', 'Tired', 'Overwhelming',
                                 'Balding', 'Sun-Damaged']

        descriptor_Surface = ['Glossy', 'Sleek', 'Smooth', 'Velvety', 'Lustrous', 'Iridescent', 'Reflective', 'Glowing', 'Pearlescent', 'Translucent',
                              'Sheer', 'Flawless', 'Clear', 'Radiant', 'Sparkling', 'Bright', 'Shimmering', 'Crystalline', 'Transparent', 'Colorful',
                              'Vivid', 'Radiant', 'Pristine', 'Polished', 'Clean', 'Dull', 'Scratched', 'Dingy', 'Streaked', 'Dirty', 'Faded', 'Patchy',
                              'Scuffed', 'Blotchy', 'Smudged', 'Mottled', 'Discolored', 'Uneven', 'Splotchy', 'Stained', 'Muddy', 'Cloudy', 'Opaque',
                              'Chipped', 'Blemished', 'Scarred', 'Pitted', 'Dented', 'Peeling', 'Cracked']

        length = ['Short', 'Medium Length', 'Long']

        style = ['Up', 'Down', 'Pulled Back', 'Slicked Back',
                 'Center Part', 'Side Part', 'Braided']

        texture_NonSurface = ['Silky', 'Smooth', 'Soft', 'Fluffy', 'Puffy', 'Velvety', 'Fuzzy', 'Thick', 'Lush', 'Shiny', 'Lustrous', 'Glossy', 'Gleaming', 'Sleek',
                              'Wavy', 'Curly', 'Bouncy', 'Voluminous', 'Feathery', 'Plush', 'Downy', 'Satin-like', 'Lacy', 'Spongy', 'Crispy', 'Frizzy', 'Tangled',
                              'Kinky', 'Coarse', 'Thick', 'Matted', 'Tough', 'Scraggly', 'Unkempt', 'Messy', 'Greasy', 'Oily', 'Dirty', 'Grubby', 'Filthy', 'Matted',
                              'Mangy', 'Ratty', 'Dull', 'Lifeless', 'Brittle', 'Dry', 'Straw-like', 'Fried', 'Coarse', 'Rough', 'Scruffy', 'Sparse', 'Patchy', 'Ragged']

        texture_Surface = ['Smooth', 'Silky', 'Supple', 'Elastic', 'Plump', 'Soft', 'Velvety', 'Satiny', 'Taut', 'Firm', 'Toned', 'Radiant', 'Healthy', 'Glowing',
                           'Flawless', 'Clear', 'Luminous', 'Fresh', 'Rosy', 'Glossy', 'Pristine', 'Dewy', 'Youthful', 'Sleek', 'Sculpted', 'Wrinkled', 'Sagging',
                           'Pitted', 'Bumpy', 'Rough', 'Scaly', 'Dry', 'Flaky', 'Patchy', 'Blotchy', 'Mottled', 'Pocked', 'Scarred', 'Damaged', 'Irritated', 'Inflamed',
                           'Acne-prone', 'Blemished', 'Uneven', 'Dull', 'Lifeless', 'Pale', 'Sallow', 'Gray', 'Sickly', 'Waxy', 'Greasy', 'Oily', 'Shiny']

        color = ['Black', 'Brown', 'Blonde', 'Red', 'Chestnut', 'Copper', 'Auburn', 'Ginger', 'Platinum', 'Silver', 'White', 'Golden', 'Midnight', 'Obsidian',
                 'Raven', 'Ashen', 'Steel', 'Sand', 'Sunset', 'Blush', 'Rose', 'Lilac', 'Amethyst', 'Emerald', 'Forest', 'Mint', 'Ocean', 'Sky', 'Sapphire',
                 'Turquoise', 'Rainbow']

        color_SkinFlesh = ['Alabaster', 'Ecru', 'Ivory', 'Sandy', 'Golden', 'Blush', 'Rose', 'Beige', 'Taupe', 'Clay', 'Tan', 'Hazel', 'Brown', 'Umber', 'Bronze',
                           'Teak', 'Walnut', 'Mahogany', 'Ebony', 'Onyx', 'Gold', 'Copper', 'Tawny', 'Sienna', 'Ochre', 'Olive']

        color_MetalicScales = ['Black', 'Blue', 'Brass', 'Bronze',
                               'Copper', 'Gold', 'Green', 'Red', 'Silver', 'White']

        # Selects random values for each description value in the above order
        selection.append(random.randint(0, 49))
        selection.append(random.randint(0, 2))
        selection.append(random.randint(0, 6))
        selection.append(random.randint(0, 49))
        selection.append(random.randint(0, 30))
        selection.append(random.randint(0, 25))
        selection.append(random.randint(0, 9))

        if covering in coveringType:
            description.update({"Length": length[selection[1]]})
            description.update(
                {"Descriptor": descriptor_NonSurface[selection[0]]})
            description.update({"Type": covering})
            description.update({"Style": style[selection[2]]})
            description.update({"Texture": texture_NonSurface[selection[3]]})
        else:
            description.update(
                {"Descriptor": descriptor_Surface[selection[0]]})
            description.update({"Texture": texture_Surface[selection[3]]})

        if covering in coveringType or "Horns" or "Shell":
            description.update({"Color": color[selection[4]]})
        elif covering == "Skin" or "Flesh":
            description.update({"Color": color_SkinFlesh[selection[5]]})
        elif covering == "Metal" or "Scales":
            description.update({"Color": color_MetalicScales[selection[6]]})

        return description

    def generateBodyType(self, height, weight):
        bodyType = ""
        bodyID = 0

        meters = height / 100
        BMI = round((weight / meters**2), 2)

        # Selects a level of health for how the person treats their body
        # 1 = In shape, 2 = Average, 3 = Not in shape
        healthLevel = random.randint(1, 3)

        if BMI <= 18.5:
            bodyID = 0
        elif 18.5 < BMI <= 24.9:
            bodyID = 1
        elif 25 < BMI <= 29.29:
            bodyID = 2
        else:
            bodyID = 3

        match healthLevel:
            case 1:
                if bodyID == 0:
                    bodyType = "Sinewy"
                elif bodyID == 1:
                    bodyType = "Lean"
                elif bodyID == 2:
                    bodyType = "Buff"
                else:
                    bodyType = "Massive"
            case 2:
                if bodyID == 0:
                    bodyType = "Thin"
                elif bodyID == 1:
                    bodyType = "Average"
                elif bodyID == 2:
                    bodyType = "Slightly Larger"
                else:
                    bodyType = "Larger"
            case 3:
                if bodyID == 0:
                    bodyType = "Reedy"
                elif bodyID == 1:
                    bodyType = "Soft"
                elif bodyID == 2:
                    bodyType = "Plump"
                else:
                    bodyType = "Fat"

        return bodyType

    def generateFace(self, charisma):
        face = {}

        # Chooses one or more colors for the eyes
        eyes = ""
        eyebrows = ""
        browline = ""
        eyeColorChoices = ['Brown', 'Blue', 'Green', 'Hazel', 'Grey', 'Amber', 'Red', 'Black', 'Violet', 'Gold', 'Silver',
                           'Pink', 'Yellow', 'Orange', 'Turquoise', 'Crystal', 'Ice blue', 'Dark green', 'Ruby red', 'Sky blue']
        eyeShapes = ['Almond-shaped', 'Round', 'Hooded', 'Upturned', 'Downturned',
                     'Deep-set', 'Prominent', 'Close-set', 'Wide-set', 'Monolid']
        browChoices = ['Thick', 'Thin', 'Arched', 'Straight', 'Bushy', 'Sparse', 'Curved', 'Angular', 'Defined', 'Delicate', 'Fleeting', 'Natural', 'Plucked',
                       'Trimmed', 'Unruly', 'Rugged', 'Tapered', 'Untamed', 'Wide-set', 'Close-set', 'Low-lying', 'High-arched', 'Matching', 'Asymmetrical', 'Fierce']
        browlineChoices = ['Deep-set', 'Sunken', 'Prominent', 'Hooded',
                           'Furrowed', 'Smooth', 'Rounded', 'Angular', 'Sharp', 'Sloping']
        eyeColor = []

        chance = random.randint(1, 100)
        if chance >= 65:
            for c in range(2):
                r = random.randint(0, 19)
                eyeColor.append(eyeColorChoices[r])
        else:
            r = random.randint(0, 19)
            eyeColor.append(eyeColorChoices[r])

        r = random.randint(0, 9)
        eyeShape = eyeShapes[r]
        browline = browlineChoices[r]
        r = random.randint(0, 24)
        eyebrows = browChoices[r]

        if len(eyeColor) == 1:
            eyes = f"{eyeShape} {eyeColor[0]} eyes"
        else:
            eyes = f"{eyeShape} {eyeColor[0]} eyes with flecks of {eyeColor[1]}"

        # Generates keywords for the description of the face
        faceGeneral = ""
        if charisma < 7:
            faceGeneral = "Unattractive"
        elif charisma >= 7 and charisma <= 13:
            faceGeneral = "Average"
        elif charisma >= 14 and charisma <= 16:
            faceGeneral = "Attractive"
        elif charisma >= 17 and charisma <= 20:
            faceGeneral = "Gorgeous"

        nose = ""
        noseChoices = ['Snub', 'Crooked', 'Prominant', 'Button', 'Sharp', 'Upturned', 'Flat', 'Wide', 'Narrow', 'Long', 'Bulbous', 'Pointed',
                       'Broken', 'Proud', 'Thin', 'Flared', 'Turned-up', 'Turned-down', 'Hooked', 'Snotty', 'Deviated', 'Pug', 'Beaky', 'Flared']
        r = random.randint(0, 23)
        nose = noseChoices[r]

        mouth = ""
        mouthChoices = ['Full', 'Thin', 'Wide', 'Narrow', 'Small', 'Large', 'Pursed', 'Plump', 'Thin-lipped', 'Full-lipped', 'Tight', 'Loose', 'Curved',
                        'Straight', 'Uneven', 'Perfectly shaped', 'Crooked', 'Downturned', 'Upturned', 'Gap-toothed', 'Toothless', 'Bitten', 'Chapped', 'Moist', 'Dry']
        r = random.randint(0, 24)
        mouth = mouthChoices[r]

        ears = ""
        earChoices = ['Small', 'Large', 'Pointy', 'Round', 'Protruding', 'Flat', 'Attached', 'Detached', 'Lobed', 'Unlobed', 'Hairy', 'Smooth',
                      'Wrinkled', 'Scarred', 'Pierced', 'Tattooed', 'Damaged', 'Deformed', 'Elf-like', 'Torn', 'Ragged', 'Nicked', 'Dirty', 'Clean', 'Unblemished']
        r = random.randint(0, 24)
        ears = earChoices[r]

        skin = ""
        skinTexture = ['Smooth', 'Silky', 'Supple', 'Elastic', 'Plump', 'Soft', 'Velvety', 'Satiny', 'Taut', 'Firm', 'Toned', 'Radiant', 'Healthy', 'Glowing',
                       'Flawless', 'Clear', 'Luminous', 'Fresh', 'Rosy', 'Glossy', 'Pristine', 'Dewy', 'Youthful', 'Sleek', 'Sculpted', 'Wrinkled', 'Sagging',
                       'Pitted', 'Bumpy', 'Rough', 'Scaly', 'Dry', 'Flaky', 'Patchy', 'Blotchy', 'Mottled', 'Pocked', 'Scarred', 'Damaged', 'Irritated', 'Inflamed',
                       'Acne-prone', 'Blemished', 'Uneven', 'Dull', 'Lifeless', 'Pale', 'Sallow', 'Gray', 'Sickly', 'Waxy', 'Greasy', 'Oily', 'Shiny']
        r = random.randint(0, 30)
        skin = skinTexture[r]

        face.update({"Overview": faceGeneral})
        face.update({"Eyes": eyes})
        face.update({"Brows": eyebrows})
        face.update({"Browline": browline})
        face.update({"Nose": nose})
        face.update({"Lips": mouth})
        face.update({"Ears": ears})
        face.update({"Skin": skin})

        return face

    def generateAppearance(self):
        ft, inch, lbs = 0, 0, 0
        coveringlist = self.infoList[2]
        charisma = self.infoList[4]

        # Generate height and weight of the NPC
        if self.infoList[3] == "Medium":
            ft = random.randint(4, 7)
            inch = random.randint(0, 11)
            lbs = random.randint(110, 250)
        else:
            ft = random.randint(2, 3)
            inch = random.randint(0, 11)
            lbs = random.randint(75, 110)

        # Convert the imperial numbers to metric and calculate BMI + resulting body type
        inches = (ft * 12) + inch

        cm = self.imperialToMetric(inches, 0)
        self.appearance.update({"Height": f"{ft}ft {inch}in / {cm}cm"})

        kg = self.imperialToMetric(lbs, 1)
        self.appearance.update({"Weight": f"{lbs}lbs / {kg}kg"})

        bodyType = self.generateBodyType(cm, kg)
        self.appearance.update({"Body": f"{bodyType}"})

        # Generate a dict that has desciptive information on the coverings (Hair, Fur, Scales) of the NPC
        if len(coveringlist) == 1:
            coveringDescription = self.chooseCoveringColor(coveringlist[0])
            self.appearance.update({"Coverings": coveringDescription})
        else:
            tempList = []
            for i in coveringlist:
                coveringDescription = self.chooseCoveringColor(i)
                tempList.append(coveringDescription)
            self.appearance.update({"Coverings": tempList})

        npcFace = self.generateFace(charisma)
        self.appearance.update({"Face": npcFace})

        return

    # TODO: Add more detail for the different types of occupations and add options for masc/fem clothing
    # Creates the NPC outfit based on status
    # Each clothing list covers the folling slots in order: Feet, Legs, Torso, Over Torso, Head
    def generateClothing(self, jobStatus):
        clothingIndex = 0
        clothing = {}
        clothingSlots = ["Feet", "Legs", "Torso", "OverTorso", "Head"]
        clothingTypes = ["Rags", "Plain", "Fine",
                         "Exquisite", "Regal", "Imperial"]

        rags_clothing = [
            ['Tattered shoes'],
            ['Ragged pants', 'Torn leggings'],
            ['Threadbare shirt'],
            ['Ripped vest', ''],
            []
        ]

        plain_clothing = [
            ['Worn-out boots', 'Old shoes'],
            ['Plain Trousers', 'Simple skirt'],
            ['Plain shirt', 'Tunic'],
            ['Simple jacket', 'Plain robe'],
            ['Hood', 'Cap']
        ]

        fine_clothing = [
            ['Leather shoes', 'Polished boots'],
            ['Silk pants', 'Embroidered skirt'],
            ['Silk shirt', 'Fancy blouse'],
            ['Fine vest', 'Fur-lined coat'],
            ['Elegant hat', 'Fancy headband']
        ]

        exquisite_clothing = [
            ['Jeweled shoes', 'Enchanted boots'],
            ['Ornate pants', 'Luxurious gown'],
            ['Enchanted shirt', 'Exquisite blouse'],
            ['Enchanted cloak', 'Magical robe'],
            ['Jeweled tiara', 'Enchanted circlet']
        ]

        regal_clothing = [
            ['Enchanted boots', 'Golden shoes'],
            ['Royal trousers', 'Silk robe'],
            ['Embellished tunic', 'Regal blouse'],
            ['Royal cloak', 'Dragonhide coat'],
            ['Regal crown', 'Golden diadem']
        ]

        imperial_clothing = [
            ['Divine boots of speed', 'Legendary greaves'],
            ['Imperial pants', 'Imperial robe'],
            ['Imperial tunic', 'Divine blouse'],
            ['Imperial cloak of protection', 'Legendary coat of arms'],
            ['Imperial crown of power', 'Divine circlet of wisdom']
        ]

        clothingOptions = [
            rags_clothing,
            plain_clothing,
            fine_clothing,
            exquisite_clothing,
            regal_clothing,
            imperial_clothing
        ]

        if jobStatus <= 3:
            clothingIndex = 0
        elif jobStatus >= 4 and jobStatus <= 5:
            clothingIndex = 1
        elif jobStatus >= 6 and jobStatus <= 7:
            clothingIndex = 2
        elif jobStatus >= 8 and jobStatus <= 10:
            clothingIndex = 3
        elif jobStatus >= 11 and jobStatus <= 13:
            clothingIndex = 4
        else:
            clothingIndex = 5

        npcClothingOptions = clothingOptions[clothingIndex]
        for i, j in enumerate(npcClothingOptions):
            if len(j) > 1:
                r = random.randint(0, len(j))
                r -= 1
                clothing.update({clothingSlots[i]: j[r]})
            elif len(j) == 1:
                clothing.update({clothingSlots[i]: j})

        self.appearance.update({"Clothing": clothing})

        return

    # Generates additional language to add more detail to NPC Outfit based on mental health
    def updateClothing(self, mentalHealth):
        return
