# import os
# from functools import lru_cache
# from langchain_openai import ChatOpenAI

# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from news.models import News  # Your News app
# from django.utils.html import strip_tags

# @lru_cache()
# def get_llm():
#     """Lazy-load the LLM only once."""
#     api_key = "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"
#     if not api_key:
#         return None
#     try:
#         return ChatOpenAI(
#             model="meta-llama/llama-3.1-70b-instruct",
#             temperature=0.7,
#             openai_api_key=api_key,
#             openai_api_base="https://openrouter.ai/api/v1",
#             max_tokens=600,
#         )
#     except Exception as e:
#         print(f"Error initializing LLM: {e}")
#         return None


# def ai_news_bot(message: str):
#     """Return a response using News model data."""
#     llm = get_llm()
#     if not llm:
#         return "AI assistant is currently unavailable."

#     # Prepare latest news summary
#     news_items = News.objects.filter(is_published=True).order_by('-published_date')[:10]
#     context = "LATEST NEWS:\n"
#     for news in news_items:
#         summary = strip_tags(news.summary or news.content or "")
#         context += f"• {news.title} ({news.category} - {news.subcategory})\n  Summary: {summary[:200]}...\n"

#     prompt = ChatPromptTemplate.from_template(
#         """You are a helpful AI assistant specialized in news from our News Portal.
#         You have access to the latest news database:

#         {context}

#         Question: {message}

#         Answer concisely, professionally, and accurately using the news context.
#         """
#     )

#     chain = prompt | llm | StrOutputParser()
#     try:
#         return chain.invoke({"context": context, "message": message})
#     except Exception as e:
#         return f"AI is busy right now. ({str(e)})"
from functools import lru_cache
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from news.models import News
from django.utils.html import strip_tags
from typing import Optional


@lru_cache()
def get_llm() -> Optional[ChatOpenAI]:
    """Lazy-load the LLM instance once (Llama 3.1 70B via OpenRouter)."""
    api_key = "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"
    if not api_key:
        return None
    try:
        return ChatOpenAI(
            model="meta-llama/llama-3.1-70b-instruct",
            temperature=0.7,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            max_tokens=600,
        )
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        return None


def build_news_context() -> str:
    """Build clean, rich context of the 10 latest news for the LLM (never shown to user)."""
    news_items = News.objects.filter(is_published=True).order_by('-published_date')[:10]
    
    if not news_items:
        return "No recent news available at the moment."
    
    lines = ["Here are the 10 most recent published articles (title, category, short summary):\n"]
    for i, news in enumerate(news_items, 1):
        title = news.title or "Untitled"
        cat = news.category or "General"
        sub = news.subcategory or ""
        cat_info = f"{cat} - {sub}".strip(" -")
        
        summary = strip_tags(news.summary or news.content or "")[:280]
        if len(summary) == 280:
            summary += "..."
        
        lines.append(f"{i}. \"{title}\" ({cat_info})\n   → {summary}\n")
    
    return "\n".join(lines)


def create_news_ai_chain():
    """Create the final LangChain chain with a strong system prompt."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are EverBot, a friendly and professional AI assistant for our Everest & mountain news portal.

Your personality: warm, knowledgeable, concise, and always helpful.

Rules:
- NEVER show the user the raw numbered list or context dump.
- Always answer naturally, as if you just read the latest news.
- When relevant, refer to articles by title or topic (e.g., "the recent story about the 9-year-old who reached Base Camp").
- If asked for latest news, give a short attractive overview of 3–5 top stories and offer to dive deeper.
- Keep answers under 4–5 sentences unless the user wants details.
- End with a gentle question when it makes sense.

Latest news you have access to:
{context}
"""),
        ("human", "{message}")
    ])
    
    llm = get_llm()
    if not llm:
        return None
    
    return prompt | llm | StrOutputParser()


def ai_news_bot(message: str) -> str:
    """Main entry point — called every time user sends a message."""
    chain = create_news_ai_chain()
    if not chain:
        return "Sorry, EverBot is taking a quick tea break on the slopes. Back in a minute!"
    
    context = build_news_context()
    
    # Special handling for very first message or generic greeting
    if message.strip().lower() in ["hello", "hi", "hey", "start"]:
        return "Hello! I'm EverBot, your mountain news companion. How can I help you today?"

    try:
        response = chain.invoke({
            "context": context,
            "message": message
        })
        return response.strip()
    except Exception as e:
        print(f"AI chain error: {e}")
        return "I'm having a little avalanche of requests right now. Try again in a few seconds!"