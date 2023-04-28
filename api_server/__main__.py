import argparse
from .http_server.http_server import HTTPServer
from .http_server.http_server_context import HTTPServerContext
from .http_server.http_server_env import HTTPServerEnv
from .aiomysql_db import AioMysqlDB

def main():
    parser = argparse.ArgumentParser(description='메이플스토리 유틸 서비스 API 서버')

    parser.add_argument('--port', type=str, help='port to open by webserver', default=8080)
    parser.add_argument('--db_host', type=str, help='db config db_host', default="db")
    parser.add_argument('--db_port', type=int, help='db config db_port', default=3306)
    parser.add_argument('--db_user', type=str, help='db config db_user', default="user")
    parser.add_argument('--db_password', type=str, help='db config db_password', default="1234")
    parser.add_argument('--db_name', type=str, help='db config db_name', default="db")

    args = parser.parse_args()

    # create db
    db = AioMysqlDB(
        db_host=args.db_host,
        db_port=args.db_port,
        db_user=args.db_user,
        db_password=args.db_password,
        db_name=args.db_name,
    )

    # create http_env
    http_env = HTTPServerEnv(
        port=args.port,
    )

    # create http_context
    http_context = HTTPServerContext(
        db=db,
        env=http_env,
    )

    # create http_server
    http_server = HTTPServer(
        ctx=http_context,
    )

    http_server.run()
    args.port

if __name__ == "__main__":
    main()