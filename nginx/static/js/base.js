'use strict';

$('#container').ready(function(){
    $("#container").corner("19px");
    $(".dropdown").corner("13px");
});

$('#menu').ready(function(){
    
    if(!$.browser.msie){
        $(".dropdown > li:first").corner("13px tl bl");
        $(".dropdown > li:last").corner("13px tr br");
    }
    var max = 0;
    var count = 0;
    var width = $(".dropdown").innerWidth();
    $("ul.dropdown li").hover(function(){
        $(this).addClass("hover");
        $('ul:first',this).css('visibility', 'visible');
    }, function(){
        $(this).removeClass("hover");
        $('ul:first',this).css('visibility', 'hidden');
    });
    
    $("ul.dropdown li ul li:has(ul)").find("a:first").append(" &raquo; ");

    $(".dropdown > li").each(function(){
        max += $(this).outerWidth();
        count++;
    });
    var bump = (width - max) / count;
    $(".dropdown > li").each(function(){
        //$(this).css("padding", "0px "+bump/2+"px");
        var ratio = $(this).outerWidth() / max * 100;
        $(this).css("width", ""+ratio+"%");
    });
});