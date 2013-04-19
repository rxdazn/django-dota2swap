$(document).ready(function() {

    // prev page
    $('#page_prev').click(function() {
        var current_page = $('.item_page').filter(":visible")
        var prev_page = current_page.prev("div.item_page");
        if (prev_page.length) {
            current_page.fadeOut("slow");
            current_page.css("display", "none");
            prev_page.fadeIn("fast");
        } else {
            // first page
            current_page.fadeOut("slow");
            current_page.css("display", "none");
            $(".item_page:last").fadeIn("fast");
        }

    });

    // next page
    $('#page_next').click(function() {
        var current_page = $('.item_page').filter(":visible")
        var next_page = current_page.nextAll("div.item_page:first");
        if (next_page.length) {
            current_page.fadeOut("slow");
            current_page.css("display", "none");
            next_page.fadeIn("fast");
        } else {
            // last page
            current_page.fadeOut("slow");
            current_page.css("display", "none");
            $(".item_page:first").fadeIn("fast");
        }

    });

    $('.item_holder').popover({ trigger: "hover" });
    $('.item_holder').popover.show();
});
