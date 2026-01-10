import pytest
import uuid
from api.projects_api import ProjectsAPI

class TestProjectsAPI:
    

    @pytest.fixture(autouse=True)
    def setup(self, api_session, base_url):
        self.api = ProjectsAPI(api_session, base_url)
        self.prefix = f"Test_{uuid.uuid4().hex[:8]}"



    def test_create_project_positive(self):
        """
        Позитивный тест: создание проекта с корректными данными.
        """
        data = {
            "title": f"{self.prefix}_NewProject",
            "description": "Test project description"
        }
        response = self.api.create_project(data)

        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        assert "id" in response.json(), "Response should contain project ID"
        assert response.json()["title"] == data["title"]

    def test_create_project_negative_missing_title(self):
        """
        Негативный тест: попытка создать проект без обязательного поля title.
        """
        data = {
            "description": "Project without title"
        }
        response = self.api.create_project(data)

        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert "error" in response.json() or "message" in response.json()

    

    def test_update_project_positive(self):
        """
        Позитивный тест: обновление проекта с корректными данными.
        """
        
        create_data = {
            "title": f"{self.prefix}_Original",
            "description": "Original description"
        }
        create_response = self.api.create_project(create_data)
        assert create_response.status_code == 201
        project_id = create_response.json()["id"]

        
        update_data = {
            "title": f"{self.prefix}_Updated",
            "description": "Updated description"
        }
        update_response = self.api.update_project(project_id, update_data)

        assert update_response.status_code == 200, f"Expected 200, got {update_response.status_code}"
        updated_project = update_response.json()
        assert updated_project["title"] == update_data["title"]
        assert updated_project["description"] == update_data["description"]

    def test_update_project_negative_invalid_id(self):
        """
        Негативный тест: попытка обновить проект с несуществующим ID.
        """
        invalid_id = "nonexistent_id_123"
        data = {
            "title": "Updated title"
        }
        response = self.api.update_project(invalid_id, data)

        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        assert "error" in response.json() or "message" in response.json()

    

    def test_get_project_positive(self):
        """
        Позитивный тест: получение существующего проекта.
        """
        # Создаём проект для получения
        create_data = {
            "title": f"{self.prefix}_ForGet",
            "description": "Project for GET test"
        }
        create_response = self.api.create_project(create_data)
        assert create_response.status_code == 201
        project_id = create_response.json()["id"]

        
        response = self.api.get_project(project_id)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        project = response.json()
        assert project["id"] == project_id
        assert project["title"] == create_data["title"]
        assert project["description"] == create_data["description"]

    def test_get_project_negative_invalid_id(self):
        """
        Негативный тест: попытка получить проект с несуществующим ID.
        """
        invalid_id = "nonexistent_id_456"
        response = self.api.get_project(invalid_id)

        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        assert "error" in response.json() or "message" in response.json()
