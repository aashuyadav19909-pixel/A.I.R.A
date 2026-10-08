from memory import remember, recall, forget, get_all_memory


print(remember("favorite_game", "Palworld"))

print(
    "Favorite game:",
    recall("favorite_game")
)

print(
    "All memory:",
    get_all_memory()
)

print(
    forget("favorite_game")
)

print(
    "After forgetting:",
    get_all_memory()
)