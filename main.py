from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *

@register(
    name="Quncheck", 
    description="群聊消息精准@回复", 
    version="0.1", 
    author="KL"
)
class GroupReplyPlugin(BasePlugin):

    def __init__(self, host: APIHost):
        # 初始化字典保存最新发送者信息 {群号: 用户ID}
        self.last_senders = {}
        self.host = host

    @handler(GroupNormalMessageReceived)
    async def handle_group_message(self, ctx: EventContext):
        """处理接收到的群消息"""
        try:
            # 获取群号和发送者ID
            group_id = ctx.event.group_id
            sender_id = ctx.event.sender_id
            
            # 记录最后发送者
            self.last_senders[group_id] = sender_id
            
            # 示例：处理特定指令
            if ctx.event.text_message == "hello":
                # 添加基础回复（后续会自动添加@）
                ctx.add_return("reply", ["hello, everyone!"])
                ctx.prevent_default()

        except Exception as e:
            self.host.logger.error(f"处理群消息出错: {str(e)}")

    @handler(GroupMessageBeforeSend)
    async def handle_group_reply(self, ctx: EventContext):
        """处理即将发送的群回复"""
        try:
            group_id = ctx.event.group_id
            
            # 获取最后发送者ID
            sender_id = self.last_senders.get(group_id)
            if sender_id:
                # 构建@消息的CQ码
                at_msg = f"[CQ:at,qq={sender_id}]"
                
                # 在原始内容前添加@信息
                ctx.event.message = f"{at_msg} {ctx.event.message}"
                
                # 删除已处理的记录
                del self.last_senders[group_id]

        except Exception as e:
            self.host.logger.error(f"处理群回复出错: {str(e)}")

    def __del__(self):
        pass
