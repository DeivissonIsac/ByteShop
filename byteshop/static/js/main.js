//document.addEventListener("DOMContentLoaded", function() {
//if (!localStorage.getItem('doNotShowModal')) {
//  var myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'), {
//    backdrop: 'static',
//    keyboard: false
//  });
//  myModal.show();
//}
//

//document.getElementById('doNotShowAgain').addEventListener('change', function() {
//  if (this.checked) {
//    localStorage.setItem('doNotShowModal', 'true');
//  } else {
//    localStorage.removeItem('doNotShowModal');
//  }
//});
//});

//Script de ver tudo e ocultar os produtos na tela de checkout.
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

//Script do valor maximo e minimo do Filtrar na pagina loja
document.getElementById("preco-minimo").addEventListener("input", function() {
    document.getElementById("min-value").textContent = this.value;
});

document.getElementById("preco-maximo").addEventListener("input", function() {
    const maxValueSpan = document.getElementById("max-value");
    const hiddenInput = document.getElementById("hidden-maximo");

    if (this.value >= 999) {
        maxValueSpan.textContent = "Máximo";
        hiddenInput.value = "maximo";
    } else {
        maxValueSpan.textContent = this.value;
        hiddenInput.value = this.value;
    }
});

//Script para mandar os paramentros da ordem pra url
var url = new URL(document.URL);
var items = document.getElementsByClassName("ordenar-item");
console.log(items);

for (i=0; i < items.length; i++){
    url.searchParams.set("ordem", items[i].name);
    items[i].href = url.href;
}

