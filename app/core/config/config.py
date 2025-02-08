"""
Utilities for text processing and formatting in podcast generation.

This module provides utilities for working with text content in podcast scripts
and outlines. It handles formatting and conversion of podcast content into
different text representations.

Key components:
- generate_markdown_script: Converts podcast outline and script into markdown format
  for easy viewing and sharing

The module helps with:
- Converting internal podcast data structures to human-readable formats
- Generating documentation and review materials from podcast content
- Maintaining consistent text formatting across the application
"""


# from dataclasses import dataclass
# from pathlib import Path
# from typing import Optional, Dict, Any, List
# import json
# import os
# from dotenv import load_dotenv
# import yaml

# from app.core.enums.prompts import (
#     PodcastGenre,
#     TargetAudience,
#     DetailedTone,
#     GenerationStyle,
#     Tone,
#     SpeakerConfiguration,
# )

# from app.core.constants import (
#     GOOGLE_GEMINI_KEY,
#     OPENAI_API_KEY,
#     TAVILY_API_KEY,
#     ELEVENLABS_API_KEY,
# )


# @dataclass
# class SpeakerPersona:
#     name: str
#     background: str
#     speaking_style: str
#     expertise: Optional[List[str]] = None

#     def to_dict(self) -> Dict[str, Any]:
#         return {
#             "name": self.name,
#             "background": self.background,
#             "speaking_style": self.speaking_style,
#             "expertise": self.expertise or [],
#         }


# @dataclass
# class PodcastSection:
#     title: str
#     subsections: List[str]

#     def as_markdown(self) -> str:
#         markdown = f"### {self.title}\n"
#         for subsection in self.subsections:
#             markdown += f"- {subsection}\n"
#         return markdown


# @dataclass
# class PodcastOutline:
#     sections: List[PodcastSection]

#     def as_markdown(self) -> str:
#         return "\n".join(section.as_markdown() for section in self.sections)


# class PodcastConfig:
#     """
#     Configuration manager for podcast generation.

#     Handles all aspects of podcast configuration including:
#     - Generation styles and tones
#     - Speaker profiles and personas
#     - API integrations (TTS, LLM)
#     - Output formats and paths
#     - Episode structure and templates

#     Supports both basic and premium features with appropriate defaults.
#     Can be initialized directly or loaded from environment variables and YAML.

#     Attributes:
#         generation_style (GenerationStyle): Style of podcast generation
#         tone (Optional[DetailedTone]): Detailed tone for premium users
#         basic_tone (Optional[Tone]): Basic tone for standard users
#         speakers (SpeakerConfiguration): Speaker configuration
#         genre (PodcastGenre): Podcast genre
#         target_audience (TargetAudience): Target audience
#         custom_personas (Optional[List[SpeakerPersona]]): Custom speaker profiles
#         is_premium (bool): Premium user status
#         custom_voice_mapping (Optional[Dict[str, str]]): Custom voice mappings for ElevenLabs
#     """

#     def __init__(
#         self,
#         # Core podcast settings
#         generation_style: GenerationStyle = GenerationStyle.CONVERSATIONAL,
#         tone: Optional[DetailedTone] = None,
#         basic_tone: Optional[Tone] = None,
#         speakers: SpeakerConfiguration = SpeakerConfiguration.TWO_SPEAKERS,
#         genre: PodcastGenre = PodcastGenre.EDUCATION,
#         target_audience: TargetAudience = TargetAudience.GENERAL_PUBLIC,
#         custom_personas: Optional[List[SpeakerPersona]] = None,
#         is_premium: bool = False,
#         # API Keys
#         google_api_key: str = GOOGLE_GEMINI_KEY,
#         elevenlabs_api_key: str = ELEVENLABS_API_KEY,
#         openai_api_key: str = OPENAI_API_KEY,
#         tavily_api_key: str = TAVILY_API_KEY,
#         anthropic_api_key: str = "",
#         # LLM Settings
#         fast_llm_provider: str = "openai",
#         long_context_llm_provider: str = "openai",
#         embeddings_model: str = "openai",
#         # TTS Settings
#         tts_provider: str = "elevenlabs",
#         tts_settings: Optional[Dict] = None,
#         custom_voice_mapping: Optional[Dict[str, str]] = None,  # Custom voice mappings
#         # Output Settings
#         output_format: str = "mp3",
#         temp_audio_dir: str = "temp_audio",
#         output_dir: str = "./output",
#         checkpoint_dir: str = "./.checkpoints",
#         # Rate Limits
#         rate_limits: Optional[Dict] = None,
#         # Episode Structure
#         podcast_name: str = "AI podcast",
#         intro: str = "Welcome to {podcast_name}. Today we're discussing {topic}.",
#         outro: str = "Thanks for listening to {podcast_name}.",
#         episode_structure: Optional[List[str]] = None,
#     ):
#         # Core settings
#         self.generation_style = generation_style
#         self.speakers = speakers
#         self.genre = genre
#         self.target_audience = target_audience
#         self.is_premium = is_premium
#         self.tone = tone if is_premium else None
#         self.basic_tone = None if is_premium else (basic_tone or Tone.INFORMATIVE)
#         self.personas = custom_personas or self._generate_default_personas()

