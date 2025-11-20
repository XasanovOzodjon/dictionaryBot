from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()



class Config:
    BOT_TOKEN = env.str("BOT_TOKEN")
    ADMINS = env.list("ADMINS")
    IP = env.str("ip")
    
    #DATABASE
    def get_database_url(self):
        user = env.str("DB_USER")
        password = env.str("DB_PASSWORD")
        host = env.str("DB_HOST")
        port = env.str("DB_PORT")
        db_name = env.str("DB_NAME")
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
    
    
config = Config()