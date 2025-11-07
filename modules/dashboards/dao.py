from typing import Optional, List, Dict, Any, Tuple
from config.database import get_connection

def _fetch_all(sql: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[List[Dict[str, Any]]]:
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"[dashboards.dao] Erro ao executar SQL (all): {e}")
        return None
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()

def _fetch_one(sql: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Dict[str, Any]]:
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        row = cursor.fetchone()
        return row
    except Exception as e:
        print(f"[dashboards.dao] Erro ao executar SQL (one): {e}")
        return None
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()

def get_viagens_mensal() -> Optional[List[Dict[str, Any]]]:
    return _fetch_all("SELECT * FROM vw_viagens_mensal")

def get_resumo_financeiro() -> Optional[List[Dict[str, Any]]]:
    return _fetch_all("SELECT * FROM vw_resumo_financeiro")

def get_analise_despesas() -> Optional[List[Dict[str, Any]]]:
    return _fetch_all("SELECT * FROM vw_analise_despesas")

def get_analise_rotas() -> Optional[List[Dict[str, Any]]]:
    return _fetch_all("SELECT * FROM vw_analise_rotas")

def get_kpis() -> Optional[List[Dict[str, Any]]]:
    return _fetch_all("SELECT * FROM vw_dashboard_kpis")

def get_top_motoristas(limit: Optional[int] = None) -> Optional[List[Dict[str, Any]]]:
    sql = "SELECT * FROM vw_top_motoristas"
    if isinstance(limit, int) and limit > 0:
        sql += " LIMIT %s"
        return _fetch_all(sql, (limit,))
    return _fetch_all(sql)

def get_top_veiculos(limit: Optional[int] = None) -> Optional[List[Dict[str, Any]]]:
    sql = "SELECT * FROM vw_top_veiculos"
    if isinstance(limit, int) and limit > 0:
        sql += " LIMIT %s"
        return _fetch_all(sql, (limit,))
    return _fetch_all(sql)

def get_ultimas_viagens(limit: Optional[int] = 50) -> Optional[List[Dict[str, Any]]]:
    sql = "SELECT * FROM vw_ultimas_viagens"
    if isinstance(limit, int) and limit > 0:
        sql += " LIMIT %s"
        return _fetch_all(sql, (limit,))
    return _fetch_all(sql)