import random  # Added to fix "random" not defined error

# Lists of philosophers
philosophers = [
    "Jean Baudrillard", "Michel Foucault", "Jacques Derrida", "Gilles Deleuze", "Félix Guattari",
    "Judith Butler", "Donna Haraway", "Fredric Jameson", "Jean-François Lyotard", "Slavoj Žižek",
    "Julia Kristeva", "Paul Virilio", "Homi K. Bhabha", "Gayatri Chakravorty Spivak", "Edward Said",
    "Luce Irigaray", "Jacques Lacan", "Henri Lefebvre", "Maurice Blanchot", "Roland Barthes",
    "Richard Rorty", "Stanley Fish", "Terry Eagleton", "Brian Massumi", "Mark Fisher",
    "Franco Berardi", "Nick Land", "Manuel DeLanda", "Rosi Braidotti", "Katherine Hayles",
    "Jean-Luc Nancy", "Giorgio Agamben", "Alain Badiou", "Bruno Latour", "Isabelle Stengers",
    "Avital Ronell", "Catherine Malabou", "Quentin Meillassoux", "Ray Brassier", "Graham Harman",
    "Elizabeth Grosz", "Achille Mbembe", "Byung-Chul Han", "Bernard Stiegler", "Lauren Berlant"
]

# Lists of concepts
concepts = [
    "simulacra", "hyperreality", "the desert of the real", "power/knowledge", "discipline",
    "biopolitics", "genealogy", "deconstruction", "rhizome", "assemblage", "deterritorialization",
    "reterritorialization", "gender performativity", "cyborg", "late capitalism", "pastiche",
    "incredulity towards metanarratives", "spectacle", "dromology", "hybridity", "subaltern",
    "orientalism", "phallogocentrism", "jouissance", "the gaze", "the Other", "heterotopia",
    "simulacrum", "schizoanalysis", "nomadology", "affect theory", "accelerationism",
    "posthumanism", "digital humanities", "neoliberalism", "post-truth",
    "hauntology", "the event", "multitude", "precarity", "necropolitics", "the Anthropocene",
    "capitalocene", "chthulucene", "actor-network theory", "object-oriented ontology",
    "speculative realism", "non-philosophy", "the commons", "cognitive capitalism", "semiocapitalism",
    "control society"
]

# Lists of terms
terms = [
    "discourse", "hegemony", "subjectivity", "intertextuality", "metanarrative",
    "hypertext", "transgression", "fragmentation", "pluralism", "decentering",
    "poststructuralism", "logocentrism", "phallocentrism", "binary opposition",
    "différance", "trace", "supplement", "aporia", "bricolage", "simulacrum",
    "schizophrenia", "deterritorialization", "reterritorialization", "rhizome",
    "assemblage", "affect", "biopower", "biopolitics", "governmentality",
    "panopticism", "heterotopia", "episteme", "genealogy", "archeology",
    "cyborg", "gender performativity", "queer theory", "postcolonialism",
    "subaltern", "hybridity", "diaspora", "transnationalism", "globalization",
    "late capitalism", "neoliberalism", "posthumanism", "digital age",
    "anthropocene", "hyperreality", "simulacra", "spectacle", "dromology",
    "speed", "accelerationism", "affect theory", "new historicism",
    "alterity", "immanence", "transversality", "becoming", "nomadism", "lines of flight",
    "minor literature", "body without organs", "war machine", "smooth space",
    "striated space", "faciality", "refusal of work", "cognitive mapping",
    "cultural logic", "postmodern sublime", "irony", "parody", "pastiche"
]

# Lists of academic vocabulary
academic_vocab = [
    "paradigm", "epistemology", "ontology", "hermeneutics", "semiotics",
    "poststructuralism", "deconstructionism", "critical theory", "cultural studies",
    "gender studies", "queer theory", "postcolonialism", "psychoanalysis", "Marxism",
    "feminism", "structuralism", "modernism", "postmodernism", "globalization",
    "capitalism", "consumerism", "media studies", "technology", "cyberspace",
    "virtual reality", "artificial intelligence", "biopolitics", "necropolitics",
    "affect theory", "new materialism", "materiality", "performativity", "dispositif",
    "agonism", "governmentality", "historicity", "teleology", "immanence",
    "transcendence", "nomadism", "multitude", "precarity", "interdisciplinarity",
    "reflexivity", "situated knowledge", "standpoint theory", "intersectionality"
]

# List of contexts (e.g., settings or frameworks for sentences)
contexts = [
    "in the context of late capitalism",
    "within the framework of postmodernity",
    "through the lens of biopolitics",
    "against the backdrop of globalization"
    # Add more contexts as needed
]

adjectives = [
    "radical", "critical", "postmodern", "deconstructive", "philosophical",
    "ethical", "political", "economic", "social", "cultural", "gendered",
    "racial", "class-based", "discursive", "powerful", "knowledgeable",
    "existential", "real", "modern", "global", "technological", "artistic",
    "literary", "historical", "scientific", "just", "subjective", "hegemonic",
    "biopolitical", "postcolonial", "hybrid", "transnational", "digital"
]

