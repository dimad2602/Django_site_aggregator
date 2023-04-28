$("button#Infobtn").click(function () {
    let textHTML = '<span id="AddRegInfo"> Зарегистрировавшись на нашем сайте вы... полезная информация</span>'
    const el = $(this).parent().next();
    el.append(textHTML)
    $('div.container').append(
        textHTML//"<span id='AddRegInfo'> Зарегистрировавшись на нашем сайте вы сможете следить за прогрессом прохождения своих, всё это будет сохраняться у нас, и доступно вам в любой момент. </span>"
    );
    document.getElementById("Infobtn").disabled = true;
});

