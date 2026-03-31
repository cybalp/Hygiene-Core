import os
import yaml
import importlib.util
import logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Orchestrator:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = BASE_DIR / "config.yaml"
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.logger = logging.getLogger("HygieneCore")
        self.modules_path = BASE_DIR / "modules"
        self.results = []

    def load_modules(self):
        modules = []
        for file in self.modules_path.glob("*.py"):
            if file.name == "__init__.py":
                continue
            
            spec = importlib.util.spec_from_file_location(file.stem, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            for attr in dir(module):
                cls = getattr(module, attr)
                if isinstance(cls, type) and cls.__module__ == file.stem:
                    if hasattr(cls, 'run'):
                        modules.append(cls(self.config))
        return modules

    def run_pipeline(self):
        modules = self.load_modules()
        self.results = [] # Reset results for each run
        for module in modules:
            module_name = module.__class__.__name__
            try:
                if hasattr(module, "pre_run"):
                    module.pre_run()
                
                self.logger.info(f"Running module: {module_name}")
                result = module.run()
                if isinstance(result, dict):
                    self.results.append(result)
                
                if hasattr(module, "post_run"):
                    module.post_run()
            except Exception as e:
                self.logger.error(f"Module {module_name} failed: {str(e)}")
        
        return self.results
