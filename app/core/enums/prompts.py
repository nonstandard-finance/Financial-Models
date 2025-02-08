from enum import Enum, auto


class GenerationStyle(str, Enum):
    CONVERSATIONAL = "Conversational"
    SUMMARY = "Summary"
    SPEECH_READING = "Speech Reading"
    NARRATIVE = "Narrative"
    INTERVIEW = "Interview"


class Tone(str, Enum):
    INFORMATIVE = "Informative"
    HUMOROUS = "Humorous"
    SERIOUS = "Serious"
    ENTHUSIASTIC = "Enthusiastic"
    ACADEMIC = "Academic"
    CASUAL = "Casual"
    DRAMATIC = "Dramatic"


class SpeakerConfiguration(str, Enum):
    SINGLE_SPEAKER = "SINGLE_SPEAKER"
    TWO_SPEAKERS = "TWO_SPEAKERS"
    MULTIPLE_SPEAKERS = "MULTIPLE_SPEAKERS"


class PodcastGenre(Enum):
    TECH = "Tech"
    SCIENCE = "Science"
    BUSINESS = "Business"
    ENTERTAINMENT = "Entertainment"
    HISTORY = "History"
    CULTURE = "Culture"
    EDUCATION = "Education"
    SELF_IMPROVEMENT = "Self Improvement"
    TRUE_CRIME = "True Crime"
    NEWS = "News"


class TargetAudience(str, Enum):
    GENERAL_PUBLIC = "General Public"
    PROFESSIONALS = "Professionals"
    STUDENTS = "Students"
    EXPERTS = "Experts"
    YOUNG_ADULTS = "Young Adults"
    SENIORS = "Seniors"


class DetailedTone(str, Enum):
    # Informative Tones
    ACADEMIC_RIGOROUS = "Academic Rigorous"
    ACADEMIC_APPROACHABLE = "Academic Approachable"
    TECHNICAL_DEEP_DIVE = "Technical Deep Dive"
    JOURNALISTIC_OBJECTIVE = "Journalistic Objective"
    RESEARCH_FOCUSED = "Research Focused"

    # Emotional Tones
    INSPIRATIONAL = "Inspirational"
    MOTIVATIONAL = "Motivational"
    EMPATHETIC = "Empathetic"
    INTROSPECTIVE = "Introspective"
    NOSTALGIC = "Nostalgic"

    # Entertaining Tones
    SATIRICAL = "Satirical"
    SARCASTIC = "Sarcastic"
    PLAYFUL = "Playful"
    WITTY = "Witty"
    ABSURDIST = "Absurdist"

    # Professional Tones
    CORPORATE_PROFESSIONAL = "Corporate Professional"
    STARTUP_CASUAL = "Startup Casual"
    CONSULTING_ANALYTICAL = "Consulting Analytical"
    MENTORSHIP = "Mentorship"

    # Narrative Tones
    STORYTELLING = "Storytelling"
    DOCUMENTARY_STYLE = "Documentary Style"
    INVESTIGATIVE = "Investigative"
    PERSONAL_NARRATIVE = "Personal Narrative"
    HISTORICAL_NARRATIVE = "Historical Narrative"
