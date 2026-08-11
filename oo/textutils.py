import re

_WORD_RE=re.compile(r"[a-z0-9']+")
_SENT_RE=re.compile(r"(?<=[.!?])\s+")

def normalize(text: str) -> str:
    """
    lowercase and collapse white space
    """
    return re.sub(r"\s+", " ", text.strip().lower())

def words(text: str) -> list[str]:
    """
    tokenize into lowercase word tokens
    """
    return _WORD_RE.findall(text.lower())

def sentences(text: str) -> list[str]:
    """
    naive sentence split (for v1)
    """
    parts=_SENT_RE.split(text.strip())
    return [p.strip() for p in parts if p.strip()]