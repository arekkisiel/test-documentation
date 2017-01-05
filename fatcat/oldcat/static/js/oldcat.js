function searchFunction() {
    var idInput, sysReqInput, testUnitInput, testIdInput, implByInput, fileInput, filter, table, field, tr, i, k, filtered;
    idInput = document.getElementById("idInput").value.toUpperCase();
    sysReqInput = document.getElementById("sysReqInput").value.toUpperCase();
    testUnitInput = document.getElementById("testUnitInput").value.toUpperCase();
    testIdInput = document.getElementById("testIdInput").value.toUpperCase();
    implByInput = document.getElementById("implByInput").value.toUpperCase();
    fileInput = document.getElementById("fileInput").value.toUpperCase();

    filter = [idInput, sysReqInput, testUnitInput, testIdInput, implByInput, fileInput];
    table = document.getElementById("testCaseTable");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        filtered = false;
        for (k = 0; k < 6; k++){
            if(!filtered){
                field = tr[i].getElementsByTagName("td")[k];
                if (field) {
                    if (field.innerHTML.toUpperCase().indexOf(filter[k]) > -1) {
                        tr[i].style.display = "";
                    } else {
                        tr[i].style.display = "none";
                        filtered = true;
                    }
                }
            }
        }
    }
}


function pageTable(tableName){
    $(tableName).tablesorterPager({container: $("#pager")});
}

// Below you can find a code copy-pasted from bamana.js

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

    showEasterEgg : function(imgPath) {
        for ( i = 0; i < 50; i++) {
            $("<img/>", {
                src : imgPath,
                style : "position: absolute; height: 100px; width: 100px; z-index: 1001;",
                id : "ee" + i
            }).prependTo($("body"));
            EASTEREGG.animateBamana($("#ee" + i));
            EASTEREGG.rotateBamana($("#ee" + i));
        }
    }
};
