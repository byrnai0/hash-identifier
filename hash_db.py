# Hash prototype database with regex, hashcat modes, weights, and context tags

import re
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class HashPrototype:
    name: str
    regex: re.Pattern
    hashcat_mode: Optional[int]
    john_format: Optional[str]
    weight: int          # 1-100: how commonly the hash is seen around the internet
    tags: List[str]      # context tags: web, linux, windows, ctf, database
    description: str     # one-line human-readable note

# ─── HASH DATABASE ────────────────────────────────────────────────────────────
HASH_PROTOTYPES = [

    # ── 32-char hex (128-bit) ─────────────────────────────────────────────────
    HashPrototype(
        name="MD5",
        regex=re.compile(r'^[a-fA-F0-9]{32}$'),
        hashcat_mode=0,
        john_format="raw-md5",
        weight=95,
        tags=["web", "linux", "ctf", "database"],
        description="Most common hash. Used in legacy web apps, checksums, CTFs."
    ),
    HashPrototype(
        name="NTLM",
        regex=re.compile(r'^[a-fA-F0-9]{32}$'),
        hashcat_mode=1000,
        john_format="nt",
        weight=80,
        tags=["windows", "ctf"],
        description="Windows authentication hash. Visually identical to MD5."
    ),
    HashPrototype(
        name="MD4",
        regex=re.compile(r'^[a-fA-F0-9]{32}$'),
        hashcat_mode=900,
        john_format="raw-md4",
        weight=30,
        tags=["windows", "ctf"],
        description="Older predecessor to MD5. Used in legacy Windows auth."
    ),
    HashPrototype(
        name="LM (LAN Manager)",
        regex=re.compile(r'^[a-fA-F0-9]{32}$'),
        hashcat_mode=3000,
        john_format="lm",
        weight=20,
        tags=["windows"],
        description="Very old Windows hash. Uppercase, split into two 7-char blocks."
    ),
    HashPrototype(
        name="RIPEMD-128",
        regex=re.compile(r'^[a-fA-F0-9]{32}$'),
        hashcat_mode=6100,
        john_format=None,
        weight=10,
        tags=["ctf"],
        description="Rare. Produces same length as MD5."
    ),

    # ── 40-char hex (160-bit) ─────────────────────────────────────────────────
    HashPrototype(
        name="SHA-1",
        regex=re.compile(r'^[a-fA-F0-9]{40}$'),
        hashcat_mode=100,
        john_format="raw-sha1",
        weight=85,
        tags=["web", "linux", "ctf", "database"],
        description="Widely used. Git commit IDs, SSL, legacy password storage."
    ),
    HashPrototype(
        name="RIPEMD-160",
        regex=re.compile(r'^[a-fA-F0-9]{40}$'),
        hashcat_mode=6000,
        john_format="ripemd-160",
        weight=20,
        tags=["ctf", "database"],
        description="Used in Bitcoin addresses. Same length as SHA-1."
    ),
    HashPrototype(
        name="MySQL 4.1 / MySQL5",
        regex=re.compile(r'^[a-fA-F0-9]{40}$'),
        hashcat_mode=300,
        john_format="mysql-sha1",
        weight=40,
        tags=["database", "web", "ctf"],
        description="MySQL's PASSWORD() function output. Same length as SHA-1."
    ),

    # ── 56-char hex (224-bit) ─────────────────────────────────────────────────
    HashPrototype(
        name="SHA-224",
        regex=re.compile(r'^[a-fA-F0-9]{56}$'),
        hashcat_mode=1300,
        john_format="raw-sha224",
        weight=40,
        tags=["web", "ctf"],
        description="SHA-2 family. Less common than SHA-256."
    ),
    HashPrototype(
        name="SHA3-224",
        regex=re.compile(r'^[a-fA-F0-9]{56}$'),
        hashcat_mode=17300,
        john_format=None,
        weight=15,
        tags=["ctf"],
        description="SHA-3 family. Keccak-based. Rare in production."
    ),

    # ── 64-char hex (256-bit) ─────────────────────────────────────────────────
    HashPrototype(
        name="SHA-256",
        regex=re.compile(r'^[a-fA-F0-9]{64}$'),
        hashcat_mode=1400,
        john_format="raw-sha256",
        weight=90,
        tags=["web", "linux", "ctf", "database"],
        description="Modern standard. TLS, Bitcoin, JWT signatures."
    ),
    HashPrototype(
        name="SHA3-256",
        regex=re.compile(r'^[a-fA-F0-9]{64}$'),
        hashcat_mode=17400,
        john_format=None,
        weight=20,
        tags=["ctf", "web"],
        description="SHA-3 variant. Same length as SHA-256."
    ),
    HashPrototype(
        name="RIPEMD-256",
        regex=re.compile(r'^[a-fA-F0-9]{64}$'),
        hashcat_mode=None,
        john_format=None,
        weight=10,
        tags=["ctf"],
        description="Rare hash. 64 hex chars just like SHA-256."
    ),
    HashPrototype(
        name="Keccak-256",
        regex=re.compile(r'^[a-fA-F0-9]{64}$'),
        hashcat_mode=17800,
        john_format=None,
        weight=35,
        tags=["ctf", "web"],
        description="Pre-standardization SHA-3. Used in Ethereum."
    ),

    # ── 96-char hex (384-bit) ─────────────────────────────────────────────────
    HashPrototype(
        name="SHA-384",
        regex=re.compile(r'^[a-fA-F0-9]{96}$'),
        hashcat_mode=10800,
        john_format="raw-sha384",
        weight=45,
        tags=["web", "ctf"],
        description="SHA-2 variant. Used in TLS certificates and some APIs."
    ),
    HashPrototype(
        name="SHA3-384",
        regex=re.compile(r'^[a-fA-F0-9]{96}$'),
        hashcat_mode=17500,
        john_format=None,
        weight=10,
        tags=["ctf"],
        description="SHA-3 family. Same length as SHA-384."
    ),

    # ── 128-char hex (512-bit) ────────────────────────────────────────────────
    HashPrototype(
        name="SHA-512",
        regex=re.compile(r'^[a-fA-F0-9]{128}$'),
        hashcat_mode=1700,
        john_format="raw-sha512",
        weight=80,
        tags=["web", "linux", "ctf", "database"],
        description="Modern high-security hash. Used in password storage, JWTs."
    ),
    HashPrototype(
        name="SHA3-512",
        regex=re.compile(r'^[a-fA-F0-9]{128}$'),
        hashcat_mode=17600,
        john_format=None,
        weight=15,
        tags=["ctf"],
        description="SHA-3 family. Same length as SHA-512."
    ),
    HashPrototype(
        name="Whirlpool",
        regex=re.compile(r'^[a-fA-F0-9]{128}$'),
        hashcat_mode=6100,
        john_format="whirlpool",
        weight=10,
        tags=["ctf"],
        description="512-bit hash. Rare in practice."
    ),

    # ── Prefixed / Structured Hashes ─────────────────────────────────────────
    HashPrototype(
        name="bcrypt",
        regex=re.compile(r'^\$2[ayb]\$[0-9]{2}\$[./A-Za-z0-9]{53}$'),
        hashcat_mode=3200,
        john_format="bcrypt",
        weight=85,
        tags=["web", "linux", "database", "ctf"],
        description="Modern password hash. $2a$, $2b$, $2y$ prefix. Deliberately slow."
    ),
    HashPrototype(
        name="SHA-512 Crypt (Unix)",
        regex=re.compile(r'^\$6\$[./0-9A-Za-z]{0,16}\$[./0-9A-Za-z]{86}$'),
        hashcat_mode=1800,
        john_format="sha512crypt",
        weight=75,
        tags=["linux"],
        description="Linux /etc/shadow format. $6$ prefix."
    ),
    HashPrototype(
        name="SHA-256 Crypt (Unix)",
        regex=re.compile(r'^\$5\$[./0-9A-Za-z]{0,16}\$[./0-9A-Za-z]{43}$'),
        hashcat_mode=7400,
        john_format="sha256crypt",
        weight=60,
        tags=["linux"],
        description="Linux /etc/shadow format. $5$ prefix."
    ),
    HashPrototype(
        name="MD5 Crypt (Unix)",
        regex=re.compile(r'^\$1\$[./0-9A-Za-z]{0,8}\$[./0-9A-Za-z]{22}$'),
        hashcat_mode=500,
        john_format="md5crypt",
        weight=55,
        tags=["linux", "ctf"],
        description="Old Linux /etc/shadow format. $1$ prefix."
    ),
    HashPrototype(
        name="Argon2",
        regex=re.compile(r'^\$argon2(i|d|id)\$v=\d+\$m=\d+,t=\d+,p=\d+\$[A-Za-z0-9+/]+\$[A-Za-z0-9+/]+$'),
        hashcat_mode=None,
        john_format=None,
        weight=50,
        tags=["web", "linux", "database"],
        description="Modern memory-hard password hash. Recommended by OWASP."
    ),
    HashPrototype(
        name="PBKDF2-SHA256 (Django)",
        regex=re.compile(r'^pbkdf2_sha256\$\d+\$[A-Za-z0-9]+\$[A-Za-z0-9+/=]{44}$'),
        hashcat_mode=10000,
        john_format=None,
        weight=55,
        tags=["web", "database"],
        description="Django's default password hasher."
    ),
    HashPrototype(
        name="MD5 WordPress",
        regex=re.compile(r'^\$P\$[./0-9A-Za-z]{31}$'),
        hashcat_mode=400,
        john_format="phpass",
        weight=65,
        tags=["web", "database", "ctf"],
        description="WordPress/phpBB phpass format. $P$ prefix."
    ),
    HashPrototype(
        name="NTLM (with colon format)",
        regex=re.compile(r'^[a-fA-F0-9]{32}:[a-fA-F0-9]{32}$'),
        hashcat_mode=1000,
        john_format="nt",
        weight=60,
        tags=["windows", "ctf"],
        description="LM:NTLM format from SAM or NTDS dumps."
    ),
    HashPrototype(
        name="MySQL 3.x (OLD_PASSWORD)",
        regex=re.compile(r'^[a-fA-F0-9]{16}$'),
        hashcat_mode=200,
        john_format="mysql",
        weight=25,
        tags=["database", "ctf"],
        description="Old MySQL password() function. 16 hex chars."
    ),
    HashPrototype(
        name="CRC32",
        regex=re.compile(r'^[a-fA-F0-9]{8}$'),
        hashcat_mode=11500,
        john_format=None,
        weight=30,
        tags=["ctf"],
        description="Cyclic redundancy check. Only 8 hex chars."
    ),
    HashPrototype(
        name="Adler32",
        regex=re.compile(r'^[a-fA-F0-9]{8}$'),
        hashcat_mode=None,
        john_format=None,
        weight=10,
        tags=["ctf"],
        description="Checksum, not a cryptographic hash. 8 hex chars."
    ),
    HashPrototype(
        name="SHA-1 (Base64)",
        regex=re.compile(r'^[A-Za-z0-9+/]{27}=$'),
        hashcat_mode=100,
        john_format="raw-sha1",
        weight=40,
        tags=["web", "ctf"],
        description="SHA-1 encoded as Base64. Seen in some Java applications."
    ),
    HashPrototype(
        name="MD5 (Base64)",
        regex=re.compile(r'^[A-Za-z0-9+/]{22}==$'),
        hashcat_mode=0,
        john_format="raw-md5",
        weight=35,
        tags=["web", "ctf"],
        description="MD5 encoded as Base64. 24 chars ending in ==."
    ),
    HashPrototype(
        name="BLAKE2b-512",
        regex=re.compile(r'^[a-fA-F0-9]{128}$'),
        hashcat_mode=600,
        john_format=None,
        weight=20,
        tags=["ctf", "linux"],
        description="BLAKE2b produces 128 hex chars. Modern, fast hash."
    ),
    HashPrototype(
        name="BLAKE2s-256",
        regex=re.compile(r'^[a-fA-F0-9]{64}$'),
        hashcat_mode=None,
        john_format=None,
        weight=25,
        tags=["ctf", "linux"],
        description="BLAKE2s variant optimised for 32-bit systems. 64 hex chars."
    ),
    HashPrototype(
        name="Blake2b-256",
        regex=re.compile(r'^[a-fA-F0-9]{64}$'),
        hashcat_mode=None,
        john_format=None,
        weight=20,
        tags=["ctf", "linux"],
        description="BLAKE2b truncated to 256 bits. 64 hex chars."
    ),
    HashPrototype(
        name="HMAC-SHA256",
        regex=re.compile(r'^[a-fA-F0-9]{64}$'),
        hashcat_mode=1450,
        john_format=None,
        weight=30,
        tags=["web", "ctf"],
        description="Keyed hash for message authentication. Same length as SHA-256."
    ),
    HashPrototype(
        name="WPA/WPA2 (PMKID)",
        regex=re.compile(r'^[a-fA-F0-9]{32}\*[a-fA-F0-9]{12}\*[a-fA-F0-9]{12}\*[a-zA-Z0-9]+$'),
        hashcat_mode=22000,
        john_format=None,
        weight=50,
        tags=["wifi", "ctf"],
        description="Wi-Fi PMKID format captured via 4-way handshake."
    ),
]