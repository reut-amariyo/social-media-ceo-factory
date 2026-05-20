# UI Enhancement: Scout → Ideator Connection

## What Was Changed

Added visibility into the Scout-to-Ideator connection in the desktop app UI.

## New UI Components

### 1. Scout Insights Section (Collapsible)
```
┌────────────────────────────────────────────────────────────┐
│ ▶ 🔍 Scout Trend Report — See What's Trending Right Now   │
└────────────────────────────────────────────────────────────┘

When expanded (click to toggle):

┌────────────────────────────────────────────────────────────┐
│ ▼ 🔍 Scout Trend Report — See What's Trending Right Now   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  TREND #1: AI Agents Replace Middle Management            │
│  What's Happening: OpenAI's new Operator agent...         │
│  The Friction: People debating if this kills jobs...      │
│  Lior's Lens: When I scaled AutoDS from 10 to 150...     │
│  Eye-Level Hook: Your team doesn't need more...          │
│                                                            │
│  TREND #2: ...                                            │
│  TREND #3: ...                                            │
│                                                            │
│  💡 Connection: The ideas below were generated from       │
│  these trends. See how the Ideator connected them to      │
│  Lior's experience.                                       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 2. Enhanced Idea Cards with Scout Badge
```
┌────────────────────────────────────────────────────────────┐
│ 💡 Idea 1  [🔍 From Scout]                                │
│                                                            │
│ IDEA: Why I replaced 3 VPs with AI agents                 │
│ ARCHETYPE: Personal Confession                            │
│ HOOK: "I just fired my Head of Operations. Not for...    │
│ ANGLE: Connect AI automation trend to AutoDS scaling...   │
│ TARGET: Entrepreneurs                                      │
│                                                            │
│                            [✏️ Edit This]  [🚀 Use This] │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│ 💡 Idea 2  [🔍 From Scout]                                │
│ ...                                                        │
└────────────────────────────────────────────────────────────┘
```

## User Experience Flow

**Before:** (Hidden process)
```
Scout runs → ??? → Ideas appear
```

**After:** (Transparent process)
```
Scout runs → [View Trends] → Ideas appear [From Scout badges]
                ↓
          "Ideas generated from these trends"
```

## Benefits

1. **Transparency**: Users see exactly what trends were found
2. **Learning**: Users understand how Scout → Ideator works
3. **Trust**: Clear connection between input (trends) and output (ideas)
4. **Debugging**: If ideas seem off, check the scout report
5. **Inspiration**: Users can read trends directly for additional context

## Files Modified

- `app.py` - Added `_create_scout_insights_section()` method
- `app.py` - Enhanced `_create_idea_card()` with "From Scout" badge
- `app.py` - Added collapsible UI component with toggle

## Testing

Run the app and:
1. Click "Start Factory"
2. Wait for Scout + Ideator to complete
3. On idea selection screen:
   - See collapsible Scout section at top
   - Click to expand/view trends
   - See "From Scout" badges on idea cards
   - Read connection note

## Color Scheme

- Scout section: Dark card background with accent border
- "From Scout" badge: Subtle gray badge
- Connection note: Warning color (yellow) for emphasis
- Collapsible: Accent color arrow (▶/▼)
