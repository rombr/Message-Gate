var timestamp = 0; // new Date().getTime();
var prevKeyCode = 0; // for double enter send

/* Методы отправки сообщений */
var sendmode = {
    enter: true,
    doubleEnter: true
};

util = {
    isBlank: function(text) {
        var blank = /^\s*$/;
            return (text.match(blank) !== null);
        }
    };
 
    /* Получение новых сообщений */
var getMsg = function() {
    $.ajax({
        url: action_adr + "get",
        async: true,
        cache: false,
        type: "POST",
        timeout: get_timeout+ 5*1000,
        dataType: "json",
        data: {'timestamp': timestamp},                                         
        complete: function(){
            //
        },
        error: function(){                                              
            setTimeout(getMsg, get_interval_error);
            $.jGrowl("Ошибка получения новых сообщений! Повтор запроса через "+ get_interval_error / 1000 +" секунд.");
        },
        success: function(array){
            timestamp = array.timestamp?array.timestamp:timestamp;                                              
            if (array.messages){
                $.each(array.messages, function(i, el) {
                    // alert(i);
                    var d = new Date()
                    d.setTime(el.timestamp*1000)
                    
                    $('.msgbox-message').append('<div class="message-line user">'
                        +'<span class="user">'+el.user+' * <\/span>'
                        +'<span class="date">'+d.toLocaleString()+' * <\/span>'
                        +'<span class="chat-message">'+el.message+'<\/span>'
                        +'<\/div>');
                })};
            $('.msgbox-message').scrollTo('.message-line:last', 1000, {axis:'y'} );
            // $.jGrowl("Получены новые сообщения!");
            if (array.error) {
                $.jGrowl(array.error);
                this.error();
            }else{
                setTimeout(getMsg, get_interval_normal);
            };
        }
    });
};

/* Отправка сообщения */
var sendMsg = function(){                          
    // $("#msg2send").attr("value").replace("\n", "");
    var message = $("#msg2send").val();
    var nickname = $("#nickname").val();
    if (util.isBlank(message) || util.isBlank(nickname)) {                                
        $("#msg2send").val('').focus();
        $.jGrowl("Пустое сообщение!");
        return false;
    };
    
    // send msg
    $('.btnSend').hide();
    $.ajax({
        type: "POST",
        async: true,
        cache: false,
        dataType: "json",
        url: action_adr + "send",
        data: {
            "msg" : message,
            "user" : nickname
        },
        complete: function(){     
            $("#msg2send").val('').focus();                               
            $('#btnSend').show();
            // $.jGrowl("Complete!");
        },
        error: function(){
            $.jGrowl("При отправке сообщения возникла ошибка, попробуйте повторить!");
        },
        success: function(html){                                                
            $.jGrowl("Сообщение успешно отправлено!");
        }
    });
    return false;
};

/* Main */
$(document).ready( function() {
    // Запуск процесса получения новых сообщений
    $.jGrowl("Для тестирования необходимо добавить в Jabber: krd-app@appspot.com, и что-нибудь написать", { sticky: true});                     
    
    getMsg();
    /*
	 * $.ajax({ url: action_adr + "test", async: true, cache: false,
	 * type: "POST", dataType: "json", data: {'comment': 'test'},
	 * success: function(test){ $("#t_a").text(test.a);
	 * $("#t_operator").text(test.operator);
	 * $("#body").text(test.body); } });
	 */
                                
    // интерфейс
    $("#tabs").tabs();
    $("#accordion").accordion(
        { 
        collapsible: true,
        autoHeight: false,
        active: 1,// false,
        });
        
        /* For widget */
        
        /*
		 * $(".msgbox").addClass("ui-widget ui-widget-content
		 * ui-helper-clearfix ui-corner-all")
		 * .find(".msgbox-header") .addClass("ui-widget-header
		 * ui-corner-all") .prepend("<span class=\"ui-icon
		 * ui-icon-closethick\"><\/span>") .end()
		 * .find(".msgbox-content");
		 * 
		 * $(".msgbox-header .ui-icon").click(function() {
		 * $(this).parents(".msgbox:first").toggle(); });
		 */
        $("#messages").sortable({
                cursor: 'crosshair',
                opacity: 0.6,
        });
        
        // custom widget
        // $("#messages").msgbox({test: "Hello widget!!!"});

    /* Отправка сообщения */
    /* по кнопке */
    $('#send').submit(sendMsg);
    
    /* фокусировка */
    $("#msg2send").val('').focus();

    /* по клавишам */
    if (sendmode.enter) $("#msg2send").keypress(function (e) {
        if (e.keyCode != 13) {prevKeyCode = e.keyCode; return;};
        if (prevKeyCode != 13 && sendmode.doubleEnter) {
            prevKeyCode = e.keyCode;
        } else {                                    
            prevKeyCode = 0;
            sendMsg();
        };
    });
});