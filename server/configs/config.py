import json
import os
from threading import Lock
from typing import Dict, Any, Optional

class Config:
    _instance = None
    _lock = Lock()
    _config_data: Dict[str, Any] = {}
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance
    
    def __init__(self):
        if not self._config_data:
            self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from JSON file"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with self._lock:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config_data = json.load(f)
    
    def get_team_by_name(self, team_name: str) -> Optional[Dict[str, Any]]:
        """Find team by name in teams list"""
        with self._lock:
            for team in self._config_data['teams']:
                if team['name'] == team_name:
                    return team
            return None
        
    def get_team_by_id(self, team_id: str) -> Optional[Dict[str, Any]]:
        """Find team by name in teams list"""
        with self._lock:
            for team in self._config_data['teams']:
                if team['id'] == team_id:
                    return team
            return None

    def get_teams(self, export = False) -> list[Dict[str, Any]]:
        """Get all teams with only id and name"""
        with self._lock:
            if export:
                return self._config_data['teams']
            else:
                return [{'id': team['id'], 'name': team['name']} for team in self._config_data['teams']]

    def get_team_config(self, team_name: str) -> Optional[Dict[str, Any]]:
        """Get team configuration by team name"""
        team = self.get_team_by_name(team_name)
        return team if team else None

    def get_groups(self, team_id: str) -> list[str]:
        """Get all group names for a specific team"""
        team = self.get_team_by_id(team_id)
        if team and 'groups' in team:
            with self._lock:
                return list(team['groups'].keys())
        return []

    def get_group_config(self, team_name: str, group_name: str) -> Optional[Dict[str, Any]]:
        """Get group configuration by team and group name"""
        team = self.get_team_by_name(team_name)
        if team and 'groups' in team:
            return team['groups'].get(group_name)
        return None
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get entire configuration"""
        with self._lock:
            return self._config_data.copy()

    def reload_config(self) -> None:
        """Reload configuration from file"""
        self.load_config()
    
def main():
    config = Config()
    teams = config.get_teams(False)
    
    for team in teams:
        print(team)
        groups = config.get_groups(team["id"])
        for group in groups:
            print(group)
            group_config = config.get_group_config(team, group)
            print(group_config)
    
    
if __name__ == '__main__':
    main()
