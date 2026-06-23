def sanitizar(name):

    # Prefijos
    prefixes = ["la", "el", "las", "los", "de", "precio de", "clima en", "clima de"]

    # Entrada en Min
    name  = name.lower()

    changed = True
    while changed:
        for p in prefixes:
            if name.startswith(p):
                name = name[len(p):].strip()
                changed = True
    
    return name 
    