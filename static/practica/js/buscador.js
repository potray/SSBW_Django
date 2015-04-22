$(document).ready(function(){
    $("#preloader").css("display", "none");
    $( "#actualizarNoticias" ).click(function(){

        //Necesario para Django
        var csrftoken = $.cookie('csrftoken');

        $.ajax({
            url:"/practica/actualizarNoticias",
            context: document.body,
            data: {'borrar': 'false'},
            dataType: "JSON",
            method: "GET",
            beforeSend: function(xhr, settings){
                    //Mostrar preloader y ocultar noticias
                    $("#preloader").css("display", "block");
                    $("#noticias").css("display", "none");
                    console.log("Enviando");
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
            success: function(response){
                var tarjetas = ""

                $.each(response.noticias, function (index, element){
                    var elementoParseado = $.parseJSON(element);
                    var tarjeta = "<div class='card indigo darken-4'><div class='card-content white-text'><span class='card-title'>"+elementoParseado.titulo+
                                   "</span><p>"+elementoParseado.descripcion+
                                   "</p><p>"+elementoParseado.fecha+
                                   "</p></div><div class='card-action'><a href='"+elementoParseado.enlace+
                                   "'>Ir a la noticia</a></div></div>";

                    tarjetas += tarjeta;

                });

                //Ocultar preloader, mostrar y rellenar noticias
                $("#preloader").css("display", "none");
                $("#noticias").css("display", "block");
                $("#noticias").html(tarjetas);

                var noticiasCreadas = response.insertadas;

                $("#textoModal").html("Se han insertado "+noticiasCreadas+" noticias nuevas.");
                $("#modal").openModal();

            }
        });
    });
});
