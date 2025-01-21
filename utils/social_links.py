import re
import logging

logger = logging.getLogger(__name__)

def extract_social_links(unique_links):
    """
    Extrait les liens des réseaux sociaux à partir d'une liste de liens.
    Supporte différents formats d'URLs pour chaque réseau social.
    """
    social_links = {
        "facebook": None,
        "instagram": None,
        "twitter": None,
        "tiktok": None,
        "linkedin": None,
        "youtube": None,
        "pinterest": None,
        "github": None,
        "snapchat": None
    }

    # Patterns plus flexibles pour les liens sociaux
    patterns = {
        "facebook": re.compile(r"https?://(www\.)?(facebook|fb)\.com/([^/\s]+)/?"),
        "instagram": re.compile(r"https?://(www\.)?instagram\.[^/]+/([^/\s]+)/?"),
        "twitter": re.compile(r"https?://(www\.)?(twitter|x)\.[^/]+/([^/\s]+)/?"),
        "tiktok": re.compile(r"https?://(www\.)?tiktok\.com/(@[^/\s]+|[^/\s]+)/?"),
        "linkedin": re.compile(r"https?://(www\.)?linkedin\.[^/]+/(company/[^/\s]+|in/[^/\s]+)/?"),
        "youtube": re.compile(r"https?://(www\.)?(youtube\.com|youtu\.be)/(channel/|user/|c/|@)?([^/\s]+)/?"),
        "pinterest": re.compile(r"https?://(www\.)?pinterest\.[^/]+/([^/\s]+)/?"),
        "github": re.compile(r"https?://(www\.)?github\.com/([^/\s]+)/?"),
        "snapchat": re.compile(r"https?://(www\.)?snapchat\.com/(add/|@)?([^/\s]+)/?")
    }

    if not unique_links:
        logger.warning("No links provided for social media extraction")
        return social_links

    logger.info(f"Analyzing {len(unique_links)} links for social media presence")

    for link in unique_links:
        if not link:
            continue

        link = link.strip().lower()
        for platform, pattern in patterns.items():
            if social_links[platform]:
                continue  # Skip if we already found a link for this platform

            match = pattern.search(link)
            if match:
                social_links[platform] = link
                logger.info(f"Found {platform} profile: {link}")

    # Log summary of found social links
    found_platforms = [platform for platform, link in social_links.items() if link]
    if found_platforms:
        logger.info(f"Found social media profiles on: {', '.join(found_platforms)}")
    else:
        logger.info("No social media profiles found")

    return social_links
