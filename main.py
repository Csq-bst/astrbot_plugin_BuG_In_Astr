from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import sys
from pathlib import Path
from typing import Dict
sys.path.insert(0, str(Path(__file__).resolve().parent))
from db_handler import DatabaseManager
from api_client import (
    fetch_leaderboard,
    fetch_gamestats,
    fetch_player_info,
    fetch_guild_info,
    fetch_match_details,
    fetch_player_stats_2025,
    fetch_user_game_log,
)
from astrbot.core.utils.astrbot_path import get_astrbot_data_path

@register("布吉岛查询", "醋酸铅糖不是糖", 'BuG-In-Astr允许你通过Astrbot访问你在Minecraft服务器"布吉岛"中的数据', "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context, config: Dict):
        super().__init__(context)
        self.config = config

        data_path = Path(get_astrbot_data_path())
        db_path = data_path / "plugin_data" / self.name / "player_data.db"
        self.db_manager = DatabaseManager(db_path)

    async def initialize(self):
        """初始化数据库"""
        await self.db_manager.init_db()

    # ========== 绑定/解绑 ==========

    @filter.command("register", aliases={"绑定"})
    async def register_player(self, event: AstrMessageEvent, game_id: str):
        """绑定 QQ 账号到游戏 ID"""
        qq_id = event.get_sender_id()
        result = await self.db_manager.bind_player(qq_id, game_id)
        if result:
            yield event.plain_result("绑定成功！")
        else:
            yield event.plain_result("绑定失败！")

    @filter.command("unbind", aliases={"解绑"})
    async def unbind_player(self, event: AstrMessageEvent):
        """解除绑定"""
        qq_id = event.get_sender_id()
        result = await self.db_manager.unbind_player(qq_id)
        if result:
            yield event.plain_result("解绑成功！")
        else:
            yield event.plain_result("解绑失败！")

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("update_auth_key")
    async def update_auth_key(self, event: AstrMessageEvent, new_key: str):
        """管理员更新 API 鉴权 Key"""
        self.config["auth_key"] = new_key
        self.config.save_config()
        yield event.plain_result("API 鉴权 Key 已更新！")

    # ========== 查询指令组 ==========

    @filter.command_group("bjd")
    def bjd(self):
        """布吉岛数据查询指令组"""
        pass

    @bjd.command("player")
    async def bjd_player(self, event: AstrMessageEvent):
        """查询玩家基本信息"""
        qq_id = event.get_sender_id()
        game_id = await self.db_manager.get_game_id(qq_id)
        if not game_id:
            yield event.plain_result("请先使用 /register 绑定游戏ID")
            return

        auth_key = self.config["auth_key"]
        data = await fetch_player_info(game_id, auth_key)
        if data:
            yield event.plain_result(f"📊 {game_id} 的玩家信息：\n{data}")
        else:
            yield event.plain_result("查询失败，请检查游戏ID或API密钥。")

    @bjd.command("guild")
    async def bjd_guild(self, event: AstrMessageEvent):
        """查询公会信息"""
        qq_id = event.get_sender_id()
        game_id = await self.db_manager.get_game_id(qq_id)
        if not game_id:
            yield event.plain_result("请先使用 /register 绑定游戏ID")
            return

        auth_key = self.config["auth_key"]
        data = await fetch_guild_info(game_id, auth_key)
        if data:
            yield event.plain_result(f"🏰 {game_id} 的公会信息：\n{data}")
        else:
            yield event.plain_result("查询失败，请检查游戏ID或API密钥。")

    @bjd.command("leaderboard")
    async def bjd_leaderboard(self, event: AstrMessageEvent):
        """查询排行榜"""
        qq_id = event.get_sender_id()
        game_id = await self.db_manager.get_game_id(qq_id)
        if not game_id:
            yield event.plain_result("请先使用 /register 绑定游戏ID")
            return

        auth_key = self.config["auth_key"]
        data = await fetch_leaderboard(game_id, auth_key)
        if data:
            yield event.plain_result(f"🏆 {game_id} 的排行榜数据：\n{data}")
        else:
            yield event.plain_result("查询失败，请检查游戏ID或API密钥。")

    @bjd.command("stats")
    async def bjd_stats(self, event: AstrMessageEvent, gametype: str):
        """查询游戏统计数据，需指定游戏类型（如 bedwars）"""
        qq_id = event.get_sender_id()
        game_id = await self.db_manager.get_game_id(qq_id)
        if not game_id:
            yield event.plain_result("请先使用 /register 绑定游戏ID")
            return

        auth_key = self.config["auth_key"]
        data = await fetch_gamestats("", game_id, gametype, auth_key)
        if data:
            yield event.plain_result(f"🎮 {game_id} 的 {gametype} 数据：\n{data}")
        else:
            yield event.plain_result("查询失败，请检查游戏ID或API密钥。")

    @bjd.command("log")
    async def bjd_log(self, event: AstrMessageEvent, page: str = "1"):
        """查询对局记录，可选页码参数"""
        qq_id = event.get_sender_id()
        game_id = await self.db_manager.get_game_id(qq_id)
        if not game_id:
            yield event.plain_result("请先使用 /register 绑定游戏ID")
            return

        auth_key = self.config["auth_key"]
        data = await fetch_user_game_log(game_id, auth_key, page)
        if data:
            yield event.plain_result(f"📜 {game_id} 的对局记录（第{page}页）：\n{data}")
        else:
            yield event.plain_result("查询失败，请检查游戏ID或API密钥。")

    @bjd.command("match")
    async def bjd_match(self, event: AstrMessageEvent, date: str):
        """查询比赛详情，需指定日期（如 2025-01-01）"""
        qq_id = event.get_sender_id()
        game_id = await self.db_manager.get_game_id(qq_id)
        if not game_id:
            yield event.plain_result("请先使用 /register 绑定游戏ID")
            return

        auth_key = self.config["auth_key"]
        data = await fetch_match_details(game_id, auth_key, date)
        if data:
            yield event.plain_result(f"⚔️ {game_id} 在 {date} 的比赛详情：\n{data}")
        else:
            yield event.plain_result("查询失败，请检查游戏ID、日期或API密钥。")

    @bjd.command("2025")
    async def bjd_2025(self, event: AstrMessageEvent):
        """查询 2025 年度总结"""
        qq_id = event.get_sender_id()
        game_id = await self.db_manager.get_game_id(qq_id)
        if not game_id:
            yield event.plain_result("请先使用 /register 绑定游戏ID")
            return

        auth_key = self.config["auth_key"]
        data = await fetch_player_stats_2025(game_id, auth_key)
        if data:
            yield event.plain_result(f"🎉 {game_id} 的 2025 年度总结：\n{data}")
        else:
            yield event.plain_result("查询失败，请检查游戏ID或API密钥。")

    @filter.permission_type(filter.PermissionType.ADMIN)
    @bjd.command("list")
    async def bjd_list(self, event: AstrMessageEvent):
        """管理员查看所有绑定记录"""
        rows = await self.db_manager.get_all_bindings()
        if not rows:
            yield event.plain_result("暂无绑定记录。")
            return

        lines = [f"📋 当前共有 {len(rows)} 条绑定记录："]
        for qq_id, game_id, created_at in rows:
            lines.append(f"QQ: {qq_id} → {game_id} ({created_at})")
        yield event.plain_result("\n".join(lines))

    # ========== LLM 工具 ==========

    @filter.llm_tool(name="bjd_player")
    async def tool_player(self, event: AstrMessageEvent) -> MessageEventResult:
        '''查询已绑定的布吉岛玩家的基础信息，如等阶、公会、VIP等级等。

        Args:
            (无参数)
        '''
        result = await self._run_query(event, fetch_player_info)
        yield event.plain_result(result)

    @filter.llm_tool(name="bjd_guild")
    async def tool_guild(self, event: AstrMessageEvent) -> MessageEventResult:
        '''查询已绑定的布吉岛玩家的公会信息。

        Args:
            (无参数)
        '''
        result = await self._run_query(event, fetch_guild_info)
        yield event.plain_result(result)

    @filter.llm_tool(name="bjd_leaderboard")
    async def tool_leaderboard(self, event: AstrMessageEvent) -> MessageEventResult:
        '''查询已绑定的布吉岛玩家的排行榜数据。

        Args:
            (无参数)
        '''
        result = await self._run_query(event, fetch_leaderboard)
        yield event.plain_result(result)

    @filter.llm_tool(name="bjd_stats")
    async def tool_stats(self, event: AstrMessageEvent, gametype: str) -> MessageEventResult:
        '''查询已绑定的布吉岛玩家的游戏统计数据。

        Args:
            gametype(string): 游戏类型，如 bedwars, skywars, vdefense, arenapvp, anqu, kitbattle, anni, achievement
        '''
        result = await self._run_query(event, lambda g, k: fetch_gamestats("", g, gametype, k))
        yield event.plain_result(result)

    @filter.llm_tool(name="bjd_log")
    async def tool_log(self, event: AstrMessageEvent, page: str) -> MessageEventResult:
        '''查询已绑定的布吉岛玩家的对局记录。

        Args:
            page(string): 页码，默认为1
        '''
        result = await self._run_query(event, lambda g, k: fetch_user_game_log(g, k, page))
        yield event.plain_result(result)

    @filter.llm_tool(name="bjd_match")
    async def tool_match(self, event: AstrMessageEvent, date: str) -> MessageEventResult:
        '''查询已绑定的布吉岛玩家的某场比赛详情。

        Args:
            date(string): 日期，格式 yyyy-MM-dd HH:mm:ss
        '''
        result = await self._run_query(event, lambda g, k: fetch_match_details(g, k, date))
        yield event.plain_result(result)

    @filter.llm_tool(name="bjd_2025")
    async def tool_2025(self, event: AstrMessageEvent) -> MessageEventResult:
        '''查询已绑定的布吉岛玩家的2025年度总结数据。

        Args:
            (无参数)
        '''
        result = await self._run_query(event, fetch_player_stats_2025)
        yield event.plain_result(result)

    # ========== 内部辅助 ==========

    async def _run_query(self, event: AstrMessageEvent, query_func) -> str:
        """执行查询的通用方法"""
        qq_id = event.get_sender_id()
        game_id = await self.db_manager.get_game_id(qq_id)
        if not game_id:
            return "请先使用 /register 绑定游戏ID"
        auth_key = self.config["auth_key"]
        data = await query_func(game_id, auth_key)
        if data:
            return str(data)
        return "查询失败，请检查游戏ID或API密钥。"

    @filter.command("bjdhelp")
    async def help(self, event: AstrMessageEvent):
        """显示帮助信息"""
        msg = (
            "📖 布吉岛查询插件使用说明\n\n"
            "/register <游戏ID> 或 /绑定 <游戏ID>  - 绑定QQ到游戏ID\n"
            "/unbind 或 /解绑  - 解除绑定\n"
            "/update_auth_key <key>  - 管理员更新API密钥\n\n"
            "/bjd player  - 查询玩家信息\n"
            "/bjd guild  - 查询公会信息\n"
            "/bjd leaderboard  - 查询排行榜\n"
            "/bjd stats <游戏类型>  - 查询游戏数据（bedwars, skywars 等）\n"
            "/bjd log [页码]  - 查询对局记录\n"
            "/bjd match <日期>  - 查询比赛详情（yyyy-MM-dd HH:mm:ss）\n"
            "/bjd 2025  - 查询2025年度总结\n"
            "/bjd list  - 显示所有绑定记录(按时间倒序)\n"
            "/bjdhelp  - 显示本帮助"
        )
        yield event.plain_result(msg)

    async def terminate(self):
        """插件被卸载/停用时调用"""
        pass