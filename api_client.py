import aiohttp
from typing import Optional, Dict, Any


async def fetch_leaderboard(username: str, auth_key: str) -> Optional[Dict[str, Any]]:
    """查询布吉岛排行榜数据"""
    url = "https://api.mcbjd.net/v2/leaderboard"
    headers = _make_headers(auth_key)
    payload = {"username": username}
    return await _post(url, headers, payload)


async def fetch_gamestats(uuid: str, username: str, gametype: str, auth_key: str) -> Optional[Dict[str, Any]]:
    """获取布吉岛游戏数据"""
    url = "https://api.mcbjd.net/v2/gamestats"
    headers = _make_headers(auth_key)
    payload = {"uuid": uuid, "username": username, "gametype": gametype}
    return await _post(url, headers, payload)


async def fetch_player_info(username: str, auth_key: str) -> Optional[Dict[str, Any]]:
    """查询玩家基本信息"""
    url = "https://api.mcbjd.net/v2/player"
    headers = _make_headers(auth_key)
    payload = {"username": username}
    return await _post(url, headers, payload)


async def fetch_guild_info(username: str, auth_key: str) -> Optional[Dict[str, Any]]:
    """查询公会信息"""
    url = "https://api.mcbjd.net/v2/guild"
    headers = _make_headers(auth_key)
    payload = {"username": username}
    return await _post(url, headers, payload)


async def fetch_match_details(username: str, auth_key: str, date: str) -> Optional[Dict[str, Any]]:
    """查询比赛详情"""
    url = "https://api.mcbjd.net/v2/gamelog/match"
    headers = _make_headers(auth_key)
    payload = {"username": username, "date": date}
    return await _post(url, headers, payload)


async def fetch_player_stats_2025(username: str, auth_key: str) -> Optional[Dict[str, Any]]:
    """查询 2025 年玩家统计数据"""
    url = "https://api.mcbjd.net/v2/player/2025total"
    headers = _make_headers(auth_key)
    payload = {"username": username}
    return await _post(url, headers, payload)


async def fetch_user_game_log(username: str, auth_key: str, page: str) -> Optional[Dict[str, Any]]:
    """查询玩家游戏记录"""
    url = "https://api.mcbjd.net/v2/gamelog/user"
    headers = _make_headers(auth_key)
    payload = {"username": username, "page": page}
    return await _post(url, headers, payload)


# ---------- 内部辅助函数 ----------

def _make_headers(auth_key: str) -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {auth_key}",
    }


async def _post(url: str, headers: Dict[str, str], payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """统一的 POST 请求入口"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status != 200:
                    return None
                return await resp.json()
    except Exception:
        return None