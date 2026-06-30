# hints.py — HashPilot Phase 3
# Application hint system
# Maps application names to hash types they are known to use
# When --hint is passed, matching hash types get a large score boost

HINT_BOOSTS = {
    "ethereum": {
        "Keccak-256":  4.0,
        "SHA-256":     0.5,
        "SHA3-256":    0.8,
        "BLAKE2s-256": 0.5,   
        "BLAKE2b-256": 0.5,   
        "HMAC-SHA256": 0.4,   
},
    "bitcoin": {
        "SHA-256":    3.0,
        "RIPEMD-160": 2.5,
    },
    "git": {
        "SHA-1":      3.0,
        "SHA-256":    2.0,   # git switched to SHA-256 in newer versions
    },
    "linux": {
        "SHA-512 Crypt (Unix)": 3.0,
        "SHA-256 Crypt (Unix)": 2.5,
        "MD5 Crypt (Unix)":     2.0,
        "bcrypt":               1.8,
    },
    "wordpress": {
        "MD5 WordPress (phpass)": 3.0,
        "bcrypt":                 2.0,
        "MD5":                    1.5,
    },
    "django": {
        "PBKDF2-SHA256 (Django)": 3.0,
        "bcrypt":                 2.0,
        "Argon2":                 2.0,
    },
    "windows": {
        "NTLM":           3.0,
        "LM (LAN Manager)": 2.0,
        "MD4":            1.8,
    },
    "mysql": {
        "MySQL 4.1 / MySQL5":    3.0,
        "MySQL 3.x (OLD_PASSWORD)": 2.5,
        "SHA-256":               1.5,
    },
    "jwt": {
        "HMAC-SHA256": 3.0,
        "SHA-256":     1.5,
        "SHA-512":     2.0,
    },
    "wifi": {
        "WPA/WPA2 (PMKID)": 3.0,
        "MD5":               0.3,
    },
}

VALID_HINTS = list(HINT_BOOSTS.keys())


def get_hint_multiplier(hash_name: str, hint: str) -> float:
    """
    Given a hash name and an application hint,
    return the boost multiplier for that specific hash.
    Returns 1.0 if no hint match found.
    """
    if not hint:
        return 1.0

    hint = hint.lower().strip()
    if hint not in HINT_BOOSTS:
        return 1.0

    return HINT_BOOSTS[hint].get(hash_name, 1.0)