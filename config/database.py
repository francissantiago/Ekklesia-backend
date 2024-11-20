import asyncmy
from asyncmy.cursors import DictCursor
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do .env
load_dotenv()

class Database:
    def __init__(self, host, user, password, db, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.pool = None

    async def connect(self):
        # Criar pool de conexões usando asyncmy
        self.pool = await asyncmy.create_pool(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            port=self.port,
            minsize=1,
            maxsize=5,
            autocommit=True,
        )

    async def disconnect(self):
        # Fechar pool de conexões
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def execute(self, query, values=None):
        # Executar comando de escrita
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, values)
                await conn.commit()

    async def fetch_all(self, query, values=None):
        # Buscar múltiplos registros
        async with self.pool.acquire() as conn:
            async with conn.cursor(cursor=DictCursor) as cur:
                await cur.execute(query, values)
                return await cur.fetchall()

    async def fetch_one(self, query, values=None):
        # Buscar um único registro
        async with self.pool.acquire() as conn:
            async with conn.cursor(cursor=DictCursor) as cur:
                await cur.execute(query, values)
                return await cur.fetchone()


# Criar instâncias para leitura e escrita com variáveis de ambiente
read_db = Database(
    host=os.getenv("DB_READ_HOST"),
    user=os.getenv("DB_READ_USER"),
    password=os.getenv("DB_READ_PASSWORD"),
    db=os.getenv("DB_READ_NAME"),
    port=int(os.getenv("DB_READ_PORT")),
)

write_db = Database(
    host=os.getenv("DB_WRITE_HOST"),
    user=os.getenv("DB_WRITE_USER"),
    password=os.getenv("DB_WRITE_PASSWORD"),
    db=os.getenv("DB_WRITE_NAME"),
    port=int(os.getenv("DB_WRITE_PORT")),
)
