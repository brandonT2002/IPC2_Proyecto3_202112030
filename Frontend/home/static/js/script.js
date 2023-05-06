function downloadPDF1() {
    var element = document.getElementById('dotR1');
    var doc = new jsPDF();
    var text = element.innerText.trim();
    doc.text(text,10,10);
    doc.save('Probabilidades.pdf');
}

function downloadPDF2() {
    var element = document.getElementById('dotR2');
    var doc = new jsPDF();
    var text = element.innerText.trim();
    doc.text(text,10,10);
    doc.save('Pesos.pdf');
}