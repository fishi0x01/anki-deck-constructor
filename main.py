from docx import Document
import genanki
import random
from lxml import etree


def has_image(cell):
    # Parse the cell's XML
    cell_xml = etree.fromstring(cell._tc.xml)
    # Check if the cell's XML contains an image tag
    return bool(cell_xml.findall('.//pic:pic', namespaces={'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture'}))


# Define your Model
card_model = genanki.Model(
  random.randrange(1 << 30, 1 << 31),
  'Core Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])

# Create a Deck
deck = genanki.Deck(
  random.randrange(1 << 30, 1 << 31),
  'PralinenCoreDeck')


doc = Document("input.docx")

media_files = []
j = 0
rel_list = reversed(doc.part.rels.values())
for rel in rel_list:
    if "image" in rel.target_ref:
        image_data = rel.target_part.blob
        image_file = f"media/image{len(media_files)}.jpg"
        with open(image_file, "wb") as f:
            f.write(image_data)
        media_files.append(image_file)

for table in doc.tables:
    for i, row in enumerate(table.rows):
        if len(row.cells) != 3:
            raise RuntimeError("Table must have 3 columns")
        front = row.cells[0].text
        back = "- " + row.cells[1].text
        back = back.replace("\n", "<br> - ")

        image = ""
        if has_image(row.cells[2]):
            p = media_files[j]
            p = p.split("/")[1]
            j += 1
            image = f"<br><img src='{p}' />"
        back += image

        note = genanki.Note(
            model=card_model,
            fields=[front, back],
        )
        deck.add_note(note)

package = genanki.Package(deck)
package.media_files = media_files
package.write_to_file('deck.apkg')
