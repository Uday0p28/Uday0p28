from typing import Optional

from langchain_aws import (
    ChatBedrockConverse
)

from config import (
    AWS_REGION,
    BEDROCK_MODEL_ID,
    BEDROCK_GUARDRAIL_ID,
    BEDROCK_GUARDRAIL_VERSION
)


class BedrockService:
    """
    Amazon Bedrock service wrapper.

    LangChain's ChatBedrockConverse is used
    to communicate with Bedrock's Converse API.
    """

    def __init__(self):

        self.model_id = (
            BEDROCK_MODEL_ID.strip()
        )

        if not self.model_id:

            self.model = None

            return

        kwargs = {
            "model": self.model_id,
            "region_name": AWS_REGION,
            "temperature": 0.2,
            "max_tokens": 3000
        }

        # Add guardrail only when configured.
        if (
            BEDROCK_GUARDRAIL_ID
            and BEDROCK_GUARDRAIL_VERSION
        ):

            kwargs[
                "guardrail_config"
            ] = {
                "guardrailIdentifier":
                    BEDROCK_GUARDRAIL_ID,

                "guardrailVersion":
                    BEDROCK_GUARDRAIL_VERSION
            }

        self.model = ChatBedrockConverse(
            **kwargs
        )

    def is_configured(self) -> bool:

        return self.model is not None

    def get_model_name(self) -> str:

        if not self.model_id:
            return "Not configured"

        return self.model_id

    def summarize(
        self,
        langchain_service,
        document_text: str
    ) -> str:

        if not self.model:

            raise RuntimeError(
                "BEDROCK_MODEL_ID is not configured."
            )

        return langchain_service.summarize(
            document_text
        )