from pathlib import Path 
import zipfile

root_dir = Path('OUTPUT')
archive_path = root_dir / Path('archive.zip')

with zipfile.ZipFile(archive_path, 'w') as zf:
  for path in root_dir.rglob("*"):
    if path.is_file() and path.name != 'archive.zip':
      zf.write(path)
      path.unlink()