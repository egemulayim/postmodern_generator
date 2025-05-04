"""
A module for storing and retrieving quotes from postmodern philosophers.
This module provides a dictionary of quotes organized by philosopher, 
designed to support academic writing and discussions on postmodern philosophy.
"""

# Quotes dictionary: maps philosopher full names to lists of their quotes
quotes = {
    "Jacques Derrida": [
        "There is nothing outside the text.",
        "Deconstruction is not a method, and cannot be transformed into one.",
        "The center is not a fixed locus but a function, a sort of non-locus in which an infinite number of sign-substitutions come into play.",
        "The trace is not a presence but the simulacrum of a presence that dislocates itself, displaces itself.",
        "The supplement is neither a presence nor an absence. No ontology can think its operation.",
        "Every sign, linguistic or nonlinguistic, spoken or written, as a small or large unity, can be cited, put between quotation marks; thereby it can break with every given context, and engender infinitely new contexts.",
        "The end of linear writing is indeed the end of the book."
    ],
    "Michel Foucault": [
        "Power is everywhere; not because it embraces everything, but because it comes from everywhere.",
        "Where there is power, there is resistance.",
        "The author is not an indefinite source of significations which fill a work; the author does not precede the works.",
        "The panopticon is a machine for dissociating the see/being seen dyad: in the peripheric ring, one is totally seen, without ever seeing.",
        "Knowledge is not for knowing: knowledge is for cutting.",
        "Discourse is not life; its time is not your time.",
        "The soul is the prison of the body.",
        "What strikes me is the fact that in our society, art has become something which is related only to objects and not to individuals, or to life.",
        "The 'Enlightenment', which discovered the liberties, also invented the disciplines."
    ],
    "Jean Baudrillard": [
        "We live in a world where there is more and more information, and less and less meaning.",
        "The simulacrum is never that which conceals the truth—it is the truth which conceals that there is none.",
        "The Gulf War did not take place.",
        "Disneyland is presented as imaginary in order to make us believe that the rest is real.",
        "The end of history is, alas, also the end of the dustbins of history.",
        "The very definition of the real becomes: that of which it is possible to give an equivalent reproduction.",
        "The great person is ahead of their time, the smart make something out of it, and the blockhead sets themselves against it.",
        "In the same way that we need statesmen to spare us the abjection of exercising power, we need scholars to spare us the abjection of learning."
    ],
    "Julia Kristeva": [
        "The speaking subject gives herself away in her speech.",
        "Women's writing is a double-edged weapon.",
        "Abjection is above all ambiguity.",
        "The semiotic is a precondition of the symbolic.",
        "The stranger lives within us: he is the hidden face of our identity.",
        "Language is a skin: when I speak, I wrap myself in my own voice; I touch myself with my own words.",
        "Forgiveness is therefore an economy of time, a way of acting against resentment and vengeance.",
        "The text is a practice that could be compared to political revolution: the one brings about in the subject what the other introduces into society."
    ],
    "Jean-François Lyotard": [
        "Simplifying to the extreme, I define postmodern as incredulity toward metanarratives.",
        "Knowledge is and will be produced in order to be sold.",
        "The sublime is the feeling of something great that the imagination cannot grasp.",
        "The differend is the unstable state and instant of language wherein something which must be able to be put into phrases cannot yet be.",
        "The end of grand narratives is the beginning of a multiplicity of little stories.",
        "Capitalism, in its use of communicational technologies, does not promote the differend: quite the contrary.",
        "To speak is to fight, in the sense of playing, and speech acts fall within the domain of a general agonistics.",
        "A work can become modern only if it is first postmodern. Postmodernism thus understood is not modernism at its end but in the nascent state, and this state is constant."
    ],
    "Roland Barthes": [
        "The death of the author is the birth of the reader.",
        "Language is a skin: I rub my language against the other.",
        "The text is a tissue of quotations drawn from the innumerable centers of culture.",
        "Myth is a system of communication, a message.",
        "The photograph is violent: not because it shows violent things, but because on each occasion it fills the sight by force.",
        "Literature is the question minus the answer.",
        "What I claim is to live to the full the contradiction of my time, which may well make sarcasm the condition of truth.",
        "To try to write love is to confront the muck of language; that region of hysteria where language is both too much and too little."
    ],
    "Gilles Deleuze": [
        "A concept is a brick. It can be used to build a courthouse of reason. Or it can be thrown through the window.",
        "The rhizome is an antigenealogy.",
        "The body without organs is the unproductive, the sterile, the unengendered, the unconsumable.",
        "The plane of immanence is the image of thought, the image thought gives itself of what it means to think.",
        "The virtual is opposed not to the real but to the actual.",
        "Philosophy is not in a state of external reflection on other domains, but in a state of active and internal alliance with them.",
        "We do not lack communication. On the contrary, we have too much of it. We lack creation. We lack resistance to the present.",
        "A society is defined by its lines of flight.",
        "Repressive forces don't stop people from expressing themselves, but rather force them to express themselves."
    ],
    "Judith Butler": [
        "Gender is not something one is, it is something one does.",
        "There is no gender identity behind the expressions of gender.",
        "The heterosexual matrix is a grid of cultural intelligibility through which bodies, genders, and desires are naturalized.",
        "Precarity is the condition of being vulnerable to others.",
        "Performativity is not a singular act, but a repetition and a ritual.",
        "When we say gender is performed, we usually mean that we've taken on a role; we're acting in some way.",
        "We lose ourselves in what we read, only to return to ourselves, transformed and part of a more expansive world.",
        "Let's face it. We're undone by each other. And if we're not, we're missing something."
    ],
    "Donna Haraway": [
        "The cyborg is a creature in a post-gender world.",
        "We are all chimeras, theorized and fabricated hybrids of machine and organism.",
        "Situated knowledges are about communities, not about isolated individuals.",
        "The god trick is this illusion of infinite vision.",
        "Companion species are about significant otherness.",
        "Objectivity is not about disengagement but about mutual and usually unequal structuring.",
        "The boundary between science fiction and social reality is an optical illusion.",
        "Biology is a political discourse, not the body itself."
    ],
    "Richard Rorty": [
        "Truth is made rather than found.",
        "The world does not speak. Only we do.",
        "Solidarity is not discovered by reflection but created.",
        "Language is a set of tools rather than a medium in which we express ourselves.",
        "The liberal ironist is the figure who has abandoned the quest for truth but not the quest for justification.",
        "There is nothing deep down inside us except what we have put there ourselves.",
        "The purpose of education is to complexify the self.",
        "We need to make a distinction between the claim that the world is out there and the claim that truth is out there."
    ],
    "Fredric Jameson": [
        "Always historicize!",
        "Postmodernism is the cultural logic of late capitalism.",
        "The fundamental ideological task of the new concept is to coordinate new forms of practice and social and mental habits with the new forms of economic production.",
        "Interpretation is not so much an act of reading as it is a more complicated gesture of rewriting the literary text in terms of a master code.",
        "The visual is essentially pornographic.",
        "The past as 'referent' finds itself gradually bracketed, and then effaced altogether, leaving us with nothing but texts.",
        "Nostalgia is a way of taking revenge on the present.",
        "History is what hurts, it is what refuses desire and sets inexorable limits to individual as well as collective praxis."
    ],
    "Slavoj Žižek": [
        "I think that the task of philosophy is not to provide answers, but to show how the way we perceive a problem can be itself part of a problem.",
        "In our politically correct times, we all love respect for the Other, the horrible Foreigner - but only insofar as this Other is not really Other.",
        "The ultimate authority is not truth but appearance.",
        "The problem with Hitler was that he was not violent enough.",
        "The true ethical test is not only the readiness to save the victims, but also - even more, perhaps - the ruthless dedication to annihilating those who made them victims.",
        "The function of ideology is not to offer us a point of escape from our reality but to offer us the social reality itself as an escape.",
        "Consciousness is a monstrous thing - it is simultaneously the direct opposite of freedom and the prerequisite for it.",
        "The true aim of political theory is not to allow us to penetrate the false mask of everyday life and perceive its real political content, but quite the opposite – to show that the political appearance is inherent to human reality."
    ],
    "Gayatri Chakravorty Spivak": [
        "Can the subaltern speak?",
        "The subaltern cannot speak.",
        "The word 'representation' is being worked in at least two ways: political representation and re-presentation.",
        "The most serious mistake is to imagine that deconstruction is an exposure of error.",
        "Deconstruction does not say there is no subject, there is no truth, there is no history. It simply questions the privileging of identity so that someone is believed to have the truth.",
        "Strategic essentialism is not a theory, it is a strategy. It is not a description of the way things are, but a suggestion about the way one might act.",
        "If the subaltern can speak then, thank God, the subaltern is not a subaltern any more.",
        "The postcolonial migrant becomes the norm against which even domestic social groups are measured. This is the new exoticism."
    ],
    "Edward Said": [
        "Orientalism is a style of thought based upon an ontological and epistemological distinction made between 'the Orient' and 'the Occident.'",
        "The Orient was almost a European invention.",
        "The intellectual's role is to speak the truth, as plainly, directly and honestly as possible.",
        "No one today is purely one thing.",
        "Every single empire in its official discourse has said that it is not like all the others, that its circumstances are special.",
        "History is written by those who win and those who dominate.",
        "Exile is strangely compelling to think about but terrible to experience.",
        "Humanism is the only resistance we have against the inhumanity of practices and doctrines."
    ],
    "Homi K. Bhabha": [
        "The colonial discourse is an apparatus of power.",
        "Hybridity is the sign of the productivity of colonial power, its shifting forces and fixities.",
        "The time lag introduces a temporal dimension to the space of representation that creates an 'in-between' where meaning is negotiated.",
        "The nation fills the void left in the uprooting of communities and kin.",
        "The liminality of migrant experience is no less a transitional phenomenon than a translational one.",
        "Cultural difference emerges from the borderline moment of translation.",
        "The 'right' to signify from the periphery of authorized power and privilege does not depend on the persistence of tradition; it is resourced by the power of tradition to be reinscribed.",
        "Culture as a strategy of survival is both transnational and translational."
    ],
    "Linda Hutcheon": [
        "Postmodernism's distinctive character lies in this kind of wholesale 'nudging' commitment to doubleness, or duplicity.",
        "Parody is repetition with critical distance.",
        "Irony is the perfect postmodern form, for it paradoxically both incorporates and challenges that which it parodies.",
        "Historiographic metafiction works to situate itself within historical discourse without surrendering its autonomy as fiction.",
        "The postmodern's initial concern is to de-naturalize some of the dominant features of our way of life.",
        "The border between art and the world is still there, but it is a permeable membrane.",
        "Postmodernism is both oedipally oppositional and filially faithful to modernism.",
        "The postmodern paradox: the past whose presence we claim to mark is only known to us today through texts."
    ],
    "Paul Virilio": [
        "Speed is power.",
        "When you invent the ship, you also invent the shipwreck.",
        "The invention of the ship was also the invention of the shipwreck.",
        "The speed of light does not merely transform the world. It becomes the world.",
        "There is no democracy without a technology of distributed information systems.",
        "The invention of the bomb is the invention of a state of generalized global accident.",
        "War is cinema, and cinema is war.",
        "The more speed increases, the faster freedom decreases."
    ],
    "bell hooks": [
        "The function of art is to do more than tell it like it is - it's to imagine what is possible.",
        "No black woman writer in this culture can write 'too much'. Indeed, no woman writer can write 'too much'.",
        "If we want a beloved community, we must stand for justice.",
        "The practice of love offers no place of safety.",
        "For me, forgiveness and compassion are always linked: how do we hold people accountable for wrongdoing and yet at the same time remain in touch with their humanity?",
        "To be oppressed means to be deprived of your ability to choose.",
        "Feminist education — the feminist classroom — is and should be a place where there is a sense of struggle.",
        "Patriarchy has no gender."
    ],
    "Giorgio Agamben": [
        "The state of exception tends increasingly to appear as the dominant paradigm of government in contemporary politics.",
        "Bare life remains included in politics in the form of the exception.",
        "In a biopolitical horizon, he who decides on the value or non-value of life is the sovereign.",
        "The tradition of the oppressed teaches us that the 'state of emergency' in which we live is not the exception but the rule.",
        "The sovereign is the point of indistinction between violence and law, the threshold on which violence passes over into law and law passes over into violence.",
        "The camp is the space that is opened when the state of exception begins to become the rule.",
        "Life and death are not properly scientific concepts but rather political concepts.",
        "What is at stake in the biopolitical paradigm is nothing less than the definition of what part of humanity can be destroyed without committing homicide."
    ]
}