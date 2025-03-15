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

first_names = ["John", "Jane", "Michael", "Emily", "David", "Sarah", "Robert", "Laura", "James", "Maria"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
adjectives = ["Critical", "Postmodern", "Deconstructive", "Feminist", "Marxist", "Psychoanalytic", "Radical", "Speculative"]
nouns = ["Perspectives", "Theories", "Readings", "Approaches", "Interpretations", "Analyses", "Discourses", "Frameworks"]
theories = ["Postmodernism", "Deconstruction", "Poststructuralism", "Critical Theory", "Cultural Studies", "Queer Theory", "Postcolonial Theory"]
contexts = ["Late Capitalism", "Globalization", "The Digital Age", "Consumer Society", "The Anthropocene", "Posthumanism", "Neoliberalism"]
publishers = ["Academic Press", "University Publishing", "Scholarly Books", "Intellectual Editions", "Critical Texts", "Theory House"]

# Mapping philosophers to their key concepts and fields (partial for brevity; expand as needed)
philosopher_concepts = {
    "Jean Baudrillard": (["simulacra", "hyperreality", "the desert of the real", "seduction", "spectacle"], "cultural studies"),
    "Michel Foucault": (["power/knowledge", "biopolitics", "genealogy", "episteme", "panopticon", "heterotopia"], "cultural studies"),
    "Jacques Derrida": (["deconstruction", "différance", "trace", "supplement", "aporia"], "literary theory"),
    "Gilles Deleuze": (["rhizome", "assemblage", "deterritorialization", "nomadology", "schizoanalysis"], "philosophy"),
    "Félix Guattari": (["rhizome", "assemblage", "deterritorialization", "schizoanalysis"], "philosophy"),
    "Judith Butler": (["gender performativity", "queer theory"], "gender studies"),
    "Donna Haraway": (["cyborg", "chthulucene", "situated knowledge"], "science and technology studies"),
    "Fredric Jameson": (["late capitalism", "pastiche", "cognitive mapping"], "cultural studies"),
    "Jean-François Lyotard": (["incredulity towards metanarratives", "postmodern sublime"], "philosophy"),
    "Slavoj Žižek": (["the Real", "ideology", "jouissance"], "psychoanalysis"),
    "Jean-Luc Nancy": (["community", "being-with"], "philosophy"),
    "Giorgio Agamben": (["homo sacer", "state of exception", "bare life"], "political philosophy"),
    "Alain Badiou": (["the event", "truth", "being"], "philosophy"),
    "Bruno Latour": (["actor-network theory", "non-modern"], "science and technology studies"),
    "Achille Mbembe": (["necropolitics", "postcolony"], "postcolonialism")
    # Add remaining philosophers similarly
}

# Possible body section titles
body_section_titles = [
    "Theoretical Foundations",
    "Historical Context",
    "Key Concepts",
    "Critical Analysis",
    "Case Studies",
    "Methodological Approaches",
    "Comparative Perspectives",
    "Future Directions"
]