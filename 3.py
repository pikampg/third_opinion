"""
Удалить информацию хранящуюся в ключе PatientName (анонимизировать файлы)

Используя информацию в ключах StudyInstanceUID, SeriesInstanceUID, SOPInstanceUID преобразовать структуру хранения файлов к следующей:

    - на первом уровне StudyInstanceUID
    - на втором уровне SeriesInstanceUID
    - именем файла будет значение SOPInstanceUID с расширением .dcm
    
Таким образом, путь к каждому файлу будет выглядеть так: $StudyInstanceUID/$SeriesInstanceUID/$SOPInstanceUID.dcm

Дополнительно, нужно создать файл, в котором путь к каждому файлу исходной структуры сопоставлен пути к файлу в конечной структуре.
"""

from pathlib import Path
import json
import pydicom

PATH_TO_PATIENTS = 'src'


def prepare_folders(file_dir: str) -> None:
    folder = Path(file_dir)
    file_map = {}
    
    for file in folder.glob('*'):
        dataset = pydicom.read_file(file)

        dataset.PatientName = None
        study = dataset.StudyInstanceUID
        series = dataset.SeriesInstanceUID
        file_name = dataset.SOPInstanceUID

        structure = f'{study}/{series}'
        Path(structure).mkdir(parents=True, exist_ok=True)

        end_file_path = f"{structure}/{file_name}.dcm"
        dataset.save_as(end_file_path)

        file_map[str(file)] = end_file_path
 

    with open("mapping.json", "a") as f:
        f.write(json.dumps(file_map, indent=4))


if __name__ == "__main__":
    prepare_folders(PATH_TO_PATIENTS)
