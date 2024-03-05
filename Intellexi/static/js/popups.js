 
export function showSuccessPopup() {
    document.getElementById('successPopup').style.display = 'block';
}

export function closeSuccessPopup() {
    document.getElementById('successPopup').style.display = 'none';
    window.location.href='/upload_document'
}
      