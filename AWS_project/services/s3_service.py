import boto3

from botocore.exceptions import (
    BotoCoreError,
    ClientError
)


class S3Service:

    def __init__(
        self,
        region_name: str,
        bucket_name: str
    ):

        self.region_name = region_name
        self.bucket_name = bucket_name

        self.client = boto3.client(
            "s3",
            region_name=region_name
        )

    def upload_file(
        self,
        file_path: str,
        object_key: str
    ) -> str:

        if not self.bucket_name:
            raise ValueError(
                "S3_BUCKET is not configured."
            )

        try:

            self.client.upload_file(
                file_path,
                self.bucket_name,
                object_key
            )

            return (
                f"s3://{self.bucket_name}/"
                f"{object_key}"
            )

        except (
            ClientError,
            BotoCoreError
        ) as exc:

            raise RuntimeError(
                f"S3 upload failed: {exc}"
            ) from exc

    def delete_file(
        self,
        object_key: str
    ) -> bool:

        try:

            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=object_key
            )

            return True

        except (
            ClientError,
            BotoCoreError
        ) as exc:

            raise RuntimeError(
                f"S3 delete failed: {exc}"
            ) from exc

    def object_exists(
        self,
        object_key: str
    ) -> bool:

        try:

            self.client.head_object(
                Bucket=self.bucket_name,
                Key=object_key
            )

            return True

        except ClientError:

            return False