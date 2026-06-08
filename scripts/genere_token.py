import argparse
import os
from datetime import datetime, timedelta, timezone
import jwt


def genere_token() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nom", required=True, help="Nom du token")
    parser.add_argument(
        "--duree",
        required=True,
        help="Durée de validité du token (par défaut en heures)",
    )
    parser.add_argument(
        "--jours",
        action="store_true",
        help="Pour porter la durée de validité du token en jours",
    )
    args = parser.parse_args()

    clef_jwt = os.getenv("MCP_CLEF_JWT", "")
    duree_du_token = _duree_du_token(float(args.duree), args.jours)
    maintenant = datetime.now(timezone.utc)

    payload = {
        "name": args.nom,
        "sub": args.nom,
        "client_id": args.nom,
        "scope": "question:poser",
        "iat": maintenant,
        "exp": maintenant + duree_du_token,
        "iss": "internal-auth-service",
        "aud": "mcp-internal-api",
    }

    token = jwt.encode(
        payload,
        clef_jwt,
        algorithm="HS256",
    )

    print(token)


def _duree_du_token(duree: float, est_en_jours: bool) -> timedelta:
    duree_token = timedelta(hours=duree)
    if est_en_jours:
        duree_token = timedelta(days=duree)
    return duree_token


if __name__ == "__main__":
    genere_token()
