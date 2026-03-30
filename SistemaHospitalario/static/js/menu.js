document.addEventListener("DOMContentLoaded", function () {
    var banner = document.querySelector('#bannerHospital');
    var carousel = new bootstrap.Carousel(banner, {
        interval: 3000,   // tiempo entre slides (ms)
        ride: 'carousel', // arranca automáticamente
        pause: 'hover'    // se pausa al pasar el mouse
    });
});