#         # API keys
#         self.google_api_key = google_api_key
#         self.elevenlabs_api_key = elevenlabs_api_key
#         self.openai_api_key = openai_api_key
#         self.tavily_api_key = tavily_api_key
#         self.anthropic_api_key = anthropic_api_key

#         # LLM settings
#         self.fast_llm_provider = fast_llm_provider
#         self.long_context_llm_provider = long_context_llm_provider
#         self.embeddings_model = embeddings_model

#         # TTS settings
#         self.tts_provider = tts_provider
#         self.tts_settings = tts_settings or self._default_tts_settings(
#             custom_voice_mapping
#         )

#         # Output settings
#         self.output_format = output_format
#         self.temp_audio_dir = temp_audio_dir
#         self.output_dir = output_dir
#         self.checkpoint_dir = checkpoint_dir

#         # Rate limits
#         self.rate_limits = rate_limits or self._default_rate_limits()

#         # Episode structure
#         self.podcast_name = podcast_name
#         self.intro = intro
#         self.outro = outro
#         self.episode_structure = episode_structure or [
#             "Episode Introduction",
#             "Main Discussion Topics",
#             "Conclusion",
#         ]

#         # Ensure the directory exists
#         Path(self.temp_audio_dir).mkdir(parents=True, exist_ok=True)

#         self._initialize_templates()

#     @classmethod
#     def load(cls, yaml_path: Optional[str] = None) -> "PodcastConfig":
#         """
#         Load configuration from environment variables and optional YAML file.
#         """
#         load_dotenv()

#         required_env_vars = [
#             "GOOGLE_API_KEY",
#             "ELEVENLABS_API_KEY",
#             "OPENAI_API_KEY",
#             "TAVILY_API_KEY",
#             "ANTHROPIC_API_KEY",
#         ]

#         config_dict = {}
#         for var in required_env_vars:
#             value = os.getenv(var)
#             if not value:
#                 raise ValueError(f"Missing required environment variable: {var}")
#             config_dict[var.lower()] = value

#         if yaml_path:
#             with open(yaml_path) as f:
#                 yaml_config = yaml.safe_load(f)
#                 config_dict.update(yaml_config)

#         return cls(**config_dict)

#     def _default_tts_settings(
#         self, custom_voice_mapping: Optional[Dict[str, str]] = None
#     ) -> Dict:
#         """
#         Generate default TTS settings with optional custom voice mappings.
#         """
#         # Default voice mappings
#         default_voice_mapping = {"Interviewer": "Chris", "Interviewee": "Charlie"}

#         # Use custom voice mappings if provided, otherwise use default
#         voice_mapping = (
#             custom_voice_mapping if custom_voice_mapping else default_voice_mapping
#         )

#         return {
#             "elevenlabs": {
#                 "voice_mapping": voice_mapping,
#                 "model": "eleven_multilingual_v2",
#             },
#             "google": {
#                 "voice_mapping": {
#                     "Interviewer": "en-US-Journey-F",
#                     "Interviewee": "en-US-Journey-D",
#                 },
#                 "language_code": "en-US",
#                 "effects_profile_id": "small-bluetooth-speaker-class-device",
#             },
#         }

#     def _default_rate_limits(self) -> Dict:
#         """
#         Default rate limits for API providers.
#         """
#         return {
#             "elevenlabs": {
#                 "requests_per_minute": 20,
#                 "max_retries": 10,
#                 "base_delay": 2.0,
#             },
#             "google": {"requests_per_minute": 20, "max_retries": 10, "base_delay": 2.0},
#         }

#     def _generate_default_personas(self) -> List[SpeakerPersona]:
#         """
#         Generate default speaker personas based on the podcast genre.
#         """
#         templates = {
#             PodcastGenre.TECH: [
#                 SpeakerPersona(
#                     name="Alex Tech",
#                     background="Tech journalist",
#                     speaking_style="Enthusiastic tech analysis",
#                     expertise=["AI", "Startups"],
#                 )
#             ],
#             PodcastGenre.SCIENCE: [
#                 SpeakerPersona(
#                     name="Dr. Nathan Cosmos",
#                     background="Astrophysicist",
#                     speaking_style="Educational",
#                     expertise=["Physics", "Space"],
#                 )
#             ],
#         }
#         return templates.get(
#             self.genre,
#             [
#                 SpeakerPersona(
#                     name="Host",
#                     background="Podcast host",
#                     speaking_style="Conversational",
#                     expertise=["Communication"],
#                 )
#             ],
#         )

