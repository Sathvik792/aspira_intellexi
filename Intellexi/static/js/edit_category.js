import * as popups from './popups.js';
const FileType = document.getElementById('FileType')
const category_id=document.getElementById('category_id').value
const promptInstructions = document.getElementById('promptInstructions')
document.getElementById('docForm').addEventListener('keydown', function (e) {
  // Check if the pressed key is Enter
  console.log("yes")
  if (e.key === 'Enter') {
    if (!e.target.tagName === 'INPUT' || !e.target.tagName === 'TEXTAREA') {
      if (!confirm('Do you want to submit the form?')) {
        e.preventDefault();
      }
    }
  }
});
const doc_form = document.getElementById("docForm");
doc_form.addEventListener("submit", (e) => {

  e.preventDefault();
  const fileType = FileType.value;

  if (fileType == 'pdf') {
    const pdfextractionOntology = document.getElementById('pdfextractionOntology')
    const pdfconversionOntology = document.getElementById('pdfconversionOntology')
   

    let pdf_extraction_string = pdfextractionOntology.value
    pdf_extraction_string = pdf_extraction_string.trim();
    pdf_extraction_string = pdf_extraction_string.replace(/\s+/g, ' ');
    pdf_extraction_string = pdf_extraction_string.replace(/[\n\r]+/g, '');
    pdf_extraction_string = pdf_extraction_string.replace(/,\s*}/g, '}').replace(/,\s*]/g, ']');
    let pdf_conversion_string = pdfconversionOntology.value
    pdf_conversion_string = pdf_conversion_string.trim();
    pdf_conversion_string = pdf_conversion_string.replace(/\s+/g, ' ');
    pdf_conversion_string = pdf_conversion_string.replace(/[\n\r]+/g, '');
    pdf_conversion_string = pdf_conversion_string.replace(/,\s*}/g, '}').replace(/,\s*]/g, ']');
    console.log(doc_form)
    if (doc_form.checkValidity()) {
      if (checkJsontype(pdf_extraction_string, pdf_conversion_string)) {
        const docFormData = new FormData(doc_form)
        fetch(`/edit-category/${category_id}`, {
          method: "POST",
          body: docFormData,
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status) {
              popups.showSuccessPopup()

              setTimeout(() => {
                popups.closeSuccessPopup();
                window.location.href = '/upload_document';
              }, 2000);
            } else {
              document.getElementById('documentCategoryError').textContent = data.message;

              setTimeout(() => {
                document.getElementById('documentCategoryError').textContent = '';
              }, 2000);
              document.getElementById('documentCategory').scrollIntoView();

            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      }
    }

    } else if (fileType == 'xlsx') {


      let excelOntology = promptInstructions.value
      excelOntology = excelOntology.trim();
      excelOntology = excelOntology.replace(/\s+/g, ' ');
      excelOntology = excelOntology.replace(/[\n\r]+/g, '');
      excelOntology = excelOntology.replace(/,\s*}/g, '}').replace(/,\s*]/g, ']');
      console.log(doc_form)
      if (doc_form.checkValidity()) {
          const docFormData = new FormData(doc_form)
          console.log("posting the data xl")
          fetch(`/edit-category/${category_id}`, {
            method: "POST",
            body: docFormData,
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.status) {
                popups.showSuccessPopup()
  
                setTimeout(() => {
                  popups.closeSuccessPopup();
                  window.location.href = '/upload_document';
                }, 2000);
              } else {
                document.getElementById('documentCategoryError').textContent = data.message;
                setTimeout(() => {
                  document.getElementById('documentCategoryError').textContent = '';
                }, 2000);
                document.getElementById('documentCategory').scrollIntoView();
  
              }
            })
            .catch((error) => {
              console.error("Error:", error);
            });
      }
    }
  })


function checkJsontype(extraction_string, conversion_string = null) {
  if (extraction_string != null) {
    try {
      JSON.parse(extraction_string);
    } catch (error) {
      console.log("error while parsing extraction string", error);
      pdfextractionOntology.classList.add("is-invalid");
      pdfextractionOntology.classList.remove("is-valid");
      return false;
    }
    pdfextractionOntology.classList.add("is-valid");
    pdfextractionOntology.classList.remove("is-invalid");
  }
  try {
    JSON.parse(conversion_string);
  } catch (error) {
    console.log("error while parsing conversion string", error);
    pdfconversionOntology.classList.add("is-invalid");
    pdfconversionOntology.classList.remove("is-valid");
    return false;
  }
  pdfconversionOntology.classList.remove("is-invalid");
  pdfconversionOntology.classList.add("is-valid");
  return true;
}

