from urllib.parse import urlsplit

def classify_links(urls: list, root_domain: str) -> dict:
    """Classifie les URLs dans des catégories prédéfinies basées sur leur chemin.
    
    Args:
        urls: Liste des URLs à classifier
        root_domain: Domaine racine pour la catégorie Home
        
    Returns:
        Dictionnaire des URLs classées par catégorie
    """
    categories = {
        "Home": [],
        "Pages": [],
        "Policies": [],
        "Blogs": [],
        "Collections": [],
        "Products": [],
        "Others": []
    }
    
    for url in urls:
        parsed = urlsplit(url)
        
        # Normalisation du path
        path = parsed.path.lower()
        if path.endswith("/"):
            path = path[:-1]
        
        # Classification: Home (root_domain exact)
        if parsed.netloc == root_domain and path == "":
            categories["Home"].append(url)
            continue
            
        # Vérification des sous-domaines
        if not parsed.netloc.endswith(root_domain):
            categories["Others"].append(url)
            continue
            
        # Classification: Autres catégories
        matched = False
        # Split path into segments
        segments = path.split("/")
        
        # Classification based on path segments
        if len(segments) > 0:
            first_segment = segments[0]
            
            if first_segment in ["pages", "page"]:
                categories["Pages"].append(url)
                matched = True
            elif first_segment in ["policies", "policy"]:
                categories["Policies"].append(url)
                matched = True
            elif first_segment in ["blogs", "blog"]:
                categories["Blogs"].append(url)
                matched = True
            elif first_segment in ["collections", "collection"]:
                categories["Collections"].append(url)
                matched = True
            elif first_segment in ["products", "product"]:
                categories["Products"].append(url)
                matched = True
            elif first_segment == "" and len(segments) > 1:
                # Handle cases like "/pages/about"
                if segments[1] in ["pages", "page"]:
                    categories["Pages"].append(url)
                    matched = True
                elif segments[1] in ["policies", "policy"]:
                    categories["Policies"].append(url)
                    matched = True
                elif segments[1] in ["blogs", "blog"]:
                    categories["Blogs"].append(url)
                    matched = True
                elif segments[1] in ["collections", "collection"]:
                    categories["Collections"].append(url)
                    matched = True
                elif segments[1] in ["products", "product"]:
                    categories["Products"].append(url)
                    matched = True
        
        # Si aucune correspondance → Others
        if not matched:
            categories["Others"].append(url)
    
    return categories
