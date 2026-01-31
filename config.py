import pandas as pd
import os

TAXON_CONFIG = {
    "HUMPBACK_WHALE": 137092,
    "BLUE_WHALE": 137090,
    "ORCA": 137102,
    "DOLPHIN": 137094,
    "NARWHAL": 383467
}

SPECIES_INFO = {
    "Humpback Whale": (
        "The humpback whale (Megaptera novaeangliae) is a large baleen whale known for its spectacular breaches "
        "and long, complex songs produced mainly by males during the breeding season. "
        "These songs typically last between 5 and 20 minutes and are repeated in sequences that can carry over tens "
        "of kilometers through the water. "
        "Humpback whales undertake extensive annual migrations between cold, nutrient‑rich feeding grounds in "
        "temperate or polar waters and warm tropical or subtropical breeding areas, often traveling thousands of "
        "kilometers each year. "
        "They feed primarily on small schooling prey such as krill and small fish, using techniques like bubble‑net "
        "feeding in which groups cooperate to trap prey in rising curtains of bubbles. "
        "Despite their massive size, humpbacks are generally considered gentle giants and play an important role in "
        "marine ecosystems by redistributing nutrients through their movements and feeding behavior. "
    ),

    "Blue Whale": (
        "The blue whale (Balaenoptera musculus) is the largest animal known to have ever lived, with adults commonly "
        "reaching 25–30 meters in length and weighing well over 100 tons. "
        "Blue whales are baleen whales and feed almost exclusively on tiny crustaceans called krill, which they filter "
        "from seawater using hundreds of baleen plates suspended from the upper jaw. "
        "During feeding seasons in cold polar or subpolar waters, a single individual can consume several tons of krill "
        "per day through powerful lunge‑feeding dives that may exceed 200 meters in depth. "
        "Most populations migrate between high‑latitude summer feeding grounds and lower‑latitude winter breeding areas, "
        "though some individuals show more flexible or partial migration patterns. "
        "Blue whales communicate using extremely low‑frequency vocalizations that can travel over vast distances in the "
        "ocean, and all recognized subspecies are currently considered endangered due to historical commercial whaling "
        "and ongoing human‑related threats. "
    ),

    "Orca": (
        "The orca or killer whale (Orcinus orca) is the largest member of the dolphin family and an apex predator found "
        "in all the world’s oceans, from polar seas to temperate and some tropical regions. "
        "Orcas live in highly social, matrilineal family groups called pods, often composed of multiple generations led "
        "by an older female, and these pods can form larger social structures such as clans and communities. "
        "Different populations specialize in distinct types of prey, ranging from fish and squid to seals, sharks, and even "
        "large whales, and they use coordinated hunting strategies that require precise communication and cooperation. "
        "Each pod has a characteristic set of vocalizations or dialect, consisting of clicks, whistles, and pulsed calls, " 
        "which function in both communication and echolocation and are culturally transmitted across generations. "
        "Because of their intelligence, complex social behavior, and top‑predator role, orcas are considered key indicators "
        "of the health and balance of marine ecosystems. "
    ),

    "Dolphin": (
        "Dolphins are highly intelligent toothed whales (odontocetes) that inhabit coastal and offshore waters worldwide, "
        "with species adapted to a broad variety of marine and, in some cases, freshwater environments. "
        "They live in social groups called pods, which can range from a few individuals to large, dynamic communities, and "
        "they engage in complex social behaviors such as cooperative hunting, play, and providing care to injured or sick "
        "members of their group."
        "Dolphins communicate using a rich repertoire of clicks, whistles, and body movements, and many species show evidence "
        "of individual “signature whistles” that function somewhat like names."
        "They use echolocation by emitting focused click sounds and interpreting returning echoes to detect prey, navigate in "
        "murky waters, and investigate objects with remarkable precision. "
        "Numerous studies highlight their advanced problem‑solving skills, cultural traditions, and capacity for innovation, "
        "which make dolphins a model group for research on animal cognition and social learning. "
    )
}

# TODO: Update config creation

os.makedirs("data/csv", exist_ok=True)

df = pd.read_csv('data/txt/occurrence.txt', sep='\t')

df.to_csv('data/csv/occurrence.csv', index=False, encoding='utf-8')