# Dictionary mapping philosophers to their specific concepts
philosopher_concepts = {
    "Jean Baudrillard": ["simulacra", "hyperreality", "the desert of the real"],
    "Michel Foucault": ["power/knowledge", "discipline", "biopolitics"],
    "Jacques Derrida": ["deconstruction", "différance", "trace"],
    "Gilles Deleuze": ["rhizome", "assemblage", "deterritorialization"],
    "Judith Butler": ["gender performativity", "queer theory"]
    # Add more philosophers and their concepts as needed
}

# Lists of first names
first_names = [
    "John", "Jane", "Michael", "Emily", "David", "Sarah", "Robert", "Laura",
    "James", "Maria", "William", "Olivia", "Emma", "Andrew", "Sophia",
    "Matthew", "Isabella", "Daniel", "Charlotte", "Joseph", "Amelia",
    "Ryan", "Mia", "Noah", "Ava", "Jacob", "Lily", "Ethan", "Chloe",
    "Alexander", "Grace", "Benjamin", "Zoey", "Nicholas", "Nora",
    "Samuel", "Scarlett", "Jonathan", "Aria", "Nathan", "Eva",
    "Tyler", "Riley", "Joshua", "Avery", "Brandon", "Sofia",
    "Henry", "Victoria", "Thomas", "Zoe", "Christopher", "Layla",
    "Anthony", "Mila", "Samuel", "Nora", "Oliver", "Harper",
    "Gabriel", "Evelyn", "Lucas", "Abigail", "Mason", "Emily",
    "Logan", "Madison", "Ethan", "Chloe", "Jackson", "Avery",
    "Aiden", "Sophie", "Caleb", "Isabelle", "Wyatt", "Lily",
    "Jayden", "Grace", "Nathan", "Scarlett", "Landon", "Hannah",
    "Grayson", "Zoe", "Owen", "Victoria", "Carter", "Natalie",
    "Dylan", "Brooklyn", "Julian", "Samantha", "Levi", "Audrey",
    "Isaac", "Savannah", "Eli", "Claire", "Max", "Alexa",
    "Liam", "Olivia", "Noah", "Emma", "William", "Ava",
    "James", "Sophia", "Benjamin", "Isabella", "Daniel", "Mia",
    "Matthew", "Charlotte", "Alexander", "Amelia", "Joseph", "Evelyn",
    "David", "Abigail", "Samuel", "Emily", "John", "Madison"
]

# Lists of last names
last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson",
    "White", "Harris", "Martin", "Thompson", "Young", "Allen", "King",
    "Scott", "Green", "Baker", "Adams", "Nelson", "Mitchell", "Perez",
    "Robinson", "Hall", "Walker", "Ward", "Turner", "Watson", "Russell",
    "Stewart", "Morris", "Coleman", "Murphy", "Bailey", "Cook", "Howard",
    "Morgan", "Bell", "Thompson", "Sanders", "Price", "Richardson",
    "Cooper", "Reed", "Kelly", "Shaw", "Ortiz", "Jordan", "Long", "Foster",
    "Jimenez", "Torres", "Kennedy", "Powell", "Simmons", "Brooks", "Ramirez",
    "Flores", "Wood", "Washington", "Cole", "West", "Barnes", "Gray",
    "Henry", "Rose", "Rice", "Morgan", "Burke", "Harvey", "Dixon", "Mills",
    "Warner", "Terry", "Reed", "Bennett", "Rios", "Hart", "Ellis", "Fernandez",
    "Greene", "Mendoza", "Wagner", "Hudson", "Sanchez", "Medina", "Fox",
    "Hawkins", "Price", "Berry", "Montgomery", "Butler", "Daniels", "Fisher",
    "Vaughn", "Davidson", "Castillo", "Oliver", "Pena", "Hunter", "Cross",
    "Lawson", "Meyer", "Peters", "Spencer", "Palmer", "Wallace", "Duncan",
    "Fleming", "Oneill", "Webb", "Welch", "Ochoa", "Wilkins", "Barker",
    "Holt", "Huff", "Donovan", "Mcbride", "Blackburn", "Bowers", "Mccoy",
    "Mckay", "Raymond", "Robbins", "Rodriguez", "Thornton", "Valdez",
    "Wiggins", "Albert", "Castro", "Daugherty", "Hickman", "Hooper",
    "Kline", "Mccall", "Melendez", "Mullen", "Rodriguez", "Sampson",
    "Shepard", "Small", "Stokes", "Trujillo", "Waters", "Wilkerson",
    "Wise", "Woodard", "Patel", "Kumar", "Singh", "Choi", "Kim", "Lee",
    "Park", "Nguyen", "Tran", "Pham", "Li", "Wang", "Zhang", "Chen",
    "Liu", "Yang", "Huang", "Zhao", "Zhou", "Wu", "Xu", "Sun", "Ma",
    "Zhu", "Hu", "Guo", "He", "Gao", "Lin", "Luo", "Tang", "Yu", "Cao",
    "Fang", "Ren", "Liang", "Xie", "Song", "Zheng", "Han", "Zou", "Pan",
    "Jiang", "Wei", "Ding", "Chang", "Qian", "Shen", "Jin", "Qiu", "Lu",
    "Wang", "Zhang", "Chen", "Liu", "Yang", "Huang", "Zhao", "Zhou", "Wu",
    "Xu", "Sun", "Ma", "Zhu", "Hu", "Guo", "He", "Gao", "Lin", "Luo",
    "Tang", "Yu", "Cao", "Fang", "Ren", "Liang", "Xie", "Song", "Zheng",
    "Han", "Zou", "Pan", "Jiang", "Wei", "Ding", "Chang", "Qian", "Shen",
    "Jin", "Qiu", "Lu"
]

