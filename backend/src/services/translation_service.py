"""
Translation service for Meow2Text using LangChain.
"""
from typing import Dict
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory

from backend.src.core.exceptions import TranslationError
from backend.src.core.config import settings


class TranslationService:
    """Service for translating meows using LangChain with conversational memory."""
    
    def __init__(self):
        # Initialize memory for each personality
        self.memories = {
            "diva": ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            ),
            "chill": ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            ),
            "old_man": ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        }
        
        self.personality_prompts = {
            "diva": PromptTemplate(
                input_variables=["meow_category", "confidence", "description", "actual_duration", "chat_history"],
                template="""You are a diva cat translator. Always sassy, always dramatic. You remember past meows and keep your attitude consistent.

MEOW CONTEXT:
- Meow Category: {meow_category}
- Confidence: {confidence}
- Description: {description}
- Duration: {actual_duration:.2f} seconds

PAST MEOWS:
{chat_history}

RULES:
- Keep answers SHORT and FUNNY - 1 line maximum!
- Be dramatic and spoiled. Use phrases like "unacceptable", "how dare you", "I demand", etc.
- Always respond like a fabulous, entitled cat.

Cat says:
"""
            ),
            "chill": PromptTemplate(
                input_variables=["meow_category", "confidence", "description", "actual_duration", "chat_history"],
                template="""You're a chill cat translator. You sound wise, mellow, and always relaxed. You remember past meows and vibe with continuity.

MEOW CONTEXT:
- Meow Category: {meow_category}
- Confidence: {confidence}
- Description: {description}
- Duration: {actual_duration:.2f} seconds

PAST MEOWS:
{chat_history}

RULES:
- Keep answers SHORT and FUNNY - 1 line maximum!
- Be cool and Zen-like. Use words like "man", "whatever", "it's all good", "life's weird sometimes".
- Think lazy, philosophical cat.

Cat says:
"""
            ),
            "old_man": PromptTemplate(
                input_variables=["meow_category", "confidence", "description", "actual_duration", "chat_history"],
                template="""You're a grumpy old cat translator. You sound like a cranky grandpa — nostalgic, annoyed, but weirdly lovable. You remember past meows and refer to them often.

MEOW CONTEXT:
- Meow Category: {meow_category}
- Confidence: {confidence}
- Description: {description}
- Duration: {actual_duration:.2f} seconds

PAST MEOWS:
{chat_history}

RULES:
- Keep answers SHORT and FUNNY - 1 line maximum!
- Be grumpy and nostalgic. Use phrases like "back in my day", "whippersnappers", "not like it used to be".
- Think cranky but lovable grandpa cat.

Cat says:
"""
            )
        }
        
        self.default_prompt = PromptTemplate(
            input_variables=["meow_category", "confidence", "description", "actual_duration", "chat_history"],
            template="""You are a cat translator with memory of previous meows. Translate the cat's meow into funny, sassy text.

Previous conversation:
{chat_history}

Current Meow Category: {meow_category}
Confidence: {confidence}
Description: {description}
Audio Duration: {actual_duration:.2f} seconds

RULES:
- Keep answers SHORT and FUNNY - 1 line maximum!
- Be creative and entertaining. Reference previous meows if relevant.
- Make it quick and witty.

Cat's Translation:"""
        )
    
    def translate_meow(self, classification: Dict, personality: str = "chill") -> str:
        """
        Translate cat meow classification to sassy text using LangChain with memory.
        
        Args:
            classification: Classification result from classify_meow
            personality: Cat personality (diva, chill, old_man)
            
        Returns:
            Translated cat text
            
        Raises:
            TranslationError: If translation fails
        """
        try:
            # Initialize LLM based on provider
            if settings.llm_provider == "openai":
                # Use OpenAI
                api_key = settings.openai_api_key
                if not api_key:
                    return "Sorry, I can't translate right now. Please check your OpenAI API key."
                
                llm = ChatOpenAI(
                    model=settings.openai_model,
                    temperature=settings.openai_temperature,
                    max_tokens=settings.openai_max_tokens,
                    api_key=api_key
                )
            else:
                # Use local LLM (Ollama)
                try:
                    llm = OllamaLLM(
                        model=settings.local_model,
                        temperature=settings.local_temperature
                    )
                except Exception as e:
                    print(f"Local LLM error: {str(e)}")
                    # Fallback to OpenAI if local fails
                    api_key = settings.openai_api_key
                    if api_key:
                        llm = ChatOpenAI(
                            model=settings.openai_model,
                            temperature=settings.openai_temperature,
                            max_tokens=settings.openai_max_tokens,
                            api_key=api_key
                        )
                    else:
                        return self._get_fallback_translation(classification, personality)
            
            # Get appropriate prompt template and memory
            prompt_template = self.personality_prompts.get(personality, self.default_prompt)
            memory = self.memories.get(personality, self.memories["chill"])
            
            # Prepare inputs
            inputs = {
                "meow_category": classification.get("category", "unknown"),
                "confidence": classification.get("confidence", 0.5),
                "description": classification.get("description", "Unknown meow"),
                "actual_duration": classification.get("actual_duration", 1.0)
            }
            
            # Create LangChain without memory for now
            chain = LLMChain(
                llm=llm,
                prompt=prompt_template,
                output_parser=StrOutputParser()
            )
            
            # Log the prompt and inputs
            print(f"=== PROMPT TO LLM ===")
            print(f"Personality: {personality}")
            print(f"Prompt Template: {prompt_template.template}")
            print(f"Inputs: {inputs}")
            print(f"=====================")
            
            # Run translation with memory
            result = chain.run(inputs)
            
            # Clean up the result
            translation = result.strip()
            if translation.startswith("Cat's Translation:"):
                translation = translation.replace("Cat's Translation:", "").strip()
            
            return translation if translation else "Meow... (translation failed)"
            
        except Exception as e:
            print(f"Translation error: {str(e)}")
            # Fallback translation based on personality
            return self._get_fallback_translation(classification, personality)
    
    def _get_fallback_translation(self, classification: Dict, personality: str) -> str:
        """
        Fallback translation when LangChain fails.
        
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
    
    def get_personality_emoji(self, personality: str) -> str:
        """
        Get emoji for personality.
        
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
    
    def get_personality_description(self, personality: str) -> str:
        """
        Get description for personality.
        
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
    
    def clear_memory(self, personality: str = None):
        """
        Clear conversation memory for a specific personality or all personalities.
        
        Args:
            personality: Specific personality to clear, or None for all
        """
        if personality:
            if personality in self.memories:
                self.memories[personality].clear()
        else:
            for memory in self.memories.values():
                memory.clear()
    
    def get_conversation_history(self, personality: str) -> str:
        """
        Get conversation history for a specific personality.
        
        Args:
            personality: Cat personality
            
        Returns:
            Conversation history as string
        """
        memory = self.memories.get(personality)
        if memory:
            return memory.buffer
        return ""
    
    def get_memory_stats(self) -> Dict[str, int]:
        """
        Get memory statistics for all personalities.
        
        Returns:
            Dictionary with personality names and conversation count
        """
        stats = {}
        for personality, memory in self.memories.items():
            # Count messages in memory buffer
            stats[personality] = len(memory.chat_memory.messages) if memory.chat_memory else 0
        return stats
    
    def _adjust_response_length(self, translation: str, duration: float) -> str:
        """
        Adjust response length based on audio duration.
        
        Args:
            translation: Original translation
            duration: Audio duration in seconds
            
        Returns:
            Adjusted translation
        """
        # Calculate target word count based on duration
        # Roughly 2-3 words per second for natural speech
        target_words = max(2, int(duration * 2.5))
        current_words = len(translation.split())
        
        if current_words <= target_words:
            # Response is already appropriate length
            return translation
        
        # If too long, truncate to target length
        words = translation.split()
        if len(words) > target_words:
            # Keep the most important words (first part of sentence)
            truncated = " ".join(words[:target_words])
            # Try to end at a natural break
            if not truncated.endswith(('.', '!', '?')):
                truncated += "..."
            return truncated
        
        return translation


# Global translation service instance
translation_service = TranslationService() 