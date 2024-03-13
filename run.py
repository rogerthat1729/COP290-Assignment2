import whisper
import pytesseract as pt
import io
from PIL import Image
import fitz as PyMuPDF
import sys

type = sys.argv[1]
name = sys.argv[2]
file = open("output_txt_files/"+name[:-4]+".txt", "w")
model = whisper.load_model("base.en")

def img_to_txt(img):
    image = Image.open(io.BytesIO(img))
    txt = (pt.image_to_string(image, lang='eng')) + '\n'
    return txt

if type == 'video':
    path = "test_videos/"+name
    result = model.transcribe(path)
    file.write(result["text"])
elif type == 'audio':
    path = "test_audios/"+name
    result = model.transcribe(path)
    file.write(result["text"])
elif type == 'pdf':
    path = "test_pdfs/"+name
    txt = ""
    with open(path, 'rb') as f:
        pdfread = PyMuPDF.open(path)
        num_pages = len(pdfread)
        txt += ("Total number of pages: "+str(num_pages)+"\n")
        for page_num in range(num_pages):
            text = pdfread[page_num].get_text()
            txt += ("Text on page:"+str(page_num)+"\n") + text + "\n"
            for img in pdfread.get_page_images(page_num):
                x = img[0]
                base_img = pdfread.extract_image(x)
                try:
                    img_text = img_to_txt(base_img["image"])
                    txt += img_text
                except:
                    print("Image format not supported on page " + str(page_num) + '\n')
    file.write(txt)
else:
    print("Invalid input - give correct argument")