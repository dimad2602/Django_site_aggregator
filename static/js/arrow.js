$('.js-scroll-top').click(function (){
    $('html,body').animate({
      scrollTop: 0
    }, 1000);
});

$(window).scroll(function (){
    // $(window).scrollTop();

    if ($(window).scrollTop() > 5) {
        $('.js-scroll-top').addClass('is-show')
    }
    else{
        $('.js-scroll-top').removeClass('is-show')
    }
});

$('.js-how-scroll').click(function (){
    $('html,body').animate({
      scrollTop: 200
    }, 500);
    $('html,body').animate({
      scrollTop: 0
    }, 500);
});

// $(window).scroll(function (){
//     if ($(window).scrollTop() > 5){
//         $('.js-how-scroll').addClass('is-show')
//     }
//     else{
//         $('.js-how-scroll').removeClass('is-show')
//     }
// });

$(document).ready(function () {
    var height_document = $(document).height();
    var height_client = document.body.clientHeight;

    if(height_document > height_client) {
        // alert('огого');
        $('.js-how-scroll').removeClass('is-show')
    }
    else{
        $('.js-how-scroll').addClass('is-show')

    }
});