from langchain_core.prompts import (
    ChatPromptTemplate
)


class LangChainService:
    """
    Creates and manages the LangChain prompt workflow.
    """

    def __init__(self, model):

        self.model = model

        self.summary_prompt = (
            ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """
You are an expert document intelligence assistant.

Your task is to analyze a document and produce
an accurate, useful summary.

Rules:

1. Only use information contained in the document.
2. Do not invent facts.
3. Do not assume information that is not present.
4. Focus on important information.
5. Use clear professional language.
6. Make the result easy to scan.

Return the response using these sections:

EXECUTIVE SUMMARY

KEY POINTS

IMPORTANT FINDINGS

CONCLUSION

KEYWORDS
                        """
                    ),
                    (
                        "human",
                        """
Analyze the following document:

{document}
                        """
                    )
                ]
            )
        )

        self.chain = (
            self.summary_prompt
            | self.model
        )

    def summarize(
        self,
        document_text: str
    ) -> str:

        response = self.chain.invoke(
            {
                "document": document_text
            }
        )

        return self._extract_content(
            response
        )

    @staticmethod
    def _extract_content(
        response
    ) -> str:

        content = getattr(
            response,
            "content",
            ""
        )

        if isinstance(content, str):
            return content

        if isinstance(content, list):

            parts = []

            for block in content:

                if isinstance(
                    block,
                    dict
                ):

                    text = block.get(
                        "text"
                    )

                    if text:
                        parts.append(text)

            return "\n".join(parts)

        return str(content)