# NPCGenerator

This is a webbased tool to be used for generating more detailed NPCs for your games. Either adhoc when your party decides they want to talk to some random person in a crowd that you didn't plan for or when you need help filling out an encounter with background people that might need to participate in the RP.

The tool is written in python with the backend and API served in Flask, with the frontend in HTML/CSS/Javascript.

When a user presses the "Generate" button, a NPC is created with a selected Race, Subrace, Job, Sexual Orientation (for when the Bard tries to seduce them), and more as the basic information. Where the tool really shines is in creating information on the NPCs personality: What their general personality is like, how they view the world, their overal mental state, and how they interact with other people.

As the project is developed more, the amount of information will be expanded on as well as become both more targeted and robust. Hopefully GMs will be able to use this tool to develop very robust NPCs on the fly that can provide a solid foundation for them to focus on the storytelling experience for their parties.

## How It Works

When a user presses the "Generate" button, the basic information is first collected from several datasets to generate a base for the NPC. These are things like Race, Subrace, Gender, Sex, Sexual Orientation, and their Job.

Along with their Job are things like Job Status and Societal Status to help give the GM and indication of the NPCs status and reputation in the world. **This is not yet fully implemented**

After that information is compiled, the personality data is compiled. This tool uses a few personality test frameworks to provide a sort of baseline that is grounded in reality. The primary framework being the [Enneagram Personality](https://www.enneagraminstitute.com/how-the-enneagram-system-works) framwork. It randomly selects one of the 9 personality architypes and then selects that types "Wing", along with a Blend percentage to create some nuance in the personality type created. For more information on why that framework was chosen, read the Medium article here. **Article coming soon**

Once the personality data is compiled, it is turned into a prompt and sent to GPT-3 for the data output. This is temporary and an NLP ML program will be created once a satisfactory dataset has been created.

Once GPT-3 returns the output, this is stored in a json object and dumped on screen.

Nice and easy.

## Roadmap

Alpha 0.x.x

- [x] NPC Information JSON creation
- [x] NPC JSON to GPT-3
- [ ] API Creation with Flask
- [ ] Basic Web Page to display result of API call
- [ ] Implement NLP AI for Name Generation

Beta 1.x.x

- [ ] Implement Status and Reputation systems
- [ ] Implement Stress and Relationship systems
- [ ] Create Login and Save NPC functions
- [ ] Implement NLP AI to replace GPT-3

Outside of the tool itself, a DnD-inspired table will be created for GMs that want to use a more traditional method of NPC creation will be created as well. This table (or series of tables) will take the process that the application goes through automatically and will allow GMs to curate the NPC creation process and let their imaginations create the final NPC.

## Contact

If anyone wants to get in contact with me, feel free to DM me on Twitter.

https://twitter.com/mk_wholesome

## Acknowledgments

- https://github.com/miethe for their [DnD Character Generator](https://github.com/miethe/DnD-Character-Generator) that inspired some of the early design I had, provided me a starting point for the data I generated, and giving me their dice rolling script so I didn't have to labour over doing the math myself.
- https://github.com/bvezilic for their [DnD Name Generator](https://github.com/bvezilic/DnD-name-generator) that also served as a great point of inspiration and guidance for some of the early design.
- The Enneagram Institue for providing a great amount of data to start with.
- John Trubys _The Anatomy of Story_ for giving me a great framework to creating interesting characters for interesting storytelling. Please go buy the book.
- My buddy Phil for helping me figure out how best to make this project happen and avoid all the pitfalls I really wanted to throw myself down.
