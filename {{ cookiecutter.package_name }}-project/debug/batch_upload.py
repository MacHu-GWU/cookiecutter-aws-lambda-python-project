# -*- coding: utf-8 -*-

from pathlib_mate import Path
from aws_idp_doc_store.config.init import config

dir_landing = Path("/Users/sanhehu/Downloads/redacted-nlp-claim-files")

env = config.dev
print(env.s3dir_doc_store.console_url)
env.s3dir_doc_store.delete_if_exists()
env.s3dir_docs_landing.upload_dir(dir_landing.abspath, overwrite=True)
