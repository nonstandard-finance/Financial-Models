from enum import Enum, auto


class ContentType(Enum):
    """
    Enumerate different types of content a user can submit
    """

    LINK = "Link"
    PDF = "PDF Document"
    DOCX = "Word Document"
    TXT = "Text File"
    WEBPAGE = "Web Page"
    YOUTUBE_TRANSCRIPT = "YouTube Transcript"
    BOOK_CHAPTER = "Book Chapter"
    BOOK_PAGE = "Book Page"


class ResearchStatus(Enum):
    PENDING = "PENDING"
    RESEARCHING = "RESEARCHING"
    GENERATING_OUTLINE = "GENERATING_OUTLINE"
    WRITING_DRAFT = "WRITING_DRAFT"
    FINALIZING = "FINALIZING"
    GENERATING_AUDIO = "GENERATING_AUDIO"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