#     def _initialize_templates(self):
#         """
#         Initialize templates for different generation styles.
#         """
#         self._style_templates = {
#             GenerationStyle.CONVERSATIONAL: self._create_template("conversational"),
#             GenerationStyle.SUMMARY: self._create_template("summary"),
#             GenerationStyle.SPEECH_READING: self._create_template("speech_reading"),
#             GenerationStyle.NARRATIVE: self._create_template("narrative"),
#             GenerationStyle.INTERVIEW: self._create_template("interview"),
#         }

#     def _create_template(self, style: str) -> str:
#         """
#         Create a template for the given generation style.
#         """
#         base = f"""
#         Generate a {style} podcast script with the following parameters:
#         - Genre: {self.genre.value}
#         - Target Audience: {self.target_audience.value}
#         - Speakers: {self.speakers.value}
#         - Structure: {self.episode_structure_for_prompt}

#         Intro Template: {self.intro}
#         Outro Template: {self.outro}
#         """
#         if self.is_premium:
#             base += f"\nTone: {self.tone.value if self.tone else 'Default'}"
#             base += f"\nVoices: {self.tts_settings[self.tts_provider]['voice_mapping']}"
#         else:
#             base += f"\nTone: {self.basic_tone.value if self.basic_tone else 'Default'}"
#         return base.strip()

#     def generate_script(self, topic: str, outline: PodcastOutline) -> str:
#         """
#         Generate a podcast script in markdown format.
#         """
#         template = self._style_templates[self.generation_style]
#         markdown = f"# {topic}\n\n## Outline\n\n{outline.as_markdown()}\n\n"
#         return markdown

#     @property
#     def episode_structure_for_prompt(self) -> str:
#         """
#         Format episode structure for use in prompts.
#         """
#         return "\n".join([f"- {section}" for section in self.episode_structure])

#     def to_json(self) -> str:
#         """
#         Serialize the configuration to JSON.
#         """
#         config_dict = {
#             "generation_style": self.generation_style.value,
#             "speakers": self.speakers.value,
#             "genre": self.genre.value,
#             "target_audience": self.target_audience.value,
#             "is_premium": self.is_premium,
#             "tts_provider": self.tts_provider,
#             "output_format": self.output_format,
#             "podcast_name": self.podcast_name,
#             "personas": [persona.to_dict() for persona in self.personas],
#         }
#         if self.is_premium and self.tone:
#             config_dict["tone"] = self.tone.value
#         elif not self.is_premium and self.basic_tone:
#             config_dict["basic_tone"] = self.basic_tone.value
#         return json.dumps(config_dict, indent=2)


from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, List
import json
import os
from dotenv import load_dotenv
import yaml

from app.core.enums.prompts import (
    PodcastGenre,
    TargetAudience,
    DetailedTone,
    GenerationStyle,
    Tone,
    SpeakerConfiguration,
)

from app.core.constants import (
    GOOGLE_GEMINI_KEY,
    OPENAI_API_KEY,
    TAVILY_API_KEY,
    ELEVENLABS_API_KEY,
)


@dataclass
class SpeakerPersona:
    name: str
    background: str
    speaking_style: str
    expertise: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "background": self.background,
            "speaking_style": self.speaking_style,
            "expertise": self.expertise or [],
        }


@dataclass
class PodcastSection:
    title: str
    subsections: List[str]

    def as_markdown(self) -> str:
        markdown = f"### {self.title}\n"
        for subsection in self.subsections:
            markdown += f"- {subsection}\n"
        return markdown


@dataclass
class PodcastOutline:
    sections: List[PodcastSection]

    def as_markdown(self) -> str:
        return "\n".join(section.as_markdown() for section in self.sections)


