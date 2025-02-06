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

    @handler(GroupNormalMessageReceived)  # 确保使用正确的事件名称
    async def handle_group_message(self, ctx: EventContext):
        try:
            msg = ctx.event.text_message
            if not msg:
                return

            # 获取发送者名称
            sender_name = "Unknown"
            if hasattr(ctx.event, 'sender') and hasattr(ctx.event.sender, 'member_name'):
                sender_name = ctx.event.sender.member_name

            # 构建修改后的消息
            modified_msg = f"群友 {sender_name} 说：{msg}"
            
            # 打印修改后的消息到控制台
            self.host.logger.debug(f"Modified message: {modified_msg}")
            
            # 修改消息内容
            if hasattr(ctx.event, 'query') and hasattr(ctx.event.query, 'user_message'):
                user_message = ctx.event.query.user_message
                if isinstance(user_message.content, list):
                    for content in user_message.content:
                        if hasattr(content, 'text'):
                            content.text = modified_msg
                else:
                    user_message.content = modified_msg

                # 更新会话中的最后一条消息
                if hasattr(ctx.event.query, 'session') and hasattr(ctx.event.query.session, 'using_conversation'):
                    conversation = ctx.event.query.session.using_conversation
                    if hasattr(conversation, 'messages') and conversation.messages:
                        last_message = conversation.messages[-1]
                        if hasattr(last_message, 'content'):
                            last_message.content = modified_msg

        except Exception as e:
            self.host.logger.error(f"Error processing message: {e}")

    def __del__(self):
        pass

