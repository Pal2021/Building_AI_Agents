from IPython.display import Markdown, display
from call_llm import callingLLM
from scraper import fetch_website_contents
from IPython.display import Markdown, display, update_display
# ======================
# Setup
# ======================
client = callingLLM()
deployment_name = "gpt-5"

url = "https://myportfolio1-wine.vercel.app/"
company_name = "PwC India"

# ======================
# Fetch Content
# ======================
content = fetch_website_contents(url)
content = content[:18000]

# ======================
# Prompt
# ======================
prompt = f"""
You are an expert marketing copywriter and business consultant specializing in creating professional company brochures.

Your task is to create a high-quality, persuasive brochure for the company based on the information available from their official website.

**Company Name:** {company_name}
**Website:** {url}

**Website Content:**
{content}

The brochure should be suitable for three key audiences:
1. Prospective Clients
2. Investors
3. Potential Recruits (job seekers)

### Brochure Structure:

1. **Cover Section**
   - Company Name
   - Tagline / One-line positioning statement
   - Short powerful introduction

2. **About the Company**
   - Brief history and background
   - Mission, Vision, and Core Values

3. **Products / Services**
   - Key offerings explained clearly
   - Unique value proposition

4. **Why Choose Us** (For Clients)
   - Key benefits and differentiators
   - Social proof

5. **Investment Opportunity** (For Investors)
   - Market potential
   - Growth highlights
   - Competitive advantage

6. **Career & Culture** (For Potential Recruits)
   - Work culture and values
   - Why join this company
   - Growth opportunities

7. **Key Achievements / Milestones**
   - Important numbers, awards, recognitions

8. **Contact & Call to Action**
   - Website and contact information
   - Strong closing statement

### Guidelines:
- Keep the tone professional, confident, and engaging.
- Use clear and persuasive language.
- Make it concise but impactful (suitable for a 2-4 page brochure).
- Do not invent false information.
- Format the output using clean Markdown with clear headings and bullet points.

Now generate the complete brochure content.
"""

# ======================
# Streaming Function
# ======================
def stream_brochure(prompt):
    stream = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "user", "content": prompt}
          ],
        stream=True
    )    
    response = ""
    display_handle = display(Markdown(""), display_id=True)
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        update_display(Markdown(response), display_id=display_handle.display_id)
    stream = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=True
    )


    
# Run
# ======================
print("Generating brochure...\n")
brochure_content = stream_brochure(prompt)

print("\n\n✅ Brochure generation completed!")