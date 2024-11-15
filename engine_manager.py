import importlib

class EngineManager:
    def load_engine(self, engine_id):
        engine_module = importlib.import_module(f'engines.engine{engine_id}')
        return engine_module.ChessEngine()

