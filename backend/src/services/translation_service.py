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
        # Initialize conversation memory for each personality
        self.conversation_memories = {
            "diva": [],
            "chill": [],
            "old_man": []
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
- Use SIMPLE ENGLISH words that a child could understand
- Be dramatic and spoiled. Use simple phrases like "no good", "bad", "want food", "play now", etc.
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
- Use SIMPLE ENGLISH words that a child could understand
- Be cool and Zen-like. Use simple words like "okay", "good", "fine", "cool", "whatever".
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
- Use SIMPLE ENGLISH words that a child could understand
- Be grumpy and nostalgic. Use simple phrases like "old days", "young cats", "not same", "better before".
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
- Use SIMPLE ENGLISH words that a child could understand
- Be creative and entertaining. Reference previous meows if relevant.
- Make it quick and witty with simple words.

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
            
            # Get appropriate prompt template and conversation history
            prompt_template = self.personality_prompts.get(personality, self.default_prompt)
            conversation_history = self.get_conversation_history(personality)
            
            # Prepare inputs
            inputs = {
                "meow_category": classification.get("category", "unknown"),
                "confidence": classification.get("confidence", 0.5),
                "description": classification.get("description", "Unknown meow"),
                "actual_duration": classification.get("actual_duration", 1.0),
                "chat_history": conversation_history
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
            print(f"Conversation History: {conversation_history}")
            print(f"=====================")
            
            # Run translation with memory
            result = chain.run(inputs)
            
            # Clean up the result
            translation = result.strip()
            if translation.startswith("Cat's Translation:"):
                translation = translation.replace("Cat's Translation:", "").strip()
            
            # Save conversation to memory
            self.save_conversation(personality, classification.get("category", "unknown"), translation)
            
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
            if personality in self.conversation_memories:
                self.conversation_memories[personality] = []
        else:
            for personality in self.conversation_memories:
                self.conversation_memories[personality] = []
    
    def get_conversation_history(self, personality: str) -> str:
        """
        Get conversation history for a specific personality.
        
        Args:
            personality: Cat personality
            
        Returns:
            Conversation history as string
        """
        memory = self.conversation_memories.get(personality, [])
        if not memory:
            return "No previous meows."
        
        # Format conversation history
        history_lines = []
        for i, (category, response) in enumerate(memory[-3:], 1):  # Last 3 interactions
            history_lines.append(f"Meow {i}: {category} → Cat: {response}")
        
        return "\n".join(history_lines)
    
    def save_conversation(self, personality: str, category: str, response: str):
        """
        Save a conversation interaction to memory.
        
        Args:
            personality: Cat personality
            category: Meow category
            response: Cat's response
        """
        if personality not in self.conversation_memories:
            self.conversation_memories[personality] = []
        
        # Add to memory (keep last 5 interactions)
        self.conversation_memories[personality].append((category, response))
        if len(self.conversation_memories[personality]) > 5:
            self.conversation_memories[personality] = self.conversation_memories[personality][-5:]
    
    def get_memory_stats(self) -> Dict[str, int]:
        """
        Get memory statistics for all personalities.
        
        Returns:
            Dictionary with personality names and conversation count
        """
        stats = {}
        for personality, memory in self.conversation_memories.items():
            stats[personality] = len(memory)
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