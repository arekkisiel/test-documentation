var BAMANA = {
    table : {},

    drawTable : function() {
        BAMANA.table = $('#baselineTable').dataTable({
            "lengthMenu" : [[10, 50, 150, -1], [10, 50, 150, "All"]],
            "ajax" : {
                "url" : CONFIG.ACCESS_POINT_WS + "/info",
                "dataSrc" : ""
            },
            "autoWidth": false,
            "columns" : [{
                "data" : null,
                "render" : function(data, type, row) {
                    return $("<input>", {
                        type : "checkbox",
                        checked : data.published,
                        id : "pubchk_" + data.continent + data.version,
                        disabled : true
                    }).prop("outerHTML");
                },
                "orderable" : false
            }, {
                "data" : "continent"
            }, {
                "data" : "version"
            }, {
                "data" : "branch"
            }, {
                "data" : "journalVersion"
            },{
                "data" : "currentVersion",
                "defaultContent" : "LOADING"
            }
            ],
            "fnInitComplete" : function() {
                BAMANA.renderCurrentVersion();
            }
        });
        $('input[type=search]').attr("id", "search_input");
    },

    renderCurrentVersion : function() {
        var data = $('#baselineTable').dataTable().fnGetData();

        for ( var i=0, ien=data.length ; i<ien ; i++ ) {

            var combinedPromise = $.when(BAMANA.checkCurrentVersion(data[i].branch), data[i], i);
            // Wait for every request.
            combinedPromise.done(function(data, json, i) {
                // json.currentVersion = data;
                $('#baselineTable').dataTable().fnUpdate(data, i, 5);
            });
        }
    },
    checkCurrentVersion : function(branch) {
        var def = new $.Deferred();
        var api = CONFIG.COREDB_MAIN_WS + "/journal/getCurrentVersion/" + branch;

        $.ajax({
            type : "GET",
            url : api,
            success : function(data) {
                if (data.status == "ERROR") {

                    BAMANA.showError("Error " + data.messagePayload.errorDetailedMessage);
                } else {
                    def.resolve(data.messagePayload.toString());
                }
            },
            error : function(jqXHR, textStatus, errorThrown) {
                var messageError = "Communication error " + jqXHR.status + " " + jqXHR.statusText;
                BAMANA.showError(messageError);
            },
            dataType : 'json',
            contentType : "*/**"
        });
        return def.promise();
    }
};


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
