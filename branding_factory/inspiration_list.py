"""
Inspiration List — Content Creator Benchmarks
==============================================
Key influencers and thought leaders that Lior's content should learn from.
Organized by platform presence and content style.

Usage in Scout:
- Monitor their latest content for format inspiration
- Learn from their engagement patterns
- Adapt successful content frameworks to Lior's voice
"""

INSPIRATION_CREATORS = [
    {
        "name": "Alex Hormozi",
        "platforms": {
            "linkedin": True,
            "x": True,
            "instagram": True,
            "tiktok": True,
            "youtube": True,
        },
        "focus": "Business scaling, acquisition.com, direct & bold communication",
        "x_handle": "AlexHormozi",
        "linkedin_url": "https://www.linkedin.com/in/alexhormozi/",
    },
    {
        "name": "Steven Bartlett",
        "company": "The Diary of a CEO",
        "platforms": {
            "linkedin": True,
            "x": True,
            "instagram": True,
            "tiktok": True,
            "youtube": True,
        },
        "focus": "Entrepreneurship, podcasting, storytelling",
        "linkedin_url": "https://www.linkedin.com/in/stevenbartlett-123/",
    },
    {
        "name": "Justin Welsh",
        "tagline": "Helping 100,000+ experts turn their expertise into income",
        "platforms": {
            "linkedin": True,
            "x": True,
            "instagram": False,
            "tiktok": False,
            "youtube": False,
        },
        "focus": "Solopreneurship, content systems, LinkedIn authority",
    },
    {
        "name": "Dan Martell",
        "platforms": {
            "linkedin": True,
            "x": True,
            "instagram": True,
            "tiktok": True,
            "youtube": True,
        },
        "focus": "SaaS coaching, scaling, Buy Back Your Time",
    },
    {
        "name": "Gary Vaynerchuk",
        "platforms": {
            "linkedin": True,
            "x": True,
            "instagram": True,
            "tiktok": True,
            "youtube": True,
        },
        "focus": "Marketing, personal brand, hustle culture",
    },
    {
        "name": "Simon Beard",
        "platforms": {
            "linkedin": True,
            "x": False,
            "instagram": True,
            "tiktok": False,
            "youtube": True,
        },
        "focus": "Business insights, LinkedIn thought leadership",
    },
    {
        "name": "Iman Gadzhi",
        "company": "Co-owner of Whop",
        "platforms": {
            "linkedin": False,
            "x": True,
            "instagram": False,
            "tiktok": True,
            "youtube": True,
        },
        "focus": "Agency growth, digital products, young entrepreneur",
    },
    {
        "name": "Matt Gray",
        "company": "CEO, Founder OS",
        "platforms": {
            "linkedin": True,
            "x": True,
            "instagram": True,
            "tiktok": False,
            "youtube": True,
        },
        "focus": "Founder systems, productivity frameworks, LinkedIn content",
    },
    {
        "name": "Sabri Suby",
        "platforms": {
            "linkedin": False,
            "x": False,
            "instagram": True,
            "tiktok": False,
            "youtube": True,
        },
        "focus": "Marketing agency, direct response, sales",
    },
    {
        "name": "Dan Koe",
        "platforms": {
            "linkedin": True,
            "x": True,
            "instagram": False,
            "tiktok": False,
            "youtube": True,
        },
        "focus": "Creator economy, digital writing, philosophy",
    },
    {
        "name": "Guillermo Rauch",
        "company": "Vercel",
        "platforms": {
            "linkedin": True,
            "x": True,
            "instagram": False,
            "tiktok": False,
            "youtube": False,
        },
        "focus": "Pure tech, AI, UX, developer experience",
        "x_handle": "rauchg",
        "linkedin_url": "https://www.linkedin.com/in/rauchg/",
        "x_example": "https://x.com/rauchg/status/2024629864951927222",
    },
    {
        "name": "Alexandr Wang",
        "company": "Scale AI",
        "tagline": "Youngest AI billionaire",
        "platforms": {
            "linkedin": False,
            "x": True,
            "instagram": False,
            "tiktok": False,
            "youtube": False,
        },
        "focus": "AI infrastructure, enterprise AI, tech insights",
        "x_handle": "alexandr_wang",
    },
    {
        "name": "Nikita Bier",
        "company": "Head of Product at X",
        "platforms": {
            "linkedin": False,
            "x": True,
            "instagram": False,
            "tiktok": False,
            "youtube": False,
        },
        "focus": "Product design, viral mechanics, consumer apps",
        "x_handle": "nikitabier",
    },
    {
        "name": "Will Ahmed",
        "company": "Whoop",
        "tagline": "Talking about the product, great TikTok",
        "platforms": {
            "linkedin": True,
            "x": True,
            "instagram": True,
            "tiktok": True,
            "youtube": "Whoop podcast",
        },
        "focus": "Wearable tech, health optimization, product storytelling",
        "linkedin_url": "https://www.linkedin.com/in/willahmed/",
        "x_handle": "willahmed",
        "tiktok_url": "https://www.tiktok.com/@willahmed",
    },
    {
        "name": "Pieter Levels",
        "platforms": {
            "linkedin": False,
            "x": True,
            "instagram": False,
            "tiktok": False,
            "youtube": False,
        },
        "focus": "Indie hacker, build in public, nomad lifestyle, remote work",
        "x_handle": "levelsio",
    },
    {
        "name": "Tyler Denk",
        "company": "CEO @ beehiiv",
        "tagline": "Build in public",
        "platforms": {
            "linkedin": True,
            "x": False,
            "instagram": False,
            "tiktok": False,
            "youtube": False,
        },
        "focus": "Newsletter platform, build in public, SaaS growth",
        "linkedin_url": "https://www.linkedin.com/in/tyler-denk/recent-activity/all/",
    },
]


