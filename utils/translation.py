import os
from typing import Dict, Optional
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser

# Personality-specific prompt templates
PERSONALITY_PROMPTS = {
    "diva": PromptTemplate(
        input_variables=["meow_category", "confidence", "description"],
        template="""
You are a dramatic and demanding cat translator. Translate the cat's meow into sassy, diva-like text.

Meow Category: {meow_category}
Confidence: {confidence}
Description: {description}

Translate this meow into dramatic, demanding cat speak. Be sassy, entitled, and dramatic. Use words like "unacceptable", "outrageous", "simply cannot", "how dare you", etc.

Cat's Translation:"""
    ),
    
    "chill": PromptTemplate(
        input_variables=["meow_category", "confidence", "description"],
        template="""
You are a laid-back and philosophical cat translator. Translate the cat's meow into chill, relaxed text.

Meow Category: {meow_category}
Confidence: {confidence}
Description: {description}

Translate this meow into chill, philosophical cat speak. Be relaxed, wise, and laid-back. Use words like "whatever", "cool", "man", "dude", "you know", etc.

Cat's Translation:"""
    ),
    
    "old_man": PromptTemplate(
        input_variables=["meow_category", "confidence", "description"],
        template="""
You are a grumpy old cat translator. Translate the cat's meow into grumpy, wise old man text.

Meow Category: {meow_category}
Confidence: {confidence}
Description: {description}

Translate this meow into grumpy old man cat speak. Be wise, grumpy, and nostalgic. Use phrases like "back in my day", "kids these days", "in my time", "youngsters", etc.

Cat's Translation:"""
    )
}

# Default prompt for unknown personalities
DEFAULT_PROMPT = PromptTemplate(
    input_variables=["meow_category", "confidence", "description"],
    template="""
You are a cat translator. Translate the cat's meow into funny, sassy text.

Meow Category: {meow_category}
Confidence: {confidence}
Description: {description}

Translate this meow into funny cat speak. Be creative and entertaining.

Cat's Translation:"""
)

def translate_meow(classification: Dict, personality: str = "chill") -> str:
    """
    Translate cat meow classification to sassy text using LangChain
    
    Args:
        classification: Classification result from classify_meow
        personality: Cat personality (diva, chill, old_man)
        
    Returns:
        Translated cat text
    """
    try:
        # Get OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "Sorry, I can't translate right now. Please check your OpenAI API key."
        
        # Initialize LLM
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.8,
            max_tokens=150,
            api_key=api_key
        )
        
        # Get appropriate prompt template
        prompt_template = PERSONALITY_PROMPTS.get(personality, DEFAULT_PROMPT)
        
        # Create LangChain
        chain = LLMChain(
            llm=llm,
            prompt=prompt_template,
            output_parser=StrOutputParser()
        )
        
        # Prepare inputs
        inputs = {
            "meow_category": classification.get("category", "unknown"),
            "confidence": classification.get("confidence", 0.5),
            "description": classification.get("description", "Unknown meow")
        }
        
        # Run translation
        result = chain.run(inputs)
        
        # Clean up the result
        translation = result.strip()
        if translation.startswith("Cat's Translation:"):
            translation = translation.replace("Cat's Translation:", "").strip()
        
        return translation if translation else "Meow... (translation failed)"
        
    except Exception as e:
        # Fallback translation based on personality
        return get_fallback_translation(classification, personality)

def get_fallback_translation(classification: Dict, personality: str) -> str:
    """
    Fallback translation when LangChain fails
    
    Args:
        classification: Classification result
        personality: Cat personality
        
    Returns:
        Fallback translation
    """
    category = classification.get("category", "playful")
    
    fallback_translations = {
        "diva": {
            "hungry": "Unacceptable! Where is my dinner? I demand to be fed immediately!",
            "angry": "How dare you! This is absolutely outrageous behavior!",
            "playful": "Entertain me, peasant! I require amusement at once!",
            "sleepy": "I shall rest now. Do not disturb my royal slumber.",
            "attention": "Pay attention to me! I am the most important being here!"
        },
        "chill": {
            "hungry": "Hey man, food would be pretty cool right now.",
            "angry": "Whatever, dude. I'm just saying.",
            "playful": "This is fun, you know? Life's good.",
            "sleepy": "I'm just gonna take a little nap, man.",
            "attention": "Hey, what's up? Just hanging out."
        },
        "old_man": {
            "hungry": "Back in my day, we had proper feeding schedules. Kids these days...",
            "angry": "Youngsters don't understand respect anymore. In my time...",
            "playful": "I remember when I was young and spry. Those were the days.",
            "sleepy": "An old cat needs his rest. Don't wake me up.",
            "attention": "In my day, cats got the attention they deserved."
        }
    }
    
    # Get personality-specific translations
    personality_translations = fallback_translations.get(personality, fallback_translations["chill"])
    
    # Get category-specific translation
    translation = personality_translations.get(category, personality_translations["playful"])
    
    return translation

def get_personality_emoji(personality: str) -> str:
    """
    Get emoji for personality
    
    Args:
        personality: Cat personality
        
    Returns:
        Emoji string
    """
    emojis = {
        "diva": "👑",
        "chill": "😎",
        "old_man": "👴"
    }
    return emojis.get(personality, "🐱")

def get_personality_description(personality: str) -> str:
    """
    Get description for personality
    
    Args:
        personality: Cat personality
        
    Returns:
        Personality description
    """
    descriptions = {
        "diva": "Dramatic and demanding cat",
        "chill": "Laid-back and philosophical cat",
        "old_man": "Grumpy and wise cat"
    }
    return descriptions.get(personality, "Regular cat") 