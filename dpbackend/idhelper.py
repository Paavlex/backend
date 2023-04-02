
# Funkce pro vytoření ID hráče, bere délku id z databáze (1,2,3....) 
# Podle délky tohoto id odstraní potřebný počet nul z paddingu a vytvoří nový string, který představuje ID ve správném formátu
def getplayerid(id):
    tag = "P"
    padding="000000000000000000000"
    given_id = str(id)
    id_len = len(given_id)
    changed_padding = padding[id_len:]
    user_id = tag+changed_padding+given_id
    print(len(user_id))
    return user_id

# Totožné jako u ID hráče, jen pro ID karty/keše
def getcacheid(id):
    tag = "GC"
    padding="0000000000"
    given_id = str(id)
    id_len = len(given_id)
    changed_padding = padding[id_len:]
    cache_id = tag+changed_padding+given_id
    print(len(cache_id))
    return cache_id

# Totožné jako u ID hráče, jen pro ID předmětu
def getitemid(id):
    tag = "TG"
    padding="00000000000000000000"
    given_id = str(id)
    id_len = len(given_id)
    changed_padding = padding[id_len:]
    item_id = tag+changed_padding+given_id
    print(len(item_id))
    return item_id



