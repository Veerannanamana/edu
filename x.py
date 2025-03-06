import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import time
import sympy as sp
from sympy import pi
from io import BytesIO
import pygame

# Initialize the recognizer
recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech using gTTS and play the audio directly using pygame."""
    try:
        tts = gTTS(text=text, lang='en')
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)

        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for the audio to finish playing
            pygame.time.Clock().tick(10)
    except Exception as e:
        st.error(f"Error in speech synthesis: {e}")

# Rest of the code remains the same...

def listen():
    """Listen to user's speech and convert it to text."""
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio).lower()
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that. Please try again."
        except sr.RequestError:
            return "Sorry, there was an issue with the speech recognition service."

def calculate(expression):
    """Evaluate a mathematical expression after replacing spoken words with symbols."""
    expression = expression.replace("plus", "+").replace("minus", "-").replace("into", "*").replace("times", "*")
    expression = expression.replace("divide", "/").replace("cap", "**").replace("x", "*")  # Handle multiplication

    try:
        result = eval(expression)  
        return round(result, 2) if isinstance(result, float) else result
    except Exception:
        return "Error: Invalid Syntax"

def integrate_expression(expression, lower_limit=None, upper_limit=None):
    """Perform symbolic integration step-by-step with optional definite limits."""
    try:
        x = sp.symbols('x')
        expr = sp.sympify(expression)

        steps = [f"**Step 1: Given Expression**\n\n∫ {expression} dx"]
        
        if lower_limit is not None and upper_limit is not None:
            definite_result = sp.integrate(expr, (x, lower_limit, upper_limit)).evalf(3)
            steps.append(f"**Final Result:**\n\n∫ {expression} dx from {lower_limit} to {upper_limit} = {definite_result}")
            return steps

        integral_result = sp.integrate(expr, x)
        steps.append(f"**Final Result:**\n\n∫ {expression} dx = {integral_result} + C")
        return steps

    except Exception as e:
        return [f"Error: {str(e)}"]

def differentiate_expression(expression):
    """Perform symbolic differentiation step-by-step."""
    try:
        x = sp.symbols('x')
        expr = sp.sympify(expression)
        derivative_result = sp.diff(expr, x)
        return [f"**Final Result:**\n\nd/dx ({expression}) = {derivative_result}"]
    except Exception as e:
        return [f"Error: {str(e)}"]

def trigonometry_operations(expression):
    """Evaluate trigonometric functions and return exact values where possible."""
    try:
        expr = sp.sympify(expression, evaluate=False)
        result = sp.simplify(expr)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("Voice-Enabled Calculator")

    # Add some custom styles
    st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextArea>textarea {
        border-radius: 4px;
        border: 1px solid #ccc;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("", ["About", "Calculator"])

    if page == "About":
        st.markdown("### About the Calculator")
        st.write("""
        This calculator performs arithmetic, integration, differentiation, and trigonometry calculations using voice commands.
        """)

    elif page == "Calculator":
        st.sidebar.markdown("### Calculator")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Basic Operations", "Mathematical Expressions", "Integration", "Differentiation", "Trigonometry"
        ])

        with tab1:
            st.subheader("Basic Operations (Voice-Based)")
            if st.button("Start Listening 🎤"):
                user_input = listen()
                if user_input:
                    result = calculate(user_input)
                    st.write(f"Result: {result}")
                    speak(str(result))
                    time.sleep(1)

        with tab2:
            st.subheader("Mathematical Expressions")
            expression = st.text_area("Enter a mathematical expression", key="math_expr")
            if st.button("Calculate"):
                if expression:
                    result = calculate(expression)
                    st.write(f"**Result:** {result}")
                    speak(f"The result is {result}")

        with tab3:
            st.subheader("Integration Operations")
            integral_expr = st.text_area("∫ Enter function to integrate", key="integral_expr")
            lower_limit = st.text_input("Lower Limit (optional)", key="lower_limit")
            upper_limit = st.text_input("Upper Limit (optional)", key="upper_limit")

            if st.button("Integrate"):
                steps = integrate_expression(integral_expr, lower_limit, upper_limit)
                for step in steps:
                    st.markdown(step)

        with tab4:
            st.subheader("Differentiation Operations")
            diff_expr = st.text_area("d/dx Enter function to differentiate", key="diff_expr")
            if st.button("Differentiate"):
                steps = differentiate_expression(diff_expr)
                for step in steps:
                    st.markdown(step)

        with tab5:
            st.subheader("Trigonometry Operations")
            trigo_expr = st.text_area("Enter trigonometric function", key="trigo_expr")
            if st.button("Evaluate Trigonometry"):
                result = trigonometry_operations(trigo_expr)
                st.write(f"**Result:** {result}")
                speak(f"The result is {result}")

if __name__ == "__main__":
    main()