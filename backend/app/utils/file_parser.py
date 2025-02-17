import pandas as pd
from io import BytesIO

from numpy.f2py.auxfuncs import throw_error


async def parse_xlsb(file):
    """Парсит XLSB-файл и возвращает DataFrame"""
    content = await file.read()
    df = pd.read_excel(BytesIO(content), sheet_name="Лист1", engine="pyxlsb")

    df = df.drop(df.columns[0], axis=1)

    # Переименовываем столбцы
    df.columns = [
        "department", "division", "position", "head", "fio",
        "hire_date", "dismissal_date", "status", "employment_type", "salary"
    ]

    # Убираем строки-заголовки
    df = df.iloc[2:].dropna(subset=["fio"])

    # Преобразуем даты
    df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce")
    df["dismissal_date"] = pd.to_datetime(df["dismissal_date"], errors="coerce")

    return df
