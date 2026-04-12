from environs import Env

# Task 6.3
env = Env()
env.read_env()

mode = env.str("MODE")
docs_user = env.str("DOCS_USER")
docs_password = env.str("DOCS_PASSWORD")
algorithm = env.str("ALGORITHM")
secret_key = env.str("SECRET_KEY")
access_token_expire_minutes = env.str("ACCESS_TOKEN_EXPIRE_MINUTES")