const mobileBreakpoint = window.matchMedia("(max-width: 991px)");

$(document).ready(function(){
    // Handle dropdown toggle
    $(".dash-nav-dropdown-toggle").click(function(){
        $(this).closest(".dash-nav-dropdown")
            .toggleClass("show")
            .find(".dash-nav-dropdown")
            .removeClass("show");

        $(this).parent()
            .siblings()
            .removeClass("show");
    });

    // Handle menu toggle based on screen size
    $(".menu-toggle").click(function(){
        if (mobileBreakpoint.matches) {
            $(".dash-nav").toggleClass("mobile-show");
        } else {
            $(".dash-nav").toggleClass("dash-compact");
        }
    });

    // Handle search box toggle
    $(".searchbox-toggle").click(function(){
        $(".searchbox").toggleClass("show");
    });

    // Dev utilities (Optional: Automatically toggles the sidebar and search box for testing)
    // $("header.dash-toolbar .menu-toggle").click();
    // $(".searchbox-toggle").click();
});
