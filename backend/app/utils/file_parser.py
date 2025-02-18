import pandas as pd
from io import BytesIO
from typing import Tuple, Optional
import hashlib
import logging

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Константы для имён столбцов
COLUMNS = [
    "department", "division", "position", "head", "fio",
    "hire_date", "dismissal_date", "status", "employment_type", "salary"
]

DATE_FORMAT = "%d.%m.%Y"  # Формат дат в исходных данных
OUTPUT_DATE_FORMAT = "%Y-%m-%d"  # Желаемый формат дат на выходе


async def parse_excel(file) -> Tuple[pd.DataFrame, Optional[pd.Timestamp], str]:
    """
    Парсит Excel-файл (XLSB, XLSX, XLS, CSV) и возвращает DataFrame с данными,
    дату из ячейки K1 и хеш данных.

    :param file: Файл для парсинга.
    :return: Кортеж (DataFrame, дата из K1, SHA-256 хеш данных).
    """
    try:
        content = await file.read()

        # Определяем формат файла
        if file.filename.endswith(".xlsb"):
            df = pd.read_excel(BytesIO(content), sheet_name="Лист1", engine="pyxlsb")
        elif file.filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(BytesIO(content), sheet_name="Лист1", engine="openpyxl")
        elif file.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(content), delimiter=",")
        else:
            raise ValueError("Неподдерживаемый формат файла")

        # Извлекаем и преобразуем дату из ячейки K1
        date_file = date_excel_to_pandas(df.columns[10])

        # Обрабатываем DataFrame
        df = process_dataframe(df)

        # Получаем SHA-256 хеш данных
        data_hash = get_data_hash(df)

        logger.info("Файл успешно обработан.")
        return df, date_file, data_hash

    except Exception as e:
        logger.error(f"Ошибка при обработке файла: {e}")
        raise


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Обрабатывает DataFrame: удаляет лишние столбцы, переименовывает столбцы,
    удаляет строки-заголовки и преобразует даты.

    :param df: Исходный DataFrame.
    :return: Обработанный DataFrame.
    """
    df = df.drop(df.columns[0], axis=1)  # Убираем первый столбец
    df.columns = COLUMNS  # Переименовываем столбцы
    df = df.iloc[2:].dropna(subset=["fio"])  # Убираем строки-заголовки
    df["hire_date"] = convert_and_format_dates(df["hire_date"])
    df["dismissal_date"] = convert_and_format_dates(df["dismissal_date"])
    # df["hire_date"] = pd.to_datetime(df["hire_date"], format=OUTPUT_DATE_FORMAT, errors="coerce").dt.date
    # df["dismissal_date"] = pd.to_datetime(df["dismissal_date"], format=OUTPUT_DATE_FORMAT, errors="coerce").dt.date

    return df


def convert_and_format_dates(date_series: pd.Series) -> pd.Series:
    """
    Преобразует серию дат в указанный формат.

    :param date_series: Серия с датами.
    :return: Серия с датами в формате OUTPUT_DATE_FORMAT.
    """
    date_series = date_series.astype(str).str.strip()
    dates = pd.to_datetime(date_series, format=DATE_FORMAT, errors="coerce")

    if dates.isna().any():
        excel_dates = pd.to_numeric(date_series, errors="coerce")
        dates = dates.fillna(pd.to_datetime(excel_dates, origin="1899-12-30", unit="D"))

    formatted_dates = dates.dt.strftime(OUTPUT_DATE_FORMAT).fillna("")
    return formatted_dates


def date_excel_to_pandas(date) -> Optional[pd.Timestamp]:
    """
    Преобразует дату из Excel (число или строку) в объект pandas.Timestamp.

    :param date: Дата из Excel (число или строка).
    :return: Преобразованная дата или None, если преобразование не удалось.
    """
    if pd.notna(date):
        if isinstance(date, (int, float)):
            return pd.to_datetime(date, origin="1899-12-30", unit="D")
        return pd.to_datetime(date, errors="coerce")
    return None


def get_data_hash(df: pd.DataFrame) -> str:
    """
    Генерирует SHA-256 хеш данных DataFrame.

    1. Сортирует строки и столбцы.
    2. Преобразует в JSON.
    3. Вычисляет SHA-256 хеш.

    :param df: DataFrame с данными.
    :return: SHA-256 хеш данных.
    """
    df_sorted = df.sort_values(by=COLUMNS, ignore_index=True)
    json_data = df_sorted.to_json(orient="records", date_format="iso")
    return hashlib.sha256(json_data.encode("utf-8")).hexdigest()
