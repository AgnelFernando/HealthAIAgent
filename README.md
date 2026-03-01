# HealthAIAgent
A wearable-integrated, RAG-grounded, agentic AI that analyzes sleep, activity, and risk signals and produces personalized recommendations + action workflows.

## Demo Questions 
- How many hours of sleep are recommended for newborns and infants?
- How many hours of sleep should adults get per day for optimal health?
- What are the health risks associated with insufficient sleep among children and adolescents?
- Why is good sleep important for heart health?
- Is short sleep duration associated with obesity, diabetes, or cardiovascular disease in adults?
- What is sleep hygiene, and how can it improve sleep quality?
- What is Shift Work Sleep Disorder (SWSD), and who is at risk?
- How can night shift work affect reproductive or overall health?
- How does sleep duration and consistency affect academic performance in adolescents or college students?
- What are the recommended physical activity guidelines for adults and children?


## Example RAG Query & Response
### Question: How many hours of sleep should adults get?

```json
{
        "answer": "Most adults need at least 7 hours of sleep each night (About Sleep and Your Heart Health).",
        "citations": [
            {
                "title": "About Sleep",
                "url": "https://www.cdc.gov/sleep/about/",
                "similarity": 0.605054056945685
            },
            {
                "title": "About Sleep and Your Heart Health",
                "url": "https://www.cdc.gov/heart-disease/about/sleep-and-heart-health.html",
                "similarity": 0.588620918650059
            },
            {
                "title": "Sleep and Health",
                "url": "https://www.cdc.gov/physical-activity-education/staying-healthy/sleep.html",
                "similarity": 0.585545438097282
            },
            {
                "title": "Sleep Duration as a Correlate of Smoking, Alcohol Use, Leisure-Time Physical Inactivity, and Obesity Among Adults: United States, 2004-2006",
                "url": "https://www.cdc.gov/nchs/data/hestat/sleep04-06/sleep04-06.htm",
                "similarity": 0.542281849912352
            },
            {
                "title": "Sleep Duration as a Correlate of Smoking, Alcohol Use, Leisure-Time Physical Inactivity, and Obesity Among Adults: United States, 2004-2006",
                "url": "https://www.cdc.gov/nchs/data/hestat/sleep04-06/sleep04-06.htm",
                "similarity": 0.53486032887877
            }
        ],
        "confidence": 0.571
    }
```
