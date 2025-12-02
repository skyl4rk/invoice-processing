## Note: this script is not functional. It is for example only.


articles = [
    "./data/structured_outputs_articles/cnns.md",
    "./data/structured_outputs_articles/llms.md",
    "./data/structured_outputs_articles/moe.md",
]


def get_article_content(path):
    with open(path, "r") as f:
        content = f.read()
    return content


content = [get_article_content(path) for path in articles]

print(content)

summarization_prompt = """
    You will be provided with content from an article about an invention.
    Your goal will be to summarize the article following the schema provided.
    Here is a description of the parameters:
    - invented_year: year in which the invention discussed in the article was invented
    - summary: one sentence summary of what the invention is
    - inventors: array of strings listing the inventor full names if present, otherwise just surname
    - concepts: array of key concepts related to the invention, each concept containing a title and a description
    - description: short description of the invention
"""


class ArticleSummary(BaseModel):
    invented_year: int
    summary: str
    inventors: list[str]
    description: str

    class Concept(BaseModel):
        title: str
        description: str

    concepts: list[Concept]


def get_article_summary(text: str):
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": dedent(summarization_prompt)},
            {"role": "user", "content": text},
        ],
        response_format=ArticleSummary,
    )

    return completion.choices[0].message.parsed


summaries = []

for i in range(len(content)):
    print(f"Analyzing article #{i + 1}...")
    summaries.append(get_article_summary(content[i]))
    print("Done.")


def print_summary(summary):
    print(f"Invented year: {summary.invented_year}\n")
    print(f"Summary: {summary.summary}\n")
    print("Inventors:")
    for i in summary.inventors:
        print(f"- {i}")
    print("\nConcepts:")
    for c in summary.concepts:
        print(f"- {c.title}: {c.description}")
    print(f"\nDescription: {summary.description}")


for i in range(len(summaries)):
    print(f"ARTICLE {i}\n")
    print_summary(summaries[i])
    print("\n\n")
