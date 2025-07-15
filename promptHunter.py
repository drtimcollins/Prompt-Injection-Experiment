import pymupdf

# Simple estimator of color intensity as 8-bit average of RGB components
def rgbIntensity(c):
    rgb = [c & 0xFF, (c >> 8) & 0xFF, (c >> 16) & 0xFF]
    return sum(rgb) / 3

# Looks for small text with high color intensity in a PDF document
def analyseDoc(fname):
    doc = pymupdf.open(fname)

    for p in range(len(doc)):
        page = doc[p]

        # read page text as a dict
        blocks = page.get_text("dict", flags=11)["blocks"]
        for b in blocks:
            for l in b["lines"]:
                for s in l["spans"]:
                    # Thresholds are arbitrary, but seem to be a reasonable comprompise
                    if rgbIntensity(s['color']) > 180 and s["size"] < 3:
                        print(f'Page {p+1}:')
                        print(f"Text: '{s["text"]}'")
                        print(f"Fontsize {s["size"]}, color {s["color"]:06x}")


def promptHunter(fileName):
    print(f'Analysing pdf: {fileName}')
    try:
        analyseDoc(fileName)
    except Exception as e:  # Catch any exception that occurs
        print(f"Error processing {fileName}: {e}")

# Example usage
promptHunter('Garbage_Paper_v1.pdf')
promptHunter('Garbage_Paper_v2.pdf')
