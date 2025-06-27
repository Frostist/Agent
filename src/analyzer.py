import os
import glob
import google.generativeai as genai

def get_two_latest_contents(content_type='market-analysis'):
    pattern = f"content/{content_type}/*.md"
    files = sorted(glob.glob(pattern), key=os.path.getctime, reverse=True)
    if len(files) < 1:
        return None, None
    def extract_main_content(filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()
        # Remove header (first two lines)
        return ''.join(lines[2:]).strip()
    latest_content = extract_main_content(files[0])
    prev_content = extract_main_content(files[1]) if len(files) > 1 else None
    return latest_content, prev_content

def gemini_is_important_update(new_content, prev_content):
    """
    Use Gemini to decide if the new content is important enough to save and continue the process.
    Returns True if important, False if not.
    """
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    prompt = f"""
    You are an expert crypto news editor. Compare the following two market analysis reports. The first is the most recent, the second is the previous one. 
    If the new report contains important new information, significant changes, or actionable insights that were not present in the previous report, respond ONLY with 'IMPORTANT'.
    If the new report is not meaningfully different, or does not add value, respond ONLY with 'NOT IMPORTANT'.
    
    ---
    NEW REPORT:
    {new_content}
    
    ---
    PREVIOUS REPORT:
    {prev_content if prev_content else '[No previous report]'}
    """
    try:
        response = model.generate_content(prompt)
        decision = response.text.strip().upper()
        return decision.startswith('IMPORTANT')
    except Exception as e:
        print(f"Error with Gemini importance check: {e}")
        # Fail safe: if Gemini fails, treat as important to avoid missing updates
        return True
