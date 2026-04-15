class ManagementAgentExtractContentHelper:
    @staticmethod
    def extract_text_from_response(response_or_content) -> str:
        # Nếu là AIMessage hoặc object có .content
        if hasattr(response_or_content, 'content'):
            content = response_or_content.content
        else:
            content = response_or_content
            
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            for block in reversed(content):
                if isinstance(block, dict) and block.get("type") == "text":
                    return block.get("text", "")
        return str(content)