# Lists of years
years = list(range(1950, 2025))

# Lists of publishers
publishers = [
    "Oxford University Press", "Cambridge University Press",
    "Harvard University Press", "Yale University Press",
    "Stanford University Press", "University of California Press",
    "University of Chicago Press", "Columbia University Press",
    "MIT Press", "Routledge", "Palgrave Macmillan", "Sage Publications",
    "Wiley-Blackwell", "Elsevier", "Taylor & Francis", "Bloomsbury Academic",
    "Duke University Press", "Cornell University Press", "Johns Hopkins University Press",
    "University of Minnesota Press", "University of Michigan Press",
    "University of Pennsylvania Press", "University of Texas Press",
    "University of Washington Press", "University of Wisconsin Press",
    "New York University Press", "University of Toronto Press",
    "McGill-Queen's University Press", "Edinburgh University Press",
    "Manchester University Press", "Ashgate Publishing", "Routledge-Cavendish",
    "Kluwer Academic Press", "Brill Academic Press", "Peter Lang Publishing",
    "Lexington Books", "Rowman & Littlefield", "Continuum International Publishing Group",
    "Zed Books", "Verso Books", "Pluto Press", "Haymarket Books",
    "Duke University Press Books", "University of Illinois Press",
    "University of Nebraska Press", "University of North Carolina Press",
    "University of Georgia Press", "Louisiana State University Press",
    "Mississippi University Press", "University of Alabama Press",
    "University of Florida Press", "University of Iowa Press",
    "University of Kansas Press", "University of New Mexico Press",
    "University of Oklahoma Press", "University of South Carolina Press",
    "University of Utah Press", "University of Arizona Press",
    "University of Colorado Press", "University of Idaho Press",
    "University of Nevada Press", "University of New Mexico Press",
    "University of Oregon Press", "University of Washington Press",
    "Springer", "Nature Publishing Group", "Wiley", "SAGE Journals",
    "APA Journals", "IEEE Xplore", "ACM Digital Library", "Emerald Insight"
]

# Lists of title words
title_words = [
    "Exploring", "Understanding", "Re-examining", "Critical", "Postmodern",
    "Deconstructing", "The Role of", "Intersections of", "Cultural",
    "Philosophical", "Ethical", "Political", "Economic", "Social",
    "Gender", "Race", "Class", "Identity", "Discourse", "Power",
    "Knowledge", "Truth", "Being", "Existence", "Reality",
    "Modernity", "Postmodernity", "Globalization", "Technology",
    "Media", "Art", "Literature", "History", "Science", "Ethics",
    "Justice", "Freedom", "Subjectivity", "Hegemony", "Alterity",
    "Immanence", "Transversality", "Becoming", "Nomadism", "Lines",
    "Minor", "Body", "War", "Smooth", "Striated", "Faciality",
    "Refusal", "Cognitive", "Cultural", "Logic", "Sublime", "Irony",
    "Parody", "Pastiche", "Biopolitics", "Genealogy", "Archeology",
    "Cyborg", "Performativity", "Queer", "Postcolonial", "Subaltern",
    "Hybridity", "Diaspora", "Transnational", "Global", "Late",
    "Neoliberal", "Posthuman", "Digital", "Anthropocene", "Hyperreality",
    "Spectacle", "Dromology", "Speed", "Acceleration", "Affect",
    "New", "Historic", "Alterity", "Immanence", "Transversality",
    "Becoming", "Nomadism", "Lines", "Flight", "Literature", "Body",
    "Without", "Organs", "Machine", "Space", "Faciality", "Refusal",
    "Work", "Mapping", "Logic", "Sublime", "Irony", "Parody", "Pastiche"
]

# Function to generate a random title
def generate_title():
    word1 = random.choice(title_words)
    word2 = random.choice(title_words)
    return f"{word1} {word2}"