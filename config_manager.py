import json
import os

class ConfigManager:
    def __init__(self, config_dir='configs'):
        self.config_dir = config_dir
        self.branch_file = os.path.join(config_dir, 'branch_list.json')
        self._ensure_config_dir()
        
    def _ensure_config_dir(self):
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            
    def load_branches(self):
        try:
            with open(self.branch_file, 'r') as f:
                data = json.load(f)
                return data.get('branches', [])
        except Exception as e:
            print(f"브랜치 파일 로딩 실패: {str(e)}")
            return []
            
    def save_branches(self, branches):
        try:
            with open(self.branch_file, 'w') as f:
                json.dump({'branches': branches}, f, indent=4)
            return True
        except Exception as e:
            print(f"브랜치 파일 저장 실패: {str(e)}")
            return False
            
    def get_branch_names(self):
        branches = self.load_branches()
        return [branch['name'] for branch in branches]
    
    def get_branch_tags(self, branch_name):
        branches = self.load_branches()
        for branch in branches:
            if branch['name'] == branch_name:
                return branch.get('tags', [])
        return []

    def load_branches_raw(self):
        """브랜치 설정 파일의 원본 JSON을 반환"""
        with open(self.branch_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_branches_raw(self, data):
        """브랜치 설정 파일에 원본 JSON을 저장"""
        with open(self.branch_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)