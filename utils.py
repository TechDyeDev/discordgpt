from pathlib import Path
from json import load, dump, JSONDecodeError

def load_json(file: Path) -> str:
	with open(file, "r") as f:
		return load(f)

def dump_json(file: Path, table: list) -> bool:
	try:
		with open(file, "w") as f:
			dump(table, f, indent=4)
		return True
	except JSONDecodeError:
		return False