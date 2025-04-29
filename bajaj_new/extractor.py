import pytesseract

# If tesseract isn't in your system PATH, specify its full path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from PIL import Image
import re
from typing import Union, List, Dict


def is_out_of_range(value: float, reference_range: str) -> bool:
    """
    Given a numeric value and a reference range string like "12.0-15.0",
    return True if value is outside [min, max].
    """
    try:
        # remove spaces, split on '-', convert to floats
        low, high = map(float, reference_range.replace(" ", "").split("-"))
        return not (low <= value <= high)
    except Exception:
        return False


def clean_test_name(name: str) -> str:
    """
    Cleans up the test name by removing unnecessary characters, line breaks, or irrelevant prefixes.
    """
    # Remove line breaks and extra spaces
    name = re.sub(r"[\n\r]+", " ", name).strip()
    # Remove irrelevant prefixes like "(Flow cytometry)" or similar
    name = re.sub(r"\(.*?\)", "", name).strip()
    return name


def extract_lab_tests_from_image(image_input: Union[str, Image.Image]) -> List[Dict]:
    """
    Extracts lab test entries from either:
      - a filesystem path (str) to an image, or
      - a PIL Image object

    Returns a list of dicts:
      {
        "test_name": str,
        "test_value": str,
        "bio_reference_range": str,
        "test_unit": str,
        "lab_test_out_of_range": bool
      }
    """
    # load PIL Image if needed
    if isinstance(image_input, str):
        img = Image.open(image_input)
    elif isinstance(image_input, Image.Image):
        img = image_input
    else:
        raise ValueError("extract_lab_tests_from_image expects a filepath or PIL.Image")

    # OCR
    raw_text = pytesseract.image_to_string(img)

    # Regex to capture: name, value, unit, reference_range
    pattern = re.compile(
        r"([A-Za-z\s\(\)%\/]+?)\s+"            # test name (lazy)
        r"([\d]+(?:\.\d+)?)\s*"                # test value
        r"([A-Za-z/%µμdL]+)?\s+"               # optional unit (g/dL, %, etc)
        r"(\d+(?:\.\d+)?\s*-\s*\d+(?:\.\d+)?)" # reference range
    )

    results = []
    for m in pattern.finditer(raw_text):
        name = clean_test_name(m.group(1))
        value = m.group(2).strip()
        unit = m.group(3).strip() if m.group(3) else ""
        ref_range = m.group(4).replace(" ", "")

        # compute out-of-range
        try:
            oor = is_out_of_range(float(value), ref_range)
        except:
            oor = False

        results.append({
            "test_name": name,
            "test_value": value,
            "bio_reference_range": ref_range,
            "test_unit": unit,
            "lab_test_out_of_range": oor
        })

    return results


# if you ever want to run this file standalone for quick tests:
if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "sample_reports/report1.png"
    tests = extract_lab_tests_from_image(path)
    for t in tests:
        print(t)
