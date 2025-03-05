//document.addEventListener("DOMContentLoaded", function() {
//// Verifica se o modal deve ser exibido
//if (!localStorage.getItem('doNotShowModal')) {
//  var myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'), {
//    backdrop: 'static',
//    keyboard: false
//  });
//  myModal.show(); // Mostra o modal
//}
//
//// Adiciona evento para checkbox
//document.getElementById('doNotShowAgain').addEventListener('change', function() {
//  if (this.checked) {
//    localStorage.setItem('doNotShowModal', 'true'); // Armazena no localStorage
//  } else {
//    localStorage.removeItem('doNotShowModal'); // Remove do localStorage
//  }
//});
//});

document.addEventListener("DOMContentLoaded", function() {
    const toggleBtn = document.getElementById('toggle-visibility');
    let expanded = false;

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            document.querySelectorAll('.produto-item[data-index]').forEach((el, index) => {
                if (index >= 2) {
                    el.classList.toggle('d-none');
                }
            });
            expanded = !expanded;
            toggleBtn.textContent = expanded ? "Ocultar" : "Ver Tudo";
        });
    }
});