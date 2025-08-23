from swarms_tools.search.exa_search import exa_search

print(
    exa_search(
        "What are the best performing semiconductor stocks?",
        characters=100,
        sources=2,
    )
)
