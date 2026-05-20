# Scout Refactoring Based on Reut's Feedback

## Changes Made

### 1. 🎯 Focus: AI in SaaS Only

**Before:** General AI news (consumer AI, research papers, etc.)

**After:** Filtered to:
- AI features in SaaS products
- AI-powered SaaS tools
- AI transforming SaaS companies
- News from: OpenAI, Anthropic, Google, Microsoft, Meta, AWS (SaaS-relevant)

**Filters out:** Consumer AI apps, general AI hype, academic research

---

### 2. 🐦 Top 5-7 X Posts with Highest Engagement

**New Function:** `_get_top_x_posts_about_ai_saas()`

**Criteria:**
- Topic: AI in SaaS specifically
- Timeframe: Last 24-48 hours
- Engagement: 1000+ total interactions (likes + retweets + replies)
- Sorted by: Highest engagement first

**Output Format:**
```
@username (15.2K engagement)
"Post text here..."
Why trending: Product Hunt launch of AI copilot for SaaS got massive traction
```

---

### 3. 📝 Output: 1 Sentence Per Trend

**Before:** Long paragraphs with multiple sections:
- What's Happening (2-3 sentences)
- The Friction (2-3 sentences)  
- Lior's Lens (2-3 sentences)
- Eye-Level Hook (1-2 sentences)
- Format Inspiration

**After:** Ultra-concise 1-sentence format:
```
1. [What's happening] + [Why SaaS companies should care]
2. [What's happening] + [Why SaaS companies should care]
3. [What's happening] + [Why SaaS companies should care]
```

**Rules:**
- Length: 20-30 words maximum per trend
- Must include: What + Why it matters for SaaS
- Must be actionable (not "AI is growing")
- Focus on business impact (revenue, retention, efficiency)

---

## Example Output

### Good Examples (Follow These):

1. "**Anthropic yesterday** released Claude with 200K context windows, letting SaaS companies build AI on entire customer histories instead of snippets."

2. "**Microsoft this week** announced $50/month Copilot pricing, proving customers will pay premium for AI features and changing SaaS pricing strategies."

3. "**OpenAI today** launched Realtime API, enabling SaaS companies to add voice AI to products in hours, not months."

### Format Requirements:

✅ **MUST include:**
- Company name at start (Anthropic, OpenAI, Microsoft, etc.)
- Timing word (yesterday, today, this week, recently)
- What happened
- Why SaaS companies should care

✅ **Length:** 25-35 words

### X Posts Format:

```
@rauchg · 3 hours ago · (18.5K engagement)
"Vercel just shipped AI SDK 4.0 with streaming..."
Why trending: Major framework update for AI in SaaS
```

### Bad Examples (Avoid):

❌ No company name: "AI is transforming how we work."
❌ No timing: "OpenAI's new API helps SaaS companies."
❌ Too vague: "SaaS companies are adopting AI at record pace."
❌ No business impact: "New AI model released."

---

## Technical Changes

### File: `branding_factory/agents/scout.py`

**New Function:**
```python
def _get_top_x_posts_about_ai_saas() -> str:
    """Use Grok to get the top 5-7 X posts about AI in SaaS with highest engagement."""
```

**Modified Sections:**
- Phase 2: Changed from "X Account Monitoring" to "Top X Posts About AI in SaaS"
- Phase 3: Changed from "Final Brief Generation" to "Generate Concise Trend Summary"
- Final prompt: Completely rewritten to output 3 one-sentence trends

**Filtering:**
```python
# Filter for AI in SaaS news only
ai_saas_news = [item for item in all_sources if any(
    keyword in item.get('title', '').lower() or keyword in item.get('source', '').lower()
    for keyword in ['ai', 'openai', 'anthropic', 'microsoft', 'google', 'saas']
)]
```

---

## Results

✅ Scout now focuses on **AI in SaaS**
✅ Gets **top 5-7 X posts** with highest engagement
✅ Outputs **3 one-sentence trends** (not paragraphs)
✅ Trends are **actionable** and **business-focused**
✅ Faster to read and understand

---

## Testing

Run the app and check:
1. Scout phase shows "Finding top X posts about AI in SaaS"
2. Final output is 3 numbered sentences (not long paragraphs)
3. Each sentence is 20-30 words
4. Trends are about AI in SaaS (not general AI)

Command:
```bash
python app.py
```

Expected output in Scout section:
```
1. [Concise 1-sentence trend about AI in SaaS]
2. [Concise 1-sentence trend about AI in SaaS]
3. [Concise 1-sentence trend about AI in SaaS]
```
