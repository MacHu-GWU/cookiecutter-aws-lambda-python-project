# -*- coding: utf-8 -*-

from s3pathlib import S3Path

from ..config.init import config
from ..logger import logger


def low_level_api(
    s3path_source: S3Path,
):
    logger.info(f"copy {s3path_source.uri}")
    logger.info(f"preview: {s3path_source.console_url}", indent=1)

    s3path_target = config.env.s3dir_target.joinpath(
        s3path_source.relative_to(config.env.s3dir_source)
    )
    logger.info(f"to {s3path_target.uri}")
    logger.info(f"preview: {s3path_target.console_url}", indent=1)
    s3path_source.copy_to(s3path_target, overwrite=True)


def lambda_handler(bucket: str, key: str):
    return low_level_api(s3path_source=S3Path(bucket, key))
