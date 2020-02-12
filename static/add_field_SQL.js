$(document).ready(function () {
        var max_fields = 10; //maximum input boxes allowed
        var wrapper = $(".input_fields_wrap_exp"); //Fields wrapper
        var add_button = $(".adicionaCampo"); //Add button ID

        var x = 0; //initial text box count
        $(add_button).click(function (e) { //on add input button click
            e.preventDefault();
            if (max_fields > x) { //max input box allowed
                x++; //text box increment
                $(wrapper).append(' '); //add input box
            }
        });
        $(wrapper).on("click", ".removeCampo", function (e) { //user click on remove text
            e.preventDefault();
            $(this).parent('div').remove();
            x--;
        });
    });
