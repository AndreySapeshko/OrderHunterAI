from enum import StrEnum


class LeadCategory(StrEnum):
    CHATBOT = "chatbot"
    RAG_KB = "rag_knowledge_base"
    AUTOMATION = "automation"
    VOICE_AGENT = "voice_agent"
    ANALYTICS = "analytics"
    SALES_AGENT = "sales_agent"
    OTHER_AI = "other_ai"
    NOT_AI = "not_ai"


class LeadStatus(StrEnum):
    NEW = "new"
    SAVED = "saved"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"
