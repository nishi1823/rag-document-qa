import re


def generate_answer(question, retrieved_chunks):
    """
    Generate an answer using only retrieved document context.
    """

    if not retrieved_chunks:
        return "I could not find relevant information in the uploaded document."

    context = "\n\n".join(
        item["text"]
        for item in retrieved_chunks
    )

    question_lower = question.lower().strip()

    # =========================================================
    # IDENTITY / NAME
    # =========================================================

    identity_words = [
        "whose document",
        "whos document",
        "whose resume",
        "who is this document",
        "who is this resume",
        "who does this document belong to",
        "who does this resume belong to"
    ]

    if any(x in question_lower for x in identity_words):

        # Look for a name before phone/email
        pattern = re.search(
            r"([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){1,4})"
            r"\s+(?=\+?\d|[\w\.-]+@)",
            context[:3000]
        )

        if pattern:
            return f"The document belongs to **{pattern.group(1).strip()}**."

    # =========================================================
    # GITHUB
    # =========================================================

    if "github" in question_lower:

        github_links = re.findall(
            r"https?://(?:www\.)?github\.com/[^\s\]\)>]+",
            context,
            re.IGNORECASE
        )

        if github_links:
            return f"The GitHub profile is: {github_links[0]}"

        github_username = re.search(
            r"github\.com/([A-Za-z0-9_-]+)",
            context,
            re.IGNORECASE
        )

        if github_username:
            return (
                "The GitHub profile is: "
                f"https://github.com/{github_username.group(1)}"
            )

        return "I could not find a GitHub profile in the retrieved document."

    # =========================================================
    # LINKEDIN
    # =========================================================

    if "linkedin" in question_lower:

        linkedin_links = re.findall(
            r"https?://(?:www\.)?linkedin\.com/[^\s\]\)>]+",
            context,
            re.IGNORECASE
        )

        if linkedin_links:
            return f"The LinkedIn profile is: {linkedin_links[0]}"

        return "I could not find a LinkedIn profile in the retrieved document."

    # =========================================================
    # EMAIL
    # =========================================================

    if "email" in question_lower or "mail id" in question_lower:

        emails = re.findall(
            r"[\w\.-]+@[\w\.-]+\.\w+",
            context
        )

        if emails:
            return f"The email address is: {emails[0]}"

        return "I could not find an email address in the retrieved document."

    # =========================================================
    # PHONE / MOBILE
    # =========================================================

    if any(
        word in question_lower
        for word in ["phone", "mobile", "contact number", "phone number"]
    ):

        numbers = re.findall(
            r"(?:\+91[\s-]?)?[6-9]\d{9}",
            context
        )

        if numbers:
            return f"The contact number is: {numbers[0]}"

        return "I could not find a phone number in the retrieved document."

    # =========================================================
    # GENERAL QUESTION ANSWERING
    # =========================================================

    stop_words = {
        "who", "what", "where", "when", "why", "how",
        "is", "are", "was", "were",
        "the", "a", "an",
        "this", "that", "these", "those",
        "does", "do", "did",
        "can", "could", "would", "should",
        "please", "tell", "me",
        "about", "of", "for", "to",
        "their", "they", "them"
    }

    question_words = {
        word.strip("?,.!:;()[]{}").lower()
        for word in question_lower.split()
        if word.strip("?,.!:;()[]{}").lower()
        not in stop_words
    }

    # =========================================================
    # SPLIT INTO SENTENCES
    # =========================================================

    sentences = []

    for paragraph in context.split("\n"):

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        parts = re.split(
            r"(?<=[.!?])\s+",
            paragraph
        )

        for sentence in parts:

            sentence = sentence.strip()

            if not sentence:
                continue

            sentence_words = {
                word.strip("?,.!:;()[]{}").lower()
                for word in sentence.split()
            }

            overlap = len(
                question_words.intersection(
                    sentence_words
                )
            )

            sentences.append(
                (overlap, sentence)
            )

    sentences.sort(
        key=lambda x: x[0],
        reverse=True
    )

    best_sentences = [
        sentence
        for score, sentence in sentences[:3]
        if score > 0
    ]

    if best_sentences:
        return ". ".join(best_sentences) + "."

    return (
        "Relevant information was retrieved from the "
        "document, but a direct answer could not be determined."
    )