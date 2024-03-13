import whisper
from moviepy.editor import VideoFileClip as VFC
import PyPDF2
import sys

type = sys.argv[1]
name = sys.argv[2]
file = open("output_txt_files/"+name[:-4]+".txt", "w")
model = whisper.load_model("base.en")

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
        pdfread = PyPDF2.PdfReader(f)
        num_pages = len(pdfread.pages)
        txt += ("Total number of pages: "+str(num_pages)+"\n")
        for page_num in range(num_pages):
            text = (pdfread.pages[page_num]).extract_text() 
            txt += ("Text on page:"+str(page_num)+"\n") + text + "\n"
    file.write(txt)
else:
    print("Invalid input - give correct argument")