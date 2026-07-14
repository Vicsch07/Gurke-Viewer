import shutil
from pathlib import Path

def clear_pycache(target_dir=".", dry_run=True):
    target = Path(target_dir).resolve()
    print(f"Suche in: {target}")

    # Sucht rekursiv nach allen __pycache__ Ordnern
    pycache_dirs = list(target.rglob("__pycache__"))

    if not pycache_dirs:
        print("Keine __pycache__ Ordner gefunden. Alles clean.")
        return

    print(f"{len(pycache_dirs)} __pycache__ Ordner gefunden.")

    for p in pycache_dirs:
        if p.is_dir():
            if dry_run:
                print(f"[DRY RUN] Würde löschen: {p}")
            else:
                try:
                    shutil.rmtree(p)
                    print(f"Gelöscht: {p}")
                except Exception as e:
                    print(f"Fehler beim Löschen von {p}: {e}")

if __name__ == "__main__":
    # dry_run=True ist dein Sicherheits-Check. 
    # Wenn du dir sicher bist, setze es auf False, um wirklich zu löschen.
    clear_pycache(dry_run=False)