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
    #TODO: add scene_a_faire, ai_regurgitation, parady, coincidental, merger (showcase table, same shape)
]