def get_x_inspiration_handles() -> list[str]:
    """Get all X/Twitter handles from inspiration list."""
    handles = []
    for creator in INSPIRATION_CREATORS:
        if creator["platforms"].get("x") and creator.get("x_handle"):
            handles.append(creator["x_handle"])
    return handles


def get_linkedin_inspiration_profiles() -> list[dict]:
    """Get LinkedIn-focused creators with their URLs."""
    profiles = []
    for creator in INSPIRATION_CREATORS:
        if creator["platforms"].get("linkedin"):
            profiles.append({
                "name": creator["name"],
                "url": creator.get("linkedin_url", ""),
                "focus": creator.get("focus", ""),
            })
    return profiles


def get_inspiration_by_platform(platform: str) -> list[dict]:
    """Get creators active on a specific platform."""
    return [
        {
            "name": c["name"],
            "focus": c.get("focus", ""),
            "company": c.get("company", ""),
            "handle": c.get(f"{platform}_handle", c.get("x_handle", "")),
        }
        for c in INSPIRATION_CREATORS
        if c["platforms"].get(platform.lower())
    ]


def get_inspiration_summary() -> str:
    """Get a formatted summary of all inspiration sources."""
    summary = "# Content Inspiration Sources\n\n"
    
    for creator in INSPIRATION_CREATORS:
        summary += f"## {creator['name']}"
        if creator.get("company"):
            summary += f" — {creator['company']}"
        summary += "\n"
        
        if creator.get("tagline"):
            summary += f"*{creator['tagline']}*\n"
        
        summary += f"**Focus:** {creator.get('focus', 'N/A')}\n"
        
        platforms = [p for p, active in creator["platforms"].items() if active]
        summary += f"**Platforms:** {', '.join(platforms)}\n\n"
    
    return summary


if __name__ == "__main__":
    print("📚 INSPIRATION LIST SUMMARY")
    print("=" * 60)
    
    print(f"\n✅ Total creators: {len(INSPIRATION_CREATORS)}")
    
    print("\n🐦 X/Twitter handles to monitor:")
    x_handles = get_x_inspiration_handles()
    for handle in x_handles:
        print(f"   @{handle}")
    
    print(f"\n💼 LinkedIn-focused creators: {len(get_inspiration_by_platform('linkedin'))}")
    print(f"📸 Instagram creators: {len(get_inspiration_by_platform('instagram'))}")
    print(f"🎵 TikTok creators: {len(get_inspiration_by_platform('tiktok'))}")
    print(f"📺 YouTube creators: {len(get_inspiration_by_platform('youtube'))}")
    
    print("\n" + "=" * 60)
    print("Use get_inspiration_summary() for full details")
