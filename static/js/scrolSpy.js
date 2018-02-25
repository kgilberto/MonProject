$(document).ready(function () {
    $(document).on("scroll", onScroll);

    $('.navbar-nav a[href^="#"]').on('click', function (e) {
        e.preventDefault();
        $(document).off("scroll");

        $('li').each(function () {
            $(this).removeClass('active');
        });
        $(this).addClass('active');
        var target = this.hash;
        $('html, body').stop().animate({
            'scrollTop': $(target).offset().top +1
        }, 500, 'swing', function () {
            window.location.hash = target;
            $(document).on("scroll", onScroll);
        });
        $(document).on("scroll", onScroll);
    });
});

function onScroll(event) {
    var scrollPosition = $(document).scrollTop();
    $('.nav a').each(function () {
        var currentLink = $(this);
        var refElement = $(currentLink.attr("href"));
        var parent = currentLink.parent();
        if (refElement.position().top <= scrollPosition && refElement.position().top + refElement.height() > scrollPosition) {
            $('.nav ul li').removeClass("active");
            parent.addClass("active");
        }
        else {
            parent.removeClass("active");
        }
    });
}


