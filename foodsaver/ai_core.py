import google.generativeai as genai
import os
import random

def get_surplus_prediction():
    """
    Connects to Gemini to predict future surplus based on patterns.
    Falls back to mock data if no API key is set.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        # Mock prediction for demo
        foods = ["Rice", "Curry", "Bread", "Vegetables"]
        predicted_food = random.choice(foods)
        predicted_qty = random.randint(10, 30)
        return {
            "prediction": f"Expected {predicted_qty}kg of {predicted_food} tomorrow based on Friday trends.",
            "status": "mock"
        }

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # In a real app, we would feed historical data CSV here
        prompt = "Analyze restaurant food waste trends for weekends. Predict surplus for tomorrow."
        
        response = model.generate_content(prompt)
        return {
            "prediction": response.text,
            "status": "real"
        }
    except Exception as e:
        return {
            "prediction": f"AI Error: {str(e)}",
            "status": "error"
        }