class PodcastConfig:
    """
    Configuration manager for podcast generation.

    Handles all aspects of podcast configuration including:
    - Generation styles and tones
    - Speaker profiles and personas
    - API integrations (TTS, LLM)
    - Output formats and paths
    - Episode structure and templates

    Supports both basic and premium features with appropriate defaults.
    Can be initialized directly or loaded from environment variables and YAML.

    Attributes:
        generation_style (GenerationStyle): Style of podcast generation
        tone (Optional[DetailedTone]): Detailed tone for premium users
        basic_tone (Optional[Tone]): Basic tone for standard users
        speakers (SpeakerConfiguration): Speaker configuration
        genre (PodcastGenre): Podcast genre
        target_audience (TargetAudience): Target audience
        custom_personas (Optional[List[SpeakerPersona]]): Custom speaker profiles
        is_premium (bool): Premium user status
        custom_voice_mapping (Optional[Dict[str, str]]): Custom voice mappings for ElevenLabs
    """

    def __init__(
        self,
        # Core podcast settings
        generation_style: GenerationStyle = GenerationStyle.CONVERSATIONAL,
        tone: Optional[DetailedTone] = None,
        basic_tone: Optional[Tone] = None,
        speakers: SpeakerConfiguration = SpeakerConfiguration.TWO_SPEAKERS,
        genre: PodcastGenre = PodcastGenre.EDUCATION,
        target_audience: TargetAudience = TargetAudience.GENERAL_PUBLIC,
        custom_personas: Optional[List[SpeakerPersona]] = None,
        is_premium: bool = False,
        # API Keys
        google_api_key: str = GOOGLE_GEMINI_KEY,
        elevenlabs_api_key: str = ELEVENLABS_API_KEY,
        openai_api_key: str = OPENAI_API_KEY,
        tavily_api_key: str = TAVILY_API_KEY,
        anthropic_api_key: str = "",
        # LLM Settings
        fast_llm_provider: str = "openai",
        long_context_llm_provider: str = "openai",
        embeddings_model: str = "openai",
        # TTS Settings
        tts_provider: str = "elevenlabs",
        tts_settings: Optional[Dict] = None,
        custom_voice_mapping: Optional[Dict[str, str]] = None,  # Custom voice mappings
        # Output Settings
        output_format: str = "mp3",
        temp_audio_dir: str = "temp_audio",
        output_dir: str = "./output",
        checkpoint_dir: str = "./.checkpoints",
        # Rate Limits
        rate_limits: Optional[Dict] = None,
        # Episode Structure
        podcast_name: str = "AI podcast",
        intro: str = "Welcome to {podcast_name}. Today we're discussing {topic}.",
        outro: str = "Thanks for listening to {podcast_name}.",
        episode_structure: Optional[List[str]] = None,
    ):
        # Core settings
        self.generation_style = generation_style
        self.speakers = speakers
        self.genre = genre
        self.target_audience = target_audience
        self.is_premium = is_premium
        self.tone = tone if is_premium else None
        self.basic_tone = None if is_premium else (basic_tone or Tone.INFORMATIVE)
        self.personas = custom_personas or self._generate_default_personas()

        # API keys
        self.google_api_key = google_api_key
        self.elevenlabs_api_key = elevenlabs_api_key
        self.openai_api_key = openai_api_key
        self.tavily_api_key = tavily_api_key
        self.anthropic_api_key = anthropic_api_key

        # LLM settings
        self.fast_llm_provider = fast_llm_provider
        self.long_context_llm_provider = long_context_llm_provider
        self.embeddings_model = embeddings_model

        # TTS settings
        self.tts_provider = tts_provider
        self.tts_settings = tts_settings or self._default_tts_settings(
            custom_voice_mapping
        )

        # Output settings
        self.output_format = output_format
        self.temp_audio_dir = temp_audio_dir
        self.output_dir = output_dir
        self.checkpoint_dir = checkpoint_dir

        # Rate limits
        self.rate_limits = rate_limits or self._default_rate_limits()

        # Episode structure
        self.podcast_name = podcast_name
        self.intro = intro
        self.outro = outro
        self.episode_structure = episode_structure or [
            "Episode Introduction",
            "Main Discussion Topics",
            "Conclusion",
        ]

        # Ensure the directory exists
        Path(self.temp_audio_dir).mkdir(parents=True, exist_ok=True)

        self._initialize_templates()

    @classmethod
    def load(cls, yaml_path: Optional[str] = None) -> "PodcastConfig":
        """
        Load configuration from environment variables and optional YAML file.
        """
        load_dotenv()

        required_env_vars = [
            "GOOGLE_API_KEY",
            "ELEVENLABS_API_KEY",
            "OPENAI_API_KEY",
            "TAVILY_API_KEY",
            "ANTHROPIC_API_KEY",
        ]

        config_dict = {}
        for var in required_env_vars:
            value = os.getenv(var)
            if not value:
                raise ValueError(f"Missing required environment variable: {var}")
            config_dict[var.lower()] = value

        if yaml_path:
            with open(yaml_path) as f:
                yaml_config = yaml.safe_load(f)
                config_dict.update(yaml_config)

        return cls(**config_dict)

    def _default_tts_settings(
        self, custom_voice_mapping: Optional[Dict[str, str]] = None
    ) -> Dict:
        """
        Generate default TTS settings with optional custom voice mappings.
        """
        # Default voice mappings
        default_voice_mapping = {"Interviewer": "Chris", "Interviewee": "Charlie"}

        # Use custom voice mappings if provided, otherwise use default
        voice_mapping = (
            custom_voice_mapping if custom_voice_mapping else default_voice_mapping
        )

        return {
            "elevenlabs": {
                "voice_mapping": voice_mapping,
                "model": "eleven_multilingual_v2",
            },
            "google": {
                "voice_mapping": {
                    "Interviewer": "en-US-Journey-F",
                    "Interviewee": "en-US-Journey-D",
                },
                "language_code": "en-US",
                "effects_profile_id": "small-bluetooth-speaker-class-device",
            },
        }

    def _default_rate_limits(self) -> Dict:
        """
        Default rate limits for API providers.
        """
        return {
            "elevenlabs": {
                "requests_per_minute": 20,
                "max_retries": 10,
                "base_delay": 2.0,
            },
            "google": {"requests_per_minute": 20, "max_retries": 10, "base_delay": 2.0},
        }

    def _generate_default_personas(self) -> List[SpeakerPersona]:
        """
        Generate default speaker personas based on the podcast genre.
        """
        templates = {
            PodcastGenre.TECH: [
                SpeakerPersona(
                    name="Alex Tech",
                    background="Tech journalist",
                    speaking_style="Enthusiastic tech analysis",
                    expertise=["AI", "Startups"],
                )
            ],
            PodcastGenre.SCIENCE: [
                SpeakerPersona(
                    name="Dr. Nathan Cosmos",
                    background="Astrophysicist",
                    speaking_style="Educational",
                    expertise=["Physics", "Space"],
                )
            ],
        }
        return templates.get(
            self.genre,
            [
                SpeakerPersona(
                    name="Host",
                    background="Podcast host",
                    speaking_style="Conversational",
                    expertise=["Communication"],
                )
            ],
        )

    def _initialize_templates(self):
        """
        Initialize templates for different generation styles.
        """
        self._style_templates = {
            GenerationStyle.CONVERSATIONAL: self._create_template("conversational"),
            GenerationStyle.SUMMARY: self._create_template("summary"),
            GenerationStyle.SPEECH_READING: self._create_template("speech_reading"),
            GenerationStyle.NARRATIVE: self._create_template("narrative"),
            GenerationStyle.INTERVIEW: self._create_template("interview"),
        }

    def _create_template(self, style: str) -> str:
        """
        Create a template for the given generation style.
        """
        base = f"""
        Generate a {style} podcast script with the following parameters:
        - Genre: {self.genre.value}
        - Target Audience: {self.target_audience.value}
        - Speakers: {self.speakers.value}
        - Structure: {self.episode_structure_for_prompt}

        Intro Template: {self.intro}
        Outro Template: {self.outro}
        """
        if self.is_premium:
            base += f"\nTone: {self.tone.value if self.tone else 'Default'}"
            base += f"\nVoices: {self.tts_settings[self.tts_provider]['voice_mapping']}"
        else:
            base += f"\nTone: {self.basic_tone.value if self.basic_tone else 'Default'}"
        return base.strip()

    def generate_script(self, topic: str, outline: PodcastOutline) -> str:
        """
        Generate a podcast script in markdown format.
        """
        template = self._style_templates[self.generation_style]
        markdown = f"# {topic}\n\n## Outline\n\n{outline.as_markdown()}\n\n"
        return markdown

    @property
    def episode_structure_for_prompt(self) -> str:
        """
        Format episode structure for use in prompts.
        """
        return "\n".join([f"- {section}" for section in self.episode_structure])

    def to_json(self) -> str:
        """
        Serialize the configuration to JSON.
        """
        config_dict = {
            "generation_style": self.generation_style.value,
            "speakers": self.speakers.value,
            "genre": self.genre.value,
            "target_audience": self.target_audience.value,
            "is_premium": self.is_premium,
            "tts_provider": self.tts_provider,
            "output_format": self.output_format,
            "podcast_name": self.podcast_name,
            "personas": [persona.to_dict() for persona in self.personas],
        }
        if self.is_premium and self.tone:
            config_dict["tone"] = self.tone.value
        elif not self.is_premium and self.basic_tone:
            config_dict["basic_tone"] = self.basic_tone.value
        return json.dumps(config_dict, indent=2)
