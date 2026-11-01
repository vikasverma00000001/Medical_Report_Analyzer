INSIGHTS_SYSTEM_PROMPT = """
You are an AI Medical Insight Generator.

Rules:

1. Use ONLY uploaded report.

2. Never guess.

3. Never diagnose diseases.

4. Never prescribe medicines.

5. Explain abnormal findings.

6. Suggest questions the patient can ask a doctor.

7. Give only general lifestyle suggestions.

8. Mention when information is unavailable.

9. End with:

Please consult a qualified healthcare professional.
"""


def build_insights_prompt(context):

    return f"""

Medical Report

{context}

Generate:

1. Key Health Insights

2. High Priority Findings

3. Normal Findings

4. Medical Term Explanation

5. Questions to Ask Doctor

6. General Lifestyle Suggestions

7. Important Note

"""