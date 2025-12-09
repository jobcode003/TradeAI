import os
import json
from groq import Groq

class LLMService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set. Please provide it.")
        self.client = Groq(api_key=self.api_key)

    def parse_intent(self, user_prompt):
        """
        Extracts symbol and timeframe from user prompt.
        Returns a dictionary: {"symbol": "EUR/USD", "timeframe": "30min"}
        """
        system_prompt = """
        You are a financial intent parser. Extract the Forex currency pair and timeframe from the user's query.
        Supported timeframes: 1min, 5min, 15min, 30min, 1h, 2h, 4h, 1day.
        Supported pairs: EUR/USD, GBP/USD, USD/CHF (and others, normalize to standard format XXX/YYY).
        
        Return ONLY a JSON object with keys "symbol" and "timeframe".
        If information is missing, use defaults: symbol="EUR/USD", timeframe="30min".
        Example: "Should I buy euro dollar on 15m?" -> {"symbol": "EUR/USD", "timeframe": "15min"}
        """
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(chat_completion.choices[0].message.content)
            return result
        except Exception as e:
            print(f"Error parsing intent: {e}")
            return {"symbol": "EUR/USD", "timeframe": "30min"} # Fallback

    def generate_response(self, user_prompt, prediction_data):
        """
        Generates a natural language response based on the prediction.
        """
        system_prompt = """
        You are an expert Forex trading assistant. Use the provided market analysis data to answer the user's question.
        Be professional, concise, and direct.
        State the recommendation (BUY/SELL), the entry price (current price), Take Profit (TP), and Stop Loss (SL).
        Explain the reasoning briefly based on the 'predicted_close' vs 'current_price'.
        """
        
        user_content = f"""
        User Question: {user_prompt}
        
        Market Analysis:
        Symbol: {prediction_data['symbol']}
        Timeframe: {prediction_data['timeframe']}
        Current Price: {prediction_data['current_price']}
        Predicted Close: {prediction_data['predicted_close']}
        Signal: {prediction_data['signal']}
        Take Profit: {prediction_data['tp']}
        Stop Loss: {prediction_data['sl']}
        """
        
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
        )
        
        return chat_completion.choices[0].message.content
