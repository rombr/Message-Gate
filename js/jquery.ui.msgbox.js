var msgbox  = {
    _init: function() {
    	//this.addBox(this);
        //alert(this.options.test);
    }, // grab the default value and use it
    
    addBox: function() {
    	this.element.append("<div class=\"msgbox\">"
    	   +"<div class=\"msgbox-header\">"
    	   +"<span class=\"ui-icon ui-icon-closethick\"><\/span>"
    	   +"widget header</div>"
    	   +"<div class=\"msgbox-content\">"
    	   +"<div class=\"msgbox-message\">Lorem ipsum dolor sit amet, consectetuer adipiscing elit</div>"
    	   +"<div class=\"msgbox-form\">"
    	   +"<form class=\"send\" action=\"/\" method=\"post\">"
    	   +"<div><textarea name=\"msg2send\" class=\"msg2send\" rows=\"3\" cols=\"20\"></textarea></div>"
    	   +"<div><input  class=\"btnSend\" type=\"submit\" value=\"Отправить\"/></div>"
    	   +"</form>"
    	   +"</div>"
    	   +"</div>"
    	   +"</div>");
        $(".msgbox").addClass("ui-widget ui-widget-content ui-helper-clearfix ui-corner-all")
            .find(".msgbox-header")
                .addClass("ui-widget-header ui-corner-all");

        $(".msgbox-header .ui-icon").click(function() {
            $(this).parents(".msgbox:first").toggle();
        });
        //form
        var w = this;
        $('.send').submit(function(){ 
        	//send msg
        	$.ajax({   
                type: "POST", 
                cache: false,
                dataType: "html",  
                //contentType: "application/x-www-form-urlencoded".
                url: "/area/operators/op1/ajax/test",   
                data: {
                    "msg" : $(this).find(".msg2send").val()
                },   
                success: function(html){    
                    w.addBox(); 
                    }   
                });   
        	return false;
        });
    },
    
    off: function() {
        this.element.css({background: 'none'});
        this.destroy(); // use the predefined function
    }
};
$.widget("ui.msgbox", msgbox);
//$.ui.msgbox.getter = "getLevel";
$.ui.msgbox.defaults = {
	test: 'Message',
};