from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini API (replace with your actual API key)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # Ensure GOOGLE_API_KEY is set in your environment
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_study_plan(subject, topics, duration, study_style):
    """Generates a study plan using Gemini."""

    prompt = f"""
    Create a study plan for {subject}.
    Topics: {', '.join(topics)}.
    Duration: {duration} days.
    Study Style: {study_style}.

    Include:
    - Daily schedule with specific topics and activities.
    - Recommended resources (books, websites, videos).
    - Practice exercises and assessments.
    - Break times and review sessions.
    - Time allocation for each topic.
    - Prioritization of topics.
    - Flexibility for unexpected delays.
    - A motivational tone.

    Output in a structured, easy-to-read format.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating study plan: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        topics = request.form.getlist('topics[]')  # Handle multiple topics
        duration = request.form['duration']
        study_style = request.form['study_style']

        study_plan = generate_study_plan(subject, topics, duration, study_style)
        return render_template('index.html', study_plan=study_plan, subject=subject, topics=topics, duration=duration, study_style=study_style)

    return render_template('index.html', study_plan=None)

@app.route('/add_topic', methods=['POST'])
def add_topic():
  """Adds a new topic input field dynamically."""
  return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)