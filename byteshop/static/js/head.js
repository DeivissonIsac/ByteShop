document.addEventListener("DOMContentLoaded", function () {
    let alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert, index) => {
        setTimeout(() => {
            alert.classList.add('show-alert');
        }, 200 * index);
        setTimeout(() => {
            alert.classList.remove('show-alert');
            setTimeout(() => alert.remove(), 500);
        }, 3000 + (200 * index));
    });
});