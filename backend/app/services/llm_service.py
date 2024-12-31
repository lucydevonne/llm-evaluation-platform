"""
LLM Service Module
Handles interactions with different language models
"""

from typing import Dict, Any, Optional, Tuple
import os
import time
import logging
import aiohttp
import asyncio
from dotenv import load_dotenv
from app.core.exceptions import ModelNotFoundError, EvaluationError

load_dotenv()
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        """Initialize API clients"""
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.hf_api_key = os.getenv("HUGGING_FACE_API_KEY")
        
        if not self.groq_api_key or not self.hf_api_key:
            raise ValueError("Missing API keys. Both GROQ_API_KEY and HUGGING_FACE_API_KEY are required.")
            
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.hf_url = "https://api-inference.huggingface.co/models/"
        
        self.models = {
            "mixtral-8x7b": {
                "provider": "groq",
                "model": "mixtral-8x7b-32768"
            },
            "gpt-2": {
                "provider": "huggingface",
                "model": "gpt2"
            },
        }

    async def get_response(self, prompt: str, system_prompt: str, model: str) -> str:
        """Get response from specified model"""
        if model not in self.models:
            raise ModelNotFoundError(model)
            
        model_config = self.models[model]
        provider = model_config["provider"]
        actual_model = model_config["model"]
        
        start_time = time.time()
        
        try:
            if provider == "groq":
                response = await self._query_groq(prompt, system_prompt, actual_model)
            else:  # huggingface
                response = await self._query_huggingface(prompt, system_prompt, actual_model)
                
            return response
            
        except Exception as e:
            logger.error(f"Error getting response from {model}: {str(e)}")
            raise EvaluationError(model, str(e))

    async def _query_groq(self, prompt: str, system_prompt: str, model: str) -> str:
        """Send request to Groq API"""
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.7
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.groq_url,
                    headers=headers,
                    json=payload,
                    timeout=30
                ) as response:
                    response_json = await response.json()
                    
                    if response.status != 200:
                        error_msg = response_json.get('error', {}).get('message', 'Unknown error')
                        raise EvaluationError(model, f"Groq API Error: {error_msg}")
                    
                    return response_json["choices"][0]["message"]["content"]
                    
        except asyncio.TimeoutError:
            raise EvaluationError(model, "Request timed out")
        except Exception as e:
            raise EvaluationError(model, str(e))

    async def _query_huggingface(self, prompt: str, system_prompt: str, model: str) -> str:
        """Send request to Hugging Face API"""
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        headers = {
            "Authorization": f"Bearer {self.hf_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": 100,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.hf_url}{model}",
                    headers=headers,
                    json=payload,
                    timeout=30
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise EvaluationError(model, f"HuggingFace API Error: {error_text}")
                    
                    result = await response.json()
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get("generated_text", "").strip()
                    return str(result).strip()
                    
        except asyncio.TimeoutError:
            raise EvaluationError(model, "Request timed out")
        except Exception as e:
            raise EvaluationError(model, str(e))

    def _evaluate_response(self, response: str) -> Tuple[int, int]:
        """Evaluate response quality"""
        accuracy = 0
        relevancy = 0
        
        # Length points (30)
        if len(response) > 50:
            accuracy += 30
            relevancy += 30
            
        # Structure points (20)
        if response.strip().endswith(('.', '!', '?')):
            accuracy += 20
            relevancy += 20
            
        # Content points (20)
        if any(word in response.lower() for word in ['because', 'therefore', 'however', 'example']):
            accuracy += 20
            relevancy += 20
            
        # Format points (20)
        if response.strip() and not response.strip().isupper():
            accuracy += 20
            relevancy += 20
            
        return accuracy, relevancy

# Make the service class available for import
__all__ = ['LLMService']