import random
import matplotlib.pyplot as plt
import numpy as np

# Define the questions and their corresponding dimensions
questions = {
    "Rationality": [
        "The natural world can be fully explained by science and reason.",
        "Logic and evidence should be the primary guides for decision-making.",
        "The human mind can be reduced to its physical components and processes.",
        "I think that artificial intelligence will eventually surpass human intelligence.",
        "I think that space exploration is essential for human progress.",
        "I believe in the concept of a technological singularity.",
    ],
    "Mysticism": [
        "I believe in the concept of fate or destiny.",
        "I think that dreams can provide insight into the subconscious mind.",
        "I believe in the concept of a higher power or divine being.",
        "I think that meditation or prayer can provide a sense of inner peace.",
        "I believe in the concept of an afterlife or spiritual realm.",
        "I think that astrology can provide insight into personality and behavior.",
        "I believe in the concept of reincarnation.",
        "I believe in the concept of a collective unconscious.",
        "I think that mysticism can provide a sense of connection to something greater than oneself."
    ],
    "Individualism": [
        "Individuals should prioritize their own interests and goals.",
        "I think that people should be responsible for their own financial well-being.",
        "Personal freedom is more important than social harmony.",
        "Individuals should be free to pursue their own happiness.",
        "Individual rights are more important than collective security.",
        "I think that gun ownership is a fundamental right.",
        "I believe in the concept of a laissez-faire economy.",
        "I think that individuals should be free to make their own choices about their own bodies.",
        "I believe in the concept of a minimalist government.",
        "I think that individualism is more important than collectivism."
    ],
    "Collectivism": [
        "The needs of the community should take precedence over individual desires.",
        "I believe in the concept of a 'common good' that benefits everyone.",
        "I think that people should be willing to make sacrifices for the greater good.",
        "The government has a responsibility to provide a social safety net.",
        "Collective well-being is more important than individual freedom.",
        "I think that immigration should be restricted to protect the interests of native-born citizens.",
        "I believe in the concept of a welfare state.",
        "I think that collective bargaining is essential for worker rights.",
        "I believe in the concept of a progressive tax system.",
        "I think that collectivism is more important than individualism."
    ],
    "Absolutism": [
        "There are objective moral standards that apply to everyone.",
        "I believe in the concept of absolute truth.",
        "Certain actions are always right or always wrong, regardless of circumstances.",
        "I think that morality is based on universal principles.",
        "I believe in the concept of a single, objective reality.",
        "I believe in the concept of a strict moral code.",
        "I believe in the concept of a universal moral law.",
        "I think that absolutism is more important than relativism."
    ],
    "Relativism": [
        "What is right or wrong depends on the cultural context.",
        "Truth is relative and depends on personal perspective.",
        "I think that morality is a product of cultural and historical context.",
        "What is true or false depends on the individual's point of view.",
        "Reality is constructed by individual perceptions and interpretations.",
        "I believe in the concept of moral relativism.",
        "I think that certain behaviors are acceptable in certain contexts.",
        "I believe in the concept of situational ethics.",
        "I think that relativism is more important than absolutism."
    ],
    "Freedom": [
        "Individuals should be free to make their own choices, as long as they harm no one else.",
        "I think that economic freedom is essential for human flourishing.",
        "Personal freedom is more important than national security.",
        "Individuals should be free to express their opinions, even if they are unpopular.",
        "I believe in the concept of a free market economy.",
        "I think that encryption should be unrestricted to protect individual privacy.",
        "I think that prostitution should be decriminalized and regulated like any other industry.",
        "I believe in the concept of a minimalist government.",
        "I think that individuals should be free to make their own decisions about their own bodies.",
        "I think that freedom is more important than security."
    ],
    "Coercion": [
        "The government has a responsibility to protect people from themselves.",
        "I believe in the concept of a 'nanny state' that protects people from harm.",
        "The government should censor certain types of speech or expression.",
        "I think that the government should regulate the economy to ensure fairness and equality.",
        "The state should regulate personal behavior for the greater good.",
        "I think that money laundering should be criminalized to prevent financial crimes.",
        "I believe in the concept of a surveillance state.",
        "I think that certain types of speech or expression should be restricted for the greater good.",
        "I think that coercion is more important than freedom."
    ]
}
count = 0
# Initialize scores for each dimension
scores = {
    "Rationality": 0,
    "Mysticism": 0,
    "Individualism": 0,
    "Collectivism": 0,
    "Absolutism": 0,
    "Relativism": 0,
    "Freedom": 0,
    "Coercion": 0
}

# Ask questions and record responses
#questions_list = [(dimension, question) for dimension, questions in questions.items() for question in questions]
questions_list = []
for dimension in questions:
    slist = questions[dimension]
    random.shuffle(slist)
    print(slist)
    for i in range(5):
        questions_list.append((dimension, slist[i]))

random.shuffle(questions_list)

for dimension, question in questions_list:
    count += 1
    print("question:  ", count)
    print(question)
    response = input("Please enter a number from 1 to 5, where 1 is 'strongly disagree' and 5 is 'strongly agree': ")
    while not response.isdigit() or not 1 <= int(response) <= 5:
        response = input("Invalid input. Please enter a number from 1 to 5: ")
    scores[dimension] += int(response)
    
# Calculate average score for each dimension
for dimension in scores:
    scores[dimension] /= len(questions[dimension])

# Plot radar graph
angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
stats = [scores["Rationality"], scores["Individualism"], scores["Absolutism"], scores["Freedom"], scores["Mysticism"], scores["Collectivism"], scores["Relativism"], scores["Coercion"]]

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, polar=True)

ax.plot(angles, stats, 'o-', linewidth=2)
ax.fill(angles, stats, alpha=0.25)

ax.set_thetagrids(angles * 180/np.pi, ["Rationality", "Individualism", "Absolutism", "Freedom", "Mysticism", "Collectivism", "Relativism", "Coercion"])
ax.set_ylim(0,5)
ax.set_title("Philosophical Leanings", va='bottom')

plt.show()