import requests
from typing import Dict, Any, Optional

class ProjectsAPI:
  

    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url
        self.endpoint = f"{self.base_url}/projects"

    def create_project(self, data: Dict[str, Any]) -> requests.Response:
        
        return self.session.post(self.endpoint, json=data)

    def update_project(self, project_id: str, data: Dict[str, Any]) -> requests.Response:
        
        url = f"{self.endpoint}/{project_id}"
        return self.session.put(url, json=data)

    def get_project(self, project_id: str) -> requests.Response:
        
        url = f"{self.endpoint}/{project_id}"
        return self.session.get(url)
