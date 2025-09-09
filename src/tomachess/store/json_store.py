import json
from pathlib import Path
from typing import Any, Sequence, Type, TypeVar, cast

from tomachess.models import Entity
from tomachess.participant import Player, Team
from tomachess.store.abstract_store import AbstractStore
from tomachess.union_type import Tournament, TeamTournament

T = TypeVar("T", bound=Entity)


class JsonStore(AbstractStore):
    def __init__(self, store_path: Path) -> None:
        self.store_path: Path = store_path
        self.store_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as f:
            return cast(dict[str, Any], json.load(f))

    @staticmethod
    def _save_json(path: Path, data: dict[str, Any]) -> None:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _get_file_path(self, folder: str, collection: str) -> Path:
        dir_path = self.store_path / folder
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path / f"{collection}.json"

    def _save_models(self, folder: str, collection: str, models: Sequence[T]) -> None:
        path = self._get_file_path(folder, collection)
        data = self._load_json(path)
        for model in models:
            data[str(model.uuid)] = model.model_dump(mode="json")
        self._save_json(path, data)

    def _load_models(self, folder: str, collection: str, model_cls: Type[T]) -> list[T]:
        path = self._get_file_path(folder, collection)
        data = self._load_json(path)
        return [model_cls(**item) for item in data.values()]

    def save_players(self, collection: str, players: Sequence[Player]) -> None:
        self._save_models("players", collection, players)

    def load_players(self, collection: str) -> list[Player]:
        return self._load_models("players", collection, Player)

    def save_teams(self, collection: str, teams: Sequence[Team]) -> None:
        self._save_models("teams", collection, teams)

    def load_teams(self, collection: str) -> list[Team]:
        return self._load_models("teams", collection, Team)

    def save_tournaments(self, collection: str, tournaments: Sequence[Tournament]) -> None:
        self._save_models("tournaments", collection, tournaments)

    def load_tournaments(self, collection: str) -> list[Tournament]:
        return self._load_models("tournaments", collection, Tournament)

    def save_team_tournaments(self, collection: str, team_tournaments: Sequence[TeamTournament]) -> None:
        self._save_models("team_tournaments", collection, team_tournaments)

    def load_team_tournaments(self, collection: str) -> list[TeamTournament]:
        return self._load_models("team_tournaments", collection, TeamTournament)
