import argparse
from services.user_service import UserService
from services.poll_service import PollService
from services.nft_service import NFTService

user_service = UserService()
poll_service = PollService()
nft_service = NFTService()

def main():
    parser = argparse.ArgumentParser(description="Controlador CLI para streamers")
    subparsers = parser.add_subparsers(dest="comando")

    # Registro
    registro = subparsers.add_parser("registrar")
    registro.add_argument("username")
    registro.add_argument("password")

    # Login
    login = subparsers.add_parser("login")
    login.add_argument("username")
    login.add_argument("password")

    # Crear encuesta
    crear = subparsers.add_parser("crear_encuesta")
    crear.add_argument("pregunta")
    crear.add_argument("opciones", nargs="+")
    crear.add_argument("--duracion", type=int, default=60)
    crear.add_argument("--tipo", choices=["simple", "multiple"], default="simple")

    # Votar
    votar = subparsers.add_parser("votar")
    votar.add_argument("poll_id")
    votar.add_argument("username")
    votar.add_argument("opcion")

    # Cerrar encuesta
    cerrar = subparsers.add_parser("cerrar_encuesta")
    cerrar.add_argument("poll_id")

    # Resultados
    resultados = subparsers.add_parser("ver_resultados")
    resultados.add_argument("poll_id")

    # Tokens
    tokens = subparsers.add_parser("mis_tokens")
    tokens.add_argument("username")

    # Transferir
    transferir = subparsers.add_parser("transferir_token")
    transferir.add_argument("token_id")
    transferir.add_argument("nuevo_owner")

    args = parser.parse_args()

    if args.comando == "registrar":
        user_service.registrar(args.username, args.password)
    elif args.comando == "login":
        user_service.login(args.username, args.password)
    elif args.comando == "crear_encuesta":
        poll_service.crear_encuesta(args.pregunta, args.opciones, args.duracion, args.tipo)
    elif args.comando == "votar":
        poll_service.votar(args.poll_id, args.username, args.opcion)
    elif args.comando == "cerrar_encuesta":
        poll_service.cerrar_encuesta(args.poll_id)
    elif args.comando == "ver_resultados":
        resultados = poll_service.resultados_finales(args.poll_id)
        print(resultados)
    elif args.comando == "mis_tokens":
        tokens = nft_service.obtener_tokens(args.username)
        print(tokens)
    elif args.comando == "transferir_token":
        nft_service.transferir_token(args.token_id, args.nuevo_owner)
    else:
        parser.print_help()
