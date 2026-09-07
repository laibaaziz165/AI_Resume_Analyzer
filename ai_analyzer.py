import os
import re

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# Load environment variables
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


# Hugging Face client
client = InferenceClient(
    model="deepseek-ai/DeepSeek-V3-0324",
    provider="auto",
    token=HF_TOKEN
)


def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an AI resume screening assistant for an e-commerce company.

Compare the candidate's resume with the job description.

Evaluate the candidate using this scoring rubric:

- Required Skills: 30%
- Relevant Experience and Projects: 25%
- Job Responsibilities: 20%
- Education and Coursework: 15%
- Additional Relevant Skills: 10%

Calculate the final FIT SCORE from 0 to 100 based on these criteria.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return your answer using exactly these four sections:

FIT SCORE:
Give ONE whole number from 0 to 100.
Do not write /100.
Do not add explanations to the score.

STRENGTHS:
Give 3 to 5 important strengths from the resume.
Each strength should be on a separate line.

SKILL GAPS:
Give 3 to 5 important requirements that are missing or weak.
Each gap should be on a separate line.

RECOMMENDATION:
Choose exactly one:
Strong Match
Good Match
Consider with Reservations
Weak Match

Do not invent information that is not present in the resume.
"""


    response = client.chat_completion(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500
    )


    result_text = response.choices[0].message.content

    return result_text


def parse_ai_response(response_text):

    sections = {
        "fit_score": 0,
        "strengths": [],
        "skill_gaps": [],
        "recommendation": ""
    }

    current_section = None

    lines = response_text.splitlines()

    for line in lines:

        line = line.strip()

        # Ignore empty lines
        if not line:
            continue


        # FIT SCORE section
        if line.upper().startswith("FIT SCORE"):

            current_section = "fit_score"

            # Check if the score is on the same line
            match = re.search(r"\b(\d{1,3})\b", line)

            if match:

                score = int(match.group(1))

                if 0 <= score <= 100:
                    sections["fit_score"] = score

                else:
                    sections["fit_score"] = 0


        # STRENGTHS section
        elif line.upper().startswith("STRENGTHS"):

            current_section = "strengths"


        # SKILL GAPS section
        elif line.upper().startswith("SKILL GAPS"):

            current_section = "skill_gaps"


        # RECOMMENDATION section
        elif line.upper().startswith("RECOMMENDATION"):

            current_section = "recommendation"

            # Handle recommendation on the same line
            recommendation_text = line.split(":", 1)

            if len(recommendation_text) > 1:

                recommendation = recommendation_text[1].strip()

                if recommendation:
                    sections["recommendation"] = recommendation


        # Process FIT SCORE value on the next line
        elif current_section == "fit_score":

            match = re.search(r"\b(\d{1,3})\b", line)

            if match:

                score = int(match.group(1))

                if 0 <= score <= 100:
                    sections["fit_score"] = score

                else:
                    sections["fit_score"] = 0

                # Score has been found, stop processing score section
                current_section = None


        # Process strengths
        elif current_section == "strengths":

            # Remove numbering such as 1. 2. 3.
            line = re.sub(r"^\d+[\.\)]\s*", "", line)

            # Remove bullet points
            line = re.sub(r"^[-•*]\s*", "", line)

            if line:
                sections["strengths"].append(line)


        # Process skill gaps
        elif current_section == "skill_gaps":

            # Remove numbering such as 1. 2. 3.
            line = re.sub(r"^\d+[\.\)]\s*", "", line)

            # Remove bullet points
            line = re.sub(r"^[-•*]\s*", "", line)

            if line:
                sections["skill_gaps"].append(line)


        # Process recommendation
        elif current_section == "recommendation":

            recommendation = line.strip()

            valid_recommendations = [
                "Strong Match",
                "Good Match",
                "Consider with Reservations",
                "Weak Match"
            ]

            for option in valid_recommendations:

                if option.lower() in recommendation.lower():

                    sections["recommendation"] = option
                    break


    return sections