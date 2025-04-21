# config.py

import os
from pathlib import Path

# ---------------------- DADOS DO SISTEMA ----------------------
APP_TITLE = "Sistema de Análises Centesimais"
LAYOUT_MODE = "wide"
SECRET_KEY = os.getenv("SECRET_KEY", "supersecreto123")

# ---------------------- BANCO DE DADOS ----------------------
# Usando Path para compatibilidade
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = os.getenv("DB_PATH", BASE_DIR / "banco.db")

# ---------------------- PARÂMETROS PADRÃO ----------------------
PADRAO_FATOR_KJELDAHL = 6.25
TIPOS_USUARIO = ["usuario", "admin"]

# ---------------------- DEBUG E LOGS ----------------------
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")