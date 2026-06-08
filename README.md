# anssi-recommandations-cyber-mcp

Serveur MCP pour exposer l'outil `pose_question` de MesQuestionsCyber.

## Installation

Pre-requis : Python 3.14, `uv` et Node.js pour lancer MCP Inspector.

```bash
uv sync
```

## Configuration

Renseigner les valeurs dans `.env` à partir du modèle `.env.template`.

`URL_MQC` et `PORT_MQC` pointent vers l'API MesQuestionsCyber.
`MCP_CLEF_JWT` est le secret local utilisé pour verifier les JWT Bearer envoyés au serveur MCP.

## Lancer le serveur MCP

Depuis la racine du projet :

```bash
uv run --env-file .env python src/serveur_mcp.py
```

Le serveur écoute ensuite sur :

```text
http://127.0.0.1:8001/mcp
```

## Générer un JWT pour Inspector

Le serveur attend un JWT HS256 signe avec `MCP_CLEF_JWT`, avec :

```text
iss=internal-auth-service
aud=mcp-internal-api
```

Exemple de generation locale :

```bash
uv run --env-file .env python scripts/genere_jwt.py
```

## Lancer MCP Inspector

Dans un autre terminal :

```bash
npx @modelcontextprotocol/inspector
```

Dans Inspector :

```text
URL: http://127.0.0.1:8001/mcp
Transport Type: Streamable HTTP
Connection Type: Via Proxy
```

Dans `Authentication > Custom Headers`, passer en mode JSON et renseigner :

```json
{
  "Authorization": "Bearer <JWT_GENERE>"
}
```

Ne rien renseigner dans `OAuth 2.0 Flow`. Si le header `Authorization` est absent, désactivé ou invalide, Inspector tente un flux OAuth et affiche une erreur `OAuth Authentication Failed`.
