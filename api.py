from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from fastapi.responses import RedirectResponse
import yaml

app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-Key")

with open("keys.yaml") as f:
    api_keys = yaml.safe_load(f)

try:
    with open("badges.yaml") as f:
        badge_dict = yaml.safe_load(f)
except FileNotFoundError:
    badge_dict = dict()


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


@app.get("/")
async def root():
    return


@app.get("/set_badge/")
async def set_badge(repo: str, new_badge: str, branch: str=None, action: str=None, api_key: str = Security(get_api_key)):
    if api_key.rsplit("-", 1)[0] != repo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No permissions for repo",
        )

    if branch is not None or action is not None:
        badge_dict[str((repo, branch, action))] = new_badge
    else:
        badge_dict[repo] = new_badge
    with open("badges.yaml", "w") as f:
        yaml.safe_dump(badge_dict, f)


@app.get("/get_badge/")
async def get_badge(repo: str, branch: str=None, action: str=None):
    if (branch is not None or action is not None and str((repo, branch, action)) not in badge_dict.keys()) or repo not in badge_dict.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Badge not found",
        )
    return RedirectResponse("https://img.shields.io/badge/" + (badge_dict[str((repo, branch, action))] if branch is not None or action is not None else badge_dict[repo]))
