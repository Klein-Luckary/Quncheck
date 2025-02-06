from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import GroupNormalMessageReceived

@register(
    name="Quncheck", 
    description="群聊识别补丁", 
    version="0.1", 
    author="KL"
)
class UserIDPlugin(BasePlugin):

    def __init__(self, host: APIHost):
        self.host = host
    
    async def initialize(self):
        pass

    @handler(GroupNormalMessageReceived)
    async def handle_group_message(self, ctx: EventContext):
        try:
            msg = ctx.event.text_message
            if not msg:
                return

            # 获取发送者信息
            sender_name = "Unknown"
            if hasattr(ctx.event, 'sender'):
                sender = ctx.event.sender
                # 优先使用群名片
                if hasattr(sender, 'card') and sender.card:
                    sender_name = sender.card
                # 其次使用群昵称
                elif hasattr(sender, 'member_name') and sender.member_name:
                    sender_name = sender.member_name
                # 最后使用QQ昵称
                elif hasattr(sender, 'nickname') and sender.nickname:
                    sender_name = sender.nickname

            # 只处理原始消息，不包含之前的内容
            original_msg = msg.split('"')[-2] if '"' in msg else msg
            modified_msg = f'{sender_name}说："{original_msg}"'
            
            # 修改消息内容
            ctx.event.text_message = modified_msg
            
            # 确保响应中使用相同的消息，但不累积之前的内容
            if hasattr(ctx.event, 'query') and hasattr(ctx.event.query, 'user_message'):
                ctx.event.query.user_message.content = modified_msg

            # Print modified message for debugging
            self.ap.logger.debug(f"Modified message: {modified_msg}")
            self.ap.logger.debug(f"Original sender name: {sender_name}")

        except Exception as e:
            self.ap.logger.error(f"Error in handle_group_message: {str(e)}")
            self.ap.logger.error(f"Event structure: {ctx.event}")  # 打印错误时的事件结构

    def __del__(self):
        pass 
