class ManagementAgentExtractContentHelper:
    @staticmethod
    def extract_text_from_response(response_or_content) -> str:
        if hasattr(response_or_content, 'content'):
            content = response_or_content.content
        else:
            content = response_or_content
            
        if isinstance(content, str):
            return content
        
        if isinstance(content, list):
            # Ưu tiên lấy text block trước
            for block in reversed(content):
                if isinstance(block, dict) and block.get("type") == "text":
                    return block.get("text", "")
            
            # Fallback: lấy thinking block nếu không có text
            for block in reversed(content):
                if isinstance(block, dict) and block.get("type") == "thinking":
                    return ""
        
        return ""  # Trả về empty string thay vì str(content)

    @staticmethod
    def extract_qdrant_search_results(search_result):
        """Trả về list of dicts thay vì set of tuples"""
        seen = {}
        for point in search_result:
            if 'category' in point.payload and 'wallet' in point.payload:
                category = point.payload.get('category')
                wallet = point.payload.get('wallet')
                key = (category, wallet)
                if key not in seen:
                    seen[key] = {"category": category, "wallet": wallet}
        return list(seen.values())