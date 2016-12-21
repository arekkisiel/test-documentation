var EASTEREGG = {

    animateBamana : function(o) {
        var h = $(window).height() - 150;
        var w = $(window).width() - 150;

        var nh = Math.floor(Math.random() * h);
        var nw = Math.floor(Math.random() * w);

        o.animate({
            top : nh,
            left : nw
        }, Math.floor(500 + 3000 * Math.random()), function() {
            EASTEREGG.animateBamana(o);
        });
    },

    rotateBamana : function(o) {
        o.css("border-spacing", 0);
        o.animate({
            borderSpacing : 360
        }, {
            queue : false,
            step : function(now, fx) {
                $(this).css('-webkit-transform', 'rotate(' + now + 'deg)');
                $(this).css('-ms-transform', 'rotate(' + now + 'deg)');
                $(this).css('transform', 'rotate(' + now + 'deg)');
            },
            duration : Math.floor(500 + 3000 * Math.random()),
            done : function() {
                EASTEREGG.rotateBamana(o);
            }
        }, 'linear');
    },

    showEasterEgg : function() {
        for ( i = 0; i < 50; i++) {
            $("<img/>", {
                src : "bamana.png",
                style : "position: absolute; height: 100px; width: 100px; z-index: 1001;",
                id : "ee" + i
            }).prependTo($("body"));
            EASTEREGG.animateBamana($("#ee" + i));
            EASTEREGG.rotateBamana($("#ee" + i));
        }
    }
};
