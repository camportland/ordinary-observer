CASES=[
    {
        "id": "verbatim_copy",
        "title": "Near-verbatim_copy",
        "expected": "HIGH",
        "work_b": "The old lighthouse had guarded the rocky harbor for over a "
                  "century. Every night its beam swept across the water, warning "
                  "ships away from the jagged reef",
        "work_a": "The old lighthouse had guarded the rocky harbor for over a "
                  "century. Each night its beam swept across the warer, warning "
                  "ships away from the jagged reef.",
    },
    {
        "id": "same_facts",
        "title": "Two articles, same event (the divergence case)",
        "expected": "LOW",
        "work_b": "A 5.2-magnitude earthquare struck near Ridgecrest on Tuesday "
                  "morning. No injuries were reported, and officials said damage "
                  "was limited to cracked roads.",
        "work_a": "Tuesday's 5.2 quake near Ridgecrest caused no injuries. "
                  "Authories reported only minor damage, mainly to roadways."
    },
    {
        "id": "ai_paraphrase",
        "title": "AI 'rewrite in your own words' of a source",
        "expected": "MODERATE",
        "work_b": "For more than a hundred years, the ancient lighthouse had "
                  "protected the stony harbor. Each evening its beam moved across "
                  "the sea, keeping vessels clear of the sharp reef.",
        "work_a": "The century-old lighthouse long shielded the rocky harbor; "
                  "nightly its light traced the water, steering boats away from "
                  "the dangerous reef."
    },
    {
        "id": "ai_regurgitation",
        "title": "LLM reproduces memorized training text",
        "expected": "HIGH",
        "work_b": "Marguerite pressed her palm aagainst the frosted glass and "
                  "watched the gaslamps blur into halos of amber. Below, a hansom "
                  "cab rattled over the cobbles, and she thought, not for the first "
                  "time, that the city kept its secrets the way she kept hers.",
        "work_a": "Marguerite pressed her palm to the frosted glass and watched "
                  "the gaslamps blur into halos of campber. Below, a hansom cab "
                  "rattled over the cobbles, and she thought, not for the first "
                  "time, that the city kept its secrets the way she kept hers."
    },
    {
        "id": "scene_a_faire",
        "title": "Shared genre conventions (scene a faire)",
        "expected": "LOW",
        "work_b": "Rain hammered the neon-slick street when she walked into my "
                  "office - trouble in a red dress, the kind of dame who meant a "
                  "long night and a longer bar tab. I poured two fingers of "
                  "bourbon and waited for the lie.",
        "work_a": "The neon bled across the wet pavement as the dame stepped "
                  "through my door, all trouble and red silk, promising a "
                  "sleepless night. I splashed whiskey into a glass and braced for "
                  "whatever story she'd invented."
    },
    {
        "id": "parody",
        "title": "Parody/transformative use",
        "expected": "MODERATE",
        "work_b": "Rise each morning with a grateful heart, for every dawn is a "
                  "gift unearned, and the road ahead, though steep, rewards the "
                  "faithful climber with vistas none can steal.",
        "work_a": "Rise each morning with a caffeinated heart, for every day is a "
                  "bill unpaid, and the road ahead, though steep with traffic, "
                  "rewards the faithful commuter with parking none can find."
    }
]