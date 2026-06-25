from typing import Dict, List

user_stats: Dict[int, Dict] = {}

def get_user_stats(user_id: int) -> Dict:
    if user_id not in user_stats:
        user_stats[user_id] = {
            "learned_words": [],
            "total_learned": 0
        }
    return user_stats[user_id]

def add_learned_word(user_id: int, word: str, trans: str) -> None:
    stats = get_user_stats(user_id)
    stats["learned_words"].append({"word": word, "trans": trans})
    stats["total_learned"] += 1

def clear_user_stats(user_id: int) -> None:
    if user_id in user_stats:
        user_stats[user_id] = {
            "learned_words": [],
            "total_learned": 0
        }

def get_learned_words(user_id: int) -> List[Dict]:
    stats = get_user_stats(user_id)
    return stats["learned_words"]

def get_total_learned(user_id: int) -> int:
    stats = get_user_stats(user_id)
    return stats["total_learned"]