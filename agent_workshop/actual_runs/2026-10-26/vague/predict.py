"""Apply the saved synthetic motif model to a local CSV without refitting."""
import argparse
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def local_path(value):
    path = (ROOT / value).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError("All paths must remain inside this run directory")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", help="CSV with sample_id and sequence columns")
    parser.add_argument("output_csv", help="New prediction CSV; must not already exist")
    arguments = parser.parse_args()
    input_path = local_path(arguments.input_csv)
    output_path = local_path(arguments.output_csv)
    if output_path.exists():
        raise ValueError("Refusing to overwrite an existing output or input file")
    model = json.loads((ROOT / "model.json").read_text(encoding="utf-8"))
    with input_path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if not {"sample_id", "sequence"}.issubset(reader.fieldnames or []):
            raise ValueError("CSV must include sample_id and sequence")
        rows = list(reader)
    seen = set()
    predictions = []
    for row in rows:
        sequence = row["sequence"]
        if not row["sample_id"] or row["sample_id"] in seen:
            raise ValueError("Missing or duplicate sample_id")
        seen.add(row["sample_id"])
        if len(sequence) != model["sequence_length"] or set(sequence) - set(model["allowed_alphabet"]):
            raise ValueError("Each sequence must be 160 uppercase A/C/G/T bases")
        presence = int(model["motif"] in sequence)
        logit = model["intercept"][0] + model["coefficient"][0][0] * presence
        probability = 1 / (1 + math.exp(-logit))
        predictions.append({
            "sample_id": row["sample_id"], "probability_label_1": probability,
            "predicted_label": int(probability >= model["threshold"]),
            "disclosed_motif_present": presence,
        })
    columns = ["sample_id", "probability_label_1", "predicted_label", "disclosed_motif_present"]
    with output_path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(predictions)
    print(f"Wrote {len(predictions)} predictions to {output_path.name}; no fitting or scoring.")


if __name__ == "__main__":
    main()
